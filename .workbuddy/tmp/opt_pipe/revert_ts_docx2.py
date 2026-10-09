# -*- coding: utf-8 -*-
"""回滚「仅时间戳」变化的交付 docx（zip 各条目内容与 HEAD 完全一致者）。"""
import io
import os
import subprocess
import zipfile

VAULT = r"C:\Obsidion\妙妙屋"
OUT = "00-首页/题组Word/初赛模拟卷/真题版式"


def run(a):
    return subprocess.run(a, cwd=VAULT, capture_output=True, text=True, encoding="utf-8")


def runb(a):
    return subprocess.run(a, cwd=VAULT, capture_output=True)


st = run(["git", "-c", "core.quotepath=false", "status", "--porcelain", "--", OUT + "/"]).stdout.splitlines()
paths = []
for ln in st:
    p = ln[3:].strip().strip('"')
    if p.endswith(".docx"):
        paths.append(p)

revert, keep = [], []
for p in paths:
    rb = runb(["git", "show", "HEAD:" + p])
    if rb.returncode != 0:
        keep.append((p, "NEW"))
        continue
    zn = zipfile.ZipFile(io.BytesIO(rb.stdout))
    zc = zipfile.ZipFile(os.path.join(VAULT, p))
    a = {n: zn.read(n) for n in zn.namelist()}
    b = {n: zc.read(n) for n in zc.namelist()}
    # 只看 word/ 下的内容条目（docProps/core.xml 是生成时间元数据，不算内容变化）
    keys = [k for k in a if k.startswith("word/")]
    changed = [k for k in keys if a.get(k) != b.get(k)]
    if set(a) == set(b) and not changed:
        revert.append(p)
    else:
        keep.append((p, changed or ["(manifest)"], [k for k in a if a.get(k) != b.get(k)]))

if "--apply" in os.sys.argv:
    for p in revert:
        run(["git", "checkout", "HEAD", "--", p])

print("保留（内容真变）%d：" % len(keep))
for p, d, meta in keep:
    print("   ", os.path.basename(p)[:50], d, ("｜仅元数据:" + ",".join(meta) if not d or d == ["(manifest)"] else ""))
print("回滚（仅时间戳）%d：%s" % (len(revert), "、".join(os.path.basename(x)[:22] for x in revert)))
