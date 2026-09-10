"""apply-copy.py — 台本.md の本文を index.html の data-t 要素に流し込む
使い方: python apply-copy.py <site_dir> [<台本.md>]
- 台本の「## キー」ごとに、index.html の data-t="キー" 要素の中身を差し替える
- 本文が「-」なら空にする
- キーが見つからない項目は警告して飛ばす（HTML は壊さない）
"""
import io, os, re, sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

def parse_md(md):
    d = {}; key = None; buf = []
    for line in md.splitlines():
        if line.startswith("## "):
            if key: d[key] = "\n".join(buf).strip()
            key = line[3:].strip(); buf = []
        elif key is not None: buf.append(line)
    if key: d[key] = "\n".join(buf).strip()
    return d

def apply(html, key, text):
    # data-t="key" を持つ開始タグを探し、同名タグの入れ子を数えて閉じタグを特定
    m = re.search(r'<([a-zA-Z][a-zA-Z0-9-]*)\b[^>]*\bdata-t="' + re.escape(key) + r'"[^>]*>', html)
    if not m: return html, False
    tag = m.group(1).lower(); i = m.end(); depth = 1
    tag_re = re.compile(r"<(/?)" + re.escape(tag) + r"\b[^>]*>", re.I)
    while depth:
        n = tag_re.search(html, i)
        if not n: return html, False
        depth += -1 if n.group(1) else 1; i = n.end() if depth else n.start()
    close_start = i
    new = "" if text == "-" else text
    return html[:m.end()] + new + html[close_start:], True

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    site = sys.argv[1].rstrip("/\\"); md_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(site + "-src", "台本.md")
    p = os.path.join(site, "index.html"); html = io.open(p, encoding="utf-8").read()
    d = parse_md(io.open(md_path, encoding="utf-8").read())
    ok = 0; miss = []
    for key, text in d.items():
        html, hit = apply(html, key, text)
        if hit: ok += 1
        else: miss.append(key)
    io.open(p, "w", encoding="utf-8").write(html)
    print(f"反映 {ok} 項目" + (f" / 見つからないキー: {', '.join(miss)}" if miss else ""))

if __name__ == "__main__":
    main()
