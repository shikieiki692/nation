#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patch_ph.py —— 修 PLACEHOLDER 闸：答案区**带图**时不算「占位声明」。
原因：手稿裁图卡的规范注记含 `答案出处/已随卡/文字化需人工转录` ⇒ 被占位闸误杀
（实测 426 裁图卡 + 112 既有「诚实图」卡全部进不了池）。
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
P = r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe\build_org.py"
s = open(P, encoding="utf-8").read()
old = "            if PLACEHOLDER.search(rawa) or PLACEHOLDER.search(rawq):\n                continue"
new = ("            # ★ 占位闸：答案区**带图**者不算占位（图片即答案；注记只是出处说明）\n"
       "            if (PLACEHOLDER.search(rawa) and '![' not in rawa) or PLACEHOLDER.search(rawq):\n"
       "                continue")
assert old in s, "anchor 未命中"
if "答案区**带图**者不算占位" not in s:
    s = s.replace(old, new, 1)
open(P, "w", encoding="utf-8", newline="\n").write(s)
print("patched")
