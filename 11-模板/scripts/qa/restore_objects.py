# -*- coding: utf-8 -*-
"""从回收站恢复被 safe-delete 移走的 git 松散对象。

- 只写 `.git/objects/XX/YYY`（路径来自 $I 元数据，正则严格限定 38 位 hex）
- 已存在则不覆盖
- 默认 dry-run；--apply 才落盘
"""
import os, re, sys, glob, shutil
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"c:\Obsidion\妙妙屋")

APPLY = "--apply" in sys.argv
ROOT = r"C:\$Recycle.Bin\S-1-5-21-2139952663-2372964669-3439918837-1001"
OBJRE = re.compile(r"\.git\\objects\\([0-9a-fA-F]{2})\\([0-9a-fA-F]{38})")

ifs = sorted(glob.glob(os.path.join(ROOT, "$I*")))
print("扫描 $I 文件 %d 个" % len(ifs))

found = {}   # (sub, name) -> $I path
for p in ifs:
    try:
        b = open(p, "rb").read()
    except OSError:
        continue
    t = b[8:].decode("utf-16-le", errors="ignore")
    m = OBJRE.search(t)
    if not m:
        continue
    sub, name = m.group(1).lower(), m.group(2).lower()
    suffix = os.path.basename(p)[2:]
    rfile = os.path.join(ROOT, "$R" + suffix)
    if not os.path.exists(rfile):
        continue
    found[(sub, name)] = rfile

print("可恢复对象 %d 个" % len(found))

existed = missing_files = 0
todo = []
for (sub, name), rfile in found.items():
    dst = os.path.join(".git", "objects", sub, name)
    if os.path.exists(dst):
        existed += 1
        continue
    todo.append((rfile, dst))

print("已存在（跳过）%d；待恢复 %d" % (existed, len(todo)))

if not APPLY:
    print("\n[dry-run] 样例：")
    for r, d in todo[:5]:
        print("   %s  →  %s  (%d bytes)" % (os.path.basename(r), d, os.path.getsize(r)))
    print("\n加 --apply 执行。")
    sys.exit(0)

ok = 0
for r, d in todo:
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copyfile(r, d)
    ok += 1
print("\n已恢复 %d 个对象" % ok)
