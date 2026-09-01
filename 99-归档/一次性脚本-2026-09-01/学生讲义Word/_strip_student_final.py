"""
Generate a thoroughly stripped student-only version from the full handout.
Removes: 解析 sections, answers, 易错提醒, 关键易错, draft language.
"""
import re

INPUT = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（完整版）.md"
OUTPUT = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（学生版-无解析）.md"

with open(INPUT, "r", encoding="utf-8") as f:
    lines = f.readlines()

output = []
skip = False
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Start skipping at ### 解析
    if stripped == "### 解析":
        skip = True
        i += 1
        continue

    # Stop skipping at next ## or ### header (but not ####)
    if skip:
        if re.match(r'^#{1,3} [^#]', stripped):
            skip = False
        else:
            i += 1
            continue

    # Remove standalone 易错提醒 / 关键易错 blocks (these are inside 解析 already, but just in case)
    if re.match(r'^>\s*\*\*⚠️\s*易错提醒\*\*', stripped):
        skip = True
        i += 1
        continue
    if re.match(r'^>\s*\*\*关键易错\*\*', stripped):
        skip = True
        i += 1
        continue

    # Remove standalone answer lines
    if re.match(r'^\*\*答案[：:]?\*\*', stripped):
        i += 1
        continue
    if re.match(r'^>\s*\*\*答案[：:]?\*\*', stripped):
        i += 1
        continue

    output.append(line)
    i += 1

# Clean up excessive blank lines (more than 2 consecutive)
final = []
blank_count = 0
for line in output:
    if line.strip() == '':
        blank_count += 1
        if blank_count <= 2:
            final.append(line)
    else:
        blank_count = 0
        final.append(line)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.writelines(final)

print(f"Input: {len(lines)} lines")
print(f"Output: {len(final)} lines")
print(f"Removed: {len(lines) - len(final)} lines")
