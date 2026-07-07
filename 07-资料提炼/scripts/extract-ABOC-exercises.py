# -*- coding: utf-8 -*-
"""
ABOC剩余习题提取脚本
从ABOC源文件中提取自学练习和章末习题
"""

import re
import os

# 源文件路径
source_file1 = r"C:\Obsidion\妙妙屋\mineru\03-教材书籍\ABOC有机化学\ABOC202505_1-200.md"
source_file2 = r"C:\Obsidion\妙妙屋\mineru\03-教材书籍\ABOC有机化学\ABOC202505_200-397.md"
output_dir = r"C:\Obsidion\妙妙屋\04-题库\教材习题\ABOC"

# 读取源文件
with open(source_file1, 'r', encoding='utf-8') as f:
    content1 = f.read()

with open(source_file2, 'r', encoding='utf-8') as f:
    content2 = f.read()

# 合并内容
all_content = content1 + "\n" + content2

# 提取自学练习的正则表达式
exercise_pattern = r"^自学练习 (\d+\.\d+(?:\.\d+)?(?:-\d+)?)\s+(.*?)(?=^自学练习 \d|^# |^$|\Z)"

# 提取章末习题的正则表达式
chapter_exercise_pattern = r"^# T(\d+)\.\s+(.*?)(?=^# T\d|^# |^$|\Z)"

# 提取所有自学练习
exercises = re.findall(exercise_pattern, all_content, re.MULTILINE | re.DOTALL)

print(f"Found {len(exercises)} self-study exercises")

# 提取所有章末习题
chapter_exercises = re.findall(chapter_exercise_pattern, all_content, re.MULTILINE | re.DOTALL)

print(f"Found {len(chapter_exercises)} chapter-end exercises")

# 定义已提取的练习编号
extracted_exercises = [
    "1.1.1", "1.2.2-1", "1.3.1-3",  # Ch1
    "2.2.2", "2.3", "2.4-2",  # Ch2
    "3.1.2", "3.4",  # Ch3
    "4.1", "4.5.1",  # Ch4
    "5.1", "5.3",  # Ch5
    "6.1", "6.5.1",  # Ch6
    "7.2.1-1", "7.2-1",  # Ch7
    "8.6",  # Ch8
    "9.2-2"  # Ch9
]

# 定义已提取的章末习题
extracted_chapter_exercises = [
    "1-T1", "2-T3", "3-T3", "4-T3", "5-T3", "6-T3", "7-T3", "8-T3", "9-T3"
]

# 计数器
next_number = 80  # 从080开始

# 处理自学练习
for exercise_id, exercise_content in exercises:
    # 检查是否已提取
    if exercise_id in extracted_exercises:
        continue

    # 确定章节
    chapter = int(exercise_id.split('.')[0])

    # 清理内容
    safe_content = re.sub(r'[^\w\s]', ' ', exercise_content).strip()
    short_content = safe_content[:30]

    # 创建文件名（使用ASCII安全的名称）
    safe_id = exercise_id.replace('.', '-').replace('-', '_')
    file_name = f"题-{next_number:03d}-ABOC-Ch{chapter}-{safe_id}.md"

    # 创建文件内容
    file_content = f"""---
title: {file_name}
type: 题目
source: ABOC 第{chapter}章 自学练习（ARX's Basic Organic Chemistry 第3版）
subject: 有机化学
module: 基础要求-有机化学
submodule: Ch.{chapter}
question_type: 机理书写题
difficulty: 2
teaching_level: 巩固
exam_stage: 初赛
syllabus_codes: ["{31 + chapter - 1}"]
knowledge_points: ["[[]]"]
tags: [化竞, ABOC, 有机化学]
aliases: [ABOC-Ch{chapter}-{exercise_id}]
updated: 2026-07-04
---

# 题-{next_number:03d}：{exercise_content.strip()[:50]}

> **来源**：ABOC 第{chapter}章 自学练习 {exercise_id}
> **难度**：⭐⭐
> **教学层级**：巩固

---

## 题目

{exercise_content}

---

## 答案

（答案见 [[提炼-ABOC-第12章-习题解析]]）

---

## 解题思路

（待补充）

---

## 知识点

- [[]]

---

## 相关题目

- [[题-062-ABOC-Ch1-1.1.1-离去基判断]]
- [[题-063-ABOC-Ch1-1.2.2-1-S-C反键轨道与端基效应]]
- [[题-064-ABOC-Ch1-1.3.1-3-金刚烷合成（碳正离子重排）]]
"""

    # 写入文件
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)

    print(f"Created: {file_name}")
    next_number += 1

# 处理章末习题
for exercise_number, exercise_content in chapter_exercises:
    # 检查是否已提取
    chapter_num = (int(exercise_number) - 1) // 10 + 1
    if f"{chapter_num}-T{exercise_number}" in extracted_chapter_exercises:
        continue

    # 确定章节（根据题号范围）
    exercise_num = int(exercise_number)
    if exercise_num <= 13:
        chapter = 1
    elif exercise_num <= 22:
        chapter = 2
    elif exercise_num <= 31:
        chapter = 3
    elif exercise_num <= 40:
        chapter = 4
    elif exercise_num <= 49:
        chapter = 5
    elif exercise_num <= 58:
        chapter = 6
    elif exercise_num <= 64:
        chapter = 7
    elif exercise_num <= 67:
        chapter = 8
    else:
        chapter = 9

    # 清理内容
    safe_content = re.sub(r'[^\w\s]', ' ', exercise_content).strip()
    short_content = safe_content[:30]

    # 创建文件名（使用ASCII安全的名称）
    file_name = f"题-{next_number:03d}-ABOC-Ch{chapter}-T{exercise_number}.md"

    # 创建文件内容
    file_content = f"""---
title: {file_name}
type: 题目
source: ABOC 第{chapter}章 章末习题（ARX's Basic Organic Chemistry 第3版）
subject: 有机化学
module: 基础要求-有机化学
submodule: Ch.{chapter}
question_type: 合成设计题
difficulty: 3
teaching_level: 拓展
exam_stage: 初赛
syllabus_codes: ["{31 + chapter - 1}"]
knowledge_points: ["[[]]"]
tags: [化竞, ABOC, 有机化学]
aliases: [ABOC-Ch{chapter}-T{exercise_number}]
updated: 2026-07-04
---

# 题-{next_number:03d}：{exercise_content.strip()[:50]}

> **来源**：ABOC 第{chapter}章 章末习题 T{exercise_number}
> **难度**：⭐⭐⭐
> **教学层级**：拓展

---

## 题目

{exercise_content}

---

## 答案

（答案见 [[提炼-ABOC-第12章-习题解析]]）

---

## 解题思路

（待补充）

---

## 知识点

- [[]]

---

## 相关题目

- [[题-053-ABOC-Ch1-T1-金刚烷合成]]
- [[题-054-ABOC-Ch2-T3-硫叶立德vs半缩硫醛选择性]]
- [[题-055-ABOC-Ch3-T3-特殊氧化烯烃邻二醇切断]]
"""

    # 写入文件
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)

    print(f"Created: {file_name}")
    next_number += 1

print(f"Done! Created {next_number - 80} files")