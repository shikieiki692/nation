#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""txt_struct.py —— 看 gamma晶体结构习题.pdf 的文字层结构（题号 / 小问号 / 评分标注分布）。"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
import fitz
try:
    fitz.TOOLS.mupdf_display_errors(False)
except Exception:
    pass
P = r"C:\Obsidion\妙妙屋\06-外部资料导入\OCR\01-题目\2026伽马寒假线上班\无机\2026年1.18无机\gamma晶体结构习题.pdf"
d = fitz.open(P)
print("页数 %d" % d.page_count)
for i in range(d.page_count):
    t = d[i].get_text()
    tn = t.replace(" ", "")
    qn = [m.group(0) for m in re.finditer(r"第\d+题", tn)]
    sub = [m.group(0) for m in re.finditer(r"\d+-\d+(?:-\d+)?", tn)]
    score = len(re.findall(r"\d+(?:\.\d+)?分", tn))
    print("  p%-3d 题头%s 小问号%d个%s 评分标注%d处 字数%d" % (
        i + 1, qn, len(sub), sub[:8], score, len(t.strip())))
d.close()
