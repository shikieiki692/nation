---
title: 题-431-Clayden-Ch23-P8-二胺选择性保护策略
type: 题目
fidelity: 原书逐字
submodule: 化学选择性与保护基
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[保护基]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch23-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 23 Problem 8
cross_references: ["[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]", "[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-431: 二胺选择性保护策略

## 题目

How would you convert this diamine to either of these two protected derivatives?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/d142aaf6101a58e2d5f90433ac528767aca3e62cae0072711989d8bc42b08a17.jpg]]

## 参考答案

**Answer (English)**: The Boc group is a common acid-sensitive protecting group for amines. Making the first derivative is easy because the amine attached to the primary carbon is less hindered and more reactive. Treating the diamine with one equivalent of 'Boc anhydride' (Boc₂O) gives the correctly protected product:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/cd87f9c68724c12c575b15665277ded14e62c9f16cc0ab01a0c28620ccc18fdc.jpg]]

The second is more of a challenge — we need to protect the less reactive amino group. The solution is first to protect with a different protecting group: Cbz will do, using CbzCl (benzyl chloroformate) and base. Now the other amino group can be protected with Boc, and finally the Cbz protecting group removed by hydrogenation. Other protecting groups might be all right too, but they have to be removable without using acid, which would remove the Boc group.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/5c4e76bbabe381d9601aa8767f91a7b625d658f4f6cea9e224726126fa45899c.jpg]]

This chemistry was used by chemists in Bordeaux and Manchester to build some new polymeric structures out of the two different amine products:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/289a0d1806a62a5e71b5710d8ff2a2e9a49f03a963376fbd77758238e5767f3d.jpg]]

**中文解析**：

关键要点：
1. **产物1（保护伯胺）**：伯胺位阻小、亲核性强→1当量Boc₂O选择性保护伯胺→简单一步完成
2. **产物2（保护仲胺）**：仲胺活性低，直接Boc保护会先保护伯胺→策略：先用CbzCl保护伯胺（形成Cbz保护的胺）→再用Boc保护仲胺→最后H₂/Pd脱Cbz（不脱Boc）
3. **保护基正交性**：Boc用酸脱除，Cbz用氢解脱除——两种保护基可以在不同条件下选择性脱除

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[保护基]] | Boc和Cbz保护基的选择性和正交性 | 直接 |
| [[化学选择性]] | 伯胺vs仲胺的选择性保护 | 直接 |
| [[胺的化学]] | 胺的亲核性和位阻对反应性的影响 | 直接 |
| 正交保护 | 两种保护基可在不同条件下选择性脱除 | 间接 |

## 解题思路

1. **读题定位**：题目要求将二胺选择性转化为两种不同的单保护产物——核心是利用伯胺和仲胺的反应性差异
2. **🔑 关键转换**：产物1：伯胺活性高→Boc₂O直接选择性保护；产物2：仲胺活性低→先用Cbz保护伯胺→再Boc保护仲胺→脱Cbz
3. **验证**：检查保护基的正交性，确认脱保护条件不会影响另一个保护基

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 不理解为什么产物2需要两步 | 没有识别伯胺vs仲胺的反应性差异 | 仲胺活性低，直接保护会先保护伯胺 | 伯胺和仲胺的亲核性差异有多大？ |
| 忽略保护基正交性 | 选用了不兼容的保护基组合 | Boc（酸脱）和Cbz（氢解脱）是正交的 | 什么是保护基的正交性？ |
| 脱Cbz时误脱Boc | 不了解不同保护基的脱除条件 | Cbz用H₂/Pd脱除，不影响Boc；Boc用酸脱除 | 为什么H₂/Pd不能脱除Boc？ |