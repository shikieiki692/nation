# -*- coding: utf-8 -*-
"""验证吞图修复后题面区。"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\Obsidion\妙妙屋\04-题库\2026机构初赛模拟题"
IMG = re.compile(r"!\[\[|!\[\]\(|<img\b")
CARDS = [
    ("清北营", "题-QBY-02-04-下图为实验室制备12二溴乙烷.md"),
    ("清北营", "题-QBY-03-09-Ineleganolide最.md"),
    ("chemy",  "题-CM-63-03-二氧化钛除金红石外还有多种晶.md"),
    ("chemy",  "题-CM-103-05-生物正交反应是在活细胞内进行.md"),
    ("chemy",  "题-CM-138-09-观察下图所示合成路线并回答后.md"),
    ("化英社", "题-HYS-03-04-甲烷单加氧酶MMO可在常温常.md"),
]
for inst, name in CARDS:
    p = os.path.join(BASE, inst, name)
    ls = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")
    qi = next(k for k, l in enumerate(ls) if l.startswith("## 题目"))
    ai = next(k for k, l in enumerate(ls) if l.startswith("## 参考答案"))
    print("=" * 80)
    print("▸ %s / %s" % (inst, name[:50]))
    for k in range(qi, ai):
        if IMG.search(ls[k]) or "\\begin{array}" in ls[k]:
            # 显示该图行的前一行做上下文
            print("   L%-4d [前] %s" % (k, ls[k - 1].strip()[:78]))
            print("        [行] %s" % ls[k].strip()[:100])
    print("   → 题面图数 = %d" % len(IMG.findall("\n".join(ls[qi:ai]))))
