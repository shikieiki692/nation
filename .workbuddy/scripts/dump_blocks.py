"""按「建议分型」打印活跃源 md 中剩余代码块的完整内容（只读，用于定规则）。

用法：python dump_blocks.py 反应式 [文字型 ...]
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\Obsidion\妙妙屋")
SRC = ROOT / "04-课件" / "学生讲义"
EXCLUDED_STEMS = {"README"}
EXCLUDED_PREFIXES = ("讲义升级模式-",)

STRUCT = re.compile(r"[├└│─┌┐└┘]|━|\|")
FLOW = re.compile(r"→|—\w*[→>]|⟶")
RE_BOX = re.compile(r"[├└┌┐]")
RE_LINE = re.compile(r"[─━]|│")
RE_GEOM = re.compile(r"\\|/|—{2,}|={2,}")
RE_STEP = re.compile(r"(?m)^\s*(?:Step\s*\d|[①②③④⑤⑥⑦⑧⑨⑩]|\d+\s*[.、)])")
RE_ARROW = re.compile(r"→|⟶|—\w*[→>]")
RE_ALIGN = re.compile(r"\S {2,}\S")
OPEN_RE = re.compile(r"^((?:\s{0,3}>\s?)*\s{0,3})(`{3,}|~{3,})\s*(\S*)\s*$")


def strip_cr(s):
    return s[:-1] if s.endswith("\r") else s


def comment_mask(lines):
    mask, inside = [False] * len(lines), False
    for i, l in enumerate(lines):
        if inside:
            mask[i] = True
        j = 0
        while True:
            if not inside:
                k = l.find("<!--", j)
                if k < 0:
                    break
                e = l.find("-->", k + 4)
                if e < 0:
                    inside = True
                    break
                j = e + 3
            else:
                e = l.find("-->", j)
                if e < 0:
                    break
                inside = False
                j = e + 3
    return mask


def scan(lines, mask):
    out, i, n = [], 0, len(lines)
    while i < n:
        m = OPEN_RE.match(lines[i])
        if not m or mask[i]:
            i += 1
            continue
        fence = m.group(2)
        close_re = re.compile(r"^(?:\s{0,3}>\s?)*\s{0,3}"
                              + re.escape(fence[0]) + r"{%d,}\s*$" % len(fence))
        body, j = [], i + 1
        while j < n and not close_re.match(lines[j]):
            body.append(strip_cr(lines[j]))
            j += 1
        out.append((i + 1, (j + 1 if j < n else n), body))
        i = j + 1 if j < n else n
    return out


def suggest(body):
    txt = "\n".join(body)
    nl = len([l for l in body if l.strip()])
    if RE_BOX.search(txt):
        return "判断树"
    if RE_LINE.search(txt):
        return "结构图/连线"
    if nl >= 3 and RE_GEOM.search(txt):
        return "几何/结构式"
    if RE_STEP.search(txt):
        return "流程步骤"
    if RE_ARROW.search(txt) and nl <= 3:
        return "反应式"
    if nl >= 2 and len([l for l in body if RE_ALIGN.search(l)]) >= 2:
        return "数据/对齐表"
    return "文字型"


want = set(sys.argv[1:]) or {"反应式", "文字型", "数据/对齐表"}
src = ROOT / ".workbuddy" / "tmp" / "dump_out.txt"
buf = []
cnt = 0
for p in sorted(SRC.rglob("*.md")):
    rel = p.relative_to(SRC)
    if "_归档" in rel.parts or rel.parts[0].startswith("_"):
        continue
    if p.stem in EXCLUDED_STEMS or p.stem.startswith(EXCLUDED_PREFIXES):
        continue
    lines = p.read_text(encoding="utf-8").split("\n")
    mask = comment_mask(lines)
    for ol, cl, body in scan(lines, mask):
        nz = [x for x in body if x.strip()]
        if not nz:
            continue
        k = suggest(nz)
        if k not in want:
            continue
        cnt += 1
        buf.append("=" * 70)
        buf.append("[%03d] %s  L%d-%d  %s  (有效行 %d)"
                   % (cnt, rel.as_posix(), ol, cl, k, len(nz)))
        for x in nz[:14]:
            buf.append("    |" + x)
        if len(nz) > 14:
            buf.append("    ... 另 %d 行" % (len(nz) - 14))
        buf.append("")

src.write_text("\n".join(buf), encoding="utf-8")
print("已导出 %d 块 -> %s" % (cnt, src))
print("分型：", sorted(want))
