# setup.ps1 — 「セットアップ」で走る全自動導入（Windows）。ユーザーはターミナルを触らない。スキルが実行する
# 入れるもの: Node.js LTS / Python 3 + Pillow / Codex CLI（Codex アプリ同梱のものを優先）/ HyperFrames（スキル + レンダ用ブラウザ）
# 使い方: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/setup.ps1 [-Agent claude|codex|both]
param([string]$Agent = "both")
$ErrorActionPreference = "Continue"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
function has($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function refreshPath { $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User") }
function say($s) { Write-Output $s }
function verOf($exe) { try { $t = (& $exe --version) 2>&1 | Select-Object -First 1; if ("$t" -match "(\d+)\.(\d+)\.(\d+)") { return [version]$matches[0] } } catch {}; return [version]"0.0.0" }
function addUserPath($dir) { $u = [Environment]::GetEnvironmentVariable("Path","User"); if ($u -notlike "*$dir*") { [Environment]::SetEnvironmentVariable("Path", ($dir + ";" + $u), "User") }; $env:Path = "$dir;" + $env:Path }
$hasWinget = has winget

say "=== Tako_LP_One-Shot セットアップ（Windows）==="

# 1) Node.js
if (has node) { say ("[OK ] Node.js " + (node -v)) }
else {
  say "[.. ] Node.js を入れます（winget）。許可のダイアログが出たら「はい」を押してください"
  if ($hasWinget) { winget install --id OpenJS.NodeJS.LTS -e --silent --accept-source-agreements --accept-package-agreements | Out-Null; refreshPath }
  if (has node) { say ("[OK ] Node.js " + (node -v) + " を入れました") } else { say "[NG ] Node.js を入れられませんでした → https://nodejs.org/ の LTS を手で入れて、もう一度「セットアップ」" }
}

# 2) Python + Pillow（Store の空コマンドは has でも通るので、実行して判定）
$pyOk = $false
try { $pv = (python --version) 2>&1; if ("$pv" -match "Python 3") { $pyOk = $true } } catch {}
if (-not $pyOk) {
  say "[.. ] Python を入れます（winget）"
  if ($hasWinget) { winget install --id Python.Python.3.12 -e --silent --accept-source-agreements --accept-package-agreements | Out-Null; refreshPath }
  try { $pv = (python --version) 2>&1; if ("$pv" -match "Python 3") { $pyOk = $true } } catch {}
}
if ($pyOk) {
  $pil = (python -c "import PIL;print(PIL.__version__)") 2>$null
  if (-not $pil) { say "[.. ] Pillow を入れます"; python -m pip install --quiet pillow 2>&1 | Out-Null; $pil = (python -c "import PIL;print(PIL.__version__)") 2>$null }
  if ($pil) { say "[OK ] $pv + Pillow $pil" } else { say "[NG ] Pillow を入れられませんでした → python -m pip install pillow" }
} else { say "[NG ] Python を入れられませんでした → https://www.python.org/ から入れて（Add to PATH にチェック）、もう一度「セットアップ」" }

# 3) Codex CLI（Codex アプリ同梱を優先。古い CLI は新しいモデルで止まることがあるので、新しい方を使う）
$codexExe = $null
$bundle = Get-ChildItem "$env:LOCALAPPDATA\OpenAI\Codex\bin" -Recurse -Filter codex.exe -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (has codex) { $codexExe = (Get-Command codex).Source }
if ($bundle -and (-not $codexExe -or ((verOf $bundle.FullName) -gt (verOf $codexExe)))) {
  addUserPath $bundle.DirectoryName; $codexExe = $bundle.FullName
  say ("[OK ] Codex CLI は Codex アプリ同梱版 " + (verOf $codexExe) + " を使います")
}
if (-not $codexExe -and (has npm)) {
  say "[.. ] Codex CLI を入れます（npm）"; npm i -g @openai/codex 2>&1 | Out-Null; refreshPath
  if (has codex) { $codexExe = (Get-Command codex).Source }
}
if ($codexExe) {
  $cv = (& $codexExe --version) 2>&1 | Select-Object -First 1
  $logged = Test-Path "$env:USERPROFILE\.codex\auth.json"
  if ($logged) { say "[OK ] Codex CLI $cv（ログイン済み）→ 画像を自動生成できる" } else { say "[.. ] Codex CLI $cv はあるがログイン前 → このあと codex login（ブラウザで Authorize を1回）" }
} else { say "[-- ] Codex CLI なし → 画像は ChatGPT 手動 or 持ち込み（Codex アプリを入れると自動生成できる）" }

# 4) HyperFrames（必須）: スキル + レンダ用ブラウザ
if (has npx) {
  say "[.. ] HyperFrames を入れます（1〜2分。初回だけ）"
  npx -y hyperframes skills 2>&1 | Select-Object -Last 2 | ForEach-Object { say "      $_" }
  npx -y hyperframes browser ensure 2>&1 | Select-Object -Last 1 | ForEach-Object { say "      $_" }
  $hfSkill = Test-Path "$env:USERPROFILE\.claude\skills\hyperframes\SKILL.md"
  if ($hfSkill -and ($Agent -eq "codex" -or $Agent -eq "both")) {
    New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
    Get-ChildItem "$env:USERPROFILE\.claude\skills" -Directory -Filter "hyperframes*" | ForEach-Object { Copy-Item $_.FullName "$env:USERPROFILE\.codex\skills\" -Recurse -Force }
  }
  if ($hfSkill) { say "[OK ] HyperFrames → ヒーロー動画を作れる" } else { say "[NG ] HyperFrames のスキルが入りませんでした → もう一度「セットアップ」" }
} else { say "[NG ] npx が無いので HyperFrames を入れられません（Node.js を入れてから、もう一度「セットアップ」）" }

# 5) Cloudflare CLI（公開用。取得だけ。ログインは公開時）
if (has npx) { npx -y wrangler --version 2>&1 | Select-Object -Last 1 | ForEach-Object { say "[OK ] Cloudflare CLI（wrangler）$_ → 「公開して」で使う" } }

say "=== 完了。「スタート」と打つと始まります ==="
