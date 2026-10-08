# -*- coding: utf-8 -*-
"""make_plan_XIV.py —— 卷 XIV（晶体专题·10 题）计划锁生成。

10 题全部为「晶体」主题（6 钙钛矿 + 4 晶体核心），全部属「结构化学」模块；
已回源核验（题面 10/10；其中 5 张文字层源逐串零缺失、5 张扫描件逐页目检吻合）。
用法: python -X utf8 make_plan_XIV.py [--dry]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_org as BO   # noqa: E402
BO.ALL_YEARS = True

DRY = '--dry' in sys.argv

# 晶体专题 10 题（钙钛矿 6 + 晶体核心 4）；顺序＝卷内题序
W = [
    "题-CM-01-05-很多具有钙钛矿结构",        # 1 chemy 迷人的钙钛矿 27分 图3        [钙钛矿]
    "题-CM-125-06-下图为理想钙钛矿",          # 2 chemy 理想钙钛矿立体结构图 10分 图8  [钙钛矿]
    "题-CM-150-06-在不同的温度和压力下",       # 3 chemy 锗酸钡及其结构变化 26分 图2    [钙钛矿]
    "题-HZ-08-05-以下是某四方晶体沿",         # 4 汇智 简单晶体结构·四方投影 22分 图5  [钙钛矿]
    "题-HYS-01-02-研究钙钛矿衍生结构",         # 5 化英社 钙钛矿衍生结构 Ramsdell 25分 图1 [钙钛矿]
    "题-QBY-10-05-的结构常被称为六方钙钛矿",    # 6 清北营 BaNiOx 六方钙钛矿 18分 图7    [钙钛矿]
    "题-QBY-08-06-611堆积层永远是",           # 7 清北营 对六方堆积层的探索 26分 图8
    "题-HZ-11-05-在晶体结构的研究中",         # 8 汇智 尖晶石及其类似晶体结构 27分 图7
    "题-XeC-12-01-在我们通常的认知里",         # 9 XeChem 基本点阵形式问题 21分 图5
    "题-2ChO-04-05-51金红石是典型",           # 10 2ChO 金红石及其相似结构 图8
]

pool = BO.build_pool()
by_base = {}
for _m in pool:
    for c in pool[_m]:
        by_base.setdefault(os.path.basename(c['path']), c)

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
    print("  %-52s d%s q%-5d 图%d calc%s" %
          (hits[0][:50], c['difficulty'], c['qlen'], len(c['imgs']), c.get('calc', 0)))
if not ok or len(got) != len(W):
    print("** 解析失败，未写盘")
    sys.exit(1)

with open(os.path.join(HERE, 'xiv_cards.txt'), 'w', encoding='utf-8', newline='\n') as f:
    for c in got:
        f.write(c['path'].replace('\\', '/') + '\n')

if DRY:
    print("(dry) 不写计划")
    sys.exit(0)

out = [["结构化学", [{"path": c['path'].replace(os.sep, '/'), "src_dir": c['src_dir'],
                    "score": 0, "fp": c.get('fp', '')} for c in got]]]
json.dump(out, open(os.path.join(HERE, 'vol_plan_XIV.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print("已写 vol_plan_XIV.json：%s" % [(m, len(g)) for m, g in out])
