# -*- coding: utf-8 -*-
"""回滚：把 媒体仓库/_待清理/ 里的文件搬回原位（只读清单，逐条移动）"""
import json, shutil, sys
from pathlib import Path
VAULT = Path(r"C:\Obsidion\妙妙屋")
# ⚠️ 清单必须读**已入库**的那份（scripts/ 下）；草稿区的 tmp/ 不入库，换机后回滚会失效
MANIFEST = VAULT / ".workbuddy/scripts/img_quarantine_manifest.json"
if not MANIFEST.exists():
    MANIFEST = VAULT / ".workbuddy/tmp/img_audit/quarantine_manifest.json"
M = json.load(open(MANIFEST, encoding="utf-8"))
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
print(("将回滚" if dry else "已回滚"), n, "个文件  清单=", MANIFEST.name)
