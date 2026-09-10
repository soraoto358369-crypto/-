#!/usr/bin/env bash
# doctor.sh — 環境チェック（macOS / Linux）。スタート時にスキルが実行する。5秒で終わる（ネットワークに出ない）
ok(){ echo "[OK ] $1"; } ; ng(){ echo "[NG ] $1"; } ; op(){ echo "[-- ] $1"; }
J="{"
if command -v node >/dev/null; then v=$(node -v); maj=${v#v}; maj=${maj%%.*}; if [ "$maj" -ge 18 ]; then ok "Node.js $v"; J+="\"node\":true,"; else ng "Node.js $v は古い → 18 以上"; J+="\"node\":false,"; fi
else ng "Node.js なし → https://nodejs.org/ から LTS を入れる"; J+="\"node\":false,"; fi
PY=""; for c in python3 python; do if command -v $c >/dev/null && $c --version >/dev/null 2>&1 && ! $c --version 2>&1 | grep -qi "not found"; then PY=$c; break; fi; done
if [ -n "$PY" ]; then pv=$($PY --version 2>&1); pil=$($PY -c "import PIL;print(PIL.__version__)" 2>/dev/null)
  if [ -n "$pil" ]; then ok "$pv + Pillow $pil"; J+="\"python\":true,"; else ng "$pv はあるが Pillow なし → pip install pillow"; J+="\"python\":false,"; fi
else ng "Python なし → https://www.python.org/ を入れて pip install pillow"; J+="\"python\":false,"; fi
if command -v codex >/dev/null; then ok "Codex CLI $(codex --version 2>&1 | head -1) → 画像は自動生成できる"; J+="\"codex\":true,"; else op "Codex CLI なし → 画像は ChatGPT 手動 or 持ち込み（「セットアップ」で入る）"; J+="\"codex\":false,"; fi
HFS=0; [ -f "$HOME/.claude/skills/hyperframes/SKILL.md" ] && HFS=1
HFB=0; { [ -d "$(npm root -g 2>/dev/null)/hyperframes" ] || ls -d "$HOME/.npm/_npx"/*/node_modules/hyperframes >/dev/null 2>&1; } && HFB=1
if [ $HFS = 1 ] && [ $HFB = 1 ]; then ok "HyperFrames → ヒーロー動画を作れる（初回は npx hyperframes doctor で確認）"; J+="\"hyperframes\":true,"
elif [ $HFS = 1 ]; then op "HyperFrames スキルはあるが CLI が未取得 → npx hyperframes doctor を1回実行"; J+="\"hyperframes\":false,"
else op "HyperFrames なし → ヒーローは CSS アニメ（npx hyperframes skills で入る）"; J+="\"hyperframes\":false,"; fi
if [ -d "./node_modules/playwright" ] || [ -d "$(npm root -g 2>/dev/null)/playwright" ]; then ok "Playwright → スクショを撮れる"; J+="\"playwright\":true}"; else op "Playwright なし → スクショは省略"; J+="\"playwright\":false}"; fi
echo "JSON $J"
