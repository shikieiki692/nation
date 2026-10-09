# -*- coding: utf-8 -*-
"""fix_xv_r4.py —— 卷 XV 数值指数「丢负号」修复（2026-10-09 视觉核验发现）。

病象：源卡把 PDF 的上标指数压成纯文本 ⇒ 负号丢失：
  · HZ-07-05 第6题：`h=6.626×10-34`（应 10⁻³⁴）、`c=3.00×108`（10⁸）、`1eV=1.602×10-19`（10⁻¹⁹）、
    答案 `=8.00×107m=800nm` —— 与同行「=800nm」自相矛盾（应 8.00×10⁻⁷ m）。
  · GChO-80-04 第3题 3-3-5：`(5.907×10-8)3=7.68g cm-32分`（应 10⁻⁸ 的立方 ⇒ g·cm⁻³；且「2分」被并进数值）。

处置：改用 **Unicode 上标**（零 texmath 风险，且与该表格其余纯文本单元格同风格），只补负号/单位，不改数值。

用法：python -X utf8 fix_xv_r4.py [--apply]
"""
import io
import os
import sys
import shutil
import datetime

R = r"C:\Obsidion\妙妙屋"
HERE = os.path.join(R, ".workbuddy", "tmp", "opt_pipe")
Q = os.path.join(R, "04-题库", "2026机构初赛模拟题")
BAKDIR = os.path.join(HERE, "card_bak_r4")
APPLY = "--apply" in sys.argv

HZ0705 = os.path.join(Q, "汇智", "题-HZ-07-05-有机金属卤化物钙钛矿材料近几.md")
GC80 = os.path.join(Q, "质心GChO", "题-GChO-80-04-41二维材料呈现出丰富的晶体.md")

EDITS = [
    (HZ0705,
     "(已知普朗克常量h=6.626×10-34J·s,光速c=3.00×108m/s,1eV=1.602×10-19J)",
     "(已知普朗克常量 h = 6.626×10⁻³⁴ J·s，光速 c = 3.00×10⁸ m/s，1 eV = 1.602×10⁻¹⁹ J)",
     "HZ-07-05 题面常数指数补负号", 1),
    (HZ0705,
     "E=hν=hc/λ（2 分）λ=hc/E=6.626×10-34×3.00×108/1.55×1.602×10-19=8.00×107m=800nm（2 分）",
     "E = hν = hc/λ（2 分）λ = hc/E = 6.626×10⁻³⁴ × 3.00×10⁸ ÷ (1.55 × 1.602×10⁻¹⁹) "
     "= 8.00×10⁻⁷ m = 800 nm（2 分）",
     "HZ-07-05 答案 800nm 指数补负号", 1),
    (GC80,
     "ρ=4×(54.94×2+58.69+69.72)/6.0221×1023×(5.907×10-8)3=7.68g cm-32分",
     "ρ = 4×(54.94×2+58.69+69.72) ÷ [6.0221×10²³ × (5.907×10⁻⁸)³] = 7.68 g·cm⁻³（2 分）",
     "GChO-80-04 3-3-5 密度式指数补负号", 1),
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
