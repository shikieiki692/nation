# -*- coding: utf-8 -*-
"""回滚：把 媒体仓库/_待清理/ 里的文件搬回原位（只读清单，逐条移动）"""
import json, shutil, sys
from pathlib import Path
VAULT = Path(r"C:\Obsidion\妙妙屋")
M = json.load(open(VAULT / ".workbuddy/tmp/img_audit/quarantine_manifest.json", encoding="utf-8"))
dry = (len(sys.argv) < 2 or sys.argv[1] != "run")
n = 0
for e in M:
    s, d = VAULT / e["dst"], VAULT / e["src"]
    if not s.exists():
        continue
    if not dry:
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(s), str(d))
    n += 1
print(("将回滚" if dry else "已回滚"), n, "个文件")
