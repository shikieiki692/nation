---
title: 题-302-Clayden-Ch15-P4-醇→卤化物转化试剂选择
type: 题目
fidelity: 原书逐字
submodule: 亲核取代反应
exam_stage: 初赛
subject: 有机化学
difficulty: 3
teaching_level: 巩固
syllabus_codes: ["3.2"]
knowledge_points: ["[[亲核取代]]", "[[离去基团]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch15-P4]
source: Clayden Organic Chemistry 2nd Ed. Chapter 15 Problem 4
cross_references: ["[[题-306-Clayden-Ch15-P8-ZnCl2与NaI催化剂在取代中的作用]]", "[[题-317-Clayden-Ch17-P8-环己基溴E2困难和构象变化]]"]
module: 有机化学
status: 已填充
---
# 题-302: 醇→卤化物转化试剂选择

## 题目

Suggest reagents for the following conversions of alcohols to halides:

1. ROH → RBr (tertiary alcohol, SN1 pathway)
2. ROH → RCl (primary alcohol, SN2 pathway)
3. ROH → inversion of configuration with OAc group

**原文题目**：

为下列醇到卤化物的转化提出合适的试剂：

1. ROH → RBr（叔醇，SN1途径）
2. ROH → RCl（伯醇，SN2途径）
3. ROH → 构型翻转并引入OAc基团

## 参考答案

**Answer (English)**:

1. **ROH → RBr (SN1)**: Use concentrated HBr or HBr gas. The acid protonates the OH, making H₂O a good leaving group. The tertiary carbocation forms readily, then Br⁻ captures it.

2. **ROH → RCl (SN2)**: Use PCl₃ or PCl₅ (or SOCl₂ with pyridine). PCl₃ converts OH into a good leaving group (–OPCl₂) that is displaced by Cl⁻ via SN2. With SOCl₂, the mechanism depends on conditions: with pyridine it goes via SN2; without pyridine it can go via SNi (retention).

3. **ROH → inversion with OAc**: Convert OH to OTs (tosylate) first using TsCl/pyridine (retention at C), then displace OTs with NaOAc (SN2, inversion). Overall: two inversions = retention, OR use a single SN2 step if starting with a suitable leaving group.

**中文解析**：

| 转化 | 推荐试剂 | 机理 | 关键点 |
|------|---------|------|--------|
| 叔醇→叔溴代烷 | HBr（浓） | SN1 | 酸质子化OH → H₂O离去 → 叔碳阳离子 → Br⁻捕获 |
| 伯醇→伯氯代烷 | PCl₃ | SN2 | PCl₃将OH转化为-OPCl₂（好的离去基团） → Cl⁻背面进攻 → 构型翻转 |
| 醇→构型翻转的OAc酯 | TsCl/吡啶 → NaOAc | SN2 | 第一步TsCl/吡啶（保持构型）→ 第二步NaOAc取代（SN2翻转） |

**详细讨论**：

1. **叔醇 + HBr**：叔醇的OH被HBr质子化后，水分子作为离去基团离开，形成稳定的叔碳阳离子。溴离子随后捕获碳阳离子。由于碳阳离子是平面结构，Br⁻可以从两面进攻，产物外消旋化。HBr比HCl更常用，因为Br⁻是更好的亲核试剂。

2. **伯醇 + PCl₃**：PCl₃首先与OH反应生成氯亚磷酸酯中间体 (-OPCl₂)，这是一个好的离去基团。Cl⁻从背面进攻伯碳，发生SN2取代，得到伯氯代烷并伴随构型翻转。

3. **构型翻转的OAc**：如果需要翻转构型并引入乙酰氧基，最可靠的方法是先将OH转化为OTs（对甲苯磺酸酯，TsCl/吡啶，保持构型），然后用NaOAc进行SN2取代（构型翻转）。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[亲核取代]] | 醇到卤化物的转化策略 | 直接 |
| [[离去基团]] | OH转化为好的离去基团（H₂O, -OPCl₂, -OTs） | 直接 |
| SN2反应 | 伯碳底物的SN2途径和构型翻转 | 间接 |

## 解题思路

1. **读题定位**：三个转化分别考察不同底物类型（叔醇、伯醇、需要构型控制）的试剂选择
2. **🔑 关键转换**：OH是差的离去基团 → 必须活化（质子化/转化为磺酸酯/与卤化磷反应）→ SN1或SN2取决于底物类型
3. **验证**：叔醇用HBr（SN1）不会发生重排（叔碳阳离子已最稳定）；伯醇用PCl₃（SN2）速率快

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 叔醇用PCl₃ | 忽略了叔碳底物SN2极慢 | 叔醇应该用HBr/SN1途径 | 为什么PCl₃不适合叔醇？ |
| 伯醇用HBr | 可能发生重排（如果生成的碳阳离子能重排） | 用PCl₃/SN2更安全，不经过碳阳离子 | 伯醇+HBr一定会发生重排吗？ |
| 误以为TsCl/吡啶会翻转构型 | 没有理解TsCl的反应机理 | TsCl与OH反应时C-O键不断裂，构型保持 | TsCl/吡啶反应中哪个键断裂？ |