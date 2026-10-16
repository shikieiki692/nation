# -*- coding: utf-8 -*-
r"""把卷 O2 第 N 题答案区的图拼成带标签接触表（一次 Read 目检多图）。"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image, ImageDraw  # noqa: E402

os.chdir(r"C:\Obsidion\妙妙屋")
Q = int(sys.argv[1]) if len(sys.argv) > 1 else 8
V = r"04-题库/初赛模拟卷O2（有机·答案版）.md"
IMG_DIRS = [r"04-题库/2026机构初赛模拟题/chemy/images",
            r"04-题库/2026机构初赛模拟题/壹尖培优/images",
            r"04-题库/2026机构初赛模拟题/伽马/images",
            r"04-题库/2026机构初赛模拟题/化英社/images",
            r"04-题库/2026机构初赛模拟题/清北营/images"]

L = io.open(V, encoding="utf-8-sig", newline="").read().replace("\r\n", "\n").split("\n")
s = next(i for i, l in enumerate(L) if l.startswith("### 第 %d 题" % Q))
e = next((i for i, l in enumerate(L) if l.startswith("### 第 %d 题" % (Q + 1))), len(L))
seg = L[s:e]
# 只取答案区
a = next((i for i, l in enumerate(seg) if l.strip() == "#### 答案"), 0)
seg = seg[a:]
found = []
for k, l in enumerate(seg):
    for m in re.finditer(r"!\[\[([0-9a-f]{64}\.\w+)", l):
        found.append((s + a + k + 1, m.group(1)))
print("答案区图 %d 张" % len(found))

thumbs = []
for ln, name in found:
    p = next((os.path.join(d, name) for d in IMG_DIRS if os.path.exists(os.path.join(d, name))), None)
    if not p:
        print("  ⛔ 缺文件", name[:12])
        continue
    im = Image.open(p).convert("RGB")
    w, h = im.size
    tw = 620
    im = im.resize((tw, max(1, int(h * tw / w))), Image.LANCZOS)
    thumbs.append((ln, name, im))

COLS, PAD, HDR = 3, 8, 22
rows = (len(thumbs) + COLS - 1) // COLS
colw = max(t[2].size[0] for t in thumbs)
rowhs = []
for r in range(rows):
    rowhs.append(max(t[2].size[1] for t in thumbs[r * COLS:(r + 1) * COLS]) + HDR)
W = COLS * colw + (COLS + 1) * PAD
H = sum(rowhs) + (rows + 1) * PAD
sheet = Image.new("RGB", (W, H), "white")
dr = ImageDraw.Draw(sheet)
y = PAD
for r in range(rows):
    x = PAD
    for t in thumbs[r * COLS:(r + 1) * COLS]:
        ln, name, im = t
        dr.text((x + 2, y + 4), "L%d  %s" % (ln, name[:10]), fill="red")
        sheet.paste(im, (x, y + HDR))
        x += colw + PAD
    y += rowhs[r] + PAD
out = r".workbuddy/tmp/opt_pipe/ansSheet_Q%d.png" % Q
sheet.save(out)
print("接触表 →", out, sheet.size)
