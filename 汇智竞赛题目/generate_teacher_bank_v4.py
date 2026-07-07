#!/usr/bin/env python3
"""
Teacher version question bank generator v4.
Key insight: questions may start with "N. " OR with "N-M " where M=1
(the first sub-question of a new main question).
"""
import re

SOURCE_PATH = r"C:\Obsidion\妙妙屋\汇智竞赛题目\结构化学专题课答案.docx.md"
OUTPUT_PATH = r"C:\Obsidion\妙妙屋\汇智竞赛题目\结构化学基础题-题库（教师版）.md"

with open(SOURCE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

ch1_start = content.find("## 第一章 原子结构")
ch2_start = content.find("## 第二章 分子结构")
ch3_start = content.find("## 第3章 晶体结构")

section1 = content[ch1_start:ch2_start]
section2 = content[ch2_start:ch3_start]
section3 = content[ch3_start:]


def find_all_question_boundaries(section_text):
    """
    Find all lines that start a new MAIN question.
    A main question starts when we see:
    - "N. " (main question header), OR
    - "N-1 " or "N-1." where N is a NEW question number not seen before
      (first sub-question of a new main question)
    """
    lines = section_text.split('\n')
    boundaries = []  # (line_idx, question_number)

    seen_main_nums = set()

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        # Skip non-question content
        if stripped.startswith("## ") or stripped.startswith("# "):
            continue
        if "2025 级化学竞赛组" in stripped:
            continue
        if stripped.startswith("第 1 部分") or stripped.startswith("第 2 部分") or stripped.startswith("第 3 部分"):
            continue

        # Main question: "N. "
        m = re.match(r'^(\d+)\.\s', stripped)
        if m:
            num = int(m.group(1))
            boundaries.append((i, num))
            seen_main_nums.add(num)
            continue

        # Sub-question that starts a new main question: "N-1 " where N not seen
        m2 = re.match(r'^(\d+)-1[\.\-\s]', stripped)
        if m2:
            num = int(m2.group(1))
            if num not in seen_main_nums:
                boundaries.append((i, num))
                seen_main_nums.add(num)
                continue

    return boundaries


def group_into_questions(section_text):
    """
    Group section text into individual questions.
    Returns list of (q_num, start_line, end_line).
    """
    lines = section_text.split('\n')
    boundaries = find_all_question_boundaries(section_text)

    if not boundaries:
        return []

    questions = []
    for idx, (start_line, q_num) in enumerate(boundaries):
        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][0]
        else:
            end_line = len(lines)
        questions.append((q_num, start_line, end_line))

    return questions


def separate_q_and_a(block_lines):
    """
    Separate a block of lines into question text and answer text.
    Answer content is in:
    - <div class="mineru-algorithm">...</div> blocks
    - <table>...</table> blocks
    - Lines after the last sub-question that look like answers
    """
    q_lines = []
    a_lines = []

    in_div = False
    in_code = False

    # First, find all sub-question lines and their positions
    sub_q_positions = []
    for i, line in enumerate(block_lines):
        stripped = line.strip()
        if re.match(r'^\d+-\d+[\.\-\s]', stripped):
            sub_q_positions.append(i)

    last_sub_q_pos = sub_q_positions[-1] if sub_q_positions else -1

    i = 0
    while i < len(block_lines):
        line = block_lines[i]
        stripped = line.strip()

        # Code blocks
        if stripped.startswith("```"):
            in_code = not in_code
            a_lines.append(line)
            i += 1
            continue

        if in_code:
            a_lines.append(line)
            i += 1
            continue

        # Div answer blocks
        if '<div class="mineru-algorithm"' in stripped:
            in_div = True
            i += 1
            continue

        if '</div>' in stripped and in_div:
            in_div = False
            i += 1
            continue

        if in_div:
            a_lines.append(line)
            i += 1
            continue

        # Table blocks - collect entirely as answer
        if stripped.startswith("<table>"):
            table_lines = [line]
            i += 1
            while i < len(block_lines):
                if '</table>' in block_lines[i]:
                    table_lines.append(block_lines[i])
                    break
                table_lines.append(block_lines[i])
                i += 1
            a_lines.append('\n'.join(table_lines))
            i += 1
            continue

        # Check if this is a sub-question line AFTER the last real sub-question
        # These are likely answer content
        is_sub_q = re.match(r'^(\d+)-(\d+)[\.\-\s]', stripped)
        if is_sub_q and i > last_sub_q_pos and last_sub_q_pos >= 0:
            # This is answer content masquerading as a sub-question
            a_lines.append(line)
            i += 1
            continue

        # Lines with "Element" or other standalone words are likely artifacts
        if stripped == "Element":
            i += 1
            continue

        # Regular question content
        q_lines.append(line)
        i += 1

    return '\n'.join(q_lines).strip(), '\n'.join(a_lines).strip()


def process_section(section_text, sec_name, sec_count):
    """Process a section and return formatted output."""
    lines = section_text.split('\n')
    questions = group_into_questions(section_text)

    output = []
    output.append(f"## {sec_name}（共{sec_count}题）")
    output.append("")

    for q_num, start, end in questions:
        block = lines[start:end]
        q_text, a_text = separate_q_and_a(block)

        if not q_text.strip():
            continue

        # Clean question text: remove leading "N. " if present
        first_line = q_text.split('\n')[0]
        m = re.match(r'^\d+\.\s*', first_line)
        if m:
            first_line = first_line[m.end():]
            rest = '\n'.join(q_text.split('\n')[1:])
            q_text = first_line + ('\n' + rest if rest else '')

        output.append(f"**{q_num}.** {q_text.strip()}")
        output.append("")
        output.append("<details>")
        output.append("<summary>\U0001f4dd 答案与解析</summary>")
        output.append("")
        if a_text.strip():
            output.append(a_text.strip())
        output.append("")
        output.append("</details>")
        output.append("")

    return '\n'.join(output)


def build_output():
    """Build the complete output file."""
    header = """# 结构化学基础题 — 题库（教师版）

> 来源：湖南师范大学附属中学 2025级化学竞赛组
> 说明：本版含全部题目、答案与解析，供教师参考使用。

---"""

    parts = [header, ""]

    sections = [
        (section1, "第一部分：原子结构", "23"),
        (section2, "第二部分：分子结构", "37"),
        (section3, "第三部分：晶体结构", "76"),
    ]

    for idx, (sec_text, sec_name, sec_count) in enumerate(sections):
        parts.append(process_section(sec_text, sec_name, sec_count))
        parts.append("")
        if idx < len(sections) - 1:
            parts.append("---")
            parts.append("")

    parts.append("---")
    parts.append("")

    return '\n'.join(parts)


if __name__ == "__main__":
    output = build_output()
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"Written to {OUTPUT_PATH}")
    line_count = output.count('\n') + 1
    print(f"Total lines: {line_count}")
    q_count = output.count('<details>')
    print(f"Total questions: {q_count}")

    for sec_name in ["第一部分：原子结构", "第二部分：分子结构", "第三部分：晶体结构"]:
        idx = output.find(sec_name)
        if idx >= 0:
            next_sec = output.find("## ", idx + 1)
            if next_sec < 0:
                next_sec = len(output)
            section_text = output[idx:next_sec]
            section_q_count = section_text.count('<details>')
            print(f"  {sec_name}: {section_q_count} questions")
