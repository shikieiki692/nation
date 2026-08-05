import re

hashes = [
    "0c40c0b603740e2ffccf0ca6ab4238b20e92b10b44742844bf527d9c0eaec89c",
    "354ad43893e642e45323ddf05b41e5afa1d7bfc08a6e252f439e97449bf4b89e",
    "302648eb1418cf36009f1c1df8fbbdc4055ec028c0a1fc4f09d6c020fb9a6582",
    "ccbb478aa79d4d2f6bc38505f1c68a082ea7a6158c74ba60be9127f5621fb0e5",
    "82b921bc60387ae7e340b9453c7db27a1a96fef22a985a2dea3adb8da0dbeadd",
    "56776f0f0701b96713fa347c3779345d437b666b1af2d52d5c7f3ca0f0cb788f",
    "73144e9020c0a35f6c6cec4555dd493e453b7fdb5b8fff2a5024d7720e2e4520"
]

captions = [
    "*图 1 物化综合解题武器库与计算桥梁*",
    "*图 2 LiF 晶体生成的 Born-Haber 循环热力学步骤*",
    "*图 3 X-H 键均裂 BDE 的三步拆解热化学循环*",
    "*图 4 Fe-H₂O 体系的 Pourbaix (E-pH) 图及水稳定区*",
    "*图 5 稳态近似决策树与不同速率常数关系的分支结论*",
    "*图 6 综合题热力学路径图 (电势至平衡常数ICE)*",
    "*图 7 Ag⁺ 基础电对与沉淀/配位平衡联立的三层路径图*"
]

filepath = r"C:\Obsidion\妙妙屋\04-课件\学生讲义\物化综合计算-超级充实版（自学完整）.md"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Update frontmatter
text = re.sub(r'has_images:\s*false', 'has_images: true', text)
text = re.sub(r'image_count:\s*0', 'image_count: 7', text)

# Replace placeholders
for i in range(1, 8):
    placeholder_pattern = re.compile(r'📌\s*\*\*图片待补（图\s*' + str(i) + r'）\*\*')
    replacement = f'<span class="claudian-embedded-image-fallback">![[{hashes[i-1]}.png]]</span>\n{captions[i-1]}'
    
    if placeholder_pattern.search(text):
        text = placeholder_pattern.sub(replacement, text)
        print(f"Replaced Fig {i}")
    else:
        print(f"Fig {i} placeholder not found!")
        
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)
