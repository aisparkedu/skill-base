# deck → 动态视频（hyperframes）

把做好的静态翻页 deck，转成会动的 MP4。用 **hyperframes**（HeyGen 的 HTML→视频框架，`npx hyperframes@0.6.52` 实测跑通；不锁版本可去掉 `@0.6.52`）。
不用 Remotion——那个要把 deck 重写成 React，纯属重做。

> **铁律：原 deck 的 `index.html` 是要保留直接用的成品，出视频绝不在它上面改。** composition 一律是**独立工程目录里的新文件**——`deck-to-video.sh` 把 deck 当只读、产出落到你指定的独立目录，并加锁拒绝把工程目录指到 deck 或覆盖已有 `index.html`。原 deck 始终原样可用。

## 一条命令脚手架

```bash
bash scripts/deck-to-video.sh <deck目录> <输出工程目录>
# 例: bash scripts/deck-to-video.sh ./my-deck ./my-deck-video
```
它建好 hyperframes 工程（`hyperframes.json`/`package.json`/`meta.json`）、把 deck **根目录**的图片拷进 `assets/`（图片在子目录的话脚手架后手动补拷），落一份 `index.html`（= `assets/skeleton/hf-composition.html` 模板）。剩下就是把 deck 内容填进 composition + 渲染。

## 把 deck 内容填进 composition（改造清单）

模板已搭好骨架，照着把 deck 搬进去：

1. **样式**：deck 的样式整段贴进模板，**删三类**——`.stage`/`.deck` 及缩放、`fit()`/翻页、`.slide` 的 opacity 切换和 `@keyframes` 入场动效（入场交给 GSAP）。`.slide` 用模板里的 `position:absolute;inset:0` 铺满 `#root`。
2. **每页变 clip**：每个 `.slide` 加 `class="clip"`，并补三个属性——`data-start="序号×PER"`、`data-duration="PER"`、`data-track-index="1"`；再给每页一个唯一 `id`（lint 要求）。框架按时间窗自动显隐每页，不用你写翻页 JS。
3. **图片路径**：deck 里 `mascot.png` 之类改成 `assets/mascot.png`。
4. **复用图唯一化**：同一张图（如吉祥物每页都放）每处 `src` 加 `?1 ?2 …`，否则被当「重复媒体」去重、可能渲错。
5. **时长**：`#root` 的 `data-duration` = 页数 × PER（模板里 PER=3，5 页 → 15）。
6. **入场动效**：模板底部的 GSAP 循环已通用（每页内容淡入+上浮、`.mascot` 浮动），一般不用改；要调节奏改 `PER` 和那几个 duration。

## 渲染 + 自检

```bash
cd <工程目录>
npm run check     # lint + validate，0 error 才往下（warning 多数可忽略，见下）
npm run render    # 出片在 renders/*.mp4
# 抽帧自检（中文有没有掉 / 动效在不在 / 图在不在）：
ffmpeg -ss 1.6 -i renders/*.mp4 -frames:v 1 /tmp/chk.png
```

## 实测踩过的坑

- **字体**：hyperframes 字体表里没有中文，会报 `No deterministic font mapping for var(--font)`。**实测中文走 fallback CJK 照样干净可读**，可直接用。要精确用 deck 的圆体/PingFang，就在 composition 里加 `@font-face` 指向一个 `assets/fonts/*.woff2`（模板里有注释好的两行，解开即可）。
- **重复媒体**：同源图不唯一化会触发 `duplicate_media_discovery_risk`，加 `?N` 解决（见清单第 4 条）。
- **只允许确定性逻辑**：composition 里禁 `Date.now()` / `Math.random()` / `fetch()`——渲染靠逐帧 seek 时间轴，非确定性会崩。
- **clip 是显隐开关**：可见的计时元素**必须**有 `class="clip"`，否则框架不控制它的显隐。
- **GSAP 必须 paused + 注册**：`window.__timelines["main"] = gsap.timeline({paused:true})`，渲染器去 seek 它。
- **`npm run dev` 是常驻服务**：要预览就后台跑，别前台（会超时）。
- **可忽略的 warning**：`timeline_track_too_dense`（页数多）、`studio_missing_editable_id`（已给 id 就没了）、`AudioContext`（无音频，无害）、对比度 `contrast` warning（浅底+白描边字的设计取向，不影响渲染）。

> 参考：composition 模板 `assets/skeleton/hf-composition.html`；脚手架 `scripts/deck-to-video.sh`；hyperframes 文档 https://hyperframes.heygen.com/introduction
