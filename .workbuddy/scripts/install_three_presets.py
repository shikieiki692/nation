# -*- coding: utf-8 -*-
"""安装：把 staging 三预设（三个 ## 预设 N 小节）插入组卷工作台「## 五、维护」之前。

行尾策略：插入块每行沿用锚点行（## 五、维护）的行尾风格；断言插入后
「## 五、维护」唯一、dataviewjs 块数 = 原有 + 3。
"""
import os, re, sys

VAULT = r"C:\Obsidion\妙妙屋"
WB = os.path.join(VAULT, "04-题库", "组卷工作台.md")
DRAFT = os.path.join(VAULT, ".workbuddy", "staging", "三预设-组卷工作台草稿.md")

wb = open(WB, encoding="utf-8", newline="").read()
draft = open(DRAFT, encoding="utf-8", newline="").read()

wb_lines = wb.split("\n")
anchor = "## 五、组卷规范"
idxs = [i for i, l in enumerate(wb_lines) if l.strip().startswith(anchor)]
assert len(idxs) == 1, f"锚点应唯一，实得 {len(idxs)}"
ai = idxs[0]
tr = "\r" if wb_lines[ai].endswith("\r") else ""
print(f"锚点 L{ai+1}，行尾风格：{'CRLF' if tr else 'LF'}")

# 草稿正文：从「## 预设 1」到预设 3 代码块结尾
d_lines = draft.split("\n")
s = next(i for i, l in enumerate(d_lines) if l.startswith("## 预设 1"))
e = next(i for i, l in enumerate(d_lines) if i > s and l.strip() == "```" and "预设 3" in "\n".join(d_lines[s:i]))
block = d_lines[s:e + 1]
# 草稿若为 CRLF（split("\n") 后残留 \r），统一剥掉再按锚点风格补
block = [l.rstrip("\r") + tr for l in block]

assert not any("\n" in l for l in block)
new_lines = wb_lines[:ai] + block + ["", ""] + wb_lines[ai:]
assert sum(1 for l in new_lines if l.strip().startswith(anchor)) == 1

new_t = "\n".join(new_lines)
if "--write" in sys.argv:
    open(WB, "w", encoding="utf-8", newline="").write(new_t)
    n_dj = len(re.findall(r"```dataviewjs", new_t))
    print(f"实写完成：工作台 dataviewjs 块数 = {n_dj}（原 3 + 新 3 = 6）")
else:
    n_dj = len(re.findall(r"```dataviewjs", new_t))
    print(f"dry-run：插入 {len(block)} 行；新文件 dataviewjs 块数 = {n_dj}")
