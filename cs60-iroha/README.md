# CS60岐阜メディカルサロンいろは 柳ヶ瀬店 — ダイエットLP

レシピ: **湯気が晴れる**（骨格 letter × 世界観 hinoki / No.047 × 演出 ripple）

## 公開する

**方法A. ドラッグ&ドロップ（推奨・1分）**

1. https://dash.cloudflare.com/ にログイン（無料・カード不要）
2. Workers & Pages → Create → Pages → **Upload assets**
3. この `cs60-iroha` フォルダをそのままドロップ
4. 出てきた `https://<名前>.pages.dev/` で公開完了

**方法B. コマンド（お手元のPCで）**

```
bash scripts/publish.sh cs60-iroha cs60-iroha
```

初回はブラウザでCloudflareのログイン画面が開くので Allow を押してください。

## 文言を直す

`cs60-iroha-src/台本.md` を編集して保存するだけで反映できます（61項目）。

```
python scripts/apply-copy.py cs60-iroha        # 1回だけ反映
python scripts/watch-copy.py cs60-iroha        # 保存のたびに自動反映
```

`index.html` を直接編集しても構いません。

## 画像を入れる

いまは画像なしで完成しています（色と文字だけで成立する設計）。

1. `cs60-iroha-src/prompts.md` を開く
2. **ビフォーアフター・院長の写真・院外の写真は実写のみ**（生成禁止。捏造になります）
3. 背景画像だけAIで作りたい場合はプロンプトを貼って生成
4. `cs60-iroha-src/images/` に保存して「画像を入れた」と言えば差し替えます

## 中身

```
cs60-iroha/
├── index.html
├── assets/css/style.css
├── assets/js/main.js
└── assets/img/  favicon.svg, ogp.jpg
```

## 注意

- フッターの「効果には個人差があります」は**消さないでください**。ダイエット表示は
  景品表示法・薬機法の対象です
- 掲載している数字は既存LPの表記のままです。変更する場合は根拠のある数字に
- 料金は載せていません（既存LPが非表示のため）。載せる場合はご相談ください
