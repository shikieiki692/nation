---
title: 题-421-Clayden-Ch13-P8-吡啶硝化产物硝基位置NMR推断
type: 题目
fidelity: 原书逐字
submodule: NMR谱学
exam_stage: 决赛
source_subject: 有机化学
difficulty: 3
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch13-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 13 Problem 8
cross_references: ["[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-536-Clayden-Ch18-P1-C6H5FO的13C NMR C-F偶合结构确定]]", "[[题-537-Clayden-Ch18-P2-Bullatenone结构A预测NMR并纠正]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 章节练习
---
# 题-421: 吡啶硝化产物硝基位置NMR推断

## 题目

A nitration product (C₈H₁₁N₃O₂) of this pyridine has been isolated which has a nitro group somewhere in the molecule. From the spectrum deduce where the nitro group is and give a full analysis of the spectrum.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/f1cf70c45994abfe82ae85a0912f631c4e0dff4d012f992bc54330d4dbb31798.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/71410b6908a2ce5f787ca6cb188c3f3eb4fb02961a9b85bd6f9ccac7fee25bf9.jpg]]

## 参考答案

**Answer (English)**: The nitro group might go on the pyridine ring or on the aliphatic side chain or even on the nitrogen atom. Checking the integral shows that it must have gone on the pyridine: the propyl side chain is still there (CH₃ triplet, CH₂ quintet, and a CH₂ triplet with large chemical shift). The NH proton is still there at 4.0 ppm. But there are now only three protons on the pyridine ring (at 6.7, 8.3, and 8.8 ppm).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/e44a6b56f8e2ed56284b6c0a0ccdce63803cc9d807739be5ec0c64b2a03b536f.jpg]]

There are four possible structures. The most significant feature is the proton at very large chemical shift (8.8) with only very small coupling. Protons next to nitrogen in pyridine rings have very large chemical shifts so this rules out all structures except the second. The nitro group also increases the shifts of neighbouring protons:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/255816f1ddc0413fa1a36e8a4a7b90c56c59b0e9f65b05bb110870964b188666.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/549cc364bb4270aa71f18068407e543b0b2c589881e669f1061d70bf499ca4ea.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/994d46201c473c9a998d965c3261e0032c6a763cf6740d49769777ef22449953.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/be7cc82a034fd6da51562173b5deeed793f6fd94151b190f5c97190100e5d206.jpg]]

**中文解析**：

关键要点：
1. **积分排除侧链硝化**：丙基侧链仍在（CH₃三重峰、CH₂五重峰、CH₂三重峰大位移），NH在4.0 ppm，说明硝基在吡啶环上
2. **关键信号**：δ 8.8的H位移极大且只有很小偶合——吡啶环上N邻位的H有极大化学位移
3. **排除法**：四个可能结构中，只有第二个结构能让N邻位H保留且位移极大
4. **硝基效应**：硝基使邻位H的化学位移增大（去屏蔽效应）

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | 通过NMR数据推断反应产物结构 | 直接 |
| [[芳香亲电取代]] | 吡啶环的硝化反应和定位效应 | 直接 |
| [[化学位移]] | 杂原子和取代基对芳香H位移的影响 | 直接 |
| [[吡啶]] | 吡啶环的电子结构和NMR特征 | 间接 |

## 解题思路

1. **读题定位**：题目给出吡啶硝化产物的分子式和NMR数据，要求确定硝基位置——核心是分析吡啶环上H的化学位移和偶合
2. **🔑 关键转换**：积分确认侧链完整→芳香区只有3个H（硝基取代了一个）→δ 8.8的H在N邻位（大位移+小偶合）→排除法确定硝基位置
3. **验证**：检查推断结构的所有NMR信号是否与数据一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忽略吡啶N对邻位H的影响 | 不了解吡啶的NMR特征 | 吡啶N邻位H有极大化学位移（δ 8–9） | 吡啶环上哪个位置的H位移最大？ |
| 没有检查侧链是否完整 | 只关注芳香区 | 先确认侧链信号（CH₃、CH₂）是否与原料一致 | 丙基侧链的典型NMR模式是什么？ |
| 忽略硝基的去屏蔽效应 | 不了解取代基对位移的影响 | 硝基使邻位H的化学位移显著增大 | 硝基的吸电子效应对NMR有什么影响？ |