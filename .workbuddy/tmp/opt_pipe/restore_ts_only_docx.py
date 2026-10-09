# -*- coding: utf-8 -*-
"""把「仅有 docProps 时间戳差异」的交付件 docx 回滚到 HEAD（避免无意义提交）。"""
import io, os, subprocess, zipfile

D = "00-首页/题组Word/初赛模拟卷/真题版式"
IGNORE = {"docProps/core.xml", "docProps/app.xml"}
restore = []
for name in sorted(os.listdir(D)):
    if not name.endswith(".docx"):
        continue
    p = f"{D}/{name}"
    r = subprocess.run(["git", "show", f"HEAD:{p}"], capture_output=True)
    if r.returncode != 0:
        continue
    cur = zipfile.ZipFile(p)
    old = zipfile.ZipFile(io.BytesIO(r.stdout))
    diff = [n for n in sorted(set(cur.namelist()) & set(old.namelist()))
            if n not in IGNORE and cur.read(n) != old.read(n)]
    if not diff and not (set(cur.namelist()) ^ set(old.namelist())):
        restore.append(p)

print("待回滚（仅时间戳）：", len(restore))
for p in restore:
    print("  ", os.path.basename(p))
if "--apply" in os.sys.argv:
    for p in restore:
        subprocess.run(["git", "checkout", "HEAD", "--", p], check=True)
    print("已回滚", len(restore))
