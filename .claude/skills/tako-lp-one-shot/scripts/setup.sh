#!/usr/bin/env bash
# setup.sh — 「セットアップ」で走る全自動導入（Mac / Linux）。ユーザーはターミナルを触らない。スキルが実行する
# 入れるもの: Node.js LTS / Python 3 + Pillow / Codex CLI（Codex アプリ同梱のものを優先）/ HyperFrames（スキル + レンダ用ブラウザ）
# 使い方: bash scripts/setup.sh [claude|codex|both]
AGENT="${1:-both}"
say(){ echo "$1"; }
has(){ command -v "$1" >/dev/null 2>&1; }
say "=== Tako_LP_One-Shot セットアップ（Mac / Linux）==="

# 1) Node.js
if has node; then say "[OK ] Node.js $(node -v)"
else
  say "[.. ] Node.js を入れます"
  if has brew; then brew install node@22 >/dev/null 2>&1 || brew install node >/dev/null 2>&1; fi
  if has node; then say "[OK ] Node.js $(node -v) を入れました"
  else say "[NG ] Node.js を入れられませんでした → https://nodejs.org/ の LTS を入れて、もう一度「セットアップ」"; fi
fi

# 2) Python + Pillow
PY=""; for c in python3 python; do if has "$c" && "$c" --version 2>&1 | grep -q "Python 3"; then PY="$c"; break; fi; done
if [ -z "$PY" ] && has brew; then say "[.. ] Python を入れます"; brew install python >/dev/null 2>&1; has python3 && PY=python3; fi
if [ -n "$PY" ]; then
  PIL=$("$PY" -c "import PIL;print(PIL.__version__)" 2>/dev/null)
  if [ -z "$PIL" ]; then say "[.. ] Pillow を入れます"; "$PY" -m pip install --quiet pillow >/dev/null 2>&1 || "$PY" -m pip install --quiet --user pillow >/dev/null 2>&1 || "$PY" -m pip install --quiet --break-system-packages pillow >/dev/null 2>&1; PIL=$("$PY" -c "import PIL;print(PIL.__version__)" 2>/dev/null); fi
  if [ -n "$PIL" ]; then say "[OK ] $("$PY" --version 2>&1) + Pillow $PIL"; else say "[NG ] Pillow を入れられませんでした → $PY -m pip install pillow"; fi
else say "[NG ] Python を入れられませんでした → https://www.python.org/ から入れて、もう一度「セットアップ」"; fi

# 3) Codex CLI（アプリ同梱を優先）
CODEX=""
if has codex; then CODEX="$(command -v codex)"
else
  B=$(ls -t "$HOME/Library/Application Support/OpenAI/Codex/bin"/*/codex 2>/dev/null | head -1)
  if [ -n "$B" ]; then
    D=$(dirname "$B"); grep -q "$D" "$HOME/.zshrc" 2>/dev/null || echo "export PATH=\"$D:\$PATH\"" >> "$HOME/.zshrc"; export PATH="$D:$PATH"; CODEX="$B"
    say "[OK ] Codex CLI（Codex アプリ同梱）を使えるようにしました"
  elif has npm; then say "[.. ] Codex CLI を入れます（npm）"; npm i -g @openai/codex >/dev/null 2>&1; has codex && CODEX="$(command -v codex)"; fi
fi
if [ -n "$CODEX" ]; then
  CV=$("$CODEX" --version 2>&1 | head -1)
  if [ -f "$HOME/.codex/auth.json" ]; then say "[OK ] Codex CLI $CV（ログイン済み）→ 画像を自動生成できる"; else say "[.. ] Codex CLI $CV はあるがログイン前 → このあと codex login（ブラウザで Authorize を1回）"; fi
else say "[-- ] Codex CLI なし → 画像は ChatGPT 手動 or 持ち込み（Codex アプリを入れると自動生成できる）"; fi

# 4) HyperFrames（必須）
if has npx; then
  say "[.. ] HyperFrames を入れます（1〜2分。初回だけ）"
  npx -y hyperframes skills 2>&1 | tail -2 | sed 's/^/      /'
  npx -y hyperframes browser ensure 2>&1 | tail -1 | sed 's/^/      /'
  if [ -f "$HOME/.claude/skills/hyperframes/SKILL.md" ]; then
    if [ "$AGENT" = "codex" ] || [ "$AGENT" = "both" ]; then mkdir -p "$HOME/.codex/skills"; cp -R "$HOME/.claude/skills/"hyperframes* "$HOME/.codex/skills/" 2>/dev/null; fi
    say "[OK ] HyperFrames → ヒーロー動画を作れる"
  else say "[NG ] HyperFrames のスキルが入りませんでした → もう一度「セットアップ」"; fi
else say "[NG ] npx が無いので HyperFrames を入れられません（Node.js を入れてから、もう一度「セットアップ」）"; fi

if has npx; then say "[OK ] Cloudflare CLI（wrangler）$(npx -y wrangler --version 2>&1 | tail -1) → 「公開して」で使う"; fi

say "=== 完了。「スタート」と打つと始まります ==="
