# -*- coding: utf-8 -*-
"""移除本轮临时登记的 24 条 render_gate 白名单（根因已由 fbase 双上下标扩展修复）。"""
import os

R = r"C:\Obsidion\妙妙屋"
AL = os.path.join(R, "11-模板/scripts/render_gate_allowlist.txt")
FAIL = os.path.join(R, ".workbuddy/tmp/_gfail24.txt")

targets = {l.strip() for l in open(FAIL, encoding="utf-8") if l.strip()}
raw = open(AL, "rb").read()
nl = "\r\n" if b"\r\n" in raw else "\n"
lines = raw.decode("utf-8-sig").split("\n")
kept, removed = [], []
for ln in lines:
    key = ln.split("\t")[0].strip()
    if key and key in targets:
        removed.append(key)
    else:
        kept.append(ln)
out = "\n".join(kept)
if not out.endswith("\n"):
    out += "\n"
with open(AL, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)
print("移除 %d 条（原 %d 行 → 现 %d 行）" % (len(removed), len(lines), len(kept)))
miss = targets - set(removed)
if miss:
    print("!! 未找到:", sorted(miss)[:5])
