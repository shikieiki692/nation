---
title: 题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性
type: 题目
fidelity: 原书逐字
submodule: 区域选择性
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["21"]
knowledge_points: ["[[区域选择性]]"]
tags: [化竞, Clayden, 有机化学, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch24-P2]
source: Clayden Organic Chemistry 2nd Ed. Chapter 24 Problem 2
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-608-Clayden-Ch36-P1-原子编号追踪重排]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-609-Clayden-Ch36-P2-Beckmann重排立体化学和机理]]"]
module: 有机化学
status: 已填充
---
# 题-433: 不饱和羰基直接/共轭加成区域选择性

## 题目

Predict the products of these reactions.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/2e29e9cc80729d22fcf0d4a703d95875d2cbd9cbbfe61544a77915ff4ac3b4a5.jpg]]

**原文题目**：预测下列反应的产物。

## 参考答案

**Answer (English)**: Both reactions involve addition of organometallic compounds to unsaturated carbonyl compounds. The key difference is the metal. With Cu(I) as catalyst, the Grignard reagent will give conjugate addition in the first case. MeLi will give direct addition in the second.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/a22d1f831e713cd6a5f5958f96af5297d5254c2fa19a71bf0821af05f8d58285.jpg]]

**中文解析**：

两个反应都涉及有机金属化合物对不饱和羰基化合物的加成，但金属的选择决定了区域选择性：

**反应1：Cu(I)催化的Grignard加成**
- Cu(I)催化下，Grignard试剂（RMgX）形成有机铜中间体（Gilman试剂 R₂CuLi 类物种）
- 有机铜是"软"亲核试剂，优先进攻"软"亲电位点——β-碳（共轭加成/1,4-加成）
- 产物：烷基连接在β-碳上，保留C=O

**反应2：MeLi直接加成**
- MeLi是"硬"亲核试剂，优先进攻"硬"亲电位点——羰基碳（直接加成/1,2-加成）
- 产物：甲基连接在羰基碳上，C=O变为C-OH

**核心规律**：硬亲核试剂（RLi, RMgX无Cu）→1,2-加成；软亲核试剂（R₂CuLi, RMgX/Cu⁺）→1,4-加成

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[区域选择性]] | 1,2-加成 vs 1,4-加成的选择 | 直接 |
| [[共轭加成]] | Cu(I)催化下有机铜的共轭加成 | 直接 |
| [[Michael加成]] | 亲核共轭加成的另一种称呼 | 间接 |
| [[软硬酸碱理论]] | 软/硬亲核试剂对加成模式的影响 | 间接 |

## 解题思路

1. **读题定位**：两个反应底物都是α,β-不饱和羰基化合物，区别在于有机金属试剂和金属种类
2. **🔑 关键转换**：判断有机金属试剂的"软硬"性质——Cu(I)催化形成软亲核试剂（→共轭加成），MeLi为硬亲核试剂（→直接加成）
3. **验证**：检查产物中碳-碳键形成的位置：共轭加成产物中烷基在β-碳，直接加成产物中烷基在羰基碳

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为Grignard总是进行1,4-加成 | 忽略了Cu催化的必要性 | 无Cu催化的Grignard也倾向于1,2-加成；Cu(I)使其变为软亲核试剂 | 有机铜中间体的真实结构是什么？ |
| 混淆产物结构 | 没有明确区分两种加成的产物 | 1,4-加成保留C=O；1,2-加成C=O→C-OH | 如何从产物逆推反应类型？ |
| 认为MeLi也能做共轭加成 | MeLi是极强的硬亲核试剂 | MeLi几乎总是进行1,2-加成，无法通过催化改变 | 什么条件下可以强制MeLi做共轭加成？ |