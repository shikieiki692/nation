# Temporary audit: find source question lines where text runs straight into a
# pipe-table header (no newline), which pandoc cannot parse as a table.
import re
from pathlib import Path

root = Path(r"C:\Obsidion\妙妙屋")
scan_roots = [
    root / "04-题库" / "真题",
    root / "04-题库" / "教材习题",
    root / "04-题库" / "有机化学",
    root / "04-题库" / "分析化学",
    root / "04-题库" / "元素化学",
    root / "04-题库" / "物理化学",
    root / "04-题库" / "经典例题",
    root / "04-题库" / "教学改编题",
]

# A line that has a `|` not at the very start (after spaces), where the char
# before `|` is not one of the structural/math characters that routinely use
# pipes. Exclude wiki links and math-heavy lines.
glue = re.compile(r"[^ \t\r\n|\\\[\]<>\-_:;=,/]{1}[\|]")

hits = []
for base in scan_roots:
    if not base.exists():
        continue
    for p in base.rglob("*.md"):
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            if not glue.search(line):
                continue
            if line.lstrip().startswith("|"):
                continue
            if "[[" in line or "]]" in line:
                continue
            # Math delimiters: lines with $...$ containing pipes are cell
            # notation / abs values; keep them out unless the glue is outside
            # all math segments.
            math_segs = re.findall(r"\$[^$]*\$", line)
            stripped = line
            for seg in math_segs:
                stripped = stripped.replace(seg, "")
            if not glue.search(stripped):
                continue
            hits.append((p, i, line))

out = root / "_tmp_source_glue_hits.txt"
with out.open("w", encoding="utf-8") as fh:
    for p, i, line in hits:
        fh.write(f"{p.relative_to(root)}:{i}: {line}\n")
print("source_glue_hits", len(hits))
