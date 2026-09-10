# 環境セットアップ — 「セットアップ」と打つだけ

ターミナルは使いません。Claude Code / Codex のデスクトップアプリのチャットに **「セットアップ」** と打つと、スキルが下の表を全部入れます（数分。途中で「許可しますか」のダイアログが出たら「はい」）。Codex のログインだけ、ブラウザで Authorize を1回押してもらいます。

終わったら「スタート」と打てば始まります。以下は、何が入るかの説明です。

| 項目 | 必須？ | 何に使う | 確認コマンド | 入れ方 |
| --- | --- | --- | --- | --- |
| Node.js 18+ | **必須** | プレビュー、QA、HyperFrames | `node -v` | https://nodejs.org/ から LTS をインストール |
| Python 3 + Pillow | **必須** | 画像の変換・EXIF 除去・QA | `python -c "import PIL"` | https://www.python.org/ → `pip install pillow` |
| Cloudflare CLI（wrangler） | **必須** | 公開（メニュー 7）。ログインはブラウザで Allow を1回 | `npx wrangler --version` | セットアップで自動取得 |
| Codex CLI | 任意 | 画像の自動生成（ChatGPT の枠で） | `codex --version` | `npm i -g @openai/codex` → `codex login`（ChatGPT でログイン） |
| HyperFrames | **必須** | **ヒーロー動画**（KV をゆっくり動かす 8〜12 秒のループ mp4）と、その作り方のスキル | `npx hyperframes doctor` | 下の「HyperFrames を入れる」 |
| Playwright | 任意 | PC / SP のフルページスクショ（納品前確認） | `npx playwright --version` | `npm i -D playwright` → `npx playwright install chromium` |

Codex と HyperFrames が無くても LP は完成します。無い時は画像は ChatGPT 手動または持ち込み、ヒーローは CSS のズームで動きます。

## HyperFrames を入れる（ヒーロー動画を使いたい人）

HyperFrames は HTML で動画を作る仕組みです。入れると、スキルがキービジュアルから短いループ動画を作ってヒーローの背景に敷きます。写真がゆっくり寄っていくだけの CSS 版より、明らかに「映像」に見えます。

1. Node.js が入っていることを確認: `node -v`
2. スキルを入れる（Claude Code に HyperFrames の使い方を教える）:
   ```
   npx hyperframes skills
   ```
   `~/.claude/skills/` に `hyperframes` `hyperframes-core` `hyperframes-animation` などが入ります
3. レンダリング用のブラウザを入れる（1回だけ、約1分）:
   ```
   npx hyperframes browser ensure
   ```
4. 動作確認:
   ```
   npx hyperframes doctor
   ```
   `Chrome OK` が出ていれば完了。`ok: false` でも、NG が Docker / whisper-cpp / TTS / BGM だけなら問題ない（どれも任意で、ヒーロー動画には使わない）
5. Claude Code を開き直す（新しいスキルを読ませるため）

初回の `npx hyperframes ...` はダウンロードに 1〜2 分かかります。グローバルインストールは不要です（`npx` が毎回最新を使います）。

レンダリングはローカルで行い、10 秒の 1280×720 で 1〜3 分です。重い PC でなくても動きます。

## 自動チェックの中身（scripts/doctor）

Windows: `powershell -File scripts/doctor.ps1`　Mac: `bash scripts/doctor.sh`

出力例:

```
[OK ] Node.js v22.4.0
[OK ] Python 3.11 + Pillow 12.3
[-- ] Codex CLI なし → 画像は ChatGPT 手動 or 持ち込み
[-- ] HyperFrames なし → ヒーローは CSS アニメ
[-- ] Playwright なし → スクショは省略
```

`[NG]` が必須項目に出た時だけ止まります。`[--]` は任意なので、そのまま進めます。

チェックはネットワークに出ません（5 秒で終わります）。HyperFrames の本当の動作確認 `npx hyperframes doctor` は初回だけ 1〜2 分かかるので、ヒーロー動画を実際に作る時（メニュー 8 か `hero_video: yes`）にだけ実行します。
