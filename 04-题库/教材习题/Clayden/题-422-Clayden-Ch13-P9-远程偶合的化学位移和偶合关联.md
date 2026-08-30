---
title: 题-422-Clayden-Ch13-P9-远程偶合的化学位移和偶合关联
type: 题目
fidelity: 原书逐字
submodule: NMR谱学
exam_stage: 决赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch13-P9]
source: Clayden Organic Chemistry 2nd Ed. Chapter 13 Problem 9
cross_references: ["[[题-537-Clayden-Ch18-P2-Bullatenone结构A预测NMR并纠正]]", "[[题-536-Clayden-Ch18-P1-C6H5FO的13C NMR C-F偶合结构确定]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]", "[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-422: 远程偶合的化学位移和偶合关联

## 题目

**【中文】**进一步关联化学位移与偶合，并解析更长程的偶合。（详细谱图数据见 OCR 原始资料。）

**【原文】**Further correlation of chemical shift and coupling with interpretation of longer-range coupling. (Detailed spectrum data provided in the OCR source.)

## 参考答案

**Answer (English)**: The ethyl group is easy to find — a typical 3H triplet at 1.2 ppm and a 2H quartet at 4.3 ppm. The large shift of the CH₂ group tells us it is next to O. The methyl group is also easy — a 3H singlet at 2.3 ppm, typical of a methyl group on an alkene. At the other end of the spectrum, the broad singlet at 12.5 ppm can only be the OH or the NH; the other is at 5.4 ppm. That leaves the three signals in the aromatic region: δ_H (ppm) 7.2 (1H, dd, J 9, 2 Hz), 7.5 (1H, d, J 9 Hz), and 8.4 (1H, d, J 2 Hz). The larger coupling is typical ortho and the small coupling typically meta:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/231586cb92bd0926f59d492aea623d6f868dd0b0280ce9d9b132a0717d525b2f.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/2570b8066435cac2d13b9938342547dc552e589a932585fefb5c40c268d1245f.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/eba16415f54ce2d4487bf1c0a32a92db36f253911208d4c3797fe2974dfb3ae8.jpg]]

**中文解析**：

关键要点：
1. **乙基的典型模式**：3H三重峰（δ 1.2）+ 2H四重峰（δ 4.3），CH₂大位移说明连接O
2. **烯甲基**：3H单峰在δ 2.3，是烯上甲基的典型位移
3. **活泼H**：δ 12.5宽单峰为OH或NH，另一个在δ 5.4
4. **芳香区三个信号的归属**：
   - δ 7.2 (1H, dd, J=9, 2 Hz)：同时有邻位和间位偶合
   - δ 7.5 (1H, d, J=9 Hz)：只有邻位偶合
   - δ 8.4 (1H, d, J=2 Hz)：只有间位偶合
5. **远程偶合**：小偶合常数（J=2 Hz）指示间位关系，大偶合（J=9 Hz）指示邻位关系

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | 综合化学位移和偶合进行完整归属 | 直接 |
| [[偶合常数]] | 邻位偶合（7–10 Hz）vs 间位偶合（2 Hz） | 直接 |
| [[1H NMR]] | 复杂分子的¹H NMR解析策略 | 直接 |
| [[芳香族化合物]] | 芳香环取代模式与偶合常数的关系 | 间接 |

## 解题思路

1. **读题定位**：题目要求综合化学位移和偶合进行完整归属——核心是系统分析每个信号
2. **🔑 关键转换**：从特征信号入手（乙基、甲基、活泼H）→剩余信号归属芳香区→用J值判断邻/间位关系→完成全部归属
3. **验证**：检查每个信号的化学位移、积分、多重性和偶合常数是否一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 混淆OH和NH的化学位移 | 两者都可能出现宽峰 | 两者位移范围都很大（10–15 ppm），需结合D₂O交换确认 | 如何通过D₂O交换区分OH和NH？ |
| 忽略dd峰包含两个J值 | 只看主要分裂 | dd峰有两个不同的偶合常数，反映两种不同的邻近H关系 | dd峰的两个J值分别代表什么？ |
| 不利用J值判断取代模式 | 只看化学位移不看偶合 | 邻位J=7–10 Hz，间位J≈2 Hz，对位J≈0 Hz | 三取代苯如何通过J值确定取代位置？ |