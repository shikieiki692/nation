# -*- coding: utf-8 -*-
"""O2 答案卷 md 表格结构最小修补（两处）。

根因：
  ① L88-90 是 3 列表，尾行图案行只有 2 格 ⇒ `layout_figs.render_block` 未补齐
     （工具已修，此处补卷 md）；
  ② L822-832 是「2 列表 + 4 列表」被**并成一个块**（缺空行）⇒ pandoc 以 2 列
     分隔行为准 ⇒ 后两列图（7ba55bf1／2894ff33／46f3da73）落不了 docx。
     ⇒ 只需在两张表之间补一个空行。

约束：精确匹配 + 计数断言 + 保 EOL（文件自身 EOL）+ 幂等。
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)
P = "04-题库/初赛模拟卷O2（有机·答案版）.md"

with io.open(P, encoding="utf-8-sig", newline="") as fh:
    raw = fh.read()
crlf = raw.count("\r\n")
lfonly = raw.count("\n") - crlf
eol = "\r\n" if crlf > lfonly else "\n"
print("EOL: CRLF=%d LF-only=%d ⇒ 用 %r" % (crlf, lfonly, eol))

lines = raw.replace("\r\n", "\n").split("\n")

# ── ① 尾行补齐 ────────────────────────────────────────────────────────────────
i1 = None
for i, l in enumerate(lines):
    if l.startswith("| ![[5dfa2765") and l.rstrip().endswith("|"):
        i1 = i
        break
assert i1 is not None, "① 未找到 5dfa2765 行"
old1 = lines[i1]
assert old1.count("![[") == 2, "① 期望 2 图: %r" % old1
new1 = old1.rstrip() + "  |"
lines[i1] = new1
print("① 行%d\n   旧: %r\n   新: %r" % (i1 + 1, old1, new1))

# ── ② 两表之间补空行 ──────────────────────────────────────────────────────────
i2 = None
for i, l in enumerate(lines):
    if l.startswith("| ![[1a019e6d"):
        i2 = i
        break
assert i2 is not None, "② 未找到 1a019e6d 行"
nxt = lines[i2 + 1]
assert nxt.startswith("|") and "9-2-1" in nxt, "② 下一行非 4 列表头: %r" % nxt
assert not nxt.strip().startswith("\n"), nxt
lines[i2 + 1:i2 + 1] = [""]  # 插入空行
print("② 在行%d（%r）之后插入空行；其下为 %r" % (i2 + 1, lines[i2], lines[i2 + 2]))

out = eol.join(lines)
assert out != raw
with io.open(P, "w", encoding="utf-8", newline="") as fh:
    fh.write(out)
print("已写盘，字节 %d → %d" % (len(raw.encode('utf-8')), len(out.encode('utf-8'))))
