# -*- coding: utf-8 -*-
"""
上海中学竞赛课程习题提取脚本
从上海中学竞赛课程第三分册中提取习题
"""

import re
import os

# 源文件路径
source_files = [
    r"C:\Obsidion\妙妙屋\上海中学竞赛教程\（已压缩）上海中学竞赛课程-化学-第3分册_1-150.md",
    r"C:\Obsidion\妙妙屋\上海中学竞赛教程\（已压缩）上海中学竞赛课程-化学-第3分册_151-277.md"
]
output_dir = r"C:\Obsidion\妙妙屋\04-题库\教材习题\上海中学竞赛课程"

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 读取所有源文件
all_content = ""
for source_file in source_files:
    with open(source_file, 'r', encoding='utf-8') as f:
        all_content += f.read() + "\n"

# 定义章节映射
chapter_map = {
    "第一讲": "卤族元素",
    "第二讲": "氧族元素",
    "第三讲": "氮族元素",
    "第四讲": "碳族硼族元素",
    "第五讲": "碱金属碱土金属",
    "第六讲": "过渡金属"
}

# 提取习题的正则表达式
exercise_pattern = r"^(\d+)\.\s+(.*?)(?=^\d+\.|^## |\Z)"

# 计数器
next_number = 1

# 按章节提取习题
for chapter_name, chapter_topic in chapter_map.items():
    # 查找章节内容
    chapter_pattern = rf"## {chapter_name}.*?## {chapter_name}.*?(?=## 第[一二三四五六七八九十]讲|\Z)"
    chapter_matches = re.findall(chapter_pattern, all_content, re.DOTALL)

    if not chapter_matches:
        # 尝试更宽松的匹配
        chapter_pattern = rf"## {chapter_name}.*?(?=## 第[一二三四五六七八九十]讲|\Z)"
        chapter_matches = re.findall(chapter_pattern, all_content, re.DOTALL)

    if not chapter_matches:
        print(f"Warning: Could not find chapter {chapter_name}")
        continue

    chapter_content = chapter_matches[0]

    # 查找"本讲习题"部分
    exercise_section_pattern = r"## 本讲习题.*?(?=## 第[一二三四五六七八九十]讲|\Z)"
    exercise_section_matches = re.findall(exercise_section_pattern, chapter_content, re.DOTALL)

    if not exercise_section_matches:
        print(f"Warning: Could not find exercise section in {chapter_name}")
        continue

    exercise_section = exercise_section_matches[0]

    # 提取习题
    exercises = re.findall(exercise_pattern, exercise_section, re.MULTILINE | re.DOTALL)

    print(f"Found {len(exercises)} exercises in {chapter_name}")

    for exercise_number, exercise_content in exercises:
        # 清理内容
        exercise_content = exercise_content.strip()

        # 创建文件名
        file_name = f"题-{next_number:03d}-上海中学-{chapter_topic}-习题{exercise_number}.md"

        # 创建文件内容
        file_content = f"""---
title: {file_name}
type: 题目
source: 上海中学竞赛课程·化学·第3分册·{chapter_name}（{chapter_topic}）
subject: 无机化学
module: 元素化学
submodule: {chapter_topic}
question_type: 计算题
difficulty: 3
teaching_level: 拓展
exam_stage: 初赛
syllabus_codes: ["13"]
knowledge_points: ["[[]]"]
tags: [化竞, 上海中学, 元素化学, {chapter_topic}]
aliases: [上海中学-{chapter_topic}-习题{exercise_number}]
updated: 2026-07-04
---

# 题-{next_number:03d}：{exercise_content[:50]}...

> **来源**：上海中学竞赛课程·化学·第3分册·{chapter_name} 习题{exercise_number}
> **难度**：⭐⭐⭐
> **教学层级**：拓展

---

## 题目

{exercise_content}

---

## 答案

（答案见原书附录）

---

## 解题思路

（待补充）

---

## 知识点

- [[]]

---

## 相关题目

- [[题-001-上海中学-卤族元素-习题1]]
"""

        # 写入文件
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)

        print(f"Created: {file_name}")
        next_number += 1

print(f"Done! Created {next_number - 1} files")