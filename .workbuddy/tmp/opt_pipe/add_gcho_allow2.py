# -*- coding: utf-8 -*-
"""add_gcho_allow2.py —— 为本轮改动的 GChO 卡登记 render_gate allowlist（统一理由）。"""
import glob, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)
F = "11-模板/scripts/render_gate_allowlist.txt"
REASON = ("2026-10-07 GChO 手写稿答案区由 OCR 文本改为**忠实裁图**（改用 PDF 文字层定位重裁），"
          "文字删除致 oMath 下降，属**预期删节**非渲染退化。")

st = subprocess.run(["git", "-c", "core.quotepath=false", "status", "--porcelain", "-uall",
                     "--", "04-题库/2026机构初赛模拟题/质心GChO"],
                    capture_output=True).stdout.decode("utf-8", "replace")
paths = [l[3:].strip().strip('"') for l in st.split("\n") if l.strip()]
print("本轮 GChO 改动卡 %d 张" % len(paths))

t = open(F, encoding="utf-8-sig").read().replace("\r\n", "\n")
if not t.endswith("\n"):
    t += "\n"
add = 0
for p in paths:
    key = p.replace("\\", "/") + "\t"
    if key in t:
        continue
    t += "%s\t%s\n" % (p.replace("\\", "/"), REASON)
    add += 1
open(F, "w", encoding="utf-8", newline="\n").write(t)
print("新增 allowlist %d 条；文件现有 %d 行" % (add, t.count("\n")))
