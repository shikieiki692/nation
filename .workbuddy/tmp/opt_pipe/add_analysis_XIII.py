#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_analysis_XIII.py v3 —— 给卷 XIII 答案版逐题在答案区尾部追加**结构化详细解析**。

v3（2026-10-08，owner：「结合知识库内容仔细来写 + 排版美观」）：
  · 结构：**考点**（含所引知识点页名）／**思路**／**分步详解**／**易错**，各成独立引用段落；
  · 内容依据 03-知识点 的判据框架（Latimer 图电子数加权与歧化「右>左」判据、多重平衡 $K=K_{sp}\beta$、
    依数性与 Clapeyron 方程等）；数据文件 an13_data1.py / an13_data2.py。
  · 勘误：v2 第 5 题 5-2-2 电池电动势符号写反（应为 $\Delta G<0$、$\mathrm{V^{2+}}$ 不能稳定存在）。

幂等：答案版 md 已含「> **考点**」则跳过（需重写请先重出卷 md：build_org --apply）。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from an13_data1 import A1
from an13_data2 import A2

A = {}
A.update(A1)
A.update(A2)

R = r"C:\Obsidion\妙妙屋"
MD = os.path.join(R, "04-题库", "初赛模拟卷XIII（非有机·答案版）.md")


def block_of(qno):
    d = A[qno]
    out = ["> —— 解析 ——", ">"]          # ★ 以「—」开头 ⇒ 出卷器居中成横幅分隔
    out += ["> **考点**：" + d["考点"], ">"]
    out += ["> **思路**：" + d["思路"], ">"]
    for tag, score, txt in d["步骤"]:
        out += ["> **%s**（%s）%s" % (tag, score, txt), ">"]
    out += ["> **易错**：" + d["易错"], ""]
    return out


txt = open(MD, encoding="utf-8-sig").read().replace("\r\n", "\n")
if "> **考点**：" in txt:
    print("已存在结构化解析，跳过（如需重写请先重出卷 md）")
    sys.exit(0)
lines = txt.split("\n")
heads = [(i, int(m.group(1))) for i, l in enumerate(lines)
         for m in [re.match(r"^### 第 (\d+) 题", l)] if m]
heads.append((len(lines), None))
out, done = list(lines[:heads[0][0]]), 0
for k in range(len(heads) - 1):
    s, qno = heads[k]
    e = heads[k + 1][0]
    blk = lines[s:e]
    if qno in A:
        idx = [j for j, l in enumerate(blk) if l.strip() == "---"]
        if idx:
            pos = idx[-1]
            blk = blk[:pos] + block_of(qno) + blk[pos:]
            done += 1
    out += blk
txt2 = "\n".join(out)
open(MD, "w", encoding="utf-8", newline="\n").write(txt2)
print("已插入结构化解析 %d 题；文件 %d 字" % (done, len(txt2)))
