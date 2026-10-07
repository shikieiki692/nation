#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""detect_noise.py —— 用「高边缘密度（二维码）」/「极低颜色数（纯色块）」识别页眉装饰噪点图。"""
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
    dark = sum(1 for v in px if v < 128) / len(px)
    e = 0
    for i in range(1, 64):
        for j in range(1, 64):
            a = px[i * 64 + j]
            if abs(a - px[(i - 1) * 64 + j]) > 60 or abs(a - px[i * 64 + j - 1]) > 60:
                e += 1
    ncol = len(set(Image.open(fp).convert("RGB").resize((32, 32), Image.LANCZOS).getdata()))
    return dark, e / (63 * 63), ncol


hits = []
for fp, ps in refs.items():
    try:
        w, h = Image.open(fp).size
    except Exception:
        continue
    if max(w, h) > 600:
        continue
    dark, edge, ncol = feats(fp)
    kind = None
    # 二维码＝纯黑白（颜色数极少）＋ 极高边缘密度 ＋ 黑白各占相当比例
    if ncol <= 10 and edge >= 0.20 and 0.20 <= dark <= 0.65:
        kind = "二维码"
    elif ncol <= 8 and dark >= 0.45:            # 纯色块/纯黑块
        kind = "纯色块"
    elif ncol <= 30 and edge >= 0.30 and dark >= 0.25:   # 高频纹理（烟花/装饰）
        kind = "装饰图"
    if kind:
        hits.append((kind, round(edge, 2), round(dark, 2), ncol, fp.replace(os.sep, "/"), len(ps)))

hits.sort(key=lambda x: (-x[1], -x[2]))
print("高置信噪点候选 %d 张：%s" % (len(hits), dict(collections.Counter(h[0] for h in hits))))
for kind, e, d, n, fp, nref in hits[:40]:
    print("   [%s] edge=%.2f dark=%.2f col=%d ×%d卡 %s" % (kind, e, d, n, nref, os.path.basename(fp)[:16]))
json.dump([[h[0], h[4]] for h in hits],
          open(os.path.join(R, ".workbuddy/tmp/opt_pipe/noise_hits.json"), "w"), ensure_ascii=False)
print("\n已存 noise_hits.json")
