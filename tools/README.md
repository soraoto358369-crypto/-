# tools/ — 記事間の相互リンクを差し替える

記事の本文には「睡眠の記事で書いたとおり」のような**文字での参照**が116箇所あります。
公開後にURLが決まったら、ここのツールで一括してリンクに差し替えられます。

## 手順

### 1. URLを記入する

`tools/links.json` の `url` に、公開後のURLを書き込みます。

```json
{
  "睡眠": {
    "file": "article_睡眠とミトコンドリア.txt",
    "title": "体質改善ダイエットで一番コスパがいいのは睡眠です",
    "url": "https://note.com/あなたのID/n/xxxxxxxx"
  }
}
```

全部そろっていなくても構いません。記入済みのものだけが差し替わります。

### 2. 記入状況と対象件数を確認する

```
python tools/apply_links.py --check
```

### 3. 変更内容を事前に見る（ファイルは書き換えません）

```
python tools/apply_links.py --dry-run
```

### 4. 実際に差し替える

```
python tools/apply_links.py
```

## 出力の形式

既定は note.com 向けです。note はURLを自動でリンクにするので、本文に括弧で添えます。

```
変更前： 睡眠の記事で書いたとおりです。
変更後： 睡眠の記事（https://note.com/…）で書いたとおりです。
```

Markdown が使える媒体なら `--style md` を指定します。

```
変更後： [睡眠の記事](https://note.com/…)で書いたとおりです。
```

## 安全のための仕様

- **二重にリンクが付きません。** すでにURLが続く参照は飛ばすので、何度実行しても大丈夫です
- **URLが空の参照は触りません。** 記入した分だけが差し替わります
- `--dry-run` で件数と対象ファイルを先に確認できます

## 参照名と記事の対応

`tools/links.json` に26件あります。`腸` と `腸内環境` のように、
本文中の書き方が複数ある参照は、同じ記事を指すよう両方登録しています。

なお「前の記事」「これまでの記事」のように対象が特定できない参照は、
差し替えの対象外です（そのまま文字のまま残ります）。

---

## Instagram カルーセル画像の生成（make_instagram_images.py）

記事の `▼Instagramキャプション` を読み取って、1:1（1080×1080）のカルーセル画像を作ります。
**記事ファイルは読むだけで、書き換えません。**

```bash
python tools/make_instagram_images.py                  # 全35本（= 275枚）
python tools/make_instagram_images.py --only 鉄と貧血    # 1本だけ確認用に
python tools/make_instagram_images.py --format 4x5     # 1080×1350 版も作れる
python tools/make_instagram_images.py --max-slides 10  # 1本あたりの上限枚数
```

出力先は `instagram/<番号>_<記事名>/01.jpg …`。**1フォルダ＝1投稿**なので、
そのフォルダの画像を番号順に選んでアップロードすればカルーセルになります。

### 枚数の内訳（1本あたり 6〜8枚）

| 順番 | 中身 |
|---|---|
| 1枚目 | 表紙（テーマ絵文字＋フックの一文） |
| 2枚目〜 | 本文（キャプションの段落をそのまま分割） |
| 途中 | 「やることはこれだけ」＝ ✅ / ▶︎ のリスト |
| 終わり近く | 「ここだけ注意」＝ ⚠️ / 👉 の一言 |
| 最後 | 保存とプロフィールリンクの案内 |

### 通し番号について

`No.00`〜`No.34` は、序章の「この先に読むもの（全34本）」に並んでいる順です。
記事を足したり順番を変えたときは、スクリプト内の `ORDER` を直してください。

### 配色

35本すべて同じ土台色（濃いチャコール）で、記事ごとにアクセント色だけが変わります。
フィードに並んだときに「同じシリーズ」に見えるようにしてあります。

### 必要なもの

- Pillow（`pip install Pillow`）
- 日本語フォント `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf`（IPAゴシック）
- 絵文字フォント `/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf`（無くても絵文字が消えるだけで動きます）

Windows で動かす場合は、スクリプト冒頭の `FONT_JP` を
`C:\Windows\Fonts\meiryo.ttc` などに、`FONT_EMOJI` を
`C:\Windows\Fonts\seguiemj.ttf` に書き換えてください。
