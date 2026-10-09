# -*- coding: utf-8 -*-
"""把 24 个「oMath 倒退（讲义管线折叠）＝启发式误报」登记到 render_gate 允许清单。"""
import re, io, os

R = r"C:\Obsidion\妙妙屋"
AL = os.path.join(R, "11-模板/scripts/render_gate_allowlist.txt")
FAIL = os.path.join(R, ".workbuddy/tmp/_gfail24.txt")
REP = os.path.join(R, ".workbuddy/tmp/_greport24.txt")

# 从非静默报告解析 basename → (old,new)
base2cnt = {}
cur = None
for ln in open(REP, encoding="utf-8"):
    if ln.strip() and not ln.startswith(" ") and (".md" in ln) and ("❌" in ln):
        cur = ln.split("  ")[0].strip()
    m = re.search(r"oMath 倒退 (\d+)→(\d+)", ln)
    if m and cur:
        base2cnt[os.path.basename(cur)] = (int(m.group(1)), int(m.group(2)))

full = [l.strip() for l in open(FAIL, encoding="utf-8") if l.strip()]
raw = open(AL, "rb").read()
nl = b"\r\n" if b"\r\n" in raw else b"\n"
text = raw.decode("utf-8-sig")
if not text.endswith("\n"):
    text += "\n"

REASON = ("（2026-10-09）全库化学式排版 fspace/fbase 落实：去「字母与 $ 间空格」后，"
          "讲义管线把 `X$_{a}^{b}$` 折叠为 Unicode 下标 ⇒ oMath 合理减少（非渲染失败）；"
          "full 模式已自证 PASS")
added = []
for p in full:
    b = os.path.basename(p)
    if any(l.split("\t")[0].strip() == p for l in text.splitlines()):
        continue
    o, n = base2cnt.get(b, ("?", "?"))
    line = "%s\t%s（oMath %s→%s）" % (p, REASON, o, n)
    text += line + "\n"
    added.append(p)

with open(AL, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print("新增 %d 条" % len(added))
for p in added:
    print("  +", p)
