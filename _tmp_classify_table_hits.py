# Temporary classifier for `text-glued-to-table` candidates.
import re
from pathlib import Path

root = Path(r"C:\Obsidion\妙妙屋")
txt = (root / "_tmp_malformed_table_hits.txt").read_text(encoding="utf-8")
lines = [l for l in txt.splitlines() if l.strip()]
book_lines = [l for l in lines if "习题书-教师版" in l]


def looks_false(line: str) -> bool:
    s = line.split(":", 2)[2] if ":" in line else line
    if "|ρ|" in s or "\\left|" in s or "|\\omega|" in s:
        return True
    # Any $...$ segment containing a pipe (electrode cells, absolute values).
    segs = re.findall(r"\$[^$]*\$", s)
    if any("|" in seg for seg in segs):
        return True
    return False


real = [l for l in book_lines if not looks_false(l)]
print("book_hits", len(book_lines), "suspected_real", len(real))
for l in real:
    print(l)

(root / "_tmp_malformed_table_real.txt").write_text("\n".join(real) + "\n", encoding="utf-8")
