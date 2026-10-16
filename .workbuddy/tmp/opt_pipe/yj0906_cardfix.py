# -*- coding: utf-8 -*-
"""源卡结构修复：题-YJ-09-06 答案区 HTML 表**缺 `<table>` 开头** ⇒ 补回。

根因链：
  L0 答案源 md 的该表为 3 列（首行 `<td colspan="3">第6题三钴碳化物簇(26分,占13%)`）；
  建卡时切片落在表内 ⇒ 卡内只剩 `<td …>…</td></tr>…</table>` 片段，**无 `<table>`**。
  ⇒ `build_org.html_table_to_md()` 的正则 `<table\b[^>]*>.*?</table>` 不匹配
  ⇒ 该表未被转成 md 管道表 ⇒ 字面 HTML 漏到卷 md（qa 闸门 ④「字面 <table>」报 1）。

修复：在片段起始处补 `<table><tr><td colspan="3">`（**最小结构修复**，
      不增删任何文字；标签文字沿用卡内既有 `三钴碳化物簇(26分,占13%)`）。
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)
P = "04-题库/2026机构初赛模拟题/壹尖培优/题-YJ-09-06-费托合成FischerTro.md"
BAK = ".workbuddy/tmp/opt_pipe/yj0906_card.bak.md"

with io.open(P, encoding="utf-8-sig", newline="") as fh:
    raw = fh.read()
crlf = raw.count("\r\n")
eol = "\r\n" if crlf * 2 > raw.count("\n") else "\n"
t = raw.replace("\r\n", "\n")
with io.open(BAK, "w", encoding="utf-8", newline="") as fh:
    fh.write(raw)
print("备份 →", BAK, "(%d 字节, EOL=%r)" % (len(raw.encode("utf-8")), eol))

assert "<table" not in t, "卡内已有 <table>，无需修复"
TGT = "三钴碳化物簇(26分,占13%)</td></tr>"
assert t.count(TGT) == 1, "目标串计数 %d（应 1）" % t.count(TGT)
NEW = "<table><tr><td colspan=\"3\">" + TGT
t = t.replace(TGT, NEW, 1)

# 结构自检：现在必须能匹配到完整 table 块，且块数 == 1
blocks = re.findall(r"<table\b[^>]*>.*?</table>", t, re.S)
assert len(blocks) == 1, "table 块数 %d（应 1）" % len(blocks)
# 标签平衡自检
assert blocks[0].count("<td") == blocks[0].count("</td>"), "td 标签不平衡"
assert blocks[0].count("<tr") == blocks[0].count("</tr>"), "tr 标签不平衡"
print("✔ 结构自检通过：1 个完整 table 块，td/tr 标签平衡；"
      "td=%d tr=%d" % (blocks[0].count("<td"), blocks[0].count("<tr")))

with io.open(P, "w", encoding="utf-8", newline="") as fh:
    fh.write(t.replace("\n", eol) if eol == "\r\n" else t)
print("已写盘，字节 %d → %d" % (len(raw.encode("utf-8")), len(t.encode("utf-8"))))

# ── 预览：走管线的 html_table_to_md 看现在会转成什么 ──────────────────────────
sys.argv = ["verify"]
sys.path.insert(0, os.path.join(".workbuddy", "tmp", "opt_pipe"))
import build_org as BO  # noqa: E402

i = t.find("## 参考答案")
ans = t[i:]
md = BO.html_table_to_md(ans)
md = re.sub(r'<img\s+[^>]*src="images/([^"]+)"[^>]*/?>', r"![[\1]]", md)
md = re.sub(r"\n{3,}", "\n\n", md)
print("\n===== html_table_to_md 产出预览 =====")
for l in md.split("\n"):
    print(repr(l)[:200])
