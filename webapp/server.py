"""
webapp/server.py - note-article-system Web UI サーバー

ブラウザのチャット画面から claude CLI をヘッドレス起動し、
CLAUDE.md のメニュー / 記事生成フローを Web アプリとして操作する。

使い方:
  python webapp/server.py
  → ブラウザで http://127.0.0.1:8788 を開く

仕組み:
  - メッセージごとに `claude -p --output-format stream-json` を起動
  - 2回目以降は `--resume <session_id>` で会話を継続
  - 出力を NDJSON でブラウザにストリーミング
  - テーマ(themes.json) / 記事(articles/) / ログインは専用 API で操作
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from flask import Flask, Response, request, send_from_directory

BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent  # claude の作業ディレクトリ = プロジェクトルート

HOST = "127.0.0.1"  # ローカル専用。外部公開しないこと
PORT = 8788         # AUTO-content-system(8787) と被らないようにずらす

# Windows コンソール文字化け対策
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def find_claude():
    """claude CLI の場所を探す。

    毎回呼び直すので、サーバー起動後に claude をインストールした場合でも
    サーバーを再起動せずに認識される。
    npm のグローバル bin が PATH に入っていない環境もあるため、
    よくあるインストール先も併せて確認する。
    """
    found = shutil.which("claude")
    if found:
        return found

    candidates = []
    if sys.platform == "win32":
        for var in ("APPDATA", "LOCALAPPDATA", "ProgramFiles"):
            base = os.environ.get(var)
            if base:
                candidates.append(Path(base) / "npm" / "claude.cmd")
    else:
        home = Path.home()
        candidates += [
            home / ".local" / "bin" / "claude",
            home / ".npm-global" / "bin" / "claude",
            home / ".claude" / "local" / "claude",
            Path("/usr/local/bin/claude"),
            Path("/opt/homebrew/bin/claude"),
        ]

    for c in candidates:
        try:
            if c.is_file():
                return str(c)
        except OSError:
            continue
    return None


CLAUDE_BIN = find_claude()
PY_BIN = sys.executable or shutil.which("python") or "python"

# --model に渡せるモデルの許可リスト（UIのドロップダウンと対応）
ALLOWED_MODELS = {
    "claude-fable-5",
    "claude-opus-4-8",
    "claude-sonnet-4-6",
    "claude-haiku-4-5",
}

# 動作モード → CLIの --permission-mode 値（"restricted" は許可リスト方式で別処理）
MODES = {
    "restricted": None,           # 許可リスト方式（既定・安全）
    "auto": "auto",               # 自動モード（CLIがよしなに判断）
    "full": "bypassPermissions",  # フルオート（確認なしで全実行）
    "plan": "plan",               # 計画モード（読み取りのみ・実行しない）
}

# フルオート（全許可）モードは環境変数 NAS_ALLOW_FULL=1 のときだけ有効。
# 既定では無効にして、Web経由の任意コマンド実行の穴を塞ぐ。
ALLOW_FULL = os.environ.get("NAS_ALLOW_FULL") == "1"

app = Flask(__name__)


def nd(obj) -> str:
    """NDJSON 1行分"""
    return json.dumps(obj, ensure_ascii=False) + "\n"


@app.get("/")
def index():
    return send_from_directory(BASE_DIR / "static", "index.html")


# ==============================
# フォルダ/ファイル ユーティリティ
# ==============================
def _safe_target(rel: str):
    """プロジェクト内に収まる絶対パスを返す。外に出る指定は ValueError。"""
    target = (PROJECT_DIR / rel.strip().strip("/\\")).resolve()
    target.relative_to(PROJECT_DIR.resolve())  # 範囲外なら ValueError
    return target


@app.post("/api/open-folder")
def api_open_folder():
    """OSのファイルマネージャ（Windows=エクスプローラー）でフォルダを開く。
    プロジェクト内のフォルダのみ許可する（任意パスは開かない）。"""
    data = request.get_json(force=True, silent=True) or {}
    rel = (data.get("path") or "").strip().strip("/\\")

    target = (PROJECT_DIR / rel).resolve() if rel else PROJECT_DIR.resolve()
    try:
        target.relative_to(PROJECT_DIR.resolve())
    except ValueError:
        return {"error": "プロジェクト外のフォルダは開けません"}, 400
    if not target.exists():
        return {"error": f"フォルダが見つかりません: {rel or '(ルート)'}"}, 404

    try:
        if sys.platform == "win32":
            os.startfile(str(target))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(target)])
        else:
            subprocess.Popen(["xdg-open", str(target)])
    except Exception as e:
        return {"error": f"フォルダを開けませんでした: {e}"}, 500
    return {"ok": True, "opened": str(target)}


# ==============================
# 記事ファイル解析（note_poster.py と同じロジックの軽量版）
# ==============================
def _parse_article(path: Path):
    """(title, char_count) を返す。"""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return path.stem, 0
    lines = text.splitlines()

    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("=" * 10) or line.startswith("＝" * 5):
            body_start = i + 1
            break
    body_lines = lines[body_start:]

    trimmed = []
    for line in body_lines:
        if "【終了】" in line:
            break
        trimmed.append(line)

    title = ""
    for line in trimmed:
        s = line.strip()
        if s.startswith("●"):
            title = s.lstrip("●").strip()
            break
    if not title:
        for line in lines[:3]:
            if line.startswith("テーマ："):
                title = line[4:].strip()[:60]
                break
    if not title:
        title = path.stem
    return title, len("\n".join(trimmed))


@app.get("/api/articles")
def api_articles():
    """articles/ (未投稿) と articles/posted/ (投稿済み) の一覧を返す。"""
    adir = PROJECT_DIR / "articles"
    pdir = adir / "posted"
    pending, posted = [], []
    if adir.is_dir():
        for p in sorted(adir.glob("*.txt"), key=lambda x: x.stat().st_mtime):
            title, chars = _parse_article(p)
            pending.append({"name": p.name, "title": title, "chars": chars,
                            "path": f"articles/{p.name}"})
    if pdir.is_dir():
        for p in sorted(pdir.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True):
            title, chars = _parse_article(p)
            posted.append({"name": p.name, "title": title, "chars": chars,
                           "path": f"articles/posted/{p.name}"})
    return {"pending": pending, "posted": posted}


@app.get("/api/themes")
def api_themes():
    """themes.json の pending / done を返す。"""
    tf = PROJECT_DIR / "themes.json"
    pending, done = [], []
    if tf.exists():
        try:
            data = json.loads(tf.read_text(encoding="utf-8") or "{}")
            pending = data.get("pending", []) or []
            done = data.get("done", []) or []
        except Exception:
            pass
    return {"pending": pending, "done": done}


@app.post("/api/themes-delete")
def api_themes_delete():
    """themes.json の pending から指定テーマ（文字列の配列）を削除する。"""
    data = request.get_json(force=True, silent=True) or {}
    targets = set(data.get("themes") or [])
    if not targets:
        return {"error": "削除対象がありません"}, 400
    tf = PROJECT_DIR / "themes.json"
    if not tf.exists():
        return {"error": "themes.json がありません"}, 404
    try:
        d = json.loads(tf.read_text(encoding="utf-8") or "{}")
    except Exception as e:
        return {"error": f"themes.json 読み込み失敗: {e}"}, 500
    pending = d.get("pending") or []
    kept = [t for t in pending if t not in targets]
    removed = len(pending) - len(kept)
    d["pending"] = kept
    d.setdefault("done", [])
    tf.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "removed": removed, "pending": kept, "done": d["done"]}


@app.post("/api/articles-delete")
def api_articles_delete():
    """記事 .txt（articles/ 直下・articles/posted/）を削除する。ローカルファイルのみ（note上の下書きは消えない）。"""
    data = request.get_json(force=True, silent=True) or {}
    paths = data.get("paths") or []
    if not paths:
        return {"error": "削除対象がありません"}, 400
    deleted = 0
    for rel in paths:
        try:
            t = _safe_target(rel)
        except ValueError:
            continue
        ok = (t.suffix == ".txt" and (
            t.parent.name == "articles"
            or (t.parent.name == "posted" and t.parent.parent.name == "articles")
        ))
        if ok and t.is_file():
            try:
                t.unlink()
                deleted += 1
            except Exception:
                pass
    return {"ok": True, "deleted": deleted}


@app.get("/api/read-file")
def api_read_file():
    rel = request.args.get("path", "")
    try:
        target = _safe_target(rel)
    except ValueError:
        return {"error": "プロジェクト外のファイルは読めません"}, 400
    if not target.is_file():
        return {"error": "ファイルが見つかりません"}, 404
    return {"content": target.read_text(encoding="utf-8", errors="replace")}


@app.post("/api/save-file")
def api_save_file():
    """記事 .txt（articles/ 直下・posted/）/ themes.json / prompt_knowledge の .txt・.md のみ編集を許可する。"""
    data = request.get_json(force=True, silent=True) or {}
    rel = data.get("path") or ""
    content = data.get("content")
    if content is None:
        return {"error": "内容がありません"}, 400
    try:
        target = _safe_target(rel)
    except ValueError:
        return {"error": "プロジェクト外のファイルは保存できません"}, 400

    is_article = (target.suffix == ".txt"
                  and (target.parent.name == "articles"
                       or (target.parent.name == "posted"
                           and target.parent.parent.name == "articles")))
    is_themes = target.name == "themes.json" and target.parent == PROJECT_DIR.resolve()
    kb_root = (PROJECT_DIR / "prompt_knowledge").resolve()
    is_knowledge = (target.suffix in (".txt", ".md") and kb_root in target.parents)
    if not (is_article or is_themes or is_knowledge):
        return {"error": "このファイルは編集できません"}, 403
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {"ok": True, "saved": str(target)}


# ==============================
# ナレッジ（筆者ルール / 記事構成）— カテゴリ別・複数管理・選択切替
# ==============================
KNOWLEDGE_DIR = PROJECT_DIR / "prompt_knowledge"

# カテゴリ定義（key=サブフォルダ名, label=表示名, ext=新規時の既定拡張子）
KB_CATS = {
    "筆者": {"label": "筆者ルール", "ext": ".txt"},
    "手順": {"label": "記事構成（手順）", "ext": ".md"},
}


def _cat_dir(cat):
    return KNOWLEDGE_DIR / cat if cat in KB_CATS else None


def _safe_kb_name(name: str):
    """カテゴリ内の .txt / .md ファイル名だけ許可。ディレクトリ移動・隠しファイルを防ぐ。"""
    name = (name or "").strip().strip("/\\")
    if not name or "/" in name or "\\" in name or name.startswith("."):
        return None
    if not (name.endswith(".txt") or name.endswith(".md")):
        return None
    return name


def _kb_title(p):
    """表示名はファイル名（拡張子なし）。ユーザーが付けた一意の名前で区別できるようにする。"""
    return p.stem


def _active_path(cat):
    d = _cat_dir(cat)
    return (d / ".active") if d else None


def _get_active(cat):
    """選択中ファイル名を返す。未設定/不正なら先頭ファイルにフォールバック。"""
    ap = _active_path(cat)
    if ap and ap.exists():
        v = ap.read_text(encoding="utf-8").strip()
        if v and (_cat_dir(cat) / v).is_file():
            return v
    d = _cat_dir(cat)
    if d and d.is_dir():
        for p in sorted(d.glob("*")):
            if p.is_file() and p.suffix in (".txt", ".md"):
                return p.name
    return ""


@app.get("/api/kb")
def api_kb_list():
    """カテゴリ（筆者 / 手順）のファイル一覧と選択中を返す。"""
    cat = (request.args.get("cat") or "").strip()
    d = _cat_dir(cat)
    if d is None:
        return {"error": "不正なカテゴリです"}, 400
    d.mkdir(parents=True, exist_ok=True)
    active = _get_active(cat)
    files = []
    for p in sorted(d.glob("*")):
        if not p.is_file() or p.suffix not in (".txt", ".md"):
            continue
        files.append({"name": p.name, "title": _kb_title(p),
                      "path": f"prompt_knowledge/{cat}/{p.name}",
                      "bytes": p.stat().st_size,
                      "active": p.name == active})
    return {"cat": cat, "label": KB_CATS[cat]["label"], "active": active, "files": files}


@app.get("/api/kb-cats")
def api_kb_cats():
    """カテゴリ一覧（表示名・選択中タイトル）を返す。ヘッダー表示用。"""
    out = []
    for cat, meta in KB_CATS.items():
        active = _get_active(cat)
        title = ""
        if active and (_cat_dir(cat) / active).is_file():
            title = _kb_title(_cat_dir(cat) / active)
        out.append({"cat": cat, "label": meta["label"],
                    "active": active, "active_title": title})
    return {"cats": out}


@app.post("/api/kb-new")
def api_kb_new():
    data = request.get_json(force=True, silent=True) or {}
    cat = (data.get("cat") or "").strip()
    d = _cat_dir(cat)
    if d is None:
        return {"error": "不正なカテゴリです"}, 400
    name = (data.get("name") or "").strip()
    if name and not (name.endswith(".txt") or name.endswith(".md")):
        name += KB_CATS[cat]["ext"]
    name = _safe_kb_name(name)
    if not name:
        return {"error": "ファイル名が不正です（.txt または .md）"}, 400
    d.mkdir(parents=True, exist_ok=True)
    target = d / name
    if target.exists():
        return {"error": "同名のファイルが既にあります"}, 409
    target.write_text(data.get("content") or "", encoding="utf-8")
    return {"ok": True, "name": name, "path": f"prompt_knowledge/{cat}/{name}"}


@app.post("/api/kb-delete")
def api_kb_delete():
    data = request.get_json(force=True, silent=True) or {}
    cat = (data.get("cat") or "").strip()
    d = _cat_dir(cat)
    if d is None:
        return {"error": "不正なカテゴリです"}, 400
    name = _safe_kb_name(data.get("name"))
    if not name:
        return {"error": "ファイル名が不正です"}, 400
    target = d / name
    if not target.is_file():
        return {"error": "ファイルが見つかりません"}, 404
    remaining = [p for p in d.glob("*") if p.is_file() and p.suffix in (".txt", ".md")]
    if len(remaining) <= 1:
        return {"error": "最後の1件は削除できません（参照先が無くなるため）"}, 400
    target.unlink()
    ap = _active_path(cat)
    if ap.exists() and ap.read_text(encoding="utf-8").strip() == name:
        ap.write_text(_get_active(cat), encoding="utf-8")
    return {"ok": True, "deleted": name}


@app.post("/api/kb-rename")
def api_kb_rename():
    data = request.get_json(force=True, silent=True) or {}
    cat = (data.get("cat") or "").strip()
    d = _cat_dir(cat)
    if d is None:
        return {"error": "不正なカテゴリです"}, 400
    old = _safe_kb_name(data.get("old"))
    new = (data.get("new") or "").strip()
    if new and not (new.endswith(".txt") or new.endswith(".md")):
        new += KB_CATS[cat]["ext"]
    new = _safe_kb_name(new)
    if not old or not new:
        return {"error": "ファイル名が不正です"}, 400
    src, dst = d / old, d / new
    if not src.is_file():
        return {"error": "元ファイルが見つかりません"}, 404
    if dst.exists():
        return {"error": "同名のファイルが既にあります"}, 409
    src.rename(dst)
    ap = _active_path(cat)
    if ap.exists() and ap.read_text(encoding="utf-8").strip() == old:
        ap.write_text(new, encoding="utf-8")
    return {"ok": True, "name": new, "path": f"prompt_knowledge/{cat}/{new}"}


@app.post("/api/kb-active")
def api_kb_active():
    """このカテゴリで参照する（記事生成時に使う）ファイルを選択中にする。"""
    data = request.get_json(force=True, silent=True) or {}
    cat = (data.get("cat") or "").strip()
    d = _cat_dir(cat)
    if d is None:
        return {"error": "不正なカテゴリです"}, 400
    name = _safe_kb_name(data.get("name"))
    if not name or not (d / name).is_file():
        return {"error": "ファイルが見つかりません"}, 404
    _active_path(cat).write_text(name, encoding="utf-8")
    return {"ok": True, "active": name}


# ==============================
# Obsidian フォルダ閲覧・指定
# ==============================
def _load_project_config():
    try:
        return json.loads((PROJECT_DIR / "config.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def _obsidian_root():
    cfg = _load_project_config()
    raw = (cfg.get("obsidian_vault_path") or "").strip()
    if not raw or raw == "あなたのobsidianフォルダ":
        return None, raw
    p = Path(raw)
    return (p if p.is_dir() else None), raw


@app.get("/api/obsidian")
def api_obsidian():
    """Obsidian Vault 配下のサブフォルダ・.md一覧を返す（rel でドリルダウン）。"""
    root, raw = _obsidian_root()
    if root is None:
        return {"configured": False, "root": raw}
    rel = (request.args.get("rel") or "").strip().strip("/\\")
    try:
        target = (root / rel).resolve()
        target.relative_to(root.resolve())   # Vault 外へ出る指定を拒否
    except Exception:
        return {"error": "Vault範囲外のフォルダです"}, 400
    if not target.is_dir():
        return {"error": "フォルダが見つかりません"}, 404
    folders, files = [], []
    try:
        for p in sorted(target.iterdir()):
            if p.name.startswith("."):
                continue
            if p.is_dir():
                md = sum(1 for _ in p.glob("*.md"))
                folders.append({"name": p.name, "md": md})
            elif p.suffix.lower() == ".md":
                files.append({"name": p.name})
    except Exception as e:
        return {"error": f"読み込み失敗: {e}"}, 500
    return {"configured": True, "root": str(root), "rel": rel,
            "abs": str(target), "folders": folders, "files": files}


@app.post("/api/obsidian-config")
def api_obsidian_config():
    """Obsidian Vault のパスを config.json に保存する。"""
    data = request.get_json(force=True, silent=True) or {}
    p = (data.get("path") or "").strip().strip('"')
    if not p or not Path(p).is_dir():
        return {"error": "そのフォルダは存在しません"}, 400
    cfg = _load_project_config()
    cfg["obsidian_vault_path"] = p
    (PROJECT_DIR / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "path": p}


@app.get("/api/accounts")
def api_accounts():
    """投稿アカウント一覧と選択中を返す。"""
    cfg = _load_project_config()
    accounts = cfg.get("accounts") or {}
    active = cfg.get("active_account", "")
    if not active and accounts:
        active = next(iter(accounts))
    return {"active": active,
            "accounts": [{"name": k, "pen_name": (v or {}).get("pen_name", "")}
                         for k, v in accounts.items()]}


@app.post("/api/account-switch")
def api_account_switch():
    """active_account を切り替える。"""
    data = request.get_json(force=True, silent=True) or {}
    name = (data.get("name") or "").strip()
    cfg = _load_project_config()
    if name not in (cfg.get("accounts") or {}):
        return {"error": "そのアカウントがありません"}, 404
    cfg["active_account"] = name
    (PROJECT_DIR / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "active": name}


@app.post("/api/account-add")
def api_account_add():
    """新しいアカウントを追加して選択中にする（chrome_data_dir を自動採番）。"""
    data = request.get_json(force=True, silent=True) or {}
    name = (data.get("name") or "").strip()
    pen = (data.get("pen_name") or "").strip()
    if not name or "/" in name or "\\" in name:
        return {"error": "アカウント名が不正です"}, 400
    cfg = _load_project_config()
    cfg.setdefault("accounts", {})
    if name in cfg["accounts"]:
        return {"error": "同名のアカウントが既にあります"}, 409
    cfg["accounts"][name] = {"chrome_data_dir": f"chrome_data_{name}", "pen_name": pen}
    cfg["active_account"] = name
    (PROJECT_DIR / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "active": name}


def _note_scraper():
    """note_scraper モジュールを遅延インポート（プロジェクト直下）。"""
    import importlib
    if str(PROJECT_DIR) not in sys.path:
        sys.path.insert(0, str(PROJECT_DIR))
    return importlib.import_module("note_scraper")


@app.get("/api/reactions")
def api_reactions():
    """note の自分の記事のスキ数を集計して返す（反応分析）。"""
    urlname = (request.args.get("urlname") or "").strip().strip("@/ ")
    if not urlname:
        urlname = (_load_project_config().get("note_urlname") or "").strip()
    if not urlname:
        return {"configured": False}
    try:
        data = _note_scraper().reactions(urlname)
    except Exception as e:
        return {"error": f"取得失敗: {e}"}, 500
    return {"configured": True, **data}


@app.post("/api/reactions-config")
def api_reactions_config():
    """反応分析の対象 note ユーザー名を config.json に保存。"""
    data = request.get_json(force=True, silent=True) or {}
    u = (data.get("urlname") or "").strip().strip("@/ ")
    if not u:
        return {"error": "note のユーザー名を入力してください"}, 400
    cfg = _load_project_config()
    cfg["note_urlname"] = u
    (PROJECT_DIR / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "urlname": u}


@app.get("/api/format-config")
def api_format_config_get():
    """note投稿の整形設定（空行・折返し）を返す。"""
    cfg = _load_project_config()
    return {
        "blank_lines": cfg.get("blank_lines", 2),
        "blank_every": cfg.get("blank_every", 2),
        "line_wrap": cfg.get("line_wrap", ""),   # "" = 整形ルール.md に従う
    }


@app.post("/api/format-config")
def api_format_config_set():
    """note投稿の整形設定を config.json に保存する。"""
    data = request.get_json(force=True, silent=True) or {}
    cfg = _load_project_config()
    bl = data.get("blank_lines")
    if isinstance(bl, int) and 1 <= bl <= 5:
        cfg["blank_lines"] = bl
    be = data.get("blank_every")
    if isinstance(be, int) and 1 <= be <= 8:
        cfg["blank_every"] = be
    lw = data.get("line_wrap")
    if lw == "none":
        cfg["line_wrap"] = "none"          # 折り返しなし
    elif lw in (None, "", 0, "0"):
        cfg.pop("line_wrap", None)         # 整形ルール.md に従う
    else:
        try:
            lw = int(lw)
            if 10 <= lw <= 40:
                cfg["line_wrap"] = lw
        except Exception:
            pass
    (PROJECT_DIR / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True,
            "blank_lines": cfg.get("blank_lines", 2),
            "blank_every": cfg.get("blank_every", 2),
            "line_wrap": cfg.get("line_wrap", "")}


@app.post("/api/pick-folder")
def api_pick_folder():
    """OSのネイティブ「フォルダを開く」ダイアログを出し、選ばれた絶対パスを返す。
    Flask スレッドでの Tk 不具合を避けるため、別プロセスで tkinter を起動する。"""
    code = (
        "import tkinter as tk\n"
        "from tkinter import filedialog\n"
        "r = tk.Tk(); r.withdraw()\n"
        "try:\n"
        "    r.attributes('-topmost', True)\n"
        "except Exception:\n"
        "    pass\n"
        "p = filedialog.askdirectory(title='記事化するフォルダを選択')\n"
        "print(p or '')\n"
    )
    try:
        proc = subprocess.run(
            [PY_BIN, "-c", code],
            cwd=str(PROJECT_DIR), text=True, encoding="utf-8",
            errors="replace", timeout=300, capture_output=True,
        )
    except subprocess.TimeoutExpired:
        return {"error": "フォルダ選択がタイムアウトしました"}, 504
    except Exception as e:
        return {"error": f"フォルダ選択ダイアログを開けませんでした: {e}"}, 500
    if proc.returncode != 0:
        err = (proc.stderr or "").strip().splitlines()[-1:] or ["不明なエラー"]
        return {"error": f"ダイアログ起動失敗: {err[0]}"}, 500
    path = (proc.stdout or "").strip()
    if not path:
        return {"ok": True, "cancelled": True}
    return {"ok": True, "path": path}


# ==============================
# 環境ステータス & ログイン
# ==============================
@app.get("/api/status")
def api_status():
    """環境チェック（Python / Chrome / パッケージ / note.comログイン状態）。"""
    def _chrome_ver():
        path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        try:
            if os.path.exists(path):
                import subprocess as sp
                out = sp.check_output([
                    "powershell", "-command",
                    f"(Get-Item '{path}').VersionInfo.ProductVersion"
                ], text=True, encoding="utf-8", errors="replace").strip()
                return out or None
        except Exception:
            return None
        return None

    # パッケージ確認
    pkg_ok = True
    for mod in ("selenium", "PIL", "psutil"):
        try:
            __import__(mod)
        except Exception:
            pkg_ok = False
            break

    # ログイン状態（config の chrome_data_dir にプロファイルがあるか）
    cfg = {}
    try:
        cfg = json.loads((PROJECT_DIR / "config.json").read_text(encoding="utf-8"))
    except Exception:
        pass
    accounts = cfg.get("accounts", {})
    active = cfg.get("active_account", "")
    acct = accounts.get(active) or (next(iter(accounts.values()), {}) if accounts else {})
    data_dir = acct.get("chrome_data_dir", "cloned_chrome_data")
    logged_in = (PROJECT_DIR / data_dir).is_dir()

    return {
        "python": sys.version.split()[0],
        "chrome": _chrome_ver(),
        "packages_ok": pkg_ok,
        "claude_cli": bool(find_claude()),
        "logged_in": logged_in,
        "active_account": active,
    }


@app.post("/api/login")
def api_login():
    """note.com ログイン窓を起動する（note_poster.py --login をバックグラウンド実行）。"""
    poster = PROJECT_DIR / "note_poster.py"
    if not poster.exists():
        return {"error": "note_poster.py が見つかりません"}, 404
    try:
        subprocess.Popen(
            [PY_BIN, str(poster), "--login"],
            cwd=str(PROJECT_DIR),
        )
    except Exception as e:
        return {"error": f"ログイン窓を起動できませんでした: {e}"}, 500
    return {"ok": True, "message": "ログイン専用Chromeを起動しました。開いた窓でnote.comにログインしてください（完了で自動的に閉じます）。"}


# ==============================
# チャット（claude CLI ストリーミング）
# ==============================
@app.post("/api/send")
def api_send():
    data = request.get_json(force=True)
    message = (data.get("message") or "").strip()
    session_id = data.get("session_id") or None
    model = data.get("model") or None
    mode = data.get("mode") or "restricted"

    if not message:
        return {"error": "メッセージが空です"}, 400
    if model and model not in ALLOWED_MODELS:
        return {"error": f"未対応のモデルです: {model}"}, 400
    if mode not in MODES:
        return {"error": f"未対応のモードです: {mode}"}, 400
    if mode == "full" and not ALLOW_FULL:
        return {"error": (
            "フルオートモードは既定で無効です。有効化するには、サーバーを "
            "NAS_ALLOW_FULL=1 を設定して起動してください"
            "（start_webapp.bat はこれを自動設定します）。"
            "※確認なしで全コマンドを実行するため、信頼できる作業のみで使用してください。"
        )}, 403
    claude_bin = find_claude()
    if not claude_bin:
        return {"error": (
            "claude CLI が見つかりません。"
            "Node.js を入れたうえで `npm install -g @anthropic-ai/claude-code` を実行してください。"
            "インストール済みなのにこの表示が出る場合は、claude が PATH に無い可能性があります"
            "（コマンドプロンプトで `where claude` を実行して確認してください）。"
        )}, 500

    cmd = [
        claude_bin, "-p",
        "--output-format", "stream-json",
        "--verbose",
    ]

    if mode == "restricted":
        # 制限モード: 記事生成フローに必要なツールだけを許可する
        allowed_tools = ",".join([
            "Read", "Write", "Edit", "Glob", "Grep",      # プロジェクト内のファイル操作
            "WebSearch", "WebFetch",                       # 売れ筋・市場リサーチ
            "Task", "TodoWrite", "Skill",                  # サブエージェント・進捗・スキル
            "Bash(python:*)",                              # note_poster.py / note_scraper.py / generate_pdf.py
            "Bash(mkdir:*)", "Bash(ls:*)", "Bash(cat:*)",  # フォルダ作成・確認
        ])
        cmd += ["--allowedTools", allowed_tools]
    else:
        cmd += ["--permission-mode", MODES[mode]]
        if mode == "full":
            cmd += ["--allow-dangerously-skip-permissions"]

    if model:
        cmd += ["--model", model]
    if session_id:
        cmd += ["--resume", session_id]
    # メッセージは stdin で渡す

    def generate():
        proc = subprocess.Popen(
            cmd,
            cwd=str(PROJECT_DIR),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        proc.stdin.write(message)
        proc.stdin.close()
        sid = session_id
        got_result = False
        noise = []
        try:
            for raw in proc.stdout:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    ev = json.loads(raw)
                except json.JSONDecodeError:
                    if len(noise) < 50:
                        noise.append(raw)
                    continue

                etype = ev.get("type")
                if etype == "system" and ev.get("subtype") == "init":
                    sid = ev.get("session_id", sid)
                    yield nd({"type": "session", "session_id": sid})
                elif etype == "assistant":
                    for block in (ev.get("message") or {}).get("content", []):
                        if block.get("type") == "text" and block.get("text"):
                            yield nd({"type": "text", "text": block["text"]})
                        elif block.get("type") == "tool_use":
                            yield nd({"type": "tool", "name": block.get("name", "")})
                elif etype == "result":
                    got_result = True
                    sid = ev.get("session_id", sid)
                    yield nd({
                        "type": "done",
                        "session_id": sid,
                        "ok": ev.get("subtype") == "success",
                    })

            proc.wait()
            if not got_result:
                tail = "\n".join(noise[-10:])
                yield nd({
                    "type": "error",
                    "message": f"claude が応答せず終了しました (exit {proc.returncode})\n{tail}",
                })
        except GeneratorExit:
            pass
        finally:
            if proc.poll() is None:
                proc.kill()

    return Response(generate(), mimetype="application/x-ndjson")


if __name__ == "__main__":
    print("=" * 60)
    print("  note-article-system Web UI")
    print(f"  http://{HOST}:{PORT} をブラウザで開いてください")
    print(f"  作業ディレクトリ: {PROJECT_DIR}")
    print(f"  claude CLI: {CLAUDE_BIN or '見つかりません（要インストール）'}")
    print("=" * 60)
    app.run(host=HOST, port=PORT, threaded=True)
