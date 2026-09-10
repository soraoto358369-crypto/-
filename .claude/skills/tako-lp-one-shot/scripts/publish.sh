#!/usr/bin/env bash
# publish.sh — Cloudflare Pages に公開する（メニュー 7 / 「公開して」でスキルが実行する。Mac / Linux）
# 使い方: bash scripts/publish.sh <サイトのフォルダ> <プロジェクト名（英小文字・数字・ハイフン）>
DIR="$1"; NAME="$2"
[ -f "$DIR/index.html" ] || { echo "[NG ] $DIR に index.html がありません"; exit 1; }
echo "$NAME" | grep -Eq '^[a-z0-9][a-z0-9-]{0,56}[a-z0-9]$' || { echo "[NG ] プロジェクト名は英小文字・数字・ハイフンだけ（例: mame-kakeibo）"; exit 1; }
if ! npx -y wrangler whoami 2>&1 | grep -q "You are logged in"; then
  echo "[.. ] Cloudflare にログインします。ブラウザが開くので Allow を押してください"
  npx -y wrangler login 2>&1 | grep -E "https://|Success" | sed 's/^/      /'
fi
if ! npx -y wrangler pages project list 2>&1 | grep -Eq "(^|[[:space:]])$NAME([[:space:]]|$)"; then
  echo "[.. ] プロジェクト $NAME を作ります"
  R=$(npx -y wrangler pages project create "$NAME" --production-branch main 2>&1)
  echo "$R" | grep -Eqi "already|taken|exists" && { echo "[NG ] その名前は使われています。別の名前で（例: $NAME-2026）"; exit 1; }
fi
echo "[.. ] アップロード中: $DIR → $NAME"
OUT=$(npx -y wrangler pages deploy "$DIR" --project-name "$NAME" --branch main --commit-dirty=true 2>&1)
if echo "$OUT" | grep -q "Deployment complete"; then
  echo "[OK ] 公開しました → https://$NAME.pages.dev/"
  echo "      初回は反映まで1〜2分かかることがあります。スマホでも開いて確認してください"
else echo "[NG ] アップロードに失敗しました"; echo "$OUT" | tail -5; exit 1; fi
