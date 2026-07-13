#!/usr/bin/env python3
"""
Robust teacher version question bank generator.
Strategy: Read entire file, split into blocks by main question headers,
then separate question text from answer text within each block.
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

assert ch1_start != -1, "Cannot find 原子结构"
assert ch2_start != -1, "Cannot find 分子结构"
assert ch3_start != -1, "Cannot find 晶体结构"

section1 = content[ch1_start:ch2_start]
section2 = content[ch2_start:ch3_start]
section3 = content[ch3_start:]


def split_into_question_blocks(section_text):
    """
    Split a section into question blocks.
    Each block starts with a main question header like "N. " or "N-M " at the start of a line.

    Returns list of (full_block_text,) where each block contains
    everything for one main question.
    """
    lines = section_text.split('\n')
    blocks = []
    current_block = []

    for line in lines:
        stripped = line.strip()

        # Skip section header and preamble lines
        if stripped.startswith("## ") or stripped.startswith("# "):
            if current_block:
                blocks.append('\n'.join(current_block))
                current_block = []
            continue

        if "2025 级化学竞赛组" in stripped:
            continue
        if stripped.startswith("第 1 部分") or stripped.startswith("第 2 部分") or stripped.startswith("第 3 部分"):
            continue
        if stripped.startswith("![") and "c1c29433" in stripped:
            continue
        if "湖南師範大學附屬中學" in stripped or "THE HIGH SCHOOL" in stripped:
            continue

        # Check if this line starts a NEW main question
        # Main question patterns: "1. ", "2. ", "3. ", etc.
        # NOT sub-questions like "1-1 ", "2-1 ", "2-2-1 "
        is_new_main_q = False

        # Pattern: "N. " where N is a number, NOT followed by "-" (which would be sub-question)
        m = re.match(r'^(\d+)\.\s', stripped)
        if m:
            is_new_main_q = True

        # Some questions start differently, like "25-1" at the top level
        # We need to handle these too

        if is_new_main_q and current_block:
            blocks.append('\n'.join(current_block))
            current_block = []

        current_block.append(line)

    if current_block:
        blocks.append('\n'.join(current_block))

    return blocks


def separate_question_answer(block_text):
    """
    Separate a question block into question text and answer text.
    """
    lines = block_text.split('\n')
    q_lines = []
    a_lines = []

    in_div = False
    in_table = False
    in_code = False
    in_answer_region = False

    for line in lines:
        stripped = line.strip()

        # Code blocks
        if stripped.startswith("```"):
            in_code = not in_code
            if in_answer_region:
                a_lines.append(line)
            else:
                q_lines.append(line)
            continue

        if in_code:
            if in_answer_region:
                a_lines.append(line)
            else:
                q_lines.append(line)
            continue

        # Div answer blocks
        if '<div class="mineru-algorithm"' in stripped:
            in_div = True
            in_answer_region = True
            continue

        if '</div>' in stripped and in_div:
            in_div = False
            continue

        if in_div:
            a_lines.append(line)
            continue

        # Table blocks - treat as answer content
        if stripped.startswith("<table>"):
            in_table = True
            table_lines = [line]
            # We'll handle this outside the loop
            continue

        if in_table:
            # Skip table content (it's handled below)
            continue

        if stripped.startswith("</table>"):
            in_table = False
            continue

        # Check if we've entered answer region
        # Answer content often starts with answer-like patterns
        # or follows after question sub-questions
        if not in_answer_region:
            # Check if this looks like answer content
            # Answer patterns: lines starting with "N-M " that are short answers
            # or text that follows after the last sub-question
            pass

        if in_answer_region:
            a_lines.append(line)
        else:
            q_lines.append(line)

    # Now handle tables - they're answer content
    # Re-scan for tables
    table_contents = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("<table>"):
            table_lines = [lines[i]]
            i += 1
            while i < len(lines):
                if '</table>' in lines[i]:
                    table_lines.append(lines[i])
                    break
                table_lines.append(lines[i])
                i += 1
            table_contents.append('\n'.join(table_lines))
        i += 1

    # Add table contents to answer
    for tc in table_contents:
        if tc not in a_lines:
            a_lines.append(tc)

    return '\n'.join(q_lines).strip(), '\n'.join(a_lines).strip()


def build_question_bank():
    """Build the complete question bank file."""

    header = """# 结构化学基础题 — 题库（教师版）

> 来源：湖南师范大学附属中学 2025级化学竞赛组
> 说明：本版含全部题目、答案与解析，供教师参考使用。

---"""

    sections = [
        (section1, "第一部分：原子结构", "23"),
        (section2, "第二部分：分子结构", "37"),
        (section3, "第三部分：晶体结构", "76"),
    ]

    output_parts = [header, ""]

    for idx, (sec_text, sec_name, sec_count) in enumerate(sections):
        output_parts.append(f"## {sec_name}（共{sec_count}题）")
        output_parts.append("")

        # Split into question blocks
        blocks = split_into_question_blocks(sec_text)

        for block in blocks:
            q_text, a_text = separate_question_answer(block)
            if not q_text:
                continue

            # Extract question number from the first line
            first_line = q_text.split('\n')[0].strip()
            m = re.match(r'^(\d+)\.\s', first_line)
            if m:
                q_num = m.group(1)
                # Remove the leading "N. " from question text
                q_display = re.sub(r'^\d+\.\s*', '', first_line)
                # Rest of question text
                rest_q = '\n'.join(q_text.split('\n')[1:])
                full_q = q_display + '\n' + rest_q if rest_q.strip() else q_display
            else:
                # Try to find question number from first sub-question
                m2 = re.match(r'^(\d+)-', first_line)
                if m2:
                    q_num = m2.group(1)
                    full_q = q_text
                else:
                    q_num = "?"
                    full_q = q_text

            output_parts.append(f"**{q_num}.** {full_q.strip()}")
            output_parts.append("")
            output_parts.append("<details>")
            output_parts.append("<summary>\U0001f4dd 答案与解析</summary>")
            output_parts.append("")
            if a_text:
                output_parts.append(a_text)
            output_parts.append("")
            output_parts.append("</details>")
            output_parts.append("")

        output_parts.append("")
        if idx < len(sections) - 1:
            output_parts.append("---")
            output_parts.append("")

    output_parts.append("---")
    output_parts.append("")

    return '\n'.join(output_parts)


if __name__ == "__main__":
    output = build_question_bank()
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"Written to {OUTPUT_PATH}")
    # Count lines
    line_count = output.count('\n') + 1
    print(f"Total lines: {line_count}")
    # Count questions
    q_count = output.count('<details>')
    print(f"Total questions with details blocks: {q_count}")
