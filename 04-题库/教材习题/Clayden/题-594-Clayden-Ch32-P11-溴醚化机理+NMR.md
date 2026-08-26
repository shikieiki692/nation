---
title: 题-594-Clayden-Ch32-P11-溴醚化机理+NMR
type: 题目
fidelity: 原书逐字
submodule: 立体选择性
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[立体化学]]"]
tags: [化竞, Clayden, 有机化学, 立体选择性]
updated: 2026-07-25
aliases: [Clayden-Ch32-P11]
source: Clayden Organic Chemistry 2nd Ed. Chapter 32 Problem 11
cross_references: ["[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]", "[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-594: 溴醚化机理+NMR

## 题目

Suggest a mechanism for the following reaction. The product has the following signals in its ¹H NMR spectrum: δ_H 3.9 (1H, ddq, J 12, 4, 7) and 4.3 (1H, dd, J 11, 3). What is the stereochemistry and conformation of the product?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ea7c1ed85dbaad19f9a44ff83b5fc5f86ed33726cff82be2852f4514a539f0d1.jpg]]

## 参考答案

**Answer (English)**: This 'bromoetherification' is a variant of the more familiar mechanism of bromolactonization. The mechanism is formation of a bromonium ion by attack on the electron-rich alkene, followed by intramolecular nucleophilic attack by the OH group at the more substituted carbon atom. The NMR spectrum shows that the protons next to Br and O are both axial, since they have a large coupling constant of around 12 Hz. The Br atom and the Me group must therefore be equatorial.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/b60ea3c20eab9424caad9d4c70890e024cca03bf5688f6f448fa4793bee16adc.jpg]]

**中文解析**：

关键步骤：
1. **溴鎓离子形成**：Br₂进攻富电子烯烃，形成溴鎓离子中间体
2. **分子内亲核进攻**：OH基团从溴鎓离子的背面进攻取代较多的碳原子（更稳定的碳正离子特征），关环形成四氢呋喃环
3. **NMR解析构象**：与Br和O相邻的两个质子（H_a和H_b）都有大偶合常数（~12 Hz），说明它们都是轴向质子。因此Br和Me基团必须是平伏位

> **核心概念**：溴醚化是溴内酯化的变体。NMR偶合常数是确定环状产物构象的有力工具——大J值（>10 Hz）表示轴向-轴向偶合，确认了Br和Me都在平伏位。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[立体化学]] | 溴鎓离子开环的立体化学 | 直接 |
| [[NMR谱学]] | 偶合常数确定构象 | 直接 |
| [[机理书写]] | 溴醚化的完整机理 | 直接 |

## 解题思路

1. **读题定位**：溴醚化机理+NMR推断构象——识别底物为含OH的环己烯
2. **关键转换**：Br₂形成溴鎓离子→OH从背面进攻多取代碳→关环→NMR显示两个大J（12 Hz）→两个相邻质子都是轴向→Br和Me为平伏位
3. **验证**：检查ddq（J=12,4,7）和dd（J=11,3）是否符合轴向质子的偶合模式

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| OH进攻取代较少的碳 | 未考虑电子效应 | 在溴鎓离子中，OH倾向于进攻取代较多的碳（部分碳正离子特征） | 什么情况下亲核试剂进攻取代较少的碳？ |
| 忽略NMR数据 | 只画机理不验证 | J=12 Hz说明是轴向-轴向偶合，必须据此推断构象 | ddq的三个J值分别对应什么偶合？ |
| 画出Br和Me都直立 | 未考虑构象稳定性 | NMR证明Br和Me是平伏位（相邻质子是轴向） | 如果Br和Me都直立，NMR会显示什么？ |