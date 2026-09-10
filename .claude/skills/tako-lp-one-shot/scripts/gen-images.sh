#!/usr/bin/env bash
# gen-images.sh — Codex CLI (ChatGPT サブスク枠) で画像を一括生成する (macOS / Linux)
# 使い方: bash gen-images.sh prompts.json /path/to/site-src
# prompts.json: [{"name":"kv","prompt":"...","size":"1536x1024"}, ...]  (jq が必要)
set -u
PROMPTS="$1"; OUT="$2"; mkdir -p "$OUT"; LOG="$OUT/gen.log"
GEN="$HOME/.codex/generated_images"
n=$(jq length "$PROMPTS")
for ((i=0;i<n;i++)); do
  name=$(jq -r ".[$i].name" "$PROMPTS"); prompt=$(jq -r ".[$i].prompt" "$PROMPTS"); size=$(jq -r ".[$i].size // \"1536x1024\"" "$PROMPTS")
  if [ -f "$OUT/$name.png" ]; then echo "SKIP $name (exists)" | tee -a "$LOG"; continue; fi
  echo "=== $name start $(date +%T)" | tee -a "$LOG"
  t0=$(date +%s)
  codex exec --skip-git-repo-check "Generate an image: $prompt. Size $size. Do NOT try to copy or move the file afterwards; just generate it." < /dev/null 2>&1 | tail -n 1 | tee -a "$LOG"
  img=$(find "$GEN" -name '*.png' -newermt "@$t0" 2>/dev/null | xargs -I{} stat -f '%m %N' {} 2>/dev/null | sort -rn | head -n1 | cut -d' ' -f2-)
  if [ -n "$img" ]; then cp "$img" "$OUT/$name.png"; echo "OK $name" | tee -a "$LOG"; else echo "FAIL $name" | tee -a "$LOG"; fi
done
echo "ALL DONE" | tee -a "$LOG"
