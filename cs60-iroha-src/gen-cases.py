"""症例ギャラリーを cases.json から生成する。
使い方: python cs60-iroha-src/gen-cases.py
  1. cs60-iroha-src/cases/<年代>/*.png|jpg を 600px 幅 JPEG に変換（上下の文字帯を切り落とす）
  2. cases.json の数値から figcaption を組み、index.html の症例セクションを差し替える
  3. brief.md の numbers_ok に数値を登録（QA の数字チェックを通すため）
写真と JSON の件数が合わない場合は中断する（取り違えを防ぐ）。
"""
import json, os, glob, re, sys
from PIL import Image, ImageOps

W, Q = 600, 80
ROOT = "cs60-iroha"; SRC = "cs60-iroha-src"
data = json.load(open(f"{SRC}/cases.json", encoding="utf-8"))
ages = [k for k in ("20", "30", "40", "50") if data.get(k)]
dst = f"{ROOT}/assets/img/cases"; os.makedirs(dst, exist_ok=True)

size = None; total = 0
for age in ages:
    # 末尾の数字で並べる。文字列順だと c40_10 が c40_2 より前に来て、
    # 写真と説明文の対応がずれる（別の方の数値が表示される）。
    def _num(f):
        m = re.search(r"_(\d+)\.[a-z]+$", f)
        return int(m.group(1)) if m else 0
    files = sorted(glob.glob(f"{SRC}/cases/{age}/*.png") + glob.glob(f"{SRC}/cases/{age}/*.jpg"), key=_num)
    if len(files) != len(data[age]):
        sys.exit(f"[NG] {age}代: 写真 {len(files)}枚 と cases.json {len(data[age])}件 が一致しません")
    for i, p in enumerate(files, 1):
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        iw, ih = im.size
        im = im.crop((0, int(ih * 0.085), iw, int(ih * 0.772)))   # 上下の焼き込み文字を落とす
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        im.save(f"{dst}/c{age}_{i}.jpg", "JPEG", quality=Q, optimize=True, progressive=True)
        size = im.size
        total += os.path.getsize(f"{dst}/c{age}_{i}.jpg")

# 体重の前後差と、画像に焼き込まれた delta が合うか照合する。
# 合わない場合は景表法上のリスクになりうるので必ず報告する（自動修正はしない）。
def _n(v): return float(v.rstrip("kg%"))
mismatch = []
for age in ages:
    for i, c in enumerate(data[age], 1):
        calc = round(_n(c["before"]) - _n(c["after"]), 1)
        if abs(calc - _n(c["delta"])) > 0.05:
            mismatch.append(f'{age}代{i}件目 {c["age"]}{c["h"]}: {c["before"]}-{c["after"]}={calc}kg / 表示 -{c["delta"]}')
if mismatch:
    print("[要確認] 体重差と表示値が一致しない症例:")
    for m in mismatch: print("  -", m)

blocks = []
for age in ages:
    items = "\n".join(
        f'''        <figure class="case">
          <img src="assets/img/cases/c{age}_{i}.jpg" alt="{c['age']}女性 3ヶ月コースのビフォーアフター {c['delta']}減"
               width="{size[0]}" height="{size[1]}" loading="lazy" decoding="async">
          <figcaption>
            <span>{c['age']}・女性／身長{c['h']}</span>
            <span>体重 {c['before']} → {c['after']}</span>
            <span>体脂肪率 {c['bf']} → {c['af']}</span>
          </figcaption>
        </figure>''' for i, c in enumerate(data[age], 1))
    blocks.append(f'''    <section class="age">
      <h3 class="age__h"><span>{age}代</span><small>3ヶ月コース／{len(data[age])}件</small></h3>
      <div class="cases">
{items}
      </div>
    </section>''')

sec = ('  <div class="ages">\n' + "\n".join(blocks) + "\n  </div>\n")
html = open(f"{ROOT}/index.html", encoding="utf-8").read()
html = re.sub(r'  <div class="ages">.*?\n  </div>\n', sec, html, count=1, flags=re.S)
open(f"{ROOT}/index.html", "w", encoding="utf-8").write(html)

# brief.md の numbers_ok を更新（症例ブロックだけ入れ替える）
nums = []
# 見出しの「N件」もページ本文に出るので登録する（QA の数字チェック対象）
nums.append("  - " + "; ".join(f'"{len(data[age])}件"' for age in ages)
            + f'; "{sum(len(data[a]) for a in ages)}件"')
for age in ages:
    for c in data[age]:
        nums.append(f'  - "{c["before"]}"; "{c["after"]}"; "{c["delta"]}"; "{c["bf"]}"; "{c["af"]}"; "{c["age"]}"; "{c["h"]}"')
block = "# --- 症例の実測値（画像に焼き込まれた値。表記のまま） ---\n" + "\n".join(nums)
b = open(f"{SRC}/brief.md", encoding="utf-8").read()
b = re.sub(r"# --- 症例の実測値.*?(?=\n\w|\n#(?! ---)|\Z)", block, b, flags=re.S) if "# --- 症例の実測値" in b \
    else b.replace('numbers_ok:', block + "\nnumbers_ok:")
open(f"{SRC}/brief.md", "w", encoding="utf-8").write(b)

print(f"生成: {sum(len(data[a]) for a in ages)}件 / 画像 {total/1024/1024:.2f}MB / 1枚 {size[0]}x{size[1]}")
print("件数:", {a: len(data[a]) for a in ages})
