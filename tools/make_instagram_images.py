# -*- coding: utf-8 -*-
"""articles/*.txt の Instagram キャプションから、1:1 カルーセル画像を生成する。

使い方:
    python tools/make_instagram_images.py                # 全35本を生成
    python tools/make_instagram_images.py --only 鉄と貧血  # 部分生成（確認用）
    python tools/make_instagram_images.py --format 4x5    # 1080x1350 で生成

出力: instagram/<番号>_<記事名>/01.jpg … （1記事 = 1フォルダ = 1カルーセル）
記事本文は触らない。読み取り専用。
"""
import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "articles"
OUT_DIR = ROOT / "instagram"

FONT_JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
FONT_EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
EMOJI_PX = 109  # NotoColorEmoji はこのサイズしか読めない（ビットマップ）

SERIES = "体質改善ダイエット"

# 配色：35本を通して同じ土台色＋記事ごとのアクセント色（フィードで並んだときに連作に見える）
BG = (21, 23, 28)
FG = (242, 239, 233)
MUTED = (142, 148, 158)
ACCENTS = [
    (242, 181, 68),   # amber
    (79, 195, 161),   # mint
    (255, 138, 107),  # coral
    (127, 179, 242),  # sky
    (201, 166, 242),  # lavender
    (111, 212, 212),  # aqua
    (242, 145, 182),  # rose
    (232, 208, 106),  # sand
]

# 序章の「この先に読むもの」に並ぶ順＝シリーズの通し番号
ORDER = [
    "article_序章_体質改善は発電所の管理です.txt",
    "article_禁煙とミトコンドリア.txt",
    "article_アルコールとミトコンドリア.txt",
    "article_朝の光と体内時計.txt",
    "article_睡眠とミトコンドリア.txt",
    "article_座りすぎとミトコンドリア.txt",
    "article_断食の時間帯と体内時計.txt",
    "article_歩き方と靴とミトコンドリア.txt",
    "article_ミトコンドリア体質改善ダイエット.txt",
    "article_運動の種類別とミトコンドリア.txt",
    "article_タンパク質とミトコンドリア.txt",
    "article_体質改善における水の重要性.txt",
    "article_腸内環境とミトコンドリア.txt",
    "article_鉄と貧血.txt",
    "article_マグネシウムとミトコンドリア.txt",
    "article_ビタミンDとミトコンドリア.txt",
    "article_オメガ3とミトコンドリア.txt",
    "article_歯と口腔環境とミトコンドリア.txt",
    "article_アレルギーと炎症とミトコンドリア.txt",
    "article_呼吸の質とミトコンドリア.txt",
    "article_姿勢とミトコンドリア.txt",
    "article_ストレスとコルチゾール.txt",
    "article_カフェインとミトコンドリア.txt",
    "article_冷えとミトコンドリア.txt",
    "article_血糖値の波とミトコンドリア.txt",
    "article_体重計の数字の読み方.txt",
    "article_常用薬と栄養とミトコンドリア.txt",
    "article_更年期とホルモンとミトコンドリア.txt",
    "article_旅行と出張の崩れ方.txt",
    "article_在宅勤務の環境とミトコンドリア.txt",
    "article_冬と夏の切り替え.txt",
    "article_家族を巻き込む方法.txt",
    "article_サプリの選び方と表示の読み方.txt",
    "article_環境要因とミトコンドリア.txt",
    "article_サウナと温冷交代.txt",
]

CAPTION_MARK = "▼Instagramキャプション"
CTA_MARK = "🔗 全文は"
DIVIDER = "┈"

_font_cache = {}


def font(size):
    key = int(size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_JP, key)
    return _font_cache[key]


# ------------------------------------------------------------------
# キャプションの読み取り
# ------------------------------------------------------------------

def read_caption(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    idx = text.find(CAPTION_MARK)
    if idx < 0:
        raise ValueError(f"{path.name}: {CAPTION_MARK} が見つかりません")
    body = text[idx:].split("\n", 1)[1]
    end = body.find(CTA_MARK)
    return (body[:end] if end >= 0 else body).strip()


def split_emoji(line: str):
    """行頭の絵文字と、残りの文字列に分ける。"""
    m = re.match(r"^([^\w\sぁ-んァ-ヶ一-龥。、「」（）]+)\s*(.*)$", line)
    if m and m.group(1).strip():
        return m.group(1).strip(), m.group(2).strip()
    return "", line.strip()


def parse_blocks(caption: str):
    """キャプションを「フック」と「ブロックの列」に分解する。"""
    lines = caption.split("\n")
    hook_emoji, hook = split_emoji(lines[0])

    blocks, cur = [], []
    for line in lines[1:]:
        s = line.strip()
        if not s or s.startswith(DIVIDER):
            if cur:
                blocks.append(cur)
                cur = []
            continue
        cur.append(s)
    if cur:
        blocks.append(cur)

    parsed = []
    for blk in blocks:
        checks = [re.sub(r"^[✅▶︎]\s*", "", x) for x in blk if x[0] in "✅▶"]
        if checks:
            lead = [x for x in blk if x[0] not in "✅▶"]
            _, lead_text = split_emoji(lead[0]) if lead else ("", "")
            parsed.append({"kind": "action", "lead": lead_text, "items": checks,
                           "tail": []})
            continue
        emo, first = split_emoji(blk[0])
        rest = [x for x in [first] + blk[1:] if x]
        warn = emo in ("⚠️", "⚠")
        kind = "note" if (warn or emo == "👉") else "prose"
        parsed.append({"kind": kind, "warn": warn, "lead": emo == "💡", "lines": rest})

    # 「💡 やることは…」の導入文と、✅ リストの直後の短い補足を、
    # 同じ1枚にまとめる（別スライドに散るとスカスカになるため）
    merged = []
    for b in parsed:
        prev = merged[-1] if merged else None
        short_lead = sum(len(l) for l in prev["lines"]) <= 45 if (
            prev and prev["kind"] == "prose") else False
        if b["kind"] == "action" and prev and prev["kind"] == "prose" \
                and (prev.get("lead") or short_lead) and not b["lead"]:
            b["lead"] = " ".join(prev["lines"])
            merged.pop()
        elif b["kind"] == "prose" and prev and prev["kind"] == "action" \
                and not prev["tail"] and sum(len(l) for l in b["lines"]) <= 90:
            prev["tail"] = b["lines"]
            continue
        merged.append(b)
    return hook_emoji, hook, merged


def build_slides(path: Path, max_slides: int):
    caption = read_caption(path)
    hook_emoji, hook, blocks = parse_blocks(caption)
    topic = path.stem.replace("article_", "").split("_")[0]

    # キャプションに出てくる順番のままスライドにする
    # （種類ごとにまとめると、2つ目の✅リストなどが落ちてしまうため）
    items = []
    for b in blocks:
        if b["kind"] == "action":
            items.append({"kind": "action", "lead": b["lead"], "items": b["items"],
                          "tail": b.get("tail") or []})
        elif b["kind"] == "note":
            items.append({"kind": "note", "warn": b.get("warn", False),
                          "lines": b["lines"]})
        else:
            items.append({"kind": "body", "kicker": topic, "lines": b["lines"]})

    def size_of(it):
        return sum(len(l) for l in it.get("lines", []))

    def merge_pass(pick):
        """隣り合う本文スライド同士をくっつける。pick が対象を選ぶ。"""
        while True:
            pairs = [i for i in range(len(items) - 1)
                     if items[i]["kind"] == "body" and items[i + 1]["kind"] == "body"]
            i = pick(pairs)
            if i is None:
                return
            items[i]["lines"] = items[i]["lines"] + items[i + 1]["lines"]
            del items[i + 1]

    # 1) 枚数が上限を超えるあいだ、合計の短い組から詰める
    merge_pass(lambda pairs: None if (not pairs or len(items) + 2 <= max_slides)
               else min(pairs, key=lambda k: size_of(items[k]) + size_of(items[k + 1])))
    # 2) スカスカな1枚（40字未満）は隣とくっつける
    merge_pass(lambda pairs: next(
        (k for k in pairs if size_of(items[k]) < 40 or size_of(items[k + 1]) < 40), None))

    return ([{"kind": "cover", "emoji": hook_emoji, "text": hook}]
            + items + [{"kind": "cta"}])


# ------------------------------------------------------------------
# 描画
# ------------------------------------------------------------------
CLOSERS = "、。）」』”！？…ー,.)!?"
OPENERS = "（「『“("


def wrap(draw, text, fnt, max_w):
    """ピクセル幅で折り返す。行頭に句読点・閉じ括弧を置かない（禁則処理）。"""
    lines, cur = [], ""
    for ch in text:
        if draw.textlength(cur + ch, font=fnt) <= max_w or not cur:
            cur += ch
            continue
        if ch in CLOSERS:            # 閉じ記号は前の行にぶら下げる
            lines.append(cur + ch)
            cur = ""
            continue
        if cur[-1] in OPENERS:       # 開き括弧は次の行へ送る
            lines.append(cur[:-1])
            cur = cur[-1] + ch
            continue
        lines.append(cur)
        cur = ch
    if cur:
        lines.append(cur)
    return lines


def layout(draw, paragraphs, max_w, max_h, size_from, size_to, lh=1.70, gap=0.55):
    """収まる一番大きい文字サイズを選び、(サイズ, 行の列, 総高さ) を返す。"""
    for size in range(size_from, size_to - 1, -2):
        fnt = font(size)
        rows, line_h = [], int(size * lh)
        for i, p in enumerate(paragraphs):
            if i:
                rows.append(None)  # 段落間のあき
            rows += wrap(draw, p, fnt, max_w)
        h = sum(int(size * gap) if r is None else line_h for r in rows)
        if h <= max_h:
            return size, rows, h
    return size_to, rows, h


def draw_rows(draw, rows, size, x, y, fill, lh=1.70, gap=0.55, bold=0):
    fnt, line_h = font(size), int(size * lh)
    for r in rows:
        if r is None:
            y += int(size * gap)
            continue
        draw.text((x, y), r, font=fnt, fill=fill, stroke_width=bold, stroke_fill=fill)
        y += line_h
    return y


def paste_emoji(img, ch, box, xy):
    """カラー絵文字を 109px で描いてから縮小して貼る。描けなければ黙って諦める。"""
    if not ch:
        return False
    try:
        ef = ImageFont.truetype(FONT_EMOJI, EMOJI_PX)
        tmp = Image.new("RGBA", (EMOJI_PX * 2, EMOJI_PX * 2), (0, 0, 0, 0))
        ImageDraw.Draw(tmp).text((0, 0), ch[0], font=ef, embedded_color=True)
        bb = tmp.getbbox()
        if not bb:
            return False
        img.paste(tmp.crop(bb).resize((box, box), Image.LANCZOS), xy,
                  tmp.crop(bb).resize((box, box), Image.LANCZOS))
        return True
    except Exception:
        return False


def kicker(draw, text, accent, x, y):
    draw.rectangle([x, y + 8, x + 16, y + 24], fill=accent)
    draw.text((x + 32, y), text, font=font(28), fill=accent)


def footer(draw, W, H, left, right, accent, margin):
    y = H - margin - 34
    draw.text((margin, y), left, font=font(26), fill=MUTED)
    if right:
        w = draw.textlength(right, font=font(26))
        draw.text((W - margin - w, y), right, font=font(26), fill=accent)


def render(slide, no, page, total, accent, W, H):
    margin = int(W * 0.082)
    cw = W - margin * 2
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # 全スライド共通の目印：左端のアクセント細線
    d.rectangle([0, 0, 6, H], fill=accent)
    tag = f"No.{no:02d}  {SERIES}"

    if slide["kind"] == "cover":
        d.rectangle([margin, margin, margin + 72, margin + 5], fill=accent)
        d.text((margin, margin + 30), SERIES, font=font(30), fill=accent)

        top = margin + 96
        if paste_emoji(img, slide["emoji"], 118, (margin, top)):
            top += 150
        else:
            top += 24

        size, rows, h = layout(d, [slide["text"]], cw, H - top - margin - 150, 74, 44, lh=1.52)
        y = draw_rows(d, rows, size, margin, top, FG, lh=1.52, bold=1)
        d.rectangle([margin, y + 26, margin + 120, y + 32], fill=accent)

        footer(d, W, H, f"No.{no:02d} / 全{total_articles:02d}回", "スワイプ →", accent, margin)

    elif slide["kind"] == "body":
        kicker(d, slide["kicker"], accent, margin, margin + 6)
        top = margin + 110
        room = H - top - margin - 110
        solo = sum(len(l) for l in slide["lines"]) < 40
        size, rows, h = layout(d, slide["lines"], cw, room,
                               72 if solo else 50, 30, lh=1.58 if solo else 1.70)
        draw_rows(d, rows, size, margin, top + max(0, (room - h) // 2), FG,
                  lh=1.58 if solo else 1.70, bold=1 if solo else 0)
        footer(d, W, H, tag, f"{page}/{total}", accent, margin)

    elif slide["kind"] == "action":
        kicker(d, "やることはこれだけ", accent, margin, margin + 6)
        top = margin + 104
        if slide["lead"]:
            size, rows, h = layout(d, [slide["lead"]], cw, 200, 56, 36, lh=1.5)
            top = draw_rows(d, rows, size, margin, top, FG, lh=1.5, bold=1) + 44

        items = slide["items"]
        room = H - top - margin - 110
        for isize in range(48, 29, -2):
            blocks, th = [], 0
            for it in items:
                rows = wrap(d, it, font(isize), cw - 78)
                blocks.append(rows)
                th += len(rows) * int(isize * 1.6) + 34
            if th <= room:
                break
        y = top
        for rows in blocks:
            cy = y + int(isize * 0.22)
            d.rounded_rectangle([margin, cy, margin + 40, cy + 40], 10, fill=accent)
            d.line([(margin + 11, cy + 21), (margin + 18, cy + 29), (margin + 30, cy + 12)],
                   fill=BG, width=5)
            y = draw_rows(d, rows, isize, margin + 78, y, FG, lh=1.6) + 34
        tail = slide.get("tail") or []
        if tail and H - y - margin - 110 > 120:
            tsize, trows, _ = layout(d, tail, cw, H - y - margin - 110, 40, 28)
            draw_rows(d, trows, tsize, margin, y + 24, MUTED)
        footer(d, W, H, tag, f"{page}/{total}", accent, margin)

    elif slide["kind"] == "note":
        kicker(d, "ここだけ注意" if slide.get("warn") else "最後にひとつ",
               accent, margin, margin + 6)
        top = margin + 120
        box_h = H - top - margin - 120
        d.rounded_rectangle([margin - 4, top, W - margin + 4, top + box_h], 24,
                            fill=(29, 32, 38))
        size, rows, h = layout(d, slide["lines"], cw - 72, box_h - 96, 50, 30)
        draw_rows(d, rows, size, margin + 32, top + (box_h - h) // 2, FG)
        footer(d, W, H, tag, f"{page}/{total}", accent, margin)

    else:  # cta
        d.rectangle([margin, margin, margin + 72, margin + 5], fill=accent)
        d.text((margin, margin + 30), SERIES, font=font(30), fill=accent)
        size, rows, h = layout(d, ["保存して、読み返す用に。"], cw,
                               260, 76, 48, lh=1.5)
        y = draw_rows(d, rows, size, margin, margin + 150, accent, lh=1.5, bold=1)
        size2, rows2, _ = layout(
            d, ["全文はプロフィールのリンクから読めます。",
                "必要になったときに、ここへ戻ってこられます。"],
            cw, H - y - margin - 140, 42, 28)
        draw_rows(d, rows2, size2, margin, y + 56, FG)
        footer(d, W, H, f"No.{no:02d} / 全{total_articles:02d}回", "プロフィールへ →", accent, margin)

    return img


total_articles = 35


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="ファイル名の一部で絞り込む")
    ap.add_argument("--format", default="1x1", choices=["1x1", "4x5"])
    ap.add_argument("--max-slides", type=int, default=8)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    W, H = (1080, 1080) if args.format == "1x1" else (1080, 1350)
    out_root = Path(args.out) if args.out else OUT_DIR
    if args.format != "1x1":
        out_root = out_root.with_name(out_root.name + "_" + args.format)

    files = [f for f in ORDER if (ARTICLES / f).exists()]
    missing = [f for f in ORDER if not (ARTICLES / f).exists()]
    if missing:
        print(f"[WARN] 見つからない記事: {missing}", file=sys.stderr)

    made = 0
    for i, fname in enumerate(files):
        if args.only and args.only not in fname:
            continue
        path = ARTICLES / fname
        slides = build_slides(path, args.max_slides)
        total = len(slides)
        accent = ACCENTS[i % len(ACCENTS)]
        name = fname.replace("article_", "").replace(".txt", "")
        folder = out_root / f"{i:02d}_{name}"
        folder.mkdir(parents=True, exist_ok=True)
        for n, slide in enumerate(slides, 1):
            img = render(slide, i, n, total, accent, W, H)
            img.save(folder / f"{n:02d}.jpg", "JPEG", quality=90, optimize=True)
        made += total
        print(f"[OK] No.{i:02d} {name} … {total}枚")
    print(f"\n完成: {made}枚  →  {out_root}")


if __name__ == "__main__":
    main()
