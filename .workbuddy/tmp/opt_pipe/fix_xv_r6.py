# -*- coding: utf-8 -*-
"""fix_xv_r6.py —— 卷 XV 第7题（YS-03-03）7-4 表格表头补全（2026-10-09）。

源 PDF（一式03答案 p5）实测：表头为 `i = 1 2 3`，卡里第三列表头丢失（两处表：题面 + 答案稿副本）。
ρ(Aᵢ) 行第三格在源扫描件里被水印整块遮黑、无法辨识；且题面要求「计算晶体 A₃ 的密度」
⇒ 该格**本就留空**（对应 i=3 待算），故只补表头 `3`，数值格保持空白（宁留白，不臆造）。

另：`并计算晶体 A₃ 的密度提示: ...` 两句在源里分属两行，卡内粘连 ⇒ 拆行。

用法：python -X utf8 fix_xv_r6.py [--apply]
"""
import io
import os
import sys
import shutil
import datetime

R = r"C:\Obsidion\妙妙屋"
HERE = os.path.join(R, ".workbuddy", "tmp", "opt_pipe")
Q = os.path.join(R, "04-题库", "2026机构初赛模拟题")
BAKDIR = os.path.join(HERE, "card_bak_r6")
APPLY = "--apply" in sys.argv

YS = os.path.join(Q, "一式", "题-YS-03-03-主族元素E的氧化物与碱金属M.md")

EDITS = [
    (YS,
     "<tr><td>i=</td><td>1</td><td>2</td><td></td></tr>",
     "<tr><td>i=</td><td>1</td><td>2</td><td>3</td></tr>",
     "① 表头补第三列「3」", 2),
    (YS,
     "并计算晶体 ${\\mathbf{A}}_{3}$ 的密度提示: 考虑不对称化学环境带来的畸变。",
     "并计算晶体 ${\\mathbf{A}}_{3}$ 的密度。\n\n提示：考虑不对称化学环境带来的畸变。",
     "② 「提示」独立成段", 1),
]


def main():
    cache = {}

    def load(p):
        if p not in cache:
            cache[p] = io.open(p, encoding="utf-8-sig").read()
        return cache[p]

    ok = True
    for path, old, new, tag, want in EDITS:
        t = load(path)
        n = t.count(old)
        if n != want:
            print("!! [%s] 命中 %d（应 %d）" % (tag, n, want))
            ok = False
            continue
        cache[path] = t.replace(old, new)
        print("OK [%s] ×%d" % (tag, n))
    if not ok:
        print("\n有未命中项，未写盘。")
        return
    if not APPLY:
        print("\n(dry) 未写盘。加 --apply 执行。")
        return
    os.makedirs(BAKDIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    for p in sorted(cache):
        shutil.copy2(p, os.path.join(BAKDIR, os.path.basename(p) + ".bak-" + stamp))
        io.open(p, "w", encoding="utf-8", newline="\n").write(cache[p])
        print("写盘", os.path.basename(p)[:52])
    print("\n完成；备份目录 =", BAKDIR)


main()
