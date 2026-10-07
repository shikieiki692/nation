# -*- coding: utf-8 -*-
"""xiii_resolve.py —— 把短名单前缀解析为完整路径（唯一命中校验），写 xiii_cards.txt / xiii_alt.txt。"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_org as BO
BO.ALL_YEARS = True

# 主选 10（前缀唯一）
MAIN = [
    "题-GChO-08-06-通过甲醇裂解制备",  # 质心GChO 甲醇裂解 热力学+电解效率
    "题-UChO-01-04-标准压力下",       # 质心UChO δ-Fe熔化 相变
    "题-QBY-02-05-本题记丙酮为",       # 清北营 丙酮/二氯甲烷 稀溶液/恒沸物
    "题-BJLY-01-05-已知51计算1L100",   # 北京夏令营 沉淀+配位平衡
    "题-QBY-05-01-以下是pH0时V",      # 清北营 V Latimer 电势图（有图）
    "题-GChO-47-02-已知的为本题",      # 质心GChO Zn(OH)2 沉淀+配位+两性
    "题-YJ-02-02-酸雨是指",           # 壹尖培优 酸雨化学平衡
    "题-CM-83-03-3-1向20mL",          # chemy 醋酸解离 酸碱平衡
    "题-HZ-03-06-工业上制备氢气",       # 汇智 工业制氢 化学平衡
    "题-QBY-10-01-11298K下",          # 清北营 弹式热量计 热化学
]
# 备选
ALT = [
    "题-CM-100-01-氯苯", "题-GChO-42-05-所有的计算和实验", "题-GChO-51-04-是一个典中典",
    "题-GChO-32-06-61现在高温", "题-UChO-01-02-经典的卡诺循环", "题-UChO-02-06-61制冷剂",
    "题-QBY-02-03-铝热反应", "题-FY-01-03-血液是生物体", "题-GM-04-02-21从表面因素",
    "题-YJ-02-07-和单质汞", "题-XeC-22-02-碘化汞", "题-2ChO-05-03-一种钠离子电池",
    "题-HZ-05-05-51某小组",
]

pool = BO.build_pool()
allc = [c for m in pool for c in pool[m]]


def resolve(keys, out):
    got, bad = [], []
    for k in keys:
        hits = [c for c in allc if os.path.basename(c['path']).startswith(k)]
        # 去重（同卡只应命中一次）
        uniq = {os.path.basename(c['path']): c for c in hits}
        if len(uniq) != 1:
            bad.append((k, [os.path.basename(x) for x in uniq]))
            continue
        got.append(list(uniq.values())[0])
    print("== %s ==" % out)
    for c in got:
        print("  OK  [%s] %s  d%s calc%s 图%d" % (c['src_dir'], os.path.basename(c['path']),
              c['difficulty'], c.get('calc', 0), len(c['imgs'])))
    for k, h in bad:
        print("  !!  命中 %d: %s | %s" % (len(h), k, h[:3]))
    with open(os.path.join(HERE, out), 'w', encoding='utf-8', newline='\n') as f:
        for c in got:
            f.write(c['path'].replace('\\', '/') + '\n')
    return got


resolve(MAIN, 'xiii_cards.txt')
resolve(ALT, 'xiii_alt.txt')
