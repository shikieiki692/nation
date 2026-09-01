# -*- coding: utf-8 -*-
"""修复被截坏的 knowledge_points 行：按整行处理，还原为裸值 flow"""
import io, re

FILES = [
 r"C:\Obsidion\妙妙屋\07-资料提炼\书籍提炼\提炼-Clayden-第24章-区域选择性.md",
 r"C:\Obsidion\妙妙屋\07-资料提炼\书籍提炼\提炼-Clayden-第2章-有机结构.md",
 r"C:\Obsidion\妙妙屋\07-资料提炼\书籍提炼\提炼-Clayden-第37章-自由基反应.md",
 r"C:\Obsidion\妙妙屋\07-资料提炼\书籍提炼\提炼-Clayden-第41章-不对称合成.md",
 r"C:\Obsidion\妙妙屋\07-资料提炼\书籍提炼\提炼-Clayden-第7章-离域与共轭.md",
 r"C:\Obsidion\妙妙屋\07-资料提炼\网课资料\Zchem 基础有机化学\资料提炼-Zchem基础有机化学-批次Z-G-综合复习与例题.md",
]

for path in FILES:
    s = io.open(path, encoding="utf-8", newline="").read()
    eol = "\r\n" if "\r\n" in s else "\n"
    lines = s.split(eol)
    idx = next(i for i, ln in enumerate(lines) if ln.startswith("knowledge_points:"))
    raw = lines[idx][len("knowledge_points:"):].strip()
    raw = raw.lstrip("[").rstrip("]")
    vals = []
    for tok in raw.split(","):
        v = re.sub(r'[\[\]"\' ]', '', tok)
        if v:
            vals.append(v)
    lines[idx] = "knowledge_points: [" + ", ".join(vals) + "]"
    io.open(path, "w", encoding="utf-8", newline="").write(eol.join(lines))
    print("修复 %d 项: %s" % (len(vals), path.rsplit(chr(92), 1)[-1]))
    print("   ", lines[idx][:200])
