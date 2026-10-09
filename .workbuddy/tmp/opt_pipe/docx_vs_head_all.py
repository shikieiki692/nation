# -*- coding: utf-8 -*-
"""逐 zip 条目比较 `00-首页/题组Word/初赛模拟卷/真题版式/*.docx` 与 HEAD 的差异。

输出：每个文件「有实质差异的条目清单」（忽略 docProps/core.xml 时间戳）。
用法：python docx_vs_head_all.py
"""
import io, os, subprocess, zipfile

D = "00-首页/题组Word/初赛模拟卷/真题版式"
IGNORE = {"docProps/core.xml", "docProps/app.xml"}

for name in sorted(os.listdir(D)):
    if not name.endswith(".docx"):
        continue
    p = f"{D}/{name}"
    cur = zipfile.ZipFile(p)
    r = subprocess.run(["git", "show", f"HEAD:{p}"], capture_output=True)
    if r.returncode != 0:
        print("%-46s 新文件" % name[:44]); continue
    old = zipfile.ZipFile(io.BytesIO(r.stdout))
    co, oo = set(cur.namelist()), set(old.namelist())
    diff = []
    for n in sorted(co & oo):
        if n in IGNORE:
            continue
        if cur.read(n) != old.read(n):
            diff.append(n)
    if co - oo:
        diff.append("仅新: %s" % sorted(co - oo)[:3])
    if oo - co:
        diff.append("仅旧: %s" % sorted(oo - co)[:3])
    print("%-46s %s" % (name[:44], diff if diff else "无"))
