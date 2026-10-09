# -*- coding: utf-8 -*-
"""r8：两卷 OCR 误字修复（品→晶；1- 半径 → I⁻ 半径）。每处唯一命中断言 + 备份。"""
import os, shutil, datetime

Q = "04-题库/2026机构初赛模拟题"
BAK = ".workbuddy/tmp/opt_pipe/card_bak_r8"
os.makedirs(BAK, exist_ok=True)

EDITS = [
    # HZ-07-05：品胞参数 → 晶胞参数（题面 5-3）
    (f"{Q}/汇智/题-HZ-07-05-有机金属卤化物钙钛矿材料近几.md",
     "的品胞参数 a=8.8 Å，1-半径为 2.0 Å。不改变品胞参数的情况下",
     r"的晶胞参数 a=8.8 Å，$\mathrm{I}^{-}$ 半径为 2.0 Å。不改变晶胞参数的情况下",
     "HZ-07-05 品胞×2 + 1-半径→I⁻"),
    # YS-02-04：所属品系 → 所属晶系
    (f"{Q}/一式/题-YS-02-04-碳化物因碳的电负性适中而表现.md",
     "的所属品系。",
     "的所属晶系。",
     "YS-02-04 品系→晶系"),
]

apply_ = "--apply" in os.sys.argv
cache, ok = {}, True
for path, old, new, tag in EDITS:
    t = open(path, encoding="utf-8-sig").read()
    n = t.count(old)
    if n != 1:
        print("!! [%s] 命中 %d 次（应为 1）" % (tag, n))
        ok = False
        continue
    if old == new:
        print("!! [%s] old==new" % tag)
        ok = False
        continue
    print("OK [%s] %d→%d 字" % (tag, len(old), len(new)))
    cache[path] = t.replace(old, new, 1)

if not ok:
    print("存在失败项，未写盘")
    os.sys.exit(1)

if apply_:
    stamp = datetime.datetime.now().strftime("%m%d_%H%M")
    for path, body in cache.items():
        shutil.copy2(path, os.path.join(BAK, os.path.basename(path) + ".bak-" + stamp))
        open(path, "w", encoding="utf-8", newline="\n").write(body)
    print("已写盘 %d 个文件" % len(cache))
else:
    print("(dry) 待写盘 %d 个文件" % len(cache))
