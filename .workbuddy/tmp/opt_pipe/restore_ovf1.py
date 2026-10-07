#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""restore_ovf1.py —— 把 round-1 rescue_ovf 改过的 51 张卡还原到「round-1 之前」的状态，
并先把当前（可能损坏的）版本另存到 ovf1_damaged/ 以便复核。"""
import glob, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/ovf_backup")
SAVE = os.path.join(R, ".workbuddy/tmp/opt_pipe/ovf1_damaged")
os.makedirs(SAVE, exist_ok=True)
n = miss = same = 0
for f in sorted(glob.glob(os.path.join(BK, "*.orig"))):
    bn = os.path.basename(f)[:-5]
    hits = glob.glob(os.path.join(R, "04-题库/2026机构初赛模拟题/**/") + bn, recursive=True)
    if not hits:
        print("！现文件缺失:", bn[:56]); miss += 1; continue
    p = hits[0]
    cur = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    old = open(f, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    if cur == old:
        same += 1; continue
    open(os.path.join(SAVE, bn + ".damaged"), "w", encoding="utf-8", newline="\n").write(cur)
    open(p, "w", encoding="utf-8", newline="\n").write(old)
    n += 1
print("还原 %d 张；未变 %d；缺失 %d" % (n, same, miss))
print("损坏版另存 → %s" % SAVE)
