#!/usr/bin/env python3
"""ナレッジBOX の道具箱。Python標準ライブラリだけで動く。

使い方:
  python3 box.py init                     箱を作る
  python3 box.py file --owner 自分        受け箱の資料を保管庫へしまう
  python3 box.py todo                     カードにしていない資料を出す
  python3 box.py add --file cards.jsonl   カードを追加する（1行1枚のJSON）
  python3 box.py done <保管先>            資料をカード化済みにする
  python3 box.py pick --recipe X投稿      仕事に要るカードだけを取り出す
  python3 box.py check                    箱を点検する（問題があれば終了コード1）
  python3 box.py stats                    棚ごとの枚数を出す
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

SHELVES = {
    "お客様": ["悩み", "願い", "言い回し", "反論", "質問"],
    "わたし": ["経験", "実績", "考え方", "口調"],
    "商品": ["内容", "価格", "条件", "事例"],
    "勝ちパターン": ["流れ"],
}
SURE = ["原文", "まとめ", "予想"]
OWNERS = ["自分", "許可あり", "公開情報"]
LEDGER_FIELDS = ["保管日", "ファイル名", "保管先", "指紋", "持ち主", "カード化"]
TEXT_EXTS = {".txt", ".md", ".csv", ".tsv", ".json", ".jsonl", ".html", ".htm", ".vtt", ".srt"}
MAX_BODY = 1200

BLOCKED_NAME = re.compile(r"(^\.env|credential|secret|token|id_rsa|\.pem$|\.key$)", re.I)
SECRET = re.compile(
    r"sk-[A-Za-z0-9_-]{16,}|xox[abprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{30,}"
    r"|gh[pousr]_[A-Za-z0-9]{30,}|BEGIN [A-Z ]*PRIVATE KEY"
)
MAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z.]{2,}")
PHONE = re.compile(r"(?<!\d)(0\d{1,4}-\d{1,4}-\d{3,4}|0[5789]0\d{8})(?!\d)")

RECIPES = {
    "X投稿": ("4000", ["お客様/悩み: 5", "お客様/言い回し: 6", "わたし/口調: 4", "わたし/経験: 3", "勝ちパターン/流れ: 1"], "商品/価格"),
    "YouTube台本": ("7000", ["お客様/悩み: 6", "お客様/質問: 5", "わたし/経験: 5", "わたし/口調: 5", "勝ちパターン/流れ: 2"], "商品/条件"),
    "LP": ("9000", ["お客様/悩み: 6", "お客様/願い: 5", "お客様/反論: 5", "商品/内容: 6", "商品/価格: 3", "商品/条件: 4", "商品/事例: 4", "わたし/実績: 3"], "わたし/口調"),
    "メール配信": ("5000", ["お客様/悩み: 4", "お客様/言い回し: 5", "わたし/口調: 5", "わたし/経験: 3", "商品/内容: 2"], "勝ちパターン/流れ"),
}

START_GUIDE = """# ナレッジBOX の使い方

資料を「受け箱」に入れて、AIにこう話しかけてください。

- 「入れて」: 受け箱の資料を保管庫へしまいます
- 「カードにして」: 資料から1話ずつカードを作ります
- 「X投稿のカードを出して」: その仕事に要るカードだけを取り出します
- 「箱を点検して」: 抜けや消し忘れを見つけます

保管庫の中の資料は書き換えないでください。
"""


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_box(option: str) -> Path:
    candidates = [Path(option).expanduser(), Path.cwd()]
    for candidate in candidates:
        if (candidate / "台帳.csv").exists():
            return candidate.resolve()
    raise SystemExit("箱が見つかりません。先に init を実行するか、--box で場所を指定してください。")


def read_ledger(box: Path) -> list[dict]:
    with (box / "台帳.csv").open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_ledger(box: Path, rows: list[dict]) -> None:
    with (box / "台帳.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_card(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    head, _, body = text.partition("\n----\n")
    card = {"_path": path, "本文": body.strip()}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            card[key.strip()] = value.strip()
    return card


def load_cards(box: Path) -> list[dict]:
    return [parse_card(path) for path in sorted((box / "カード").rglob("C*.md"))]


def sources_of(card: dict) -> list[str]:
    return [item.strip() for item in card.get("出どころ", "").split("|") if item.strip()]


def problems_of(card: dict, ledger_by_place: dict[str, dict]) -> list[str]:
    """カード1枚の問題点を返す。add と check が同じ基準を使う。"""
    problems: list[str] = []
    shelf, kind, sure = card.get("棚", ""), card.get("種類", ""), card.get("確かさ", "")
    body = card.get("本文", "")
    if shelf not in SHELVES:
        return [f"棚「{shelf}」はありません（{'・'.join(SHELVES)}）"]
    if kind not in SHELVES[shelf]:
        problems.append(f"棚「{shelf}」に種類「{kind}」はありません（{'・'.join(SHELVES[shelf])}）")
    if sure not in SURE:
        problems.append(f"確かさは {'・'.join(SURE)} のどれかにしてください")
    if not body:
        problems.append("本文が空です")
    if len(body) > MAX_BODY:
        problems.append(f"本文が{MAX_BODY}字を超えています。1枚1話に分けてください")
    if SECRET.search(body):
        problems.append("本文に鍵らしき文字列があります")
    if MAIL.search(body) or PHONE.search(body):
        problems.append("本文にメールアドレスか電話番号があります。伏せてください")

    sources = sources_of(card)
    if sure != "予想" and not sources:
        problems.append("出どころがありません")
    owners = []
    for source in sources:
        if source.startswith("本人談"):
            if shelf not in ("わたし", "商品"):
                problems.append("本人談を出どころにできるのは「わたし」「商品」の棚だけです")
            owners.append("自分")
            continue
        place = nfc(source.split("#", 1)[0].strip())
        row = ledger_by_place.get(place)
        if row is None:
            problems.append(f"出どころ「{place}」が台帳にありません")
        else:
            owners.append(row["持ち主"])
    if "公開情報" in owners:
        if shelf != "勝ちパターン":
            problems.append("他の人の公開情報から作れるのは「勝ちパターン」の棚だけです")
        elif len(sources) < 2:
            problems.append("他の人の公開情報から流れを作るときは、資料を2つ以上示してください")
    return problems


def ledger_index(rows: list[dict]) -> dict[str, dict]:
    return {nfc(row["保管先"]): row for row in rows}


def cmd_init(args) -> int:
    box = Path(args.box).expanduser().resolve()
    folders = ["受け箱", "保管庫", "レシピ"] + [f"カード/{shelf}" for shelf in SHELVES]
    for folder in folders:
        (box / folder).mkdir(parents=True, exist_ok=True)
    if not (box / "台帳.csv").exists():
        write_ledger(box, [])
    for name, (limit, lines, avoid) in RECIPES.items():
        recipe = box / "レシピ" / f"{name}.md"
        if not recipe.exists():
            recipe.write_text("\n".join([f"上限: {limit}", *lines, f"読まない: {avoid}"]) + "\n", encoding="utf-8")
    guide = box / "はじめに.md"
    if not guide.exists():
        guide.write_text(START_GUIDE, encoding="utf-8")
    ignore = box / ".gitignore"
    if not ignore.exists():
        ignore.write_text("受け箱/\n保管庫/\nカード/\n台帳.csv\n", encoding="utf-8")
    print(f"箱を用意しました: {box}")
    return 0


def inbox_files(box: Path) -> list[Path]:
    inbox = box / "受け箱"
    return sorted(p for p in inbox.rglob("*") if p.is_file() and not p.name.startswith(".DS_Store"))


def cmd_file(args) -> int:
    box = find_box(args.box)
    rows = read_ledger(box)
    known = {row["指紋"] for row in rows}
    month = datetime.now().strftime("%Y-%m")
    moved = skipped = 0
    for path in inbox_files(box):
        relative = path.relative_to(box / "受け箱")
        if BLOCKED_NAME.search(path.name):
            print(f"入れません（鍵や秘密のファイルのようです）: {relative}")
            skipped += 1
            continue
        mark = fingerprint(path)
        if mark in known:
            print(f"同じ中身がすでにあります: {relative}")
            skipped += 1
            continue
        name = nfc("_".join(relative.parts))
        target_dir = box / "保管庫" / month
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / name
        number = 2
        while target.exists():
            target = target_dir / f"{Path(name).stem}_{number}{Path(name).suffix}"
            number += 1
        shutil.move(str(path), str(target))
        rows.append({
            "保管日": datetime.now().strftime("%Y-%m-%d"),
            "ファイル名": name,
            "保管先": target.relative_to(box).as_posix(),
            "指紋": mark,
            "持ち主": args.owner,
            "カード化": "未",
        })
        known.add(mark)
        moved += 1
        print(f"しまいました: {target.relative_to(box).as_posix()}")
    write_ledger(box, rows)
    print(f"しまった資料 {moved}件 / 入れなかった資料 {skipped}件")
    return 0


def readable_path(box: Path, place: str) -> Path | None:
    path = box / place
    if path.suffix.lower() in TEXT_EXTS and path.exists():
        return path
    sidecar = path.with_name(path.name + ".txt")
    return sidecar if sidecar.exists() else None


def cmd_todo(args) -> int:
    box = find_box(args.box)
    pending = [row for row in read_ledger(box) if row["カード化"] == "未"]
    if not pending:
        print("カードにしていない資料はありません。")
        return 0
    for row in pending:
        readable = readable_path(box, row["保管先"])
        note = f"読む場所: {readable.relative_to(box).as_posix()}" if readable else f"先に文字にする: {row['保管先']}.txt を作る"
        print(f"{row['保管先']}（{row['持ち主']}）  {note}")
    return 0


def cmd_done(args) -> int:
    box = find_box(args.box)
    rows = read_ledger(box)
    wanted = {nfc(item) for item in args.places}
    found = set()
    for row in rows:
        if nfc(row["保管先"]) in wanted:
            row["カード化"] = "済"
            found.add(nfc(row["保管先"]))
    write_ledger(box, rows)
    for missing in sorted(wanted - found):
        print(f"台帳にありません: {missing}")
    print(f"カード化済みにした資料 {len(found)}件")
    return 0 if found == wanted else 1


def normalized_body(text: str) -> str:
    return re.sub(r"\s+", "", nfc(text))


def cmd_add(args) -> int:
    box = find_box(args.box)
    raw = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    index = ledger_index(read_ledger(box))
    cards = load_cards(box)
    seen = {normalized_body(card["本文"]) for card in cards}
    numbers = [int(card["番号"][1:]) for card in cards if re.fullmatch(r"C\d+", card.get("番号", ""))]
    next_number = max(numbers, default=0) + 1
    added = rejected = 0
    for line_number, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            print(f"{line_number}行目: JSONとして読めません")
            rejected += 1
            continue
        tags = item.get("タグ", [])
        tags = [str(tag).strip() for tag in tags] if isinstance(tags, list) else [t.strip() for t in str(tags).split(",")]
        source = item.get("出どころ", "")
        source = " | ".join(source) if isinstance(source, list) else str(source)
        card = {
            "棚": nfc(str(item.get("棚", ""))),
            "種類": nfc(str(item.get("種類", ""))),
            "確かさ": nfc(str(item.get("確かさ", ""))),
            "出どころ": nfc(source),
            "本文": str(item.get("本文", "")).strip(),
        }
        problems = problems_of(card, index)
        if normalized_body(card["本文"]) in seen:
            problems.append("同じ本文のカードがすでにあります")
        if problems:
            print(f"{line_number}行目: " + " / ".join(problems))
            rejected += 1
            continue
        number = f"C{next_number:04d}"
        next_number += 1
        seen.add(normalized_body(card["本文"]))
        folder = box / "カード" / card["棚"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{number}_{card['種類']}.md").write_text(
            f"番号: {number}\n棚: {card['棚']}\n種類: {card['種類']}\n"
            f"タグ: {', '.join(t for t in tags if t)}\n確かさ: {card['確かさ']}\n"
            f"出どころ: {card['出どころ']}\n----\n{card['本文']}\n",
            encoding="utf-8",
        )
        added += 1
    print(f"追加 {added}枚 / 追加できなかった行 {rejected}件")
    return 1 if rejected else 0


def load_recipe(box: Path, name: str) -> tuple[int, list[tuple[str, int]], set[str]]:
    path = box / "レシピ" / f"{nfc(name)}.md"
    if not path.exists():
        available = "・".join(sorted(p.stem for p in (box / "レシピ").glob("*.md")))
        raise SystemExit(f"レシピ「{name}」がありません（あるもの: {available}）")
    limit, wanted, avoid = 6000, [], set()
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.partition(":")
        key, value = nfc(key.strip()), nfc(value.strip())
        if not sep:
            continue
        if key == "上限":
            limit = int(value)
        elif key == "読まない":
            avoid = {item.strip() for item in value.split(",") if item.strip()}
        elif "/" in key:
            wanted.append((key, int(value)))
    return limit, wanted, avoid


def cmd_pick(args) -> int:
    box = find_box(args.box)
    limit, wanted, avoid = load_recipe(box, args.recipe)
    limit = args.limit or limit
    tags = {nfc(tag.strip()) for tag in (args.tag or "").split(",") if tag.strip()}
    cards = load_cards(box)
    pools: dict[str, list[dict]] = {}
    for slot, _count in wanted:
        if slot in avoid:
            continue
        shelf, kind = slot.split("/", 1)
        pool = [c for c in cards if c.get("棚") == shelf and c.get("種類") == kind]
        if not args.with_guess:
            pool = [c for c in pool if c.get("確かさ") != "予想"]

        def rank(card: dict):
            card_tags = {nfc(t.strip()) for t in card.get("タグ", "").split(",")}
            return (-len(tags & card_tags), SURE.index(card["確かさ"]) if card.get("確かさ") in SURE else 9, card.get("番号", ""))

        pools[slot] = sorted(pool, key=rank)

    # 上限の字数を棚で取り合わないよう、種類ごとに1枚ずつ順番に取る
    chosen: dict[str, list[dict]] = {slot: [] for slot in pools}
    quota = dict(wanted)
    total, cut = 0, 0
    progress = True
    while progress:
        progress = False
        for slot, pool in pools.items():
            position = len(chosen[slot])
            if position >= quota[slot] or position >= len(pool):
                continue
            size = len(pool[position]["本文"])
            if total + size > limit:
                cut += 1
                continue
            chosen[slot].append(pool[position])
            total += size
            progress = True

    print(f"# {nfc(args.recipe)} に使うカード（本文 {total}字 / 上限 {limit}字）\n")
    print("カードに無いことは、想像で補わないでください。\n")
    for slot, picked in chosen.items():
        print(f"## {slot}")
        if not picked:
            print("カードなし。ここは書かないか、社長に聞いてください。\n")
            continue
        for card in picked:
            print(f"- [{card['番号']} / {card['確かさ']}] {card['本文']}")
        print()
    if avoid:
        print(f"読まないもの: {', '.join(sorted(avoid))}")
    if cut:
        print(f"上限の字数に収まらず、{cut}回カードの追加を止めました。必要なら --limit で増やしてください。")
    return 0


def cmd_check(args) -> int:
    box = find_box(args.box)
    rows = read_ledger(box)
    index = ledger_index(rows)
    errors: list[str] = []
    notes: list[str] = []
    bodies: dict[str, str] = {}
    cards = load_cards(box)
    for card in cards:
        name = card["_path"].relative_to(box).as_posix()
        for problem in problems_of(card, index):
            errors.append(f"{name}: {problem}")
        key = normalized_body(card.get("本文", ""))
        if key and key in bodies:
            errors.append(f"{name}: {bodies[key]} と本文が同じです")
        elif key:
            bodies[key] = name
    for row in rows:
        path = box / row["保管先"]
        if not path.exists():
            errors.append(f"{row['保管先']}: 台帳にあるのに、ファイルがありません")
        elif fingerprint(path) != row["指紋"]:
            errors.append(f"{row['保管先']}: しまった後に中身が変わっています")
        elif readable_path(box, row["保管先"]) is None:
            notes.append(f"{row['保管先']}: 文字にしたファイルがまだありません")
    waiting = len(inbox_files(box))
    if waiting:
        notes.append(f"受け箱にまだ {waiting}件あります")
    pending = sum(1 for row in rows if row["カード化"] == "未")
    if pending:
        notes.append(f"カードにしていない資料が {pending}件あります")
    guesses = sum(1 for card in cards if card.get("確かさ") == "予想")
    if guesses:
        notes.append(f"確かさが「予想」のカードが {guesses}枚あります（取り出しには使われません）")
    for message in errors:
        print("直す: " + message)
    for message in notes:
        print("確認: " + message)
    print(f"カード {len(cards)}枚 / 直すところ {len(errors)}件 / 確認 {len(notes)}件")
    return 1 if errors else 0


def cmd_stats(args) -> int:
    box = find_box(args.box)
    cards = load_cards(box)
    print("棚 / 種類 / 枚数 / うち原文")
    for shelf, kinds in SHELVES.items():
        for kind in kinds:
            matched = [c for c in cards if c.get("棚") == shelf and c.get("種類") == kind]
            original = sum(1 for c in matched if c.get("確かさ") == "原文")
            print(f"{shelf} / {kind} / {len(matched)} / {original}")
    rows = read_ledger(box)
    print(f"資料 {len(rows)}件（カード化済み {sum(1 for r in rows if r['カード化'] == '済')}件）")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="ナレッジBOX の道具箱")
    parser.add_argument("--box", default="ナレッジBOX", help="箱の場所（既定: 今いるフォルダの ナレッジBOX）")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init").set_defaults(run=cmd_init)
    filing = commands.add_parser("file")
    filing.add_argument("--owner", choices=OWNERS, required=True)
    filing.set_defaults(run=cmd_file)
    commands.add_parser("todo").set_defaults(run=cmd_todo)
    done = commands.add_parser("done")
    done.add_argument("places", nargs="+")
    done.set_defaults(run=cmd_done)
    adding = commands.add_parser("add")
    adding.add_argument("--file")
    adding.set_defaults(run=cmd_add)
    picking = commands.add_parser("pick")
    picking.add_argument("--recipe", required=True)
    picking.add_argument("--tag")
    picking.add_argument("--limit", type=int)
    picking.add_argument("--with-guess", action="store_true")
    picking.set_defaults(run=cmd_pick)
    commands.add_parser("check").set_defaults(run=cmd_check)
    commands.add_parser("stats").set_defaults(run=cmd_stats)
    args = parser.parse_args()
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())
