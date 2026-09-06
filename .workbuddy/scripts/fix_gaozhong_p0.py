# -*- coding: utf-8 -*-
"""
03-知识点/高中化学基础 · P0 修复（无风险机械修正）
  1) 教师用书链接改名：[[必修1 Ch1 - 物质及其变化 教师用书提炼]] -> [[Ch1-物质及其变化]]
  2) 图片相对路径修正：../xxx / xxx -> ../../<vault 相对路径>
  3) 双链反斜杠分隔符 -> /

用法：
  python fix_gaozhong_p0.py            # 预演，只打印不落盘
  python fix_gaozhong_p0.py --apply    # 实际写入
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

VAULT = r"C:\Obsidion\妙妙屋"
TARGET = os.path.join(VAULT, "03-知识点", "高中化学基础")
TEACHER = os.path.join(VAULT, "07-资料提炼", "教师用书")

APPLY = "--apply" in sys.argv

# ---------- 素材 ----------
# 教师用书所有 md 的 basename 索引
teacher_idx = {}
for root, dirs, files in os.walk(TEACHER):
    for f in files:
        if f.endswith(".md"):
            teacher_idx.setdefault(f[:-3], []).append(os.path.join(root, f))

# 链接改名模板：[[必修1 Ch1 - 物质及其变化 教师用书提炼]]
TPL = re.compile(r"^\s*(必修\d|选修\d)\s+(Ch\d+)\s*-\s*(.+?)\s*教师用书提炼\s*$")
# 图片：![alt](path)
IMG = re.compile(r"(!\[[^\]]*\])\(([^)]+)\)")

stats = {"link": 0, "img": 0, "slash": 0, "file": 0}
unresolved = []
changes = []  # (file, kind, old, new)


def build_link_fix(target: str):
    """按模板推导正确链接名，命中教师用书实际文件才返回"""
    m = TPL.match(target)
    if not m:
        return None
    ch, name = m.group(2), m.group(3)
    cand = f"{ch}-{name.replace(' ', '')}"
    if cand in teacher_idx:
        return cand
    # 退一步：保留空格
    cand2 = f"{ch}-{name.strip()}"
    return cand2 if cand2 in teacher_idx else None


def rel_from_target(abs_path: str) -> str:
    """把 vault 绝对路径转成 高中化学基础/ 下的相对路径"""
    return "../../" + os.path.relpath(abs_path, VAULT).replace(os.sep, "/")


for fn in sorted(os.listdir(TARGET)):
    if not fn.endswith(".md"):
        continue
    fp = os.path.join(TARGET, fn)
    src = open(fp, encoding="utf-8").read()
    out = src

    # --- 1) 双链：反斜杠 -> 斜杠；教师用书改名 ---
    def wiki_sub(mo):
        bang = mo.group(1)
        inner = mo.group(2)
        new_inner = inner

        if "\\" in inner:
            new_inner = inner.replace("\\", "/")
            stats["slash"] += 1
            changes.append((fn, "分隔符", inner, new_inner))

        # 去掉前后空白再解析，保留可能存在的 #锚点 / |别名
        core = new_inner.strip()
        tgt_name = core.split("|")[0].split("#")[0].strip()
        fix = build_link_fix(tgt_name)
        if fix:
            new_inner = fix + core[len(tgt_name):]
            stats["link"] += 1
            changes.append((fn, "链接改名", tgt_name, fix))
        elif tgt_name.endswith("教师用书提炼"):
            unresolved.append((fn, tgt_name))

        return f"{bang}[[{new_inner}]]"

    out = re.sub(r"(!?)\[\[([^\]]+)\]\]", wiki_sub, out)

    # --- 2) 图片路径：统一为 ../../<vault 相对路径> ---
    def img_sub(mo):
        prefix, path = mo.group(1), mo.group(2).strip()
        if path.startswith(("http://", "https://", "data:")):
            return mo.group(0)
        p = path.replace("\\", "/").rstrip("/")
        # 剥掉前导 ../ 后在 vault 根下定位
        stripped = p
        while stripped.startswith("../"):
            stripped = stripped[3:]
        abs_p = os.path.normpath(os.path.join(VAULT, stripped))
        if not os.path.isfile(abs_p):
            unresolved.append((fn, path))
            return mo.group(0)
        new_path = rel_from_target(abs_p)
        if new_path != path:
            stats["img"] += 1
            changes.append((fn, "图片路径", path[:70], new_path[:70]))
        return f"{prefix}({new_path})"

    out = re.sub(IMG, img_sub, out)

    if out != src:
        stats["file"] += 1
        if APPLY:
            with open(fp, "w", encoding="utf-8", newline="") as fh:
                fh.write(out)

# ---------- 报告 ----------
print("=" * 70)
print("P0 修复" + ("（已应用）" if APPLY else "（预演，未落盘）"))
print("=" * 70)
print(f"改动文件数      : {stats['file']}")
print(f"教师用书链接改名: {stats['link']} 处")
print(f"图片路径修正    : {stats['img']} 处")
print(f"反斜杠分隔符修正: {stats['slash']} 处")
print(f"未能解析        : {len(unresolved)} 处")

if unresolved:
    print("\n--- 未能自动解析（需人工定夺，本次不动）---")
    for fn, t in unresolved:
        print(f"  {fn}  ->  {t[:90]}")

if not APPLY:
    print("\n--- 变更样例（前 25 条）---")
    for fn, kind, old, new in changes[:25]:
        print(f"  [{kind}] {fn}")
        print(f"      - {old}")
        print(f"      + {new}")
    print(f"\n（共 {len(changes)} 条变更，加 --apply 落盘）")
