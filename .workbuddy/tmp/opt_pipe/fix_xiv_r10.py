# -*- coding: utf-8 -*-
"""r10：HYS-01-02 答案区回显行内的方括号化学式下标规范化。"""
import os, shutil, datetime

P = "04-题库/2026机构初赛模拟题/化英社/题-HYS-01-02-研究钙钛矿衍生结构时常用Ra.md"
BAK = ".workbuddy/tmp/opt_pipe/card_bak_r10"
os.makedirs(BAK, exist_ok=True)

PAIRS = [("[O6]", "[O₆]"), ("[Ba₂O4]", "[Ba₂O₄]"), ("[BaO3]", "[BaO₃]"), ("[BaO2]", "[BaO₂]")]

apply_ = "--apply" in os.sys.argv
t0 = open(P, encoding="utf-8-sig").read()
t = t0
for old, new in PAIRS:
    n = t.count(old)
    print("%-10s → %-10s  %d 处" % (old, new, n))
    t = t.replace(old, new)

if t == t0:
    print("无变化")
    os.sys.exit(0)

if apply_:
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    shutil.copy2(P, os.path.join(BAK, os.path.basename(P) + ".bak-" + stamp))
    open(P, "w", encoding="utf-8", newline="\n").write(t)
    print("已写盘")
else:
    print("(dry)")
