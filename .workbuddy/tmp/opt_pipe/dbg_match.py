#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dbg_match.py —— 最小复现：打印 stem 与目录文件的 repr。"""
import csv, glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
OCR = os.path.join(R, "06-外部资料导入/OCR")
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
r = [x for x in rows if "GM-08-01" in x["path"]][0]
p = os.path.join(R, r["path"])
t = open(p, encoding="utf-8-sig", errors="replace").read()
m = re.search(r'^source_file:\s*["\']?(.*?)["\']?\s*$', t, re.M)
sf = m.group(1) if m else ""
print("source_file raw =", repr(sf))
stem = re.sub(r"\.md$", "", os.path.basename(sf))
print("stem            =", repr(stem))
pat = OCR + "/**/" + stem + "*.pdf"
print("pattern         =", repr(pat))
srcs = glob.glob(pat, recursive=True)
print("srcs            =", srcs)
if srcs:
    d = os.path.dirname(srcs[0])
    print("dir             =", repr(d))
    print("listdir         =", repr(os.listdir(d)[:5]))
    for b in os.listdir(d):
        if "模拟8答案" in b:
            print("  命中候选:", repr(b), "| startswith(stem)=", b.startswith(stem),
                  "| tail=", repr(b[len(stem):]))
