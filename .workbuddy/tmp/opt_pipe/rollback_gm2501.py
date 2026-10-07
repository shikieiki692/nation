#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rollback_gm2501.py —— 回滚 题-GM-25-01（源文件确实未给第1题答案）。"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/gm25_backup")
CARD = os.path.join(R, "04-题库/2026机构初赛模拟题/伽马/题-GM-25-01-题源化英社3809金红石是缺.md")
orig = None
for f in os.listdir(BK):
    if f.startswith("题-GM-25-01"):
        orig = open(os.path.join(BK, f), encoding="utf-8").read()
print("备份文件：", f if orig else "无")
if orig and "--apply" in sys.argv:
    open(CARD, "w", encoding="utf-8", newline="\n").write(orig)
    print("✔ 已回滚")
t = open(CARD, encoding="utf-8-sig").read().replace("\r\n", "\n")
j = t.find("## 参考答案"); k = t.find("## 知识点映射")
print("当前答案区：", t[j:k].strip()[:180])
