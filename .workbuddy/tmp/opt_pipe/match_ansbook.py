#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""match_ansbook.py —— 用「卷号」精确匹配答案册（如 模拟8 ↔ 模拟8答案、试卷9 ↔ 试卷9-参考答案）。"""
import csv, glob, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
OCR = os.path.join(R, "06-外部资料导入/OCR")
rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]

VOLPAT = [
    (r"模拟\s*卷?\s*(\d+)", "模拟%s"),
    (r"试卷\s*(\d+)", "试卷%s"),
    (r"练习\s*([一二三四五六七八九十]+)", "练习%s"),
    (r"模拟\s*(\d+)", "模拟%s"),
]

found = collections.defaultdict(list)
unmatched = []
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    g = lambda k: (re.search(r"^" + k + r":\s*[\"']?(.*?)[\"']?\s*$", t, re.M) or [None, ""])[1]
    keys = " ".join([g("source"), g("source_norm")])
    key = None
    for pat, fmt in VOLPAT:
        m = re.search(pat, keys)
        if m:
            key = fmt % m.group(1); break
    # 源 PDF 所在目录
    sf = g("source_file")
    stem = re.sub(r"\.md$", "", os.path.basename(sf))
    srcs = glob.glob(OCR + "/**/" + stem + "*.pdf", recursive=True)
    d = os.path.dirname(srcs[0]) if srcs else None
    cand = []
    if d and key:
        for f in glob.glob(os.path.join(d, "*.pdf")):
            b = os.path.basename(f)
            if ("答案" in b or "解析" in b or "参考" in b) and key in b.replace(" ", ""):
                cand.append(b)
    if cand:
        found[key].append((r["inst"], os.path.basename(p)[:36], cand[0][:40]))
    else:
        unmatched.append((r["inst"], os.path.basename(p)[:38], key or "无卷号", os.path.basename(d) if d else "无目录"))

print("精确匹配到答案册：%d 张" % sum(len(v) for v in found.values()))
for k, v in found.items():
    print("\n  【%s】%d 张" % (k, len(v)))
    for inst, nm, ab in v[:12]:
        print("     %-8s %-36s → %s" % (inst, nm, ab))
print("\n未匹配：%d 张（前 14）" % len(unmatched))
for inst, nm, key, dirn in unmatched[:14]:
    print("   %-8s %-38s 卷号[%s] 目录[%s]" % (inst, nm, key, dirn[:26]))
