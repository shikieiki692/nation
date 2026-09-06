#!/usr/bin/env python3
"""
批量修复知识点格式错误的文件 - 使用简单的字符串替换
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

    # 使用简单的字符串替换来修复格式
    # 查找所有 knowledge_points 行
    lines = content.split('\n')
    fixed = False

    for i, line in enumerate(lines):
        if line.startswith('knowledge_points:'):
            # 提取所有 [[...]] 格式的知识点
            points = re.findall(r'\[\[([^\]]+)\]\]', line)

            if points:
                # 去重并保持顺序
                seen = set()
                unique_points = []
                for point in points:
                    if point not in seen:
                        seen.add(point)
                        unique_points.append(f'[[{point}]]')

                # 格式化为正确的YAML列表
                new_line = f'knowledge_points: {unique_points}'
                lines[i] = new_line
                fixed = True

    if fixed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
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
