#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""spot_check_reject.py —— 抽验「不可组卷」判据的真伪（防误杀）。"""
import csv, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
rows = [r for r in csv.DictReader(open(R + "/09-审计报告/2026-10-07-不可组卷题目清单.csv", encoding="utf-8-sig"))
        if r["klass"] == "A"]
picks = {}
for r in rows:
    picks.setdefault(r["reason"], [])
    if len(picks[r["reason"]]) < 2:
        picks[r["reason"]].append(r)

for reason, rs in picks.items():
    for r in rs:
        p = R + "/" + r["path"]
        t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
        j = t.find("## 参考答案"); k = t.find("## 知识点映射")
        i = t.find("## 题目")
        a = t[j:k] if j > 0 and k > j else ""
        q = t[i:j] if i > 0 and j > i else ""
        print("═" * 96)
        print("【%s】%s" % (reason, r["path"].split("/")[-1][:60]))
        print("--- 题面首 200 ---")
        print(re.sub(r"\s+", " ", q)[:200])
        print("--- 答案首 260 ---")
        print(re.sub(r"\s+", " ", a)[:260])
        print()
