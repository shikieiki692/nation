#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_cm6904.py —— 题-CM-69-04：题面尾 OCR 重复行 + 串入的「第5 题」题头。"""
import os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
p = os.path.join(R, "04-题库/2026机构初赛模拟题/chemy/题-CM-69-04-4-1将过渡金属氯化物与过渡.md")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/ovf2_backup")
os.makedirs(BK, exist_ok=True)
t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
i = t.find("## 题目"); j = t.find("## 参考答案")
q = t[i:j]
BAD = "X1？常温高压下，X2 是否有可能自发转化为X1？第5 题"
if BAD not in q:
    print("未命中目标行，放弃"); sys.exit(0)
newq = q.replace(BAD, "").rstrip() + "\n\n> ⛔ 校勘（2026-10-07）：题面区尾部原有一行 OCR 重复文本并串入下一题题头「第5 题」，已剔除。\n"
newt = t[:i] + newq + t[j:]
bfp = os.path.join(BK, os.path.basename(p) + ".orig")
if not os.path.exists(bfp):
    open(bfp, "w", encoding="utf-8", newline="\n").write(t)
open(p, "w", encoding="utf-8", newline="\n").write(newt)
print("✔ 已修 题-CM-69-04")
print("题面尾现在:", repr(newt[i:newt.find('## 参考答案')][-160:]))
