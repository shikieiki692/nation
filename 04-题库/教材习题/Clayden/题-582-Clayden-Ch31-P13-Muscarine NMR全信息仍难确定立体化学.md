---
title: 题-582-Clayden-Ch31-P13-Muscarine NMR全信息仍难确定立体化学
type: 题目
fidelity: 原书逐字
submodule: 立体电子效应
exam_stage: 初赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[NMR谱学]]"]
tags: [化竞, Clayden, 有机化学, 天然产物化学]
updated: 2026-07-25
aliases: [Clayden-Ch31-P13]
source: Clayden Organic Chemistry 2nd Ed. Chapter 31 Problem 13
cross_references: ["[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]", "[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]"]
module: 有机化学
status: 已填充
---
# 题-582: Muscarine NMR全信息仍难确定立体化学

## 题目

Muscarine, the poisonous component of the death cap mushroom, has the structure below. We give the proton NMR spectrum. Can you see any definite evidence for the stereochemistry? Couplings are in Hz, m stands for multiplet, and \* means that the proton exchanges with D₂O.

$\delta_{H}$ 1.16 (3H, d, J 6.5), 1.86 (1H, ddd, J 12.5, 9.5, 9.5), 2.02 (1H, ddd, J 12.5, 6.0, 2.0), 3.36 (9H, s), 3.54 (1H, dd, J 13, 9.0), 3.92 (1H, dq, J 2.5, 6.5), 4.03 (1H, m), 4.30* (1H, d, J 3.5), and 4.68 (1H, m).

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/6ef9011e8f5121eb7175fe29f4f02c77bab03b76cf034dc532e0cfce2bc08819.jpg]]

**原文题目**：Can you see any definite evidence for the stereochemistry of muscarine from the NMR?

## 参考答案

**Answer (English)**: Couplings round five-membered rings tend to be much the same whether they are ²J (geminal), ³J_cis, or ³J_trans (vicinal). Even so, the two diastereotopic CH₂ groups are easy to find with their large ²J couplings of 13 and 12.5 Hz. The one with extra coupling must be in the side chain and the other in the ring. You will see that it is very difficult to get conclusive evidence on stereochemistry from NMR alone without using NOE. You should see that, in general, cis couplings in five-membered rings tend to be larger than trans, though there are many, many exceptions!

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/139d0671a45b1e1e86053439c23887bcf5cd12c78b26074c830a85cdb15c895b.jpg]]

**中文解析**：

关键步骤：
1. **五元环偶合特点**：五元环上的偶合——²J（同碳）、³J_cis和³J_trans的值往往非常接近，难以区分
2. **信号归属**：
   - 3.36 (9H, s)：三甲基铵基NMe₃⁺
   - 1.16 (3H, d, J=6.5)：侧链甲基（CHMe）
   - 1.86和2.02 (ddd, J=12.5)：两个CH₂的非对映体氢（²J=12.5 Hz）
   - 3.54 (dd, J=13, 9.0)：另一个CH₂的非对映体氢
   - 4.30* (d, J=3.5, D₂O交换)：OH基团
3. **立体化学困境**：
   - 五元环中cis偶合通常大于trans（但有很多例外）
   - 没有NOE数据，仅靠偶合常数无法确定立体化学
4. **结论**：NMR本身不足以确定muscarine的立体化学——需要NOE实验

> **注意**：这是本章的重要教训——即使有完整的NMR数据，五元环体系的立体化学有时仍无法仅靠偶合常数确定。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[NMR谱学]] | 五元环偶合常数的局限性，NOE的必要性 | 直接 |
| [[立体化学]] | NMR确定立体化学的局限性，cis/trans偶合在五元环中的重叠 | 直接 |
| [[天然产物化学]] | Muscarine（毒鹅膏毒素）的结构与立体化学 | 间接 |

## 解题思路

1. **读题定位**：完整NMR数据，但问题是"能否确定立体化学"——暗示答案可能是"不能"
2. **🔑 关键转换**：五元环偶合常数²J≈³J_cis≈³J_trans→无法区分→需要NOE→NMR本身不够
3. **验证**：检查所有偶合常数是否确实落在无法区分的范围内

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 强行用偶合常数区分五元环立体化学 | 不了解五元环的局限性 | 五元环的²J、³J_cis、³J_trans值太接近，无法可靠区分 | 为什么五元环比六元环更难分析？ |
| 忽略D₂O交换信号的意义 | 没有注意到星号标记 | 4.30*的星号表示D₂O交换→OH基团 | D₂O交换实验有什么用？ |
| 认为NMR总能确定立体化学 | 过度自信 | NMR有局限性——五元环体系常需要NOE辅助 | NOE如何补充NMR的不足？ |