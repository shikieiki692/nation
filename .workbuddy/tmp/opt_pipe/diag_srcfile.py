#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diag_srcfile.py —— 列出 94 张「源确缺答案」卡的 source_file 与源文件可定位性。"""
import csv, glob, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
OCR = os.path.join(R, "06-外部资料导入/OCR/01-题目")
print("共 %d 张\n" % len(rows))
nomd, ok = 0, 0
bystem = collections.Counter()
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    m = re.search(r'^source_file:\s*["\']?(.*?)["\']?\s*$', t, re.M)
    sf = m.group(1) if m else ""
    # source_file 形如 2026机构初赛模拟题/chemY/xxx.md
    base = os.path.basename(sf)
    stem = re.sub(r"\.md$", "", base)
    hits = glob.glob(OCR + "/**/" + stem + "*.pdf", recursive=True) if stem else []
    ok += 1 if hits else 0
    if not hits:
        nomd += 1
    bystem[r["inst"]] += 1
    if len(bystem) <= 20:
        pass
print("源 PDF 可定位：%d / %d（未定位 %d）\n" % (ok, len(rows), nomd))
print("按机构：", dict(bystem.most_common()))
print("\n样例（前 14 张）：")
for r in rows[:14]:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    m = re.search(r'^source_file:\s*["\']?(.*?)["\']?\s*$', t, re.M)
    sf = m.group(1) if m else "?"
    stem = re.sub(r"\.md$", "", os.path.basename(sf))
    hits = glob.glob(OCR + "/**/" + stem + "*.pdf", recursive=True)
    print("   %-8s %-38s %s" % (r["inst"], os.path.basename(p)[:38], (hits[0].replace(OCR + os.sep, "") if hits else "❌无PDF")))
