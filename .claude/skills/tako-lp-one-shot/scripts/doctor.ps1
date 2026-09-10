# doctor.ps1 — 環境チェック（Windows）。スタート時にスキルが実行する。5秒で終わる（ネットワークに出ない）
# 出力: 1行1項目。[OK ] / [NG ] / [-- ](任意で未導入)。最後に JSON 1行
$r = [ordered]@{}
function has($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

# Node
if (has node) { $v = (node -v) 2>$null; $ok = [int]($v -replace '^v','' -split '\.')[0] -ge 18; $r.node = @{ok=$ok; v=$v}; Write-Output ("[{0}] Node.js {1}" -f ($(if($ok){"OK "}else{"NG "})), $v) }
else { $r.node = @{ok=$false}; Write-Output "[NG ] Node.js なし → https://nodejs.org/ から LTS を入れる" }

# Python + Pillow
if (has python) { $pv = (python --version) 2>&1; $pil = (python -c "import PIL,sys;print(PIL.__version__)") 2>$null
  if ($pil) { $r.python = @{ok=$true; v="$pv + Pillow $pil"}; Write-Output "[OK ] $pv + Pillow $pil" }
  else { $r.python = @{ok=$false; v="$pv"}; Write-Output "[NG ] $pv はあるが Pillow なし → pip install pillow" } }
else { $r.python = @{ok=$false}; Write-Output "[NG ] Python なし → https://www.python.org/ を入れて pip install pillow" }

# Codex (optional)
$cx = $null; if (has codex) { $cx = "codex" } else { $b = Get-ChildItem "$env:LOCALAPPDATA\OpenAI\Codex\bin" -Recurse -Filter codex.exe -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1; if ($b) { $cx = $b.FullName } }
if ($cx) { $cv = (& $cx --version) 2>&1 | Select-Object -First 1; $r.codex = @{ok=$true; v="$cv"}; Write-Output "[OK ] Codex CLI $cv → 画像は自動生成できる" }
else { $r.codex = @{ok=$false}; Write-Output "[-- ] Codex CLI なし → 画像は ChatGPT 手動 or 持ち込み（「セットアップ」で入る）" }

# HyperFrames (optional) — スキルの有無 + キャッシュの有無だけ見る（npx は実行しない: 遅いため）
$hfSkill = Test-Path "$env:USERPROFILE\.claude\skills\hyperframes\SKILL.md"
$hfBin = (Test-Path "$env:APPDATA\npm\node_modules\hyperframes") -or ((Test-Path "$env:LOCALAPPDATA\npm-cache\_npx") -and ((Get-ChildItem "$env:LOCALAPPDATA\npm-cache\_npx" -Recurse -Directory -Filter "hyperframes" -ErrorAction SilentlyContinue | Select-Object -First 1) -ne $null))
if ($hfSkill -and $hfBin) { $r.hyperframes = @{ok=$true}; Write-Output "[OK ] HyperFrames → ヒーロー動画を作れる（初回は npx hyperframes doctor で確認）" }
elseif ($hfSkill) { $r.hyperframes = @{ok=$false; skill=$true}; Write-Output "[-- ] HyperFrames スキルはあるが CLI が未取得 → npx hyperframes doctor を1回実行" }
else { $r.hyperframes = @{ok=$false; skill=$false}; Write-Output "[-- ] HyperFrames なし → 「セットアップ」と打つと入る（必須）" }

# Playwright (optional) — ローカル or グローバルの node_modules を見る
$pw = (Test-Path ".\node_modules\playwright") -or (Test-Path "$env:APPDATA\npm\node_modules\playwright")
if ($pw) { $r.playwright = @{ok=$true}; Write-Output "[OK ] Playwright → スクショを撮れる" } else { $r.playwright = @{ok=$false}; Write-Output "[-- ] Playwright なし → スクショは省略" }

Write-Output ("JSON " + ($r | ConvertTo-Json -Compress -Depth 3))
