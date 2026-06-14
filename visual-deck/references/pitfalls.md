# 踩坑清单（动手前读一遍，省下重蹈覆辙的时间）

这些都是真实踩过的坑，每条都让人卡过一阵。

## 1. imgen 不支持透明背景

`imgen ... -b transparent` 会报 **400「Transparent background is not supported」**。
→ 解法：出**白底图**，prompt 末尾加 `on a plain flat pale cream background, clear silhouette easy to cut out`，再用抠图工具去背景。

## 2. 抠透明：用 chroma_cut（自动阈值），别用 u2net 抠带白块的物件

- **`scripts/chroma_cut.py`（首选）**：连通域色键 + **自动阈值**，保护主体内部孔洞。需 scipy + PIL。
  ```bash
  python3 scripts/chroma_cut.py in.png out.png            # 阈值自动（推荐）
  python3 scripts/chroma_cut.py in.png out.png 16 2       # 手动: 阈值16 内缩2px（自动不准时再用）
  ```
  - **阈值必须自适应**（踩过）：旧版固定阈值，遇到「白主体 + 浅 cream 底」（白纸/白机器人）会把白块当背景**整片删掉** → 放上去漏出页面底色。现在按「背景峰之后第一个谷」自动选阈值，白主体那张也保得住。
  - 顺带 **1px 内缩**去掉边缘混色脏环——放到深色页面上不冒 cream/绿 halo（浅底看不出、深底才暴露，验证要放深底上看）。
  - 注：`cut.png` 只改 alpha、RGB 完好，所以 `Image.open(cut).convert("RGB")` 能还原原图重抠，不必重新出图。
- **`npx hyperframes remove-background in.png -o out.png`**（u2net）：对**人物/单一显著主体**好，CoreML 加速、首次下 168MB 模型。**但别用来抠「带大白块的物件」**（文档/表格/白纸）——它按显著性分割，会把不显著的大白块当背景丢掉（实测把白文档整张删了，只留蓝箭头）。这类一律用 chroma_cut。

## 3. 竖图素材塞进扁横条 → 脸只剩一半

时间线/列表里要放「视频帧缩略」时，**别用竖向半身人物图** cover 进扁横条——cover 只会显示一个横切片，脸永远不全，调 `background-position` 也救不了（横条根本放不下完整竖脸）。
→ 解法：专门用**横向构图** prompt 出一张「视频帧」素材（头肩对镜头、landscape 16:9），cover 进横条就能显示完整脸。见 `imgen-prompts.md` 的「横向视频帧」。

## 4. 全屏 letterbox 色差缝（最坑的一层）

> 视觉页现在和信息页一样是**定尺 `.slide`**（多挂一个 `bgcover` class，底图当 `.slide` 背景 cover）。早先「单页用 `position:fixed;inset:0` + vw 叠字、合成进 deck 才发现不铺满」的返工根因**已消除**——别再用 `position:fixed`/vw。但 letterbox 色差缝这件事本身还在，仍要防。

deck 被 `fit()` 等比缩放居中，窗口不是正好 slide 比例时，四周会露出 `body` 背景的 letterbox 边条。所以 **body 底色必须 = slide 边缘色**（deck.html 注释里有），别给 body 用和封面不一致的渐变，否则 deck 边缘一条色差缝。

**叠字遮罩还藏一个色差**：给底图叠白色遮罩压出文字区时，别用**斜向**渐变（如 `linear-gradient(100deg,…)`）——倾斜角会让某一角白色覆盖不足，把 imgen 底图本就不均匀的光斑/色块漏在文字**正后方**。改成**水平 `90deg` + 文字安全区一段实心近白「平台」再淡出**：`linear-gradient(90deg,#f3f8ff 0 40%,rgba(243,248,255,.6) 56%,transparent 72%)`，文字区彻底铺平、零色差。

**整图封面更麻烦**：full-bleed imgen 封面四边本身就不均匀（如左白右蓝），单一 body 色没法同时贴合四边 → 哪条边反差大就在哪冒缝。解法：① body 设成封面**主边缘色**（如左字封面取左缘近白色）；② 给封面底图加 **radial mask** 让四边淡出 + 一层 **inset box-shadow 同色内描边**羽化外圈，让四边都融进 body 色（注意：mask 会连 box-shadow 一起裁，rim 要放在**没被 mask 的另一层**，如 `::before`）。满幅封面的缝只在「非 16:9 窗口」露、真 16:9 播放不可见，也可直接接受这条警告，别为消缝硬加特效把观感做坏（踩过）。

**验证别再靠肉眼**：跑 `scripts/deckcheck.py index.html`——它自动用比 slide **更宽**和**更高**两种窗口截图、扫四缘像素报 ΔRGB（只在 1920×1080 下采样会漏掉边条这层），顺带把每页溢出也查了。ΔRGB 都接近 0 才算过。

## 5. 单页内容溢出 slide 高（默认 1080）

信息页元素塞太多会超出 slide 高被截（底部内容/时间轴消失）。
→ 解法：压缩元素高度和间距（卡片 padding、行间 margin、标题 `margin-bottom`），别硬塞。`.sbody{justify-content:center}` 让内容垂直居中，但前提是内容总高 < 可用高。
→ 别靠肉眼：`scripts/deckcheck.py` 会报每页 `scrollHeight` 超出 slide 高多少。

## 6. 本机没装 Chrome 也能截图预览（跨平台）

系统 Chrome 可能不存在。playwright 装过的话，缓存里有 headless chromium：
- macOS arm64：`~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell`
- macOS x64 / Linux：同结构，架构目录是 `…-mac-x64` / `…-linux64`；Linux 缓存根是 `~/.cache/ms-playwright`
- Windows（git-bash / WSL）：`%LOCALAPPDATA%/ms-playwright` 下同结构
`scripts/preview.sh` 已封装好跨平台查找（多缓存根 × 各架构通配 + 系统 chrome/chromium 兜底）。`--virtual-time-budget=1500` 让入场动效跑完再截、`--force-device-scale-factor=2` 出高清。`deckcheck.py` 走 python playwright 自带的 chromium，无需另找。

## 7. imgen 能出中文，但只信标题

imgen 出中文标题大字基本准，但**正文小字、密集文字偶有错字/乱码**。所以：拼接图/抽卡定风格时「只看风格别看字」；关键准确文字一律交给 HTML 叠，别指望 imgen 把一屏文字都拼对。

## 8. 入场动效的 transform 覆盖了居中用的 transform

deck.html 给标题块上了 `animation:rise`，而 rise 的结束帧是 `transform:translateY(0)`。如果同一个标题块又用 `transform:translateY(-50%)` 做垂直居中，**动画结束帧会盖掉居中位移**（同元素两个 transform，动画赢）→ 标题从中线掉下去 / 跑偏。
→ 解法：**居中交给 flex（父级 `align-items:center`），不要用 transform 居中**；transform 只留给入场位移（translateY 40→0），两者不再打架。本 skill 的 `visual-page.html` 已改成 flex 居中。

## 9. 在 .slide 上重声明 flex，忘了 flex-direction

基类 `.slide` 是 `display:flex;flex-direction:column`。封面/特殊页想垂直居中又写了 `display:flex;align-items:center`，但**漏了 `flex-direction:row`** → 仍是 column：`align-items:center` 变成**水平**居中、`justify-content` 默认 `flex-start` 把内容顶到**最上**。症状：标题卡在「右上 / 上方」，调 margin 也救不回来。
→ 解法：重新 flex 化 `.slide` 时**显式写 `flex-direction:row`**。要「左字右图」就 `flex-direction:row;align-items:center;justify-content:flex-start` + 文字块 `margin-left`。

## 10. 波形/EQ 用满圆角 + 少量粗条 → 看着像一串泡泡

`.wave i{flex:1;border-radius:999px}` 只放 ~18 根，每根被撑到 ~70px 宽 + 全圆角，读成气泡不是波形。
→ 解法：放**多根细条（~28–40 根）**、小圆角（4–6px）、`align-self:center` 做上下对称，就是「语音备忘录」那种波形识别度。

## 11. 全屏缩放别用 flex 居中定尺 deck —— 窄屏右边会被裁（最坑，必看）

定尺 `.deck`(默认 1920px 宽)靠 `.stage{display:flex;justify-content:center}` 居中、再 `transform-origin:center center` + `scale()` 缩放——**看似没问题，但视口宽 < 1920px 时右边会被裁掉一块**。原因：deck 的**布局宽**永远是 1920（transform 不改布局尺寸），视口窄于它时 deck 溢出 `.stage`，浏览器对溢出 flex 元素的居中处理会把左缘钉到 0、几何中心算成 960，绕中心缩放后整体右移 → 右侧出界被裁。**和比例无关**：1280×720 这种标准 16:9 笔记本照样裁 200+px。
→ 解法：**别靠 flex 居中**。`.deck` 用 `position:fixed;top:0;left:0;transform-origin:top left`，居中由 JS 显式算：
```js
function fit(){var d=document.querySelector('.deck');
  var sw=d.offsetWidth, sh=d.offsetHeight;
  var k=Math.min(innerWidth/sw, innerHeight/sh);
  var x=(innerWidth-sw*k)/2, y=(innerHeight-sh*k)/2;
  d.style.transform='translate('+x+'px,'+y+'px) scale('+k+')';}
```
单页 `fit.js` 同理。这是**等比缩放**（16:9 不变形）+ JS 居中，代价是非 16:9 窗口有 letterbox 边条（用坑#4 统一各页底色消缝）。验证：在 **1280×720 / 1366×768** 这类**窄于 1920** 的视口下截图，确认左右留白相等、右缘没出界。

## 12. 默认风格取向（可按项目改）

- 标题字偏**扁平描边**（白字+彩色描边+轻阴影），**不要厚重 3D 挤出字**（实测易被退回）
- 信息页别堆太满，留白舒服；默认面向非技术读者，文案直白
- 经历/数字/踩坑**不编**，没有就留 `> [!待补]` 问用户
- **别用 emoji 当图标**（🎭👍✅）：系统/平台渲染不一、一眼掉质感 → 一律 imgen 小图标抠透明当 `<img>`，或干净 CSS（纯符号 ✓✕ 可以，彩色 emoji 不行）
- **提质感靠"真素材"不靠特效**：多用 imgen 实体（吉祥物贯穿全场 + 焦点物件替代纯 CSS 卡），别堆豆腐块；别为让 deckcheck 色差归零给满幅封面硬加边缘描边/虚化（缝只在非 16:9 窗口露、真播放不可见，加特效反而把观感做坏）

## 13. 信息页版式雷同（不先出拼接图、套一个模板凭空写每页）

不先出「拼接结构总览图」就直接写 HTML，最容易每页都套同一个骨架（顶部 badge+标题横条 + 中间一块居中卡）→ 翻起来千篇一律，一眼就嫌「结构都差不多」、容易被推翻重做。
→ 解法（SKILL 第 1.5 步）：先让 imgen 出一张**全部页拼一张**的结构总览图（每格一页、版式各不同、风格统一、`-n 2/3` 可让用户选），选定后**逐页照对应格的布局排**——大数字压底 / 左右分栏 / 侧栏竖排 / 倾斜抽卡…换着来。
→ **风格统一 ≠ 版式统一**：配色 / 字体 / 质感 / 吉祥物全程一致（品牌一致性），但每页 layout 必须换（节奏）。一张拼接图既能总览整套风格，又顺带把版式也定了。
