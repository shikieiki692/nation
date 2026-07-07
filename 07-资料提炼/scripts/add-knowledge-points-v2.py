#!/usr/bin/env python3
"""
为题目文件添加知识点标签
根据子模块和题目内容自动添加相关的知识点
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

# 知识点映射表
KNOWLEDGE_POINT_MAP = {
    # 上海中学竞赛课程
    "卤族元素": ["卤素", "卤化物", "氧化还原", "滴定分析"],
    "氧族元素": ["氧族元素", "硫化物", "硫酸", "氧化还原"],
    "氮族元素": ["氮族元素", "含氮化合物", "氧化还原", "酸碱平衡"],
    "碱金属碱土金属": ["碱金属", "碱土金属", "离子晶体", "焰色反应"],
    "过渡金属": ["过渡金属", "配合物", "晶体场理论", "氧化还原"],

    # 化学竞赛初赛讲义
    "反应方程式": ["化学方程式", "配平", "氧化还原"],
    "化学平衡": ["化学平衡", "平衡常数", "Le Chatelier原理"],
    "电化学": ["电化学", "原电池", "电解", "电极电位"],
    "热化学": ["热化学", "焓变", "熵变", "Gibbs自由能"],
    "溶液": ["溶液", "浓度", "依数性", "胶体"],
    "原子结构": ["原子结构", "电子构型", "周期律"],
    "分子结构": ["分子结构", "化学键", "分子轨道", "杂化"],
    "晶体结构": ["晶体结构", "晶格", "晶胞", "堆积"],
    "配位化合物": ["配合物", "配位键", "晶体场理论", "配位数"],
    "元素化学": ["元素化学", "主族元素", "过渡金属"],
    "有机化学基础": ["有机化学", "官能团", "反应机理"],
    "分析化学基础": ["分析化学", "滴定", "光谱分析"],

    # ABOC
    "Ch.1": ["结构基础", "Lewis酸碱", "电子效应", "碳正离子"],
    "Ch.2": ["基本反应", "氧化反应", "还原反应"],
    "Ch.3": ["烯烃加成", "亲电加成", "Markovnikov规则"],
    "Ch.4": ["取代反应", "消除反应", "SN1", "SN2", "E1", "E2"],
    "Ch.5": ["芳香族化合物", "芳香性", "亲电取代", "胺"],
    "Ch.6": ["缩合反应", "Aldol缩合", "Claisen缩合"],
    "Ch.7": ["周环反应", "Diels-Alder反应", "电环化反应"],
    "Ch.8": ["金属催化", "偶联反应", "Pd催化"],
    "Ch.9": ["杂环化合物", "杂环合成"],
    "Ch.10": ["光谱分析", "自由基反应"],
    "Ch.11": ["综合应用", "全合成"],
    "Ch.12": ["习题解析", "答案"],
}

def extract_knowledge_points(file_path):
    """根据文件内容提取知识点"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 从frontmatter中提取子模块
    submodule_match = re.search(r'submodule:\s*(.+)', content)
    if not submodule_match:
        return []

    submodule = submodule_match.group(1).strip()

    # 查找对应的知识点
    knowledge_points = []

    # 精确匹配
    if submodule in KNOWLEDGE_POINT_MAP:
        knowledge_points = KNOWLEDGE_POINT_MAP[submodule]
    else:
        # 模糊匹配
        for key, points in KNOWLEDGE_POINT_MAP.items():
            if key in submodule or submodule in key:
                knowledge_points = points
                break

    # 如果没有找到，根据题目内容推断
    if not knowledge_points:
        # 根据题目内容中的关键词推断
        keywords = {
            "滴定": ["滴定分析", "酸碱平衡"],
            "氧化还原": ["氧化还原", "电化学"],
            "平衡": ["化学平衡", "平衡常数"],
            "电极": ["电化学", "电极电位"],
            "配合物": ["配合物", "配位键"],
            "晶体": ["晶体结构", "晶格"],
            "有机": ["有机化学", "官能团"],
            "反应机理": ["反应机理", "电子效应"],
        }

        for keyword, points in keywords.items():
            if keyword in content:
                knowledge_points.extend(points)

        # 去重
        knowledge_points = list(set(knowledge_points))

    # 格式化为Obsidian wikilink格式
    formatted_points = [f'[[{point}]]' for point in knowledge_points[:4]]  # 最多4个知识点

    return formatted_points

def update_knowledge_points(file_path):
    """更新文件中的知识点"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取知识点
    knowledge_points = extract_knowledge_points(file_path)

    if not knowledge_points:
        return False

    # 检查是否已经有知识点
    if 'knowledge_points:' in content:
        # 替换现有的knowledge_points
        new_points_str = str(knowledge_points).replace("'", '"')
        content = re.sub(
            r'knowledge_points:\s*\[.*?\]',
            f'knowledge_points: {new_points_str}',
            content
        )
    else:
        # 添加knowledge_points字段
        content = content.replace(
            'tags:',
            f'knowledge_points: {str(knowledge_points).replace(chr(39), chr(34))}\ntags:'
        )

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    """主函数"""
    print("开始为题目文件添加知识点标签...")

    updated_count = 0

    for question_dir in QUESTION_DIRS:
        if not question_dir.exists():
            continue

        print(f"\n处理目录: {question_dir}")

        for file_path in question_dir.glob("题-*.md"):
            if update_knowledge_points(file_path):
                updated_count += 1
                print(f"  已更新: {file_path.name}")

    print(f"\n完成! 共更新了 {updated_count} 个文件")

if __name__ == "__main__":
    main()
