#!/usr/bin/env python3
"""articles/ 内の記事間の文字参照を、実際のURLリンクに差し替える。

使い方:
  1) tools/links.json の "url" に、公開後のURLを記入する
  2) python tools/apply_links.py --check     … 記入漏れと置換対象の件数を確認
  3) python tools/apply_links.py --dry-run   … 変更内容を表示（ファイルは書き換えない）
  4) python tools/apply_links.py             … 実際に書き換える

形式（--style で選択）:
  note   : 睡眠の記事（https://…）で書いた   ← 既定。note.comはURLを自動リンクする
  md     : [睡眠の記事](https://…)で書いた   ← Markdown対応の媒体向け

何度実行しても二重にリンクが付かないよう、すでにURLが続く参照は飛ばす。
"""
import json, re, sys, glob, os, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, 'articles')
MAP = os.path.join(ROOT, 'tools', 'links.json')


def load():
    with open(MAP, encoding='utf-8') as f:
        return json.load(f)


def build_rules(links, style):
    """(正規表現, 置換関数) の組を、参照名の長い順に作る。"""
    rules = []
    for ref, info in sorted(links.items(), key=lambda kv: -len(kv[0])):
        url = (info.get('url') or '').strip()
        if not url:
            continue
        if ref == '序章':
            # 「序章で書いた」「序章で示した」など
            pat = re.compile(r'序章(?!\s*[（(\[])(?=[でに])')
            rep = (lambda u: (lambda m: f'序章（{u}）'))(url) if style == 'note' \
                  else (lambda u: (lambda m: f'[序章]({u})'))(url)
        else:
            # 「<参照名>の記事」。直後にURLや括弧が続くものは除外（二重防止）
            pat = re.compile(re.escape(ref) + r'の記事(?!\s*[（(\[])')
            if style == 'note':
                rep = (lambda r, u: (lambda m: f'{r}の記事（{u}）'))(ref, url)
            else:
                rep = (lambda r, u: (lambda m: f'[{r}の記事]({u})'))(ref, url)
        rules.append((ref, pat, rep))
    return rules


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='URLの記入状況と対象件数を表示')
    ap.add_argument('--dry-run', action='store_true', help='書き換えずに差分件数を表示')
    ap.add_argument('--style', choices=['note', 'md'], default='note')
    a = ap.parse_args()

    links = load()
    filled = {k: v for k, v in links.items() if (v.get('url') or '').strip()}
    missing = [k for k in links if not (links[k].get('url') or '').strip()]

    if a.check:
        print(f'URL記入済み: {len(filled)} / {len(links)} 件')
        if missing:
            print('未記入:')
            for k in missing:
                print(f'  {k:14} {links[k]["title"]}')
        print()
        rules = build_rules(links, a.style)
        tot = 0
        for f in sorted(glob.glob(os.path.join(ART, '*.txt'))):
            t = open(f, encoding='utf-8').read()
            n = sum(len(p.findall(t)) for _, p, _ in rules)
            tot += n
        print(f'いま置換できる箇所: {tot} 件（style={a.style}）')
        return

    rules = build_rules(links, a.style)
    if not rules:
        print('tools/links.json にURLが1件も記入されていません。先に記入してください。')
        return

    grand = 0
    for f in sorted(glob.glob(os.path.join(ART, '*.txt'))):
        t = orig = open(f, encoding='utf-8').read()
        per = []
        for ref, pat, rep in rules:
            t, n = pat.subn(rep, t)
            if n:
                per.append(f'{ref}×{n}')
        if t != orig:
            grand += 1
            name = os.path.basename(f)
            print(f'{"[dry] " if a.dry_run else ""}{name}: ' + ', '.join(per))
            if not a.dry_run:
                open(f, 'w', encoding='utf-8').write(t)
    print(f'\n{"変更対象" if a.dry_run else "書き換え"}: {grand} ファイル')


if __name__ == '__main__':
    main()
