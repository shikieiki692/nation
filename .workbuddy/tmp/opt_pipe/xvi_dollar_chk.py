# -*- coding: utf-8 -*-
"""判据 23 扫描：闭合 $ 不得紧跟数字（针对卷 md 解析注入区）。"""
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8")
t = io.open(r"04-题库/初赛模拟卷XVI（非有机·答案版）.md", encoding="utf-8-sig").read()
lines = t.split("\n")
# 解析块定位：从「> —— 解析 ——」到下一个「---」
blocks, cur = [], None
for idx, ln in enumerate(lines):
    if ln.strip().startswith("> —— 解析 ——"):
        cur = idx
    elif cur is not None and ln.strip() == "---":
        blocks.append((cur, idx))
        cur = None
print("解析块数:", len(blocks))
bad = 0
for (a, b) in blocks:
    for i in range(a, b + 1):
        ln = lines[i]
        # 逐字符统计未转义 $ 的奇偶
        cnt = 0
        j = 0
        while j < len(ln):
            c = ln[j]
            if c == "\\":
                j += 2
                continue
            if c == "$":
                cnt += 1
                nxt = ln[j + 1] if j + 1 < len(ln) else ""
                if cnt % 2 == 0 and nxt.isdigit():  # 闭合$紧跟数字
                    print("L%d: ...%s..." % (i + 1, ln[max(0, j - 30):j + 12]))
                    bad += 1
            j += 1
print("闭合$紧跟数字:", bad)
