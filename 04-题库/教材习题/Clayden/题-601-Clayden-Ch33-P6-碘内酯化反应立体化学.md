---
title: 题-601-Clayden-Ch33-P6-碘内酯化反应立体化学
type: 题目
fidelity: 原书逐字
submodule: 非对映选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[立体化学]]"]
tags: [化竞, Clayden, 有机化学, 非对映选择性]
updated: 2026-07-25
aliases: [Clayden-Ch33-P6]
source: Clayden Organic Chemistry 2nd Ed. Chapter 33 Problem 6
cross_references: ["[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
source_category: 教材课后习题
source_grade: B
---
# 题-601: 碘内酯化反应立体化学

## 题目

Explain how the stereochemistry of this epoxide is controlled.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/3d625c680cf5dde9466b934f88f5ee5f57811fe0ebd415fa7d523a672d0e2c91.jpg]]

## 参考答案

**Answer (English)**: The bicarbonate (NaHCO₃) is a strong enough base to remove the proton from the carboxylic acid. Iodine attacks the alkene reversibly to give a mixture of diastereoisomers of the iodonium ion. If the I⁺ and Me groups are on the same side of the chain, the carboxylate group can attack the iodonium ion from the back and set up a trans iodolactone. The iodolactone is cleaved by methoxide and the oxyanion displaces iodide to give the epoxide.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/8dc392c622ebb4685eaf37ac04f3702a41d896160e78dc9e8919d4055ec1a9e4.jpg]]

**中文解析**：

关键步骤：
1. **碘鎓离子形成**：I₂进攻烯烃（可逆），形成碘鎓离子。由于可逆性，最终只有一种非对映异构体的碘鎓离子导致产物
2. **碘内酯化**：当I⁺和Me在链的同侧时，羧酸根可以从背面进攻碘鎓离子，形成trans碘内酯。这是分子内S_N2反式开环的结果
3. **环氧化物形成**：碘内酯被甲氧基裂解，生成的氧负离子从背面取代碘化物（分子内S_N2），形成环氧化物

> **核心概念**：碘内酯化是碘化学中的经典反应。通过形成碘鎓离子中间体，然后由分子内亲核试剂（羧酸根）进行反式开环，可以高立体选择性地构建含碘的环状中间体，最终转化为环氧化物。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[立体化学]] | 碘鎓离子形成的立体化学 | 直接 |
| [[非对映选择性]] | trans碘内酯化的选择性 | 直接 |
| [[碘化学]] | 碘内酯化+甲氧基裂解的序列 | 直接 |

## 解题思路

1. **读题定位**：解释环氧化物的立体化学控制——识别反应为碘内酯化+甲氧基裂解
2. **关键转换**：I₂→碘鎓离子→羧酸根反式开环→trans碘内酯→甲氧基裂解→氧负离子S_N2关环→环氧化物
3. **验证**：检查碘内酯是否为trans，环氧化物的立体化学是否与碘内酯一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 画出cis碘内酯 | 未理解反式开环要求 | 羧酸根必须从碘鎓离子背面进攻，得到trans产物 | 碘鎓离子开环为什么必须反式？ |
| 忽略I₂加成的可逆性 | 以为两种碘鎓离子都反应 | 只有合适的碘鎓离子异构体能被羧酸根有效开环 | 为什么碘鎓离子形成是可逆的？ |
| 环氧化物立体化学画反 | 未考虑S_N2构型翻转 | 氧负离子从I的背面取代，环氧化物立体化学由碘内酯决定 | 甲氧基裂解的机理是什么？ |