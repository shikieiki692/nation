# -*- coding: utf-8 -*-
"""Step0：扫描各卷 md 的「卷级分区标题」（## 第…部分 / ## 序号 部分）实测分布。只读。"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Obsidion\妙妙屋"
QD = os.path.join(ROOT, "04-题库")

VOLS = ["X", "XI", "XIp", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "O1"]
# 卷级分区标题：H2 且含「部分」或形如 一、二、… / 1./2.
HEAD = re.compile(r"^##\s+(.*)$")
PART = re.compile(r"部分")

for v in VOLS:
    kind = "有机" if v == "O1" else "非有机"
    md = os.path.join(QD, f"初赛模拟卷{v}（{kind}·答案版）.md")
    if not os.path.exists(md):
        print(f"[MISS] {v}  {md}"); continue
    lines = open(md, "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
    parts, other_h2 = [], []
    for i, ln in enumerate(lines, 1):
        m = HEAD.match(ln)
        if not m:
            continue
        t = m.group(1).strip()
        if PART.search(t):
            parts.append((i, t))
        else:
            other_h2.append((i, t))
    print(f"===== {v} （H2 共 {len(parts)+len(other_h2)} 处）=====")
    for i, t in parts:
        print(f"  [部分] L{i}: {t}")
    if not parts:
        print("  （无「## …部分」标题）")
    print(f"  其余 H2（前 8）：" + " ｜ ".join(f"L{i}:{t[:26]}" for i, t in other_h2[:8]))
    print()
