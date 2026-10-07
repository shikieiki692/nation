# -*- coding: utf-8 -*-
"""make_plan_XIII.py —— 卷 XIII（只有物理化学·10 题）计划锁生成。
从池内按**完整文件名前缀**解析（规避卡 ID 撞车）；不在池中即报错。
用法: python -X utf8 make_plan_XIII.py [--dry]
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_org as BO
BO.ALL_YEARS = True

DRY = '--dry' in sys.argv

# 化学原理（10）——全物理化学，黑白可打印，跨 7 机构，偏计算
W = [
    "题-GChO-08-06-通过甲醇裂解制备",  # 质心GChO 甲醇裂解 热力学+电解效率
    "题-UChO-01-04-标准压力下",       # 质心UChO δ-Fe熔化 相变热力学
    "题-QBY-02-05-本题记丙酮为",       # 清北营 丙酮/二氯甲烷 稀溶液+恒沸物
    "题-BJLY-01-05-已知51计算1L100",   # 北京夏令营 沉淀+配位平衡
    "题-QBY-05-01-以下是pH0时V",      # 清北营 V Latimer 电势图（有图·黑白）
    "题-CM-100-01-氯苯A和溴苯",        # chemy 氯苯/溴苯 理想液态混合物 气液平衡
    "题-YJ-02-02-酸雨是指",           # 壹尖培优 酸雨化学平衡
    "题-CM-83-03-3-1向20mL",         # chemy 醋酸缓冲/铅 酸碱+沉淀+配位
    "题-HZ-03-06-工业上制备氢气",       # 汇智 工业制氢 化学平衡
    "题-QBY-10-01-11298K下",          # 清北营 弹式热量计 热化学
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
    if c not in pool["化学原理"]:
        print("!! %s 不在化学原理（实际在 %s）" % (hits[0], [m for m in pool if c in pool[m]]))
        ok = False
    got.append(c)
    print("  %s  d%s q%s calc%s 图%d" % (hits[0], c['difficulty'], c['qlen'], c.get('calc', 0), len(c['imgs'])))
if not ok:
    print("** 解析失败，未写盘")
    sys.exit(1)

plan = [["化学原理", got]]
with open(os.path.join(HERE, 'xiii_cards.txt'), 'w', encoding='utf-8', newline='\n') as f:
    for c in got:
        f.write(c['path'].replace('\\', '/') + '\n')
if DRY:
    print("(dry) 不写计划"); sys.exit(0)
out = [["化学原理", [{"path": c['path'].replace(os.sep, '/'), "src_dir": c['src_dir'],
                    "score": 0, "fp": c.get('fp', '')} for c in got]]]
json.dump(out, open(os.path.join(HERE, 'vol_plan_XIII.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print("已写 vol_plan_XIII.json：%s" % [(m, len(g)) for m, g in plan])
