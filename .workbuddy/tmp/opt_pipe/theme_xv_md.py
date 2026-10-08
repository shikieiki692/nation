# -*- coding: utf-8 -*-
"""卷 XV 卷 md 主题化（晶体专题）：部分标题 + 组卷口径补注。带断言。"""
import os
import sys

ROOT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(ROOT, "04-题库")
APPLY = "--apply" in sys.argv

JOBS = [
    ("初赛模拟卷XV（非有机·答案版）.md", [
        ("## 第一部分　结构化学（第 1–10 题，共 130 分）",
         "## 第一部分　晶体结构（第 1–10 题，共 130 分）"),
        ("第一部分　结构化学（第 1–10 题，130 分）",
         "第一部分　晶体结构（第 1–10 题，130 分）"),
        ("> 题卡溯源见卷末选题清单。",
         "> ★ **本题为「晶体结构」专题卷**：10 题全部为晶体主题（其中 **7 题为钙钛矿／钙钛矿衍生／"
         "反钙钛矿结构**，另有刚玉、黄铜矿型、二维晶体等）；题面与答案已逐张回源核验。\n"
         "> 题卡溯源见卷末选题清单。"),
    ]),
    ("初赛模拟卷XV（非有机·学生版）.md", [
        ("## 第一部分　结构化学（第 1–10 题，共 130 分）",
         "## 第一部分　晶体结构（第 1–10 题，共 130 分）"),
        ("第一部分　结构化学（第 1–10 题，130 分）",
         "第一部分　晶体结构（第 1–10 题，130 分）"),
    ]),
]

for fn, reps in JOBS:
    p = os.path.join(QB, fn)
    t = open(p, encoding="utf-8-sig").read()
    assert "\r\n" not in t, fn + " 含 CRLF"
    for old, new in reps:
        c = t.count(old)
        print("  %-58s 命中 %d" % (old[:56], c))
        assert c == 1, "命中数须为 1：%s" % old[:40]
        t = t.replace(old, new)
    print("%s：替换 %d 组" % (fn, len(reps)))
    if APPLY:
        open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("  ✅ 已写盘")
print("完成")
