# -*- coding: utf-8 -*-
"""
化学竞赛初赛讲义习题提取脚本
从化学竞赛初赛讲义中提取习题
"""

import re
import os

# 源文件路径
source_files = [
    r"C:\Obsidion\妙妙屋\化学竞赛初赛讲义\（已压缩）1-50.md",
    r"C:\Obsidion\妙妙屋\化学竞赛初赛讲义\（已压缩）51-100.md",
    r"C:\Obsidion\妙妙屋\化学竞赛初赛讲义\（已压缩）101-150.md",
    r"C:\Obsidion\妙妙屋\化学竞赛初赛讲义\（已压缩）151-200.md",
    r"C:\Obsidion\妙妙屋\化学竞赛初赛讲义\（已压缩）201-250.md",
    r"C:\Obsidion\妙妙屋\化学竞赛初赛讲义\（已压缩）251-300.md",
    r"C:\Obsidion\妙妙屋\化学竞赛初赛讲义\（已压缩）301-350.md",
    r"C:\Obsidion\妙妙屋\化学竞赛初赛讲义\（已压缩）351-400.md"
]
output_dir = r"C:\Obsidion\妙妙屋\04-题库\教材习题\化学竞赛初赛讲义"

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 读取所有源文件
all_content = ""
for source_file in source_files:
    with open(source_file, 'r', encoding='utf-8') as f:
        all_content += f.read() + "\n"

# 定义章节映射
chapter_map = {
    "第1讲": "反应方程式",
    "第2讲": "原子结构",
    "第3讲": "分子结构",
    "第4讲": "配合物",
    "第5讲": "金属有机化学",
    "第6讲": "推断技术",
    "第7讲": "晶体结构",
    "第8讲": "热力学和动力学初步",
    "第9讲": "溶液与化学分析",
    "第10讲": "有机化学基本原理",
    "第11讲": "人名反应与机理推断",
    "第12讲": "有机波谱学初步",
    "第13讲": "高分子化学简介",
    "附录A": "元素化学复习问题",
    "附录B": "有机化学知识要点"
}

# 提取习题的正则表达式
exercise_pattern = r"【习题(\d+\.\d+)】(.*?)(?=【习题\d|## |\Z)"

# 计数器
next_number = 1

# 按章节提取习题
for chapter_name, chapter_topic in chapter_map.items():
    # 查找章节内容
    chapter_pattern = rf"## {chapter_name}.*?(?=## 第\d+讲|## 附录[AB]|\Z)"
    chapter_matches = re.findall(chapter_pattern, all_content, re.DOTALL)

    if not chapter_matches:
        print(f"Warning: Could not find chapter {chapter_name}")
        continue

    chapter_content = chapter_matches[0]

    # 提取习题
    exercises = re.findall(exercise_pattern, chapter_content, re.MULTILINE | re.DOTALL)

    print(f"Found {len(exercises)} exercises in {chapter_name}")

    for exercise_id, exercise_content in exercises:
        # 清理内容
        exercise_content = exercise_content.strip()

        # 创建文件名
        file_name = f"题-{next_number:03d}-初赛讲义-{chapter_topic}-习题{exercise_id}.md"

        # 创建文件内容
        file_content = f"""---
title: {file_name}
type: 题目
source: 化学竞赛初赛讲义·{chapter_name}·{chapter_topic}
subject: 无机化学
module: 化学原理
submodule: {chapter_topic}
question_type: 计算题
difficulty: 3
teaching_level: 拓展
exam_stage: 初赛
syllabus_codes: ["1"]
knowledge_points: ["[[]]"]
tags: [化竞, 初赛讲义, {chapter_topic}]
aliases: [初赛讲义-{chapter_topic}-习题{exercise_id}]
updated: 2026-07-04
---

# 题-{next_number:03d}：{exercise_content[:50]}...

> **来源**：化学竞赛初赛讲义·{chapter_name} 习题{exercise_id}
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

- [[题-001-初赛讲义-反应方程式-习题1.2]]
"""

        # 写入文件
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)

        print(f"Created: {file_name}")
        next_number += 1

print(f"Done! Created {next_number - 1} files")