#!/usr/bin/env python3
"""
为 ABOC 题目文件添加图片引用
从源文件中提取图片，复制到 media 目录，并添加到对应的题目文件中
"""

import os
import re
import shutil
from pathlib import Path

# 配置
ABOC_DIR = Path("04-题库/教材习题/ABOC")
SOURCE_FILE = Path("mineru/03-教材书籍/ABOC有机化学/ABOC202505_1-200.md")
SOURCE_FILE2 = Path("mineru/03-教材书籍/ABOC有机化学/ABOC202505_200-397.md")
SOURCE_IMG_DIR1 = Path("mineru/03-教材书籍/ABOC有机化学/ABOC202505_1-200_images")
SOURCE_IMG_DIR2 = Path("mineru/03-教材书籍/ABOC有机化学/ABOC202505_200-397_images")
MEDIA_DIR = Path("media")

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

def find_all_images_in_source(source_content):
    """从源文件中找到所有图片引用及其位置"""
    # 匹配 ![[...images/...]] 格式的图片（更宽松的匹配）
    image_pattern = r'!\[\[([^\]]+images/[^\]]+)\]\]'
    return [(m.start(), m.group(1)) for m in re.finditer(image_pattern, source_content)]

def find_exercises_with_images(source_content, all_images):
    """找到所有包含图片的习题"""
    exercises_with_images = {}

    # 查找所有习题
    exercise_patterns = [
        (r'自学练习\s+(\d+\.\d+(?:\.\d+)?)', '自学练习'),
        (r'#\s*T(\d+)\.', '章末习题'),
    ]

    for pattern, ex_type in exercise_patterns:
        for match in re.finditer(pattern, source_content):
            exercise_id = match.group(1)
            exercise_start = match.start()

            # 查找该习题后的图片
            nearby_images = []
            for img_pos, img_path in all_images:
                if exercise_start <= img_pos <= exercise_start + 1500:
                    nearby_images.append(img_path)

            if nearby_images:
                exercises_with_images[exercise_id] = nearby_images

    return exercises_with_images

def copy_image_to_media(img_path):
    """将图片复制到 media 目录"""
    # 从路径中提取文件名
    img_filename = Path(img_path).name

    # 检查源文件是否存在
    source_img = SOURCE_IMG_DIR1 / img_filename
    if not source_img.exists():
        source_img = SOURCE_IMG_DIR2 / img_filename

    if source_img.exists():
        # 复制到 media 目录
        dest_img = MEDIA_DIR / img_filename
        if not dest_img.exists():
            shutil.copy2(source_img, dest_img)
            print(f"  复制图片: {img_filename}")
        return True
    else:
        print(f"  警告: 找不到源图片 {img_filename}")
        return False

def update_exercise_file(file_path, images):
    """更新题目文件，添加图片引用"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经有图片
    if '![[ABOC' in content or '![[media/' in content:
        return False

    # 在题目部分添加图片
    if images:
        # 构建图片引用（使用 media 目录下的文件名）
        image_refs = '\n'.join([f'![[{Path(img).name}]]' for img in images])

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

    # 确保 media 目录存在
    MEDIA_DIR.mkdir(exist_ok=True)

    # 读取源文件
    source_content = read_source_files()
    print(f"源文件长度: {len(source_content)} 字符")

    # 找到所有图片
    all_images = find_all_images_in_source(source_content)
    print(f"找到 {len(all_images)} 个图片引用")

    # 找到包含图片的习题
    exercises_with_images = find_exercises_with_images(source_content, all_images)
    print(f"找到 {len(exercises_with_images)} 个包含图片的习题")

    # 显示一些示例
    for ex_id, imgs in list(exercises_with_images.items())[:3]:
        print(f"  习题 {ex_id}: {len(imgs)} 张图片")

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

            # 检查该习题是否有图片
            if exercise_id in exercises_with_images:
                images = exercises_with_images[exercise_id]

                # 复制图片到 media 目录
                for img in images:
                    copy_image_to_media(img)

                # 更新文件
                if update_exercise_file(file_path, images):
                    updated_count += 1
                    print(f"已更新: {file_path.name} (添加了 {len(images)} 张图片)")

    print(f"\n完成! 共更新了 {updated_count} 个文件")

if __name__ == "__main__":
    main()
