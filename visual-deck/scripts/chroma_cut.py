#!/usr/bin/env python3
"""连通域色键抠图：去掉与图像边缘连通的纯色背景，保护主体内部孔洞。

阈值自动（Otsu 自适应每张图）——解决「白色主体 + 浅色底」被整片误删的坑：
固定高阈值(旧默认52)会把和 cream 底很近的白纸/白机器人当背景灌掉；Otsu 按本图
背景簇与主体簇的间隙自动选阈值，白主体也能保住。再做 1px 内缩去掉边缘脏环(放到
深底上不会冒 cream/绿 halo)。

用法: chroma_cut.py in.png out.png [thr=auto] [erode=1]
  thr 传数字=手动阈值；传 auto 或不传=Otsu 自动。
需 scipy + PIL（anaconda 自带）。
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

inp, outp = sys.argv[1], sys.argv[2]
thr_arg = sys.argv[3] if len(sys.argv) > 3 else "auto"
erode = int(sys.argv[4]) if len(sys.argv) > 4 else 1

im = Image.open(inp).convert("RGBA")
arr = np.asarray(im).copy()
rgb = arr[..., :3].astype(np.float32)

# 背景色 = 四角 24x24 块平均
c = np.concatenate([
    rgb[:24, :24].reshape(-1, 3), rgb[:24, -24:].reshape(-1, 3),
    rgb[-24:, :24].reshape(-1, 3), rgb[-24:, -24:].reshape(-1, 3)])
bg = c.mean(0)
dist = np.sqrt(((rgb - bg) ** 2).sum(-1))


def valley_thr(vals, span=80, frac=0.01):
    """找「背景簇尾 ↔ 最近主体簇头」之间的谷做阈值。
    背景像素全挤在 dist≈0 的尖峰，主体（哪怕是接近底色的白纸）也和背景隔着一段空谷。
    全局 Otsu 会在「背景 vs 远处彩色」切、把近背景的白主体一起删——所以不用 Otsu。"""
    hist, edges = np.histogram(vals, bins=span, range=(0, span))
    if hist.sum() == 0:
        return 52.0
    peak = float(hist[:4].max())          # 背景峰在最低几个 bin
    floor = max(peak * frac, 1.0)
    i = 1
    while i < span and hist[i] >= floor:  # 背景簇尾
        i += 1
    bg_end = i
    j = bg_end
    while j < span and hist[j] < floor:   # 最近主体簇头
        j += 1
    thr = (bg_end + j) / 2.0 if j < span else bg_end + 8.0
    return float(edges[1] * thr)          # bin 宽=1，edges[1]=1


if thr_arg == "auto":
    thr = valley_thr(dist.ravel())
    thr = float(np.clip(thr, 6.0, 60.0))  # 防极端
    thr_mode = f"auto-valley={thr:.1f}"
else:
    thr = float(thr_arg)
    thr_mode = f"manual={thr:.1f}"

bgmask = dist < thr

# 只删与边缘连通的背景；主体内部接近背景色的孔洞保留
try:
    from scipy import ndimage
    lbl, n = ndimage.label(bgmask)
    edge = np.unique(np.concatenate([lbl[0], lbl[-1], lbl[:, 0], lbl[:, -1]]))
    edge = edge[edge != 0]
    connected = np.isin(lbl, edge)
    keep = ~connected
    # 1px 内缩：丢掉和背景混色的边缘脏环，深底上不冒 halo
    if erode > 0:
        keep = ndimage.binary_erosion(keep, iterations=erode)
    mode = f"connected-component (scipy, {n} labels, erode={erode})"
except Exception as e:
    keep = ~bgmask
    mode = f"flat-threshold (no scipy: {e})"

alpha = np.where(keep, 255, 0).astype(np.uint8)
# 边缘羽化 0.8px（内缩后只需轻羽化）
alpha_img = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.8))
arr[..., 3] = np.asarray(alpha_img)
Image.fromarray(arr).save(outp)
transp = 100.0 * (alpha < 128).mean()
print(f"OK {outp} | bg={bg.astype(int).tolist()} thr({thr_mode}) | {mode} | 透明={transp:.1f}%")
