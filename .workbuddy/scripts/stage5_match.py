"""阶段5：对剩余 46 块逐块定向检索图谱库候选。

与 img_hit_survey.py（主题级粗查）不同：这里每块给**专属关键词**，
并只输出带【视觉核验】/🟢 的高置信条目，便于逐块决策。
"""
import csv
import re
from pathlib import Path

IDX = [
    ("有机", Path(r"10-索引与统计/01-有机化学图谱总索引.md")),
    ("结构", Path(r"10-索引与统计/02-结构与无机化学图谱总索引.md")),
    ("物化", Path(r"10-索引与统计/03-物化与分析化学图谱总索引.md")),
]
CACHE = {tag: (p.read_text(encoding="utf-8") if p.exists() else "") for tag, p in IDX}

rows = list(csv.DictReader(
    open(r".workbuddy/tmp/verbatim_worklist.csv", encoding="utf-8-sig")))

# 块序号 -> (学科, [关键词...])   序号对应 stage5 清单
Q = {
    1:  ("物化", ["胶团", "胶束", "双电层", "电动电位"]),
    2:  ("有机", ["SN2", "瓦尔登", "背面进攻", "过渡态"]),
    3:  ("有机", ["SN2", "构型翻转", "立体化学"]),
    5:  ("有机", ["Diels", "endo", "双烯合成", "内型"]),
    6:  ("有机", ["电环化", "顺旋", "对旋"]),
    9:  ("有机", ["共振", "羧酸根", "甲酸根"]),
    10: ("有机", ["Fischer", "费歇尔", "投影式", "甘油醛"]),
    11: ("物化", ["红外", "IR 谱", "特征频率", "波数"]),
    12: ("有机", ["Cram", "克拉姆"]),
    13: ("有机", ["Wagner", "瓦格纳", "甲基迁移", "碳正离子重排"]),
    14: ("有机", ["卡宾", "carbene", "单线态"]),
    15: ("物化", ["势能", "反应坐标", "过渡态", "活化能"]),
    16: ("有机", ["Simmons", "西蒙斯", "环丙烷化"]),
    17: ("有机", ["CIP", "Re 面", "Si 面", "对映面"]),
    19: ("有机", ["邻基参与", "锚定", "桥环"]),
    20: ("有机", ["Cram", "Felkin", "不对称诱导"]),
    21: ("有机", ["NBS", "琥珀酰亚胺"]),
    24: ("有机", ["NBS", "烯丙位", "溴化"]),
    27: ("有机", ["催化循环", "基元反应"]),
    28: ("有机", ["复分解", "metathesis", "金属杂环"]),
    29: ("有机", ["Cram", "Felkin"]),
    30: ("有机", ["Wagner", "重排", "碳正离子"]),
    31: ("有机", ["Pinacol", "频哪醇"]),
    32: ("有机", ["Claisen", "克莱森"]),
    34: ("结构", ["多碘", "I3", "I₅", "聚碘"]),
    35: ("结构", ["多碘", "I3", "三碘"]),
    36: ("结构", ["EDTA", "钌", "Ru"]),
    37: ("结构", ["d轨道", "电子排布", "eg", "t2g"]),
    38: ("结构", ["d轨道", "电子排布", "eg", "t2g"]),
    39: ("结构", ["八面体场", "晶体场", "分裂", "eg"]),
    40: ("结构", ["醋酸亚铬", "Cr2", "四重键", "Cr-Cr"]),
    41: ("结构", ["三核", "铬", "Cr3", "三角形"]),
    42: ("结构", ["三核", "铬", "Cr3"]),
    45: ("结构", ["铼", "Re", "氮化物", "链状"]),
    46: ("结构", ["铼", "Re", "氮化物"]),
}

RE_ROW = re.compile(r"^\|\s*([0-9a-f]{40,}\.jpg)\s*\|")


def search(subj, kws, limit=3):
    txt = CACHE.get(subj, "")
    hits = []
    for line in txt.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        desc = cells[2]
        if not cells[0].endswith(".jpg"):
            continue
        score = sum(1 for k in kws if k in desc or k in cells[0])
        if score == 0:
            continue
        good = ("视觉核验" in desc) or ("🟢" in line)
        hits.append((score, good, cells[0], desc))
    hits.sort(key=lambda x: (-x[0], not x[1]))
    return hits[:limit]


print("%-4s %-46s %s" % ("#", "块（首行截断）", "候选（★=已视觉核验）"))
print("-" * 118)
found = 0
for i, r in enumerate(rows, 1):
    if i not in Q:
        continue
    subj, kws = Q[i]
    hits = search(subj, kws)
    first = (r["首行"] or "").strip()[:42]
    if not hits:
        print("%-4d %-46s （无命中）" % (i, first))
        continue
    found += 1
    for j, (sc, good, h, d) in enumerate(hits):
        tag = "★" if good else " "
        prefix = "%-4d %-46s" % (i, first) if j == 0 else "%-4s %-46s" % ("", "")
        print("%s %s %s  %s" % (prefix, tag, h[:16] + "…", d[:66]))
print()
print("有候选的块：%d / %d" % (found, len(Q)))
