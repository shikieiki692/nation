# -*- coding: utf-8 -*-
"""复核 6 卡池状态（修复后）与池规模。"""
import os, sys, importlib.util as u
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"; os.chdir(R)
sys.path.insert(0, os.path.join(R, ".workbuddy", "tmp", "opt_pipe"))
sp = u.spec_from_file_location("B", os.path.join(R, ".workbuddy", "tmp", "opt_pipe", "build_org.py"))
B = u.module_from_spec(sp); sp.loader.exec_module(B)
B.ALL_YEARS = True
pool = B.build_pool()
print("池规模：%d（元素 %d / 结构 %d / 原理 %d）" % (
    sum(len(v) for v in pool.values()),
    len(pool.get("元素与分析", [])), len(pool.get("结构化学", [])), len(pool.get("化学原理", []))))
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
CARDS = [
    ("清北营", "题-QBY-02-04-下图为实验室制备12二溴乙烷.md"),
    ("清北营", "题-QBY-03-09-Ineleganolide最.md"),
    ("chemy",  "题-CM-63-03-二氧化钛除金红石外还有多种晶.md"),
    ("chemy",  "题-CM-103-05-生物正交反应是在活细胞内进行.md"),
    ("chemy",  "题-CM-138-09-观察下图所示合成路线并回答后.md"),
    ("化英社", "题-HYS-03-04-甲烷单加氧酶MMO可在常温常.md"),
]
print("\n6 卡池状态：")
for inst, name in CARDS:
    why = B.why_not_in_pool(os.path.join(BASE, inst, name))
    print("  %-46s %s" % (name[:44], "★在池" if why is None else "掉池：" + str(why)))
