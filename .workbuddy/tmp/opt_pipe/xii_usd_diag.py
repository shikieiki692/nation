# -*- coding: utf-8 -*-
"""定位卷 XII 答案版中「字面 $」的来源行（只读）。"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
MD = R + r"\04-题库\初赛模拟卷XII（非有机·答案版）.md"
t = io.open(MD, encoding="utf-8-sig").read().replace("\r\n", "\n")

# ① `$$` 块内出现单个 `$`（坏结构）
n = 0
for m in re.finditer(r"\$\$(.*?)\$\$", t, re.S):
    if "$" in m.group(1):
        n += 1
        seg = m.group(0).replace("\n", "⏎")
        print("[块内 $] …%s…" % seg[:160])
print("块内含 $ 的块数:", n)

# ② 全文中 `$` 计数为奇数的行
print("\n[奇数 $ 行]")
for i, l in enumerate(t.split("\n"), 1):
    if l.count("$") % 2 == 1:
        print("  L%-5d %s" % (i, l[:130]))
