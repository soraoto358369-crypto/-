"""copyify.py — index.html の文言要素に data-t="キー" を振り、台本.md を書き出す
使い方: python copyify.py <site_dir> [<out_md>]
- 対象: 見出し・本文・ボタン・リストなど（下の TARGET）。script/style/svg の中は触らない
- すでに data-t がある要素はそのキーを使う（再実行しても安定）
- 出力: <site>-src/台本.md（既定）。「## キー」の下に本文。<br> と <em>強調</em> は使える
その後は apply-copy.py（1回反映）か watch-copy.py（保存のたびに自動反映）を使う
"""
import io, os, re, sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

TARGET_CLASSES = {"lv", "h2", "p", "say", "ps", "hero__sub", "hero__lead", "hero__h1", "eyebrow", "from__p", "from__link", "mid__t", "price__note", "demo__note", "ba__cap", "node__n", "fin__p", "timer__cap", "timer__sub", "hero__note", "sec__no", "sec__title", "id__tag", "id__jp"}
TARGET_TAGS = {"h1", "h2", "h3", "dt", "dd", "li", "figcaption"}
TARGET_BTN = "btn"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
SKIP = {"script", "style", "svg", "canvas", "iframe", "noscript"}
TAG_RE = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9-]*)([^>]*?)(/?)>")

def tokenize(html):
    """(start, end, close?, tag, attrs, selfclosing) を順に返す。コメントは飛ばす"""
    i = 0
    while True:
        m = TAG_RE.search(html, i)
        if not m: return
        if html.startswith("<!--", m.start()):
            j = html.find("-->", m.start()); i = j + 3 if j >= 0 else len(html); continue
        yield m.start(), m.end(), bool(m.group(1)), m.group(2).lower(), m.group(3), bool(m.group(4))
        i = m.end()

def elements(html):
    """対象要素の (tag, attrs, open_start, open_end, close_start, close_end) を文書順で返す"""
    stack = []; out = []; skip_depth = 0
    for s, e, closing, tag, attrs, selfc in tokenize(html):
        if tag in VOID or selfc: continue
        if not closing:
            if tag in SKIP or skip_depth: skip_depth += 1; stack.append((tag, s, e, True)); continue
            stack.append((tag, s, e, False))
        else:
            # スタックから同名の直近を探す
            for k in range(len(stack) - 1, -1, -1):
                if stack[k][0] == tag:
                    t, os_, oe, skipped = stack[k]; del stack[k:]
                    if skipped: skip_depth = max(0, skip_depth - 1); break
                    out.append((t, attrs_of(html, os_, oe), os_, oe, s, e)); break
    out.sort(key=lambda x: x[2]); return out

def attrs_of(html, os_, oe):
    m = TAG_RE.match(html, os_); return m.group(3) if m else ""

def classes(attrs):
    m = re.search(r'class=["\']([^"\']*)', attrs); return set(m.group(1).split()) if m else set()

def is_target(tag, attrs, html, os_, oe, cs):
    cl = classes(attrs)
    if cl & TARGET_CLASSES: return True
    if TARGET_BTN in cl: return True
    if tag in TARGET_TAGS: return True
    return False

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    site = sys.argv[1].rstrip("/\\"); out_md = sys.argv[2] if len(sys.argv) > 2 else os.path.join(site + "-src", "台本.md")
    p = os.path.join(site, "index.html"); html = io.open(p, encoding="utf-8").read()
    els = elements(html)
    # 親に対象があるなら子は対象にしない（入れ子の二重編集を防ぐ）
    chosen = []; last_end = -1
    for tag, attrs, os_, oe, cs, ce in els:
        if not is_target(tag, attrs, html, os_, oe, cs): continue
        if os_ < last_end: continue
        inner = html[oe:cs]
        if not inner.strip() or len(re.sub(r"<[^>]+>", "", inner).strip()) < 1: continue
        chosen.append((tag, attrs, os_, oe, cs, ce)); last_end = ce
    # キーを振る（既存 data-t を尊重）。セクション id/data-lv を接頭に
    sec_key = "top"; counters = {}; edits = []; entries = []
    for tag, attrs, os_, oe, cs, ce in chosen:
        # 直前の <section ...> を探して接頭辞に
        secm = list(re.finditer(r'<section\b([^>]*)>', html[:os_]))
        if secm:
            a = secm[-1].group(1); idm = re.search(r'id="([^"]+)"', a); lvm = re.search(r'data-lv="([^"]+)"', a)
            sec_key = idm.group(1) if idm else ("lv" + lvm.group(1) if lvm else "sec")
        elif "timer" in attrs or "loader" in attrs: sec_key = "top"
        m = re.search(r'data-t="([^"]+)"', attrs)
        if m: key = m.group(1)
        else:
            cl = classes(attrs); base = next(iter(cl & TARGET_CLASSES), None) or (TARGET_BTN if TARGET_BTN in cl else tag)
            base = base.replace("__", "-")
            n = counters.get((sec_key, base), 0) + 1; counters[(sec_key, base)] = n
            key = f"{sec_key}.{base}" + (f".{n}" if n > 1 or base in ("li", "dt", "dd", "h3", "btn") else "")
            edits.append((oe - 1, f' data-t="{key}"'))  # 開始タグの > の直前に挿入
        entries.append((key, html[oe:cs].strip()))
    # 挿入（後ろから）
    for pos, ins in sorted(edits, key=lambda x: -x[0]):
        html = html[:pos] + ins + html[pos:]
    io.open(p, "w", encoding="utf-8").write(html)
    os.makedirs(os.path.dirname(out_md), exist_ok=True)
    with io.open(out_md, "w", encoding="utf-8") as f:
        f.write(f"# 台本 — {os.path.basename(site)}\n\n")
        f.write("「## キー」の下の本文を書き換えて保存すると、ページに反映されます（watch-copy.py 実行中なら自動、そうでなければ apply-copy.py）。\n")
        f.write("使える記法: <br>（改行）、<em>強調</em>（赤）、<b>太字</b>。キーの行は変えないでください。行を消しても要素は消えません（空にしたい時は本文を「-」にする）。\n\n")
        for key, text in entries:
            f.write(f"## {key}\n{text}\n\n")
    print(f"data-t: {len(edits)} 追加 / 台本: {len(entries)} 項目 → {out_md}")

if __name__ == "__main__":
    main()
