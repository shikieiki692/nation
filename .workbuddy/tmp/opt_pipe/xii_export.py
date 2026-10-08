# -*- coding: utf-8 -*-
"""导出卷 XII 各题的题面与答案区全文（撰写解析用，只读）。"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
MD = os.path.join(R, "04-题库", "初赛模拟卷XII（非有机·答案版）.md")
t = io.open(MD, encoding="utf-8-sig").read().replace("\r\n", "\n")
blocks = list(re.finditer(r"(?m)^### 第 (\d+) 题[^\n]*\n", t))
LO, HI = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1, 10)
out = []
for k, b in enumerate(blocks):
    no = int(b.group(1))
    if not (LO <= no <= HI):
        continue
    s = b.end()
    e = blocks[k + 1].start() if k + 1 < len(blocks) else len(t)
    body = t[s:e]
    q = re.split(r"(?m)^#### 答案", body)[0]
    a = re.search(r"(?m)^#### 答案\s*\n(.*?)(?=^> —— 解析 ——|^---\s*$|\Z)", body, re.S)
    q = re.sub(r"\n{3,}", "\n\n", q).strip()
    an = re.sub(r"\n{3,}", "\n\n", a.group(1)).strip() if a else ""
    out.append("=" * 96)
    out.append("【第 %d 题】%s" % (no, t[b.start():b.end()].strip()))
    out.append("-" * 40 + " 题面 " + "-" * 40)
    out.append(q)
    out.append("-" * 40 + " 答案 " + "-" * 40)
    out.append(an)
p = os.path.join(R, ".workbuddy/tmp/opt_pipe/xii_export_%d_%d.txt" % (LO, HI))
io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("已导出 %s（%d 字）" % (p, len("\n".join(out))))
