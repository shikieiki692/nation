# -*- coding: utf-8 -*-
r"""图幅绝对宽度分布（只读）——找出「绝对偏小」的图（<6cm），与 dpi 余量无关。"""
import os, re, io, zipfile, glob
import numpy as np
from PIL import Image
os.chdir(r'C:\Obsidion\妙妙屋')
EMU = 360000.0
VOLS = ['X', 'XI', 'XIp', 'XIV', 'XV', 'XVI', 'XVII']
IMGDIRS = [r for r, d, f in os.walk('04-题库') if os.path.basename(r) == 'images']

def find_img(name):
    b = os.path.basename(name)
    for d in IMGDIRS:
        p = os.path.join(d, b)
        if os.path.isfile(p):
            return p
    return None

for V in VOLS:
    for tag, pat in [('学生版', '*学生版*'), ('答案版', '*答案*')]:
        f = glob.glob('00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷%s（%s.docx' % (V, pat))
        if not f:
            continue
        z = zipfile.ZipFile(f[0]); x = z.read('word/document.xml').decode('utf-8')
        rels = z.read('word/_rels/document.xml.rels').decode('utf-8')
        rid2f = {m.group(1): m.group(2) for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', rels)}
        ws = []
        for p in re.findall(r'<w:p[ >].*?</w:p>', x, re.S):
            if '<w:drawing' not in p:
                continue
            m = re.search(r'<wp:extent cx="(\d+)"', p); r = re.search(r'r:embed="(rId\d+)"', p)
            if not (m and r):
                continue
            w = float(m.group(1)) / EMU
            nm = rid2f.get(r.group(1), '')
            px = None
            fp = find_img(nm) if nm else None
            if fp:
                try:
                    px = Image.open(fp).size[0]
                except Exception:
                    pass
            ws.append((w, px))
        if not ws:
            print('%-6s %-4s 图 0 张' % (V, tag)); continue
        width = [w for w, _ in ws]
        tiny = [(w, px) for w, px in ws if w < 6.0]
        print('%-6s %-4s 图 %2d 张 ｜ 宽 min %.2f / 中位 %.2f / max %.2f cm ｜ <6cm 的 %d 张'
              % (V, tag, len(ws), min(width), sorted(width)[len(width)//2], max(width), len(tiny)))
        for w, px in tiny[:6]:
            print('          %.2fcm (源 %s px ⇒ 150dpi 上限 %.2fcm)' % (w, px, (px/150*2.54) if px else 0))
