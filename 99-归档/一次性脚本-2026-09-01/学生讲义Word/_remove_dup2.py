#!/usr/bin/env python3
"""Remove the remaining duplicate: 专题六 真题2 嫦娥石."""
import re

FILE = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（完整版）.md"
STUDENT = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（学生版-无解析）.md"

with open(FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the 嫦娥石 duplicate in 专题六
start = None
end = None
for i, line in enumerate(lines):
    if "36届二场第7题" in line and "嫦娥石" in line and line.strip().startswith("### 真题2"):
        # Go back to find the preceding "---"
        start = i - 1
        if start >= 0 and lines[start].strip() == "---":
            pass  # include the ---
        else:
            start = i
        break

if start is not None:
    # Find end: "---" before "### 真题3"
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == "---" and i + 1 < len(lines) and lines[i+1].strip().startswith("### 真题3"):
            end = i + 1
            break
    # Also handle case where end is "---" before next ### 真题
    if end is None:
        for i in range(start + 1, len(lines)):
            s = lines[i].strip()
            if s.startswith("### 真题3"):
                # Go back to find "---"
                end = i
                while end > start and lines[end - 1].strip() == "---":
                    end -= 1
                break

if start is not None and end is not None:
    print(f"Removing lines {start+1}-{end+1}")
    del lines[start:end+1]
    print("Done.")
else:
    print(f"Could not find duplicate. start={start}, end={end}")

with open(FILE, "w", encoding="utf-8") as f:
    f.writelines(lines)

# Count 真题 entries
count = sum(1 for l in lines if l.strip().startswith("### 真题"))
print(f"Total 真题 entries: {count}")

# Regenerate student version
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
print(f"Student version: {len(student)} chars")
