# -*- coding: utf-8 -*-
"""回滚：把图片治理的各步改动**逆序**撤回（三类清单）。

设计原则：**每步独立可逆**，且**逆序**执行（后做的先撤），否则会互相覆盖。
  顺序（正）：欠曝增强 → 镜像翻转 → 子目录并入顶层 → 栅格化 SVG-in-.png → 灰底白化
  顺序（回滚）：灰底白化 → 栅格化 → 并入顶层 → 镜像翻转 → 欠曝增强

三类动作：
  ① 移动类（从图库移走 / 从子目录 moved）→ 按清单 move 回原位
  ② 覆盖类（原地覆盖修复）→ 从备份目录 copy 回原位
  ③ 栅格化类（多目录、异名备份）→ 按 item["path"] + `md5__name` 备份名还原
  ④ 源料侧镜像（`06-外部资料导入/` 下的同名副本）→ items 为路径列表，备份名 `<父目录名>__<原名>`

⚠️ 清单一律读**已入库**的 `scripts/` 版；`tmp/` 只是草稿区，换机后不可依赖。
⚠️ 干跑（默认）只报数，不动文件；确认后加 `run`。
"""
import json, shutil, sys
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
S = VAULT / ".workbuddy/scripts"
dry = (len(sys.argv) < 2 or sys.argv[1] != "run")
verb = "将回滚" if dry else "已回滚"

# ── ① 移动类：隔离区搬回 + 子目录并入顶层的反向移动 ────────────────────────────
MOVES = [
    (S / "img_quarantine_manifest.json", "隔离区搬回原位"),
    (S / "img_flatten_manifest.json", "子目录图片撤回子目录"),
]
for _man, _desc in MOVES:
    if not _man.exists():
        print(f"  [跳过] {_desc}：清单不存在 {_man.name}")
        continue
    m = json.load(open(_man, encoding="utf-8"))
    n = 0
    for e in m:
        s, d = VAULT / e["dst"], VAULT / e["src"]      # 现在在 dst，原在 src
        if not s.exists():
            continue
        if not dry:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(s), str(d))
        n += 1
    print(verb, n, f"个文件（{_desc}）  清单={_man.name}")

# ── ② 覆盖类：从备份目录 copy 回原位（逆序）──────────────────────────────────
OVERWRITE = [
    (S / "img_margin_manifest.json", "媒体仓库/_待清理/_白边原图", "白边裁切"),
    (S / "img_degray_manifest.json", "媒体仓库/_待清理/_灰底原图", "灰底白点拉伸"),
    (S / "img_mirror_manifest.json", "媒体仓库/_待清理/_镜像原图", "镜像水平翻转"),
    (S / "img_deexpose_manifest.json", "媒体仓库/_待清理/_欠曝原图", "欠曝对比度增强"),
]
for _man, _bakdir, _desc in OVERWRITE:
    if not _man.exists():
        print(f"  [跳过] {_desc}：清单不存在 {_man.name}")
        continue
    m = json.load(open(_man, encoding="utf-8"))
    bak = VAULT / _bakdir
    n = 0
    for e in m["items"]:
        b = bak / e["name"]
        d = VAULT / "媒体仓库" / e["name"]
        if not b.exists():
            continue
        if not dry:
            shutil.copy2(b, d)
        n += 1
    print(verb, n, f"个文件（{_desc}）  备份={_bakdir}")

# ── ③ 栅格化类：多目录 + 异名备份（<md5[:12]>__<原名>）────────────────────────
_man = S / "img_svg_raster_manifest.json"
if _man.exists():
    m = json.load(open(_man, encoding="utf-8"))
    bak = VAULT / m["backup_dir"]
    n = 0
    for e in m["items"]:
        b = bak / f'{e["md5_before"][:12]}__{Path(e["path"]).name}'
        d = VAULT / e["path"]
        if not b.exists():
            continue
        if not dry:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(b, d)
        n += 1
    print(verb, n, f'个文件（SVG 栅格化还原为原 .svg 内容）  备份={m["backup_dir"]}')
else:
    print("  [跳过] SVG 栅格化：清单不存在")

# ── ④ 源料侧镜像：items 是路径字符串，备份名 <父目录名>__<原名> ─────────────────
_man = S / "img_mirror_src_manifest.json"
if _man.exists():
    m = json.load(open(_man, encoding="utf-8"))
    bak = VAULT / m["backup_dir"]
    n = 0
    for rel in m["items"]:
        d = VAULT / rel
        b = bak / f"{Path(rel).parent.name}__{Path(rel).name}"
        if not b.exists():
            continue
        if not dry:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(b, d)
        n += 1
    print(verb, n, f'个文件（源料侧镜像翻转还原）  备份={m["backup_dir"]}')
else:
    print("  [跳过] 源料侧镜像：清单不存在")

if dry:
    print("\n（干跑）确认无误后加 run 执行；建议先跑一次 git status 看有无他人未提交改动。")
