#!/usr/bin/env python3
"""
将所有题目文件中引用的图片复制到 media 目录
"""

import os
import re
import shutil
from pathlib import Path

# 配置
QUESTION_DIRS = [
    Path("04-题库/教材习题/上海中学竞赛课程"),
    Path("04-题库/教材习题/化学竞赛初赛讲义"),
    Path("04-题库/教材习题/ABOC"),
]

SOURCE_IMAGE_DIRS = [
    Path("上海中学竞赛教程/（已压缩）上海中学竞赛课程-化学-第3分册_1-150_images"),
    Path("化学竞赛初赛讲义/（已压缩）1-50_images"),
    Path("mineru/03-教材书籍/ABOC有机化学/ABOC202505_1-200_images"),
    Path("mineru/03-教材书籍/ABOC有机化学/ABOC202505_200-397_images"),
]

MEDIA_DIR = Path("media")

def find_image_references(file_path):
    """查找文件中的图片引用"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 ![[filename.jpg]] 格式
    pattern = r'!\[\[([^\]]+\.jpg)\]\]'
    return re.findall(pattern, content)

def copy_image_to_media(img_filename):
    """将图片复制到 media 目录"""
    dest_img = MEDIA_DIR / img_filename

    # 如果已经存在，跳过
    if dest_img.exists():
        return True

    # 在源目录中查找
    for source_dir in SOURCE_IMAGE_DIRS:
        source_img = source_dir / img_filename
        if source_img.exists():
            shutil.copy2(source_img, dest_img)
            return True

    return False

def main():
    """主函数"""
    print("开始复制图片到 media 目录...")

    # 确保 media 目录存在
    MEDIA_DIR.mkdir(exist_ok=True)

    copied_count = 0
    missing_count = 0

    for question_dir in QUESTION_DIRS:
        if not question_dir.exists():
            continue

        print(f"\n处理目录: {question_dir}")

        for file_path in question_dir.glob("题-*.md"):
            images = find_image_references(file_path)

            for img_filename in images:
                if copy_image_to_media(img_filename):
                    copied_count += 1
                    print(f"  已复制: {img_filename}")
                else:
                    missing_count += 1
                    print(f"  缺失: {img_filename} (文件: {file_path.name})")

    print(f"\n完成!")
    print(f"已复制: {copied_count} 张图片")
    print(f"缺失: {missing_count} 张图片")

if __name__ == "__main__":
    main()
