# -*- coding: utf-8 -*-
"""把 `card_bak_globalfmt/` 里的备份还原回 `04-题库/2026机构初赛模拟题/**/题-*.md`。

用途：全局 fmt 规则有缺陷时，先回滚再改规则重跑（保证最终态 = f(修正规则, 原始)）。
映射：按 basename 匹配（已核实 718 个备份无重名）。
用法：`python revert_global_fmt.py [--apply]`
"""
import os, sys, glob, shutil, collections

R = r"C:\Obsidion\妙妙屋"
Q = os.path.join(R, "04-题库/2026机构初赛模拟题")
BAK = os.path.join(R, ".workbuddy", "tmp", "opt_pipe", "card_bak_globalfmt")

bak_map = {}
for b in glob.glob(os.path.join(BAK, "*.bak-*")):
    key = os.path.basename(b).split(".bak-")[0]
    bak_map.setdefault(key, []).append(b)

dups = {k: v for k, v in bak_map.items() if len(v) > 1}
print("备份 %d 个（唯一名 %d；重名 %d）" % (sum(len(v) for v in bak_map.values()), len(bak_map), len(dups)))

apply_ = "--apply" in sys.argv
n = miss = 0
for fp in glob.glob(os.path.join(Q, "**", "题-*.md"), recursive=True):
    key = os.path.basename(fp)
    if key not in bak_map:
        continue
    src = sorted(bak_map[key])[0]
    if apply_:
        shutil.copy2(src, fp)
    n += 1
print("%s 还原 %d 个卡" % ("已写盘" if apply_ else "(dry)", n))
