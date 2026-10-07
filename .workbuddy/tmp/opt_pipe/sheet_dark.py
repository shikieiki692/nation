#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sheet_dark.py —— 把黑占比候选拼版，供目检。用法：python sheet_dark.py <批次>"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image, ImageDraw
R = r"C:\Obsidion\妙妙屋"
cand = json.load(open(os.path.join(R, ".workbuddy/tmp/opt_pipe/dark_cand.json"), encoding="utf-8"))
b = int(sys.argv[1]) if len(sys.argv) > 1 else 0
sel = cand[b * 30:(b + 1) * 30]
W = 260
items = []
for r, fp in sel:
    p = os.path.join(R, fp)
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert("RGB")
    items.append(("%.2f %s" % (r, os.path.basename(p)[:10]), im.resize((W, int(im.height * W / im.width)))))
if not items:
    sys.exit("no items")
cols = 6
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
out = os.path.join(R, ".workbuddy/tmp/opt_pipe/render_out/_dark_b%d.png" % b)
c.save(out)
print(out, c.size, len(items))
