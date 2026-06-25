"""
Clean up inline answers from 课堂填空版 handouts.
Two patterns:
1) (答案：...) lines - single or multi-line, remove entirely
2) **答案速查** answer tables - remove header + answer table
"""
import re
import os

HANDOUTS_DIR = r"C:\Obsidion\妙妙屋\04-课件\学生讲义"

handouts = [
    "原子结构-超级充实版（课堂填空）.md",
    "元素周期表与周期律-超级充实版（课堂填空）.md",
    "分子结构基础-超级充实版（课堂填空）.md",
]

for fname in handouts:
    fpath = os.path.join(HANDOUTS_DIR, fname)
    if not os.path.exists(fpath):
        print(f"[SKIP] {fname} not found")
        continue

    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    original_text = "".join(lines)
    new_lines = []
    i = 0
    removed_answers = 0
    removed_tables = 0

    while i < len(lines):
        line = lines[i]

        # Pattern 1: Line starting with （答案：...）
        # Single-line: （答案：...）
        if line.strip().startswith("（答案：") or line.strip().startswith("(答案："):
            # Skip this line and any continuation lines
            # These answers may contain ）inside math expressions
            # So we match from （答案： to the last ）followed by blank line or end
            removed_answers += 1
            i += 1
            # Check if next lines are continuation (no blank line between)
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line == "" or next_line.startswith("---"):
                    break
                # Check if this continuation line is still the answer
                # (indented or part of same paragraph)
                if next_line.endswith("）") or next_line.endswith(")"):
                    # This might be the end of multi-line answer
                    # But only skip if it's not the start of a new section
                    if not next_line.startswith("#") and not next_line.startswith(">"):
                        i += 1
                        break
                    break
                i += 1
            continue

        # Pattern 2: **答案速查** line followed by answer table
        if line.strip().startswith("**答案速查**"):
            removed_tables += 1
            i += 1  # Skip the header
            # Skip blank lines after header
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            # Skip table rows (lines starting with |)
            while i < len(lines) and lines[i].strip().startswith("|"):
                i += 1
            # Skip trailing blank lines after table
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            continue

        # Normal line - keep it
        new_lines.append(line)
        i += 1

    new_text = "".join(new_lines)

    if new_text != original_text:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_text)
        print(f"[OK] {fname}: removed {removed_answers} inline answers, {removed_tables} answer tables")
    else:
        print(f"[=] {fname}: no changes")
