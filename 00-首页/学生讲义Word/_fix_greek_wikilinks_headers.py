#!/usr/bin/env python3
"""
Fix 3 issues:
1. Remove wiki-link residuals [[...]]
2. Wrap bare Greek letters in $...$ math delimiters
3. Replace abrupt "一、开场·真题直击" with topic-specific headers
Then regenerate student version.
"""

import re

INPUT = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（完整版）.md"
OUTPUT = INPUT  # overwrite
OUTPUT_STUDENT = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（学生版-无解析）.md"

with open(INPUT, "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# FIX 1: Remove wiki-link residuals
# ============================================================
# Pattern: 、[[...]]  (standalone wiki-link lines)
content = re.sub(r'\n、\[\[[^\]]+\]\]\n', '\n', content)
# Also handle any remaining [[...]] anywhere
content = re.sub(r'\[\[[^\]]+\]\]', '', content)
print("[OK] Removed wiki-link residuals")

# ============================================================
# FIX 2: Wrap bare Greek letters in $...$ math delimiters
# ============================================================
# Greek letters that appear in the text outside math mode
# We need to be careful not to double-wrap already-mathed text

# First, protect existing math blocks by replacing them with placeholders
math_blocks = []
def protect_math(m):
    math_blocks.append(m.group(0))
    return f"§MATH{len(math_blocks)-1}§"

# Protect $...$ inline math
protected = re.sub(r'\$[^$]+\$', protect_math, content)
# Protect $$...$$ display math
protected = re.sub(r'\$\$[^$]+\$\$', protect_math, protected)

# Now wrap bare Greek letters
# Greek letters: σ π Δ δ λ μ χ θ ρ ψ ω α β γ ε η ι κ ν ξ ζ φ
greek_letters = {
    'σ': 'σ', 'π': 'π', 'Δ': 'Δ', 'δ': 'δ', 'λ': 'λ',
    'μ': 'μ', 'χ': 'χ', 'θ': 'θ', 'ρ': 'ρ', 'ψ': 'ψ',
    'ω': 'ω', 'α': 'α', 'β': 'β', 'γ': 'γ', 'ε': 'ε',
    'η': 'η', 'ι': 'ι', 'κ': 'κ', 'ν': 'ν', 'ξ': 'ξ',
    'ζ': 'ζ', 'φ': 'φ',
}

# Match Greek letters that are NOT already inside $...$ or **...**
# Strategy: wrap individual Greek letters that appear in regular text
# But skip if they're inside **bold** markers or at start of words

# More targeted: wrap Greek letters that appear as standalone symbols
# or in common patterns like "σ(C-H)", "σ*", "π→σ" etc.

# Pattern: Greek letter not preceded by $ or \ and not followed by {
# Also skip if inside **...**
for gr, replacement in greek_letters.items():
    # Skip if already wrapped: $σ$ or $\sigma$
    # Wrap: σ not preceded by $ or \ and not part of a word like "σ₂"
    # Use negative lookbehind for $ and \
    pattern = r'(?<!\$)(?<!\\)(' + re.escape(gr) + r')(?!\$|\{)'
    # Only wrap if the Greek letter is in a context where it should be math
    # e.g., "σ(C-H)" → "$σ$(C-H)", "σ*" → "$σ$*"
    protected = re.sub(pattern, r'$\1$', protected)

# Restore math blocks
for i, block in enumerate(math_blocks):
    protected = protected.replace(f"§MATH{i}§", block)

content = protected
print("[OK] Wrapped bare Greek letters in math delimiters")

# ============================================================
# FIX 3: Replace abrupt "一、开场·真题直击" with topic headers
# ============================================================
# Find each occurrence and determine the topic from the next ### 真题 line
topic_map = {
    "Bent规则与VSEPR": "Lewis与VSEPR实战",
    "gauche vs staggered": "MO理论与立体电子效应",
    "Fe/Cr合金": "晶体结构基础",
    "Ce$O_{2}$投影图": "晶体结构进阶",
    "Ru配合物": "配位化合物",
    "ReNₓ": "跨模块综合实战",
}

lines = content.split("\n")
new_lines = []
i = 0
topic_count = 0
topic_names = [
    "Lewis与VSEPR实战",
    "MO理论与立体电子效应",
    "晶体结构基础",
    "晶体结构进阶",
    "配位化合物",
    "跨模块综合实战",
]

while i < len(lines):
    line = lines[i]

    if line.strip() == "## 一、开场·真题直击":
        topic_count += 1
        if topic_count == 1:
            # First occurrence: keep as main section divider but add topic context
            new_lines.append(f"## 专题一：{topic_names[0]}")
        else:
            # Subsequent occurrences: replace with topic-specific header
            idx = topic_count - 1
            if idx < len(topic_names):
                new_lines.append(f"## 专题{['一','二','三','四','五','六'][idx]}：{topic_names[idx]}")
            else:
                new_lines.append(line)
        i += 1
        continue

    new_lines.append(line)
    i += 1

content = "\n".join(new_lines)
print(f"[OK] Replaced {topic_count} abrupt section headers with topic-specific headers")

# ============================================================
# Save fixed full version
# ============================================================
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[SAVED] Full version: {OUTPUT}")

# ============================================================
# Regenerate student version
# ============================================================
lines = content.split("\n")
student_lines = []
skip = False

i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Detect "### 解析" headers - skip everything until next ### or ## or ---
    if stripped.startswith("### 解析") or stripped.startswith("**解析**"):
        skip = True
        i += 1
        continue

    # Detect answer sections
    if re.match(r'\*\*\d+[\.\d]*\s*答案\*\*', stripped) or stripped == "**答案**":
        skip = True
        i += 1
        continue

    # Stop skipping at section boundaries
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

    # Skip 易错提醒 blocks
    if "⚠️ **易错提醒**" in stripped:
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line == "" or next_line.startswith("#") or next_line.startswith("###"):
                break
            i += 1
        continue

    # Skip "**关键易错**" blocks
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
# Clean up excessive blank lines
student_content = re.sub(r'\n{4,}', '\n\n\n', student_content)

with open(OUTPUT_STUDENT, "w", encoding="utf-8") as f:
    f.write(student_content)
print(f"[SAVED] Student version: {OUTPUT_STUDENT}")

# Stats
print(f"\n[STATS]")
print(f"  Full: {len(content)} chars, {content.count(chr(10))} lines, {content.count(chr(10)+'|:')} tables")
print(f"  Student: {len(student_content)} chars, {student_content.count(chr(10))} lines")
