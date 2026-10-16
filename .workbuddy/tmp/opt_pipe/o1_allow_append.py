# -*- coding: utf-8 -*-
"""向 render_gate 允许清单追加 O1 条目（LF 保尾，仅追加）。"""
import io, os

R = r"C:\Obsidion\妙妙屋"
p = os.path.join(R, "11-模板", "scripts", "render_gate_allowlist.txt")
line = ("04-题库/初赛模拟卷O1（有机·答案版）.md\t"
        "2026-10-16 答案区去「题面重述行」⇒ oMath 110→109（该句含 $CO_{2}$，"
        "同句在题面区第 185 行完好保留，属预期内容删除非渲染退化）；full 模式 PASS（109）\n")

raw = open(p, "rb").read()
assert b"\r\n" not in raw, "该文件为 LF，勿按 CRLF 写回"
if not raw.endswith(b"\n"):
    raw += b"\n"
if line.encode("utf-8") in raw:
    print("已存在，跳过")
else:
    with open(p, "ab") as fh:
        fh.write(line.encode("utf-8"))
    print("已追加")
print(open(p, encoding="utf-8").read().splitlines()[-1])
