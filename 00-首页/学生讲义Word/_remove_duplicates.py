#!/usr/bin/env python3
"""Remove 2 duplicate exam questions and regenerate student version."""
import re

FILE = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（完整版）.md"
STUDENT = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（学生版-无解析）.md"

with open(FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# === Duplicate 1: 专题二 真题5 (39届初赛第8题 8.1 完整解法) ===
# Find start: "### 真题5：39届初赛第8题 8.1 — Bent规则键角分析（完整解法）"
# Find end: next "---" after the section, before "## 专题三"

start1 = None
end1 = None
for i, line in enumerate(lines):
    if "真题5：39届初赛第8题 8.1 — Bent规则键角分析" in line:
        # Go back to find the preceding "---"
        start1 = i - 1
        if start1 >= 0 and lines[start1].strip() == "---":
            start1 = i - 1  # include the ---
        else:
            start1 = i
        break

if start1 is not None:
    # Find end: look for "## 专题三" or the next "---" followed by "---" or "##"
    for i in range(start1 + 1, len(lines)):
        if lines[i].strip() == "---" and i + 1 < len(lines) and (lines[i+1].strip() == "---" or lines[i+1].strip().startswith("## ")):
            end1 = i + 1
            break
        if lines[i].strip().startswith("## 专题三"):
            # Go back to find the preceding "---"
            end1 = i
            while end1 > start1 and lines[end1 - 1].strip() == "---":
                end1 -= 1
            break

print(f"Duplicate 1 (专题二 真题5 8.1): lines {start1+1}-{end1+1}")

# === Duplicate 2: 专题六 真题2 (36届二场第7题 嫦娥石) ===
# Find start: "### 真题2：36届二场第7题 — 嫦娥石"
# Find end: next "---" before "### 真题3"

start2 = None
end2 = None
for i, line in enumerate(lines):
    if "真题2：36届二场第7题 — 嫦娥石" in line:
        # Go back to find "---"
        start2 = i - 1
        if start2 >= 0 and lines[start2].strip() == "---":
            start2 = i - 1
        else:
            start2 = i
        break

if start2 is not None:
    # Find end: "---" before "### 真题3"
    for i in range(start2 + 1, len(lines)):
        if lines[i].strip() == "---" and i + 1 < len(lines) and lines[i+1].strip().startswith("### 真题3"):
            end2 = i + 1
            break

print(f"Duplicate 2 (专题六 真题2 嫦娥石): lines {start2+1}-{end2+1}")

# === Remove duplicates (in reverse order to preserve line numbers) ===
if end2 is not None and start2 is not None:
    print(f"Removing lines {start2+1}-{end2+1} (嫦娥石 duplicate)")
    del lines[start2:end2+1]

if end1 is not None and start1 is not None:
    print(f"Removing lines {start1+1}-{end1+1} (8.1 duplicate)")
    del lines[start1:end1+1]

# Also renumber: after removing 真题5 from 专题二, the 专题二 section has 4 真题
# After removing 真题2 from 专题六, the 专题六 section has 4 真题
# The "## 三、真题精练" header before the removed 嫦娥石 in 专题六 is now orphaned
# Need to check if it should be removed too

with open(FILE, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"\nTotal lines: {len(lines)}")

# Count 真题 entries
count = sum(1 for l in lines if l.strip().startswith("### 真题"))
print(f"Total 真题 entries: {count}")

# === Regenerate student version ===
content = "".join(lines)
s_lines = content.split("\n")
out = []
skip = False
i = 0
while i < len(s_lines):
    line = s_lines[i]
    s = line.strip()
    if s.startswith("### 解析") or s.startswith("**解析**"):
        skip = True; i += 1; continue
    if re.match(r'\*\*\d+[\.\d]*\s*答案\*\*', s) or s == "**答案**":
        skip = True; i += 1; continue
    if skip:
        if any(s.startswith(p) for p in ['### 真题','## ','---','### 工具','### 补充','# ','> **']):
            skip = False
        else:
            i += 1; continue
    if '⚠️ **易错提醒**' in s:
        i += 1
        while i < len(s_lines):
            if s_lines[i].strip() == '' or s_lines[i].strip().startswith('#') or s_lines[i].strip().startswith('###'):
                break
            i += 1
        continue
    if '**关键易错**' in s:
        i += 1
        while i < len(s_lines):
            if s_lines[i].strip() == '' or s_lines[i].strip().startswith('#') or s_lines[i].strip().startswith('###'):
                break
            i += 1
        continue
    out.append(line); i += 1

student = re.sub(r'\n{4,}', '\n\n\n', '\n'.join(out))
with open(STUDENT, "w", encoding="utf-8") as f:
    f.write(student)
print(f"\nStudent version: {len(student)} chars")
