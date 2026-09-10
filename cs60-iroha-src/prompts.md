# 画像プロンプト（cs60-iroha）

作り方: 下のプロンプトを画像生成サービスに貼って生成し、指定のファイル名で
`cs60-iroha-src/images/` に保存 → Claude Code で「画像を入れた」と言ってください。

対応サービス: ChatGPT（無料枠でも可）/ Midjourney / Adobe Firefly / Canva の AI 画像 /
Google ImageFX / Leonardo。どれでも同じプロンプトで大丈夫です。
比率が選べないサービスでは正方形で生成して構いません（こちらで切り抜きます）。

---

## ⚠ 生成してはいけない画像（重要）

次の3スロットは **必ずご本人・お客様の実写のみ** を使ってください。
AIで作ってはいけません。作った場合、実績の捏造になり、景品表示法違反になります。

| スロット | 中身 |
| --- | --- |
| `before_after_1` `before_after_2` `before_after_3` | お客様のビフォーアフター写真（同意取得済みのもの）　→ **未投入** |
| `owner_portrait` | 院長のお顔写真　→ **投入済み**（IMG_6245） |
| `counseling` | カウンセリング風景　→ **投入済み**（IMG_5214） |
| `owner_standing` | サロンに立つ院長　→ **投入済み**（IMG_4648） |
| `shop_exterior` | 院外の写真　→ 未投入 |

### 投入済み写真について
- 3枚とも **EXIF を完全に除去** しました。うち2枚に GPS 座標が入っていたため、
  そのまま公開していたら撮影場所が誰でも特定できる状態でした
- 向きが横倒しだったものは正しい向きに補正しています
- `counseling`（IMG_5214）には **お客様が写っています**。掲載の同意が
  取れていない場合は、`index.html` の `<figure class="shot">` を1ブロック
  削除すれば外せます

既存LPに掲載されている写真をそのまま使えます。ファイル名を上の名前に合わせて
`cs60-iroha-src/images/` に入れてください（例: `before_after_1.jpg`）。

---

## 1. kv.jpg — ヒーロー背景（任意・最重要）

- 比率: 3:2（横長）。1536×1024 か 1920×1280
- 場所: 最初の画面の背景。上に大きな見出しが乗るので、中央〜左は明るく静かに
- プロンプト（英語・そのまま貼る）:

```
hinoki wood bath with rising steam and soft window light, Japanese onsen, calm,
warm cream and pale beige tones, soft morning haze, minimal, serene, empty space
in the left half, no people, no text, no letters, no watermark, no logo
```

- 日本語の意味: 檜の浴槽から湯気が立ち、窓から柔らかい光。生成り〜淡いベージュ。左半分は余白
- NG: 文字入り、人物、ビビッドな色、ネオン
- **これ1枚を入れるだけで見栄えが大きく変わります。** 他は無くても成立します

## 2. steam.jpg — セクション区切りの湯気（任意）

- 比率: 3:2
- 場所: 「なぜ、いろはで変わるのか」の上に敷く帯

```
abstract soft white steam drifting over warm cream background, Japanese onsen atmosphere,
very soft gradient, minimal, calm, no objects, no people,
no text, no letters, no watermark, no logo
```

## 3. hinoki-grain.jpg — 木目のテクスチャ（任意）

- 比率: 16:9

```
close-up of pale hinoki cypress wood grain, natural warm beige, soft even light,
flat lay, subtle texture, no objects, no people,
no text, no letters, no watermark, no logo
```

---

### サービス別の注意

- **Midjourney**: 末尾に `--ar 3:2 --no text` を付ける
- **Canva**: プロンプトの後ろに日本語で「テキストなし」と足す
- **ChatGPT**: そのまま貼ってOK。「比率3:2で」と添えると確実
