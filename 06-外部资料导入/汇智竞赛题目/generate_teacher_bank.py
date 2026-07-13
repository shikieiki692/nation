#!/usr/bin/env python3
"""
Generate teacher version question bank from source answer file.
Reads the source markdown file, parses questions and answers,
and outputs a structured question bank with <details> answer blocks.
"""
import re
import os

SOURCE_PATH = r"C:\Obsidion\妙妙屋\汇智竞赛题目\结构化学专题课答案.docx.md"
OUTPUT_PATH = r"C:\Obsidion\妙妙屋\汇智竞赛题目\结构化学基础题-题库（教师版）.md"

with open(SOURCE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Split into three sections
# Chapter 1: lines 15-606 (原子结构)
# Chapter 2: lines 607-1597 (分子结构)
# Chapter 3: lines 1598-end (晶体结构)

# Find section boundaries
ch1_start = content.find("## 第一章 原子结构")
ch2_start = content.find("## 第二章 分子结构")
ch3_start = content.find("## 第3章 晶体结构")

section1 = content[ch1_start:ch2_start].strip()
section2 = content[ch2_start:ch3_start].strip()
section3 = content[ch3_start:].strip()


def parse_questions(section_text, section_name):
    """
    Parse questions from a section.
    Returns list of (question_text, answer_text) tuples.
    """
    lines = section_text.split('\n')
    questions = []
    current_question_lines = []
    current_answer_lines = []
    in_answer = False
    in_table = False

    # Track question numbering
    q_num = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip empty lines and section headers
        if stripped == "" or stripped.startswith("## ") or stripped.startswith("# "):
            if current_question_lines or current_answer_lines:
                # Don't add empty lines between questions
                pass
            continue

        # Skip the image at the very top
        if stripped.startswith("![") and "c1c29433" in stripped:
            continue
        if "湖南師範大學附屬中學" in stripped or "THE HIGH SCHOOL" in stripped:
            continue
        if stripped.startswith("## 2025 级化学竞赛组"):
            continue
        if stripped.startswith("第 1 部分") or stripped.startswith("第 2 部分") or stripped.startswith("第 3 部分"):
            continue

        # Detect answer blocks (div with class mineru-algorithm)
        if '<div class="mineru-algorithm"' in stripped:
            in_answer = True
            continue
        if '</div>' in stripped and in_answer:
            in_answer = False
            continue

        # Detect table blocks
        if stripped.startswith("<table>"):
            in_table = True
        if stripped.startswith("</table>"):
            in_table = False
            # Add table content to answer
            if current_answer_lines:
                pass  # already added
            continue

        # Detect question starts - patterns like "1.", "1-1", "2-1", etc.
        q_pattern = re.match(r'^(\d+)[\.\-]\s*(.+)', stripped)
        sub_q_pattern = re.match(r'^(\d+)-(\d+)[\.\-]\s*(.+)', stripped)
        sub_sub_q_pattern = re.match(r'^(\d+)-(\d+)-(\d+)[\.\-]\s*(.+)', stripped)

        is_question_start = False
        if sub_sub_q_pattern:
            is_question_start = True
            q_num = int(sub_sub_q_pattern.group(1))
        elif sub_q_pattern:
            is_question_start = True
            q_num = int(sub_q_pattern.group(1))
        elif q_pattern:
            is_question_start = True
            q_num = int(q_pattern.group(1))

        if is_question_start and not in_answer and not in_table:
            # Save previous question if exists
            if current_question_lines or current_answer_lines:
                q_text = '\n'.join(current_question_lines).strip()
                a_text = '\n'.join(current_answer_lines).strip()
                if q_text:
                    questions.append((q_text, a_text))
            current_question_lines = [stripped]
            current_answer_lines = []
        elif in_answer:
            current_answer_lines.append(line)
        elif in_table:
            current_answer_lines.append(line)
        elif is_question_start and in_answer:
            # Answer text that starts with a number
            current_answer_lines.append(line)
        else:
            # Regular content line
            if current_question_lines:
                current_question_lines.append(line)
            elif current_answer_lines:
                current_answer_lines.append(line)

    # Don't forget the last question
    if current_question_lines or current_answer_lines:
        q_text = '\n'.join(current_question_lines).strip()
        a_text = '\n'.join(current_answer_lines).strip()
        if q_text:
            questions.append((q_text, a_text))

    return questions


# Since the source file is complex with mixed content,
# let's use a simpler approach: read the entire file and
# process it line by line to separate questions from answers.

def build_output():
    """Build the complete output file."""

    header = """# 结构化学基础题 — 题库（教师版）

> 来源：湖南师范大学附属中学 2025级化学竞赛组
> 说明：本版含全部题目、答案与解析，供教师参考使用。

---"""

    # Now let's process the content more carefully
    # We'll split by the three chapter headers and process each

    # For each section, we need to:
    # 1. Find question starts (numbered items)
    # 2. Find answer blocks (div class="mineru-algorithm" or tables or regular text after questions)
    # 3. Format as question + <details> answer

    sections = []

    # Process each section
    for sec_text, sec_name, sec_count in [
        (section1, "第一部分：原子结构", "23"),
        (section2, "第二部分：分子结构", "37"),
        (section3, "第三部分：晶体结构", "76"),
    ]:
        # Parse questions from this section
        questions = parse_section_questions(sec_text)

        sec_header = f"\n## {sec_name}（共{sec_count}题）\n"
        sec_content = sec_header + "\n"

        for q_num_str, q_text, a_text in questions:
            sec_content += f"**{q_num_str}.** {q_text}\n\n"
            sec_content += "<details>\n"
            sec_content += "<summary>\U0001f4dd 答案与解析</summary>\n\n"
            if a_text:
                sec_content += a_text + "\n\n"
            sec_content += "</details>\n\n"

        sections.append(sec_content)

    output = header + "\n"
    for i, sec in enumerate(sections):
        output += sec
        if i < len(sections) - 1:
            output += "\n---\n"

    output += "\n---\n"

    return output


def parse_section_questions(section_text):
    """
    Parse questions from a section text.
    Returns list of (question_number_str, question_text, answer_text).
    """
    lines = section_text.split('\n')
    results = []

    # We'll collect content and split at question boundaries
    # Questions start with patterns like:
    # "1. " "1-1 " "2-1 " "2-2-1 " etc.

    current_block_type = None  # 'q' or 'a'
    current_lines = []
    current_q_num = None
    current_q_text = ""
    current_a_text = ""

    def flush_block():
        nonlocal current_q_num, current_q_text, current_a_text
        if current_q_num is not None:
            q = current_q_text.strip()
            a = current_a_text.strip()
            if q:
                results.append((current_q_num, q, a))
        current_q_num = None
        current_q_text = ""
        current_a_text = ""

    in_div = False
    in_table = False
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if current_block_type == 'q':
                current_q_text += line + '\n'
            elif current_block_type == 'a':
                current_a_text += line + '\n'
            else:
                current_a_text += line + '\n'
            continue

        # Track div blocks (answers)
        if '<div class="mineru-algorithm"' in stripped:
            in_div = True
            current_block_type = 'a'
            continue
        if '</div>' in stripped and in_div:
            in_div = False
            continue

        # Track table blocks
        if stripped.startswith("<table>"):
            in_table = True
        if stripped.startswith("</table>"):
            in_table = False
            if current_block_type == 'a':
                current_a_text += line + '\n'
            continue

        if in_div or in_table or in_code_block:
            if current_block_type == 'a' or current_block_type is None:
                current_a_text += line + '\n'
            else:
                current_q_text += line + '\n'
            continue

        # Check for main question start (e.g., "1. ", "2. ", "3. ")
        # These are the TOP-LEVEL questions (not sub-questions like 1-1, 2-1)
        main_q_match = re.match(r'^(\d+)\.\s+(.+)', stripped)

        # Check for sub-question starts
        sub_q_match = re.match(r'^(\d+)-(\d+)\s+(.+)', stripped)
        sub_sub_q_match = re.match(r'^(\d+)-(\d+)-(\d+)\s+(.+)', stripped)

        # Check for answer-like content
        is_answer_content = False
        if main_q_match:
            num = int(main_q_match.group(1))
            # This is a new main question
            flush_block()
            current_q_num = f"{num}"
            current_q_text = stripped
            current_a_text = ""
            current_block_type = 'q'
            continue

        if sub_sub_q_match:
            # Sub-sub-question - this is part of a main question's sub-questions
            # Add to current question text
            if current_block_type == 'q':
                current_q_text += '\n' + line
            else:
                # Might be answer text
                current_a_text += line + '\n'
                current_block_type = 'a'
            continue

        if sub_q_match:
            # Sub-question - add to current question text
            if current_block_type == 'q':
                current_q_text += '\n' + line
            elif current_block_type == 'a':
                current_a_text += line + '\n'
            else:
                current_q_text += '\n' + line
                current_block_type = 'q'
            continue

        # Regular content line
        if current_block_type == 'q':
            current_q_text += '\n' + line
        elif current_block_type == 'a':
            current_a_text += '\n' + line
        else:
            # Before any question - skip or add to current
            if stripped:
                current_q_text += '\n' + line
                current_block_type = 'q'

    flush_block()
    return results


# Actually, given the complexity, let me take a different approach
# Read the file and manually identify questions and answers

def parse_section_v2(section_text):
    """
    Better parsing approach.
    """
    lines = section_text.split('\n')
    results = []

    # States
    IN_QUESTION = 0
    IN_ANSWER = 1

    state = IN_QUESTION
    current_q_num = None
    q_lines = []
    a_lines = []

    def flush():
        nonlocal current_q_num, q_lines, a_lines
        if current_q_num is not None:
            q = '\n'.join(q_lines).strip()
            a = '\n'.join(a_lines).strip()
            if q:
                results.append((current_q_num, q, a))
        current_q_num = None
        q_lines = []
        a_lines = []

    in_div = False
    in_table = False
    in_code = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Code blocks
        if stripped.startswith("```"):
            in_code = not in_code
            if state == IN_QUESTION:
                q_lines.append(line)
            else:
                a_lines.append(line)
            i += 1
            continue

        if in_code:
            if state == IN_QUESTION:
                q_lines.append(line)
            else:
                a_lines.append(line)
            i += 1
            continue

        # Div answer blocks
        if '<div class="mineru-algorithm"' in stripped:
            in_div = True
            state = IN_ANSWER
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

        # Table blocks
        if '<table>' in stripped:
            in_table = True
            # Collect entire table
            table_lines = [line]
            i += 1
            while i < len(lines) and '</table>' not in lines[i]:
                table_lines.append(lines[i])
                i += 1
            if i < len(lines):
                table_lines.append(lines[i])  # closing </table>
            table_content = '\n'.join(table_lines)
            if state == IN_ANSWER:
                a_lines.append(table_content)
            else:
                a_lines.append(table_content)
                state = IN_ANSWER
            i += 1
            continue

        # Check for main question start: "N. " pattern
        main_q = re.match(r'^(\d+)\.\s', stripped)

        if main_q:
            num = main_q.group(1)
            flush()
            current_q_num = num
            state = IN_QUESTION
            q_lines = [stripped]
            a_lines = []
            i += 1
            continue

        # Check for sub-question: "N-M " or "N-M- " pattern at line start
        sub_q = re.match(r'^(\d+)-(\d+)[\.\-\s]', stripped)

        if sub_q:
            if state == IN_QUESTION:
                q_lines.append(line)
            elif state == IN_ANSWER:
                a_lines.append(line)
            i += 1
            continue

        # Check for answer-like content: lines that look like answers
        # (e.g., "1-1 ", "1-2 ", "23-1 ", etc. at the start of a line)
        ans_pattern = re.match(r'^(\d+)-(\d+)\s', stripped)

        if ans_pattern and state == IN_QUESTION:
            # This could be answer content after a question
            state = IN_ANSWER
            a_lines.append(line)
            i += 1
            continue

        # Regular content
        if state == IN_QUESTION:
            q_lines.append(line)
        else:
            a_lines.append(line)

        i += 1

    flush()
    return results


# Given the extreme complexity of parsing this file automatically,
# let's take the most reliable approach: read the file in full,
# identify question boundaries manually based on the actual content structure,
# and build the output file.

# The key insight is that in each section, questions follow this pattern:
# Main questions are numbered (1., 2., 3., etc.)
# Sub-questions are numbered (1-1, 1-2, 2-1, 2-2, etc.)
# Answers are in <div class="mineru-algorithm"> blocks or in tables or as text

# Let me use a regex-based approach to find all questions

def extract_all_content():
    """Extract all content from the source file."""
    with open(SOURCE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines


def process_file():
    """Main processing function."""

    with open(SOURCE_PATH, 'r', encoding='utf-8') as f:
        full_content = f.read()

    # Find section boundaries
    ch1_start = full_content.find("## 第一章 原子结构")
    ch2_start = full_content.find("## 第二章 分子结构")
    ch3_start = full_content.find("## 第3章 晶体结构")

    if ch1_start == -1 or ch2_start == -1 or ch3_start == -1:
        print("ERROR: Could not find section headers")
        return

    section1_text = full_content[ch1_start:ch2_start]
    section2_text = full_content[ch2_start:ch3_start]
    section3_text = full_content[ch3_start:]

    # Build output
    output_lines = []
    output_lines.append("# 结构化学基础题 — 题库（教师版）")
    output_lines.append("")
    output_lines.append("> 来源：湖南师范大学附属中学 2025级化学竞赛组")
    output_lines.append("> 说明：本版含全部题目、答案与解析，供教师参考使用。")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")

    # Process each section
    sections = [
        (section1_text, "第一部分：原子结构", "23"),
        (section2_text, "第二部分：分子结构", "37"),
        (section3_text, "第三部分：晶体结构", "76"),
    ]

    for idx, (sec_text, sec_name, sec_count) in enumerate(sections):
        output_lines.append(f"## {sec_name}（共{sec_count}题）")
        output_lines.append("")

        # Process this section
        process_section_output(sec_text, output_lines)

        output_lines.append("")
        if idx < len(sections) - 1:
            output_lines.append("---")
            output_lines.append("")

    output_lines.append("---")
    output_lines.append("")

    # Write output
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"Written to {OUTPUT_PATH}")
    print(f"Total lines: {len(output_lines)}")


def process_section_output(section_text, output_lines):
    """Process a section and append to output_lines."""

    lines = section_text.split('\n')

    # We need to find question boundaries
    # Main questions: lines starting with "N. "
    # Collect everything between main questions as the question text
    # Answer blocks: <div class="mineru-algorithm">...</div> or tables or
    # lines that start with answer-like patterns

    questions = []  # List of (q_num, q_text, a_text)

    current_q_num = None
    current_q_lines = []
    current_a_lines = []
    state = 'idle'  # 'question' or 'answer'

    in_div = False
    in_table = False
    in_code = False

    def flush_question():
        nonlocal current_q_num, current_q_lines, current_a_lines
        if current_q_num is not None:
            q = '\n'.join(current_q_lines).strip()
            a = '\n'.join(current_a_lines).strip()
            if q:
                questions.append((current_q_num, q, a))
        current_q_num = None
        current_q_lines = []
        current_a_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines at the start
        if state == 'idle' and stripped == '':
            i += 1
            continue

        # Skip header-like content
        if stripped.startswith("# ") and state == 'idle':
            i += 1
            continue
        if "2025 级化学竞赛组" in stripped:
            i += 1
            continue
        if stripped.startswith("第 1 部分") or stripped.startswith("第 2 部分") or stripped.startswith("第 3 部分"):
            i += 1
            continue

        # Handle code blocks
        if stripped.startswith("```"):
            in_code = not in_code
            if state == 'question':
                current_q_lines.append(line)
            elif state == 'answer':
                current_a_lines.append(line)
            i += 1
            continue

        if in_code:
            if state == 'question':
                current_q_lines.append(line)
            elif state == 'answer':
                current_a_lines.append(line)
            i += 1
            continue

        # Handle div answer blocks
        if '<div class="mineru-algorithm"' in stripped:
            in_div = True
            state = 'answer'
            i += 1
            continue

        if '</div>' in stripped and in_div:
            in_div = False
            i += 1
            continue

        if in_div:
            current_a_lines.append(line)
            i += 1
            continue

        # Handle table blocks - collect entire table as answer
        if stripped.startswith("<table>"):
            in_table = True
            table_lines = [line]
            i += 1
            while i < len(lines):
                if '</table>' in lines[i]:
                    table_lines.append(lines[i])
                    break
                table_lines.append(lines[i])
                i += 1
            table_content = '\n'.join(table_lines)
            current_a_lines.append(table_content)
            state = 'answer'
            in_table = False
            i += 1
            continue

        # Check for main question start
        main_q_match = re.match(r'^(\d+)\.\s+(.*)', stripped)

        if main_q_match:
            flush_question()
            current_q_num = main_q_match.group(1)
            current_q_lines = [stripped]
            current_a_lines = []
            state = 'question'
            i += 1
            continue

        # Check for answer-like patterns (lines starting with "N-M " that are answers)
        # These appear when the answer section starts
        ans_match = re.match(r'^(\d+)-(\d+)\s', stripped)

        if ans_match and state == 'question':
            # Check if this looks like answer content
            # Answer content often starts with "N-1 ", "N-2 " etc. as standalone lines
            # or has specific answer indicators
            # For now, treat as answer if we're in question state and see a new sub-question
            # that doesn't match the current question number
            pass

        # Regular content
        if state == 'question':
            current_q_lines.append(line)
        elif state == 'answer':
            current_a_lines.append(line)
        else:
            # Before any question - might be preamble
            if stripped:
                current_q_lines.append(line)
                state = 'question'

        i += 1

    flush_question()

    # Now write questions to output
    for q_num, q_text, a_text in questions:
        output_lines.append(f"**{q_num}.** {q_text}")
        output_lines.append("")
        output_lines.append("<details>")
        output_lines.append("<summary>\U0001f4dd 答案与解析</summary>")
        output_lines.append("")
        if a_text:
            output_lines.append(a_text)
        output_lines.append("")
        output_lines.append("</details>")
        output_lines.append("")


if __name__ == "__main__":
    process_file()
