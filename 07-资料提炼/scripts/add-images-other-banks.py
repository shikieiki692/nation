#!/usr/bin/env python3
"""
为上海中学竞赛课程和化学竞赛初赛讲义题目文件添加图片引用
"""

import os
import re
import shutil
from pathlib import Path

# 配置
SHANGHAI_DIR = Path("04-题库/教材习题/上海中学竞赛课程")
COMPETITION_DIR = Path("04-题库/教材习题/化学竞赛初赛讲义")
SHANGHAI_SOURCE = Path("上海中学竞赛教程/（已压缩）上海中学竞赛课程-化学-第3分册_1-150.md")
COMPETITION_SOURCE = Path("化学竞赛初赛讲义/（已压缩）1-50.md")
MEDIA_DIR = Path("media")

def find_images_in_source(source_file):
    """从源文件中找到所有图片引用"""
    if not source_file.exists():
        return []

    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 ![](path/images/...) 格式的图片
    image_pattern = r'!\[\]\(([^)]+_images/[^)]+)\)'
    return [(m.start(), m.group(1)) for m in re.finditer(image_pattern, content)]

def find_exercises_near_images(source_content, all_images):
    """找到所有包含图片的习题"""
    exercises_with_images = {}

    # 查找所有习题
    exercise_patterns = [
        (r'##\s*本讲习题', '本讲习题'),
        (r'【习题\s*(\d+\.\d+\*?)】', '习题'),
    ]

    for pattern, ex_type in exercise_patterns:
        for match in re.finditer(pattern, source_content):
            exercise_start = match.start()

            # 查找该习题后的图片
            nearby_images = []
            for img_pos, img_path in all_images:
                if exercise_start <= img_pos <= exercise_start + 2000:
                    nearby_images.append(img_path)

            if nearby_images:
                exercises_with_images[match.group(0)] = nearby_images

    return exercises_with_images

def copy_image_to_media(img_path):
    """将图片复制到 media 目录"""
    # 提取文件名
    img_filename = Path(img_path).name

    # 检查源文件是否存在
    if Path(img_path).exists():
        source_img = Path(img_path)
    else:
        # 尝试在源目录中查找
        source_dirs = [
            Path("上海中学竞赛教程/（已压缩）上海中学竞赛课程-化学-第3分册_1-150_images"),
            Path("化学竞赛初赛讲义/（已压缩）1-50_images"),
        ]
        source_img = None
        for d in source_dirs:
            if (d / img_filename).exists():
                source_img = d / img_filename
                break

    if source_img and source_img.exists():
        # 复制到 media 目录
        dest_img = MEDIA_DIR / img_filename
        if not dest_img.exists():
            shutil.copy2(source_img, dest_img)
            print(f"  复制图片: {img_filename}")
        return True
    else:
        print(f"  警告: 找不到源图片 {img_filename}")
        return False

def main():
    """主函数"""
    print("开始处理上海中学竞赛课程和化学竞赛初赛讲义的图片...")

    # 确保 media 目录存在
    MEDIA_DIR.mkdir(exist_ok=True)

    # 处理上海中学竞赛课程
    print("\n=== 上海中学竞赛课程 ===")
    if SHANGHAI_SOURCE.exists():
        all_images = find_images_in_source(SHANGHAI_SOURCE)
        print(f"找到 {len(all_images)} 个图片引用")

        with open(SHANGHAI_SOURCE, 'r', encoding='utf-8') as f:
            source_content = f.read()

        exercises_with_images = find_exercises_near_images(source_content, all_images)
        print(f"找到 {len(exercises_with_images)} 个包含图片的习题")

        # 复制图片到 media 目录
        for ex_marker, imgs in exercises_with_images.items():
            for img in imgs:
                copy_image_to_media(img)

    # 处理化学竞赛初赛讲义
    print("\n=== 化学竞赛初赛讲义 ===")
    if COMPETITION_SOURCE.exists():
        all_images = find_images_in_source(COMPETITION_SOURCE)
        print(f"找到 {len(all_images)} 个图片引用")

        with open(COMPETITION_SOURCE, 'r', encoding='utf-8') as f:
            source_content = f.read()

        exercises_with_images = find_exercises_near_images(source_content, all_images)
        print(f"找到 {len(exercises_with_images)} 个包含图片的习题")

        # 复制图片到 media 目录
        for ex_marker, imgs in exercises_with_images.items():
            for img in imgs:
                copy_image_to_media(img)

    print("\n完成!")

if __name__ == "__main__":
    main()
