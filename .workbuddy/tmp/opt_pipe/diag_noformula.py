#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diag_noformula.py —— 诊断「答案公式未转录」卡：答案是否含图、源 md 是否有公式。"""
import csv, glob, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
sys.argv = ["x", "--vol", "D", "--all-years"]
import build_org as BO
X = BO.X

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "答案公式未转录"]
print("「答案公式未转录」%d 张\n" % len(rows))
stat = collections.Counter()
for r in rows[:60]:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    m = re.search(r"^source_file:\s*[\"']?(.*?)[\"']?\s*$", t, re.M)
    sf = m.group(1) if m else ""
    try:
        c = X.extract(p)
    except Exception as e:
        print("  提取异常", r["path"][-40:]); continue
    rawa, rawq = c["answer"], c["question"]
    nimg = len(re.findall(r"!\[", rawa))
    # 答案是否为「题面复读」：与题面 8-gram 覆盖率
    an = re.sub(r"\s+", "", re.sub(r"!\[[^\]]*\)?", "", rawa))
    qn = re.sub(r"\s+", "", re.sub(r"!\[[^\]]*\)?", "", rawq))
    gs = [qn[k:k + 8] for k in range(0, max(1, len(qn) - 8), 5)]
    cov = sum(1 for g in gs if g in an) / max(1, len(gs))
    kind = "含图" if nimg else "无图"
    if cov >= 0.6:
        kind += "+题面复读"
    stat[kind] += 1
    print("  %-34s 答案%5d字 $%2d 图%d 覆盖%.2f %s" % (
        os.path.basename(p)[:34], len(rawa), rawa.count("$"), nimg, cov, kind))
print("\n分类：", dict(stat))
