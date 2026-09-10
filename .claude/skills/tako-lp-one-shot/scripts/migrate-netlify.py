# -*- coding: utf-8 -*-
"""migrate-netlify.py — Netlify に上げてある既存サイトを手元に取り出す（Cloudflare Pages への移行用）
使い方: python scripts/migrate-netlify.py <netlify のサイト名 or URL> [<保存先フォルダ>]
  例:   python scripts/migrate-netlify.py https://xxxx-yyyy-123456.netlify.app  ./mysite
前提: Netlify にログイン済み（初回は `npx -y netlify-cli login` → ブラウザで Authorize）
動き: Netlify の API から公開中のファイル一覧を取り、全部ダウンロードして <保存先> に置く。
      Netlify 側が 503（usage_exceeded）で止まっていても API は使えるので取り出せる。
その後: 「公開して」（scripts/publish.ps1 -Dir <保存先> -Name <名前>）で Cloudflare Pages に上げる。
"""
import io, json, os, sys, subprocess, urllib.request, urllib.parse
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

def token():
    cands = [os.path.join(os.environ.get("APPDATA", ""), "netlify", "Config", "config.json"),
             os.path.expanduser("~/Library/Preferences/netlify/config.json"),
             os.path.expanduser("~/.config/netlify/config.json")]
    for p in cands:
        if os.path.exists(p):
            try:
                d = json.load(io.open(p, encoding="utf-8"))
                for u in d.get("users", {}).values():
                    t = u.get("auth", {}).get("token")
                    if t: return t
            except Exception: pass
    return os.environ.get("NETLIFY_AUTH_TOKEN")

def api(path, tok, raw=False):
    req = urllib.request.Request("https://api.netlify.com/api/v1" + path, headers={"Authorization": "Bearer " + tok, **({"Content-Type": "application/vnd.bitballoon.v1.raw"} if raw else {})})
    return urllib.request.urlopen(req, timeout=60).read()

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    tok = token()
    if not tok: print("[NG ] Netlify にログインしていません → npx -y netlify-cli login を実行してから再度"); sys.exit(1)
    key = sys.argv[1].strip().rstrip("/")
    name = urllib.parse.urlparse(key).netloc if key.startswith("http") else key
    name = name.replace(".netlify.app", "")
    sites = json.loads(api("/sites?per_page=200", tok))
    site = next((s for s in sites if s.get("name") == name or s.get("url", "").rstrip("/").endswith(name)), None)
    if not site: print("[NG ] サイトが見つかりません:", name, "/ あるもの:", ", ".join(s.get("name", "") for s in sites)); sys.exit(1)
    sid = site["id"]; out = sys.argv[2] if len(sys.argv) > 2 else name
    files = json.loads(api("/sites/%s/files" % sid, tok))
    os.makedirs(out, exist_ok=True); n = 0
    for f in files:
        p = f["path"]
        if p.startswith("/.netlify/"): continue
        dst = os.path.join(out, p.lstrip("/")); os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "wb").write(api("/sites/%s/files%s" % (sid, urllib.parse.quote(p)), tok, raw=True)); n += 1
    print("[OK ] %s から %d ファイルを %s/ に取り出しました" % (site.get("url", name), n, out))
    print("      次: 「公開して」か  powershell -File scripts/publish.ps1 -Dir %s -Name %s" % (out, name.split("-")[0] if name.count("-") >= 2 else name))
    if os.path.exists(os.path.join(out, "index.html")):
        h = io.open(os.path.join(out, "index.html"), encoding="utf-8", errors="ignore").read()
        if "data-netlify" in h: print("[!! ] index.html に Netlify Forms（data-netlify）があります。Cloudflare では動かないので、フォームを gform / embed / line に変えてください（parts/forms.md）")
        if ".netlify.app" in h: print("[!! ] index.html の中に .netlify.app への URL があります。移行後の URL に貼り替えてください")

if __name__ == "__main__": main()
