---
title: 题-499-Clayden-Ch34-P11-氧化触发分子内DA效应
type: 题目
fidelity: 原书逐字
submodule: 环加成反应
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[Diels-Alder反应]]"]
tags: [化竞, Clayden, 有机化学, 环加成反应]
updated: 2026-07-25
aliases: [Clayden-Ch34-P11]
source: Clayden Organic Chemistry 2nd Ed. Chapter 34 Problem 11
cross_references: ["[[题-501-Clayden-Ch35-P1-Nazarov关环+Grignard和cuprate步骤]]", "[[题-502-Clayden-Ch35-P2-Claisen-3,3-σ迁移入门]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-499: 氧化触发分子内DA效应

## 题目

This unsaturated alcohol is perfectly stable until it is oxidized with Cr(VI): it then cyclizes to the product shown. Explain.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/a9b29e621adab696530a475e2a7b8def6134891d6fba8907eac2c1124ea47a96.jpg]]

**原文题目**：This unsaturated alcohol is perfectly stable until it is oxidized with Cr(VI): it then cyclizes to the product shown. Explain.

## 参考答案

**Answer (English)**: The starting material might undergo a Diels-Alder reaction but the diene and the dienophile are poorly matched. Both have high energy HOMOs and there isn't a low energy LUMO in sight. Once the enone is formed, the alkene becomes electron-deficient: now the energies match well and cycloaddition is fast. The stereochemistry comes from an endo arrangement.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/8136793eabcb75086d29a9e366917034c456cb028c975480ef471e0cf716f366.jpg]]

**中文解析**：

关键分析：
1. **起始物的稳定性**：
   - 起始物是不饱和醇，理论上可能发生DA反应
   - 但二烯体和亲二烯体"不匹配"——两者都有高能HOMO，没有低能LUMO
   - 因此DA反应在热力学上不利，起始物稳定

2. **氧化的触发作用**：
   - Cr(VI)氧化烯丙基醇为烯酮（enone）
   - 烯酮中的烯烃变得缺电子（C=O的吸电子效应）
   - 现在能量匹配：二烯体HOMO + 烯酮LUMO → DA反应快速发生

3. **立体化学**：
   - endo过渡态：烯酮的羰基藏在二烯体下方
   - 次级轨道重叠稳定endo过渡态

4. **总结**：
   - 氧化改变了亲二烯体的电子性质
   - 从"不匹配"（两个HOMO）变为"匹配"（HOMO-LUMO）
   - 这是"氧化触发"分子内DA反应的经典例子

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| Diels-Alder反应 | 分子内DA反应的电子需求匹配 | 直接 |
| [[周环反应]] | DA反应的轨道对称性要求 | 直接 |
| [[氧化反应]] | Cr(VI)氧化烯丙基醇为烯酮 | 直接 |
| [[前线轨道理论]] | HOMO-LUMO能量匹配决定反应性 | 直接 |
| [[endo/exo]] | endo过渡态的稳定性 | 间接 |

## 解题思路

1. **读题定位**：解释为什么氧化后才发生环化 → 分析氧化前后的电子性质变化
2. **🔑 氧化前**：
   - 二烯体和亲二烯体都有高能HOMO
   - 没有低能LUMO → DA反应不发生
   - 起始物稳定
3. **🔑 氧化后**：
   - Cr(VI)氧化醇为烯酮 → 烯烃变缺电子
   - 烯酮提供低能LUMO → 与二烯体HOMO匹配
   - DA反应快速发生
4. **🔑 立体化学**：
   - endo过渡态 → 羰基藏在二烯体下方
   - 次级轨道重叠稳定过渡态

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为起始物不能发生DA | 没有分析电子需求 | 起始物可以发生DA，只是能量不匹配 | 为什么两个HOMO不能有效反应？ |
| 忽略氧化改变电子性质 | 只关注氧化官能团转化 | 氧化将醇变为烯酮，改变了亲二烯体的LUMO能量 | 烯酮的LUMO比烯烃低多少？ |
| 没有解释"触发"机制 | 只说"氧化后反应" | 需要解释氧化如何使HOMO-LUMO能量匹配 | 为什么氧化前不反应，氧化后就反应了？ |
| 立体化学解释不完整 | 只说"endo" | 需要说明次级轨道重叠如何稳定endo过渡态 | endo和exo的能量差大约是多少？ |