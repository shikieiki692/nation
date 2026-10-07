#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""match_ansbook4.py —— 双策略匹配答案册：① 尾部特征串；② 卷号核心（模拟卷4/模拟8/练习一…）。"""
import csv, glob, os, re, sys, json, collections
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
OCR = os.path.join(R, "06-外部资料导入/OCR")
ANSKW = ("答案", "解析", "参考", "评分标准", "version")
ALLPDF = glob.glob(OCR + "/**/*.pdf", recursive=True)
VOLCORE = re.compile(r"(模拟\s*卷?\s*\d+|练习\s*[一二三四五六七八九十]+|试卷\s*\d+)")

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
found, none = [], []
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    m = re.search(r'^source_file:\s*["\']?(.*?)["\']?\s*$', t, re.M)
    sf = m.group(1) if m else ""
    stem = re.sub(r"\.md$", "", os.path.basename(sf))
    keys = {stem[-9:]} if len(stem) >= 9 else {stem}
    mv = VOLCORE.search(stem)
    core = mv.group(1).replace(" ", "") if mv else None
    if core:
        keys.add(core)
    cands = []
    for f in ALLPDF:
        b = os.path.basename(f).replace(" ", "")
        if not any(w in b for w in ANSKW):
            continue
        if any(k.replace(" ", "") in b for k in keys):
            cands.append(f)
    # 汇智需同机构（避免跨机构误配）
    if core and r["inst"] == "汇智":
        cands = [c for c in cands if "汇智" in os.path.basename(c)]
    if cands:
        found.append((r["inst"], r["path"], r["qno"], os.path.basename(p)[:32], stem[:26],
                      [c.replace(R + os.sep, "") for c in cands[:2]]))
    else:
        none.append((r["inst"], os.path.basename(p)[:34], stem[:26], core or "-"))

print("★ 找到答案册：%d 张" % len(found))
for inst, path, qno, nm, stem, cs in found:
    print("   %-8s %-32s ← %s" % (inst, nm, cs[0][-56:]))
print("\n未找到：%d 张 %s" % (len(none), dict(collections.Counter(n[0] for n in none).most_common())))
for inst, nm, stem, core in none[:14]:
    print("   %-8s %-34s 源[%s] 核心[%s]" % (inst, nm, stem, core))
json.dump([[f[1], f[2], f[5]] for f in found],
          open(os.path.join(R, ".workbuddy/tmp/opt_pipe/ansbook_hits.json"), "w"), ensure_ascii=False)
