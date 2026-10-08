# -*- coding: utf-8 -*-
"""fix_xv_cards2.py —— 卷 XV 追加源卡修复。

  HYS-20-04：题面里嵌着 4-1 的答案（`$$3K2NiF6→…$$`）⇒ 移入答案区；
             并把粘连的「4-1写出」拆为「4-1 写出」（否则组卷重编号不识别）。
用法: python -X utf8 fix_xv_cards2.py [--apply]
"""
import os
import shutil
import sys

Q = r"04-题库/2026机构初赛模拟题"
APPLY = "--apply" in sys.argv

P = f"{Q}/化英社/题-HYS-20-04-ABCDE是五种元素组成相同.md"

E = [
    # ① 题面：拆粘连 + 把 4-1 答案移出
    ("C的变体。4-1写出反应2的化学反应方程式。\n\n$$\n"
     "3 \\mathrm{K} _ {2} \\mathrm{NiF} _ {6} \\rightarrow 2 \\mathrm{K} _ {3} \\mathrm{NiF} _ {6} + "
     "\\mathrm{NiF} _ {2} + 2 \\mathrm{F} _ {2} (2 \\text {分})\n$$\n\n4-2 写出",
     "C的变体。4-1 写出反应2的化学反应方程式。\n\n4-2 写出",
     "HYS-20-04 题面移出 4-1 答案"),
    # ② 答案区：补 4-1 答案
    ("正在阅读**；请与前文「题目」段合并阅读。",
     "正在阅读**；请与前文「题目」段合并阅读。",
     "noop-placeholder"),
]

t = open(P, encoding="utf-8-sig").read()

ok = True
# ①
old, new, tag = E[0]
if t.count(old) != 1:
    print("!! [%s] 命中 %d" % (tag, t.count(old)))
    ok = False
else:
    t = t.replace(old, new, 1)
    print(" OK [%s]" % tag)

# ② 在答案区 📌 提示之后插入 4-1 答案
anchor = "请与前文「题目」段合并阅读。\n"
ins = ("请与前文「题目」段合并阅读。\n\n"
       "**4-1** $3\\mathrm{K_2NiF_6} \\rightarrow 2\\mathrm{K_3NiF_6} + \\mathrm{NiF_2} + "
       "2\\mathrm{F_2}$（2 分）\n")
if t.count(anchor) != 1:
    print("!! [HYS-20-04 答案区补 4-1] 命中 %d" % t.count(anchor))
    ok = False
else:
    t = t.replace(anchor, ins, 1)
    print(" OK [HYS-20-04 答案区补 4-1]")

if not ok:
    print("** 未写盘")
    sys.exit(1)

if not APPLY:
    print("(dry) 待改 1 文件")
    sys.exit(0)

shutil.copy2(P, P + ".bak-xv2")
open(P, "w", encoding="utf-8", newline="\n").write(t)
print("写盘 %s" % P)
