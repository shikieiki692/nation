#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qr_list.py —— 由 dark_cand.json 筛出「二维码」高置信集合（0.41≤dark≤0.52 且方形），
统计其来源卡/机构，并输出清单。"""
import json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image
R = r"C:\Obsidion\妙妙屋"
cand = json.load(open(os.path.join(R, ".workbuddy/tmp/opt_pipe/dark_cand.json"), encoding="utf-8"))
# 图 → 引用它的卡
D = os.path.join(R, "04-题库/2026机构初赛模拟题")
refs = collections.defaultdict(list)
for p in __import__("glob").glob(D + "/**/题-*.md", recursive=True):
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    d = os.path.dirname(p)
    for n in set(re.findall(r"images/([0-9a-f]{32,}\.(?:jpg|png))", t)):
        fp = os.path.join(d, "images", n)
        if os.path.exists(fp):
            refs[os.path.basename(fp)].append(p)

sel = [(r, fp) for r, fp in cand if 0.41 <= r <= 0.52]
print("二维码候选 %d 张" % len(sel))
inst = collections.Counter()
cards = set()
for r, fp in sel:
    for p in refs.get(os.path.basename(fp), []):
        inst[p.split(os.sep)[-2]] += 1
        cards.add(p)
print("涉及 %d 张卡，按机构：" % len(cards))
for k, v in inst.most_common():
    print("   %-12s %d 处" % (k, v))
json.dump([[r, fp] for r, fp in sel], open(os.path.join(R, ".workbuddy/tmp/opt_pipe/qr_sel.json"), "w"), ensure_ascii=False)
print("\n卡清单（前 20）：")
for c in sorted(cards)[:20]:
    print("   ", c.replace(R + os.sep, "").replace(os.sep, "/")[:80])
json.dump(sorted(c.replace(os.sep, "/") for c in cards),
          open(os.path.join(R, ".workbuddy/tmp/opt_pipe/qr_cards.json"), "w"), ensure_ascii=False)
