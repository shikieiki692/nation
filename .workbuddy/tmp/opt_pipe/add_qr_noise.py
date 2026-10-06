# -*- coding: utf-8 -*-
"""把目检确认的**二维码噪声**并入 noise_hashes.json（union），供组卷判噪剔除。

候选规则（宁多勿少）：60≤边长≤160、近方、dark∈[0.20,0.55]。
随后**逐张目检**（拼版 render_out/_qr_cand.png）确认：
  非二维码（真结构图/多面体/晶胞）= 排序后的 #1-6、#29、#72-78 ⇒ 剔除；
  其余 = 二维码。
"""
import glob
import json
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r"C:\Obsidion\妙妙屋")
NF = os.path.join(".workbuddy", "tmp", "opt_pipe", "noise_hashes.json")
NONQR = {1, 2, 3, 4, 5, 6, 29, 72, 73, 74, 75, 76, 77, 78}   # 1-based，目检为「非二维码」

cand = []
for p in glob.glob("04-题库/2026机构初赛模拟题/*/images/*"):
    try:
        im = Image.open(p).convert("L")
    except Exception:
        continue
    w, h = im.size
    if not (60 <= w <= 160 and 60 <= h <= 160):
        continue
    if not (0.85 <= w / h <= 1.18):
        continue
    g = im.resize((200, 200))
    px = list(g.getdata())
    dark = sum(1 for v in px if v < 110) / len(px)
    if 0.20 <= dark <= 0.55:
        cand.append((os.path.basename(p), p, w, h, os.path.getsize(p), dark))
cand.sort(key=lambda x: x[5], reverse=True)

qr = [c for i, c in enumerate(cand, 1) if i not in NONQR]
print("候选 %d；目检确认二维码 %d" % (len(cand), len(qr)))

d = json.load(open(NF, encoding="utf-8"))
before = set(d.get("union", []))
qrset = {c[0] for c in qr}
d["qr"] = sorted(qrset)
d["union"] = sorted(before | qrset)
json.dump(d, open(NF, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("union %d → %d（新增 %d）" % (len(before), len(d["union"]), len(d["union"] - before)))
for c in qr[:5]:
    print("   %s  %dx%d %dB dark=%.3f" % (c[0][:40], c[2], c[3], c[4], c[5]))
