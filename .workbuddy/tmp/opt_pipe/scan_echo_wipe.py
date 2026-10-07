#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_echo_wipe.py —— 全量扫描：strip_q_echo 是否把答案区吞掉。"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
sys.argv = ["x", "--vol", "EW", "--all-years"]
import build_org as BO
rows = []
n = 0
for p in glob.glob(os.path.join(R, "04-题库/2026机构初赛模拟题/**/题-*.md"), recursive=True):
    n += 1
    try:
        c = BO.X.extract(p)
    except Exception:
        continue
    q = BO.conv_imgs(BO.clean_q(c["question"]))
    a = BO.conv_imgs(c["answer"])
    rawa_len = len(re.sub(r"\s+", "", a))
    if rawa_len < 300:
        continue
    a1 = BO.strip_q_echo(q, a)
    kept = len(re.sub(r"\s+", "", a1))
    if kept <= 0.05 * rawa_len:          # 被吞掉 ≥95%
        rows.append((p, rawa_len, kept, a.count("!["), a1.count("![")))
print("扫描 %d 张卡；「答案被吞」 %d 张\n" % (n, len(rows)))
for p, r0, k, i0, i1 in sorted(rows, key=lambda x: -x[1])[:40]:
    print("  原 %5d 字/%2d 图 → 剩 %4d 字/%2d 图 | %s" % (r0, i0, k, i1, p.replace(R + os.sep, "")[:80]))
