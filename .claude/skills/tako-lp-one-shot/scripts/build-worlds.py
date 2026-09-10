# -*- coding: utf-8 -*-
"""build-worlds.py — worlds_data.py（世界観50種）から次を生成する
  recipes/worlds.json        機械可読の辞書（提案・QA が読む）
  recipes/worlds.md          人が読む辞書（Claude/Codex が案を出す時に読む）
  ../Tako_LP_Lookbook/index.html  世界観の見本帳（スキルとは別フォルダ。特典として別配布）
  <out>/prompts.json         見本帳画像の生成用（--prompts <dir>。img が無い世界観だけ）
使い方: python scripts/build-worlds.py [--prompts ../lookbook-src]
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from worlds_data import W

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOOK = os.path.join(os.path.dirname(ROOT), "Tako_LP_Lookbook")   # 見本帳（別フォルダ・別配布）
SIG = {"lightning":"雷撃","ink-splat":"墨","spotlight":"スポットライト","tear":"紙を破く","ripple":"波紋","letters-fall":"文字落下",
       "card-flip":"カード裏返し","stamp":"スタンプ","neon-power":"ネオン点灯","none":"なし（静止で勝つ）","glitch-title":"グリッチ","flare":"信号弾"}
GROUP = {"dark":"ダーク・壮大","light":"明るい・上品","cute":"かわいい・ポップ","retro":"レトロ","nature":"和・自然","business":"ビジネス・テック","genre":"ジャンル（ホラー・SF・ゲーム）","minimal":"ミニマル","cool":"かっこいい・クール","gira":"商材屋（ギラギラ）"}
GROUP_ORDER = ["dark","light","cute","retro","nature","business","genre","minimal","cool","gira"]
FONT_W = {"Noto Sans JP":":wght@400;700;900","Noto Serif JP":":wght@400;600","Shippori Mincho B1":":wght@800","Zen Maru Gothic":":wght@700;900",
          "Zen Kaku Gothic New":":wght@700;900","Playfair Display":":ital,wght@0,400;1,400","Cormorant Garamond":":ital,wght@0,500;1,500",
          "Fredoka":":wght@600;700","Orbitron":":wght@700","M PLUS 1p":":wght@800","Inter Tight":":wght@800","Inter":":wght@400",
          "Klee One":":wght@600","Caveat":":wght@600","BIZ UDPGothic":":wght@700","Zen Old Mincho":":wght@700","Fraunces":":ital,wght@0,600;1,600",
          "Libre Baskerville":":ital,wght@0,700;1,400","M PLUS Rounded 1c":":wght@800","Zen Kaku Gothic Antique":":wght@700","Oswald":":wght@600","Zen Kurenaido":"","Cinzel":":wght@700","Exo 2":":wght@700","Michroma":"","Teko":":wght@600","Black Ops One":"","Rajdhani":":wght@700","Yuji Syuku":"","VT323":"","DotGothic16":"","Press Start 2P":"","Special Elite":"","Bangers":"","Righteous":"","Archivo Black":"","Kosugi Maru":"","Space Mono":":wght@400;700","Bebas Neue":""}
SUBJECT = "a wooden desk by a window with a cup of coffee, an open notebook and a pen"
NEG = ", no text, no letters, no watermark, no logo"

def hx(v):
    h = v.lstrip("#")
    return "#" + "".join(ch*2 for ch in h) if len(h) == 3 else "#" + h
def is_dark(c):
    h = hx(c["bg"])[1:]; r,g,b = int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return (r*299+g*587+b*114)/1000 < 128

# 通し番号（グループ順。見本帳・辞書・案の表で共通）
_n = 0
for _g in GROUP_ORDER:
    for _x in W:
        if _x["group"] == _g: _n += 1; _x["no"] = _n

# ---------- worlds.json ----------
json_path = os.path.join(ROOT, "recipes", "worlds.json")
io.open(json_path, "w", encoding="utf-8").write(json.dumps(W, ensure_ascii=False, indent=1))

# ---------- worlds.md ----------
md = []
md.append(f"# 世界観（World）— {len(W)}種 + custom\n")
md.append("World は「色トークン」「書体2〜3」「質感」「画像プロンプトの接頭辞」「必須装備」「禁止装備」「使える演出」「章番号の例（ARM 01 / 第一幕 など）」のセット。**画風もここに属する。** 見本帳 `lookbook/index.html` に全種の代表画面がある。機械可読版は `recipes/worlds.json`（このファイルと同じ内容。`scripts/build-worlds.py` が両方を生成する。**手で直す時は `scripts/worlds_data.py` を直して再生成**）。\n")
md.append("## 全 World 共通の禁止（`recipes/taste.md`）\n")
md.append("- 写実の象徴物（紋章・メダル・王冠・金塊・宝石）を生成しない。名前の由来（たこ・鷹 など）を紋章にしない。\n- 1つの素材（金グラデ等）を文字・ボタン・枠・粒に全部塗らない。強い色は「1か所」。\n- 明るい World で `cinematic photorealistic` を使わない。イラスト・切り抜き・抽象にする。\n- 英字の箔付け語（PREMIUM / LUXURY / 8 FIGURES 等）を置かない。\n")
md.append("## 選び方\n")
md.append("1. brief の「見た目の希望」を下の表で**グループ**に落とす（複数可）\n2. そのグループの中から、用途（uses）と読者に合う World を**5種類以上**選んで10案に散らす（同じ World は最大2案）\n3. 希望が「おまかせ」なら: 女性寄り → cute+nature / 男性寄り → dark+retro / ビジネス → business+light を混ぜる\n4. 10案の「世界観」列にはここの id をそのまま書く。ユーザーが見本帳で見比べられる\n")
md.append("| 希望 | グループ | 代表 |\n| --- | --- | --- |")
rep = {"dark":"wafu-dark, midnight-navy, deep-ocean, cinema-black","light":"paper-white, ivory-serif, letterpress, newspaper","cute":"pastel-pop-dark, pastel-pop, candy-shop, macaron",
       "retro":"retro-future, showa-kissa, pixel-8bit, riso-poster","nature":"watercolor, sumi-ink, forest-moss, ocean-blue","business":"trust-navy, fintech-emerald, data-dashboard, clinic-clean","genre":"horror-west, horror-jp, sf-space, game-rpg, game-esports, anime-kinetic","minimal":"mono-minimal, minimal-black, minimal-type, gallery-white","cool":"paper-black, neon-tokyo, concrete, carbon-red","gira":"abyss-gold, gold-rush, red-alert, money-green"}
wish = {"dark":"ダーク / 壮大 / 映画っぽく / 静かに重い","light":"上品 / 信頼 / ミニマル / クラフト","cute":"かわいい / ポップ / 元気","retro":"レトロ / 昭和 / 80s / ゲーム",
        "nature":"和風 / 自然 / やさしい / 季節","business":"ビジネス / 医療 / テック / 数字で信頼","genre":"ホラー / SF / ゲーム / アニメ・作品の公式サイト","minimal":"ミニマル / 余白 / 文字だけ","cool":"かっこいい / クール / 硬派 / 速い","gira":"商材屋 / ギラギラ / 黒金 / セール"}
for g in GROUP_ORDER: md.append(f"| {wish[g]} | {g}（{GROUP[g]}） | {rep[g]} |")
md.append("\n## 一覧（id → 名前 / 方向性 / 向く用途）\n")
md.append("| No. | id | 名前 | 方向性 | 向く用途 |\n| --- | --- | --- | --- | --- |")
for x in sorted(W, key=lambda x: x["no"]): md.append(f"| {x['no']} | {x['id']} | {x['name']} | {x['tag']} | {x['uses']} |")
md.append("\n---\n")
n = 0
for g in GROUP_ORDER:
    md.append(f"\n# {GROUP[g]}\n")
    for x in W:
        if x["group"] != g: continue
        n += 1; c = x["colors"]
        md.append(f"## No.{x['no']} {x['id']} — {x['name']}（{x['tag']}）")
        md.append("```css\n:root{--bg:%s;--bg2:%s;--card:%s;--ink:%s;--body:%s;--muted:%s;--line:%s;--accent:%s;--accent-2:%s}\n```" % (c["bg"],c["bg2"],c["card"],c["ink"],c["body"],c["muted"],c["line"],c["accent"],c["accent2"]))
        md.append(f"- 書体: {x['fonts'][0]}（英字・数字）/ {x['fonts'][1]}（見出し）/ {x['fonts'][2]}（本文・キャプション）")
        md.append(f"- 質感: {x['texture']}")
        md.append(f"- 画像接頭辞: `{x['prefix']}`")
        md.append(f"- 必須装備: {' / '.join(x['must'])}")
        md.append(f"- 禁止: {' / '.join(x['forbid'])}")
        md.append(f"- 使える演出: {' / '.join(x['sigs'])}（{' / '.join(SIG[s] for s in x['sigs'])}）")
        md.append(f"- 章番号の例: {x['count']}")
        md.append(f"- KV の被写体例: `{x['kv']}`")
        md.append(f"- 向く用途: {x['uses']}\n")
md.append("---\n\n## custom — ヒアリングで独自 World を作る\n")
md.append("`world: custom` の時は次の6問を**1つのメッセージで**聞く。\n\n1. 好きなサイト・ブランド・雑誌を3つ（URLでも名前でも）\n2. 嫌いな見た目（例: ギラギラ、丸っこい、写真が多い）\n3. 読者に持ってほしい気分を一言（例: 安心、ワクワク、緊張）\n4. 色を3つ（無ければ「おまかせ」）\n5. 文字の印象: やわらかい / 硬い / 手書き / 機械的\n6. 参考画像があれば添付\n")
md.append("答えから次を作り `worlds/custom-<name>.md` に保存する: トークン CSS（上と同じ変数名で）/ 書体2〜3（Google Fonts にあるもの）/ 画像接頭辞（画風・光・質感・色を英語で1行）/ 必須装備3つ / 禁止3つ / 使える演出2〜3。作った World を1段落で説明してから生成に進む。以後は通常の World として指定できる。一番近い既存 World を「ベース」として名指しすると速い（例: ベース = linen-sage、色だけ藍に）。\n")
io.open(os.path.join(ROOT, "recipes", "worlds.md"), "w", encoding="utf-8").write("\n".join(md))

# ---------- lookbook ----------
fams = []
for x in W:
    for f in x["fonts"]:
        if f not in fams: fams.append(f)
fam_q = "&".join("family=" + f.replace(" ", "+") + FONT_W.get(f, "") for f in fams)
def card(x):
    c = x["colors"]; d = is_dark(c); h = x["hero"]; en, jp = x["fonts"][0], x["fonts"][1]
    serif = any(k in jp for k in ("Mincho","Serif","Playfair","Cormorant","Baskerville","Fraunces","Klee","Cinzel","Yuji"))
    wt = 600 if serif else 900
    bg = hx(c["bg"]); r,g,b = int(bg[1:3],16),int(bg[3:5],16),int(bg[5:7],16)
    veil = f"linear-gradient(to top,{bg} 0%,rgba({r},{g},{b},{'.3' if d else '.12'}) 60%)" if d else f"linear-gradient(to top,rgba({r},{g},{b},.96) 0%,rgba({r},{g},{b},.08) 58%)"
    em = c["accent2"] if c["accent2"] != c["accent"] else c["accent"]
    if em.lower() == c["ink"].lower(): em = c["accent"]
    if x["group"] == "cute": btn = f"background:{c['accent']};color:#fff;border-radius:999px;box-shadow:0 4px 0 rgba(0,0,0,.18)"
    elif d: btn = f"border:1px solid {c['accent']};color:{c['ink']};letter-spacing:.2em"
    elif c["accent"].lower() == c["ink"].lower(): btn = f"border-bottom:1px solid {c['ink']};color:{c['ink']};padding:4px 0;letter-spacing:.2em"
    else: btn = f"background:{c['accent']};color:{bg};letter-spacing:.14em"
    emh = f'<span style="color:{em}">{h["em"]}</span>' if h["em"] else ""
    sw = "".join(f'<i style="background:{v}"></i>' for v in dict.fromkeys([c["bg"],c["bg2"],c["ink"],c["accent"],c["accent2"]]))
    body_font = x["fonts"][2]
    sample = f'''<div class="w__type" style="background:{c['bg2']};color:{c['body']}"><p class="w__type-cap" style="font-family:'{en}';color:{c['accent']}">{x['count']}</p><h3 style="font-family:'{jp}';font-weight:{wt};color:{c['ink']}">{x['name']}</h3><p class="w__type-body" style="font-family:'{body_font}'">見出しは {jp}、英字と数字は {en}。本文は {body_font}。強い色は1か所だけ。</p><p class="w__type-num" style="font-family:'{en}';color:{em}">01</p><span class="w__btn w__btn--s" style="{btn}">{h['btn']}</span></div>'''
    return f'''<article class="w" id="{x['id']}" data-g="{x['group']}">
  <div class="w__hero" style="background:{bg}"><img loading="lazy" onerror="this.style.display='none'" src="img/{x['id']}-kv.jpg" alt=""><div class="veil" style="background:{veil}"></div>
    <div class="t"><p class="w__cap" style="font-family:'{en}';color:{c['accent'] if not d or c['accent'].lower()!=c['ink'].lower() else c['muted']}">{h['cap']}</p><h2 class="w__h" style="font-family:'{jp}';font-weight:{wt};color:{c['ink']}">{h['h']}{emh}</h2><span class="w__btn" style="{btn}">{h['btn']}</span></div></div>
  <div class="w__pair"><figure class="w__desk" style="background:{bg}"><img loading="lazy" onerror="this.style.display='none'" src="img/{x['id']}.jpg" alt=""><figcaption>同じ被写体で比較</figcaption></figure>{sample}</div>
  <div class="w__body"><div class="w__name"><i class="w__no">No.{x['no']:03d}</i><b>{x['id'].upper()}</b><span>{x['name']}</span></div><p class="w__tag">{x['tag']}</p>
    <div class="sw">{sw}</div>
    <dl><dt>書体</dt><dd>{' / '.join(x['fonts'])}</dd><dt>質感</dt><dd>{x['texture']}</dd><dt>演出</dt><dd>{' / '.join(SIG[s] for s in x['sigs'])}</dd><dt>章番号の例</dt><dd>{x['count']}</dd><dt>向く用途</dt><dd>{x['uses']}</dd></dl></div>
</article>'''
sections = []
for g in GROUP_ORDER:
    xs = [x for x in W if x["group"] == g]
    sections.append(f'<h2 class="gh" id="g-{g}"><span>{GROUP[g]}</span><small>{len(xs)}種 — No.{xs[0]["no"]:03d}〜{xs[-1]["no"]:03d}</small></h2>\n<section class="grid">\n' + "\n\n".join(card(x) for x in xs) + "\n</section>")
nav = "".join(f'<a href="#g-{g}">{GROUP[g]} {sum(1 for x in W if x["group"]==g)}</a>' for g in GROUP_ORDER)
html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>世界観の見本帳 | Tako_LP_One-Shot</title>
<meta name="description" content="Tako_LP_One-Shot の世界観{len(W)}種。同じ被写体を各世界観の画風で生成し、色・書体・演出を並べて比較できる見本帳。">
<meta name="theme-color" content="#111">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{fam_q}&display=swap" rel="stylesheet">
<style>
:root{{--ink:#151515;--body:#444;--muted:#8a8a8a;--line:#e3e3e3;--paper:#f6f6f4;--accent:#d10a1e}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth;overflow-x:clip}}
body{{margin:0;background:var(--paper);color:var(--body);font-family:"Noto Sans JP",sans-serif;font-size:15px;line-height:1.8;-webkit-font-smoothing:antialiased}}
img{{max-width:100%;display:block}}
h1,h2,h3,p,ul{{margin:0}}ul{{padding:0;list-style:none}}
a{{color:inherit;text-decoration:none}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 clamp(18px,4vw,48px)}}
header.top{{padding:56px 0 28px;border-bottom:1px solid var(--line)}}
.top .en{{font-family:"Bebas Neue",sans-serif;font-size:14px;letter-spacing:.34em;color:var(--accent)}}
.top h1{{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;font-size:clamp(30px,5vw,54px);line-height:1.15;color:var(--ink);margin-top:8px}}
.top p{{margin-top:14px;max-width:44em}}
.tags{{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px;position:sticky;top:0;background:var(--paper);padding:10px 0;z-index:5}}
.tags a{{font-size:12px;font-weight:700;letter-spacing:.08em;border:1px solid var(--line);background:#fff;padding:6px 12px;border-radius:999px;color:var(--ink)}}
.tags a:hover{{border-color:var(--ink)}}
.lead{{margin-top:14px;font-size:15px}}
.lead b{{color:var(--ink)}}
.flow{{display:grid;grid-template-columns:repeat(5,1fr);gap:0;margin-top:18px;counter-reset:f}}
.flow li{{position:relative;background:#fff;border:1px solid var(--line);padding:14px 12px 14px 14px;font-size:12.5px;line-height:1.6;color:var(--ink);display:flex;gap:10px;align-items:flex-start}}
.flow li+li{{margin-left:-1px}}
.flow li::after{{content:"";position:absolute;right:-8px;top:50%;width:14px;height:14px;background:#fff;border-right:1px solid var(--line);border-top:1px solid var(--line);transform:translateY(-50%) rotate(45deg);z-index:1}}
.flow li:last-child::after{{display:none}}
.flow b{{font-family:"Bebas Neue",sans-serif;font-size:26px;line-height:1;color:var(--accent);flex:none}}
.flow li.here{{background:#fff4f5;border-color:var(--accent)}}
.flow li.here::after{{background:#fff4f5;border-color:var(--accent)}}
.flow code,.say code{{font-family:"Noto Sans JP",sans-serif;background:#111;color:#fff;padding:1px 7px;border-radius:3px;font-size:12px}}
.say{{margin-top:14px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:12px}}
.say__t{{font-weight:700;color:var(--muted);letter-spacing:.1em;margin-right:4px}}
.say code{{background:var(--accent);font-size:13px;padding:6px 12px}}
.note{{margin-top:14px;font-size:12.5px;color:var(--muted)}}
@media(max-width:860px){{.flow{{grid-template-columns:1fr}}.flow li+li{{margin-left:0;margin-top:-1px}}.flow li::after{{display:none}}}}
.search{{margin-top:14px;display:flex;gap:10px;align-items:center}}
.search input{{font:inherit;padding:8px 12px;border:1px solid var(--line);border-radius:6px;width:min(100%,360px);background:#fff}}
.gh{{display:flex;flex-direction:column;gap:4px;padding:44px 0 6px;scroll-margin-top:64px}}
.gh span{{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;font-size:24px;color:var(--ink)}}
.gh small{{font-size:12px;color:var(--muted)}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:28px;padding:16px 0 24px}}
@media(max-width:860px){{.grid{{grid-template-columns:1fr}}}}
.w{{border:1px solid var(--line);background:#fff;overflow:hidden;scroll-margin-top:64px}}
.w[hidden]{{display:none}}
.w__hero{{position:relative;aspect-ratio:16/10;overflow:hidden;display:flex;align-items:flex-end;padding:22px}}
.w__hero img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.w__hero .veil{{position:absolute;inset:0}}
.w__hero .t{{position:relative;z-index:1}}
.w__cap{{font-size:11px;letter-spacing:.3em;text-transform:uppercase;margin-bottom:8px}}
.w__h{{font-size:clamp(26px,3.2vw,40px);line-height:1.15}}
.w__btn{{display:inline-block;margin-top:14px;padding:9px 16px;font-size:12px;font-weight:700;letter-spacing:.12em}}
.w__pair{{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line)}}
.w__desk{{margin:0;position:relative;aspect-ratio:4/3;overflow:hidden}}
.w__desk img{{width:100%;height:100%;object-fit:cover}}
.w__desk figcaption{{position:absolute;left:10px;bottom:8px;font-size:10px;letter-spacing:.14em;color:#fff;background:rgba(0,0,0,.45);padding:3px 8px}}
.w__type{{padding:16px 18px;display:flex;flex-direction:column;gap:6px;min-width:0}}
.w__type-cap{{font-size:10px;letter-spacing:.2em}}
.w__type h3{{font-size:20px;line-height:1.2}}
.w__type-body{{font-size:11.5px;line-height:1.6;opacity:.85}}
.w__type-num{{font-size:34px;line-height:1;margin-top:auto}}
.w__btn--s{{margin-top:6px;padding:6px 12px;font-size:11px;align-self:flex-start}}
@media(max-width:480px){{.w__pair{{grid-template-columns:1fr}}}}
.w__body{{padding:18px 20px 22px}}
.w__name{{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}}
.w__name b{{font-family:"Bebas Neue",sans-serif;font-size:26px;letter-spacing:.06em;color:var(--ink)}}
.w__no{{font-style:normal;font-family:"Bebas Neue",sans-serif;font-size:14px;letter-spacing:.12em;color:#fff;background:var(--accent);padding:2px 8px;border-radius:3px}}
.w__name span{{font-size:13px;color:var(--muted)}}
.w__tag{{font-size:11px;font-weight:700;color:var(--accent);letter-spacing:.1em;margin-top:2px}}
.sw{{display:flex;gap:6px;margin:12px 0}}
.sw i{{width:26px;height:26px;border-radius:50%;border:1px solid rgba(0,0,0,.12)}}
dl{{display:grid;grid-template-columns:78px 1fr;gap:4px 12px;font-size:12.5px;margin-top:8px}}
dt{{color:var(--muted);letter-spacing:.06em}}dd{{margin:0;color:var(--ink)}}
footer{{border-top:1px solid var(--line);padding:24px 0 48px;font-size:12px;color:var(--muted);margin-top:40px}}
</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <p class="en">TAKO_LP_ONE-SHOT — LOOKBOOK</p>
  <h1>世界観の見本帳 <small style="font-size:.45em;color:var(--muted);font-weight:700">{len(W)}種</small></h1>
  <p class="lead">世界観 {len(W)}種の見本。<b>スキルで10案が出た時に、番号を見比べるための本</b>です。</p>
  <ol class="flow">
    <li><b>1</b><span>Claude Code で<br><code>スタート</code> と打つ</span></li>
    <li><b>2</b><span>質問に答える<br>方向性を ①〜⑩ から選ぶ</span></li>
    <li><b>3</b><span>デザイン10案が出る<br>各案に世界観の <code>No.</code> が付く</span></li>
    <li class="here"><b>4</b><span>この見本帳で<br>その No. を見比べる</span></li>
    <li><b>5</b><span>番号で返事する<br>→ 完成</span></li>
  </ol>
  <div class="say"><span class="say__t">返事の例</span><code>3番で</code><code>No.023 で作って</code><code>No.012 の色を黒にして</code><code>No.005 と No.041 を混ぜて</code></div>
  <p class="note">上の画像＝その世界観で作ったLPの1画面目。下の画像＝比較用に同じ机を各画風で描いたもの。ここに無い雰囲気は「独自に作って」と言えば6問で作れます。</p>
  <div class="search"><input id="q" type="search" placeholder="No. / id / 用途で絞る。10案の No. リストをそのまま貼り付けても可"><span id="cnt" style="font-size:12px;color:var(--muted)"></span></div>
  <nav class="tags">{nav}</nav>
</header>

{chr(10).join(sections)}

<footer>© Tako_LP_One-Shot — 世界観の見本帳。画像はすべてスキルの手順で生成したもの。10案の「世界観」列は、ここに載っている id で指定できる。「かわいい系」「かっこいい系」の希望を言えば、該当グループの案が3つ以上出る。ここに無い雰囲気は「custom」で6問に答えると作れる。</footer>
</div>
<script>
(function(){{var q=document.getElementById('q'),cnt=document.getElementById('cnt'),cards=[].slice.call(document.querySelectorAll('.w'));
function run(){{var raw=(q.value||'').trim().toLowerCase();var nums=raw.match(/no\.?\s*0*(\d{{1,3}})/g);var set=null;if(nums&&nums.length){{set={{}};nums.forEach(function(t){{var m=t.match(/(\d{{1,3}})$/);if(m)set[('000'+m[1]).slice(-3)]=1;}});}}var v=raw;var n=0;cards.forEach(function(c){{var ok;if(set){{ok=!!set[c.querySelector('.w__no').textContent.replace('No.','')];}}else{{ok=!v||c.textContent.toLowerCase().indexOf(v)>-1||c.id.indexOf(v)>-1;}}c.hidden=!ok;if(ok)n++;}});
document.querySelectorAll('.gh').forEach(function(h){{var s=h.nextElementSibling;h.hidden=![].some.call(s.querySelectorAll('.w'),function(c){{return !c.hidden}});}});cnt.textContent=v?n+' / '+cards.length:'';}}
q.addEventListener('input',run);}})();
</script>
</body>
</html>'''
os.makedirs(os.path.join(LOOK, "img"), exist_ok=True)
io.open(os.path.join(LOOK, "index.html"), "w", encoding="utf-8").write(html)

# ---------- prompts.json ----------
if "--prompts" in sys.argv:
    out = sys.argv[sys.argv.index("--prompts") + 1]; os.makedirs(out, exist_ok=True)
    have = {os.path.splitext(f)[0] for f in os.listdir(os.path.join(LOOK, "img"))} if os.path.isdir(os.path.join(LOOK, "img")) else set()
    jobs = [{"name": x["id"], "size": "1536x1024", "prompt": SUBJECT + ". " + x["prefix"] + NEG} for x in W if x["id"] not in have]
    jobs += [{"name": x["id"] + "-kv", "size": "1536x1024", "prompt": x["kv"] + ". " + x["prefix"] + NEG} for x in W if x["id"] + "-kv" not in have]
    io.open(os.path.join(out, "prompts.json"), "w", encoding="utf-8").write(json.dumps(jobs, ensure_ascii=False, indent=1))
    print("prompts:", len(jobs), "->", os.path.join(out, "prompts.json"))
print("worlds:", len(W), "| fonts:", len(fams))
