#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_gcho_allow.py —— 把本轮 426 张 GChO 裁图卡登记进 render_gate allowlist。"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
AL = os.path.join(R, "11-模板/scripts/render_gate_allowlist.txt")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/gcho_ans_backup")
REL = "04-题库/2026机构初赛模拟题/质心GChO/"

names = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(BK, "*.orig")))
reason = ("2026-10-07 GChO 手写解析稿答案治理：答案区由手写稿 OCR 文本（乱码）改为**忠实裁图**，"
          "文字删除导致 oMath 下降，属**预期删节**非渲染退化；`verify_gcho_crop.py` 已断言"
          "题面/FM 逐字节不变、图全在、断图 0。")
t = open(AL, encoding="utf-8-sig").read().replace("\r\n", "\n")
if not t.endswith("\n"):
    t += "\n"
have = {ln.split("\t")[0] for ln in t.split("\n") if ln.strip()}
add = 0
for n in names:
    p = REL + n
    if p in have:
        continue
    t += "%s\t%s\n" % (p, reason)
    add += 1
open(AL, "w", encoding="utf-8", newline="\n").write(t)
print("allowlist 原有 %d 条；新增 %d 条；现共 %d 行" % (len(have), add, t.count("\n")))
