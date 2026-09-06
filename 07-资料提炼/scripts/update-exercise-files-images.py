#!/usr/bin/env python3
"""
更新上海中学竞赛课程和化学竞赛初赛讲义题目文件，添加图片引用
"""

import os
import re
from pathlib import Path

# 配置
SHANGHAI_DIR = Path("04-题库/教材习题/上海中学竞赛课程")
COMPETITION_DIR = Path("04-题库/教材习题/化学竞赛初赛讲义")
SHANGHAI_SOURCE = Path("上海中学竞赛教程/（已压缩）上海中学竞赛课程-化学-第3分册_1-150.md")
COMPETITION_SOURCE = Path("化学竞赛初赛讲义/（已压缩）1-50.md")

def find_images_in_source(source_file):
    """从源文件中找到所有图片引用及其位置"""
    if not source_file.exists():
        return []

    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 ![](path/images/...) 格式的图片
    image_pattern = r'!\[\]\(([^)]+_images/[^)]+)\)'
    return [(m.start(), m.group(1)) for m in re.finditer(image_pattern, content)]

def find_exercise_with_images(source_content, all_images):
    """找到每个习题附近的图片"""
    exercise_images = {}

    # 查找所有习题标记
    exercise_patterns = [
        (r'(\d+)\.\s+', 'numbered'),  # 编号习题
    ]

    for pattern, ex_type in exercise_patterns:
        for match in re.finditer(pattern, source_content):
            exercise_start = match.start()
            exercise_num = match.group(1)

            # 查找该习题后的图片
            nearby_images = []
            for img_pos, img_path in all_images:
                if exercise_start <= img_pos <= exercise_start + 1500:
                    nearby_images.append(img_path)

            if nearby_images:
                exercise_images[exercise_num] = nearby_images

    return exercise_images

def update_exercise_files(exercise_dir, exercise_images):
    """更新题目文件，添加图片引用"""
    updated_count = 0

    for file_path in exercise_dir.glob("题-*.md"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已经有图片
        if '![[media/' in content or '![](' in content:
            continue

        # 从文件名中提取习题编号
        file_name = file_path.stem
        # 匹配习题编号，如 习题4, 习题1.2 等
        id_match = re.search(r'习题(\d+)', file_name)
        if id_match:
            exercise_num = id_match.group(1)

            # 检查该习题是否有图片
            if exercise_num in exercise_images:
                images = exercise_images[exercise_num]

                # 构建图片引用
                image_refs = '\n'.join([f'![[{Path(img).name}]]' for img in images])

                # 在题目部分添加图片
                if '## 题目' in content:
                    parts = content.split('## 题目')
                    if len(parts) == 2:
                        # 在题目内容后添加图片
                        question_part = parts[1].split('---')[0]
                        if '下图' in question_part or '如图' in question_part or '装置图' in question_part:
                            content = parts[0] + '## 题目' + question_part + '\n\n' + image_refs + '\n\n---' + parts[1].split('---', 1)[1]

                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            updated_count += 1
                            print(f"已更新: {file_path.name} (添加了 {len(images)} 张图片)")

    return updated_count

def main():
    """主函数"""
    print("开始更新题目文件...")

    # 处理上海中学竞赛课程
    print("\n=== 上海中学竞赛课程 ===")
    if SHANGHAI_SOURCE.exists():
        all_images = find_images_in_source(SHANGHAI_SOURCE)
        print(f"找到 {len(all_images)} 个图片引用")

        with open(SHANGHAI_SOURCE, 'r', encoding='utf-8') as f:
            source_content = f.read()

        exercise_images = find_exercise_with_images(source_content, all_images)
        print(f"找到 {len(exercise_images)} 个习题有图片")

        updated = update_exercise_files(SHANGHAI_DIR, exercise_images)
        print(f"更新了 {updated} 个文件")

    # 处理化学竞赛初赛讲义
    print("\n=== 化学竞赛初赛讲义 ===")
    if COMPETITION_SOURCE.exists():
        all_images = find_images_in_source(COMPETITION_SOURCE)
        print(f"找到 {len(all_images)} 个图片引用")

        with open(COMPETITION_SOURCE, 'r', encoding='utf-8') as f:
            source_content = f.read()

        exercise_images = find_exercise_with_images(source_content, all_images)
        print(f"找到 {len(exercise_images)} 个习题有图片")

        updated = update_exercise_files(COMPETITION_DIR, exercise_images)
        print(f"更新了 {updated} 个文件")

    print("\n完成!")

if __name__ == "__main__":
    main()
