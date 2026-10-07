#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_echo_ratio.py —— 统计「答案≈题面回显」的卡（ratio 高、非回显实质少）。"""
import csv, glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
sys.argv = ["x", "--vol", "ER", "--all-years"]
import build_org as BO
verd = {}
for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig")):
    verd[os.path.basename(r["path"])] = (r["verdict"], r["reason"], r["klass"])
buckets = {"ratio>=0.80": [], "0.70-0.80": [], "0.60-0.70": []}
for p in glob.glob(os.path.join(R, "04-题库/2026机构初赛模拟题/**/题-*.md"), recursive=True):
    try:
        c = BO.X.extract(p)
    except Exception:
        continue
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c["question"])))
    a = BO.html_table_to_md(BO.clean_a(BO.conv_imgs(c["answer"]), BO.conv_imgs(BO.clean_q(c["question"]))))
    an = len(re.sub(r"\s+", "", a))
    if an < 120:
        continue
    r = BO.contain_ratio(re.sub(r"\s+", "", a), re.sub(r"\s+", "", q))
    non = an * (1 - r)
    if r >= 0.60:
        key = "ratio>=0.80" if r >= 0.80 else ("0.70-0.80" if r >= 0.70 else "0.60-0.70")
        buckets[key].append((r, an, non, os.path.basename(p), verd.get(os.path.basename(p), ("?", "", "?"))))
for k in ("ratio>=0.80", "0.70-0.80", "0.60-0.70"):
    v = sorted(buckets[k], key=lambda x: x[2])      # 非回显实质升序
    inn = [x for x in v if x[4][0] == "入池"]
    print("=" * 100)
    print("【%s】%d 张（其中**入池** %d 张）" % (k, len(v), len(inn)))
    for r, an, non, bn, (vd, rs, kl) in v[:12]:
        print("   ratio=%.2f 答案%5d 字 非回显≈%4d 字 | %-4s %-8s | %s" % (r, an, non, vd, rs or "—", bn[:44]))
