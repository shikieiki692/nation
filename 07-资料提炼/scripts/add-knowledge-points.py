# -*- coding: utf-8 -*-
"""
知识点标签补充脚本
为新提取的题目添加知识点标签
"""

import re
import os

# 题库目录
question_dirs = [
    r"C:\Obsidion\妙妙屋\04-题库\教材习题\上海中学竞赛课程",
    r"C:\Obsidion\妙妙屋\04-题库\教材习题\化学竞赛初赛讲义"
]

# 知识点映射表
knowledge_point_map = {
    # 上海中学竞赛课程
    "卤族元素": ["卤素", "卤化物", "氧化还原", "滴定分析"],
    "氧族元素": ["氧族元素", "硫化学", "氧化还原"],
    "氮族元素": ["氮族元素", "磷化学", "氨"],
    "碱金属碱土金属": ["碱金属", "碱土金属", "离子晶体"],
    "过渡金属": ["过渡金属", "d区元素", "配合物"],

    # 化学竞赛初赛讲义
    "反应方程式": ["化学方程式", "氧化还原", "配平"],
    "原子结构": ["原子结构", "电子排布", "量子数"],
    "分子结构": ["分子结构", "化学键", "VSEPR", "杂化轨道"],
    "配合物": ["配合物", "配位键", "晶体场理论"],
    "金属有机化学": ["金属有机", "有机金属", "催化"],
    "推断技术": ["元素推断", "物质推断", "逻辑推理"],
    "晶体结构": ["晶体结构", "晶胞", "X射线衍射"],
    "热力学和动力学初步": ["热力学", "动力学", "化学平衡", "反应速率"],
    "溶液与化学分析": ["溶液", "分析化学", "滴定", "光度法"],
    "有机化学基本原理": ["有机化学", "反应机理", "官能团"],
    "人名反应与机理推断": ["人名反应", "反应机理", "有机合成"],
    "有机波谱学初步": ["波谱分析", "NMR", "IR", "质谱"],
    "高分子化学简介": ["高分子", "聚合反应", "高分子材料"],
    "元素化学复习问题": ["元素化学", "主族元素", "过渡金属"],
    "有机化学知识要点": ["有机化学", "反应类型", "官能团"]
}

# 计数器
updated_count = 0

# 处理每个题库目录
for question_dir in question_dirs:
    # 获取所有题目文件
    question_files = [f for f in os.listdir(question_dir) if f.startswith("题-") and f.endswith(".md")]

    for file_name in question_files:
        file_path = os.path.join(question_dir, file_name)

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已有知识点标签
        if "knowledge_points:" in content:
            # 检查知识点是否为空
            if '["[[]]"]' in content or "['[[]]']" in content:
                # 需要补充知识点
                pass
            else:
                # 已有知识点，跳过
                continue

        # 提取submodule信息
        submodule_match = re.search(r"submodule:\s*(.+)", content)
        if not submodule_match:
            continue

        submodule = submodule_match.group(1).strip()

        # 获取对应的知识点
        knowledge_points = knowledge_point_map.get(submodule, [])

        if not knowledge_points:
            continue

        # 创建新的知识点标签
        new_knowledge_points = str(["[[" + kp + "]]" for kp in knowledge_points])

        # 替换旧的知识点标签
        new_content = re.sub(
            r'knowledge_points:\s*\[.*?\]',
            f'knowledge_points: {new_knowledge_points}',
            content
        )

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Updated: {file_name} -> {knowledge_points}")
        updated_count += 1

print(f"Done! Updated {updated_count} files")