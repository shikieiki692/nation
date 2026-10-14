# -*- coding: utf-8 -*-
r"""图幅 + dpi 余量（只读，直接从 docx media 取像素）。"""
import os, re, io, zipfile, glob
from PIL import Image
os.chdir(r'C:\Obsidion\妙妙屋')
EMU = 360000.0

for V in ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']:
    for tag, pat in [('学生', '*学生版*'), ('答案', '*答案*')]:
        f = glob.glob('00-首页/题组Word/初赛模拟卷/真题版式/初赛模拟卷%s（%s.docx' % (V, pat))
        if not f:
            continue
        z = zipfile.ZipFile(f[0]); x = z.read('word/document.xml').decode('utf-8')
        rels = z.read('word/_rels/document.xml.rels').decode('utf-8')
        rid2f = {m.group(1): m.group(2) for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', rels)}
        rows = []
        for p in re.findall(r'<w:p[ >].*?</w:p>', x, re.S):
            if '<w:drawing' not in p:
                continue
            m = re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"', p); r = re.search(r'r:embed="(rId\d+)"', p)
            if not (m and r):
                continue
            w = float(m.group(1)) / EMU
            nm = rid2f.get(r.group(1), '')
            px = py = None
            if nm:
                try:
                    im = Image.open(io.BytesIO(z.read('word/media/' + nm)))
                    px, py = im.size
                except Exception:
                    pass
            rows.append((w, px))
        if not rows:
            print('%-6s %-3s 图 0' % (V, tag)); continue
        head = 0; dpi_min = 1e9; dpi_list = []
        for w, px in rows:
            if not px:
                continue
            dpi = px / (w / 2.54)
            dpi_list.append(dpi)
            if dpi > 205:      # 余量 > 1.35x
                head += 1
        ws = [w for w, _ in rows]
        print('%-6s %-3s 图 %2d ｜ 宽 min %.2f/中位 %.2f/max %.2f cm ｜ dpi min %5.0f ｜ 余量>1.35x 的 %d 张'
              % (V, tag, len(rows), min(ws), sorted(ws)[len(ws)//2], max(ws), (min(dpi_list) if dpi_list else 0), head))
