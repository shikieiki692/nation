---
title: 题-565-Clayden-Ch30-P6-饱和芳香杂环立体化学合成
type: 题目
fidelity: 原书逐字
submodule: 杂环合成
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
question_type: [机理]
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[杂环化合物]]"]
tags: [化竞, Clayden, 有机化学, 杂环合成]
updated: 2026-07-25
aliases: [Clayden-Ch30-P6]
source: Clayden Organic Chemistry 2nd Ed. Chapter 30 Problem 6
cross_references: ["[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]", "[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
used_in: ["[[有机化学阶段测试卷]]", "[[04-题库/有机化学阶段测试卷]]"]
---
# 题-565: 饱和+芳香杂环+立体化学合成

## 题目

**【中文】**请给出图中所示这些用于制备稠合吡啶（fused pyridine）的反应的机理。为什么必须使用保护基？

**【原文】**Give mechanisms for these reactions used to prepare a fused pyridine. Why is it necessary to use a protecting group?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/b9b1c594716f93443884f32cb86f6e1abd500d2f065b519349a1d6f8427ecada.jpg]]

## 参考答案

**Answer (English)**: The first starting material is a stable cyclic enamine and conjugate addition is what we should expect with an enone. If the aldehyde were unprotected, direct addition might occur there as well as carbonyl condensations. The product is in equilibrium with both its enols, one of which can cyclize to form the new six-membered ring.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ed2ef32f8c2a84dbdce8316fd935395245a9ed492cfc72b9735e8cdeec3acf85.jpg]]

The enol must attack the five-membered ring in a cis fashion as the tether is too short to reach the other side. There is no control over one stereogenic centre (represented with a wiggly line) but that is unimportant as it is soon to disappear.

Now the reaction with hydroxylamine in acid solution. Formation of the oxime of the ketone produces one molecule of water—just enough to hydrolyse the acetal—and the pyridine synthesis is completed by cyclization and a double dehydration.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/0acb37098fd11e72b62324b308d9f2a3fd96b874cc62e75b2b768f7867cf8afb.jpg]]

**中文解析**：

**步骤一：Michael加成+分子内Aldol**
1. 环烯胺作为亲核试剂，对烯酮做共轭加成（Michael加成）
2. 产物与两种烯醇互变平衡，其中一种可环化形成新的六元环
3. 环化必须是顺式（cis）——因为连接链太短，无法从反面进攻

**保护基的作用**：醛基如果不保护（缩醛保护），会发生直接加成（1,2-加成到醛）和各种羰基缩合副反应。缩醛保护确保只有共轭加成发生。

**步骤二：羟胺+酸→吡啶合成**
1. 羟胺与酮形成肟（oxime）——产生一分子水
2. 水恰好水解缩醛保护基，释放醛基
3. 醛与肟氮环化，双脱水完成吡啶环的构建

> **精妙设计**：肟形成产生的水恰好用于脱保护——一石二鸟！顺式环化由tether长度控制。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[杂环化合物]] | 饱和杂环（环烯胺）→芳香杂环（吡啶）的转化 | 直接 |
| [[保护基]] | 缩醛保护醛基防止副反应，羟胺反应时自动脱保护 | 直接 |
| [[共轭加成]] | 环烯胺对烯酮的Michael加成 | 直接 |
| [[立体化学]] | 顺式环化的立体控制（tether长度限制） | 间接 |

## 解题思路

1. **读题定位**：环烯胺+烯酮→稠合吡啶——需要Michael加成、环化、吡啶合成三步
2. **🔑 关键转换**：Michael加成→Aldol环化→缩醛保护→羟胺反应（产生水+脱保护+环化+双脱水→吡啶）
3. **验证**：检查立体化学（顺式环化）；检查保护基的脱除时机（羟胺反应产生的水）

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 没有保护醛基 | 不理解保护的必要性 | 醛基不保护会发生1,2-加成和多种缩合副反应 | 缩醛保护基的条件是什么？ |
| 画反式环化 | 没考虑tether长度限制 | 连接链太短只能顺式环化，反面无法到达 | 为什么tether长度决定立体化学？ |
| 忘记双脱水步骤 | 吡啶形成需要脱两次水 | 肟+醛环化后需双脱水才能得到芳香吡啶 | 吡啶合成需要几次脱水？ |