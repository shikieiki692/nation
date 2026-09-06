#!/usr/bin/env python3
"""
将题目文件中的图片引用从源文件格式转换为 Obsidian 格式
![](path/images/file.jpg) -> ![[file.jpg]]
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

def convert_image_references(file_path):
    """将文件中的图片引用转换为 Obsidian 格式"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 ![](path/images/file.jpg) 格式
    pattern = r'!\[\]\(([^)]+_images/[^)]+)\)'

    def replace_image(match):
        img_path = match.group(1)
        # 提取文件名
        img_filename = Path(img_path).name
        # 转换为 Obsidian 格式
        return f'![[{img_filename}]]'

    new_content = re.sub(pattern, replace_image, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    """主函数"""
    print("开始转换图片引用格式...")

    updated_count = 0

    for question_dir in QUESTION_DIRS:
        if not question_dir.exists():
            continue

        print(f"\n处理目录: {question_dir}")

        for file_path in question_dir.glob("题-*.md"):
            if convert_image_references(file_path):
                updated_count += 1
                print(f"  已转换: {file_path.name}")

    print(f"\n完成! 共转换了 {updated_count} 个文件")

if __name__ == "__main__":
    main()
