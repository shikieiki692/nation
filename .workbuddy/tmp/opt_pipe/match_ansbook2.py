#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""match_ansbook2.py —— 用「源 PDF 名前缀 + 答案后缀」在同目录精确找答案册。"""
import csv, glob, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
OCR = os.path.join(R, "06-外部资料导入/OCR")
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
ANSKW = ("答案", "解析", "参考", "评分标准", "version")

found, unmatched = [], []
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    m = re.search(r'^source_file:\s*["\']?(.*?)["\']?\s*$', t, re.M)
    sf = m.group(1) if m else ""
    stem = re.sub(r"\.md$", "", os.path.basename(sf))
    srcs = glob.glob(OCR + "/**/" + stem + "*.pdf", recursive=True)
    if not srcs:
        unmatched.append((r["inst"], os.path.basename(p)[:38], "源PDF未定位", "")); continue
    src = srcs[0]
    d = os.path.dirname(src)
    cand = []
    try:
        names = os.listdir(d)
    except Exception:
        names = []
    for b in names:
        if not b.lower().endswith(".pdf"):
            continue
        if b == os.path.basename(src):
            continue
        if b.startswith(stem) and any(w in b[len(stem):] for w in ANSKW):
            cand.append(b)
        elif any(w in b for w in ANSKW) and stem[-6:] in b:
            cand.append(b)
    if cand:
        found.append((r["inst"], r["path"], r["qno"], os.path.basename(p)[:36], stem[:34], cand[0][:46]))
    else:
        unmatched.append((r["inst"], os.path.basename(p)[:38], stem[:30], os.path.basename(d)[:24]))

print("找到同源答案册：%d 张" % len(found))
for inst, path, qno, nm, stem, ab in found:
    print("   %-8s %-36s 第%-3s题 → %s" % (inst, nm, qno, ab))
print("\n未找到：%d 张（前 18）" % len(unmatched))
for inst, nm, stem, dirn in unmatched[:18]:
    print("   %-8s %-38s 源[%s] 目录[%s]" % (inst, nm, stem, dirn))
import json
json.dump([[f[1], f[2], f[4]] for f in found], open(os.path.join(R, ".workbuddy/tmp/opt_pipe/ansbook_hits.json"), "w"), ensure_ascii=False)
