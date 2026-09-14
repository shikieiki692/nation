# -*- coding: utf-8 -*-
"""扫描回收站 $I 元数据，找原始路径含 .git/objects 的条目。"""
import os, sys, glob, struct
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\$Recycle.Bin\S-1-5-21-2139952663-2372964669-3439918837-1001"
ifs = glob.glob(os.path.join(ROOT, "$I*"))
print("$I 元数据文件数:", len(ifs))

hit = []
paths = {}
for p in ifs[:4000]:
    try:
        b = open(p, "rb").read()
    except OSError:
        continue
    # Windows 10+ 格式：8字节头(版本+大小+时间) 后为 UTF-16LE 原始路径
    for enc in ("utf-16-le", "utf-8", "gbk"):
        try:
            t = b[8:].decode(enc, errors="ignore")
        except Exception:
            continue
        if "objects" in t or "\\" in t:
            t2 = t.replace("\x00", "").strip()
            if "objects" in t2:
                hit.append((p, t2))
                break
print("命中 .git/objects 的条目:", len(hit))
for p, t in hit[:8]:
    print("   %s" % t[:160])
