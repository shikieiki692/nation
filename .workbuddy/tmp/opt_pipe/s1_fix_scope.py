# -*- coding: utf-8 -*-
"""S1 修复 Step0：范围复现（只读）
- 11 张待修卡的卷归属（vol_plan_X~XVI）
- 每张卡题面/答案区图数、图引用行号、题面引用语句行号
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")

TRUES1 = [  # 真 S1（图在卡内、引用位置错）
    ("chemy", "题-CM-65-06-6-1化学式为的化合物中含有.md", "富瓦烯结构如右图"),
    ("化英社", "题-HYS-02-01-已知XYZ是同族元素其相对原.md", "下左图的化合物"),
    ("化英社", "题-HYS-03-05-硫与铜元素可形成多种化合物它.md", "俯视图与晶胞示意图"),
    ("XeChem", "题-XeC-07-04-beginarraycmat.md", "如图1/图2"),
    ("chemy", "题-CM-123-07-利用手性助剂可实现双键不对称.md", "机理如下图所示"),
    ("chemy", "题-CM-165-02-顾名思义超酸是一类酸度极强的.md", "下图所示化合物"),
    ("chemy", "题-CM-17-07-超分子自组装的选择性.md", "下图所示金属配合物/PtLCl2"),
]
MISSING = [  # 题面图缺失（图不在卡内）
    ("chemy", "题-CM-106-01-1-1在C减压下丙二酸用脱水.md", "1-5烟花如下图"),
    ("汇智", "题-HZ-02-05-奎宁分子结构如右图所示是从金.md", "奎宁结构如右图"),
    ("质心GChO", "题-GChO-42-04-下图展示了某过渡元素X相关的.md", "下图展示转化"),
    ("化英社", "题-HYS-01-01-某金属元素M在自然界中分布广.md", None),
]

IMG = re.compile(r"!\[\[([^\]]+)\]\]|!\[\]\(([^)]+)\)|<img[^>]+src=\"([^\"]+)\"")


def volof(p):
    hits = []
    for f in sorted(glob.glob(os.path.join(R, ".workbuddy/tmp/opt_pipe", "vol_plan_*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for _m, lst in d:
            for c in lst:
                if os.path.basename(c["path"]) == os.path.basename(p):
                    hits.append(os.path.basename(f)[9:-5])
    return hits


def dump(inst, name, tag):
    p = os.path.join(BASE, inst, name)
    if not os.path.exists(p):
        print("!! 缺:", p)
        return
    t = open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")
    ls = t.split("\n")
    qi = next((k for k, l in enumerate(ls) if l.startswith("## 题目")), -1)
    ai = next((k for k, l in enumerate(ls) if l.startswith("## 参考答案")), -1)
    q = "\n".join(ls[qi:ai]); a = "\n".join(ls[ai:])
    qn = len(IMG.findall(q)); an = len(IMG.findall(a))
    print("=" * 76)
    print("▸ [%s] %s  ｜ 分类=%s ｜ 卷归属=%s" % (inst, name[:40], tag, volof(p) or "—"))
    print("   题面图 %d ｜ 答案图 %d ｜ 题面区行 %d-%d ｜ 答案区行 %d-EOF" % (qn, an, qi + 1, ai, ai + 1))
    # 题面引用语句行
    for k in range(qi, ai):
        s = ls[k].strip()
        if re.search(r"如下图|如右图|见下图|下图所示|如图|下左图", s):
            print("   题面引用 L%d: %s" % (k + 1, s[:88]))
    # 答案区前 3 个图引用行
    n = 0
    for k in range(ai, len(ls)):
        if IMG.search(ls[k]):
            print("   答案图   L%d: %s" % (k + 1, ls[k].strip()[:88]))
            n += 1
            if n >= 3:
                break


print("########## 真 S1（位置搬移）##########")
for inst, name, note in TRUES1:
    dump(inst, name, "真S1")
print("\n########## 题面图缺失（回源补图）##########")
for inst, name, note in MISSING:
    dump(inst, name, "题面图缺失")
