---
title: 题-292-Clayden-Ch14-P2-旋光值区分
type: 题目
submodule: 立体化学
exam_stage: 初赛
subject: 有机化学
difficulty: 2
teaching_level: 入门
syllabus_codes: ["36"]
knowledge_points: ["[[旋光性]]", "[[对映异构]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch14-P2]
source: Clayden Organic Chemistry 2nd Ed. Chapter 14 Problem 2
cross_references: ["[[题-293-Clayden-Ch14-P3-灰姑娘水晶鞋旋光性]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
---
# 题-292: 旋光值区分

## 题目

If a solution of a compound has an optical rotation of +12, how could you tell if this was actually +12 or really -348 or +372?

**原文题目**：如果一个化合物溶液的旋光度为+12，你如何判断这到底是+12，还是实际是-348或+372？

## 参考答案

**Answer (English)**: Check the equation that states rotation depends on three things: the rotating power of the molecule, the length of the cell, and the concentration. Halve the concentration and the rotation will change to +6, -174, or +186. Any change of concentration will distinguish them.

**中文解析**：

旋光度 α 取决于三个因素：
1. **分子本身的旋光能力**（比旋光度 [α]）
2. **样品管长度**（l）
3. **溶液浓度**（c）

公式：α = [α] × l × c

**区分方法**：改变浓度（最简单的方法）
- 浓度减半→旋光度变为：+6、-174、或+186
- 这三个值各不相同→可以区分

关键概念：旋光度是外消旋测量值，可能差360°的整数倍。+12和-348差360°，+12和+372也差360°。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[旋光性]] | 旋光度的测量和影响因素 | 直接 |
| [[对映异构]] | 旋光度与对映体的关系 | 直接 |

## 解题思路

1. **读题定位**：+12可能是真值，也可能是差360°的其他值→需要实验区分
2. **🔑 关键转换**：改变浓度→旋光度线性变化→三个候选值变成三个不同的值→可以区分
3. **验证**：+12/2=+6, -348/2=-174, +372/2=+186——三个值互不相同

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为旋光度可以区分对映体 | 混淆了旋光度和比旋光度 | 旋光度受浓度和管长影响，比旋光度才是物质的固有性质 | 比旋光度的单位是什么？ |
| 不理解差360°的问题 | 没有意识到旋光测量的周期性 | 旋光计只能测量-180°到+180°范围，超出时会差360°的整数倍 | 为什么旋光测量有周期性？ |