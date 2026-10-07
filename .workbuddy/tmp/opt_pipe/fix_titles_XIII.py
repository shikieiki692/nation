# -*- coding: utf-8 -*-
"""fix_titles_XIII.py —— 卷 XIII 答案版题名人工修正（幂等）。
题名由 build_org.desc_of 从卡内抽取，个别卡因题面以公式/编号开头而抽成残段，此处人工给定。
仅改答案版 md 的「### 第 N 题（分）<题名>」行与卷末选题清单「题名」列。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
MD = os.path.join(R, "04-题库", "初赛模拟卷XIII（非有机·答案版）.md")

FIX = {
    4: ("已知51计算1L100mol", "氨水溶解氯化银"),
    8: ("3-1 向 20 mL 浓度", "醋酸缓冲液溶解硫酸铅"),
}

txt = open(MD, encoding="utf-8-sig").read()
n = 0
for q, (old, new) in FIX.items():
    heads = ("### 第 %d 题（13 分）%s" % (q, old), "### 第 %d 题（13 分）%s" % (q, new))
    if heads[0] in txt:
        txt = txt.replace(heads[0], heads[1])
        n += 1
    cell = ("| %d | %s |" % (q, old), "| %d | %s |" % (q, new))
    if cell[0] in txt:
        txt = txt.replace(cell[0], cell[1])
        n += 1
open(MD, "w", encoding="utf-8", newline="\n").write(txt)
print("题名修正 %d 处" % n)
