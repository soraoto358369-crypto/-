"""
article_formatter.py - 記事を「貼り付け用テキスト」に整形するスクリプト

よもぎ蒸しサロン記事生成システムでは、記事は articles/ に保存するだけで
自動投稿はしません。ブログ・UTAGE・Instagram などに貼り付けるときに、
読みやすい改行・空行に整えるのがこのスクリプトの役割です。

使い方:
  python article_formatter.py --list                 # 記事の一覧を表示
  python article_formatter.py --file articles/xxx.txt  # 整形して表示
  python article_formatter.py --file articles/xxx.txt --save  # _貼り付け用.txt を書き出す
  python article_formatter.py --all --save           # articles/ 直下すべてを書き出す

記事ファイル形式（articles/*.txt）:
  1行目  : テーマ：タイトル
  2行目  : 生成日時：...
  3行目  : ===...===
  4行目〜: 本文
           ●見出し   → 大見出し
           ＝＝＝＝＝ → スキップ
           【終了】   → ここで終端

整形の設定（config.json）:
  "line_wrap"   : 1行の折り返し文字数。"none" で折り返しなし。未設定なら整形ルール.md から読む
  "blank_every" : 何文ごとに空行を入れるか（既定 2）
  "blank_lines" : 区切りの空行を何本にそろえるか（既定 2）
"""

import re
import sys
import json
import argparse
from pathlib import Path

# Windows コンソール文字化け対策
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR     = Path(__file__).parent
CONFIG_FILE  = BASE_DIR / "config.json"
ARTICLES_DIR = BASE_DIR / "articles"


def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


# ==============================
# 記事ファイルの解析
# ==============================
def parse_article(path: Path) -> tuple[str, str]:
    """
    ファイルを解析して (title, body_text) を返す。
    - title: 最初の ●見出し テキスト（●を除去）
    - body : ===以降〜【終了】前 のテキスト
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    # ヘッダー行（テーマ:/生成日時:/===）をスキップ
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("=" * 10) or line.startswith("＝" * 5):
            body_start = i + 1
            break

    body_lines = lines[body_start:]

    # 【終了】で打ち切り
    trimmed = []
    for line in body_lines:
        if "【終了】" in line or line.strip() == "【終了】":
            break
        trimmed.append(line)

    # タイトル = 最初の ● 行（その行と直後の空行は本文から除外＝二重見出し防止）
    title = ""
    title_idx = -1
    for idx, line in enumerate(trimmed):
        stripped = line.strip()
        if stripped.startswith("●"):
            title = stripped.lstrip("●").strip()
            title_idx = idx
            break

    # タイトルが取れなかった場合はテーマ行から
    if not title:
        for line in lines[:3]:
            if line.startswith("テーマ："):
                raw = line[4:].strip()
                raw = re.sub(r"^\[.*?\]\s*@\S+:\s*", "", raw)
                title = raw[:60]
                break

    if title_idx >= 0:
        rest = trimmed[title_idx + 1:]
        while rest and not rest[0].strip():   # タイトル直後の空行も除去
            rest.pop(0)
        body_text = "\n".join(rest)
    else:
        body_text = "\n".join(trimmed)
    return title, body_text


# ==============================
# 整形（折り返し・空行）
# ==============================
def _wrap_width() -> int:
    """整形ルール.md の「1行…N文字」を読んで折返し幅を決める。
    config.json に "line_wrap" があればそれを最優先。見つからなければ 25。"""
    cfg = load_config()
    if isinstance(cfg.get("line_wrap"), int) and cfg["line_wrap"] > 0:
        return cfg["line_wrap"]
    try:
        rule = (BASE_DIR / "prompt_knowledge" / "整形ルール.md").read_text(encoding="utf-8")
        m = re.search(r"1行[^0-9]{0,14}(\d{1,3})\s*[〜~\-]?\s*(\d{1,3})?\s*(?:文字|字)", rule)
        if m:
            return int(m.group(2) or m.group(1))
    except Exception:
        pass
    return 25


def _fold_sentence(sent: str, width: int) -> list[str]:
    """1文を読点（、）で width 以内に折る。読点が無い長文は強制分割。"""
    if len(sent) <= width:
        return [sent]
    parts = re.split(r"(、)", sent)
    tokens, i = [], 0
    while i < len(parts):
        t = parts[i]
        if i + 1 < len(parts) and parts[i + 1] == "、":
            t += "、"; i += 2
        else:
            i += 1
        if t:
            tokens.append(t)
    lines, cur = [], ""
    for tk in tokens:
        if cur and len(cur) + len(tk) > width:
            lines.append(cur); cur = tk
        else:
            cur += tk
    if cur:
        lines.append(cur)
    # 読点が無く極端に長い塊だけ強制分割
    final = []
    for l in lines:
        while len(l) > int(width * 1.6):
            final.append(l[:width]); l = l[width:]
        final.append(l)
    return final


def _fold_paragraph(text: str, width: int) -> list[str]:
    """段落テキストを文単位→読点で折り、太字（**）が行をまたいで割れないよう補正。"""
    sentences = [s for s in re.findall(r"[^。！？]*[。！？]?", text) if s]
    lines = []
    for sent in sentences:
        lines.extend(_fold_sentence(sent, width))
    fixed, i = [], 0
    while i < len(lines):
        l = lines[i]
        while l.count("**") % 2 == 1 and i + 1 < len(lines):
            i += 1; l += lines[i]
        fixed.append(l); i += 1
    return fixed


def reflow_for_paste(body: str, width: int = None) -> str:
    """貼り付け直前の軽い整形。claude が既に折り返した行はそのまま尊重し、
    表示幅を超える「長すぎる行だけ」読点で折る（＝崩れ防止の安全網）。"""
    cfg = load_config()
    no_wrap = str(cfg.get("line_wrap")) == "none"

    if width is None:
        # スマホ表示（全角約20字）を超えないよう上限を設ける
        width = min(_wrap_width(), 20)

    out = []
    if no_wrap:
        # 折り返しなし：段落（連続する非空行）を連結し、1文1行に戻す
        para = []

        def flush_join():
            if para:
                joined = "".join(para)
                out.extend(_fold_paragraph(joined, 10 ** 9))
                para.clear()

        for ln in body.splitlines():
            s = ln.strip()
            if re.match(r"^[＝=]{5,}$", s):
                continue
            if not s:
                flush_join(); out.append("")
            elif s.startswith("●"):
                flush_join(); out.append(s)
            else:
                para.append(s)
        flush_join()
    else:
        # 折り返しあり：claude の折りを尊重し、長すぎる行だけ読点で折る
        for ln in body.splitlines():
            s = ln.strip()
            if re.match(r"^[＝=]{5,}$", s):
                continue
            if not s:
                out.append("")
                continue
            if s.startswith("●"):
                out.append(s)
                continue
            if len(s) > width:
                out.extend(_fold_paragraph(s, width))
            else:
                out.append(s)

    # セクション内の詰まり防止：N文（句点）ごとに空行を入れて余白を作る
    every = cfg.get("blank_every")
    every = every if isinstance(every, int) and every >= 1 else 2
    spaced, sent = [], 0
    for i, l in enumerate(out):
        spaced.append(l)
        if l == "" or l.startswith("●"):
            sent = 0
            continue
        if l[-1] in "。！？!?":
            sent += 1
            if sent >= every:
                nxt = out[i + 1] if i + 1 < len(out) else ""
                if nxt != "" and not nxt.startswith("●"):
                    spaced.append("")
                sent = 0
    out = spaced

    # 各区切りの空行を blank_lines 本に正規化
    gap = cfg.get("blank_lines")
    gap = gap if isinstance(gap, int) and gap >= 1 else 2
    normalized, i, n = [], 0, len(out)
    while i < n:
        if out[i] == "":
            while i < n and out[i] == "":
                i += 1
            if normalized and i < n:   # 先頭・末尾の空行は無視
                normalized.extend([""] * gap)
        else:
            normalized.append(out[i]); i += 1
    return "\n".join(normalized)


def format_file(path: Path) -> tuple[str, str]:
    """記事ファイルを (タイトル, 貼り付け用本文) に整形して返す。"""
    title, body = parse_article(path)
    return title, reflow_for_paste(body)


# ==============================
# CLI
# ==============================
def _target_files(args) -> list[Path]:
    if args.file:
        p = Path(args.file)
        if not p.is_absolute():
            p = BASE_DIR / p
        if not p.exists():
            print(f"✗ ファイルが見つかりません: {p}")
            sys.exit(1)
        return [p]
    return sorted(ARTICLES_DIR.glob("*.txt"))


def main():
    ap = argparse.ArgumentParser(description="記事を貼り付け用テキストに整形する")
    ap.add_argument("--file", help="整形する記事ファイル（例: articles/article_○○.txt）")
    ap.add_argument("--all", action="store_true", help="articles/ 直下のすべての記事を対象にする")
    ap.add_argument("--list", action="store_true", help="記事の一覧を表示する")
    ap.add_argument("--save", action="store_true",
                    help="結果を articles/貼り付け用/ に .txt で書き出す")
    args = ap.parse_args()

    if args.list:
        files = sorted(ARTICLES_DIR.glob("*.txt"))
        published = sorted((ARTICLES_DIR / "published").glob("*.txt"))
        print(f"■ 未公開: {len(files)}件")
        for f in files:
            t, _ = parse_article(f)
            print(f"  - {f.name}  … {t}")
        print(f"■ 公開済み: {len(published)}件")
        for f in published:
            print(f"  - {f.name}")
        return

    if not args.file and not args.all:
        ap.print_help()
        return

    out_dir = ARTICLES_DIR / "貼り付け用"
    for path in _target_files(args):
        title, text = format_file(path)
        if args.save:
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / path.name
            out.write_text(f"{title}\n\n{text}\n", encoding="utf-8")
            print(f"✓ {out}")
        else:
            print("=" * 50)
            print(f"タイトル: {title}")
            print("=" * 50)
            print(text)


if __name__ == "__main__":
    main()
