# -*- coding: utf-8 -*-
"""吞图 10 张 — 关键行原始 repr（只读）。"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\Obsidion\妙妙屋\04-题库\2026机构初赛模拟题"

JOBS = [
    ("chemy",    "题-CM-12-07-71近年人们发现高压下可以制.md",  [36]),
    ("chemy",    "题-CM-17-02-锂离子电池技术的进步极大地推.md", [41, 43]),
    ("清北营",   "题-QBY-03-09-Ineleganolide最.md",           [38]),
    ("chemy",    "题-CM-95-08-利用大量可得的天然不对称化合.md", [38, 40, 41, 42, 43]),
    ("chemy",    "题-CM-138-09-观察下图所示合成路线并回答后.md", [38, 40]),
    ("质心UChO", "题-UChO-02-06-下图为一种实验室制备水合茚三.md", [37, 39, 41, 42, 43]),
    ("化英社",   "题-HYS-03-04-甲烷单加氧酶MMO可在常温常.md",  [37, 39]),
]

for inst, name, lines in JOBS:
    p = os.path.join(BASE, inst, name)
    ls = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")
    print("=" * 90)
    print("▸ %s / %s" % (inst, name[:56]))
    for ln in lines:
        print("  L%d:" % ln)
        print("    %r" % ls[ln - 1])
