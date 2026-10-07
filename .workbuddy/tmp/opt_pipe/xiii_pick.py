# -*- coding: utf-8 -*-
"""xiii_pick.py —— 卷 XIII 遴选（只有物理化学）候选列出。

修复既往工具 bug：bw_pick/zero_pick/bw_audit 的「排除既往卷已用卡」用 `c['path'] in used`
比对，但 build_org 的 c['path'] 混用 '\\' 与 '/'（如 '04-题库/2026机构初赛模拟题\\化英社\\x.md'），
而 used 里全是 '/' ⇒ **排除失效**（卷 XII 的卡仍出现在候选里）。本脚本两侧统一 norm。

用法: python -X utf8 xiii_pick.py [n]
输出: flag 彩占比 图数 calc 答案字 [机构] 卡名 | 题面前 46 字
"""
import os
import re
import sys
import glob
import json
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_org as BO
BO.ALL_YEARS = True

PHYS = re.compile(
    r'热力学|焓|熵|吉布斯|自由能|平衡常数|化学平衡|相图|相平衡|蒸气压|活度|化学势|稀释|'
    r'动力学|反应速率|速率常数|反应级数|活化能|半衰期|稳态近似|Arrhenius|阿伦尼乌斯|催化|'
    r'电化学|电极电势|电动势|原电池|电解|能斯特|Nernst|Latimer|电池|超电势|'
    r'量子|波函数|薛定谔|能级|跃迁|配分函数|统计热力学|玻尔兹曼|Boltzmann|德布罗意|隧穿|'
    r'理想气体|热容|状态方程|范德华|卡诺|绝热|等温|焦耳|'
    r'吸附|Langmuir|表面张力|胶体|渗透压|依数性|溶液|稀溶液|'
    r'溶度积|溶解平衡|酸碱平衡|电离平衡|pH|缓冲|配位平衡|稳定常数|'
    r'熔化|沸腾|升华|三相点|临界|克拉佩龙|Clapeyron|晶格能|Born|Haber|生成焓|键能|熵变')

ORG2 = re.compile(
    r'有机|碳正离子|碳负离子|亲核|亲电|离去基|手性|对映|非对映|旋光|光活性|消旋|立体选|'
    r'构型|构象|官能团|烯烃|炔烃|芳烃|卤代|羧|酯|酰胺|胺|酚|醌|杂环|吡啶|呋喃|噻吩|吡咯|'
    r'卟啉|酞菁|冠醚|席夫碱|Diels|Alder|Wittig|Grignard|格氏|傅克|重氮|周环|电环化|'
    r'加成反应|消除反应|取代反应|聚合|全合成|保护基|卡宾|烷基|羟基|羰基|亚胺|重排|'
    r'比较下列|选出下列|排序|稳定性大小|基团')

IMG = re.compile(r"!\[\[([^\]\|]+?)(?:\\?\|\d+)?\]\]|!\[[^\]]*\]\(([^)]+)\)")
# 答案「洁净」判据：无 array/hline（texmath 会印字面）、无元注记、无占位
ANS_BAD = re.compile(r'\\begin\{array\}|\\hline|回收补录|自动拆卡标记|尚未经人工复核|待人工校准|'
                     r'\\omega\b|答案由源')

IDX = {}
for p in glob.glob(os.path.join(BO.ROOT, "04-题库/2026机构初赛模拟题/*/images/*")):
    IDX.setdefault(os.path.basename(p), p)


def norm(p):
    return p.replace('\\', '/')


def color_frac(path):
    try:
        im = Image.open(path).convert("RGB")
    except Exception:
        return None
    im.thumbnail((400, 400))
    px = list(im.getdata())
    n = len(px)
    if not n:
        return None
    return sum(1 for r, g, b in px if max(r, g, b) - min(r, g, b) > 50) / n


def imgs_of(c):
    t = c['question'] + '\n' + c['answer']
    got = []
    for a, b in IMG.findall(t):
        got.append((a or b).strip())
    return list(dict.fromkeys(got))


# ── 既往卷已用卡（修复版排除）──
used = set()
for pf in sorted(glob.glob(os.path.join(HERE, 'vol_plan_*.json'))):
    try:
        for _m, _l in json.load(open(pf, encoding='utf-8')):
            for _c in _l:
                used.add(norm(_c['path']))
    except Exception:
        pass
# 15 张换卡替代卡
SWAP = {"题-HYS-02-02-21", "题-HYS-02-03-钴氧体系", "题-UChO-01-05", "题-HYS-03-01",
        "题-HYS-01-06-光子晶体", "题-QBY-02-07", "题-CM-173-08", "题-GM-01-08-81", "题-HYS-02-10-101",
        "题-GM-25-05", "题-QBY-01-05", "题-CM-60-20", "题-CM-150-06", "题-HZ-12-03", "题-HYS-08-01"}

n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 60
pool = BO.build_pool()

rows = []
for c in pool["化学原理"]:
    if norm(c['path']) in used:
        continue
    base = os.path.basename(c['path'])[:20]
    if any(base.startswith(s) for s in SWAP):
        continue
    x = BO.desc_of(c) + ' ' + c['question'] + ' ' + c['answer']
    if not PHYS.search(c['question'] + c['answer']) or ORG2.search(x):
        continue
    im = imgs_of(c)
    fr = [f for f in (color_frac(IDX[k]) for k in im if k in IDX) if f is not None]
    mx = max(fr) if fr else 0.0
    rows.append((c.get('calc', 0), mx, len(im), c))

rows.sort(key=lambda r: -r[0])
print("# 化学原理（物化∩非有机，已排除既往卷+换卡替代）：候选 %d 张（按 calc 降序，前 %d）" % (len(rows), n))
for calc, mx, ni, c in rows[:n]:
    if ni == 0:
        tag = "零图 "
    elif mx < 0.02:
        tag = "黑白 "
    elif mx < 0.10:
        tag = "浅色 "
    else:
        tag = "彩色 "
    ans = re.sub(r'\s+', ' ', c['answer'])
    a_img = len(re.findall(r'!\[\[|!\[' , c['answer']))
    clean = "CLEAN" if not ANS_BAD.search(c['answer']) else "DIRTY"
    q = re.sub(r'\s+', ' ', re.sub(r'!\[\[[^\]]*\]\]', '', c['question']))[:46]
    print("%s %s 彩%5.1f%% 图%2d 答图%d calc%6.2f 答%5d字 [%s] %s | %s"
          % (clean, tag, mx * 100, ni, a_img, calc, len(ans), c['src_dir'],
             os.path.basename(c['path'])[:30], q))
