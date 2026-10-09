# -*- coding: utf-8 -*-
"""fix_xiv_r7.py —— 卷 XIV 第 1 题（CM-01-05）**题面要素回补**（2026-10-09）。

病象（owner 反馈「第一题不全，图片感觉少了」）：题面缺 4 处源 PDF p6 上明明白白印在**题面**的内容，
它们在建卡时被划入答案区：
  ① 过渡段「对称性的下降是产生钙钛矿独特物理化学性质的必要条件…得到一系列二维钙钛矿结构。」
  ② **5-2 的配图**（三种二维钙钛矿结构：Ruddlesden-Popper／Dion-Jacobson／Aurivillius）★ 学生版因此无图
  ③ 过渡段「二维钙钛矿在太阳能电池领域…均能产生二次谐波信号。」
  ④ 5-4 的题干「有机-无机杂化钙钛矿已成为材料领域的热门研究对象。称取 1.89 g …得到二维钙钛矿晶体 M。」
另：5-1-3、5-2、5-3、5-4-1、5-4-2、5-4-3 六行**无空行分隔** ⇒ 渲染成同一段落（子问挤在一起）。

处置：按源 PDF 顺序把 ①~④ 插回题面，并给每个子问补空行；答案区里同名段落交给
`build_org.strip_q_echo()` 自动剥离（文字逐字相同）。

用法：python -X utf8 fix_xiv_r7.py [--apply]
"""
import io
import os
import sys
import shutil
import datetime

R = r"C:\Obsidion\妙妙屋"
HERE = os.path.join(R, ".workbuddy", "tmp", "opt_pipe")
CARD = os.path.join(R, "04-题库", "2026机构初赛模拟题", "chemy",
                    "题-CM-01-05-很多具有钙钛矿结构的化合物是.md")
BAKDIR = os.path.join(HERE, "card_bak_r7")
APPLY = "--apply" in sys.argv

A = ("对称性的下降是产生钙钛矿独特物理化学性质的必要条件,调控钙钛矿的对称性也是科研领域的重要课题。"
     "将三维钙钛矿沿垂直四重轴的平面切开,并调整层间的原子即可得到一系列二维钙钛矿结构。")
IMG = "![](images/3e836873135ef1527b0d40dee3f60bd50288ec5efe97a648cd0d1c079f700927.jpg)"
C = ("二维钙钛矿在太阳能电池领域展现出极大的应用前景,这与其非线性光学性质息息相关。"
     "二次谐波(Second Harmonic Generation, SHG)是指非线性介质将相同频率的光子混合而产生的频率加倍的信号,"
     "一系列不具有对称中心的二维钙钛矿晶体均能产生二次谐波信号。")
D = ("有机-无机杂化钙钛矿已成为材料领域的热门研究对象。称取 "
     "$1.89 \\mathrm{~g} \\mathrm{Pb}(\\mathrm{CH}_{3} \\mathrm{COO})_{2} \\cdot 3 \\mathrm{H}_{2} \\mathrm{O}$ "
     "溶解在 HBr 溶液中, 再加入 $0.32 \\mathrm{~g}$ 乙胺, 在合适的条件下反应即可得到一种二维钙钛矿晶体 M。")

L52 = ("5-4-1 直接指出 M 属于哪种类型的二维钙钛矿"
       "(Ruddlesden-Popper 相、Dion-Jacobson 相或 Aurivillius 相)。")

EDITS = [
    ("提示：晶胞图中给出的原子并不都在晶胞内。\n5-1-3 ",
     "提示：晶胞图中给出的原子并不都在晶胞内。\n\n5-1-3 ",
     "① 提示 / 5-1-3 分行", 1),
    ("属于铁电相。\n5-2 下面给出了",
     "属于铁电相。\n\n" + A + "\n\n5-2 下面给出了",
     "② 插入过渡段（补题面）", 1),
    ("则记为 C)\n5-3 由于传统的",
     "则记为 C)\n\n" + IMG + "\n\n" + C + "\n\n5-3 由于传统的",
     "③ 插入 5-2 配图 + 过渡段 ★", 1),
    ("解释原因。\n5-4-1 ",
     "解释原因。\n\n" + D + "\n\n5-4-1 ",
     "④ 插入 5-4 题干", 1),
    (L52 + "\n5-4-2 ", L52 + "\n\n5-4-2 ", "⑤ 5-4-1 / 5-4-2 分行", 1),
    ("据此计算 M 的化学式。\n5-4-3 ",
     "据此计算 M 的化学式。\n\n5-4-3 ",
     "⑥ 5-4-2 / 5-4-3 分行", 1),
]


def main():
    t = io.open(CARD, encoding="utf-8-sig").read()
    ok = True
    for old, new, tag, want in EDITS:
        n = t.count(old)
        if n != want:
            print("!! [%s] 命中 %d（应 %d）" % (tag, n, want))
            ok = False
            continue
        t = t.replace(old, new, 1)
        print("OK [%s]" % tag)
    if not ok:
        print("\n有未命中项，未写盘。")
        return
    if not APPLY:
        print("\n(dry) 未写盘。加 --apply 执行。")
        return
    os.makedirs(BAKDIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    shutil.copy2(CARD, os.path.join(BAKDIR, os.path.basename(CARD) + ".bak-" + stamp))
    io.open(CARD, "w", encoding="utf-8", newline="\n").write(t)
    print("写盘", os.path.basename(CARD))
    print("备份 =", BAKDIR)


main()
