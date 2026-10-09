# -*- coding: utf-8 -*-
"""fix_xv_r5.py —— 卷 XV 最后一批修复（2026-10-09 视觉核验）。

① YS-03-03 答案 `(a)(b)(c) 正前（2 分）` —— 「正前」非词（源 PDF p4 该处被水印遮挡，目检不完全清晰；
   题面为「选出下列说法中正确的」）⇒ 订正为「正确」。
② HYS-20-04 `4-3-2` 详解中 `ρ = 3.251 g·mol⁻¹` —— 源 PDF p8 实测即如此（源卷笔误：密度单位），
   而同题盒式答案作 `g cm⁻³` ⇒ 径改 + 加校勘注。

用法：python -X utf8 fix_xv_r5.py [--apply]
"""
import io
import os
import sys
import shutil
import datetime

R = r"C:\Obsidion\妙妙屋"
HERE = os.path.join(R, ".workbuddy", "tmp", "opt_pipe")
Q = os.path.join(R, "04-题库", "2026机构初赛模拟题")
BAKDIR = os.path.join(HERE, "card_bak_r5")
APPLY = "--apply" in sys.argv

YS0303 = os.path.join(Q, "一式", "题-YS-03-03-主族元素E的氧化物与碱金属M.md")
HYS2004 = os.path.join(Q, "化英社", "题-HYS-20-04-ABCDE是五种元素组成相同.md")

OLD_TAIL = ("\\\\ & (\\text {共} 3 \\text {分}) \\end{array}\n$$\n")

EDITS = [
    (YS0303, "(a)(b)(c) 正前 （2 分）", "(a)(b)(c) 正确（2 分）", "① 正前→正确", 1),
    (HYS2004, "= 3.251 \\mathrm{g} \\cdot \\mathrm{mol} ^ {- 1} (2 \\text {分})",
     "= 3.251 \\mathrm{g} \\cdot \\mathrm{cm} ^ {- 3} (2 \\text {分})",
     "② 密度单位 mol⁻¹→cm⁻³", 1),
    (HYS2004, OLD_TAIL,
     OLD_TAIL + "\n> 校勘（2026-10-09）：`4-3-2` 密度的单位，源卷详解误作 `g·mol⁻¹`，"
                 "已按密度单位订正为 `g·cm⁻³`（与本题盒式答案一致）。\n",
     "②b 加校勘注", 1),
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
        print("OK [%s]" % tag)
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
