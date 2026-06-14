#!/bin/bash
# 截图预览 HTML —— 封装 playwright 缓存里的 headless chromium（本机常没装 Chrome）
# 用法: bash preview.sh <源.html> <输出.png> [宽=1920] [高=1080]
# 跨平台: macOS(arm64/x64) / Linux(x64)。Windows 走 git-bash / WSL 时也能命中 %LOCALAPPDATA%。
set -e
SRC="$1"; OUT="$2"; W="${3:-1920}"; H="${4:-1080}"
[ -z "$SRC" ] || [ -z "$OUT" ] && { echo "用法: bash preview.sh <源.html> <输出.png> [宽] [高]"; exit 1; }

# 找 headless chromium：遍历各平台 playwright 缓存根 × 各平台二进制路径（版本号/架构用通配）
BIN=""
for ROOT in "$HOME/Library/Caches/ms-playwright" "$HOME/.cache/ms-playwright" "$LOCALAPPDATA/ms-playwright"; do
  [ -z "$ROOT" ] && continue
  for G in \
    "$ROOT"/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell \
    "$ROOT"/chromium-*/chrome-linux/chrome \
    "$ROOT"/chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium ; do
    C=$(ls $G 2>/dev/null | head -1)
    [ -n "$C" ] && { BIN="$C"; break; }
  done
  [ -n "$BIN" ] && break
done
# 缓存里没有就退回系统装的 chrome / chromium
if [ -z "$BIN" ]; then
  for X in google-chrome-stable google-chrome chromium chromium-browser \
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium" ; do
    if command -v "$X" >/dev/null 2>&1; then BIN="$X"; break; fi
    if [ -x "$X" ]; then BIN="$X"; break; fi
  done
fi
[ -z "$BIN" ] && { echo "找不到 headless chromium。先跑一次 npx playwright install chromium，或装 Chrome/Chromium。"; exit 1; }

# 转绝对路径（file:// 需要）
ABS="$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")"

"$BIN" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=1500 \
  --force-device-scale-factor=2 --screenshot="$OUT" --window-size="${W},${H}" \
  "file://$ABS" 2>/dev/null

[ -f "$OUT" ] && echo "OK: $OUT" || { echo "FAIL"; exit 1; }
