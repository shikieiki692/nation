# -*- coding: utf-8 -*-
"""vol_poolchk.py —— 校验「计划锁内的卡是否仍在池」（**改完源卡后必跑**）。

【为什么】`build_org.load_plan_picks` 的规则是「计划内**任一张**不在池 ⇒ 整卷重选」
（`picks=None` ⇒ 回落到 `pick_vol` 重新选题）。改卡（格式/结构/标注）后若某张掉池，
再组卷就会**整卷换题**，而 stdout 只有一句 `⚠ 计划内卡不在池中`，极易被忽略
（2026-10-08 实测：`题-GChO-03-02` 因题面区生成「（N 分」被判题面泄露而掉池 ⇒ 卷 XII 十题全换）。

用法：python vol_poolchk.py --vol XII      # 有掉池 ⇒ 退出码 1
"""
import argparse
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp"))
import build_org as BO  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--vol", required=True)
A = ap.parse_args()

BO.ALL_YEARS = True
pool = BO.build_pool()
inpool = set()
for m in pool:
    for c in pool[m]:
        inpool.add(c["path"].replace("\\", "/"))

plan_p = os.path.join(R, ".workbuddy/tmp/opt_pipe", "vol_plan_%s.json" % A.vol)
plan = json.load(open(plan_p, encoding="utf-8"))
miss = []
for _mod, lst in plan:
    for c in lst:
        p = c["path"].replace("\\", "/")
        if p not in inpool:
            miss.append(p)
n = sum(len(l) for _, l in plan)
print("卷 %s：计划 %d 张 ｜ 池内 %d 张 ｜ **掉池 %d 张**" % (A.vol, n, len(inpool), len(miss)))
for p in miss:
    print("   ✗ 掉池:", p)
print("池规模:", {m: len(pool[m]) for m in pool})
if miss:
    print("\n⛔ 有卡掉池 ⇒ **禁止组卷**（会导致整卷重选）；先修卡或改计划锁。")
sys.exit(1 if miss else 0)
