# publish.ps1 — Cloudflare Pages に公開する（メニュー 7 / 「公開して」でスキルが実行する。Windows）
# 使い方: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/publish.ps1 -Dir <サイトのフォルダ> -Name <プロジェクト名（英数字とハイフン）>
# 初回: ログイン画面がブラウザで開く → Allow を押す。2回目以降はそのままアップされる。URL は https://<Name>.pages.dev
param([Parameter(Mandatory=$true)][string]$Dir, [Parameter(Mandatory=$true)][string]$Name)
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
if (-not (Test-Path (Join-Path $Dir "index.html"))) { Write-Output "[NG ] $Dir に index.html がありません"; exit 1 }
if ($Name -notmatch '^[a-z0-9][a-z0-9-]{0,56}[a-z0-9]$') { Write-Output "[NG ] プロジェクト名は英小文字・数字・ハイフンだけ（例: mame-kakeibo）"; exit 1 }

# 1) ログイン確認（未ログインならブラウザが開く）
$who = (npx -y wrangler whoami 2>&1 | Out-String)
if ($who -notmatch "You are logged in") {
  Write-Output "[.. ] Cloudflare にログインします。ブラウザが開くので Allow を押してください"
  npx -y wrangler login 2>&1 | Select-String "https://|Success" | ForEach-Object { Write-Output ("      " + $_.Line) }
}

# 2) プロジェクト（無ければ作る）
$list = (npx -y wrangler pages project list 2>&1 | Out-String)
if ($list -notmatch ("(^|\s)" + [regex]::Escape($Name) + "(\s|$)")) {
  Write-Output "[.. ] プロジェクト $Name を作ります"
  $r = (npx -y wrangler pages project create $Name --production-branch main 2>&1 | Out-String)
  if ($r -match "already|taken|exists") { Write-Output "[NG ] その名前は使われています。別の名前で（例: $Name-2026）"; exit 1 }
}

# 3) デプロイ
Write-Output "[.. ] アップロード中: $Dir → $Name"
$out = (npx -y wrangler pages deploy $Dir --project-name $Name --branch main --commit-dirty=true 2>&1 | Out-String)
if ($out -match "Deployment complete") {
  Write-Output "[OK ] 公開しました → https://$Name.pages.dev/"
  Write-Output "      初回は反映まで1〜2分かかることがあります。スマホでも開いて確認してください"
} else { Write-Output "[NG ] アップロードに失敗しました"; Write-Output ($out | Select-Object -Last 5) ; exit 1 }
