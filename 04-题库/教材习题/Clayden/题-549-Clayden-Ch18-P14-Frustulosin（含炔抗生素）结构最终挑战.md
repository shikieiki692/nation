---
title: 题-549-Clayden-Ch18-P14-Frustulosin（含炔抗生素）结构最终挑战
type: 题目
fidelity: 原书逐字
submodule: 波谱综合解析
exam_stage: 决赛
subject: 有机化学
difficulty: 5
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[波谱综合解析]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch18-P14]
source: Clayden Organic Chemistry 2nd Ed. Chapter 18 Problem 14
cross_references: ["[[题-415-Clayden-Ch13-P2-酐加MeMgBr产物用IR 13C 1H NMR区分]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]", "[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-414-Clayden-Ch13-P1-五个化合物1H NMR信号和化学位移预测]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-549: Frustulosin（含炔抗生素）结构最终挑战

## 题目

The yellow crystalline antibiotic frustulosin was isolated from a fungus in 1978 and it was suggested the structure was an equilibrium mixture of A and B. Apart from the difficulty that the NMR spectrum clearly shows one compound and not an equilibrium mixture of two compounds, what else makes you unsure of this assignment? Suggest a better structure. Signals marked * exchange with D₂O.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/8923d0e1d186a455453a704119fb912a516fa96f45917c3458886a62a66ba46a.jpg]]

**Frustulosin:**

m/z 202 (100%), 174 (20%);

νmax (cm⁻¹) 3279, 1645, 1613, and 1522;

δH (ppm) 2.06 (3H, dd, J 1.0, 1.6 Hz), 5.44 (1H, dq, J 2.0, 1.6 Hz), 5.52 (1H, dq, J 2.0, 1.0 Hz), 4.5* (1H, broad s), 7.16 (1H, d, J 9.0 Hz), 6.88 (1H, dd, J 9.0, 0.4 Hz), 10.31 (1H, d, J 0.4 Hz), and 11.22* (1H, broad s);

δC (ppm) 22.8, 80.8, 100.6, 110.6, 118.4, 118.7, 112.6, 125.2, 129.1, 151.8, 154.5, and 196.6.

**Warning!** This is difficult—after all, the original authors got it wrong initially. Hint: How might the DBEs be achieved without a second ring?

**Purpose of the problem**: A serious and difficult determination of a natural product as a final challenge.

## 参考答案

**Answer (English)**: Structure B is definitely wrong because the NMR shows only one methyl group, not two, and only one carbonyl group, not two. Structure A looks unlikely because it appears to be unstable, but that is not evidence. The NMR shows two protons on the same end of a double bond (at 5.44 and 5.52 ppm) with the characteristic small coupling, but they are coupled to a methyl group, presumably by allylic coupling, and the methyl group is too far away in B. But what is the signal at 80.8 in the ¹³C NMR? The 'hint' was meant to guide you towards suggesting an alkyne. That solves many of the problems even though the carbons of the alkene and the aromatic ring cannot be assigned with confidence. At least the revised structure is one compound and not two.

■ The true structure was later described with the help of NMR as you can read in R. C. Ronald et al., J. Org. Chem., 1982, 47, 2541 and M. S. Nair and M. Anchel, Phytochemistry, 1977, 16, 390, revised from M. S. Nair and M. Anchel, Tetrahedron Lett., 1975, 2641.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/7c952b30d8725308083d1f92da165b603cdf9a6017befd5b9cfe46baf429e5ac.jpg]]

**中文解析**：

关键解析步骤：

1. **质疑原始结构**：
   - NMR 明确显示单一化合物，而非 A/B 平衡混合物
   - 结构 B 有两个甲基和两个 C=O → 与数据矛盾（实际仅 1 个 Me、1 个 C=O）
   - 结构 A 虽看似不稳定，但不稳定不是排除的充分证据

2. **分子式与不饱和度分析**：
   - M⁺ = 202，从碎片 174 = M⁺-28（丢失 CO）推断含醛基
   - δC 196.6 → 醛羰基（C=O）
   - δC 80.8 → **关键信号！** 这是 sp 杂化碳的典型区域 → 含 C≡C 炔键

3. **¹H NMR 详细分析**：
   - δ 5.44 (1H, dq, J=2.0, 1.6 Hz) + 5.52 (1H, dq, J=2.0, 1.0 Hz)：两个烯氢在同一双键末端（=CH₂），小偶合（J=2.0 Hz）为同碳偶合
   - δ 2.06 (3H, dd, J=1.0, 1.6 Hz)：甲基通过烯丙基偶合与 =CH₂ 相连（J 值很小，符合远程偶合）
   - δ 7.16 (1H, d, J=9.0 Hz) + 6.88 (1H, dd, J=9.0, 0.4 Hz)：邻位偶合的两个芳香氢
   - δ 10.31 (1H, d, J=0.4 Hz)：醛氢（与芳香氢有远程偶合）
   - δ 4.5* + 11.22*：D₂O 交换质子（OH）

4. **¹³C NMR 分析**：
   - δ 196.6：醛 C=O
   - δ 80.8：炔碳（sp 杂化，关键诊断信号）
   - δ 22.8：甲基碳
   - 其余为 sp² 碳（烯烃 + 芳香环）

5. **结论**：Frustulosin 的正确结构含苯环、醛基、末端烯基（=CH₂）和炔键（C≡C），而非原始提出的双环酮结构

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[波谱综合解析]] | 高难度天然产物结构修正——从错误结构到正确结构 | 直接 |
| [[NMR谱学]] | 炔碳 δC ~80 ppm 的诊断意义；烯丙基远程偶合 | 直接 |
| [[质谱]] | M⁺-28 丢失 CO 确认醛基；分子离子稳定性 | 直接 |
| [[天然产物化学]] | 真菌抗生素的结构鉴定历史 | 间接 |

## 解题思路

1. **读题定位**：题目明确提示"原始作者最初搞错了" → 需要质疑给定结构；Hint 指向"不用第二个环也能满足不饱和度" → 暗示三键
2. **🔑 关键转换**：δC 80.8 ppm 是 sp 碳（炔）的"签名"信号 → 引入 C≡C 后，分子式和不饱和度问题全部解决；δH 5.44/5.52 两个 dq 峰 → 末端烯 =CH₂，与甲基有烯丙基远程偶合
3. **验证**：修正后的结构为单一化合物（非平衡混合物），含 1 个 Me、1 个 CHO、1 个 =CH₂、1 个 C≡C → 与全部 NMR 数据吻合

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 接受原始结构 A/B 平衡混合物的解释 | 未注意 NMR 显示单一化合物 | NMR 在正常条件下只显示一套信号，如果是快平衡应看到平均信号，慢平衡应看到两套信号 | 如何从 NMR 判断动态平衡？ |
| 忽略 δC 80.8 的诊断意义 | 不熟悉 sp 碳的 ¹³C 位移范围 | δC 65-90 ppm 是炔碳的特征区域（sp 杂化）；这个信号是解开全题的钥匙 | 炔碳和烯碳的 ¹³C 化学位移有何区别？ |
| 将 δH 5.44/5.52 的小偶合误认为仪器噪声 | 未识别末端烯的同碳偶合特征 | J=2.0 Hz 是 =CH₂ 两个氢的同碳偶合（²J_HH），dq 峰中的 q 来自与甲基的烯丙基偶合 | 末端烯烃的 ¹H NMR 有什么特征偶合模式？ |