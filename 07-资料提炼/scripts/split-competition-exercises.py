# -*- coding: utf-8 -*-
"""
化学竞赛初赛讲义合并题目拆分脚本
拆分包含多道习题的文件，使其成为独立文件
"""

import re
import os

# 题库目录
question_dir = r"C:\Obsidion\妙妙屋\04-题库\教材习题\化学竞赛初赛讲义"

# 获取所有题目文件
question_files = [f for f in os.listdir(question_dir) if f.startswith("题-") and f.endswith(".md")]

# 计数器
split_count = 0

# 处理每个文件
for file_name in question_files:
    file_path = os.path.join(question_dir, file_name)

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否包含多道习题
    exercise_matches = re.findall(r"【习题\s*(\d+\.\d+\*?)】", content)

    if len(exercise_matches) <= 1:
        continue

    print(f"Splitting {file_name} ({len(exercise_matches)} questions)")

    # 提取frontmatter
    frontmatter_match = re.match(r"---\n(.*?)\n---\n", content, re.DOTALL)
    if not frontmatter_match:
        print(f"  Warning: No frontmatter found in {file_name}")
        continue

    frontmatter = frontmatter_match.group(1)

    # 提取题目部分（从第一个【习题到最后一个习题）
    first_exercise_pos = content.find("【习题")
    if first_exercise_pos == -1:
        continue

    # 提取所有习题
    exercise_pattern = r"【习题\s*(\d+\.\d+\*?)】(.*?)(?=【习题\s*\d|---\n## 答案|\Z)"
    exercises = re.findall(exercise_pattern, content[first_exercise_pos:], re.DOTALL)

    # 删除原文件
    os.remove(file_path)
    print(f"  Deleted: {file_name}")

    # 为每道习题创建新文件
    for exercise_id, exercise_content in exercises:
        exercise_content = exercise_content.strip()

        # 清理习题编号中的特殊字符
        clean_id = exercise_id.replace('*', '').replace(' ', '')

        # 创建新文件名
        new_file_name = file_name.replace(f"习题{exercise_matches[0]}", f"习题{clean_id}")

        # 如果原文件名不包含第一个习题编号，使用新的命名方式
        original_num_match = re.match(r"题-(\d+)-", file_name)
        if f"习题{exercise_matches[0]}" not in file_name:
            # 提取原文件名中的编号部分
            if original_num_match:
                original_num = original_num_match.group(1)
                new_file_name = f"题-{original_num}-初赛讲义-{file_name.split('-')[3]}-习题{clean_id}.md"

        # 创建新的frontmatter
        new_frontmatter = frontmatter.replace(
            f"习题{exercise_matches[0]}",
            f"习题{clean_id}"
        ).replace(
            f"aliases: [初赛讲义-{file_name.split('-')[3]}-习题{exercise_matches[0]}]",
            f"aliases: [初赛讲义-{file_name.split('-')[3]}-习题{clean_id}]"
        )

        # 创建新文件内容
        new_content = f"""---
{new_frontmatter}
---

# 题-{original_num_match.group(1) if original_num_match else '000'}：{exercise_content[:50]}...

> **来源**：化学竞赛初赛讲义 习题{clean_id}
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

        # 写入新文件
        new_file_path = os.path.join(question_dir, new_file_name)
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  Created: {new_file_name}")
        split_count += 1

print(f"Done! Split {split_count} questions from {len(question_files)} files")