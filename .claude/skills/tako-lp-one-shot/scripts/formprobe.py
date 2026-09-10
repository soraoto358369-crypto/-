"""formprobe.py — 登録フォームの URL / 埋め込みコードを解析して、LP に設置する方式を決める
使い方: python formprobe.py "<URL または貼り付けコード>"
出力: JSON 1行 {"kind": ..., "method": ..., ...}

kind:
  line      LINE 友だち追加 URL (lin.ee / line.me)
  embed     <form>/<iframe>/<script> を含む埋め込みコード
  formpage  フォームがあるページ URL（UTAGE / MyASP / オレンジメール / Google フォーム 等）
  page      フォームが見つからないページ URL
method（formpage の時の設置方式。上から順に試す）:
  native    ページの <form> を LP 内に再構築して直接 POST（action と input が取れて、CSRF トークンや JS 必須でない時）
  iframe    ページごと iframe 埋め込み（X-Frame-Options / CSP frame-ancestors で拒否されていない時）
  link      ボタンで遷移
"""
import json, re, sys, urllib.request, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TakoLP/1.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", "ignore"), dict(r.headers)

def parse_forms(html):
    forms = []
    for m in re.finditer(r"<form\b([^>]*)>([\s\S]*?)</form>", html, re.I):
        attrs, body = m.group(1), m.group(2)
        action = (re.search(r'action=["\']([^"\']*)', attrs, re.I) or [None, ""])[1]
        method = (re.search(r'method=["\']([^"\']*)', attrs, re.I) or [None, "get"])[1].lower()
        inputs = []
        for im in re.finditer(r"<(input|select|textarea)\b([^>]*)>", body, re.I):
            a = im.group(2)
            name = (re.search(r'name=["\']([^"\']*)', a, re.I) or [None, ""])[1]
            typ = (re.search(r'type=["\']([^"\']*)', a, re.I) or [None, im.group(1)])[1].lower()
            val = (re.search(r'value=["\']([^"\']*)', a, re.I) or [None, ""])[1]
            req = bool(re.search(r"\brequired\b", a, re.I))
            if name: inputs.append({"name": name, "type": typ, "value": val if typ == "hidden" else "", "required": req})
        forms.append({"action": action, "method": method, "inputs": inputs})
    return forms

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    src = sys.argv[1].strip()
    out = {"input": src[:80]}
    if re.search(r"https?://(lin\.ee|line\.me)/", src):
        out.update(kind="line", method="line", url=src); print(json.dumps(out, ensure_ascii=False)); return
    if re.search(r"<(form|iframe|script)\b", src, re.I):
        out.update(kind="embed", method="embed", hosts=sorted(set(re.findall(r"https?://([^/\"'\s]+)", src))))
        print(json.dumps(out, ensure_ascii=False)); return
    if not re.match(r"https?://", src):
        out.update(kind="unknown"); print(json.dumps(out, ensure_ascii=False)); return
    try:
        html, headers = fetch(src)
    except Exception as e:
        out.update(kind="page", method="link", url=src, error=str(e)[:80]); print(json.dumps(out, ensure_ascii=False)); return
    h = {k.lower(): v for k, v in headers.items()}
    xfo = h.get("x-frame-options", "").upper()
    csp = h.get("content-security-policy", "")
    frame_blocked = xfo in ("DENY", "SAMEORIGIN") or "frame-ancestors" in csp and "*" not in csp
    forms = parse_forms(html)
    forms = [f for f in forms if any(i["type"] in ("email", "text", "tel") for i in f["inputs"])]
    out.update(kind="formpage" if forms else "page", url=src, frame_blocked=frame_blocked, vendor=guess_vendor(src, html))
    if forms:
        f = forms[0]
        csrf = any(re.search(r"token|csrf|nonce|_key", i["name"], re.I) for i in f["inputs"])
        jsdriven = bool(re.search(r"(recaptcha|hcaptcha|turnstile)", html, re.I))
        out["form"] = f
        if f["action"] and f["method"] == "post" and not csrf and not jsdriven: out["method"] = "native"
        elif not frame_blocked: out["method"] = "iframe"
        else: out["method"] = "link"
        out["reason"] = ("csrf" if csrf else "") + ("captcha" if jsdriven else "")
    else:
        out["method"] = "iframe" if not frame_blocked and re.search(r"<input\b", html, re.I) else "link"
    print(json.dumps(out, ensure_ascii=False))

def guess_vendor(url, html):
    for key, name in (("utage", "UTAGE"), ("myasp", "MyASP"), ("orange", "オレンジメール"), ("docs.google.com/forms", "Google フォーム"), ("notion", "Notion"), ("convertkit", "ConvertKit"), ("brevo", "Brevo"), ("mailchimp", "Mailchimp"), ("lstep", "Lステップ"), ("prolinefree", "ProLine")):
        if key in url.lower() or key in html.lower()[:20000]: return name
    return ""

if __name__ == "__main__":
    main()
