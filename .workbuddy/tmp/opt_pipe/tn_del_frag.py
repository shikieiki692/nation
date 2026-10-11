# -*- coding: utf-8 -*-
"""HYS-03-04 题面 OCR 碎片「NOH OH /」清理（与上批同类）。"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
p = r"C:\Obsidion\妙妙屋\04-题库\2026机构初赛模拟题\化英社\题-HYS-03-04-甲烷单加氧酶MMO可在常温常.md"
t0 = open(p, encoding="utf-8-sig", newline="").read()
assert "\r" not in t0, "CRLF"
ls = t0.split("\n")
il = [i for i, l in enumerate(ls) if l.strip() == "NOH OH /"]
assert len(il) == 1, "命中 %d" % len(il)
i = il[0]
del ls[i]
if 0 < i < len(ls) and ls[i] == "" and ls[i - 1] == "":
    del ls[i]
t1 = "\n".join(ls)
assert "NOH OH /" not in t1
assert "\r" not in t1
open(p, "w", encoding="utf-8", newline="").write(t1)
print("HYS-03-04 已删碎片行；残留计数 =", t1.count("NOH OH /"))
