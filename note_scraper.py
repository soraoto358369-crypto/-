"""
note_scraper.py - note 売れ筋有料記事リサーチ（非公式API版）

Selenium/Chrome は使わず、note の公開JSON API（api/v3/searches 等）から
売れ筋の有料記事を収集する。note-research_ver4 のAPIロジックをPythonへ移植。

使い方:
  python note_scraper.py --keyword "副業"              # キーワードで検索
  python note_scraper.py --keyword "投資" --pages 5     # 探索量（ソートごとのページ数）
  python note_scraper.py --keyword "AI" --min-price 3000 # 最低価格
  python note_scraper.py --keyword "恋愛" --limit 50    # 出力件数（ブレンド後）

出力:
  テーマ/scrape_result_{keyword}_{timestamp}.txt  に結果を保存
  標準出力に [DATA_START] … JSON … [DATA_END] を表示（Claude Code が読み取る）

ブレンド選定（パクリ回避）:
  A群=今売れている(24h購入シグナル) / B群=スキが多い(普遍的人気) / C群=急上昇・新着
  を A:B:C ≒ 4:4:2 で混ぜて出力する。
"""

import os
import sys
import json
import time
import argparse
import threading
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Windows コンソール文字化け対策
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ==============================
# 設定
# ==============================
BASE_DIR = Path(__file__).parent
_CONFIG_FILE = BASE_DIR / "config.json"
THEME_DIR = BASE_DIR / "テーマ"

NOTE_API_BASE = "https://note.com/api/v3"

# note へ礼儀正しくアクセスする設定（403/429 を出にくくする）
REQUEST_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ja,en-US;q=0.9,en;q=0.8",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
}
REQUEST_GAP_MS = 80        # 全リクエストを最低この間隔に揃える
REQUEST_TIMEOUT = 15       # 秒
PAGE_SIZE = 50             # 1ページ取得件数
HYDRATE_CONCURRENCY = 5    # 詳細取得の同時実行数（noteへの負荷を抑える）
HYDRATE_CAP = 80           # 詳細取得（売れシグナル判定）の上限件数
# 売れシグナル & スキ を両方拾うため複数ソートを統合する
SORTS = ["popular", "hot", "new", "like"]
SORT_LABEL = {"popular": "定番", "hot": "急上昇", "new": "新着", "like": "スキ"}

_next_request_at = 0.0           # スロットル用
_throttle_lock = threading.Lock()
_cache = {}                      # URL -> json（実行中の重複取得を防ぐ）


# ==============================
# HTTP（スロットル・429リトライ・タイムアウト）
# ==============================
def _throttle():
    """全リクエストの開始を REQUEST_GAP_MS ずつずらす（複数スレッドでも安全）。"""
    global _next_request_at
    if REQUEST_GAP_MS <= 0:
        return
    with _throttle_lock:
        now = time.time()
        scheduled = max(now, _next_request_at)
        _next_request_at = scheduled + REQUEST_GAP_MS / 1000.0
        wait = scheduled - now
    if wait > 0:
        time.sleep(wait)


def fetch_json(url):
    """note API を GET。429 は retry-after 待機で1回だけ再試行。失敗時 None。"""
    if url in _cache:
        return _cache[url]
    for attempt in range(2):
        _throttle()
        try:
            req = Request(url, headers=REQUEST_HEADERS)
            with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
                _cache[url] = data
                return data
        except HTTPError as e:
            if e.code == 429 and attempt == 0:
                retry_after = 2
                try:
                    retry_after = int(e.headers.get("retry-after") or 2)
                except Exception:
                    pass
                time.sleep(min(10, max(1, retry_after)))
                continue
            print(f"[WARN] APIエラー {e.code}: {url[:80]}")
            return None
        except (URLError, TimeoutError, json.JSONDecodeError) as e:
            print(f"[WARN] 取得失敗: {e}")
            return None
    return None


# ==============================
# 取得・正規化
# ==============================
def _strip_html(text):
    import re
    return re.sub(r"<[^>]+>", "", text or "").strip()


def note_url(item):
    user = (item.get("user") or {}).get("urlname", "")
    key = item.get("key", "")
    if user and key:
        return f"https://note.com/{quote(user)}/n/{key}"
    return f"https://note.com/n/{key}" if key else ""


def normalize(item, sort):
    """検索APIの1件を内部形式へ。"""
    price_num = int(item.get("price") or 0)
    user = item.get("user") or {}
    sold = bool(item.get("is_purchased_within_last_24_hours") or item.get("is_recently_purchased"))
    return {
        "key": item.get("key", ""),
        "title": item.get("name") or "",
        "priceNum": price_num,
        "price": f"¥{price_num:,}" if price_num > 0 else "無料/言い値",
        "likes": int(item.get("like_count") or 0),
        "comments": int(item.get("comment_count") or 0),
        "user": user.get("nickname") or user.get("name") or "",
        "authorId": user.get("urlname") or "",
        "publishedAt": item.get("publish_at") or item.get("created_at") or "",
        "description": _strip_html(item.get("description") or "")[:120],
        "url": note_url(item),
        "sold_24h": sold,
        "sorts": {sort},
    }


def fetch_search_page(keyword, sort, start):
    qs = urlencode({
        "context": "note_for_sale",   # 有料記事
        "q": keyword,
        "sort": sort,
        "size": PAGE_SIZE,
        "start": start,
    })
    return fetch_json(f"{NOTE_API_BASE}/searches?{qs}")


def fetch_notes(keyword, pages):
    """複数ソートを統合して有料記事を取得し、URLでユニーク化して返す。"""
    by_url = {}
    for sort in SORTS:
        print(f"[INFO] 取得中（{SORT_LABEL.get(sort, sort)}）: {keyword}")
        for page in range(pages):
            json_data = fetch_search_page(keyword, sort, page * PAGE_SIZE)
            if not json_data:
                break
            bucket = (json_data.get("data") or {}).get("notes_for_sale") or {}
            contents = bucket.get("contents") or []
            for raw in contents:
                item = normalize(raw, sort)
                if not item["key"]:
                    continue
                u = item["url"]
                if u in by_url:
                    by_url[u]["sorts"].update(item["sorts"])
                    # 売れシグナル・スキは最大値を採用
                    by_url[u]["sold_24h"] = by_url[u]["sold_24h"] or item["sold_24h"]
                    by_url[u]["likes"] = max(by_url[u]["likes"], item["likes"])
                else:
                    by_url[u] = item
            if not contents or bucket.get("is_last_page") is True:
                break
    return list(by_url.values())


# ==============================
# 詳細取得（売れシグナル判定）— 検索APIには出ないため記事ごとに取得
# ==============================
def _fetch_detail(item):
    """api/v3/notes/{key} で is_purchased_within_last_24_hours を取得し item を更新。"""
    data = fetch_json(f"{NOTE_API_BASE}/notes/{quote(item['key'])}")
    d = (data or {}).get("data") or {}
    if d:
        item["sold_24h"] = bool(
            d.get("is_purchased_within_last_24_hours") or d.get("is_recently_purchased")
        )
        item["likes"] = int(d.get("like_count") or item["likes"])
        if d.get("price"):
            item["priceNum"] = int(d["price"])
            item["price"] = f"¥{item['priceNum']:,}"
    return item


def hydrate(items, cap):
    """スキ上位 cap 件の詳細を取得して売れシグナルを判定する（同時 HYDRATE_CONCURRENCY）。"""
    targets = sorted(items, key=lambda x: x["likes"], reverse=True)[:cap]
    print(f"[INFO] 詳細取得で売れシグナル判定中… {len(targets)}件（同時{HYDRATE_CONCURRENCY}・80ms間隔）")
    with ThreadPoolExecutor(max_workers=HYDRATE_CONCURRENCY) as ex:
        list(ex.map(_fetch_detail, targets))
    return items


# ==============================
# 反応分析（自分の記事のスキ数を取得）
# ==============================
def fetch_creator_notes(urlname, max_notes=80):
    """note の creators API で著者の記事一覧（スキ数つき）を取得。"""
    out = []
    for page in range(1, 21):
        url = f"https://note.com/api/v2/creators/{quote(urlname)}/contents?kind=note&page={page}"
        data = fetch_json(url)
        if not data:
            break
        d = data.get("data") or {}
        contents = d.get("contents") or []
        for c in contents:
            price = int(c.get("price") or 0)
            out.append({
                "title": c.get("name") or "",
                "likes": int(c.get("likeCount") or c.get("like_count") or 0),
                "comments": int(c.get("commentCount") or c.get("comment_count") or 0),
                "price": price,
                "priceLabel": f"¥{price:,}" if price > 0 else "無料",
                "publishedAt": c.get("publishAt") or c.get("publish_at") or "",
                "url": c.get("noteUrl") or note_url(c),
            })
        if d.get("isLastPage") or not contents or len(out) >= max_notes:
            break
    return out[:max_notes]


def reactions(urlname):
    """著者の記事を集計して反応分析データを返す。"""
    notes = fetch_creator_notes(urlname)
    likes = [n["likes"] for n in notes]
    total = sum(likes)
    cnt = len(notes)
    avg = round(total / cnt) if cnt else 0
    top = sorted(notes, key=lambda x: x["likes"], reverse=True)[:8]
    return {"urlname": urlname, "count": cnt, "total_likes": total, "avg": avg, "top": top}


# ==============================
# ブレンド選定（A:売れ / B:スキ / C:急上昇・新着）
# ==============================
def build_blend(items, target, ratio=(0.4, 0.4, 0.2)):
    A = sorted([a for a in items if a["sold_24h"]],
               key=lambda x: (x["likes"], x["priceNum"]), reverse=True)
    B = sorted(items, key=lambda x: x["likes"], reverse=True)
    C = sorted([a for a in items if ("new" in a["sorts"] or "hot" in a["sorts"])],
               key=lambda x: x["publishedAt"], reverse=True)

    nA = int(target * ratio[0])
    nB = int(target * ratio[1])
    nC = target - nA - nB

    selected, seen = [], set()

    def take(lst, n, group):
        c = 0
        for a in lst:
            if c >= n:
                break
            if a["url"] in seen:
                continue
            seen.add(a["url"])
            picked = dict(a)
            picked["group"] = group
            picked.pop("sorts", None)
            selected.append(picked)
            c += 1

    take(A, nA, "A")   # 今売れている
    take(B, nB, "B")   # スキが多い（普遍的人気）
    take(C, nC, "C")   # 急上昇・新着
    # 不足分は B（スキ順）で補う
    if len(selected) < target:
        take(B, target - len(selected), "B")
    return selected


# ==============================
# 保存・出力
# ==============================
def save_scrape_result(keyword, articles, min_price):
    THEME_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = THEME_DIR / f"scrape_result_{keyword}_{timestamp}.txt"

    g = {"A": "今売れている(24h)", "B": "スキが多い", "C": "急上昇・新着"}
    lines = [
        "note 売れ筋調査結果（非公式API）",
        f"キーワード: {keyword}",
        f"取得日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
        f"対象: 有料記事 ¥{min_price:,}以上 / popular+hot+new+like 統合",
        f"件数: {len(articles)}件（A:売れ {sum(1 for a in articles if a['group']=='A')} / "
        f"B:スキ {sum(1 for a in articles if a['group']=='B')} / "
        f"C:新着 {sum(1 for a in articles if a['group']=='C')}）",
        "=" * 60, "",
    ]
    for i, a in enumerate(articles, 1):
        mark = "🔥売れ" if a["sold_24h"] else ""
        lines.append(f"[{i}] ({g.get(a['group'], a['group'])}) {a['title']}")
        lines.append(f"    {a['price']}  スキ{a['likes']}  {mark}  著者: {a['user']}")
        lines.append(f"    URL: {a['url']}")
        lines.append("")
    filename.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[INFO] 結果保存: {filename}")
    return filename


# ==============================
# メイン
# ==============================
def main():
    parser = argparse.ArgumentParser(description="note 売れ筋有料記事リサーチ（非公式API）")
    parser.add_argument("--keyword", help="検索キーワード（売れ筋リサーチ）")
    parser.add_argument("--author", help="著者urlname（反応分析：自分の記事のスキ数を集計）")
    parser.add_argument("--pages", type=int, default=8, help="ソートごとの探索ページ数（既定: 8）")
    parser.add_argument("--min-price", type=int, default=1980, help="最低価格（既定: 1980）")
    parser.add_argument("--limit", type=int, default=40, help="出力件数（ブレンド後・既定: 40）")
    parser.add_argument("--hydrate-cap", type=int, default=HYDRATE_CAP,
                        help=f"売れシグナル判定で詳細取得する上限（既定: {HYDRATE_CAP}）")
    parser.add_argument("--no-hydrate", action="store_true",
                        help="詳細取得（売れシグナル判定）をスキップして高速化")
    args = parser.parse_args()

    # 反応分析モード（自分の記事のスキ数集計）
    if args.author:
        data = reactions(args.author.strip().strip("@/"))
        print(f"[INFO] 反応分析 @{data['urlname']}: 記事{data['count']}件 / 総スキ{data['total_likes']} / 平均{data['avg']}")
        print("\n[DATA_START]")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        print("[DATA_END]")
        return
    if not args.keyword:
        print("[ERROR] --keyword か --author を指定してください")
        return

    print(f"\n{'='*50}")
    print(f"  note 売れ筋リサーチ（非公式API・Chrome不要）")
    print(f"  キーワード: {args.keyword}  最低価格: ¥{args.min_price:,}")
    print(f"{'='*50}")

    try:
        items = fetch_notes(args.keyword, args.pages)
        before = len(items)
        items = [a for a in items if a["priceNum"] >= args.min_price]
        print(f"\n[INFO] 取得 {before}件 → 有料¥{args.min_price:,}以上 {len(items)}件")

        if not items:
            print("\n[WARN] 条件に合う記事が見つかりませんでした")
            return

        if not args.no_hydrate:
            hydrate(items, args.hydrate_cap)

        sold_total = sum(1 for a in items if a["sold_24h"])
        articles = build_blend(items, args.limit)

        # 統計
        likes = [a["likes"] for a in articles]
        print(f"\n[INFO] 調査結果（ブレンド {len(articles)}件 / 売れシグナル母数 {sold_total}件）:")
        if likes:
            print(f"  スキ: 最大{max(likes)} / 中央値{sorted(likes)[len(likes)//2]}")
        print(f"  A:今売れ {sum(1 for a in articles if a['group']=='A')} / "
              f"B:スキ {sum(1 for a in articles if a['group']=='B')} / "
              f"C:新着 {sum(1 for a in articles if a['group']=='C')}")

        save_scrape_result(args.keyword, articles, args.min_price)

        json_output = [{
            "title": a["title"],
            "price": a["price"],
            "priceNum": a["priceNum"],
            "likes": a["likes"],
            "sold_24h": a["sold_24h"],
            "group": a["group"],
            "user": a["user"],
            "url": a["url"],
            "publishedAt": a["publishedAt"],
        } for a in articles]
        print("\n[DATA_START]")
        print(json.dumps(json_output, ensure_ascii=False, indent=2))
        print("[DATA_END]")

    except Exception as e:
        import traceback
        print(f"\n[ERROR] リサーチ失敗: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
