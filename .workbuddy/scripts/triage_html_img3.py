# -*- coding: utf-8 -*-
"""定稿：库产物区 HTML <img> 的最终可修清单（basename 递归查 媒体仓库/）。"""
import os, io, re, collections

R = r"C:\Obsidion\妙妙屋"
SKIP = {".git", "媒体仓库", "_归档", ".workbuddy", "node_modules", "09-AI工作区"}
LIB = ("04-题库", "04-课件", "04-专题与题型", "03-知识点", "07-资料提炼",
       "13-教案", "06-学生侧材料", "12-教学洞察", "02-考纲条目", "01-考纲导航", "00-首页")
IMG = re.compile(r'<img[^>]*src="([^"]+)"')

# 媒体仓库 basename 索引（递归）
media = set()
for dp, dns, fns in os.walk(os.path.join(R, "媒体仓库")):
    for fn in fns:
        media.add(fn)
print("媒体仓库文件数(去重 basename):", len(media))

out = []
for dp, dns, fns in os.walk(R):
    dns[:] = [d for d in dns if d not in SKIP]
    for fn in fns:
        if not fn.endswith(".md"):
            continue
        p = os.path.join(dp, fn)
        try:
            t = io.open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        srcs = IMG.findall(t)
        if not srcs:
            continue
        rel = os.path.relpath(p, R).replace("\\", "/")
        fixable = miss = 0
        mlist = []
        for s in srcs:
            b = os.path.basename(s.replace("\\", "/"))
            if b in media:
                fixable += 1
            else:
                miss += 1
                mlist.append(b)
        out.append((rel, len(srcs), fixable, miss, mlist))

print()
print("=== 库产物区 ===")
t1 = t2 = t3 = 0
for rel, n, f, m, ml in sorted(out, key=lambda x: -x[2]):
    if rel.startswith(LIB):
        t1 += n
        t2 += f
        t3 += m
        tag = "✗缺图" if m else "可修"
        print(f"  {tag}  可修{f:3d} 缺{m:2d} 总{n:3d}  {rel}")
        if ml:
            print(f"          缺: {ml[:3]}")
print(f"  ── 库产物区：总 {t1} 处 / 可修 {t2} / 缺图 {t3}")

print()
print("=== 非库产物区（源料，仅汇总）===")
s = collections.Counter()
for rel, n, f, m, ml in out:
    if not rel.startswith(LIB):
        s["总"] += n
        s["可修"] += f
        s["缺"] += m
print(" ", dict(s))
