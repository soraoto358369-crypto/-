"""qa.py — 納品前の自動検査。全部 PASS になるまで納品しない。
使い方: python qa.py <site_dir> [brief.md]
検査:
 1 HTML の開閉タグ一致
 2 参照ファイル（src/href の相対パス）が全部存在
 3 総重量 3MB 以下
 4 外部通信が fonts.googleapis.com / fonts.gstatic.com / cdnjs.cloudflare.com 以外にない
 5 <title> / description / og:image / theme-color がある
 6 prefers-reduced-motion の分岐がある
 7 画像の EXIF が空
 8 brief があり subject が person/product/service の時、本文の数字（単位付き）が facts に含まれる
 9 brief に subject: work か fictional: true がある時、「架空」がフッターにある
出力: qa-report.md を <site_dir> の隣（<site_dir>-src/ があればそこ）に書く
"""
import os, re, sys
from html.parser import HTMLParser
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
ALLOWED_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdnjs.cloudflare.com")

class TagCheck(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.errors = []; self.refs = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("src", "href") and v: self.refs.append(v)
        if tag not in VOID: self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack: self.errors.append(f"閉じタグ </{tag}> に対応する開始タグがない {self.getpos()}"); return
        if self.stack[-1][0] != tag:
            self.errors.append(f"</{tag}> が来たが開いているのは <{self.stack[-1][0]}> {self.getpos()}")
            # 回復: スタックから探す
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag: del self.stack[i:]; break
        else: self.stack.pop()

def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    extra = []
    if "--allow" in sys.argv:
        i = sys.argv.index("--allow"); extra = [h.strip() for h in sys.argv[i + 1].split(",")]
        if sys.argv[i + 1] in args: args.remove(sys.argv[i + 1])
    global ALLOWED_HOSTS; ALLOWED_HOSTS = tuple(ALLOWED_HOSTS) + tuple(extra)
    site = args[0].rstrip("/\\"); brief = args[1] if len(args) > 1 else None
    results = []
    def rec(ok, name, detail=""): results.append((ok, name, detail))
    html_files = [os.path.join(dp, f) for dp, _, fs in os.walk(site) for f in fs if f.endswith(".html")]
    css_js = [os.path.join(dp, f) for dp, _, fs in os.walk(site) for f in fs if f.endswith((".css", ".js"))]
    all_text = "".join(read(p) for p in html_files + css_js)
    # 1,2
    refs = []
    for hf in html_files:
        p = TagCheck(); p.feed(read(hf)); refs += [(hf, r) for r in p.refs]
        rec(not p.errors and not p.stack, f"タグ整合: {os.path.relpath(hf, site)}", "; ".join(p.errors[:3]) + (f"; 未閉鎖 {[t for t,_ in p.stack][:3]}" if p.stack else ""))
    missing = []
    for hf, r in refs:
        # 外部URL(リンク先)はここでは見ない。通信の検査は下の「許可ホスト」で行う
        if r.startswith(("http://", "https://", "//")): continue
        if r.startswith(("#", "mailto:", "tel:", "data:", "javascript:")): continue
        path = os.path.normpath(os.path.join(os.path.dirname(hf), r.split("?")[0].split("#")[0]))
        if not os.path.exists(path): missing.append(r)
    rec(not missing, "参照ファイルが全部存在", ", ".join(missing[:5]))
    # 3
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(site) for f in fs)
    rec(total <= 3 * 1024 * 1024, f"総重量 {total/1024/1024:.2f}MB (上限 3MB)")
    # 4: 実際に通信が発生する参照だけを見る（<a href> のリンク先は対象外）
    res = re.findall(r'\bsrc=["\'](?:https?:)?//([^/"\']+)', all_text)
    res += re.findall(r'<link\b[^>]*?\bhref=["\'](?:https?:)?//([^/"\']+)', all_text, re.I)
    res += re.findall(r'\b(?:fetch|importScripts)\(\s*["\'](?:https?:)?//([^/"\']+)', all_text)
    res += re.findall(r'@import\s+(?:url\()?["\'](?:https?:)?//([^/"\']+)', all_text)
    bad = sorted({h for h in res if h not in ALLOWED_HOSTS})
    rec(not bad, "外部通信は許可ホストのみ", ", ".join(bad))
    # 5
    idx = read(os.path.join(site, "index.html")) if os.path.exists(os.path.join(site, "index.html")) else ""
    for key, pat in (("<title>", r"<title>[^<]+</title>"), ("description", r'name="description"'), ("og:image", r'property="og:image"'), ("theme-color", r'name="theme-color"')):
        rec(bool(re.search(pat, idx)), f"メタ: {key}")
    # 6
    rec("prefers-reduced-motion" in all_text, "prefers-reduced-motion の分岐")
    # 7
    try:
        from PIL import Image
        exif_bad = []
        for dp, _, fs in os.walk(site):
            for f in fs:
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    ex = Image.open(os.path.join(dp, f)).getexif()
                    if len(ex): exif_bad.append(f)
        rec(not exif_bad, "画像 EXIF なし", ", ".join(exif_bad))
    except ImportError:
        rec(False, "画像 EXIF なし", "Pillow 未導入")
    # 8,9 brief
    if brief and os.path.exists(brief):
        b = read(brief)
        subject = (re.search(r"^subject:\s*(\w+)", b, re.M) or [None, ""])[1]
        fictional = bool(re.search(r"^fictional:\s*true", b, re.M)) or subject == "work"
        text = re.sub(r"<[^>]+>", " ", idx)
        text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", text)
        nums = set(re.findall(r"[0-9０-９][0-9０-９,\.]*\s*(?:%|％|円|万|部|人|件|名|回|倍|時間|日|年|kg|km)", text))
        if subject in ("person", "product", "service") and not fictional:
            # facts に加えて numbers_ok:（実績ではない数字表現。「3ステップ」「24時間」など）も許可
            allowed = re.sub(r"[\s,]", "", b)
            unknown = [n for n in nums if re.sub(r"[\s,]", "", n) not in allowed]
            rec(not unknown, "数字は brief の facts / numbers_ok 由来のみ", ", ".join(sorted(unknown)[:8]) + ("  → brief の numbers_ok: に追記して再実行" if unknown else ""))
        if fictional:
            rec("架空" in text, "架空の明記（フッター）")
    else:
        rec(True, "brief なし: 数字・架空チェックはスキップ")
    # report
    lines = ["# QA report", f"site: {site}", ""] + [f"- [{'PASS' if ok else 'FAIL'}] {n}" + (f" — {d}" if d else "") for ok, n, d in results]
    out_dir = site + "-src" if os.path.isdir(site + "-src") else os.path.dirname(site) or "."
    with open(os.path.join(out_dir, "qa-report.md"), "w", encoding="utf-8") as f: f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    fails = [r for r in results if not r[0]]
    print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL'}")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
