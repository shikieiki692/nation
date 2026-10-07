#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_table_fix.py —— 验证 html_table_to_md 修正效果。"""
import glob, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe")
sys.argv = ["x", "--vol", "T", "--all-years"]
import build_org as BO

TB = re.compile(r"<table>.*?</table>", re.S)
for pat, tag in [("**/题-HZ-12-06-*.md", "HZ-12-06 题面"),
                 ("**/题-CM-12-07-*.md", "CM-12-07 题面")]:
    fs = glob.glob("04-题库/2026机构初赛模拟题/" + pat, recursive=True)
    if not fs:
        continue
    c = BO.X.extract(fs[0])
    rawq = c["question"]
    for tb in TB.findall(rawq):
        print("=" * 90)
        print("[%s] 表 %d 字" % (tag, len(tb)))
        # ★ 与 build_org 同序：先 conv_imgs（把 <img> 变 ![](...)）再转表
        print(BO.html_table_to_md(BO.conv_imgs(tb))[:900])
        print()
