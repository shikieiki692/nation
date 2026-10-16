# -*- coding: utf-8 -*-
"""导出 O1 答案版卷 md 的「题面区」文本（每题：从 `### 第 N 题` 到 `#### 答案`），
图行折叠为 [图×k]，便于一次性通读 10 题。"""
import os, re, io

R = r"C:\Obsidion\妙妙屋"
md = os.path.join(R, "04-题库", "初赛模拟卷O1（有机·答案版）.md")
txt = open(md, encoding="utf-8-sig").read().replace("\r\n", "\n")
lines = txt.split("\n")

QN = re.compile(r"^### 第 (\d+) 题")
ANS = re.compile(r"^\s*####\s*答案")
IMG = re.compile(r"!\[\[")

cur = None
buf = {}
order = []
for ln in lines:
    m = QN.match(ln)
    if m:
        cur = int(m.group(1))
        if cur not in buf:
            buf[cur] = []
            order.append(cur)
        buf[cur].append(ln)
        continue
    if cur is None:
        continue
    if ANS.match(ln):
        cur = None
        continue
    if IMG.search(ln):
        n = len(IMG.findall(ln))
        buf[cur].append("[图×%d]" % n)
        continue
    buf[cur].append(ln)

out = []
for q in sorted(buf):
    body = "\n".join(buf[q])
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    # 折叠表格分隔行
    body = re.sub(r"(?m)^\|[:\-\s|]+\|$", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    out.append("========== 第 %d 题 ==========\n%s" % (q, body))

res = "\n\n".join(out)
op = os.path.join(R, ".workbuddy", "tmp", "opt_pipe", "o1_qtext.txt")
io.open(op, "w", encoding="utf-8").write(res)
print("写入", op, len(res), "字")
