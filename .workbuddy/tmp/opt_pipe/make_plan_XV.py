# -*- coding: utf-8 -*-
"""make_plan_XV.py —— 卷 XV（晶体专题·10 题）计划锁生成。

10 题全属「结构化学」；8 题钙钛矿／钙钛矿衍生／反钙钛矿，2 题通用晶体。
用法: python -X utf8 make_plan_XV.py [--dry]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_org as BO   # noqa: E402
BO.ALL_YEARS = True

DRY = "--dry" in sys.argv

W = [
    "题-HZ-07-04-41著名的钙钛矿型晶体",     # 1 汇智   钙钛矿型晶体 ABCCC
    "题-CM-13-05-人们研究了一系列化学式",    # 2 chemy  MCrF3 钙钛矿
    "题-GChO-80-04-41二维材料呈现",          # 3 质心   MoS2 等晶体结构与性能
    "题-GChO-75-05-mathrmLaAlO3的晶",       # 4 质心   LaAlO3 晶体结构（钙钛矿）
    "题-HZ-01-04-刚玉corundum即是一种",      # 5 汇智   刚玉及其衍生结构
    "题-HZ-07-05-有机金属卤化物钙钛矿材料近几",  # 6 汇智   有机金属卤化物钙钛矿
    "题-YS-03-03-主族元素E的氧化物与碱金属M", # 7 一式   热致变色晶体（钙钛矿型）
    "题-YS-02-04-碳化物因碳的电负性",         # 8 一式   稀土碳化物（反钙钛矿）
    "题-HYS-20-04-ABCDE是五种元素",          # 9 化英社 镍盐结构演变（钙钛矿型）
    "题-HYS-20-05-半导体材料X是一种含ABC三", # 10 化英社 半导体黄铜矿型晶体结构
]

pool = BO.build_pool()
by_base = {}
for _m in pool:
    for c in pool[_m]:
        by_base.setdefault(os.path.basename(c["path"]), c)

got, ok = [], True
for k in W:
    hits = [b for b in by_base if b.startswith(k)]
    if len(hits) != 1:
        print("!! %s 命中 %d: %s" % (k, len(hits), hits[:4]))
        ok = False
        continue
    c = by_base[hits[0]]
    mods = [m for m in pool if c in pool[m]]
    if "结构化学" not in mods:
        print("!! %s 不在结构化学（实际 %s）" % (hits[0], mods))
        ok = False
    got.append(c)
    print("  %-50s d%s q%-5d 图%d calc%s" %
          (hits[0][:48], c["difficulty"], c["qlen"], len(c["imgs"]), c.get("calc", 0)))
if not ok or len(got) != len(W):
    print("** 解析失败，未写盘")
    sys.exit(1)

with open(os.path.join(HERE, "xv_cards.txt"), "w", encoding="utf-8", newline="\n") as f:
    for c in got:
        f.write(c["path"].replace("\\", "/") + "\n")

if DRY:
    print("(dry) 不写计划；xv_cards.txt 已更新")
    sys.exit(0)

out = [["结构化学", [{"path": c["path"].replace(os.sep, "/"), "src_dir": c["src_dir"],
                    "score": 0, "fp": c.get("fp", "")} for c in got]]]
json.dump(out, open(os.path.join(HERE, "vol_plan_XV.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("已写 vol_plan_XV.json：%s" % [(m, len(g)) for m, g in out])
