"""年代別ビフォーアフター画像を公開用に変換する。
使い方: python cs60-iroha-src/build-cases.py 20 30 40 50
  cs60-iroha-src/cases/<年代>/*.png|jpg → cs60-iroha/assets/img/cases/c<年代>_<n>.jpg
  600px幅・品質80・EXIF除去・プログレッシブ。
"""
import sys, os, glob
from PIL import Image, ImageOps
W, Q = 600, 80
dst = "cs60-iroha/assets/img/cases"; os.makedirs(dst, exist_ok=True)
total = 0
for age in (sys.argv[1:] or ["20", "30", "40", "50"]):
    files = sorted(glob.glob(f"cs60-iroha-src/cases/{age}/*.png") + glob.glob(f"cs60-iroha-src/cases/{age}/*.jpg"))
    for i, p in enumerate(files, 1):
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        # 上の「3ヶ月コース」帯と下の数値帯を落とす。数値は HTML の figcaption 側で出す
        # （画像とテキストで数字が二重になるのと、赤字が檜の色調とぶつかるのを避ける）
        iw, ih = im.size
        im = im.crop((0, int(ih * 0.085), iw, int(ih * 0.772)))
        s = W / im.width
        im = im.resize((W, round(im.height * s)), Image.LANCZOS)
        out = f"{dst}/c{age}_{i}.jpg"
        im.save(out, "JPEG", quality=Q, optimize=True, progressive=True)  # exif を渡さない = 除去
        total += os.path.getsize(out)
    if files: print(f"{age}代: {len(files)}枚")
print(f"cases 合計 {total/1024/1024:.2f}MB")
