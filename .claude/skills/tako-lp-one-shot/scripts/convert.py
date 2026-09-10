"""convert.py — 生成 PNG / 持ち込み画像を公開用 JPG に変換する
使い方: python convert.py <src_dir> <site_dir> [--ogp kv] [--quality 84]
- <src_dir> の png/jpg/webp を <site_dir>/assets/img/<name>.jpg に保存（EXIF 除去、プログレッシブ）
- --ogp で指定した画像から 1200x630 の ogp.jpg を切り出す（既定: kv があれば kv）
- 長辺 2000px を超える画像は縮小
"""
import glob, os, sys
from PIL import Image

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    src, site = sys.argv[1], sys.argv[2]
    ogp = "kv"; q = 84
    if "--ogp" in sys.argv: ogp = sys.argv[sys.argv.index("--ogp") + 1]
    if "--quality" in sys.argv: q = int(sys.argv[sys.argv.index("--quality") + 1])
    dst = os.path.join(site, "assets", "img"); os.makedirs(dst, exist_ok=True)
    files = []
    for ext in ("png", "jpg", "jpeg", "webp"): files += glob.glob(os.path.join(src, f"*.{ext}"))
    if not files: print("no images in", src); sys.exit(1)
    names = []
    for p in sorted(files):
        name = os.path.splitext(os.path.basename(p))[0]; names.append(name)
        im = Image.open(p).convert("RGB")
        w, h = im.size
        if max(w, h) > 2000:
            s = 2000 / max(w, h); im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
        im.save(os.path.join(dst, name + ".jpg"), "JPEG", quality=q, optimize=True, progressive=True)  # exif は渡さない = 除去
        print("ok", name, im.size)
    key = ogp if ogp in names else names[0]
    im = Image.open(os.path.join(dst, key + ".jpg"))
    w, h = im.size; tw, th = 1200, 630; s = max(tw / w, th / h)
    im2 = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    l = (im2.width - tw) // 2; t = int((im2.height - th) * 0.45)
    im2.crop((l, t, l + tw, t + th)).save(os.path.join(dst, "ogp.jpg"), "JPEG", quality=85, optimize=True)
    print("ogp from", key)

if __name__ == "__main__":
    main()
