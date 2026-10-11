# -*- coding: utf-8 -*-
"""清单 CSV 更新：吞图 6 已修复 + 4 假阳性重判。"""
import csv, os, sys
sys.stdout.reconfigure(encoding="utf-8")
CSV = r"C:\Obsidion\妙妙屋\09-审计报告\2026-10-09-机构域题面图位置缺陷清单.csv"

FIXED = {
    "题-QBY-02-04-下图为实验室制备12二溴乙烷": " 【已修复 2026-10-11 · 吞图·图引用搬移（答案区装置图→题面）】",
    "题-QBY-03-09-Ineleganolide最":          " 【已修复 2026-10-11 · 吞图·图引用搬移（全合成路线→题面）】",
    "题-CM-63-03-二氧化钛除金红石外还有多种晶": " 【已修复 2026-10-11 · 吞图·图引用搬移（锐钛矿晶胞→题面）】",
    "题-CM-103-05-生物正交反应是在活细胞内进行": " 【已修复 2026-10-11 · 吞图·图引用搬移（Ru 催化循环→题面）】",
    "题-CM-138-09-观察下图所示合成路线并回答后": " 【已修复 2026-10-11 · 吞图·图引用搬移（合成路线→题面）＋删题面破碎 math 垃圾】",
    "题-HYS-03-04-甲烷单加氧酶MMO可在常温常":  " 【已修复 2026-10-11 · 吞图·图引用搬移（HL 配体→题面）＋删 OCR 碎片「NOH OH /」】",
}
FP = {
    "题-CM-12-07-71近年人们发现高压下可以制": " 【重判 2026-10-11 · 初筛假阳性：题面 L36 已含 HTML 表格图（方向/X/Y 投影 6 图，与答案区联图同内容）】",
    "题-CM-17-02-锂离子电池技术的进步极大地推": " 【重判 2026-10-11 · 初筛假阳性：题面 L43 已含 HTML 表格图（晶胞＋小立方体 A/B 3 图）】",
    "题-CM-95-08-利用大量可得的天然不对称化合": " 【重判 2026-10-11 · 初筛假阳性：题面已含 $$ 公式合成路线（与答案区图同路线）；是否图片化待 owner】",
    "题-UChO-02-06-下图为一种实验室制备水合茚三": " 【重判 2026-10-11 · 初筛假阳性：题面已含 $$ 公式合成路线（含用量）】",
}

rows = list(csv.reader(open(CSV, encoding="utf-8-sig", newline="")))
hdr, data = rows[0], rows[1:]
n_fix = n_fp = 0
for r in data:
    base = os.path.basename(r[0])[:-3]
    for k, v in FIXED.items():
        if base == k and "已修复" not in r[-1]:
            r[-1] += v; n_fix += 1; break
    else:
        for k, v in FP.items():
            if base == k and "重判" not in r[-1]:
                r[-1] += v; n_fp += 1; break
with open(CSV, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(data)
print("已修复标注 %d 行 ｜ 假阳性重判 %d 行" % (n_fix, n_fp))
for r in data:
    if "吞图·已目检" in r[-1] or "假阳性：题面" in r[-1]:
        print("   %s" % r[-1][:96])
