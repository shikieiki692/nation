#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""phash_cluster.py —— 对机构模拟题的小尺寸引用图做感知哈希聚类，
找出「反复出现的同一装饰图」（页眉二维码／logo 的典型特征）。"""
import glob, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image

D = "04-题库/2026机构初赛模拟题"


def phash(fp, size=8):
    im = Image.open(fp).convert("L").resize((size, size), Image.LANCZOS)
    px = list(im.getdata())
    avg = sum(px) / len(px)
    bits = 0
    for i, v in enumerate(px):
        if v > avg:
            bits |= (1 << i)
    return bits


refs = collections.defaultdict(list)
for p in glob.glob(D + "/**/题-*.md", recursive=True):
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    d = os.path.dirname(p)
    for n in set(re.findall(r"images/([0-9a-f]{32,}\.(?:jpg|png))", t)):
        fp = os.path.join(d, "images", n)
        if os.path.exists(fp):
            refs[fp].append(p)

small = []
for fp, ps in refs.items():
    try:
        w, h = Image.open(fp).size
    except Exception:
        continue
    if max(w, h) <= 320:                       # 只看小图（噪点候选）
        small.append((fp, w, h, len(ps)))
print("小图 %d 张，计算指纹…" % len(small))

clusters = collections.defaultdict(list)
for fp, w, h, nref in small:
    try:
        clusters[phash(fp)].append((fp, w, h, nref))
    except Exception:
        pass

big = [(k, v) for k, v in clusters.items() if len(v) >= 5]
big.sort(key=lambda x: -len(x[1]))
print("指纹簇 ≥5 张的：%d 簇" % len(big))
out = []
for k, v in big[:40]:
    print("  簇 %d 张：%s" % (len(v), ", ".join("%dx%d×%d" % (w, h, n) for _, w, h, n in v[:4])))
    out.append([x[0].replace(os.sep, "/") for x in v])
import json
json.dump(out, open(".workbuddy/tmp/opt_pipe/phash_clusters.json", "w"), ensure_ascii=False)
print("\n已存 phash_clusters.json")
