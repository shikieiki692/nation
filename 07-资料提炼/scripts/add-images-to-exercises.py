#!/usr/bin/env python3
"""
为 ABOC 题目文件添加图片引用
从源文件中提取图片，并添加到对应的题目文件中
"""

import os
import re
from pathlib import Path

# 配置
ABOC_DIR = Path("04-题库/教材习题/ABOC")
SOURCE_FILE = Path("mineru/03-教材书籍/ABOC有机化学/ABOC202505_1-200.md")
SOURCE_FILE2 = Path("mineru/03-教材书籍/ABOC有机化学/ABOC202505_200-397.md")

def read_source_files():
    """读取源文件内容"""
    content1 = ""
    content2 = ""

    if SOURCE_FILE.exists():
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            content1 = f.read()

    if SOURCE_FILE2.exists():
        with open(SOURCE_FILE2, 'r', encoding='utf-8') as f:
            content2 = f.read()

    return content1 + content2

def extract_images_from_source(source_content):
    """从源文件中提取图片引用"""
    # 匹配 ![[...images/...]] 格式的图片
    image_pattern = r'!\[\[(ABOC\d{4}_\d+-\d+_images/[^\]]+)\]\]'
    return re.findall(image_pattern, source_content)

def find_exercise_images(source_content, exercise_id):
    """为指定习题找到对应的图片"""
    images = []

    # 查找习题位置
    exercise_patterns = [
        rf'自学练习\s+{re.escape(exercise_id)}',
        rf'T{exercise_id}\.',
        rf'【习题\s*{re.escape(exercise_id)}】',
    ]

    for pattern in exercise_patterns:
        matches = list(re.finditer(pattern, source_content))
        if matches:
            # 找到习题后，搜索附近的图片
            for match in matches:
                start = match.start()
                # 在习题后500字符内查找图片
                search_text = source_content[start:start+1000]
                image_matches = re.findall(r'!\[\[(ABOC\d{4}_\d+-\d+_images/[^\]]+)\]\]', search_text)
                images.extend(image_matches)
            break

    return images

def update_exercise_file(file_path, images):
    """更新题目文件，添加图片引用"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经有图片
    if '![[ABOC' in content:
        return False

    # 在题目部分添加图片
    if images:
        # 构建图片引用
        image_refs = '\n'.join([f'![[{img}]]' for img in images])

        # 在"## 题目"部分后添加图片
        if '## 题目' in content:
            parts = content.split('## 题目')
            if len(parts) == 2:
                # 在题目内容后添加图片
                question_part = parts[1].split('---')[0]
                if '下图' in question_part or '如图' in question_part:
                    content = parts[0] + '## 题目' + question_part + '\n\n' + image_refs + '\n\n---' + parts[1].split('---', 1)[1]

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return True

    return False

def main():
    """主函数"""
    print("开始为 ABOC 题目添加图片...")

    # 读取源文件
    source_content = read_source_files()
    print(f"源文件长度: {len(source_content)} 字符")

    # 获取所有题目文件
    exercise_files = list(ABOC_DIR.glob("题-*.md"))
    print(f"找到 {len(exercise_files)} 个题目文件")

    updated_count = 0

    for file_path in exercise_files:
        # 从文件名中提取习题ID
        file_name = file_path.stem
        # 匹配习题ID，如 1.1.2, 1.2.2-1 等
        id_match = re.search(r'Ch\d+-(\d+\.\d+(?:\.\d+)?(?:-\d+)?)', file_name)
        if id_match:
            exercise_id = id_match.group(1)

            # 查找对应的图片
            images = find_exercise_images(source_content, exercise_id)

            if images:
                # 更新文件
                if update_exercise_file(file_path, images):
                    updated_count += 1
                    print(f"已更新: {file_path.name} (添加了 {len(images)} 张图片)")

    print(f"\n完成! 共更新了 {updated_count} 个文件")

if __name__ == "__main__":
    main()
