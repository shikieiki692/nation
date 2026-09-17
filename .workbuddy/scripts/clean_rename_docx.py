# -*- coding: utf-8 -*-
"""清理 docx 输出目录的管线中间产物，并按 README 命名规范重命名 docx。

规范（00-首页/题组Word/README.md）：
  - 版本后缀一律连字符：`-教师版` / `-学生版`（禁全角括号）
  - 文件名禁中点 `·`
用法： python clean_rename_docx.py           # dry-run
       python clean_rename_docx.py --write
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
WRITE = "--write" in sys.argv
os.chdir(r"C:\Obsidion\妙妙屋")

DIRS = ["00-首页/题组Word/第一轮·竞赛教材版", "00-首页/题组Word/第一轮·综合套卷"]


def newname(stem: str) -> str:
    n = stem
    n = n.replace("（教师版）", "-教师版").replace("（学生版）", "-学生版")
    n = n.replace("·", "-")
    n = n.lstrip("_")          # __总索引 → 总索引
    n = n.replace("总索引", "总索引")
    return n


removed = 0
renames = []
fails = []
for d in DIRS:
    if not os.path.isdir(d):
        print("⚠ 目录不存在:", d)
        continue
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if not os.path.isfile(p):
            continue
        if f.endswith(".tmp.md"):
            if WRITE:
                for _ in range(5):
                    try:
                        os.remove(p)
                        removed += 1
                        break
                    except OSError as e:
                        last = e
                else:
                    fails.append((f, repr(last)))
            else:
                removed += 1
            continue
        if f.endswith(".docx"):
            stem, ext = os.path.splitext(f)
            nn = newname(stem) + ext
            if nn != f:
                renames.append((d, f, nn))

print("=== tmp 中间产物 ===")
print("  %s %d 个" % ("已删" if WRITE else "将删（dry-run）", removed))
print()
print("=== 待重命名 docx（%d 个）===" % len(renames))
seen = set()
for d, a, b in renames:
    key = (d, a)
    if key in seen:
        continue
    seen.add(key)
    if len(seen) <= 6 or len(seen) > len(renames) - 3:
        print("   %s\n     → %s" % (a, b))

if WRITE:
    done = 0
    for d, a, b in renames:
        pa, pb = os.path.join(d, a), os.path.join(d, b)
        if os.path.exists(pb):
            fails.append((a, "目标已存在 " + b))
            continue
        for _ in range(5):
            try:
                os.rename(pa, pb)
                done += 1
                break
            except OSError as e:
                last = e
        else:
            fails.append((a, repr(last)))
    print()
    print("已重命名 %d 个" % done)

if fails:
    print()
    print("⚠ 失败 %d 个:" % len(fails))
    for a, why in fails[:10]:
        print("   ", a, why)
