#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sheet_A.py —— 把「无文字层届」的兜底定位卡按首片拼版，供目检。
用法：python sheet_A.py <批次号>   （每批 10 张）
"""
import glob, json, os, re, sys
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe")
import gcho_crop as GC
R = r"C:\Obsidion\妙妙屋"
NOTEXT = [6, 7, 9, 13, 14, 18, 19, 23, 24, 25, 26, 34, 40, 43, 46, 54, 63, 68]
rows = []
for rnd in NOTEXT:
    f = os.path.join(GC.LOC, "GChO%d.json" % rnd)
    if not os.path.exists(f):
        continue
    idx = json.load(open(f, encoding="utf-8"))
    order = [m[0] for m in GC.markers(idx, 150)]
    for c in sorted(glob.glob(os.path.join(GC.GDIR, "题-GChO-%02d-*.md" % rnd))):
        q = GC.card_qno(c)
        if q is None or q in order:
            continue
        t = open(c, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
        j = t.find("## 参考答案"); k = t.find("## 知识点映射")
        if "手写解析手稿" not in t[j:k]:
            continue
        ims = re.findall(r"!\[\]\(images/([^)]+)\)", t[j:k])
        rows.append((rnd, q, len(ims), c, [os.path.join(os.path.dirname(c), "images", n) for n in ims]))

batch = int(sys.argv[1]) if len(sys.argv) > 1 else 0
sel = rows[batch * 10:(batch + 1) * 10]
print("兜底卡共 %d 张；本批 %d 张（#%d）" % (len(rows), len(sel), batch))
W = 330; items = []
for rnd, q, n, c, fps in sel:
    im = Image.open(fps[0]).convert("RGB")
    items.append(("届%d 第%d题 图%d %dx%d" % (rnd, q, n, im.width, im.height),
                  im.resize((W, int(im.height * W / im.width)))))
if not items:
    sys.exit(0)
cols = 5; rowsn = (len(items) + cols - 1) // cols; ch = max(i.height for _, i in items) + 22
canv = Image.new("RGB", (cols * (W + 6), rowsn * ch), "white"); dr = ImageDraw.Draw(canv)
for kk, (n, im) in enumerate(items):
    r, cc = divmod(kk, cols); x = cc * (W + 6) + 3; y = r * ch + 18
    canv.paste(im, (x, y)); dr.text((x, y - 15), n, fill="red")
out = os.path.join(R, ".workbuddy/tmp/opt_pipe/render_out/_A_b%d.png" % batch)
canv.save(out); print(out, canv.size)
