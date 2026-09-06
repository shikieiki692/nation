---
title: 题-397-Clayden-Ch22-P7-氯吡啶亲核取代选择性
type: 题目
fidelity: 原书逐字
submodule: 共轭加成
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[芳香亲核取代]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch22-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 22 Problem 7
cross_references: ["[[题-629-Clayden-Ch38-P2-另一种卡宾方法→天然抗生素]]", "[[题-320-Clayden-Ch19-P1-HCl对三个烯烃加成方向]]", "[[题-628-Clayden-Ch38-P1-碱引发两个简单卡宾反应]]", "[[题-321-Clayden-Ch19-P2-两个烯烃溴化机理和产物]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
---
# 题-397: 氯吡啶亲核取代选择性（2/4 vs 3）

## 题目

Pyridine is a six-electron aromatic system like benzene. You have not yet been taught anything systematic about pyridine (that will come in chapter 29) but see if you can work out why 2- and 4-chloropyridines react with nucleophiles but 3-chloropyridine does not.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/731b2a5fd7ab0571fb389006cadc0ae1d833b68057545df1f58e6ff1b2b7886b.jpg]]

**原文题目**：Explain why 2- and 4-chloropyridines undergo nucleophilic aromatic substitution but 3-chloropyridine does not. Use the concept of negative charge stabilization in the intermediate.

## 参考答案

**Answer (English)**: The problem is to find somewhere to park the negative charge in the intermediate and the only possible place is on the pyridine nitrogen atom. This is easy with 2- and 4-chloropyridine but impossible with 3-chloropyridine. Using a general nucleophile:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/7fe4cfc66983fc6dad322f8d06f05fab08f02cb7efc5db56c62d20220b87f640.jpg]]

Amine formation by this reaction is particularly important as you will see in chapters 29 and 30. The mechanism is the same with a few proton transfers.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/f751bc370417a27a08517282a0b5253fb5f0ef5eaa3bd2c3157b110a5a10807e.jpg]]

**中文解析**：

关键步骤：
1. **SNAr的关键**：SNAr反应的决速步是亲核进攻形成Meisenheimer复合物。这个中间体的稳定性决定了反应能否发生
2. **2-和4-氯吡啶**：当亲核试剂进攻2-位或4-位时，中间体的负电荷可以离域到吡啶氮原子上（氮比碳更电负性，能更好地稳定负电荷）
3. **3-氯吡啶**：亲核试剂进攻3-位时，中间体的负电荷只能离域到碳原子上，无法到达氮原子，因此中间体不稳定，反应无法进行

> **核心概念**：SNAr反应需要吸电子基团来稳定Meisenheimer复合物中的负电荷。在吡啶中，氮原子就是这个"吸电子基团"，但它只能稳定邻位（2-位）和对位（4-位）的负电荷。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[芳香亲核取代]] | SNAr反应中负电荷稳定化的关键作用 | 直接 |
| [[杂环化合物]] | 吡啶氮原子作为电子撤离基团 | 直接 |
| [[吡啶]] | 吡啶环上不同位置的反应性差异 | 间接 |

## 解题思路

1. **读题定位**：题目问为什么2/4-氯吡啶能SNAr而3-氯吡啶不能——核心是Meisenheimer复合物的稳定性
2. **🔑 关键转换**：SNAr需要稳定负电荷→吡啶N可以稳定邻/对位负电荷→2/4-位进攻时负电荷可到N上→3-位不行
3. **验证**：画出三种位置进攻的中间体，检查负电荷是否能离域到N上

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为吡啶N是碱性基团，会与亲核试剂竞争 | 对吡啶的电子效应理解不深 | N的吸电子效应使邻/对位缺电子，有利于SNAr | 吡啶N的碱性和吸电子效应有什么区别？ |
| 忽略Meisenheimer复合物的稳定性 | 对SNAr机理理解不深 | SNAr能否发生取决于中间体的稳定性 | 为什么3-位的中间体不稳定？ |
| 混淆吡啶和苯的反应性 | 没有考虑杂原子的影响 | 吡啶N是吸电子基团，使环上不同位置的反应性不同 | 吡啶和苯在SNAr反应性上有什么区别？ |