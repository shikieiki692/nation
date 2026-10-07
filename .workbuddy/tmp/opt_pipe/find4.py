#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""find4.py —— 定位含「答案/解析」关键词的 4 个源文件全路径。"""
import glob, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
OCR = os.path.join(R, "06-外部资料导入/OCR")
hits = json.load(open(os.path.join(R, ".workbuddy/tmp/opt_pipe/content_hits.json"), encoding="utf-8"))
names = {}
for path, qno, f, cov in hits:
    names.setdefault(f, []).append((path, qno, cov))
TARGETS = ["gamma晶体结构习题.pdf", "无机化学一_课后习题11.9.pdf",
           "260609-汇智起航2026年（暑假）全国化学初赛模拟试题5试题.pdf",
           "39届初赛模拟试题分享-2 10th XChem-ArCHO..pdf"]
for t in TARGETS:
    fs = glob.glob(OCR + "/**/" + t, recursive=True)
    print("%-58s → %s" % (t[:58], (fs[0].replace(R + os.sep, "") if fs else "❌未找到")))
    for p, q, c in names.get(t, [])[:6]:
        print("      第%-3s题 覆盖%.2f  %s" % (q, c, os.path.basename(p)[:44]))
