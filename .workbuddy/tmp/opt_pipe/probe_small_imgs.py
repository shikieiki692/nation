# -*- coding: utf-8 -*-
"""列出某份 docx 中「渲染宽 < 阈值」或 dpi<150 的图（含 descr 与像素）。"""
import io
import os
import re
import sys
import zipfile

from PIL import Image

VAULT = r"C:\Obsidion\妙妙屋"
OUT = os.path.join(VAULT, "00-首页", "题组Word", "初赛模拟卷", "真题版式")
DRAW_RE = re.compile(r"<w:drawing>.*?</w:drawing>", re.S)
BLIP_RE = re.compile(r'<a:blip[^>]*r:embed="([^"]+)"')
DESCR_RE = re.compile(r'<pic:cNvPr[^>]*?\bdescr="([^"]*)"')
EXT_RE = re.compile(r'<wp:extent cx="(\d+)" cy="(\d+)"')
RELS_RE = re.compile(r'<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"')
EMU_CM = 360000

key = sys.argv[1]
W_MM = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0

for f in sorted(os.listdir(OUT)):
    if not f.endswith(".docx") or key not in f:
        continue
    z = zipfile.ZipFile(os.path.join(OUT, f))
    x = z.read("word/document.xml").decode("utf-8")
    rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
    rid2t = {m.group(1): m.group(2) for m in RELS_RE.finditer(rels)}
    print("=" * 92)
    print(f)
    for d in DRAW_RE.findall(x):
        b = BLIP_RE.search(d)
        e = EXT_RE.search(d)
        if not e:
            print("   ⚠️ 无 wp:extent 的 drawing：", d[:120].replace("\n", " "))
            continue
        nm = (DESCR_RE.search(d).group(1) if DESCR_RE.search(d) else "").strip()
        cx, cy = int(e.group(1)), int(e.group(2))
        w_mm, h_mm = cx / EMU_CM * 10, cy / EMU_CM * 10
        t = rid2t.get(b.group(1), "") if b else ""
        name = ("word/" + t.replace("../", "")) if t else ""
        px = None
        try:
            with Image.open(io.BytesIO(z.read(name))) as im:
                px = im.size
        except Exception as ex:
            px = ("ERR", str(ex)[:30])
        if w_mm < W_MM or h_mm < 20 or (isinstance(px, tuple) and px and isinstance(px[0], int) and px[0] / (w_mm / 25.4) < 150):
            dpi = (px[0] / (w_mm / 25.4)) if isinstance(px, tuple) and isinstance(px[0], int) else 0
            print("   %-38s %.1f×%.1fmm  px=%s  %.1fdpi  media=%s" % (nm[:38], w_mm, h_mm, px, dpi, name))
