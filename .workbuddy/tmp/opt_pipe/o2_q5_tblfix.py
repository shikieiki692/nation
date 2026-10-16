# -*- coding: utf-8 -*-
"""O2 答案卷 Q5 答案区：**残破 HTML 碎片 → 3 列 md 管道表**（零文字改动）。

背景：源卡 `题-YJ-09-06` 的答案表缺 `<table>` 开头（已另行修复源卡），
      故建卷期 `html_table_to_md()` 未匹配 ⇒ 字面 HTML 碎片漏进卷 md（qa ④ 报 1 项）。
      卷 md 已含全部文字与图（未被丢弃），只是**结构**是碎片 ⇒ 本脚本只重排结构。

手法：从原文按「标签边界」切出 token 序列，**逐项断言**后按已知表结构重排。
      ⇒ 任何文字/图丢失或顺序变化都会触发断言失败。
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)
P = "04-题库/初赛模拟卷O2（有机·答案版）.md"

with io.open(P, encoding="utf-8-sig", newline="") as fh:
    raw = fh.read()
crlf = raw.count("\r\n")
eol = "\r\n" if crlf * 2 > raw.count("\n") else "\n"
lines = raw.replace("\r\n", "\n").split("\n")
print("EOL=%r 行数=%d" % (eol, len(lines)))

# ── 定位区域 ─────────────────────────────────────────────────────────────────
st = [i for i, l in enumerate(lines) if "三钴碳化物簇(26分,占13%)</td></tr>" in l]
en = [i for i, l in enumerate(lines) if l.rstrip().endswith("</table>")]
assert len(st) == 1, "起始行计数 %d" % len(st)
assert len(en) == 1, "结束行计数 %d" % len(en)
s, e = st[0], en[0]
assert s < e
region = lines[s:e + 1]
before = "\n".join(region)
print("区域 L%d..L%d（%d 行，%d 字符）" % (s + 1, e + 1, len(region), len(before)))

# ── 切 token（逐行 → 按 HTML 标签切，空行不产生 token）──────────────────────
TAG = re.compile(r"</?(?:table|tr|t[dh])\b[^>]*>", re.I)
toks = []
for ln in region:
    for piece in TAG.split(ln):
        p = piece.strip()
        if p:
            toks.append(p)
print("token 数 = %d" % len(toks))
for i, tk in enumerate(toks):
    print("  [%2d] %s" % (i, tk[:110]))

# ── 断言 token 序列 == 预期（防丢字/乱序）──────────────────────────────────
IMG = re.compile(r"^!\[\[([0-9a-f]{8})[0-9a-f]*\.jpg\]\]$")
exp_img = ["5159bec0", "a522e918", "50802ae4", "5d5e2b3a",
           "40469e2e", "217774ee", "99e02b86", "4913da2e"]
got_img = [IMG.match(t).group(1) for t in toks if IMG.match(t)]
assert got_img == exp_img, "图序列不符:\n got=%s\n exp=%s" % (got_img, exp_img)

LAB = ["三钴碳化物簇(26分,占13%)", "5-1共2分", "5-2共3分", "5-3-1共4分", "P", "Q",
       "5-3-2共2分", "5-4-1共3分", "5-4-2共9分", "A", "B", "C"]
for x in LAB:
    assert x in toks, "缺 token: %r" % x
assert len(toks) == 30, "token 数 %d（预期 30）" % len(toks)

# ── 按已知结构重排（全部取自 toks，不改字）──────────────────────────────────
i = 0


def take():
    global i
    v = toks[i]
    i += 1
    return v


label = take()
assert label == LAB[0]
r_51 = [take(), take(), ""]                      # 5-1共2分 | <式>(2分) | ""
r_52 = [take(), "%s %s" % (take(), take()), ""]  # 5-2共3分 | ![[..]] (3分) |
r_531 = [take(), "%s %s" % (take(), take()), "%s %s" % (take(), take())]
r_pq = ["", take(), take()]                      #  | P | Q
r_532 = [take(), "%s %s" % (take(), take()), ""]
r_541 = [take(), "%s %s" % (take(), take()), ""]
r_542 = [take(), "%s %s" % (take(), take()), "%s %s" % (take(), take())]
r_ab = ["", take(), take()]                      #  | A | B
r_x = ["", "%s %s" % (take(), take()), take()]   #  | ![[..]] (3分,..) | 共9分。
r_c = ["", take(), ""]                           #  | C |
assert i == len(toks), "未消费完：剩 %d" % (len(toks) - i)

rows = [r_51, r_52, r_531, r_pq, r_532, r_541, r_542, r_ab, r_x, r_c]
new_tbl = ["| %s |  |  |" % label, "| :---: | :---: | :---: |"]
for r in rows:
    assert len(r) == 3
    new_tbl.append("| %s | %s | %s |" % tuple(r))

# ── 守恒自检 ─────────────────────────────────────────────────────────────────
after = "\n".join(new_tbl)
assert not TAG.search(after), "仍有 HTML 标签"
ai = re.findall(r"!\[\[([0-9a-f]{8})[0-9a-f]*\.jpg\]\]", after)
assert ai == exp_img, "图不守恒 %s" % ai
# 非图非标签文字必须逐字保留
b_txt = sorted(x for x in toks if not IMG.match(x))
a_txt = sorted(re.findall(r"[^|!\[\]|<>\n][^|\n]*?(?=\s*\||\s*$)", after))
# 简化核对：每个原 token（非图）都要出现在新表内
for x in b_txt:
    assert x in after, "文字丢失: %r" % x
print("\n✔ 守恒自检通过：图 %d/8、token 全保留、无 HTML 残留" % len(ai))

print("\n===== 新表 =====")
for l in new_tbl:
    print(l[:200])

lines[s:e + 1] = new_tbl
out = eol.join(lines)
assert out != raw
with io.open(P, "w", encoding="utf-8", newline="") as fh:
    fh.write(out)
print("\n已写盘：字节 %d → %d" % (len(raw.encode("utf-8")), len(out.encode("utf-8"))))
