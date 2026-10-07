#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dark_ratio.py —— 按「黑色像素占比」筛二维码类噪点图（二维码约 30~55%，结构式 <15%）。"""
import glob, os, re, sys, collections, json
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image

D = "04-题库/2026机构初赛模拟题"
refs = collections.defaultdict(list)
for p in glob.glob(D + "/**/题-*.md", recursive=True):
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    d = os.path.dirname(p)
    for n in set(re.findall(r"images/([0-9a-f]{32,}\.(?:jpg|png))", t)):
        fp = os.path.join(d, "images", n)
        if os.path.exists(fp):
            refs[fp].append(p)


def dark_ratio(fp):
    im = Image.open(fp).convert("L")
    small = im.resize((64, 64), Image.LANCZOS)
    px = list(small.getdata())
    dark = sum(1 for v in px if v < 128)
    return dark / len(px), im.size


# 正样本：CM-12-07 已确认的二维码
POS = ["1bb27ea368a70b785cffe66c629104cffebc432ca4c94975967808863db0bac1",
       "adce5881eb2216caa4ff051e602dd0e7dd199201791df13af56568ce745d3372"]
print("=== 正样本校准（二维码）===")
for h in POS:
    for fp in refs:
        if h in fp:
            r, sz = dark_ratio(fp)
            print("   %s… %s 黑占比 %.2f" % (h[:10], sz, r))
            break

print("\n=== 疑似噪点候选（方形 且 黑占比 ≥0.22）===")
cand = []
for fp, ps in refs.items():
    try:
        w, h = Image.open(fp).size
    except Exception:
        continue
    if max(w, h) > 400 or not (0.8 <= w / max(1, h) <= 1.25):
        continue
    r, sz = dark_ratio(fp)
    if r >= 0.22:
        cand.append((r, fp.replace(os.sep, "/"), sz, len(ps)))
cand.sort(reverse=True)
print("共 %d 张" % len(cand))
for r, fp, sz, n in cand[:30]:
    print("   %.2f  %s  ×%d卡  %s" % (r, sz, n, os.path.basename(fp)[:18]))
json.dump([[r, fp] for r, fp, _, _ in cand], open(".workbuddy/tmp/opt_pipe/dark_cand.json", "w"), ensure_ascii=False)
