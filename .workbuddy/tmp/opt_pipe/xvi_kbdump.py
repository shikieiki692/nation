# -*- coding: utf-8 -*-
"""批量打印 03-知识点 页正文（跳过 FM），供解析撰写取材。
用法: python xvi_kbdump.py <batch_name>
"""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")

B = {
 "b1": ["无机和结构化学/MOF材料.md", "化学原理/配合物.md", "无机和结构化学/配位数.md",
        "决赛要求/物理化学深化/Langmuir吸附等温式.md", "决赛要求/金属有机与超分子/超分子作用力.md"],
 "b2": ["无机和结构化学/晶胞.md", "无机和结构化学/晶体密度公式.md",
        "无机和结构化学/晶体结构.md", "无机和结构化学/晶胞投影图分析.md"],
 "b3": ["无机和结构化学/能带理论.md", "高中化学基础/分子极性与分子间作用力.md",
        "无机和结构化学/点阵类型.md", "无机和结构化学/晶体对称性.md"],
 "b4": ["化学原理/化学平衡.md", "化学原理/van't Hoff方程.md",
        "决赛要求/物理化学深化/相变热力学.md", "决赛要求/物理化学深化/克拉佩隆方程.md",
        "化学原理/溶度积.md"],
 "b5": ["无机和结构化学/磁矩.md", "无机和结构化学/18电子规则.md",
        "无机和结构化学/过渡金属羰基化合物.md", "分析化学/条件稳定常数.md",
        "分析化学/分布分数.md"],
 "b6": ["化学原理/Nernst方程.md", "分析化学/分光光度法.md",
        "决赛要求/金属有机与超分子/金属有机化学基础.md", "无机和结构化学/配位化学.md"],
}
key = sys.argv[1]
for rel in B[key]:
    p = os.path.join("03-知识点", rel)
    t = io.open(p, encoding="utf-8-sig").read()
    if t.startswith("---"):
        i = t.find("\n---", 3)
        t = t[i + 4:] if i > 0 else t
    print("\n" + "=" * 78)
    print("### KB PAGE: " + p)
    print("=" * 78)
    print(t.strip())
