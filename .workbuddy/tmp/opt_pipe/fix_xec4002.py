#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_xec4002.py —— 题-XeC-40-02：口语化题名规范化（教研语气要求）。"""
import os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
p = os.path.join(R, "04-题库/2026机构初赛模拟题/XeChem/题-XeC-40-02-请注意本题的21和22两部分.md")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/title_backup")
os.makedirs(BK, exist_ok=True)
t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
OLD = "### 第 2 题 希望我的硅簇晶体物语果然没问题！（35 分，占 16%）"
NEW = "### 第 2 题 硅簇晶体的合成与结构（35 分，占 16%）"
if OLD not in t:
    print("未命中标题，放弃"); sys.exit(0)
newt = t.replace(OLD, NEW)
bfp = os.path.join(BK, os.path.basename(p) + ".orig")
if not os.path.exists(bfp):
    open(bfp, "w", encoding="utf-8", newline="\n").write(t)
open(p, "w", encoding="utf-8", newline="\n").write(newt)
print("✔ 题名规范化：", OLD.split("题 ", 1)[1], "→", NEW.split("题 ", 1)[1])
