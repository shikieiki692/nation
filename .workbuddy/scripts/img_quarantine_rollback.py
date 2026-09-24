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

# ── 第二类：原位覆盖类修复的回滚（欠曝增强 / 镜像翻转）──────────────────────────
# 与上面的「移动类隔离」不同：这两类是**原地覆盖**，回滚 = 把备份里的原图**复制回原位**。
# 顺序有意义：镜像翻转在欠曝增强**之后**做 ⇒ 回滚要**逆序**（先撤翻转，再撤增强）。
OVERWRITE = [
    # (清单, 备份目录, 说明)  —— 逆序回滚
    (VAULT / ".workbuddy/scripts/img_mirror_manifest.json",
     "媒体仓库/_待清理/_镜像原图", "镜像翻转（水平翻转）"),
    (VAULT / ".workbuddy/scripts/img_deexpose_manifest.json",
     "媒体仓库/_待清理/_欠曝原图", "欠曝对比度增强"),
]
for _man, _bakdir, _desc in OVERWRITE:
    if not _man.exists():
        print(f"  [跳过] {_desc}：清单不存在 {_man.name}")
        continue
    _m = json.load(open(_man, encoding="utf-8"))
    _bak = VAULT / _bakdir
    _n = 0
    for e in _m["items"]:
        b = _bak / e["name"]
        d = VAULT / "媒体仓库" / e["name"]
        if not b.exists():
            continue
        if not dry:
            shutil.copy2(b, d)
        _n += 1
    print(("将回滚" if dry else "已回滚"), _n, f"个文件（{_desc}）  备份={_bakdir}")

