# -*- coding: utf-8 -*-
"""命名规范修复（2026-08-31）：
1. 上海中学 127：题-{xxx}-{n}-上海中学-{主题}-习题{m} → 题-{xxx}-上海中学-{主题}-习题{m}
   （14 个冲突对：合规旧版已 deprecated，先删旧版再重命名新版）
2. 初赛讲义 11：题-初赛讲义-高分子化学简介-习题13.{10..20} → 题-{108..118}-... 
全程：先备份，全库 wikilink 引用替换，再重命名，最后更新 frontmatter title。"""
import json, re, os, sys
from pathlib import Path
from collections import defaultdict

VAULT = Path(r"C:/Obsidion/妙妙屋")
BACKUP = VAULT / "09-审计报告" / "备份" / "命名规范-2026-08-31"

# ── 1. 构建重命名映射 rel → new_rel ──────────────────────
rename: dict[str, str] = {}
deprecated_del: list[str] = []   # 14 个 deprecated 合规旧版，删除

sh_dir = VAULT / "04-题库/教材习题/上海中学竞赛课程"
for f in sorted(sh_dir.glob("*.md")):
    m = re.match(r"^(题-\d{3})-(\d+)-(上海中学-.+-习题\d+)$", f.stem)
    if m:
        new = f"{m.group(1)}-{m.group(3)}"
        rename[f"04-题库/教材习题/上海中学竞赛课程/{f.name}"] = \
            f"04-题库/教材习题/上海中学竞赛课程/{new}.md"
# 冲突对：合规名文件若存在且 deprecated → 删除；若存在但非 deprecated → 记冲突中止
for rel in list(rename.keys()):
    old_name = Path(rel).name
    new_stem = Path(rename[rel]).stem
    twin = sh_dir / f"{new_stem}.md"
    if twin.exists():
        txt = twin.read_text(encoding="utf-8", errors="replace")
        if "deprecated" in txt.split("---")[1][:400] if "---" in txt else False:
            deprecated_del.append(f"04-题库/教材习题/上海中学竞赛课程/{twin.name}")
        else:
            print(f"  ⚠ 冲突且非 deprecated，跳过: {twin.name}")

cz_dir = VAULT / "04-题库/教材习题/化学竞赛初赛讲义"
for i, f in enumerate(sorted(cz_dir.glob("题-初赛讲义-高分子*.md"))):
    num = 108 + i   # 13.10→108 ... 13.20→118
    m = re.match(r"^题-初赛讲义-(高分子化学简介-习题13\.\d+)$", f.stem)
    new = f"题-{num}-初赛讲义-{m.group(1)}"
    rename[f"04-题库/教材习题/化学竞赛初赛讲义/{f.name}"] = \
        f"04-题库/教材习题/化学竞赛初赛讲义/{new}.md"

print(f"重命名映射: {len(rename)}，deprecated 待删: {len(deprecated_del)}")

# ── 2. 备份 ───────────────────────────────────────────────
for rel in list(rename.keys()) + deprecated_del:
    src = VAULT / rel
    if src.exists():
        bak = BACKUP / rel
        bak.parent.mkdir(parents=True, exist_ok=True)
        bak.write_bytes(src.read_bytes())

# ── 3. 全库 wikilink 引用替换（旧stem → 新stem）──────────
old2new = {Path(k).stem: Path(v).stem for k, v in rename.items()}
# 长名优先，避免子串误替换
for old, new in old2new.items():
    if old == new:
        continue
    # 替换 [[前缀]旧stem]]/[[旧stem|alias]]/[[旧stem#锚]] 与 frontmatter 内同名引用
    pat = re.compile(r"(\[\[[^\]|#]*?)" + re.escape(old) + r"(?=\]\]|\||#)")
    hits = []
    for f in VAULT.rglob("*.md"):
        parts = set(f.parts)
        if parts & {".obsidian", ".git", "node_modules", "__pycache__", "09-AI工作区", ".chem_media"}:
            continue
        try:
            t = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if old in t:
            n, cnt = pat.subn(r"\1" + new, t)
            if cnt:
                f.write_text(n, encoding="utf-8")
                hits.append((str(f.relative_to(VAULT)), cnt))
    print(f"  [{old[:30]}...] → {new[:30]}  引用更新 {len(hits)} 文件")

# ── 4. 执行重命名 + 更新 title ───────────────────────────
for rel, new_rel in rename.items():
    src = VAULT / rel
    dst = VAULT / new_rel
    if dst.exists():
        print(f"  ⚠ 目标已存在，跳过: {new_rel}")
        continue
    src.rename(dst)
    # 更新 frontmatter title（若 title 与旧 stem 一致）
    try:
        txt = dst.read_text(encoding="utf-8")
        if f"title: {Path(rel).stem}" in txt or f'title: "{Path(rel).stem}"' in txt:
            txt2 = re.sub(r"(?m)^title:.*$", f'title: "{dst.stem}"', txt, count=1)
            dst.write_text(txt2, encoding="utf-8")
    except Exception as e:
        print(f"  ⚠ title 更新失败 {new_rel}: {e}")

# ── 5. 删除 deprecated 合规旧版（已备份）─────────────────
for rel in deprecated_del:
    p = VAULT / rel
    if p.exists():
        p.unlink()
        print(f"  🗑 删除 deprecated: {rel}")

print("完成。")
