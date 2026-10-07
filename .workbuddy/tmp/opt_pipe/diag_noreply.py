#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diag_noreply.py —— 诊断「无答案/占位」94 张：命中位置（题面/答案）、答案形态、是否源确缺。"""
import csv, glob, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
sys.argv = ["x", "--vol", "D2", "--all-years"]
import build_org as BO
X = BO.X

rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
print("「无答案/占位」%d 张\n" % len(rows))
stat = collections.Counter()
detail = []
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    try:
        c = X.extract(p)
    except Exception:
        stat["提取异常"] += 1; continue
    rawa, rawq = c["answer"], c["question"]
    mq = BO.PLACEHOLDER.search(rawq)
    ma = BO.PLACEHOLDER.search(rawa)
    nimg = len(re.findall(r"!\[", rawa))
    body = "\n".join(l for l in rawa.split("\n") if l.strip() and not BO.NOTE_LINE.search(l.strip()))
    blen = len(re.sub(r"\s+", "", body))
    # 判定子类
    if mq:
        sub = "题面命中"
    elif nimg:
        sub = "答案有图"
    elif "源确缺答案" in rawa:
        sub = "源确缺答案"
    elif blen < 25:
        sub = "剔注记后<25字"
    else:
        sub = "其他"
    stat[sub] += 1
    detail.append((sub, r["inst"], os.path.basename(p)[:40], len(rawa), nimg, blen,
                   (mq.group(0) if mq else ""), (ma.group(0) if ma else "")))

for sub, n in stat.most_common():
    print("  %-14s %d" % (sub, n))
print()
for sub in ["题面命中", "答案有图", "其他", "剔注记后<25字"]:
    grp = [d for d in detail if d[0] == sub]
    if not grp:
        continue
    print("── %s（%d）──" % (sub, len(grp)))
    for s, inst, nm, alen, ni, blen, hq, ha in grp[:12]:
        print("   %-8s %-42s 答%5d字 图%d 剔后%4d 题面命中[%s] 答案命中[%s]" % (
            inst, nm, alen, ni, blen, hq, ha))
    print()
