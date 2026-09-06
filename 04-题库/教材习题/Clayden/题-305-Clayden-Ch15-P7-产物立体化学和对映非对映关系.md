---
title: "题-305-Clayden-Ch15-P7-产物立体化学和对映非对映关系"
type: 题目
fidelity: 原书逐字
submodule: 亲核取代反应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["3.2"]
knowledge_points: ["[[立体化学]]", "[[亲核取代]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch15-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 15 Problem 7
cross_references: ["[[题-307-Clayden-Ch15-P9-两个反应的立体化学]]", "[[题-294-Clayden-Ch14-P4-四个化合物立体化学讨论]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
source_grade: B
---
# 题-305: 产物立体化学和对映/非对映关系

## 题目

1. An achiral epoxide (meso compound) reacts with an amine nucleophile. What is the stereochemical relationship between the products?
2. An achiral substrate with an OTs leaving group reacts with a thiol nucleophile. What is the stereochemistry of the product?

**原文题目**：

1. 一个非手性的环氧化物（内消旋化合物）与胺类亲核试剂反应。产物之间有什么立体化学关系？
2. 一个非手性的带有OTs离去基团的底物与硫醇亲核试剂反应。产物的立体化学是什么？

## 参考答案

**Answer (English)**:

1. The achiral epoxide (meso, with a plane of symmetry) is opened by the amine via SN2 (backside attack on one carbon). This gives a product with two stereocenters. Since the starting material is meso and the attack is stereospecific (inversion at the attacked carbon), the product is a **single diastereoisomer** (not a single enantiomer, because the product is still achiral — it has an internal plane of symmetry).

2. The thiolate (RS⁻) displaces OTs via SN2 with inversion at the stereocenter. The starting material is achiral, so the product is also achiral (achiral → achiral via SN2 gives a single achiral product). The product has **cis** geometry (both groups on the same side).

**中文解析**：

**问题1：环氧化物开环**

起始原料是一个内消旋的环氧化物（有对称面，虽然有手性中心但整体非手性）。

- 胺亲核试剂通过SN2机理进攻环氧化物的一个碳原子
- SN2进攻导致该碳原子的构型翻转
- 产物有两个手性中心
- 但由于起始原料是内消旋的（有对称面），产物仍然有一个对称面
- 因此产物是一个**非对映异构体**（单一非对映体），而不是对映异构体
- 产物仍然是非手性的（内消旋）

**关键点**：内消旋起始原料 + SN2（构型翻转）→ 单一非对映体产物（仍然非手性）

**问题2：OTs的SN2取代**

- 起始原料是非手性的
- RS⁻（硫醇负离子）通过SN2进攻，背面进攻OTs所在的碳
- 构型翻转发生
- 但由于起始原料是非手性的，翻转后的产物也是非手性的
- 产物中两个取代基处于顺式位置（同一侧）

**立体化学总结**：

| 情况 | 起始原料 | 反应类型 | 产物立体化学 |
|------|---------|---------|-------------|
| 内消旋环氧化物开环 | 内消旋（非手性） | SN2（翻转） | 单一非对映体（仍非手性） |
| 非手性底物SN2 | 非手性 | SN2（翻转） | 非手性产物 |

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[立体化学]] | SN2翻转对产物立体化学的影响 | 直接 |
| [[亲核取代]] | 环氧化物开环和OTs取代的立体化学 | 直接 |
| [[对映异构]] | 对映体和非对映体的区分 | 间接 |

## 解题思路

1. **读题定位**：两个问题都考察SN2反应的立体化学结果，关键是对称性分析
2. **🔑 关键转换**：内消旋起始原料 → SN2翻转 → 产物是否仍具有对称面？有→内消旋（非对映体）；无→手性对映体
3. **验证**：画出所有可能的立体异构体，检查对称性

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为内消旋环氧化物开环得到对映体 | 没有检查产物的对称性 | 产物仍有对称面，是内消旋体（非对映异构体） | 如何判断一个分子是否有对称面？ |
| 混淆对映体和非对映体 | 没有理解立体异构体的关系 | 对映体：镜像关系；非对映体：不是镜像的立体异构体 | 两个内消旋化合物之间是什么关系？ |
| 认为SN2翻转总是产生手性产物 | 忽略了起始原料的对称性 | 如果起始原料是内消旋的，翻转后产物可能仍非手性 | 什么条件下SN2产物一定是手性的？ |