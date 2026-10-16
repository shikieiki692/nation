# -*- coding: utf-8 -*-
r"""Q4 标签粘连修复（源号 + 年份被 OCR 粘连；同卷 X `md_patches`「类 B 连字符源号」缺陷）。

`4-1-12021 年` → `4-1-1 2021 年`；`4-32023 年` → `4-3 2023 年`（卷两版＋卡 GM-10-08）。
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Obsidion\妙妙屋")
PAIRS = [("4-1-12021 年", "4-1-1 2021 年"), ("4-32023 年", "4-3 2023 年")]
CP = [("8-1-12021 年", "8-1-1 2021 年"), ("8-32023 年", "8-3 2023 年")]
FILES = [
    ("04-题库/初赛模拟卷O2（有机·答案版）.md", PAIRS),
    ("04-题库/初赛模拟卷O2（有机·学生版）.md", PAIRS),
    ("04-题库/2026机构初赛模拟题/伽马/题-GM-10-08-8112021年Richmo.md", CP),
]
for p, pairs in FILES:
    with io.open(p, encoding="utf-8-sig", newline="") as fh:
        raw = fh.read()
    crlf = raw.count("\r\n")
    eol = "\r\n" if crlf * 2 > raw.count("\n") else "\n"
    t = raw.replace("\r\n", "\n")
    tot = 0
    for old, new in pairs:
        c = t.count(old)
        assert c >= 1, "%s 目标 %r 计数 %d" % (os.path.basename(p), old, c)
        t = t.replace(old, new)
        tot += c
    with io.open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(t.replace("\n", eol) if eol == "\r\n" else t)
    print("  [%s] %d 处；%d → %d 字节"
          % (os.path.basename(p)[:40], tot, len(raw.encode("utf-8")), len(t.encode("utf-8"))))
print("完成")
