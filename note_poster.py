"""
note_poster.py - note.com 下書き自動投稿スクリプト

使い方:
  python note_poster.py --count 5    # 5件を下書き保存
  python note_poster.py --count 1    # 1件だけ

記事ファイル形式（articles/*.txt）:
  1行目  : テーマ：タイトル
  2行目  : 生成日時：...
  3行目  : ===...===
  4行目〜: 本文
           ●見出し  → note H2
           ＝＝＝＝＝ → スキップ
           【終了】  → ここで終端
"""

import os
import re
import sys
import time
import shutil
import hashlib
import argparse
from pathlib import Path

# Windows コンソール文字化け対策
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from PIL import Image, ImageDraw, ImageFont

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException
)

# ==============================
# 設定
# ==============================
BASE_DIR         = Path(__file__).parent
_CONFIG_FILE     = BASE_DIR / "config.json"

def _load_note_config():
    if _CONFIG_FILE.exists():
        import json
        with open(_CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def _resolve_account(config):
    """active_account のアカウント固有設定を返す。accounts未対応なら旧形式フォールバック。"""
    accounts = config.get("accounts")
    if accounts:
        name = config.get("active_account", "")
        acct = accounts.get(name) or next(iter(accounts.values()))
        return acct, name
    return {
        "chrome_data_dir": "cloned_chrome_data",
    }, ""

_config          = _load_note_config()
_acct, _acct_name = _resolve_account(_config)
CHROME_USER_DATA = str(BASE_DIR / _acct.get("chrome_data_dir", "cloned_chrome_data"))
PROFILE_DIR      = _config.get("chrome_profile_dir", "Profile 1")
ARTICLES_DIR     = BASE_DIR / "articles"
POSTED_DIR       = ARTICLES_DIR / "posted"
THUMB_DIR        = BASE_DIR / "thumbs"
THEMES_FILE      = BASE_DIR / "themes.json"
NOTE_NEW_URL     = "https://note.com/notes/new"

# サムネイルサイズ（note.com 推奨）
THUMB_W, THUMB_H = 1280, 670

# 背景色パレット（タイトルハッシュで選択）
BG_COLORS = [
    (41,  98,  255),   # ブルー
    (0,  168,  107),   # グリーン
    (220,  53,   69),  # レッド
    (138,  43,  226),  # パープル
    (255, 140,    0),  # オレンジ
    (32,  178,  170),  # ティール
    (199,  21,  133),  # ピンク
]

# Windowsフォント候補（日本語対応）
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\meiryo.ttc",
    r"C:\Windows\Fonts\YuGothM.ttc",
    r"C:\Windows\Fonts\msgothic.ttc",
    r"C:\Windows\Fonts\msmincho.ttc",
]

# ==============================
# サムネイル生成（Pillow）
# ==============================
def _get_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def generate_thumbnail(title: str, out_path: Path) -> Path:
    """タイトルから Pillow でサムネイル画像を生成"""
    hash_val = int(hashlib.md5(title.encode("utf-8")).hexdigest(), 16)
    bg = BG_COLORS[hash_val % len(BG_COLORS)]

    img = Image.new("RGB", (THUMB_W, THUMB_H), bg)
    draw = ImageDraw.Draw(img)

    # 下部グラデーション風の暗い帯
    grad_h = THUMB_H // 3
    for i in range(grad_h):
        ratio = i / grad_h
        r = max(0, int(bg[0] * (1 - ratio * 0.5)))
        g = max(0, int(bg[1] * (1 - ratio * 0.5)))
        b = max(0, int(bg[2] * (1 - ratio * 0.5)))
        y = THUMB_H - grad_h + i
        draw.line([(0, y), (THUMB_W, y)], fill=(r, g, b))

    # タイトルテキスト（16文字で折り返し、最大3行）
    wrap_width = 16
    raw_lines = []
    for i in range(0, len(title), wrap_width):
        raw_lines.append(title[i:i + wrap_width])
    lines = raw_lines[:3]
    if len(raw_lines) > 3:
        lines[2] = lines[2][:14] + "…"

    font_size = 60 if len(title) <= 20 else 50
    font = _get_font(font_size)
    line_h = font_size + 12
    total_h = len(lines) * line_h
    y_start = (THUMB_H - total_h) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = (THUMB_W - text_w) // 2
        y = y_start + i * line_h
        # 影
        draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0))
        # 本文
        draw.text((x, y), line, font=font, fill=(255, 255, 255))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), "JPEG", quality=92)
    print(f"[INFO] サムネイル生成: {out_path.name}")
    return out_path


# ==============================
# 記事ファイル解析
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
            # 最初の区切り行の次から本文
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
                # タイムスタンプ形式を除去
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
# Selenium - Chromeドライバー
# ==============================
def setup_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument(f"--user-data-dir={CHROME_USER_DATA}")
    opts.add_argument(f"--profile-directory={PROFILE_DIR}")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=opts)
    driver.set_window_size(1400, 900)
    return driver


def _wait(driver, by, selector, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )


def _find_any(driver, selectors: list[str]):
    """複数セレクタを順番に試して最初に見つかった要素を返す"""
    for sel in selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            return el
        except NoSuchElementException:
            continue
    return None


def _find_any_xpath(driver, xpaths: list[str]):
    for xp in xpaths:
        try:
            el = driver.find_element(By.XPATH, xp)
            return el
        except NoSuchElementException:
            continue
    return None


# ==============================
# note.com エディタ操作
# ==============================
def input_title(driver, title: str) -> bool:
    """タイトルを入力"""
    selectors = [
        "textarea[placeholder*='タイトル']",
        "input[placeholder*='タイトル']",
        "div[data-placeholder*='タイトル']",
        "[data-testid='title']",
        ".title-field textarea",
        ".title-field input",
    ]
    try:
        el = WebDriverWait(driver, 15).until(
            lambda d: _find_any(d, selectors)
        )
        el.click()
        time.sleep(0.3)
        el.clear()
        ActionChains(driver).send_keys(title).perform()
        print(f"[INFO] タイトル入力: {title[:40]}…")
        return True
    except Exception as e:
        print(f"[ERROR] タイトル入力失敗: {e}")
        return False


def _get_editor(driver):
    """本文エディタ要素を取得"""
    selectors = [
        ".public-DraftEditor-content",
        "div[contenteditable='true']",
        ".DraftEditor-editorContainer [contenteditable]",
        ".note-editor [contenteditable]",
        "[data-testid='body'] [contenteditable]",
    ]
    for sel in selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            if el.is_displayed():
                return el
        except NoSuchElementException:
            continue
    return None


def _apply_heading_h2(driver):
    """
    現在カーソル行を H2 見出しに変換する。
    note.comの操作フロー:
      1. 行頭に移動
      2. 行全体を選択
      3. ツールバーのH2ボタンをクリック（なければスキップ）
    """
    actions = ActionChains(driver)

    # 行選択（Home → Shift+End）
    actions.key_down(Keys.HOME).key_up(Keys.HOME).perform()
    time.sleep(0.15)
    actions.key_down(Keys.SHIFT).send_keys(Keys.END).key_up(Keys.SHIFT).perform()
    time.sleep(0.3)

    # ツールバーH2ボタンを探す
    h2_selectors = [
        "button[data-type='header-two']",
        "button[data-style='header-two']",
        "button[aria-label*='見出し2']",
        "button[aria-label*='Heading 2']",
        "button[title*='見出し2']",
        "button[title*='H2']",
        "[data-testid='toolbar-heading2']",
        ".public-DraftStyleDefault-h2-button",
    ]
    for sel in h2_selectors:
        try:
            btn = driver.find_element(By.CSS_SELECTOR, sel)
            if btn.is_displayed():
                btn.click()
                time.sleep(0.2)
                return True
        except Exception:
            continue

    # note の「見出し」ドロップダウン → 「大」(H2) を選ぶ
    try:
        head_btn = _find_any_xpath(driver, [
            "//button[contains(normalize-space(), '見出し')]",
            "//*[@role='button'][contains(normalize-space(), '見出し')]",
            "//button[contains(@aria-label, '見出し')]",
        ])
        if head_btn is not None and head_btn.is_displayed():
            head_btn.click()
            time.sleep(0.4)
            opt = _find_any_xpath(driver, [
                "//*[self::button or self::a or @role='menuitem' or @role='option'][normalize-space()='大']",
                "//*[self::button or self::a or @role='menuitem' or @role='option'][contains(normalize-space(),'見出し大')]",
                "//*[self::li or self::button or self::a][contains(normalize-space(),'大')]",
            ])
            if opt is not None and opt.is_displayed():
                opt.click()
                time.sleep(0.2)
                return True
    except Exception:
        pass

    # キーボードショートカット試行 (Ctrl+Alt+2)
    try:
        actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys("2") \
               .key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
        time.sleep(0.2)
    except Exception:
        pass
    return False


def _type_bold_line(driver, line: str):
    """**bold** マーカーを解析してCtrl+Bで太字入力"""
    parts = re.split(r"(\*\*[^*]+\*\*)", line)
    for part in parts:
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            bold_text = part[2:-2]
            ActionChains(driver).key_down(Keys.CONTROL).send_keys("b") \
                                .key_up(Keys.CONTROL).perform()
            time.sleep(0.1)
            ActionChains(driver).send_keys(bold_text).perform()
            time.sleep(0.05)
            ActionChains(driver).key_down(Keys.CONTROL).send_keys("b") \
                                .key_up(Keys.CONTROL).perform()
            time.sleep(0.1)
        else:
            if part:
                ActionChains(driver).send_keys(part).perform()
                time.sleep(0.03)


# ==============================
# 投稿直前リフロー（整形ルールを note 反映）
# ==============================
def _wrap_width() -> int:
    """整形ルール.md の「1行…N文字」を読んで折返し幅を決める。
    config.json に "line_wrap" があればそれを最優先。見つからなければ 25。"""
    try:
        cfg = _load_note_config()
        if isinstance(cfg.get("line_wrap"), int) and cfg["line_wrap"] > 0:
            return cfg["line_wrap"]
    except Exception:
        pass
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
    # 「、」を残したまま分割
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
    # ** の対が行をまたいで割れたら次行と結合して直す
    fixed, i = [], 0
    while i < len(lines):
        l = lines[i]
        while l.count("**") % 2 == 1 and i + 1 < len(lines):
            i += 1; l += lines[i]
        fixed.append(l); i += 1
    return fixed


def reflow_for_note(body: str, width: int = None) -> str:
    """投稿直前の軽い整形。claude が既に折り返した行はそのまま尊重し、
    note の表示幅を超える「長すぎる行だけ」読点で折る（＝崩れ防止の安全網）。
    行の連結や再折りはしない（claude の整形を壊さない）。"""
    # 「折り返しなし」設定なら、長い行も折らずそのままにする
    no_wrap = False
    try:
        if str(_load_note_config().get("line_wrap")) == "none":
            no_wrap = True
    except Exception:
        pass
    if width is None:
        # note の表示カラム（全角約20字）を超えないよう上限を設ける
        width = min(_wrap_width(), 20)
    out = []
    if no_wrap:
        # 折り返しなし：段落（連続する非空行）を連結し、1文1行に戻す
        para = []

        def flush_join():
            if para:
                joined = "".join(para)
                out.extend(_fold_paragraph(joined, 10 ** 9))  # 文単位で分割（折らない）
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
    every = 2
    try:
        cfg = _load_note_config()
        if isinstance(cfg.get("blank_every"), int) and cfg["blank_every"] >= 1:
            every = cfg["blank_every"]
    except Exception:
        pass
    spaced, sent = [], 0
    for i, l in enumerate(out):
        spaced.append(l)
        if l == "" or l.startswith("●"):
            sent = 0
            continue
        if l[-1] in "。！？!?":          # 文の終わり
            sent += 1
            if sent >= every:
                nxt = out[i + 1] if i + 1 < len(out) else ""
                if nxt != "" and not nxt.startswith("●"):
                    spaced.append("")   # 余白を挿入
                sent = 0
    out = spaced

    # 各区切りの空行を blank_lines 本に正規化（既定2本＝しっかり余白）
    gap = 2
    try:
        cfg = _load_note_config()
        if isinstance(cfg.get("blank_lines"), int) and cfg["blank_lines"] >= 1:
            gap = cfg["blank_lines"]
    except Exception:
        pass
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


def input_body(driver, body: str) -> bool:
    """本文をフォーマット付きで入力"""
    # 投稿直前に整形ルール（1行N文字・段落）へ機械的に揃える
    try:
        body = reflow_for_note(body)
    except Exception as e:
        print(f"[WARN] リフロー失敗（元の本文で続行）: {e}")
    editor = _get_editor(driver)
    if editor is None:
        # タイトル入力後Tabで本文へ移動
        ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(0.5)
        editor = _get_editor(driver)

    if editor is None:
        print("[ERROR] 本文エディタが見つかりません")
        return False

    editor.click()
    time.sleep(0.5)

    # ＝＝＝区切りを除去し、先頭・末尾の空行を落とす
    raw_lines = [ln for ln in body.splitlines()
                 if not re.match(r"^[＝=]{5,}$", ln.strip())]
    while raw_lines and not raw_lines[0].strip():
        raw_lines.pop(0)
    while raw_lines and not raw_lines[-1].strip():
        raw_lines.pop()

    # 行単位で入力する。
    #   - 空行          → Enter（空のブロック＝note上で見える余白）
    #   - ● 見出し      → 新ブロックにして H2
    #   - 段落内の折返し → 直前がテキスト行なら Shift+Enter（詰まった改行）
    #   - 新ブロック開始 → Enter
    prev_text = False
    first = True
    for ln in raw_lines:
        s = ln.strip()
        if not s:
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(0.06)
            prev_text = False
            continue
        if s.startswith("●"):
            if not first:
                ActionChains(driver).send_keys(Keys.ENTER).perform()
                time.sleep(0.08)
            ActionChains(driver).send_keys(s.lstrip("●").strip()).perform()
            time.sleep(0.2)
            _apply_heading_h2(driver)
            time.sleep(0.1)
            prev_text = False
            first = False
            continue
        # 通常テキスト
        if prev_text:
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER) \
                                .key_up(Keys.SHIFT).perform()
            time.sleep(0.04)
        elif not first:
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(0.08)
        _type_bold_line(driver, s)
        prev_text = True
        first = False

    print("[INFO] 本文入力完了")
    return True


def upload_thumbnail(driver, thumb_path: Path) -> bool:
    """サムネイル（アイキャッチ）画像をアップロード"""
    abs_path = str(thumb_path.resolve())

    # ① 非表示を含む file input を直接探す
    input_selectors = [
        "input[type='file'][accept*='image']",
        "input[type='file']",
    ]
    for sel in input_selectors:
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            for el in els:
                try:
                    el.send_keys(abs_path)
                    time.sleep(2)
                    print(f"[INFO] サムネイルアップロード完了")
                    return True
                except Exception:
                    continue
        except Exception:
            continue

    # ② アイキャッチ追加ボタンをクリック → ダイアログ内の input を探す
    btn_xpaths = [
        "//button[contains(., 'アイキャッチ')]",
        "//button[contains(., 'サムネイル')]",
        "//button[contains(@aria-label, 'アイキャッチ')]",
        "//*[contains(@class,'eyecatch')]//button",
    ]
    for xp in btn_xpaths:
        try:
            btn = driver.find_element(By.XPATH, xp)
            btn.click()
            time.sleep(1.5)
            # ダイアログ内の file input
            file_el = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_el.send_keys(abs_path)
            time.sleep(2)
            print(f"[INFO] サムネイルアップロード完了（ダイアログ経由）")
            return True
        except Exception:
            continue

    print("[WARN] サムネイルアップロード要素が見つかりません（スキップ）")
    return False


def save_draft(driver) -> bool:
    """下書き保存"""
    # XPathで「下書き」を含むボタンを探す
    xpaths = [
        "//button[contains(text(), '下書き保存')]",
        "//button[contains(text(), '下書き')]",
        "//button[contains(., '下書き')]",
        "//a[contains(text(), '下書き保存')]",
    ]
    for xp in xpaths:
        try:
            btn = driver.find_element(By.XPATH, xp)
            if btn.is_displayed():
                btn.click()
                time.sleep(3)
                print("[INFO] 下書き保存しました")
                return True
        except Exception:
            continue

    # Ctrl+S でも試みる
    try:
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("s") \
                            .key_up(Keys.CONTROL).perform()
        time.sleep(2)
        print("[INFO] Ctrl+S で保存試行")
        return True
    except Exception:
        pass

    print("[WARN] 下書き保存ボタンが見つかりません")
    return False


# ==============================
# 1記事投稿フロー
# ==============================
def post_article(driver, title: str, body: str, thumb_path: Path) -> bool:
    """1記事を note.com に下書き投稿"""
    try:
        driver.get(NOTE_NEW_URL)
        print(f"[INFO] note.com 新規記事ページを開きました")
        time.sleep(4)

        # タイトル入力
        if not input_title(driver, title):
            return False
        time.sleep(0.5)

        # 本文クリックで移動
        try:
            body_area = _get_editor(driver)
            if body_area:
                body_area.click()
            else:
                ActionChains(driver).send_keys(Keys.TAB).perform()
            time.sleep(0.5)
        except Exception:
            pass

        # 本文入力
        if not input_body(driver, body):
            return False
        time.sleep(1)

        # サムネイルアップロード
        upload_thumbnail(driver, thumb_path)
        time.sleep(1)

        # 下書き保存
        return save_draft(driver)

    except Exception as e:
        print(f"[ERROR] 投稿中にエラー: {e}")
        return False


# ==============================
# ファイル管理
# ==============================
def get_pending_files(n: int) -> list[Path]:
    """未投稿のtxtファイルをn件取得（更新順）"""
    ARTICLES_DIR.mkdir(exist_ok=True)
    files = sorted(ARTICLES_DIR.glob("*.txt"), key=lambda p: p.stat().st_mtime)
    return files[:n]


def find_files_by_title(keyword: str) -> list[Path]:
    """
    キーワードでファイルを検索する。
    ファイル名 or ファイル内タイトル（●行）をLOWER比較で部分一致。
    """
    ARTICLES_DIR.mkdir(exist_ok=True)
    kw = keyword.lower()
    matches = []
    for path in sorted(ARTICLES_DIR.glob("*.txt")):
        # ファイル名で一致
        if kw in path.stem.lower():
            matches.append(path)
            continue
        # ファイル内タイトルで一致
        try:
            title, _ = parse_article(path)
            if kw in title.lower():
                matches.append(path)
        except Exception:
            continue
    return matches


def show_status():
    """articles/ と articles/posted/ の一覧とステータスを表示"""
    ARTICLES_DIR.mkdir(exist_ok=True)
    POSTED_DIR.mkdir(parents=True, exist_ok=True)

    pending = sorted(ARTICLES_DIR.glob("*.txt"), key=lambda p: p.stat().st_mtime)
    posted  = sorted(POSTED_DIR.glob("*.txt"),   key=lambda p: p.stat().st_mtime, reverse=True)

    print()
    print("=" * 60)
    print(f"  未投稿: {len(pending)}件  /  投稿済み: {len(posted)}件")
    print("=" * 60)

    if pending:
        print("\n[ 未投稿 ]")
        for i, p in enumerate(pending, 1):
            try:
                title, body = parse_article(p)
                chars = len(body)
            except Exception:
                title, chars = p.stem, 0
            print(f"  {i:3}. {title[:45]:<45}  ({chars}文字)")

    if posted:
        print("\n[ 投稿済み（直近10件）]")
        for i, p in enumerate(posted[:10], 1):
            try:
                title, _ = parse_article(p)
            except Exception:
                title = p.stem
            print(f"  {i:3}. {title[:45]}")

    print()


def move_to_posted(path: Path):
    """投稿済みファイルを posted/ フォルダへ移動"""
    POSTED_DIR.mkdir(parents=True, exist_ok=True)
    dest = POSTED_DIR / path.name
    # 同名ファイルが既にあれば連番をつける
    counter = 1
    while dest.exists():
        dest = POSTED_DIR / f"{path.stem}_{counter}{path.suffix}"
        counter += 1
    shutil.move(str(path), str(dest))
    print(f"[INFO] 移動: {path.name} → posted/")


def _normalize_theme(s: str) -> str:
    """照合用にテーマ/タイトルを正規化（空白・記号・括弧を除去して小文字化）。"""
    return re.sub(
        r"[\s　、。「」『』【】（）()\[\]！!？?・,.\-—–~〜:：;；\"'”’“`｜|]",
        "", (s or "").lower()
    )


def mark_theme_done(title: str, filepath: Path):
    """投稿成功した記事に対応するテーマを themes.json で pending→done へ移動する。
    記事タイトル / ファイル名（article_接頭辞を除去）と pending 各テーマを正規化して照合。"""
    if not THEMES_FILE.exists():
        return
    import json
    try:
        data = json.loads(THEMES_FILE.read_text(encoding="utf-8") or "{}")
    except Exception as e:
        print(f"[WARN] themes.json 読み込み失敗: {e}")
        return
    pending = data.get("pending") or []
    done = data.get("done") or []
    if not pending:
        return

    stem = filepath.stem
    if stem.startswith("article_"):
        stem = stem[len("article_"):]
    cands = [c for c in (_normalize_theme(title), _normalize_theme(stem)) if c]

    best_idx, best_score = -1, 0
    for idx, theme in enumerate(pending):
        nt = _normalize_theme(theme)
        if not nt:
            continue
        for c in cands:
            if nt == c:
                score = 10000                      # 完全一致
            elif nt in c or c in nt:
                score = min(len(nt), len(c))        # 部分一致＝重なりの長さ
            else:
                score = 0
            if score > best_score:
                best_score, best_idx = score, idx

    # 短すぎる部分一致での誤爆を防ぐ（最低6文字相当）
    if best_idx >= 0 and best_score >= 6:
        moved = pending.pop(best_idx)
        if moved not in done:
            done.append(moved)
        data["pending"], data["done"] = pending, done
        THEMES_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[INFO] themes.json 更新: pending→done 「{moved[:40]}」（残り pending {len(pending)}件）")
    else:
        print(f"[WARN] themes.json: 対応テーマが見つからず未更新（title: {title[:30]}…）")


# ==============================
# ログインヘルパー
# ==============================
def do_login():
    """
    既存Chromeプロファイルでnote.comを開き、
    ログイン完了を自動検出してブラウザを閉じる。
    """
    label = f"（アカウント: {_acct_name}）" if _acct_name else "（Profile 1）"
    print(f"[INFO] Chromeを起動します{label}")
    driver = setup_driver()
    driver.get("https://note.com/login")
    print()
    print("=" * 55)
    print("  ブラウザが開きました。")
    print("  note.com に手動でログインしてください。")
    print("  （メール/パスワード or SNSログイン）")
    print()
    print("  ログイン完了後、自動でブラウザが閉じます。")
    print("  タイムアウト: 5分")
    print("=" * 55)

    # ログイン完了を自動検出（最大5分）
    timeout = 300
    interval = 3
    elapsed = 0
    logged_in = False

    while elapsed < timeout:
        time.sleep(interval)
        elapsed += interval
        try:
            current_url = driver.current_url
            # /login または /oauth ページ以外の note.com ページにいればログイン成功
            is_login_page = any(kw in current_url for kw in ["/login", "/oauth", "/auth", "signin"])
            if "note.com" in current_url and not is_login_page:
                logged_in = True
                break
            # ログイン済みを示す要素（複数パターン）
            logged_in_selectors = [
                "a[href*='/settings']",
                "a[href*='/dashboard']",
                "[data-testid='header-user']",
                ".o-headerMenu__userIcon",
                "img[alt*='アイコン']",
                "a[href='/notes/new']",
                ".m-siteHeader__userArea",
                "[class*='userIcon']",
                "[class*='UserIcon']",
            ]
            for sel in logged_in_selectors:
                els = driver.find_elements(By.CSS_SELECTOR, sel)
                if els:
                    logged_in = True
                    break
            if logged_in:
                break
        except WebDriverException:
            break
        print(f"[INFO] ログイン待機中... ({elapsed}/{timeout}秒)  URL: {driver.current_url[:60]}", end="\r")

    print()
    driver.quit()

    if logged_in:
        print("[INFO] ログイン完了を検出しました。")
        print("[INFO] 次回から --count N で自動投稿できます。")
    else:
        print("[WARN] タイムアウトしました。もう一度 --login を実行してください。")


# ==============================
# メイン
# ==============================
def main():
    parser = argparse.ArgumentParser(
        description="note.com 下書き自動投稿",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "使い方:\n"
            "  python note_poster.py --count 5\n"
            "  python note_poster.py --title \"副業\"\n"
            "  python note_poster.py --status\n"
            "  python note_poster.py --login\n"
        )
    )
    parser.add_argument("--count", type=int, default=1,
                        help="先頭からN件を投稿（デフォルト: 1）")
    parser.add_argument("--title", type=str, default=None,
                        help="タイトルキーワードで記事を検索して投稿")
    parser.add_argument("--status", action="store_true",
                        help="未投稿/投稿済み一覧を表示")
    parser.add_argument("--login", action="store_true",
                        help="note.com に手動ログインしてクッキーを保存")
    args = parser.parse_args()

    # ログインモード
    if args.login:
        do_login()
        return

    # ステータス表示モード
    if args.status:
        show_status()
        return

    # タイトル指定モード
    if args.title:
        files = find_files_by_title(args.title)
        if not files:
            print(f"[INFO] 「{args.title}」に一致するファイルが見つかりません")
            print("[INFO]  --status で一覧を確認してください")
            return
        if len(files) > 1:
            print(f"[INFO] {len(files)}件ヒットしました:")
            for i, f in enumerate(files, 1):
                title, _ = parse_article(f)
                print(f"  {i}. {title[:55]}")
            print("[INFO] 全件を投稿します")
    else:
        files = get_pending_files(args.count)
        if not files:
            print("[INFO] 投稿するファイルがありません（articles/*.txt が空）")
            return

    print(f"[INFO] {len(files)}件を下書き投稿します")
    driver = setup_driver()

    success = 0
    try:
        for i, filepath in enumerate(files, 1):
            print(f"\n{'='*50}")
            print(f"[{i}/{len(files)}] {filepath.name}")
            print(f"{'='*50}")

            # 記事解析
            title, body = parse_article(filepath)
            if not title:
                print("[WARN] タイトルが取得できません。スキップします")
                continue

            print(f"[INFO] タイトル: {title[:50]}")
            print(f"[INFO] 本文: {len(body)}文字")

            # サムネイル生成
            thumb_name = f"thumb_{filepath.stem[:40]}.jpg"
            # ファイル名に使えない文字を除去
            thumb_name = re.sub(r'[\\/:*?"<>|]', "_", thumb_name)
            thumb_path = THUMB_DIR / thumb_name
            generate_thumbnail(title, thumb_path)

            # 投稿
            ok = post_article(driver, title, body, thumb_path)

            if ok:
                move_to_posted(filepath)
                mark_theme_done(title, filepath)
                success += 1
                print(f"[OK] 下書き保存完了: {title[:50]}")
            else:
                print(f"[NG] 失敗: {title[:50]}")

            # 連続投稿の間隔
            if i < len(files):
                print("[INFO] 次の投稿まで5秒待機...")
                time.sleep(5)

    finally:
        driver.quit()
        print(f"\n{'='*50}")
        print(f"[完了] {success}/{len(files)}件 下書き保存しました")
        print(f"{'='*50}")


if __name__ == "__main__":
    main()
