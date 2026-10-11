# -*- coding: utf-8 -*-
"""吞图 10 张 — 范围复现（只读）。
dump: 题面区引用句 / 答案区图行+上下文 / 池状态 / 卷计划锁归属。
"""
import os, re, sys, glob, json, importlib.util as u
sys.stdout.reconfigure(encoding="utf-8")

R = r"C:\Obsidion\妙妙屋"
os.chdir(R)
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")

CARDS = [
    ("清北营",   "题-QBY-02-04-下图为实验室制备12二溴乙烷.md"),
    ("清北营",   "题-QBY-03-09-Ineleganolide最.md"),
    ("chemy",    "题-CM-63-03-二氧化钛除金红石外还有多种晶.md"),
    ("chemy",    "题-CM-95-08-利用大量可得的天然不对称化合.md"),
    ("chemy",    "题-CM-103-05-生物正交反应是在活细胞内进行.md"),
    ("chemy",    "题-CM-12-07-71近年人们发现高压下可以制.md"),
    ("chemy",    "题-CM-17-02-锂离子电池技术的进步极大地推.md"),
    ("chemy",    "题-CM-138-09-观察下图所示合成路线并回答后.md"),
    ("化英社",   "题-HYS-03-04-甲烷单加氧酶MMO可在常温常.md"),
    ("质心UChO", "题-UChO-02-06-下图为一种实验室制备水合茚三.md"),
]

IMG = re.compile(r"!\[\[[^\]]+\]\]|!\[\]\([^)]+\)|<img[^>]+>")
QREF = re.compile(r"下图|上图|右图|左图|如图所示|如图|见图|见下")

# --- 卷计划锁 ---
plans = {}
for f in sorted(glob.glob(os.path.join(R, ".workbuddy", "tmp", "opt_pipe", "vol_plan_*.json"))):
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    vol = os.path.basename(f).replace("vol_plan_", "").replace(".json", "")
    for _m, lst in d:
        for c in lst:
            plans.setdefault(c["path"], []).append(vol)

# --- 池 ---
sp = u.spec_from_file_location("B", os.path.join(R, ".workbuddy", "tmp", "opt_pipe", "build_org.py"))
B = u.module_from_spec(sp); 
try:
    B.ALL_YEARS = True
except Exception:
    pass
sp.loader.exec_module(B)
B.ALL_YEARS = True
pool = B.build_pool()
print("池规模：%d（元素 %d / 结构 %d / 原理 %d）" % (
    sum(len(v) for v in pool.values()),
    len(pool.get("元素与分析", [])), len(pool.get("结构化学", [])), len(pool.get("化学原理", []))))
print()

for inst, name in CARDS:
    p = os.path.join(BASE, inst, name)
    t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
    ls = t.split("\n")
    qi = next((k for k, l in enumerate(ls) if l.startswith("## 题目")), None)
    ai = next((k for k, l in enumerate(ls) if l.startswith("## 参考答案")), None)
    print("=" * 84)
    print("▸ %s / %s" % (inst, name[:52]))
    print("   题面区行: %s  答案区起: %s  总行: %d" % (qi, ai, len(ls)))
    # 卷归属
    vols = plans.get(os.path.relpath(p, R).replace("/", "\\"), []) or plans.get(os.path.relpath(p, R), [])
    if not vols:
        for kk, vv in plans.items():
            if name.rsplit(".", 1)[0][:40] in kk:
                vols = vv; break
    print("   卷计划锁: %s" % ("、".join(vols) if vols else "（不在任何卷）"))
    why = B.why_not_in_pool(p)
    print("   池状态: %s" % ("★在池" if why is None else "掉池：" + str(why)))
    # 题面引用句
    print("   -- 题面区引用句 --")
    for k in range(qi, ai):
        if QREF.search(ls[k]):
            print("     Q L%-4d %s" % (k + 1, ls[k].strip()[:110]))
    # 题面区现有图
    print("   -- 题面区现有图 --")
    nq = 0
    for k in range(qi, ai):
        if IMG.search(ls[k]):
            nq += 1
            print("     Q L%-4d %s" % (k + 1, ls[k].strip()[:110]))
    if nq == 0:
        print("     （题面区 0 图）")
    # 答案区图行 + 上下文
    print("   -- 答案区图行（含前后文）--")
    for k in range(ai, len(ls)):
        if IMG.search(ls[k]):
            prev = ls[k - 1].strip()[:80] if k > 0 else ""
            print("     A L%-4d [前] %s" % (k + 1, prev))
            print("            [图] %s" % ls[k].strip()[:120])
