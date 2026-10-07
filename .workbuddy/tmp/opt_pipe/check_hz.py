#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_hz.py —— 看汇智源目录内「讲评/解析」PDF 是否含无机化学初赛模拟1的答案。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding="utf-8")
import fitz
try:
    fitz.TOOLS.mupdf_display_errors(False)
except Exception:
    pass
R = r"C:\Obsidion\妙妙屋"
D = os.path.join(R, "06-外部资料导入/OCR/01-题目/2026年夏令营汇智长沙班/热力学等44项文件")
for f in sorted(os.listdir(D)):
    if not f.lower().endswith(".pdf"):
        continue
    p = os.path.join(D, f)
    try:
        d = fitz.open(p)
    except Exception as e:
        print("  !!", f, e); continue
    tl = sum(len(d[i].get_text().strip()) for i in range(d.page_count))
    head = re.sub(r"\s+", " ", d[0].get_text())[:110]
    print("### %-58s 页%-3d 字层%-6d | %s" % (f[:58], d.page_count, tl, head))
    if tl > 200:
        for i in range(min(d.page_count, 20)):
            t = d[i].get_text().replace(" ", "")
            hits = [m.group(0) for m in re.finditer(r"第\d+题", t)]
            if hits:
                print("      p%-3d %s" % (i + 1, hits[:6]))
    d.close()
