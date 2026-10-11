# -*- coding: utf-8 -*-
"""S1 真缺陷卡的**当前池状态**核查（用 build_org.why_not_in_pool，返回 None=在池）。"""
import importlib.util as _u
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
os.chdir(R)
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
spec = _u.spec_from_file_location("B", os.path.join(R, ".workbuddy/tmp/opt_pipe/build_org.py"))
B = _u.module_from_spec(spec)
spec.loader.exec_module(B)

BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")
CARDS = {
    "真S1": [
        ("XeChem", "题-XeC-07-04-beginarraycmat.md"),
        ("chemy", "题-CM-123-07-利用手性助剂可实现双键不对称.md"),
        ("chemy", "题-CM-165-02-顾名思义超酸是一类酸度极强的.md"),
        ("chemy", "题-CM-17-07-超分子自组装的选择性.md"),
        ("chemy", "题-CM-65-06-6-1化学式为的化合物中含有.md"),
        ("化英社", "题-HYS-02-01-已知XYZ是同族元素其相对原.md"),
        ("化英社", "题-HYS-03-05-硫与铜元素可形成多种化合物它.md"),
    ],
    "题面图缺失·未标注": [
        ("chemy", "题-CM-106-01-1-1在C减压下丙二酸用脱水.md"),
        ("汇智", "题-HZ-02-05-奎宁分子结构如右图所示是从金.md"),
        ("质心GChO", "题-GChO-42-04-下图展示了某过渡元素X相关的.md"),
        ("化英社", "题-HYS-01-01-某金属元素M在自然界中分布广.md"),
    ],
    "假阳性(抽样)": [
        ("2ChO", "题-2ChO-01-04-在苯溶液中将105mmolT.md"),
        ("chemy", "题-CM-127-02-臭氧是一类人类生活生产以及研.md"),
        ("清北营", "题-QBY-08-06-对高分子反应规律的探寻具有重.md"),
    ],
}

print("跑 build_pool（ALL_YEARS=True，与建计划同口径）…")
B.ALL_YEARS = True
pool = B.build_pool()
print("池规模：%d\n" % sum(len(v) for v in pool.values()))

for cat, lst in CARDS.items():
    print("== %s ==" % cat)
    for inst, name in lst:
        p = os.path.join(BASE, inst, name)
        why = B.why_not_in_pool(p)
        print("   %-46s %s" % (name[:44], "★在池" if why is None else "掉池：" + why))
