# -*- coding: utf-8 -*-
"""回滚今天的阶段测试卷产物：删 3 卷 + 移除 183 处 used_in"""
import io, os, re

ROOT = r"C:\Obsidion\妙妙屋\04-题库"
PAPERS = ["结构化学阶段测试卷", "有机化学阶段测试卷", "元素与分析阶段测试卷"]

# 1) 删卷
for pp in PAPERS:
    fp = os.path.join(ROOT, pp + ".md")
    if os.path.exists(fp):
        os.remove(fp)
        print("删除卷:", pp)

# 2) 移除 used_in 行
n = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in {"_归档", "_archive_v2",
                   "浙江卷2021", "浙江卷2022", "浙江卷2023"}]
    for f in filenames:
        if not f.endswith(".md"):
            continue
        p = os.path.join(dirpath, f)
        s = io.open(p, encoding="utf-8", newline="").read()
        if "used_in:" not in s:
            continue
        eol = "\r\n" if "\r\n" in s else "\n"
        lines = s.split(eol)
        out = [ln for ln in lines if not ln.strip().startswith("used_in:")]
        if len(out) != len(lines):
            io.open(p, "w", encoding="utf-8", newline="").write(eol.join(out))
            n += 1
print("used_in 移除:", n, "文件")
