# 画像なしで先に完成 → プロンプト書き出し → 後から差し替え

Codex も ChatGPT も使わない人のための経路（`images: later`）。**画像が無くても完成品として成立させ**、あとから画像を入れると格上げされる設計にする。

## 1. 画像スロットを「仮の絵」で埋める

画像が入る場所は全部 `<figure class="slot" data-slot="kv">` にし、中に World の色で描いた仮の絵を入れる。仮の絵は「素材が来ていない」感を出さない。それ自体でデザインとして成立させる。

| World | 仮の絵の作り方 |
| --- | --- |
| abyss-gold / horror-west / wafu-dark | 黒地に放射グラデ + 金 or 差し色の細線（SVG）。グレイン |
| pastel-pop* | 単色のブロブ（border-radius モーフ）+ 小さな丸を2〜3個 |
| paper-* / mono-minimal | 罫線の枠 + 対角線1本。または大きな番号 |
| neon-tokyo | 黒地 + ネオン色の細い枠 + 走査線 |
| brutal | 黄色の塗り + 太い黒枠 + 斜線 |
| retro-future | 放射線 + 太陽の円 |
| watercolor | にじみ（feTurbulence）の淡い色面 |
| 上記以外 | その World の `--bg` の色面 + `--accent` の細線1本か大きな番号。質感（`recipes/worlds.md` の「質感」）が CSS で作れるなら足す |

比率は本番の画像と同じ（KV 3:2、カード 1:1 など）。`<img>` は置かず、`data-slot` だけ持たせる。

## 2. prompts.md を書き出す

サイトの隣（`<site>-src/prompts.md`）に、**スロットごと**に次を書く。

```
# 画像プロンプト（<site>）

作り方: 下のプロンプトを画像生成サービスに貼って生成し、指定のファイル名で `<site>-src/images/` に保存 → Claude Code で「画像を入れた」と言う。

対応サービス: ChatGPT（無料枠でも可）/ Midjourney / Adobe Firefly / Canva の AI 画像 / Google ImageFX / Leonardo。どれでも同じプロンプトで大丈夫です。
比率が選べないサービスでは、正方形で生成して構いません（こちらで切り抜きます）。

---

## 1. kv.jpg — ヒーロー背景（最重要）
- 比率: 3:2（横長）。1536×1024 か 1920×1280
- 場所: 最初の画面全体の背景。上に見出しが乗るので、中央〜下は暗め・シンプルに
- プロンプト（英語・そのまま貼る）:
  abstract swirling crimson ink and liquid gold in black water, ... no text, no letters, no watermark
- 日本語の意味: 黒い水の中で赤い墨と金が渦を巻く抽象。文字なし
- NG: 文字入り、白背景、人物の顔

## 2. emblem.jpg — アイコン代わりの象徴（任意）
- 比率: 1:1
- 場所: 名前の上の丸いアイコン枠。本人写真があるならこの画像は不要
...
```

規則:
- World の接頭辞をそのまま使い、被写体は copy から。`no text, no letters, no watermark, no logo` を全部に付ける。
- 「最重要」「任意」を付け、**KV だけ作れば見栄えが変わる**ことを明記する（全部作らなくてよい）。
- 本人写真で代替できるスロットは「写真でも可」と書く。
- サービス別の注意を1行ずつ: Midjourney は `--ar 3:2 --no text`、Canva は「テキストなし」を日本語で追記、ChatGPT はそのまま。

## 3. 差し替え（「画像を入れた」と言われたら）

1. `<site>-src/images/` を読む。ファイル名がスロット名と一致するものを対象にする。似た名前（`kv (1).png` など）は寄せて解釈し、報告に書く。
2. `scripts/convert.py <site>-src/images <site>` で JPG 化・EXIF 除去・OGP 切り出し。
3. `data-slot` に対応する `<img>` を差し込む（`loading` / `alt` / `fetchpriority` を付ける）。仮の絵は残して `<img>` の下に敷く（読み込み中の背景になる）。
4. 無いスロットはそのまま仮の絵で公開できる。
5. QA を再実行して報告。「残り: emblem.jpg（任意）」のように未投入を列挙する。

## 4. Codex が無い人への説明文（納品メッセージに入れる）

「画像はまだ入っていませんが、このまま公開できます。`<site>-src/prompts.md` のプロンプトを ChatGPT（無料でも可）などに貼って画像を作り、`images/` に保存して『画像を入れた』と言ってください。KV の1枚だけでも見た目が大きく変わります。」
