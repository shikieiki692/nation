#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_hys0106.py —— 题-HYS-01-06：题面尾部串入「第7題（18分，占9%）」及其内容，按题界截断。"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
p = os.path.join(R, "04-题库/2026机构初赛模拟题/化英社/题-HYS-01-06-卤原子转移反应是实现氧化态转.md")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/leak2_backup")
os.makedirs(BK, exist_ok=True)
t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
i = t.find("## 题目"); j = t.find("## 参考答案")
q = t[i:j]
m = re.search(r'第\s*7\s*題\s*[（(]', q)
if not m:
    print("未找到题头，放弃"); sys.exit(0)
keep = q[:m.start()].rstrip()
drop = q[m.start():].strip()
note = "\n\n> 📄 校勘（2026-10-07）：题面区尾部串入了**后一题**（第 7 題）的题头及其内容（%d 字），已按题界截断。\n" % len(drop)
newt = t[:i] + keep + note + t[j:]
bfp = os.path.join(BK, os.path.basename(p) + ".orig")
if not os.path.exists(bfp):
    open(bfp, "w", encoding="utf-8", newline="\n").write(t)
open(p, "w", encoding="utf-8", newline="\n").write(newt)
print("✔ HYS-01-06 题面 %d → %d（删 %d）" % (len(q), len(keep), len(drop)))
print("  保留段尾 160:", re.sub(r"\s+", " ", keep[-160:]))
