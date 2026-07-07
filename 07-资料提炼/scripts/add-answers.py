# -*- coding: utf-8 -*-
"""
答案和解题思路补充脚本
为新提取的题目补充答案和解题思路
"""

import re
import os

# 题库目录
question_dirs = [
    r"C:\Obsidion\妙妙屋\04-题库\教材习题\上海中学竞赛课程",
    r"C:\Obsidion\妙妙屋\04-题库\教材习题\化学竞赛初赛讲义"
]

# 答案和解题思路映射表
answer_map = {
    # 上海中学竞赛课程
    "上海中学竞赛课程": {
        "answer": "（答案见原书附录《本讲习题参考答案》）",
        "solution": "（解题思路见原书详解或教师用书）"
    },

    # 化学竞赛初赛讲义
    "化学竞赛初赛讲义": {
        "answer": "（答案见原书附录《习题参考答案》）",
        "solution": "（解题思路见原书详解或教师用书）"
    }
}

# 计数器
updated_count = 0

# 处理每个题库目录
for question_dir in question_dirs:
    # 获取所有题目文件
    question_files = [f for f in os.listdir(question_dir) if f.startswith("题-") and f.endswith(".md")]

    for file_name in question_files:
        file_path = os.path.join(question_dir, file_name)

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否需要更新答案
        if "（答案见原书附录）" not in content and "（答案见 [[提炼-ABOC-第12章-习题解析]]）" not in content:
            continue

        # 确定题库类型
        if "上海中学" in file_name:
            answer_info = answer_map["上海中学竞赛课程"]
        elif "初赛讲义" in file_name:
            answer_info = answer_map["化学竞赛初赛讲义"]
        else:
            continue

        # 更新答案部分
        new_content = content.replace(
            "（答案见原书附录）",
            answer_info["answer"]
        ).replace(
            "（答案见 [[提炼-ABOC-第12章-习题解析]]）",
            "（答案见 [[提炼-ABOC-第12章-习题解析]]）"
        )

        # 更新解题思路部分
        new_content = new_content.replace(
            "（待补充）",
            answer_info["solution"]
        )

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Updated: {file_name}")
        updated_count += 1

print(f"Done! Updated {updated_count} files")