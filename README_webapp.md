# note-article-system — Web UI（アプリ版）

`note-article-system-cli_ver2` を **ブラウザで操作できるアプリ**にしたものです。
（AUTO-content-system_ver05 の webapp と同じ仕組み：ローカルFlaskサーバ＋claude CLI）

## 起動方法

1. **`start_webapp.bat` をダブルクリック**
2. 自動でブラウザが開きます → `http://127.0.0.1:8788`
   - 開かない場合は手動でこのURLを開いてください
3. 終了するときは、起動した黒いウィンドウ（コマンドプロンプト）を閉じます

> 初回は Flask が自動インストールされます。

## 前提

- Python 3.x がインストール済み
- `claude` CLI がインストール済み（`npm install -g @anthropic-ai/claude-code`）
- selenium / Pillow / psutil（投稿に使用）

## 画面の使い方

- **中央のチャット**：「○○のテーマで記事を書いて投稿して」など自由に指示。claude が CLAUDE.md に従って動きます
- **左パネル（クイック操作）**：メニュー[1]〜[7] 相当のボタン、環境チェック、**note.comログイン**、フォルダを開く
- **右パネル**：環境ステータス／テーマ残数（themes.json）／記事一覧（未投稿・投稿済）
  - テーマをクリック → そのテーマで生成＋投稿を指示
  - 記事をクリック → その場で本文を編集・保存
- **ヘッダー**：モデル選択（Opus/Sonnet/Haiku/Fable）・動作モード切替

## note.com ログイン

左パネルの「🔑 note.com にログイン」を押すと、**専用のChromeウィンドウ**が開きます。
その窓で note.com にログインすると自動で閉じ、以降は自動投稿できます。
（普段使いのChromeではログインしないでください。保存先プロファイルが別です）

## 動作モードについて

- **フルオート（既定）**：確認なしで記事生成〜下書き投稿まで一気に実行。`start_webapp.bat` が `NAS_ALLOW_FULL=1` を設定して有効化します
- **制限（安全）**：ファイル操作・リサーチ・python実行など必要なツールのみ許可
- **自動 / 計画のみ**：CLI のパーミッションモードに委譲

## ポート

`8788`（AUTO-content-system の 8787 と被らないようにしています）。
変更したい場合は `webapp/server.py` の `PORT` を編集してください。

## ファイル構成（追加分）

```
note-article-system_ver4/
├── start_webapp.bat          ← ダブルクリックで起動
├── webapp/
│   ├── server.py             ← Flaskサーバ（claude CLI をストリーミング起動）
│   └── static/index.html     ← 画面
└── （以下は cli_ver2 から一式コピー）
    CLAUDE.md / note_poster.py / note_scraper.py / themes.json / articles/ …
```
