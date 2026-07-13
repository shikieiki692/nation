#!/usr/bin/env python3
"""
Teacher version question bank generator v3.
Handles the complex structure of the source file where questions
may start with "N. " or directly with sub-questions "N-M ".
"""
import re

SOURCE_PATH = r"C:\Obsidion\妙妙屋\汇智竞赛题目\结构化学专题课答案.docx.md"
OUTPUT_PATH = r"C:\Obsidion\妙妙屋\汇智竞赛题目\结构化学基础题-题库（教师版）.md"

with open(SOURCE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find section boundaries
ch1_start = content.find("## 第一章 原子结构")
ch2_start = content.find("## 第二章 分子结构")
ch3_start = content.find("## 第3章 晶体结构")

section1 = content[ch1_start:ch2_start]
section2 = content[ch2_start:ch3_start]
section3 = content[ch3_start:]


def find_question_starts(section_text):
    """
    Find all lines that start a new question or sub-question.
    Returns list of (line_index, question_number, is_main_question, line_text).
    """
    lines = section_text.split('\n')
    starts = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        # Main question: "N. " where N is a number
        m_main = re.match(r'^(\d+)\.\s', stripped)
        if m_main:
            starts.append((i, int(m_main.group(1)), True, stripped))
            continue

        # Sub-question: "N-M " or "N-M-" at start of line
        m_sub = re.match(r'^(\d+)-(\d+)[\.\-\s]', stripped)
        if m_sub:
            starts.append((i, int(m_sub.group(1)), False, stripped))
            continue

    return starts


def group_questions(section_text):
    """
    Group the section into questions.
    Each question starts with either "N. " or "N-M " pattern.
    We group by the main question number N.
    """
    lines = section_text.split('\n')
    starts = find_question_starts(section_text)

    if not starts:
        return []

    questions = []  # List of (q_num, start_line, end_line)

    for idx, (line_idx, q_num, is_main, text) in enumerate(starts):
        # Find the end of this question (start of next question with different main num)
        end_line = len(lines)
        for j in range(idx + 1, len(starts)):
            next_line_idx, next_q_num, next_is_main, next_text = starts[j]
            if next_q_num != q_num:
                end_line = next_line_idx
                break

        questions.append((q_num, line_idx, end_line))

    return questions


def extract_question_content(lines, start, end):
    """
    Extract question text and answer text from lines[start:end].
    Question text is everything before the answer blocks.
    Answer text is in <div> blocks, tables, or after question sub-questions.
    """
    block_lines = lines[start:end]

    q_lines = []
    a_lines = []

    in_div = False
    in_table = False
    in_code = False
    past_last_sub_q = False

    # First pass: find where answer content starts
    # Answer content is in <div> blocks, tables, or follows after all sub-questions
    last_sub_q_line = -1
    for i, line in enumerate(block_lines):
        stripped = line.strip()
        if re.match(r'^\d+-\d+[\.\-\s]', stripped):
            last_sub_q_line = i

    # Second pass: separate question and answer
    i = 0
    while i < len(block_lines):
        line = block_lines[i]
        stripped = line.strip()

        # Code blocks
        if stripped.startswith("```"):
            in_code = not in_code
            if in_code:
                a_lines.append(line)
            else:
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

        # Table blocks - collect as answer
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

        # Check if this is a sub-question line after the last sub-question
        # If so, it's likely answer content
        is_sub_q = re.match(r'^\d+-\d+[\.\-\s]', stripped)

        if is_sub_q and i > last_sub_q_line:
            # This sub-question number appears after the last real sub-question
            # It's likely answer content
            a_lines.append(line)
            i += 1
            continue

        # Regular content - question text
        q_lines.append(line)
        i += 1

    return '\n'.join(q_lines).strip(), '\n'.join(a_lines).strip()


def process_section(section_text, sec_name, sec_count):
    """Process a section and return formatted text."""
    lines = section_text.split('\n')
    questions = group_questions(section_text)

    output = []
    output.append(f"## {sec_name}（共{sec_count}题）")
    output.append("")

    seen_nums = set()
    for q_num, start, end in questions:
        if q_num in seen_nums:
            # Duplicate question number - skip or merge
            # For now, skip
            continue
        seen_nums.add(q_num)

        q_text, a_text = extract_question_content(lines, start, end)

        # Clean up question text - remove leading "N. " if present
        q_first_line = q_text.split('\n')[0] if q_text else ""
        m = re.match(r'^(\d+)\.\s*', q_first_line)
        if m:
            q_first_line = q_first_line[m.end():]
            q_rest = '\n'.join(q_text.split('\n')[1:])
            q_text = q_first_line + ('\n' + q_rest if q_rest else '')

        if not q_text.strip():
            continue

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

    # Count per section
    for sec_name in ["第一部分：原子结构", "第二部分：分子结构", "第三部分：晶体结构"]:
        idx = output.find(sec_name)
        if idx >= 0:
            next_sec = output.find("## ", idx + 1)
            if next_sec < 0:
                next_sec = len(output)
            section_text = output[idx:next_sec]
            section_q_count = section_text.count('<details>')
            print(f"  {sec_name}: {section_q_count} questions")
