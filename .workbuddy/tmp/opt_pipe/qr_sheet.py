#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qr_sheet.py —— 放大拼版二维码候选（用于逐张目检）。用法：python qr_sheet.py <批次>"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image, ImageDraw
R = r"C:\Obsidion\妙妙屋"
sel = json.load(open(os.path.join(R, ".workbuddy/tmp/opt_pipe/qr_sel.json"), encoding="utf-8"))
b = int(sys.argv[1]) if len(sys.argv) > 1 else 0
N = 12
part = sel[b * N:(b + 1) * N]
W = 480
items = []
for r, fp in part:
    p = os.path.join(R, fp)
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert("RGB")
    items.append(("%.2f %s" % (r, os.path.basename(p)[:8]), im.resize((W, int(im.height * W / im.width)))))
cols = 4
rows = (len(items) + cols - 1) // cols
ch = max(i.height for _, i in items) + 22
c = Image.new("RGB", (cols * (W + 6), rows * ch), "white")
dr = ImageDraw.Draw(c)
for k, (n, im) in enumerate(items):
    rr, cc = divmod(k, cols)
    x = cc * (W + 6) + 3
    y = rr * ch + 18
    c.paste(im, (x, y))
    dr.text((x, y - 15), n, fill="red")
out = os.path.join(R, ".workbuddy/tmp/opt_pipe/render_out/_qr_b%d.png" % b)
c.save(out)
print(out, c.size, len(items))
