# -*- coding: utf-8 -*-
r"""O2 答案版 Q7 答案区：删除残缺引用块（残渣）＋ 修 2 处粘连/缺标。

现状：
  L602-632 ＝ `> 源：…` 起的 29 行**引用块**，内容与下方「清理后答案」**重复**且含碎片行
  （`> 示。` / `> 移程度大于B。` / `> 方式。` 等）；全卷仅此 1 处、O1 卷 0 处 ⇒ 系 `--ans` 时代残渣。
  其中**唯一独有信息＝`> 杂化为sp3 杂化`（7-6 的答案）**，须保留。
另两处：
  · `**7-4** ABCED中错误之处…` ⇒ `ABCE` 与 `D 中错误…` 粘连（源为两条）⇒ 插分隔；
  · `7-6 ![[…]]` ⇒ 缺 `**7-6**` 标（且 7-6 的 sp3 文字只在引用块里）。
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Obsidion\妙妙屋")
P = "04-题库/初赛模拟卷O2（有机·答案版）.md"

with io.open(P, encoding="utf-8-sig", newline="") as fh:
    raw = fh.read()
crlf = raw.count("\r\n")
eol = "\r\n" if crlf * 2 > raw.count("\n") else "\n"
L = raw.replace("\r\n", "\n").split("\n")

# ── ① 定位并删除引用块 ───────────────────────────────────────────────────────
a = [i for i, l in enumerate(L) if l.startswith("> 源：`2026年清北营寒假班-试卷1-参考答案")]
assert len(a) == 1, "引用块起点计数 %d" % len(a)
s = a[0]
e = next(i for i in range(s, len(L)) if not L[i].startswith(">"))
assert e is not None and L[e - 1].startswith("> 参考结构"), "块尾异常: %r" % L[e - 1]
# 块内不含非引用内容
blk = L[s:e]
assert all(l.startswith(">") or not l.strip() for l in blk), "块内含非引用行"
n_quote = len(blk)
print("① 引用块 L%d..L%d（%d 行）将删除" % (s + 1, e, n_quote))

# ── ② 抽出唯一独有信息 ──────────────────────────────────────────────────────
assert any(l.strip() == "> 杂化为sp3 杂化" for l in blk), "块内未见 sp3 一行"

# ── ③ 修 7-4 粘连 ───────────────────────────────────────────────────────────
g = [i for i, l in enumerate(L) if l.startswith("**7-4** ABCED中错误之处")]
assert len(g) == 1, "7-4 行计数 %d" % len(g)
old74 = L[g[0]]
L[g[0]] = old74.replace("**7-4** ABCED中错误之处", "**7-4** ABCE　D 中错误之处")
print("③ 7-4: %r → %r" % (old74[:40], L[g[0]][:48]))

# ── ④ 修 7-6 缺标补 sp3 ─────────────────────────────────────────────────────
h = [i for i, l in enumerate(L) if re.match(r"^7-6 !\[\[[0-9a-f]{64}\.jpg\]\]$", l)]
assert len(h) == 1, "7-6 行计数 %d" % len(h)
old76 = L[h[0]]
L[h[0]] = old76.replace("7-6 ", "**7-6** 杂化为sp3 杂化　", 1)
print("④ 7-6: %r → %r" % (old76[:34], L[h[0]][:52]))

# ── 执行删除（在最后，避免索引偏移）────────────────────────────────────────
del L[s:e]

# ── 自检 ────────────────────────────────────────────────────────────────────
out = eol.join(L)
assert "> 源：`2026年清北营寒假班" not in out
assert "杂化为sp3 杂化" in out
assert "**7-4** ABCE　D 中错误之处" in out
assert "**7-6** 杂化为sp3 杂化" in out
print("自检通过；%d → %d 字节" % (len(raw.encode("utf-8")), len(out.encode("utf-8"))))
with io.open(P, "w", encoding="utf-8", newline="") as fh:
    fh.write(out)
print("已写盘")
