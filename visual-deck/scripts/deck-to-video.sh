#!/bin/bash
# 把一套 deck 文件夹脚手架成 hyperframes 视频工程（建配置 + 拷图片素材 + 落 composition 模板）。
# 用法: bash deck-to-video.sh <deck目录> <输出工程目录>
# 之后两步：
#   1. 按 references/hyperframes.md 把 deck 内容填进 <工程>/index.html
#   2. cd <工程> && npm run check && npm run render   （出片在 renders/）
set -e
DECK="$1"; OUT="$2"
{ [ -z "$DECK" ] || [ -z "$OUT" ]; } && { echo "用法: bash deck-to-video.sh <deck目录> <输出工程目录>"; exit 1; }
[ -d "$DECK" ] || { echo "找不到 deck 目录: $DECK"; exit 1; }
HFVER="0.6.52"
SKILLDIR="$(cd "$(dirname "$0")/.." && pwd)"
DECK_ABS="$(cd "$DECK" && pwd)"

# 安全锁：原 deck 的 index.html 是要保留直接用的成品，绝不在它上面改。
# composition 一律是独立工程里的新文件 → 拒绝把工程目录指到 deck、或覆盖已有 index.html。
if [ -e "$OUT" ]; then
  OUT_ABS="$(cd "$OUT" && pwd)"
  [ "$OUT_ABS" = "$DECK_ABS" ] && { echo "✗ 工程目录不能=deck目录（会覆盖原 deck 的 index.html）。换一个新目录。"; exit 1; }
  [ -f "$OUT/index.html" ] && { echo "✗ $OUT/index.html 已存在，拒绝覆盖。换一个空目录。"; exit 1; }
fi

mkdir -p "$OUT/assets" "$OUT/renders"

# 拷 deck 的图片素材进 assets/（composition 里图片路径要相应改成 assets/…）
find "$DECK" -maxdepth 1 -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.webp' \) -exec cp {} "$OUT/assets/" \; 2>/dev/null || true

cat > "$OUT/hyperframes.json" <<'JSON'
{
  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": { "blocks": "compositions", "components": "compositions/components", "assets": "assets" }
}
JSON

cat > "$OUT/package.json" <<JSON
{
  "name": "hf-deck", "private": true, "type": "module",
  "scripts": {
    "dev": "npx --yes hyperframes@$HFVER preview",
    "check": "npx --yes hyperframes@$HFVER lint && npx --yes hyperframes@$HFVER validate",
    "render": "npx --yes hyperframes@$HFVER render"
  }
}
JSON

cat > "$OUT/meta.json" <<JSON
{ "id": "hf-deck", "name": "$(basename "$OUT")" }
JSON

cp "$SKILLDIR/assets/skeleton/hf-composition.html" "$OUT/index.html"

echo "✅ 工程已建: $OUT （原 deck $DECK 只读、未改动，可继续直接用）"
echo "图片已拷进 assets/:"; ls "$OUT/assets" 2>/dev/null | sed 's/^/   /'
echo ""
echo "下一步:"
echo "  1. 按 references/hyperframes.md 把 deck 内容填进 $OUT/index.html"
echo "     （每页改 .slide.clip + data-start；图片路径改 assets/…；复用图加 ?1 ?2 唯一化）"
echo "  2. cd \"$OUT\" && npm run check && npm run render"
echo "  3. 抽帧自检: ffmpeg -ss 1.6 -i renders/*.mp4 -frames:v 1 /tmp/chk.png  （看中文/动效/图）"
