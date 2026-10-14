# -*- coding: utf-8 -*-
r"""pilot：在源 PDF 的内嵌图里按内容检索目标图，命中即无损提取（只读探查，不写库）。"""
import os, io, glob, sys
import numpy as np
from PIL import Image
import fitz, cv2
os.chdir(r'C:\Obsidion\妙妙屋')

TARGETS = ['373c9cadfe512cf9', 'b8c987a2cb8e0b53']
PDFS = glob.glob('06-外部资料导入/OCR/chemy/第33届*.pdf')

def find_target(pre):
    for r, d, f in os.walk('04-题库'):
        if os.path.basename(r) != 'images':
            continue
        for fn in f:
            if fn.startswith(pre):
                return os.path.join(r, fn)
    return None

def norm(a, size=(96, 96)):
    g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY) if a.ndim == 3 else a
    g = cv2.resize(g, size, interpolation=cv2.INTER_AREA)
    g = cv2.GaussianBlur(g, (3, 3), 0)
    return g.astype(np.float32)

for pre in TARGETS:
    fp = find_target(pre)
    a = np.asarray(Image.open(fp).convert('L'))
    t = norm(a)
    t = (t - t.mean()) / (t.std() + 1e-6)
    print('=== 目标 %s  %dx%d ===' % (pre, a.shape[1], a.shape[0]))
    best = []
    for pdf in PDFS:
        d = fitz.open(pdf)
        for pno in range(d.page_count):
            pg = d[pno]
            xrefs = {im[0] for im in pg.get_images(full=True)}
            for xref in xrefs:
                try:
                    info = d.extract_image(xref)
                except Exception:
                    continue
                try:
                    im = Image.open(io.BytesIO(info['image'])).convert('L')
                except Exception:
                    continue
                if min(im.size) < 40:
                    continue
                arr = np.asarray(im)
                if arr.ndim != 2:
                    continue
                c = norm(arr)
                c = (c - c.mean()) / (c.std() + 1e-6)
                score = float((c * t).mean())
                best.append((score, pdf.split('/')[-1][:22], pno + 1, im.size, len(info['image'])))
        d.close()
    best.sort(reverse=True)
    print('  内嵌图候选 %d 个，前 6：' % len(best))
    for s, pdf, p, sz, nb in best[:6]:
        print('    score=%.3f  %s p%d  %s  %d bytes' % (s, pdf, p, sz, nb))
    if best and best[0][0] > 0.9:
        w, h = a.shape[1], a.shape[0]
        sw, sh = best[0][3]
        print('  ⇒ 命中，尺寸增益 %.2fx (宽) / %.2fx (高)' % (sw / w, sh / h))
    print()
