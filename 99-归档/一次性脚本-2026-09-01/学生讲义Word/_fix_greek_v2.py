#!/usr/bin/env python3
"""
More thorough Greek letter wrapping.
Strategy: Process line by line, protect math blocks, then wrap ALL bare Greek letters.
"""

import re

FILE = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（完整版）.md"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Greek letters to wrap
GREEK = r'[σπΔδλμχθρψωαβγεηικνξζφ]'

# Step 1: Fix double-$ issues from previous script
# Pattern: $$X$ where X is a Greek letter → should be $X$
content = re.sub(r'\$\$([' + GREEK[1:-1] + r'])\$', r'$\1$', content)
# Also fix: $$σ$_{2}$$s^{2}$ → $σ_{2}s^{2}$ (these were originally like $σ_{2}s^{2}$)
content = re.sub(r'\$\$([' + GREEK[1:-1] + r'])(\$\$[^$]+\$\$)', r'$\1\2', content)

# Step 2: Protect all math blocks with placeholders
math_store = []
def save_math(m):
    idx = len(math_store)
    math_store.append(m.group(0))
    return f"§M{idx}§"

# Protect $$...$$ first (display math)
protected = re.sub(r'\$\$[^$]+\$\$', save_math, content)
# Protect $...$ (inline math)
protected = re.sub(r'\$[^$\n]+\$', save_math, protected)

# Step 3: Wrap ALL remaining bare Greek letters
# Match Greek letter not inside a word (not preceded/followed by alphanumeric)
# But allow next to special chars like *, ), (, -, →, etc.
pattern = r'(?<!\$)(?<!\\)(' + GREEK + r')(?![_a-zA-Z0-9{\\])'
protected = re.sub(pattern, r'$\1$', protected)

# Step 4: Restore math blocks
for i, block in enumerate(math_store):
    protected = protected.replace(f"§M{i}§", block)

# Step 5: Clean up any double-wrapped $$$$$ → $$
protected = re.sub(r'\$\$\$+', r'$', protected)
# Clean up $$$ → $$
protected = re.sub(r'(?<!\$)\$\$\$(?!\$)', r'$$', protected)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(protected)

# Count remaining bare Greek letters
bare_count = 0
for line in protected.split('\n'):
    # Skip lines that are inside math blocks
    if line.strip().startswith('$$') or line.strip().startswith('$'):
        continue
    # Check for bare Greek letters (not inside $...$)
    # Simple check: find Greek letters not between $ signs
    parts = re.split(r'\$[^$]+\$', line)
    for part in parts:
        matches = re.findall(GREEK, part)
        bare_count += len(matches)

print(f"[OK] Greek letters wrapped. Bare Greek remaining outside math: {bare_count}")
print(f"[SAVED] {FILE}")

# Also regenerate student version
INPUT = FILE
OUTPUT_STUDENT = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（学生版-无解析）.md"

lines = protected.split("\n")
student_lines = []
skip = False

i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    if stripped.startswith("### 解析") or stripped.startswith("**解析**"):
        skip = True
        i += 1
        continue

    if re.match(r'\*\*\d+[\.\d]*\s*答案\*\*', stripped) or stripped == "**答案**":
        skip = True
        i += 1
        continue

    if skip:
        if (stripped.startswith("### 真题") or
            stripped.startswith("## ") or
            stripped == "---" or
            stripped.startswith("### 工具") or
            stripped.startswith("### 补充") or
            stripped.startswith("# ") or
            stripped.startswith("> **")):
            skip = False
        else:
            i += 1
            continue

    if "⚠️ **易错提醒**" in stripped:
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line == "" or next_line.startswith("#") or next_line.startswith("###"):
                break
            i += 1
        continue

    if "**关键易错**" in stripped:
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line == "" or next_line.startswith("#") or next_line.startswith("###"):
                break
            i += 1
        continue

    student_lines.append(line)
    i += 1

student_content = "\n".join(student_lines)
student_content = re.sub(r'\n{4,}', '\n\n\n', student_content)

with open(OUTPUT_STUDENT, "w", encoding="utf-8") as f:
    f.write(student_content)
print(f"[SAVED] Student version: {OUTPUT_STUDENT}")
