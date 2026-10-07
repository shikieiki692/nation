#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gcho_batch_apply.py —— 对全部手写届批量执行裁图治理（有 OCR 缓存者）。"""
import glob, importlib, os, re, sys, io, contextlib
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
GC = importlib.import_module("gcho_crop")

ANS = os.path.join(R, "06-外部资料导入/OCR/01-题目/质心合集新/GChO模拟试题合集答案")
rounds = sorted(int(re.search(r"GChO(\d+)解析手稿", os.path.basename(f)).group(1))
                for f in glob.glob(os.path.join(ANS, "ZCHEM-GChO*解析手稿.pdf")))
done, skip = 0, []
for rnd in rounds:
    cache = os.path.join(GC.LOC, "GChO%d.json" % rnd)
    if not os.path.exists(cache):
        skip.append(rnd); continue
    sys.argv = ["gcho_crop", "--round", str(rnd), "--apply"]
    try:
        GC.main()
        done += 1
    except Exception as e:
        print("届 %d 失败：%s" % (rnd, e))
print("\n完成 %d 届；无 OCR 跳过 %s" % (done, skip))
