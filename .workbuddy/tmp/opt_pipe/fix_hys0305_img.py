# -*- coding: utf-8 -*-
"""HYS-03-05 回源补图：从源 PDF 裁「5-3 俯视图与晶胞示意图」→ images/ → 插入题面区；顺清题面「化菜」噪音。"""
import hashlib
import os
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
PDF = os.path.join(R, r"06-外部资料导入\OCR\01-题目\第40届化英社化学奥林匹克（初赛）夏季\第40届化英社化学奥林匹克（初赛）夏季模拟试题3.pdf")
CARD = os.path.join(R, r"04-题库\2026机构初赛模拟题\化英社\题-HYS-03-05-硫与铜元素可形成多种化合物它.md")
IMGDIR = os.path.join(R, r"04-题库\2026机构初赛模拟题\化英社\images")
ANCHOR = "5-3 下图展示出了某种铜硫化合物的俯视图与晶胞示意图"

# ① 裁图（P5，纯图区；参数经目检确认）
doc = pymupdf.open(PDF)
pg = doc[4]
r = pg.rect
clip = pymupdf.Rect(0.030 * r.width, 0.363 * r.height, 0.970 * r.width, 0.544 * r.height)
pix = pg.get_pixmap(dpi=220, clip=clip)
jpg = pix.tobytes("jpeg", jpg_quality=92) if hasattr(pix, "tobytes") else pix.tobytes("png")
# PyMuPDF: 用 Pillow 转 jpg（稳妥）
from PIL import Image
import io
im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
buf = io.BytesIO()
im.save(buf, "JPEG", quality=92)
jpg = buf.getvalue()
doc.close()
h = hashlib.sha256(jpg).hexdigest()
name = h + ".jpg"
os.makedirs(IMGDIR, exist_ok=True)
dst = os.path.join(IMGDIR, name)
open(dst, "wb").write(jpg)
print("裁图 → %s  (%d×%d, %d bytes)" % (name[:20] + "…", im.width, im.height, len(jpg)))

# ② 插入题面 + 清「化菜」
t = open(CARD, encoding="utf-8-sig", newline="").read()
assert "\r" not in t, "CRLF 存在"
assert t.count("![](" + "images/" + name + ")") == 0
lines = t.split("\n")
ai = [i for i, l in enumerate(lines) if ANCHOR in l]
assert len(ai) == 1, "锚点命中 %d" % len(ai)
ai = ai[0]
# 清理紧随其后的「化菜」噪音行（含水印残留）
rm = 0
j = ai + 1
while j < len(lines) and j < ai + 5:
    s = lines[j].strip()
    if s in ("化菜", "化英社", "化"):
        del lines[j]
        rm += 1
        continue
    j += 1
# 在锚点行后插入空行 + 图 + 空行（若其后已有空行则不重复加尾空行）
ins = ["", "![](images/%s)" % name]
lines[ai + 1:ai + 1] = ins
t2 = "\n".join(lines)
# 收敛 3+ 连续空行
import re
t2 = re.sub(r"\n{4,}", "\n\n\n", t2)
assert t2.count("![](images/%s)" % name) == 1
assert "化菜" not in t2
open(CARD, "w", encoding="utf-8", newline="").write(t2)
print("题面已插入图；清理噪音 %d 行；CRLF=%s" % (rm, "\r" in open(CARD, "rb").read().decode("utf-8", "ignore")))
