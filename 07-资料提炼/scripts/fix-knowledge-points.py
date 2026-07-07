#!/usr/bin/env python3
"""
修复题目文件中的知识点格式问题
"""

import os
import re
from pathlib import Path

# 配置
QUESTION_DIRS = [
    Path("04-题库/教材习题/上海中学竞赛课程"),
    Path("04-题库/教材习题/化学竞赛初赛讲义"),
    Path("04-题库/教材习题/ABOC"),
]

def fix_knowledge_points(file_path):
    """修复文件中的知识点格式"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找knowledge_points字段
    # 匹配 knowledge_points: [...] 格式，包括可能的重复内容
    pattern = r'knowledge_points:\s*\[.*?\](?:\]\'?,?\s*\'?\[.*?\])*'

    def replace_knowledge_points(match):
        # 提取第一个有效的知识点列表
        first_match = re.search(r'knowledge_points:\s*\[(.*?)\]', match.group(0))
        if first_match:
            # 提取知识点内容
            points_str = first_match.group(1)
            # 清理格式
            points = re.findall(r"'\[\[(.*?)\]\]'|\"\\[\\[(.*?)\\]\\]\"", points_str)
            clean_points = []
            for p in points:
                point = p[0] or p[1]
                if point:
                    clean_points.append(f'[[{point}]]')

            if clean_points:
                return f'knowledge_points: {clean_points}'
            else:
                return match.group(0)  # 如果无法解析，返回原内容
        else:
            return match.group(0)

    new_content = re.sub(pattern, replace_knowledge_points, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    """主函数"""
    print("开始修复知识点格式...")

    fixed_count = 0

    for question_dir in QUESTION_DIRS:
        if not question_dir.exists():
            continue

        print(f"\n处理目录: {question_dir}")

        for file_path in question_dir.glob("题-*.md"):
            if fix_knowledge_points(file_path):
                fixed_count += 1
                print(f"  已修复: {file_path.name}")

    print(f"\n完成! 共修复了 {fixed_count} 个文件")

if __name__ == "__main__":
    main()
