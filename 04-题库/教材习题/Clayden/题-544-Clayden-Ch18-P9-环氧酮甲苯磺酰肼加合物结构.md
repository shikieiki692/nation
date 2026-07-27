---
title: 题-544-Clayden-Ch18-P9-环氧酮甲苯磺酰肼加合物结构
type: 题目
submodule: 波谱综合解析
exam_stage: 决赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[波谱综合解析]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch18-P9]
source: Clayden Organic Chemistry 2nd Ed. Chapter 18 Problem 9
cross_references: ["[[题-414-Clayden-Ch13-P1-五个化合物1H NMR信号和化学位移预测]]", "[[题-415-Clayden-Ch13-P2-酐加MeMgBr产物用IR 13C 1H NMR区分]]", "[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]"]
module: 有机化学
status: 已填充
---
# 题-544: 环氧酮甲苯磺酰肼加合物结构

## 题目

Treatment of this epoxy-ketone with tosyl hydrazine gives a compound with the spectra shown below. What is its structure?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/d23280442b7c221d9b91ea580838e713785b9ad4c259ec1b8b00d938d5257e50.jpg]]

m/z 138 (M⁺, 12%), 109 (56%), 95 (100%), 81 (83%), 82 (64%), and 79 (74%);

IR 3290, 2115, 1710 cm⁻¹;

δH (ppm in CDCl₃) 1.12 (6H, s), 2.02 (1H, t, J 3 Hz), 2.15 (3H, s), 2.28 (2H, d, J 3 Hz), and 2.50 (2H, s);

δC (ppm in CDCl₃) 26, 31, 32, 33, 52, 71, 82, 208.

**Purpose of the problem**: Further practice at structure determination, adding a curious chemical shift.

## 参考答案

**Answer (English)**: The compound is an alkyne formed by a reaction known as the Eschenmoser fragmentation. It is not possible to assign all the ¹³C NMR signals but you can spot the alkyne carbons in the region 70–85 ppm and the alkyne CH at about 2 in the proton NMR. The triple bond signals in the IR at about 2150 cm⁻¹ is a give-away too. Alkyne C–H bonds are strong and come well above 3000 in the IR. The lack of vicinal coupling in the ¹H NMR helps identify the rest of the skeleton of the molecule.

■ G. Magnusson and S. Thorén, J. Org. Chem., 1973, 38, 1380.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/f596b3c97bb9048cfe9106f39e281ad5a14b00acfe7620ea29fee6a348e125cd.jpg]]

**中文解析**：

关键解析步骤：

1. **IR 分析**：
   - 3290 cm⁻¹：≡C-H 伸缩振动（末端炔烃 C-H，特征性 > 3000 cm⁻¹）
   - 2115 cm⁻¹：C≡C 三键伸缩振动
   - 1710 cm⁻¹：C=O 酮羰基
2. **质谱分析**：M⁺ = 138，碎片 95 = M⁺-43 (C₃H₇O 或 C₃H₅N)，81 = M⁺-57
3. **¹H NMR 分析**：
   - δ 2.02 (1H, t, J=3 Hz)：末端炔氢（≡C-H），与相邻 CH₂ 偶合
   - δ 2.28 (2H, d, J=3 Hz)：与炔氢偶合的 CH₂
   - δ 1.12 (6H, s) + 2.15 (3H, s)：孤立的甲基，无邻位偶合
   - δ 2.50 (2H, s)：孤立 CH₂，无邻位偶合
4. **¹³C NMR 分析**：
   - δ 71, 82：炔烃碳（sp 杂化碳典型区域）
   - δ 208：酮羰基
   - 其余为 sp³ 碳
5. **反应背景**：Eschenmoser 碎裂反应 — 环氧酮与甲苯磺酰肼反应后发生 C-C 键断裂，生成末端炔烃
6. **结论**：产物为含末端炔基的酮，结构为 5,5-二甲基-1-己炔-4-酮类化合物

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[波谱综合解析]] | 从 IR 和 NMR 综合识别炔烃官能团 | 直接 |
| [[化学位移]] | 炔碳 70-85 ppm 的特征 ¹³C 位移；末端炔氢 ~2 ppm | 直接 |
| [[NMR谱学]] | 末端炔氢的小偶合常数（J ≈ 3 Hz） | 直接 |
| [[重排反应]] | Eschenmoser 碎裂反应的结构转化 | 间接 |

## 解题思路

1. **读题定位**：环氧酮 + TsNHNH₂ → 产物含 N？不，M⁺ = 138（偶数），说明 N 已离去 → Eschenmoser 碎裂产生炔烃
2. **🔑 关键转换**：IR 3290 + 2115 cm⁻¹ → 末端炔烃的"指纹"组合；δC 71/82 确认 sp 碳；δH 2.02 (t) 为 ≡C-H
3. **验证**：6H 单峰（CMe₂）+ 3H 单峰（COMe）+ 2H 单峰（孤立 CH₂）+ 2H + 1H 偶合对（CH₂-C≡CH）→ 所有片段吻合

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 忽略 IR 3290 cm⁻¹ 的炔氢信息 | 仅关注 2115 cm⁻¹ 的三键峰 | 3290 cm⁻¹（>3000）是末端炔 C-H 的特征，区别于烯烃 C-H（~3080）和芳烃 C-H（~3030） | 末端炔与内炔的 IR 有何区别？ |
| 将 δC 208 误判为醛 | 未结合 ¹H NMR 中无醛氢信号 | 208 ppm 为酮羰基（醛通常 >190 ppm 且有 ¹H 信号 ~9-10 ppm） | 醛和酮的 ¹³C NMR 化学位移有何差异？ |
| 误认为产物仍含氮 | 未注意 M⁺ 为偶数（氮规则） | TsNHNH₂ 参与反应但 N 以 N₂ 形式离去，产物不含氮 | Eschenmoser 碎裂的驱动力是什么？ |