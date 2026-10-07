#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qr_detect2.py —— 二维码精判：纯黑白（灰阶像素极少）+ 高边缘密度 + 黑占比适中。"""
import glob, os, re, sys, collections, json
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image

R = r"C:\Obsidion\妙妙屋"
D = os.path.join(R, "04-题库/2026机构初赛模拟题")
refs = collections.defaultdict(list)
for p in glob.glob(D + "/**/题-*.md", recursive=True):
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    d = os.path.dirname(p)
    for n in set(re.findall(r"images/([0-9a-f]{32,}\.(?:jpg|png))", t)):
        fp = os.path.join(d, "images", n)
        if os.path.exists(fp):
            refs[fp].append(p)


def feats(fp):
    g = Image.open(fp).convert("L").resize((64, 64), Image.LANCZOS)
    px = list(g.getdata())
    n = len(px)
    dark = sum(1 for v in px if v < 100) / n
    mid = sum(1 for v in px if 100 <= v <= 200) / n      # 灰阶占比
    e = 0
    for i in range(1, 64):
        for j in range(1, 64):
            a = px[i * 64 + j]
            if abs(a - px[(i - 1) * 64 + j]) > 70 or abs(a - px[i * 64 + j - 1]) > 70:
                e += 1
    return dark, mid, e / (63 * 63)


hits = []
for fp, ps in refs.items():
    try:
        w, h = Image.open(fp).size
    except Exception:
        continue
    if max(w, h) > 600:
        continue
    dark, mid, edge = feats(fp)
    # 二维码：纯黑白（mid 极小）＋ 黑白都在场 ＋ 边缘密
    if mid <= 0.12 and 0.25 <= dark <= 0.60 and edge >= 0.18:
        hits.append((round(mid, 3), round(dark, 3), round(edge, 3), fp.replace(os.sep, "/"), len(ps)))

hits.sort(key=lambda x: x[0])
print("二维码精判候选 %d 张" % len(hits))
inst = collections.Counter()
cards = set()
for mid, dark, edge, fp, n in hits:
    for p in refs[fp]:
        inst[p.split(os.sep)[-2]] += 1
        cards.add(p)
print("涉及 %d 卡，按机构：%s" % (len(cards), dict(inst.most_common())))
for mid, dark, edge, fp, n in hits[:25]:
    print("   mid=%.3f dark=%.2f edge=%.2f %s" % (mid, dark, edge, os.path.basename(fp)[:16]))
json.dump([[h[3], h[0]] for h in hits], open(os.path.join(R, ".workbuddy/tmp/opt_pipe/qr2.json"), "w"), ensure_ascii=False)
