# -*- coding: utf-8 -*-
"""S1 终判核对：dump 每张卡题面区所有含「图」或「画」的行（判断是「引用已有图」还是「作答要求」）。"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
import importlib.util as _u
spec = _u.spec_from_file_location("t", os.path.join(R, ".workbuddy/tmp/opt_pipe/s1_triage.py"))
_m = _u.module_from_spec(spec)
spec.loader.exec_module(_m)

for inst, name in _m.TODO:
    p = os.path.join(BASE, inst, name)
    if not os.path.exists(p):
        continue
    t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
    i, j = t.find("## 题目"), t.find("## 参考答案")
    q = t[i + 5:j] if j > i > 0 else t[i + 5:]
    hits = []
    for ln in q.split("\n"):
        s = ln.strip()
        if ("图" in s or "画" in s) and len(s) > 4:
            hits.append(s)
    print("=" * 74)
    print("▸ [%s] %s" % (inst, name[:34]))
    for s in hits[:6]:
        print("   %s" % s[:104])
