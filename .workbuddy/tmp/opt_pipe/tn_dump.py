# -*- coding: utf-8 -*-
"""吞图 10 张 — 题面全文 + 答案区首段（只读）。"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\Obsidion\妙妙屋\04-题库\2026机构初赛模拟题"

CARDS = [
    ("清北营",   "题-QBY-02-04-下图为实验室制备12二溴乙烷.md", (32, 72)),
    ("清北营",   "题-QBY-03-09-Ineleganolide最.md",          (33, 70)),
    ("chemy",    "题-CM-63-03-二氧化钛除金红石外还有多种晶.md", (32, 62)),
    ("chemy",    "题-CM-95-08-利用大量可得的天然不对称化合.md", (33, 66)),
    ("chemy",    "题-CM-103-05-生物正交反应是在活细胞内进行.md", (33, 72)),
    ("chemy",    "题-CM-12-07-71近年人们发现高压下可以制.md",  (31, 74)),
    ("chemy",    "题-CM-17-02-锂离子电池技术的进步极大地推.md", (34, 84)),
    ("chemy",    "题-CM-138-09-观察下图所示合成路线并回答后.md", (33, 72)),
    ("化英社",   "题-HYS-03-04-甲烷单加氧酶MMO可在常温常.md",  (32, 76)),
    ("质心UChO", "题-UChO-02-06-下图为一种实验室制备水合茚三.md", (32, 60)),
]

for inst, name, (qi, hi) in CARDS:
    p = os.path.join(BASE, inst, name)
    ls = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")
    ai = next((k for k, l in enumerate(ls) if l.startswith("## 参考答案")), len(ls))
    print("=" * 88)
    print("▸ %s / %s   [题面起 %d / 答案起 %d]" % (inst, name[:50], qi, ai))
    for k in range(qi - 1, min(hi, len(ls))):
        mark = "Q" if k < ai else "A"
        print("  %s%4d| %s" % (mark, k + 1, ls[k][:150]))
