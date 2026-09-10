# gen-images.ps1 — Codex CLI (ChatGPT サブスク枠) で画像を一括生成する
# 使い方: powershell -NoProfile -ExecutionPolicy Bypass -File gen-images.ps1 -Prompts prompts.json -Out C:\path\to\site-src
# prompts.json: [{"name":"kv","prompt":"...","size":"1536x1024"}, ...]
# 前提: codex CLI が入っていて ChatGPT でログイン済み。1 枚あたり約 1 分。
param(
  [Parameter(Mandatory=$true)][string]$Prompts,
  [Parameter(Mandatory=$true)][string]$Out
)
New-Item -ItemType Directory -Force $Out | Out-Null
$jobs = Get-Content $Prompts -Raw -Encoding UTF8 | ConvertFrom-Json
$log = Join-Path $Out "gen.log"
foreach ($j in $jobs) {
  if (Test-Path (Join-Path $Out "$($j.name).png")) { "SKIP $($j.name) (exists)" | Tee-Object -FilePath $log -Append; continue }
  $size = if ($j.size) { $j.size } else { "1536x1024" }
  $t0 = Get-Date
  "=== $($j.name) start $t0" | Tee-Object -FilePath $log -Append
  '' | codex exec --skip-git-repo-check "Generate an image: $($j.prompt). Size $size. Do NOT try to copy or move the file afterwards; just generate it." 2>&1 | Select-Object -Last 1 | Tee-Object -FilePath $log -Append
  $img = Get-ChildItem "$env:USERPROFILE\.codex\generated_images" -Recurse -Filter *.png -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -gt $t0 } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($img) { Copy-Item $img.FullName (Join-Path $Out "$($j.name).png"); "OK $($j.name)" | Tee-Object -FilePath $log -Append }
  else { "FAIL $($j.name)" | Tee-Object -FilePath $log -Append }
}
"ALL DONE" | Tee-Object -FilePath $log -Append
