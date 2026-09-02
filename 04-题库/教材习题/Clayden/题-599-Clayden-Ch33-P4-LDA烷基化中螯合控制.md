---
title: "题-599-Clayden-Ch33-P4-LDA烷基化中螯合控制"
type: 题目
fidelity: 原书逐字
submodule: 非对映选择性
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
question_type: [简答]
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[非对映选择性]]"]
tags: [化竞, Clayden, 有机化学, 非对映选择性]
updated: 2026-07-25
aliases: [Clayden-Ch33-P4]
source: Clayden Organic Chemistry 2nd Ed. Chapter 33 Problem 4
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-433-Clayden-Ch24-P2-不饱和羰基直接共轭加成区域选择性]]", "[[题-432-Clayden-Ch24-P1-氨基醇制备中区域选择性试剂选择]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
used_in: "[[有机化学阶段测试卷]]"
---
# 题-599: LDA/烷基化中螯合控制

## 题目

**【中文】**当该羟基酯（见图）用两倍过量的 LDA 处理、然后再进行烷基化时，产物中某一个非对映异构体占优势。为什么？

**【原文】**When this hydroxy-ester is treated with a two-fold excess of LDA and then alkylated, one diastereoisomer of the product predominates. Why?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/fd24fc9fc5cf324ca94deaf1c188e3cff0dd97666fcb625e83a64cc71052a7e5.jpg]]

## 参考答案

**Answer (English)**: The first LDA molecule removes the OH proton and only the second gives the lithium enolate. The enolate is held in a ring by chelation to the first lithium atom so that the allyl group adds to the less hindered face—opposite the methyl group.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/c407392d0d9f4a9bdb997b36afe5c6763f618ee8b37c4b299af40f11df37f9d7.jpg]]

**中文解析**：

关键步骤：
1. **两当量LDA的作用**：第一当量LDA夺取OH质子（生成醇锂），第二当量LDA形成锂烯醇盐
2. **螯合控制**：锂烯醇盐通过第一个锂原子与醇锂氧的螯合作用，被固定在环状结构中。这使得烯醇盐的α-碳只有一面暴露给亲电试剂
3. **位阻控制**：烯丙基溴从位阻较小的一面（与甲基相反的一面）进攻，得到主要的非对映异构体

> **核心概念**：当底物同时含有OH和烯醇化位点时，使用过量强碱（如2 equiv LDA）可以形成螯合的锂烯醇盐。这种螯合作用将开链分子固定在特定构象中，实现高非对映选择性的烷基化。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[非对映选择性]] | 螯合锂烯醇盐的烷基化选择性 | 直接 |
| [[螯合控制]] | 双锂螯合固定构象 | 直接 |
| [[立体化学]] | 从位阻较小面进攻的立体化学结果 | 间接 |

## 解题思路

1. **读题定位**：解释LDA处理后烷基化的非对映选择性——识别底物为含OH的酯
2. **关键转换**：2 equiv LDA→第一当量去OH质子→第二当量形成锂烯醇盐→Li螯合固定构象→烯丙基从甲基对面进攻
3. **验证**：检查螯合环是否为六元环，烷基化面是否在甲基的对面

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 认为1当量LDA就够了 | 未考虑OH也会消耗LDA | 第一当量去OH质子，第二当量才形成烯醇盐 | 为什么需要2当量LDA？ |
| 画出非螯合的过渡态 | 忽略Li⁺的螯合作用 | Li⁺同时与醇氧和烯醇氧配位，形成螯合环 | 螯合环是几元环？ |
| 烷基化面画反 | 未考虑甲基的位阻 | 烯丙基从甲基的对面（位阻较小面）进攻 | 甲基和烯丙基哪个更大？ |