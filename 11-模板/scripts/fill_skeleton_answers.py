#!/usr/bin/env python3
"""
Batch-fill skeleton question files by extracting answers from chapter answer files.

Usage:
    python fill_skeleton_answers.py --dry-run    # Preview what would be done
    python fill_skeleton_answers.py              # Actually fill files
"""

import os
import re
import sys
from pathlib import Path

# --- Configuration ---
BASE_DIR = Path(r"C:\Obsidion\妙妙屋\04-题库\教材习题\化学竞赛初赛讲义")
QUESTION_DIR = BASE_DIR
ANSWER_DIR = BASE_DIR / "答案"

# Mapping from submodule name (in filename) to answer file chapter number
SUBMODULE_TO_CHAPTER = {
    "反应方程式": 1,
    "原子结构": 2,
    "分子结构": 3,
    "配合物": 4,
    "金属有机化学": 5,
    "推断技术": 6,
    "晶体结构": 7,
    "热力学和动力学初步": 8,
    "溶液与化学分析": 9,
    "有机化学基本原理": 10,
    "人名反应与机理推断": 11,
    "有机波谱学初步": 12,
    "高分子化学简介": 13,
}

# Reverse: chapter number -> answer file suffix
CHAPTER_TO_ANSWER_FILE = {
    1: "第1讲-反应方程式-答案.md",
    2: "第2讲-原子结构-答案.md",
    3: "第3讲-分子结构-答案.md",
    4: "第4讲-配合物-答案.md",
    5: "第5讲-金属有机化学-答案.md",
    6: "第6讲-推断技术-答案.md",
    7: "第7讲-晶体结构-答案.md",
    8: "第8讲-热力学和动力学初步-答案.md",
    9: "第9讲-溶液与化学分析-答案.md",
    10: "第10讲-有机化学基本原理-答案.md",
    11: "第11讲-人名反应与机理推断-答案.md",
    12: "第12讲-有机波谱学初步-答案.md",
    13: "第13讲-高分子化学简介-答案.md",
}


def find_skeleton_files():
    """Find all .md files with status: 骨架 in frontmatter, excluding 答案/ dir."""
    skeleton_files = []
    for md_file in QUESTION_DIR.glob("题-*.md"):
        # Skip files in 答案/ subdirectory
        try:
            md_file.relative_to(ANSWER_DIR)
            continue
        except ValueError:
            pass  # Not in 答案/, good

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for status: 骨架 in frontmatter
        frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            if re.search(r"^status:\s*骨架\s*$", frontmatter, re.MULTILINE):
                skeleton_files.append(md_file)

    return sorted(skeleton_files)


def extract_exercise_number(filename):
    """Extract exercise number from filename like '习题6.17' -> '6.17'."""
    # Stop before .md extension by not allowing dot followed by 'md' at end
    match = re.search(r"习题([\d.]+[a-z]?)(?=\.md$)", filename)
    if match:
        return match.group(1)
    return None


def extract_chapter_from_exercise(exercise_num):
    """Extract chapter number from exercise number like '6.17' -> 6."""
    parts = exercise_num.split(".")
    if parts:
        try:
            return int(parts[0])
        except ValueError:
            return None
    return None


def extract_submodule_from_filename(filename):
    """Extract submodule name from filename like '题-017-初赛讲义-推断技术-习题6.17.md' -> '推断技术'."""
    match = re.search(r"初赛讲义-([^-\d][^-]*?)-习题", filename)
    if match:
        return match.group(1)
    return None


def parse_answer_file(answer_file_path):
    """Parse an answer file and return a dict of exercise_number -> answer_content."""
    if not answer_file_path.exists():
        return {}

    with open(answer_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by ## headings (exercise sections)
    # Pattern: ## X.Y followed by content until next ## heading or end of file
    sections = {}
    # Find all ## X.Y headings and their content
    pattern = r"^## (\d+\.\d+[a-z]?)\s*\n(.*?)(?=^## |\Z)"
    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)

    for match in matches:
        exercise_num = match.group(1)
        answer_content = match.group(2).rstrip("\n")
        sections[exercise_num] = answer_content

    return sections


def extract_answer_section(content):
    """Extract the answer section from a skeleton file.
    Returns (start_pos, end_pos, answer_content) or None if not found."""
    # Find ## 答案 heading
    answer_start_match = re.search(r"^## 答案\s*\n", content, re.MULTILINE)
    if not answer_start_match:
        return None

    start_pos = answer_start_match.end()

    # Find the next ## heading after answer section
    next_heading_match = re.search(r"^## ", content[start_pos:], re.MULTILINE)
    if next_heading_match:
        end_pos = start_pos + next_heading_match.start()
    else:
        # No next heading found, find the last --- separator or end of content
        end_pos = len(content)

    answer_content = content[start_pos:end_pos].rstrip("\n")

    return (answer_start_match.start(), end_pos, answer_content)


def replace_answer_section(content, new_answer):
    """Replace the answer section in the file content with new answer."""
    answer_section = extract_answer_section(content)
    if not answer_section:
        return content

    start_pos, end_pos, old_answer = answer_section

    # Build the new content
    new_content = content[:start_pos] + f"## 答案\n\n{new_answer}\n\n" + content[end_pos:]

    return new_content


def update_frontmatter_status(content):
    """Change status: 骨架 to status: 已填充 in frontmatter."""
    return re.sub(
        r"^(status:\s*)骨架\s*$",
        r"\1已填充",
        content,
        count=1,
        flags=re.MULTILINE,
    )


def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print(f"{'DRY RUN' if dry_run else 'EXECUTING'}: Fill skeleton answers")
    print("=" * 60)
    print()

    # Find skeleton files
    skeleton_files = find_skeleton_files()
    print(f"Found {len(skeleton_files)} skeleton files")
    print()

    # Parse all answer files
    answer_data = {}
    for chapter_num, answer_filename in CHAPTER_TO_ANSWER_FILE.items():
        answer_path = ANSWER_DIR / answer_filename
        if answer_path.exists():
            answer_data[chapter_num] = parse_answer_file(answer_path)
            print(f"  Loaded {len(answer_data[chapter_num])} answers from {answer_filename}")
        else:
            print(f"  WARNING: Answer file not found: {answer_filename}")
            answer_data[chapter_num] = {}
    print()

    # Process each skeleton file
    updated = 0
    skipped = 0
    failed = 0
    no_answer = 0

    for skeleton_file in skeleton_files:
        filename = skeleton_file.name
        exercise_num = extract_exercise_number(filename)
        submodule = extract_submodule_from_filename(filename)

        if not exercise_num:
            print(f"  SKIP (no exercise number): {filename}")
            skipped += 1
            continue

        chapter_num = extract_chapter_from_exercise(exercise_num)

        # Try to find chapter from submodule first, then from exercise number
        if submodule and submodule in SUBMODULE_TO_CHAPTER:
            chapter_num_from_submodule = SUBMODULE_TO_CHAPTER[submodule]
            if chapter_num != chapter_num_from_submodule:
                # Exercise number chapter doesn't match submodule, use submodule
                chapter_num = chapter_num_from_submodule

        if chapter_num is None:
            print(f"  FAIL (can't determine chapter): {filename}")
            failed += 1
            continue

        # Look up the answer
        if chapter_num in answer_data and exercise_num in answer_data[chapter_num]:
            answer_content = answer_data[chapter_num][exercise_num]
        else:
            print(f"  NO ANSWER: {filename} -> exercise {exercise_num}, chapter {chapter_num}")
            no_answer += 1
            continue

        # Read the skeleton file
        try:
            with open(skeleton_file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"  FAIL (read error): {filename}: {e}")
            failed += 1
            continue

        # Check if answer section exists
        answer_section = extract_answer_section(content)
        if not answer_section:
            print(f"  FAIL (no ## 答案 section): {filename}")
            failed += 1
            continue

        # Replace answer content
        new_content = replace_answer_section(content, answer_content)

        # Update status
        new_content = update_frontmatter_status(new_content)

        if dry_run:
            print(f"  WOULD UPDATE: {filename}")
            print(f"    Exercise: {exercise_num}, Chapter: {chapter_num}")
            print(f"    Answer length: {len(answer_content)} chars")
        else:
            try:
                with open(skeleton_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  UPDATED: {filename}")
                print(f"    Exercise: {exercise_num}, Chapter: {chapter_num}")
            except Exception as e:
                print(f"  FAIL (write error): {filename}: {e}")
                failed += 1
                continue

        updated += 1

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Updated:  {updated}")
    print(f"  No answer: {no_answer}")
    print(f"  Skipped:  {skipped}")
    print(f"  Failed:   {failed}")
    print(f"  Total skeleton files: {len(skeleton_files)}")
    print()


if __name__ == "__main__":
    main()
