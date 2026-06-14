#!/usr/bin/env python3
"""deck 自动体检：截全每页 + 查溢出 + 扫四缘色差缝。把最易错的人工像素采样自动化（坑#4/#5）。

用法:  python3 deckcheck.py <index.html> [输出目录=_check] [色差阈值=12]
依赖:  python playwright（anaconda 装过；缺则提示 pip install playwright && playwright install chromium）

产出（落 输出目录/）:
  slide-N.png        每页干净截图（给作者 review，#5）
  seam-N-*.png       仅当某页四缘色差超阈值时，存下宽/高窗截图便于定位（#4）
退出码 0=全过；1=有溢出或色差缝。

原理:
  · 溢出(#5/#7): 取 .slide.active 的 scrollHeight，> slide 自身高度即内容被截。
  · 色差缝(#4): deck 被 fit 等比缩放居中，窗口非 slide 比例时四周露 body letterbox 条。
    用「比 slide 更宽」窗口测左右缝、「更高」窗口测上下缝：比对最外层(body)与紧贴 slide 边缘
    的一条像素，ΔRGB≈0 才算 body 底色 = slide 边缘色、无缝。
"""
import sys, os
import numpy as np
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else ""
OUT = sys.argv[2] if len(sys.argv) > 2 else "_check"
THR = float(sys.argv[3]) if len(sys.argv) > 3 else 12.0
if not SRC or not os.path.isfile(SRC):
    sys.exit("用法: python3 deckcheck.py <index.html> [输出目录] [阈值]")
os.makedirs(OUT, exist_ok=True)
ABS = "file://" + os.path.abspath(SRC)

try:
    from playwright.sync_api import sync_playwright
except Exception as e:
    sys.exit(f"缺 playwright: {e}\n  pip install playwright && playwright install chromium\n"
             f"  （只想截图可改用 scripts/preview.sh）")

def band(a):  # 取中间 60% 避开圆角/装饰
    n = a.shape[0]; lo = int(n*0.2); hi = int(n*0.8)
    return a[lo:hi]

def avg(px):  # px: (k,3) -> 平均 RGB
    return px.reshape(-1, 3).astype(np.float32).mean(0)

def dRGB(c1, c2):
    return float(np.abs(c1 - c2).max())

issues = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(device_scale_factor=1)
    pg.goto(ABS)
    pg.wait_for_timeout(400)
    info = pg.evaluate("""() => {
        const slides = [...document.querySelectorAll('.slide')];
        const s0 = slides[0];
        return {n: slides.length, hasShow: typeof window.show === 'function',
                sw: s0 ? s0.offsetWidth : 0, sh: s0 ? s0.offsetHeight : 0};
    }""")
    n, sw, sh = info["n"], info["sw"], info["sh"]
    if n == 0:
        sys.exit("没找到 .slide")
    print(f"deck: {n} 页, slide {sw}×{sh}, 阈值ΔRGB={THR}")

    # ---- 每页：干净截图 + 溢出检测 ----
    pg.set_viewport_size({"width": sw, "height": sh})
    for i in range(n):
        if info["hasShow"]:
            pg.evaluate(f"show({i})")
        pg.wait_for_timeout(550)  # 等 rise 入场动效结束
        m = pg.evaluate("""() => {
            const s = document.querySelector('.slide.active') || document.querySelectorAll('.slide')[0];
            return {sh: s.scrollHeight, ch: s.clientHeight};
        }""")
        pg.screenshot(path=os.path.join(OUT, f"slide-{i+1}.png"))
        over = m["sh"] - m["ch"]
        tag = "  ⚠ 溢出 %dpx，底部内容会被截" % over if over > 2 else "ok"
        print(f"  第{i+1}页 高度 {m['sh']}/{m['ch']}  {tag}")
        if over > 2:
            issues.append(f"第{i+1}页溢出 {over}px")

    # ---- 窄屏缩放居中（坑#11）：视口窄于 slide 时，slide 不能被裁出视口、且要居中 ----
    # 默认只测 ≥slide 尺寸的窗口会漏掉这个最常见的全屏裁切 bug（笔记本宽<1920）。
    print("检查窄屏缩放居中（slide 别被裁出视口、要居中）…")
    for vw, vh, tag in [(round(sw*0.7), round(sh*0.7), "等比窄屏"),
                        (round(sw*0.6), round(sh*0.92), "更窄异比")]:
        pg.set_viewport_size({"width": vw, "height": vh})
        if info["hasShow"]:
            pg.evaluate("show(0)")
        pg.wait_for_timeout(300)
        r = pg.evaluate("""() => {
            const s = document.querySelector('.slide.active') || document.querySelectorAll('.slide')[0];
            const b = s.getBoundingClientRect();
            return {l:Math.round(b.left), t:Math.round(b.top), r:Math.round(b.right), bo:Math.round(b.bottom)};
        }""")
        clip = []
        if r["r"] > vw+1: clip.append(f"右出界{r['r']-vw}px")
        if r["l"] < -1:   clip.append(f"左出界{-r['l']}px")
        if r["bo"] > vh+1: clip.append(f"下出界{r['bo']-vh}px")
        if r["t"] < -1:   clip.append(f"上出界{-r['t']}px")
        off = abs(r["l"] - (vw - r["r"])) > 2 or abs(r["t"] - (vh - r["bo"])) > 2
        if clip or off:
            why = " ".join(clip) if clip else "未居中(左右/上下留白不等)"
            print(f"  ⚠ {tag} {vw}x{vh}: {why}  → fit 缩放居中有问题（别用 flex 居中定尺 deck）")
            issues.append(f"{tag}{vw}x{vh} slide {why}")
        else:
            print(f"  {tag} {vw}x{vh}  ok 完整居中")

    # ---- 四缘色差缝 ----
    # 不假设居中：实测渲染后 slide 的 getBoundingClientRect，只采「真有 letterbox 条」的边
    # （居中布局 / 左上角锚定都对；某边没 bar 就根本不会有缝，不测）。
    GAP = 6          # bar 至少这么宽才值得测
    SAMP = 4         # 采样条厚度(px)
    worst = {}       # 每页每边取最大 ΔRGB，跨两次窗口去重
    def scan(label, vw, vh):
        pg.set_viewport_size({"width": vw, "height": vh})
        for i in range(n):
            if info["hasShow"]:
                pg.evaluate(f"show({i})")
            pg.wait_for_timeout(450)
            r = pg.evaluate("""() => {
                const s = document.querySelector('.slide.active') || document.querySelectorAll('.slide')[0];
                const b = s.getBoundingClientRect();
                return {l:Math.round(b.left), t:Math.round(b.top), r:Math.round(b.right), bo:Math.round(b.bottom)};
            }""")
            png = pg.screenshot()
            tmp = os.path.join(OUT, "_tmp.png")
            with open(tmp, "wb") as f: f.write(png)
            im = np.asarray(Image.open(tmp).convert("RGB"))
            H, W = im.shape[:2]
            l, t, rr, bo = r["l"], r["t"], r["r"], r["bo"]
            edges = []   # (边名, body条, slide边缘条)
            if l > GAP:                         # 左侧有 bar
                edges.append(("左", im[:, 2:2+SAMP], im[:, l+3:l+3+SAMP]))
            if W-rr > GAP:                       # 右侧有 bar
                edges.append(("右", im[:, W-2-SAMP:W-2], im[:, rr-3-SAMP:rr-3]))
            if t > GAP:                          # 上侧有 bar
                edges.append(("上", im[2:2+SAMP, :].transpose(1,0,2), im[t+3:t+3+SAMP, :].transpose(1,0,2)))
            if H-bo > GAP:                       # 下侧有 bar
                edges.append(("下", im[H-2-SAMP:H-2, :].transpose(1,0,2), im[bo-3-SAMP:bo-3, :].transpose(1,0,2)))
            hit = False
            for name, body, edge in edges:
                if body.shape[0] < 4 or edge.shape[0] < 4: continue
                d = dRGB(avg(band(body)), avg(band(edge)))
                if d > THR:
                    hit = True
                    cur = worst.setdefault(i+1, {})
                    if d > cur.get(name, 0): cur[name] = d
            if hit:
                Image.fromarray(im).save(os.path.join(OUT, f"seam-{i+1}-{label}.png"))
        if os.path.exists(os.path.join(OUT, "_tmp.png")):
            os.remove(os.path.join(OUT, "_tmp.png"))

    print("扫色差缝（body 底色是否 = slide 边缘色，只测真有 letterbox 的边）…")
    scan("wide", round(sw*1.3), sh)   # 更宽 → 逼出横向 letterbox
    scan("tall", sw, round(sh*1.3))   # 更高 → 逼出纵向 letterbox
    b.close()

for pg_no in sorted(worst):
    detail = " ".join(f"{nm}缘ΔRGB={d:.0f}" for nm, d in worst[pg_no].items())
    print(f"  ⚠ 第{pg_no}页色差缝: {detail}  → body 底色≠slide边缘色")
    issues.append(f"第{pg_no}页{detail}")

print("—" * 20)
if issues:
    print(f"✗ {len(issues)} 处问题：")
    for x in issues: print("  ·", x)
    sys.exit(1)
print(f"✓ 全过：{n} 页无溢出、四缘无色差缝。截图在 {OUT}/")
