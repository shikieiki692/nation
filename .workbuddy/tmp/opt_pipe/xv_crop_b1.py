# -*- coding: utf-8 -*-
"""xv_crop_b1.py —— XV 重制第一批裁切（常量模块级；执行调用仅在 __main__，⛔ 可安全 import）"""
import os
import sys

import numpy as np
import pymupdf as fitz
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
B = os.path.join(ROOT, "06-外部资料导入", "OCR", "01-题目")
STG = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "xv_img_staging")
os.makedirs(STG, exist_ok=True)

G80 = os.path.join(B, r"质心合集新\GChO模拟试题合集\ZCHEM-GChO80试题.pdf")
YS03 = os.path.join(B, r"2026一式暑期刷题班及数据\一式03\一式03.pdf")
HZ7 = os.path.join(B, r"2026年8月汇智长沙夏令营刷题班\2026暑假长沙化学刷题试题\长沙化学刷初赛模拟7.pdf")
HZ1 = os.path.join(B, r"2026年夏令营汇智长沙班\长沙冲刺测试卷\长沙冲刺综合1.pdf")
HYS = os.path.join(B, r"第40届化英社化学奥林匹克（初赛）夏季\第40届化英社化学奥林匹克(初赛)夏季结构专题参考答案.pdf")


def crop_pt(pdf, pno, name, box_frac, zoom_out=3.4, dark=150, pad=6):
    """box_frac=(x0,y0,x1,y1) 页面比例粗窗 → trim_to_ink → zoom_out 裁切 → staging"""
    doc = fitz.open(pdf)
    pg = doc[pno - 1]
    r = pg.rect
    x0 = r.x0 + box_frac[0] * r.width
    y0 = r.y0 + box_frac[1] * r.height
    x1 = r.x0 + box_frac[2] * r.width
    y1 = r.y0 + box_frac[3] * r.height
    clip = fitz.Rect(x0, y0, x1, y1)
    zloc = 3.0
    pix = pg.get_pixmap(matrix=fitz.Matrix(zloc, zloc), clip=clip)
    g = np.asarray(Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("L"))
    sub = g < dark
    rws = np.where(sub.sum(axis=1) >= 2)[0]
    cls = np.where(sub.sum(axis=0) >= 2)[0]
    if len(rws) == 0 or len(cls) == 0:
        print("EMPTY", name)
        doc.close()
        return
    bx = (max(0, cls[0] - pad), max(0, rws[0] - pad),
          min(g.shape[1], cls[-1] + pad), min(g.shape[0], rws[-1] + pad))
    nx0 = r.x0 + (clip.x0 + bx[0] / zloc)
    ny0 = r.y0 + (clip.y0 + bx[1] / zloc)
    nx1 = r.x0 + (clip.x0 + bx[2] / zloc)
    ny1 = r.y0 + (clip.y0 + bx[3] / zloc)
    pix2 = pg.get_pixmap(matrix=fitz.Matrix(zoom_out, zoom_out),
                         clip=fitz.Rect(nx0, ny0, nx1, ny1))
    im = Image.frombytes("RGB", (pix2.width, pix2.height), pix2.samples)
    doc.close()
    im.save(os.path.join(STG, name + ".jpg"), "JPEG", quality=92)
    print("saved %-14s %dx%d" % (name, im.width, im.height))


if __name__ == "__main__":
    crop_pt(G80, 4, "48b8cb40", (0.40, 0.375, 0.60, 0.462))
    crop_pt(G80, 4, "0a59b27c", (0.27, 0.578, 0.50, 0.725))
    crop_pt(G80, 4, "84e8d115", (0.48, 0.578, 0.72, 0.725))
    crop_pt(YS03, 2, "4b79f930", (0.36, 0.578, 0.87, 0.782))
    crop_pt(HZ7, 4, "0bc567c5", (0.08, 0.705, 0.42, 0.802))
    crop_pt(HZ1, 4, "NEW_gangyu", (0.16, 0.085, 0.68, 0.44))
