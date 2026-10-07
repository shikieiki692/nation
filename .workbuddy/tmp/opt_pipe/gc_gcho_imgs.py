#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gc_gcho_imgs.py —— 回滚 GChO 卡（.orig）并回收「今日新建且无人引用」的裁图。"""
import glob, os, re, shutil, sys, time, datetime
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
GDIR = os.path.join(R, "04-题库/2026机构初赛模拟题/质心GChO")
IMGDIR = os.path.join(GDIR, "images")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/gcho_ans_backup")

mode = sys.argv[1] if len(sys.argv) > 1 else "gc"

if mode == "restore":
    n = 0
    for f in glob.glob(os.path.join(BK, "*.orig")):
        tgt = os.path.join(GDIR, os.path.basename(f)[:-5])
        shutil.copyfile(f, tgt); n += 1
    print("已回滚 %d 卡" % n)
else:
    # 收集所有被引用图名
    used = set()
    for p in glob.glob(os.path.join(GDIR, "**", "*.md"), recursive=True):
        t = open(p, encoding="utf-8-sig", errors="replace").read()
        used |= set(re.findall(r"!\[\]\(images/([^)]+)\)", t))
    today = datetime.date.today()
    removed, kept = 0, 0
    for f in glob.glob(os.path.join(IMGDIR, "*")):
        b = os.path.basename(f)
        if b in used:
            continue
        if datetime.date.fromtimestamp(os.path.getmtime(f)) != today:
            continue
        os.remove(f); removed += 1
    print("回收今日新建孤儿图 %d 张" % removed)
