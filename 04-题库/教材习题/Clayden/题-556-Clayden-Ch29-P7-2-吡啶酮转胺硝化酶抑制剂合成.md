---
title: 题-556-Clayden-Ch29-P7-2-吡啶酮转胺硝化酶抑制剂合成
type: 题目
fidelity: 原书逐字
submodule: 杂环化合物
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[吡啶]]"]
tags: [化竞, Clayden, 有机化学, 杂环]
updated: 2026-07-25
aliases: [Clayden-Ch29-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 29 Problem 7
cross_references: ["[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]", "[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
---
# 题-556: 2-吡啶酮→胺→硝化→酶抑制剂合成

## 题目

**【中文】**请提出将 2-吡啶酮（2-pyridone）转化为图中所示胺的方法。该胺经硝化得到化合物 A，其 NMR 谱如下。A 的结构是什么？为什么生成的是这个异构体？A 的 NMR：δH 1.0 (3H, t, J 7 Hz)、1.7 (2H, sextet, J 7 Hz)、3.3 (2H, t, J 7 Hz)、5.9 (1H, broad s)、6.4 (1H, d, J 8 Hz)、8.1 (1H, dd, J 8 and 2 Hz)、8.9 (1H, d, J 2 Hz)。需要把化合物 A 转化为下图所示的酶抑制剂，这可以如何实现？

**【原文】**Suggest how 2-pyridone might be converted into the amine shown. This amine undergoes nitration to give compound A with the NMR spectrum given. What is the structure of A? Why is this isomer formed?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ff175fa4d92dce98f0cf83c31a71202b7354536539931b9c94e79ba8dcd11c3b.jpg]]

NMR of A: δH 1.0 (3H, t, J 7 Hz), 1.7 (2H, sextet, J 7 Hz), 3.3 (2H, t, J 7 Hz), 5.9 (1H, broad s), 6.4 (1H, d, J 8 Hz), 8.1 (1H, dd, J 8 and 2 Hz), and 8.9 (1H, d, J 2 Hz). Compound A was needed for conversion into the enzyme inhibitor below. How might this be achieved?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/10a25afb8551a31e3d337ad061c6fbcf204336638632a8b48becfd00c789c901.jpg]]

## 参考答案

**Answer (English)**: The first step requires nucleophilic substitution so we could convert the pyridine into 2-chloropyridine and displace the chlorine with the amine.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/186d7563e29d8ea638685108dd0bdfe1ac3d5554a532c0a78327e8ab21776185.jpg]]

The nitration occurs only because this pyridine is activated by the extra amino group. Key points from NMR: (i) A has only three aromatic protons so nitration has occurred on the ring, (ii) there is only one coupling large enough to be between ortho hydrogens (8 Hz), and (iii) there is a proton that has only meta coupling (2 Hz) a long way downfield. All this fits the structure shown. The amino group directs ortho, para and para is preferred sterically.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/990666fa1ea20be2360699c050f154bee5b77e2d8f184ee7de7b1b5a33b3a89f.jpg]]

To get the enzyme inhibitor we need to reduce the nitro group to an amine and add the new chain to the other amine. This conjugate addition is best done first while there is only one nucleophilic amine. The ester is probably the best derivative to use.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/bf8501bf0dcb4554c0f76d2e30ea45ccd7f35ff636f758e711cc532e4a9db2bd.jpg]]

**中文解析**：

**步骤一：2-吡啶酮→2-氯吡啶→胺基吡啶**
1. 将2-吡啶酮转化为2-氯吡啶（POCl₃处理），再用丙胺进行亲核取代得到胺基吡啶

**步骤二：硝化得到化合物A**
1. 氨基是活化基团（邻对位定位基），使吡啶环可以发生硝化
2. NMR分析：(i) 3个芳香H说明硝化在环上；(ii) 只有一个大的邻位偶合（8 Hz）；(iii) 一个只有间位偶合（2 Hz）的H在低场（8.9 ppm，受吡啶N和NO₂双重去屏蔽）
3. 硝基在氨基的对位（位阻有利）

**步骤三：转化为酶抑制剂**
1. 先做Michael加成（胺与α,β-不饱和酯的共轭加成），此时只有一个亲核胺
2. 再还原硝基为氨基

> **NMR解题技巧**：吡啶N和NO₂的去屏蔽效应使特定H显著低场移动，是确定取代位点的关键。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[吡啶]] | 吡啶酮的转化和吡啶环的反应性 | 直接 |
| [[芳香亲电取代]] | 活化吡啶环的硝化反应和区域选择性 | 直接 |
| NMR解析 | 利用偶合常数和化学位移推断硝化位点 | 直接 |
| [[共轭加成]] | 胺对α,β-不饱和酯的Michael加成 | 间接 |

## 解题思路

1. **读题定位**：多步合成问题——2-吡啶酮→胺→硝化→酶抑制剂。需要NMR辅助推断A的结构
2. **🔑 关键转换**：POCl₃处理吡啶酮→2-氯吡啶→SNAr引入丙胺→氨基活化硝化→NMR验证→共轭加成+还原
3. **验证**：检查NMR数据是否与推断结构一致——3个芳香H、特定偶合模式、低场H

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 硝化位点判断错误 | 没有结合NMR数据分析 | 利用偶合常数（J=8 Hz邻位，J=2 Hz间位）定位 | δ 8.9的H为什么特别低场？ |
| 先还原硝基再做共轭加成 | 没考虑化学选择性 | 共轭加成先做——此时只有一个亲核胺，避免双反应 | 如果先还原硝基会出什么问题？ |
| 2-吡啶酮直接硝化 | 吡啶酮本身活性不够 | 需要先转化为胺基吡啶，氨基活化后才能硝化 | 氨基如何活化吡啶环的硝化？ |