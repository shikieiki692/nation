#!/usr/bin/env python3
"""
Generate the teacher version question bank from the source answer file.
Key improvement: flatten <table> content before parsing question starts.
"""

import re
import os

source_path = r'C:\Obsidion\妙妙屋\汇智竞赛题目\结构化学专题课答案.docx.md'
output_path = r'C:\Obsidion\妙妙屋\汇智竞赛题目\结构化学基础题-题库（教师版）.md'

with open(source_path, 'r', encoding='utf-8') as f:
    raw_content = f.read()

# ── Step 1: Flatten tables ──────────────────────────────────────────
# Replace <table>...</table> blocks by extracting text from each <td>.
# This makes question markers inside tables visible to the line scanner.

def flatten_tables(text):
    """Replace each <table>...</table> with the plain text from its <td> cells."""
    parts = []
    pos = 0
    while True:
        tstart = text.find('<table>', pos)
        if tstart == -1:
            parts.append(text[pos:])
            break
        parts.append(text[pos:tstart])
        tend = text.find('</table>', tstart)
        if tend == -1:
            parts.append(text[tstart:])
            break
        block = text[tstart:tend + len('</table>')]
        # Extract text inside each <td>...</td>
        td_texts = re.findall(r'<td[^>]*>(.*?)</td>', block, re.DOTALL)
        # Clean HTML tags from each cell but keep content
        cleaned = []
        for td in td_texts:
            # Preserve <img> tags with proper path
            td_clean = re.sub(
                r'<img\s+src="images/([^"]+)"',
                r'![](结构化学专题课答案.docx_images/\1)', td)
            # Remove remaining HTML tags
            td_clean = re.sub(r'<[^>]+>', '', td_clean)
            td_clean = td_clean.strip()
            if td_clean:
                cleaned.append(td_clean)
        parts.append('\n'.join(cleaned))
        pos = tend + len('</table>')
    return ''.join(parts)

flat = flatten_tables(raw_content)
lines = flat.split('\n')

# ── Step 2: Locate chapter boundaries ──────────────────────────────
chap_starts = []
chap_names = []
for i, ln in enumerate(lines):
    if ln.startswith('## 第一章'):
        chap_starts.append(i); chap_names.append('原子结构')
    elif ln.startswith('## 第二章'):
        chap_starts.append(i); chap_names.append('分子结构')
    elif ln.startswith('## 第3章'):
        chap_starts.append(i); chap_names.append('晶体结构')
chap_starts.append(len(lines))

# ── Step 3: Detect main-question start lines ───────────────────────
def detect_questions(ch_lo, ch_hi):
    """Return list of (line_index, question_number) for main questions."""
    qs = []
    prev = 0
    for i in range(ch_lo, ch_hi):
        ln = lines[i].strip()
        if not ln:
            continue
        # --- Pattern A:  "N. "  or  "N."  or  "N.非空白" -------------
        m = re.match(r'^(\d{1,3})\s*[.．]', ln)
        if m:
            n = int(m.group(1))
            if n <= 100 and (n > prev or (n == 1 and prev == 0)):
                qs.append((i, n))
                prev = n
                continue
        # --- Pattern B:  "N-1" followed by space/period/non-digit ----
        m = re.match(r'^(\d{1,3})-1[^\d]', ln)
        if m:
            n = int(m.group(1))
            if n <= 100 and n > prev:
                qs.append((i, n))
                prev = n
                continue
        # --- Pattern C:  "N " (no period), small gap ----------------
        m = re.match(r'^(\d{1,3})\s', ln)
        if m:
            n = int(m.group(1))
            if n <= 100 and n > prev and n <= prev + 2:
                qs.append((i, n))
                prev = n
                continue
    return qs

# ── Step 4: Find answer boundary inside a question block ───────────
def find_answer_start(text):
    """Return the offset where the answer section begins, or -1."""
    # <div class="mineru-algorithm" ...>
    m = re.search(r'<div\s+class="mineru-algorithm"', text)
    if m:
        return m.start()
    # <table> after substantial question text
    m = re.search(r'<table>', text)
    if m and len(text[:m.start()].strip()) > 30:
        return m.start()
    # ``` code block after question text
    m = re.search(r'```', text)
    if m and len(text[:m.start()].strip()) > 30:
        return m.start()
    return -1

# ── Step 5: Build output ───────────────────────────────────────────
header = """# 结构化学基础题 — 题库（教师版）

> 来源：湖南师范大学附属中学 2025级化学竞赛组
> 说明：本版含全部题目、答案与解析，供教师参考使用。

---
"""

section_titles = {
    '原子结构': '第一部分：原子结构（共23题）',
    '分子结构': '第二部分：分子结构（共37题）',
    '晶体结构': '第三部分：晶体结构（共76题）',
}

out = [header]

for ci in range(3):
    lo = chap_starts[ci]
    hi = chap_starts[ci + 1]
    name = chap_names[ci]
    qs = detect_questions(lo, hi)

    out.append(f'## {section_titles[name]}\n')

    for qi, (start, qnum) in enumerate(qs):
        end = qs[qi + 1][0] if qi + 1 < len(qs) else hi
        # Collect raw lines (skip leading blank lines)
        block_lines = []
        started = False
        for j in range(start, end):
            if not started:
                if lines[j].strip():
                    started = True
                else:
                    continue
            block_lines.append(lines[j])
        raw = '\n'.join(block_lines)

        # Find answer boundary
        ans_pos = find_answer_start(raw)
        if ans_pos >= 0:
            qtext = raw[:ans_pos].strip()
            answer = raw[ans_pos:].strip()
        else:
            # No clear boundary: split at first blank line
            parts = re.split(r'\n\s*\n', raw, maxsplit=1)
            if len(parts) == 2:
                qtext = parts[0].strip()
                answer = parts[1].strip()
            else:
                qtext = ''
                answer = raw.strip()

        # Clean question text: remove leading "N. " or "N-1 " prefix
        qtext_clean = re.sub(r'^\d{1,3}\s*[.．]\s*', '', qtext)
        qtext_clean = re.sub(r'^\d{1,3}-\d+\s*', '', qtext_clean, count=1)
        # Remove standalone "Element" artifact lines
        qtext_clean = re.sub(r'\nElement\n', '\n', qtext_clean)
        qtext_clean = qtext_clean.strip()

        out.append(f'**{qnum}.** {qtext_clean}\n')
        out.append('<details>')
        out.append('<summary>📝 答案与解析</summary>\n')
        out.append(answer)
        out.append('\n</details>\n')

    if ci < 2:
        out.append('\n---\n')

result = '\n'.join(out)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(result)

# ── Report ──────────────────────────────────────────────────────────
import sys
sys.stdout.reconfigure(encoding='utf-8')
for ci in range(3):
    lo = chap_starts[ci]
    hi = chap_starts[ci + 1]
    qs = detect_questions(lo, hi)
    nums = [q[1] for q in qs]
    print(f'{chap_names[ci]}: {len(qs)} questions, numbers: {nums}')

fsize = os.path.getsize(output_path)
print(f'\nOutput file: {output_path}')
print(f'Size: {fsize:,} bytes')
print(f'First 300 chars:\n{result[:300]}')
