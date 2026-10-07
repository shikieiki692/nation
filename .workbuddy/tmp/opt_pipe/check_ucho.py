#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_ucho.py —— 核验 UChO 7 张「源确缺答案」卡与答案合集的对应关系。"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
import fitz
try:
    fitz.TOOLS.mupdf_display_errors(False)
except Exception:
    pass
R = r"C:\Obsidion\妙妙屋"
AB = os.path.join(R, "06-外部资料导入/OCR/01-题目/质心合集新/UChO模拟试题合集答案")
print("答案合集目录：")
for f in sorted(os.listdir(AB)):
    print("   ", f)
print()
for n in ["1st ZCHEM-UChO 答案.pdf", "2nd ZCHEM-UChO 答案.pdf"]:
    p = os.path.join(AB, n)
    if not os.path.exists(p):
        print("缺", n); continue
    d = fitz.open(p)
    tl = sum(len(d[i].get_text().strip()) for i in range(d.page_count))
    print("### %s 页%d 文字层%d" % (n, d.page_count, tl))
    for i in range(d.page_count):
        t = d[i].get_text()
        hits = [m.group(0).replace(" ", "") for m in re.finditer(r"第\s*\d+\s*题", t)]
        if hits:
            print("    p%-3d %s" % (i + 1, hits[:6]))
    d.close()
print()
print("=== 7 张卡的 source_file ===")
for f in sorted(glob.glob(R + "/04-题库/2026机构初赛模拟题/质心UChO/题-UChO-15-*.md")):
    t = open(f, encoding="utf-8-sig", errors="replace").read()
    sf = (re.search(r'^source_file:\s*["\']?(.*?)["\']?\s*$', t, re.M) or [None, ""])[1]
    src = (re.search(r'^source:\s*["\']?(.*?)["\']?\s*$', t, re.M) or [None, ""])[1]
    print("   %-44s | %s | %s" % (os.path.basename(f)[:44], sf[:34], src[:40]))
