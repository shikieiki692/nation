# -*- coding: utf-8 -*-
"""修 OCR 形近错字（品体→晶体、品系→晶系），限于卷 X 及其 16 张源卡。

⚠️ 必须带负向后视：`样品体系/样品体积/样品体积磁化率` 里的「品体」是**正确**用法。
"""
import io, json, os, re, sys

R = r"C:\Obsidion\妙妙屋"
PLAN = os.path.join(R, ".workbuddy", "tmp", "opt_pipe")
sys.stdout.reconfigure(encoding="utf-8")

RULE1 = re.compile(r"(?<!样)品体")
RULE2 = re.compile(r"(?<!产|作|样|出|系)品系")


def fix(t):
    n1 = len(RULE1.findall(t)); t = RULE1.sub("晶体", t)
    n2 = len(RULE2.findall(t)); t = RULE2.sub("晶系", t)
    return t, n1, n2


apply_ = "--apply" in sys.argv
cards = [c["path"] for _m, l in json.load(open(os.path.join(PLAN, "vol_plan_X.json"), encoding="utf-8")) for c in l]
files = [os.path.join(R, "04-题库/初赛模拟卷X（非有机·学生版）.md"),
         os.path.join(R, "04-题库/初赛模拟卷X（非有机·答案版）.md")] + \
        [os.path.join(R, p) for p in cards]
tot1 = tot2 = 0
for p in files:
    raw = io.open(p, encoding="utf-8-sig").read()
    new, n1, n2 = fix(raw)
    if n1 or n2:
        print("  %-56s 品体→晶体 %d ｜ 品系→晶系 %d" % (os.path.basename(p)[:54], n1, n2))
        tot1 += n1; tot2 += n2
        if apply_:
            # 保留原行尾：这里文件均为 LF
            io.open(p, "w", encoding="utf-8", newline="\n").write(new)
print("合计 品体→晶体 %d ／ 品系→晶系 %d（apply=%s）" % (tot1, tot2, apply_))
