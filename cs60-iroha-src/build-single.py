"""単一ファイル版を作る（CSS/JS/画像37枚を1つの HTML に埋め込む）。
使い方: python cs60-iroha-src/build-single.py
出力: cs60-iroha-lp.html  ダブルクリックで開ける。サーバー不要・外部依存なし
      （Google Fonts と GSAP のみ CDN から取得。オフラインでも崩れない）
"""
import re, base64, pathlib, mimetypes
site = pathlib.Path("cs60-iroha")
html = (site / "index.html").read_text(encoding="utf-8")
css = (site / "assets/css/style.css").read_text(encoding="utf-8")
js = (site / "assets/js/main.js").read_text(encoding="utf-8")
title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
cache = {}
def repl(m):
    rel = m.group(1)
    if rel not in cache:
        p = site / rel
        mt = mimetypes.guess_type(str(p))[0] or "image/jpeg"
        cache[rel] = f"data:{mt};base64," + base64.b64encode(p.read_bytes()).decode()
    return f'src="{cache[rel]}"'
body = html.split("<body>", 1)[1].split("</body>", 1)[0]
body = re.sub(r'src="(assets/img/[^"]+)"', repl, body)
body = body.replace('<script src="assets/js/main.js"></script>', "")
body = re.sub(r'\n<script src="https://cdnjs[^>]+></script>', "", body)
head = html.split("<head>", 1)[1].split("</head>", 1)[0]
head = re.sub(r'\n *<link rel="stylesheet" href="assets/[^"]+">', "", head)
head = re.sub(r'\n *<link rel="icon"[^>]+>', "", head)
out = (f"<!doctype html>\n<html lang=\"ja\">\n<head>{head}\n<style>\n{css}\n</style>\n</head>\n<body>{body}\n"
       '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
       '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>\n'
       f"<script>\n{js}\n</script>\n</body>\n</html>\n")
pathlib.Path("cs60-iroha-lp.html").write_text(out, encoding="utf-8")
print(f"cs60-iroha-lp.html  {len(out.encode())/1024/1024:.2f}MB  画像 {len(cache)}枚を埋め込み")
