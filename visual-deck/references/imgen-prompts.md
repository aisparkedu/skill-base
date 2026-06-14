# imgen prompt 模板

imgen 的 prompt **英文质量更好**；要图里出中文时，把中文文字用引号明确写进 prompt（但记住坑 #7：只信标题大字）。

**出图尺寸跟 slide 比例走，默认横版**：16:9 用 `-s 1536x864`。换比例就换尺寸 + 把 prompt 里的 `horizontal 16:9` 改掉（竖版 `-s 864x1536` + `vertical 9:16`，方图 `-s 1024x1024`）。底图比例要和 `--slide-w/--slide-h` 一致，否则 cover 会裁掉构图。

> `imgen` 是一个文生图 CLI（输出 PNG，`-s` 尺寸 / `-q` 质量 / `-o` 输出 / `-i` 图生图）。不是本 skill 自带、也非通用公开工具——把你自己的文生图 CLI 别名成 `imgen` 并对齐参数即可，详见 README。

## A0. 拼接结构总览图（排版蓝本 · SKILL 第 1.5 步，最先做）

一张图放下「全部页缩略 + 每页不同版式 + 统一风格」，照它逐页排 HTML。要点：① 网格排布（3×2 / 4×2…按页数）② **每格点名一个不同版式** ③ 反复压 unified style + 同一吉祥物 ④ 文字只要灰条占位（`NO readable letters`，准确字之后 HTML 叠）⑤ 想给选择感就 `-n 2`/`-n 3` 出变体。⑥ 锁既定风格/吉祥物 → 用 `-i 参考图.png` 图生图。

模板：
```
A clean montage 'slide template overview sheet': <N> presentation slide thumbnails in a <列>x<行> grid on a soft light background, small gaps. Each thumbnail is a 16:9 slide with a DIFFERENT layout: (1) <封面: 左标题块+右吉祥物>; (2) <横向步骤流程卡+箭头>; (3) <超大背景数字+单焦点面板>; (4) <左侧彩色竖栏+右侧纵向清单>; (5) <左深色输入框+右浅色成品卡 对照>; (6) <结尾 CTA + 吉祥物庆祝>. Unified visual style across ALL six: <风格词, 如 glossy pink-blue glassmorphism cartoon>, rounded soft cards, the SAME <吉祥物> recurring in several thumbnails. Only simple grey placeholder bars where text goes, NO readable letters. Organized, premium.
```
尺寸用整图比例（默认横版 `-s 1536x864`）。出图后**逐格当版式蓝本**：第 2/3 步逐页照对应格的布局排，每页天然不同。

## A. 视觉页「留白底图」（图当底 + HTML 叠字的核心）

目标：主体在一侧、另一侧大面积留白、**图里不放主标题文字**，给 HTML 叠字腾地方。出不透明整图，当背景用。

模板：
```
3D <风格> style horizontal 16:9 banner background. <主体描述>, placed on the RIGHT third of the frame. The LEFT two-thirds is clean empty <留白色> space reserved for a title to be added later. <可选装饰: clouds, stars...>. <质感词>. NO text anywhere in the image.
```

实例（黏土风封面底图）：
```
3D clay claymation style horizontal 16:9 banner background. A cute boy with black curly hair in a purple hoodie sitting at a desk with a laptop, clapperboard and plant, placed on the RIGHT third. The LEFT two-thirds is clean empty soft lavender-purple space reserved for a title. Cute clouds and a star top-right. Soft matte plasticine texture. NO text anywhere in the image.
```
尺寸 `-s 1536x864`（16:9）。留白侧可左可右，和 HTML 叠字位置对应即可。

## B. 横向「视频帧」素材（给信息页里的片段缩略）

避开坑 #3：要横向头肩构图，cover 进横条才显示完整脸。
```
3D <风格> style, <人物> talking to camera, head and shoulders portrait, soft plain studio background, horizontal landscape framing, face fully visible and centered, <质感词>
```
尺寸 `-s 1536x864`。这种当 clip 背景用 `background:linear-gradient(色罩),url(...);background-size:cover`，色罩区分不同状态（如删除前紫罩/删除后绿罩）。

## C. 白底素材（图标/小人/物件，待抠透明）

避开坑 #1：出白底，末尾必加便于抠图的话。
```
3D <风格> app icon of <物件>, <颜色> rounded, soft matte texture, glossy highlight, centered, on a plain flat pale cream background, clear silhouette easy to cut out
```
出图后用 `scripts/chroma_cut.py` 抠透明（自动阈值，**白色主体也能保住**——见坑#2）。
> 主体若**几乎全是白/极浅**、和 cream 底贴太近，自动阈值仍可能分不开 → prompt 把底色换成一个**和主体差异大的纯色**（如 `plain flat green background` / 强蓝），chroma_cut 就稳了。带白块的物件**别用 u2net**（会把白块当背景丢，坑#2）。

## C2. 吉祥物（贯穿全场，重在「同一只」）

出一个全身吉祥物，白底待抠，全套每页复用（封面放大、信息页放角落做反应）。机器人最好保持一致、也最「AI」：
```
<风格词> illustration of a cute friendly <角色: assistant robot / boy…>, <特征: white rounded body, glowing screen face smiling>, <动作: waving hello>, soft <配色> palette, clean smooth 3D, soft drop shadow, centered, full body, on a plain flat pale cream background, clear silhouette easy to cut out
```
**要多个姿势又不变脸**：先出本体，再 `imgen -i 本体.png "<同一角色>... now pointing to the side / thumbs up / holding a blank sign..."` **图生图**出姊妹姿势——别重新文生图（会变成另一只）。出图后 `chroma_cut.py` 抠透明。

## D. 风格词参考（换风格改这里，黏土只是默认）

| 风格 | 关键词 |
|---|---|
| 黏土 3D（默认） | `3D clay claymation, soft matte plasticine, rounded` |
| 亮色卡通 | `bright flat-cartoon, bold black outline, vivid, playful` |
| 等距 2.5D | `isometric 2.5D, soft pastel tech palette, dimensional` |
| 玻璃科技 | `clean light-tech, glassmorphism, frosted, soft blue-white` |
| 杂志极简 | `editorial minimalist, white space, thin lines, serif accent` |

### 「抽卡定风格」轻量法（极简稿、不需要版式多样时）

不出拼接图、只想快速定个风格调性：同一构图用 4-6 个不同风格词各出一张，**只看风格调性别看字**，让用户挑一个定下来，整套统一用它。多页且要版式多样时，优先用 A0 的拼接结构总览图（它顺带把版式也定了）。
