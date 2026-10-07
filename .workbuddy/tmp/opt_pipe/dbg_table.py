#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dbg_table.py —— 打印 html_table_to_md 的中间 grid（诊断 CM-12-07 表）。"""
import glob, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe")
sys.argv = ["x", "--vol", "T", "--all-years"]
import build_org as BO

TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
TC = re.compile(r"<t[dh]([^>]*)>(.*?)</t[dh]>", re.S)
TB = re.compile(r"<table>.*?</table>", re.S)

fs = glob.glob("04-题库/2026机构初赛模拟题/chemy/题-CM-12-07-*.md", recursive=True)
c = BO.X.extract(fs[0])
tb = TB.findall(c["question"])[0]
print("表 %d 字" % len(tb))
grid, pending, rowspans = [], {}, []
for rm in TR.finditer(tb):
    row, col, sp = [], [0], []

    def fillp():
        while col[0] in pending:
            row.append('')
            pending[col[0]] -= 1
            if pending[col[0]] <= 0:
                del pending[col[0]]
            col[0] += 1
    fillp()
    for cm in TC.finditer(rm.group(1)):
        attrs, inner = cm.group(1), cm.group(2)
        csm = re.search(r'colspan\s*=\s*"?(\d+)"?', attrs)
        rsm = re.search(r'rowspan\s*=\s*"?(\d+)"?', attrs)
        cs = int(csm.group(1)) if csm else 1
        rs = int(rsm.group(1)) if rsm else 1
        sp.append((len(row), cs))
        row.append(BO._cell_clean(inner))
        row.extend([''] * (cs - 1))
        if rs > 1:
            for k in range(cs):
                pending[col[0] + k] = rs - 1
        col[0] += cs
        fillp()
    grid.append(row); rowspans.append(sp)
    print("  行%d 宽%d spans=%s" % (len(grid), len(row), sp))
    for j, cell in enumerate(row):
        print("      列%d: %r" % (j, cell[:60]))
print()
print("ncol =", max(len(r) for r in grid))
