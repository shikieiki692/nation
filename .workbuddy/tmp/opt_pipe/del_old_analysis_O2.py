# -*- coding: utf-8 -*-
r"""删除 O2 答案版卷 md 中所有题的旧「> —— 解析 ——」块（删到块尾下一个 `---` 前）。
幂等：已无旧块则报 0。"""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8")
MD = r"04-题库/初赛模拟卷O2（有机·答案版）.md"
txt = io.open(MD, encoding="utf-8-sig", newline="").read().replace("\r\n", "\n")
lines = txt.split("\n")
out, i, removed = [], 0, 0
while i < len(lines):
    if lines[i].strip() == "> —— 解析 ——":
        # 找到该题块内下一个独立的 `---` 行
        j = i + 1
        while j < len(lines) and lines[j].strip() != "---":
            j += 1
        if j >= len(lines):
            print("⛔ 未找到块尾 ---，中止（行 %d）" % (i + 1))
            sys.exit(1)
        removed += 1
        i = j  # 从 `---` 行继续（保留分隔线）
        continue
    out.append(lines[i])
    i += 1
io.open(MD, "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("已删除旧解析块 %d 个；剩余 `> **考点**` 行数 = %d" % (
    removed, sum(1 for l in out if l.strip().startswith("> **考点**"))))
