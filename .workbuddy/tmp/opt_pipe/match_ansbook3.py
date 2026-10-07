#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""match_ansbook3.py —— 全 OCR 树按「源名尾部 + 答案关键词」匹配答案册。"""
import csv, glob, os, re, sys, json, collections
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
OCR = os.path.join(R, "06-外部资料导入/OCR")
ANSKW = ("答案", "解析", "参考", "评分标准", "version")
ALLPDF = glob.glob(OCR + "/**/*.pdf", recursive=True)
print("OCR 树 pdf 总数 %d" % len(ALLPDF))

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
found, none = [], []
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    m = re.search(r'^source_file:\s*["\']?(.*?)["\']?\s*$', t, re.M)
    sf = m.group(1) if m else ""
    stem = re.sub(r"\.md$", "", os.path.basename(sf))
    key = stem[-9:] if len(stem) >= 9 else stem          # 尾部特征串
    cands = []
    for f in ALLPDF:
        b = os.path.basename(f)
        if any(w in b for w in ANSKW) and key in b:
            cands.append(f)
    if cands:
        found.append((r["inst"], r["path"], r["qno"], os.path.basename(p)[:34], stem[:30],
                      [c.replace(R + os.sep, "") for c in cands[:2]]))
    else:
        none.append((r["inst"], os.path.basename(p)[:36], stem[:30]))

print("\n★ 找到答案册：%d 张" % len(found))
for inst, path, qno, nm, stem, cs in found:
    print("   %-8s %-34s 第%-3s题 ← %s" % (inst, nm, qno, " | ".join(c[:52] for c in cs)))
print("\n未找到：%d 张（按机构 %s）" % (len(none), dict(collections.Counter(n[0] for n in none).most_common())))
json.dump([[f[1], f[2], f[5]] for f in found],
          open(os.path.join(R, ".workbuddy/tmp/opt_pipe/ansbook_hits.json"), "w"), ensure_ascii=False)
