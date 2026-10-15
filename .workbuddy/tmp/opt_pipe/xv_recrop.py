# -*- coding: utf-8 -*-
"""xv_recrop.py —— 定点重裁 XV 三张退化图（仅裁到 staging，不覆盖磁盘）。
1) 48b8cb40  3-2 MgSb      G80  p4   （旧框 y0=0.375 切掉 "Mg"）
2) 4b79f930  7-1 晶格      YS03 p2   （旧框 x0=0.36 切掉左下 c/b 坐标轴）
3) 9576157c  5-3-1 投影图  HYS  p9   （旧框过宽=连带右侧邻图空白、且切顶）
"""
import os
import sys

import numpy as np
import pymupdf as fitz
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
B = os.path.join(ROOT, "06-外部资料导入", "OCR", "01-题目")
STG = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "xv_recrop2")
os.makedirs(STG, exist_ok=True)

G80 = os.path.join(B, r"质心合集新\GChO模拟试题合集\ZCHEM-GChO80试题.pdf")
YS03 = os.path.join(B, r"2026一式暑期刷题班及数据\一式03\一式03.pdf")
HYS = os.path.join(B, r"第40届化英社化学奥林匹克（初赛）夏季\第40届化英社化学奥林匹克(初赛)夏季结构专题参考答案.pdf")


def crop(pdf, pno, name, box, zoom=3.4, dark=150, pad=6, zloc=3.0):
    d = fitz.open(pdf)
    pg = d[pno - 1]
    r = pg.rect
    clip = fitz.Rect(r.x0 + box[0] * r.width, r.y0 + box[1] * r.height,
                     r.x0 + box[2] * r.width, r.y0 + box[3] * r.height)
    pix = pg.get_pixmap(matrix=fitz.Matrix(zloc, zloc), clip=clip)
    g = np.asarray(Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("L"))
    sub = g < dark
    rws = np.where(sub.sum(axis=1) >= 2)[0]
    cls = np.where(sub.sum(axis=0) >= 2)[0]
    if len(rws) == 0 or len(cls) == 0:
        print("EMPTY", name); d.close(); return None
    bx = (max(0, cls[0] - pad), max(0, rws[0] - pad),
          min(g.shape[1], cls[-1] + pad), min(g.shape[0], rws[-1] + pad))
    nx0 = clip.x0 + bx[0] / zloc
    ny0 = clip.y0 + bx[1] / zloc
    nx1 = clip.x0 + bx[2] / zloc
    ny1 = clip.y0 + bx[3] / zloc
    pix2 = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=fitz.Rect(nx0, ny0, nx1, ny1))
    im = Image.frombytes("RGB", (pix2.width, pix2.height), pix2.samples)
    # 落盘相对页面比例（便于核对）
    fx0, fy0 = (nx0 - r.x0) / r.width, (ny0 - r.y0) / r.height
    fx1, fy1 = (nx1 - r.x0) / r.width, (ny1 - r.y0) / r.height
    print("%-10s 实际框=(%.4f,%.4f,%.4f,%.4f)  %dx%d" % (name, fx0, fy0, fx1, fy1, im.width, im.height))
    d.close()
    return im, (fx0, fy0, fx1, fy1)


def dewm(im, T=170, SAT=20):
    im = im.convert("RGB")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if (max(r, g, b) - min(r, g, b)) < SAT and (r + g + b) // 3 >= T:
                px[x, y] = (255, 255, 255)
    return im


JOBS = [
    (G80, 4, "48b8cb40", (0.360, 0.364, 0.660, 0.470), 150, False),
    (YS03, 2, "4b79f930", (0.130, 0.576, 0.900, 0.828), 150, False),
    (HYS, 9, "9576157c", (0.335, 0.6405, 0.675, 0.7482), 150, True),
]
for pdf, pno, name, box, dark, do_dewm in JOBS:
    out = crop(pdf, pno, name, box, dark=dark)
    if not out:
        continue
    im, frac = out
    if do_dewm:
        im = dewm(im)
    p = os.path.join(STG, name + ".jpg")
    im.save(p, "JPEG", quality=92)
    print("   -> ", p)
