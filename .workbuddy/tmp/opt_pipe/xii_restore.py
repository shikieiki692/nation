# -*- coding: utf-8 -*-
"""把 volpost 的 fmt 备份还原回源卡（用于带缺陷的规则回滚后重跑）。"""
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BAK = os.path.join(R, ".workbuddy/tmp/opt_pipe/volpost_bak_XII_fmt")
n = 0
for f in sorted(os.listdir(BAK)):
    rel = f.replace("__", "/")
    dst = os.path.join(R, rel)
    if not os.path.isfile(dst):
        print("  [目标缺失]", rel)
        continue
    shutil.copy2(os.path.join(BAK, f), dst)
    n += 1
    print("  还原 %s" % os.path.basename(rel)[:52])
print("还原 %d 张" % n)
