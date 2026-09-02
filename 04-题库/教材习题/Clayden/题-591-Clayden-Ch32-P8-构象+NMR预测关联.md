---
title: 题-591-Clayden-Ch32-P8-构象+NMR预测关联
type: 题目
fidelity: 原书逐字
submodule: 立体选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[构象分析]]"]
tags: [化竞, Clayden, 有机化学, 立体选择性]
updated: 2026-07-25
aliases: [Clayden-Ch32-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 32 Problem 8
cross_references: ["[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]", "[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-591: 构象+NMR预测关联

## 题目

Draw conformational drawings for these compounds. State in each case why the substituents have the positions you give. To what extent could you confirm your predictions experimentally?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/5225985e7c3e5afaf3b04ea588aae6ee50615fc5bff5b1544b6b44312e82decf.jpg]]

## 参考答案

**Answer (English)**: The first two compounds have no choice about their conformation but the third does. The two functional groups prefer to be equatorial rather than axial.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/a1a1e9d4c520fe0fdc366910941cf12d388c04736bde2434d8d4f35517ce0a4b.jpg]]

Confirming the conformations experimentally means measuring coupling constants in the proton NMR so we need to look at the vital protons and consider whether they can be seen in the spectrum.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ecebdb1dbbf5430468f1f690ac9d74d9b419f9df9aa279786efcc8af88b94565.jpg]]

In the first molecule, proton H has two neighbours, one axial and one equatorial so it will appear as a double doublet with characteristic large axial/axial and small axial/equatorial couplings. By contrast the two marked equatorial Hs in the second compound have each got two axial and two equatorial neighbours and all the coupling constants will be about the same and small. They will both appear as narrow triplets of triplets but may be difficult to analyse. The important thing is that they have no large couplings. The two axial protons in the third example have each got two axial and two equatorial neighbours and will again appear as triple triplets but this time one triplet will have a large axial/axial coupling.

**中文解析**：

关键步骤：
1. **构象固定**：前两个化合物的构象没有选择余地（反式十氢化萘和特定并环结构），第三个化合物的两个官能团倾向于取平伏位
2. **NMR偶合常数验证**：确认构象的关键是测量¹H NMR中的偶合常数（J值）
3. **偶合模式分析**：
   - 第一个分子：H有两个邻居（一个a一个e），表现为dd（大J_axial/axial + 小J_axial/equatorial）
   - 第二个分子：标记的两个平伏H各有2个a和2个e邻居，所有J值相近且小，表现为窄的tt（无大偶合）
   - 第三个分子：两个轴向H各有2个a和2个e邻居，表现为tt，但其中一个三重峰有大J（轴向-轴向偶合）

> **核心概念**：构象分析和NMR是互补工具。椅式构象中轴向-轴向偶合常数大（J ≈ 10-13 Hz），而轴向-平伏或平伏-平伏偶合常数小（J ≈ 2-5 Hz）。通过分析关键质子的偶合模式，可以确认构象预测。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[构象分析]] | 平伏位vs直立位的构象偏好 | 直接 |
| [[NMR谱学]] | 偶合常数与构象的关系 | 直接 |
| [[立体化学]] | 轴向/平伏向质子的NMR特征 | 间接 |

## 解题思路

1. **读题定位**：画构象式+NMR验证——识别三个化合物的构象特征和关键质子
2. **关键转换**：判断构象是否固定→画出椅式构象→找出关键质子→分析其邻居（a/e）→预测J值和偶合模式
3. **验证**：检查第一个化合物的dd是否有大J，第二个的tt无大J，第三个的tt有大J

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为三个化合物都有构象选择 | 未仔细分析结构 | 前两个构象固定，第三个可以翻转 | 反式十氢化萘为什么构象固定？ |
| 混淆J值大小 | 不清楚J值规则 | J_a-a大（10-13Hz），J_a-e和J_e-e小（2-5Hz） | 如何从NMR谱图判断质子是轴向还是平伏？ |
| 忽略关键质子的可识别性 | 不确定能否在谱中找到 | 关键质子都在官能团旁边，容易识别 | 如果关键质子与多个质子重叠怎么办？ |