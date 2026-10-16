# -*- coding: utf-8 -*-
r"""扫卷 md 题面区「句中断行」—— 高信号判据（建卡期内容丢失的可疑点）。

判据：题面区（`### 第 N 题` → `#### 答案`）内的文本行
      ① 不以句末标点（。？！；：）」』"…）收尾
      ② 不是标题/表格/图/公式/引用行
      ③ 下一非空行为图或表格（说明该行被图/表截断）
⇒ 报为候选（**只筛值得看，终判人工逐字核对**）。
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Obsidion\妙妙屋")

END = "。？！；：）」』”\"…)]}"  # 视为「句末」的收尾字符
IMG = re.compile(r"^!\[\[[0-9a-f]{64}\.[A-Za-z0-9]+\]\]$")
TBL = re.compile(r"^[ \t]*\|")
f = sys.argv[1] if len(sys.argv) > 1 else "04-题库/初赛模拟卷O2（有机·学生版）.md"
with io.open(f, encoding="utf-8-sig", newline="") as fh:
    L = fh.read().replace("\r\n", "\n").split("\n")

cur = None
for i, l in enumerate(L):
    if l.startswith("### 第 "):
        cur = l[:40]
    if l.startswith("#### 答案"):
        cur = None
    if cur is None:
        continue
    s = l.rstrip()
    if not s or TBL.match(s) or IMG.match(s) or s.startswith(("#", ">", "$$", "$", "![")):
        continue
    if s[-1] in END:
        continue
    # 下一非空行
    j = i + 1
    while j < len(L) and not L[j].strip():
        j += 1
    nxt = L[j].strip() if j < len(L) else ""
    if IMG.match(nxt) or TBL.match(nxt):
        print("[%s] L%d (%d字) %s" % (cur, i + 1, len(s), s[:88]))
