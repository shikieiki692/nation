#!/usr/bin/env python3
import re
from pathlib import Path

def fix_image_references():
    """修复图片引用格式"""
    base_dir = Path('C:/Obsidion/妙妙屋')
    question_dir = base_dir / '04-题库' / '教材习题' / '结构化学基础'
    
    # 需要修复的文件
    files_to_fix = [
        '题-196-结构化学基础-晶体结构-习题7.15.md',
        '题-218-结构化学基础-金属晶体-习题8.1.md',
        '题-242-结构化学基础-金属晶体-习题8.25.md',
        '题-251-结构化学基础-离子化合物-习题9.9.md'
    ]
    
    for filename in files_to_fix:
        filepath = question_dir / filename
        if not filepath.exists():
            print(f"文件不存在: {filename}")
            continue
        
        content = filepath.read_text(encoding='utf-8')
        
        # 查找图片引用格式错误
        # 匹配 ![](xxx 或 ![](xxx.jpg)
        pattern = r'!\[\]\(([^)]+)\)'
        matches = re.findall(pattern, content)
        
        if matches:
            print(f"修复 {filename}:")
            for match in matches:
                # 提取文件名部分
                if '/' in match:
                    # 路径格式，提取文件名
                    img_filename = match.split('/')[-1]
                else:
                    img_filename = match
                
                # 确保文件名以.jpg结尾
                if not img_filename.endswith('.jpg'):
                    img_filename += '.jpg'
                
                # 替换为wikilink格式
                old_ref = f'![]({match})'
                new_ref = f'![[{img_filename}]]'
                
                content = content.replace(old_ref, new_ref)
                print(f"  {old_ref} -> {new_ref}")
            
            # 保存修改
            filepath.write_text(content, encoding='utf-8')
            print(f"  已保存: {filename}")
        else:
            print(f"未找到图片引用错误: {filename}")

if __name__ == '__main__':
    fix_image_references()