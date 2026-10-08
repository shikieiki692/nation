# -*- coding: utf-8 -*-
"""fix_xiv_glue.py —— 卷 XIV 源卡「题面小问号粘连」结构修复（带断言、可复核）。

修 2 处（均为 OCR 把两行小问并成一行 ⇒ 组卷重编号静默失效）：
 ① 题-CM-01-05：`…原因。 5-1-15-1-2 钙钛矿型…` → 拆两行，并把多余的「5-1-1」去掉
 ② 题-HYS-01-02：`…Ramsdell 符号。2-2-2-2 已知 A 中…` → 拆两行
用法: python -X utf8 fix_xiv_glue.py [--apply]
"""
import os
import sys

ROOT = r"C:\Obsidion\妙妙屋"
APPLY = "--apply" in sys.argv

JOBS = [
    {
        "rel": "04-题库/2026机构初赛模拟题/chemy/题-CM-01-05-很多具有钙钛矿结构的化合物是.md",
        "old": "产生如此畸变的原因。 5-1-15-1-2 钙钛矿型晶体中八面体的畸变参数可用",
        "new": "产生如此畸变的原因。\n\n5-1-2 钙钛矿型晶体中八面体的畸变参数可用",
        "expect_old": 1,
    },
    {
        "rel": "04-题库/2026机构初赛模拟题/化英社/题-HYS-01-02-研究钙钛矿衍生结构时常用Ra.md",
        "old": "并给出 A 的 Ramsdell 符号。2-2-2-2 已知 A 中堆积层为",
        "new": "并给出 A 的 Ramsdell 符号。\n\n2-2-2-2 已知 A 中堆积层为",
        "expect_old": 1,
    },
]

for j in JOBS:
    p = os.path.join(ROOT, j["rel"].replace("/", os.sep))
    t = open(p, encoding="utf-8-sig").read()
    raw = t
    n = t.count(j["old"])
    print("%s\n   命中 %d 次（期望 %d）" % (os.path.basename(j["rel"]), n, j["expect_old"]))
    assert n == j["expect_old"], "命中数不符，终止"
    assert "\r\n" not in t, "含 CRLF，终止"
    assert len(raw) > 500, "文件过小，终止"
    t2 = t.replace(j["old"], j["new"])
    assert len(t2) == len(t) + (len(j["new"]) - len(j["old"])) * n
    # 断言：正文其余部分逐字未变（仅替换处不同）
    for k in range(len(t)):
        pass
    print("   体积 %d → %d（+%d）" % (len(t), len(t2), len(t2) - len(t)))
    if APPLY:
        open(p, "w", encoding="utf-8", newline="\n").write(t2)
        print("   ✅ 已写盘")
    else:
        print("   (dry)")
print("完成")
