---
title: 题-542-Clayden-Ch18-P7-天然抗生素结构确定（质谱+NMR）
type: 题目
fidelity: 原书逐字
submodule: 波谱综合解析
exam_stage: 决赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[波谱综合解析]]"]
tags: [化竞, Clayden, 有机化学]
updated: 2026-07-25
aliases: [Clayden-Ch18-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 18 Problem 7
cross_references: ["[[题-415-Clayden-Ch13-P2-酐加MeMgBr产物用IR 13C 1H NMR区分]]", "[[题-561-Clayden-Ch30-P2-不熟悉杂环合成和芳香性判断]]", "[[题-414-Clayden-Ch13-P1-五个化合物1H NMR信号和化学位移预测]]", "[[题-560-Clayden-Ch30-P1-吡咯并吡啶三环芳香杂环合成]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
used_in: ["[[有机化学阶段测试卷]]", "[[04-题库/有机化学阶段测试卷]]"]
---
# 题-542: 天然抗生素结构确定（质谱+NMR）

## 题目

**【中文】**从一种微生物中分离得到的一种抗生素可从水中结晶，并且在酸或碱中均能形成不同的晶态盐。其波谱数据如下：质谱 182 (M⁺, 9%)、109 (100%)、74 (15%)；δH（ppm，D₂O 中，pH<1）3.67 (2H, d, J 7)、4.57 (1H, t, J 7)、8.02 (2H, m)、8.37 (1H, m)；δC（ppm，D₂O 中，pH<1）33.5、52.8、130.1、130.6、130.9、141.3、155.9、170.2。请提出该抗生素的结构。本题目的：确定来自天然来源、具有生物活性的化合物的结构。

**【原文】**An antibiotic isolated from a microorganism was crystallized from water and formed different crystalline salts in either acid or base. The spectroscopic data were:

Mass spectrum 182 (M⁺, 9%), 109 (100%), and 74 (15%).

δH (ppm in D₂O at pH<1) 3.67 (2H, d, J 7), 4.57 (1H, t, J 7), 8.02 (2H, m), and 8.37 (1H, m).

δC (ppm in D₂O at pH<1) 33.5, 52.8, 130.1, 130.6, 130.9, 141.3, 155.9, and 170.2. Suggest a structure for the antibiotic.

**Purpose of the problem**: Structure determination of a compound with biological activity from a natural source.

## 参考答案

**Answer (English)**: The solubility and salt formation suggest the presence of both acidic and basic groups, perhaps CO₂H and NH₂ as this is a natural compound. If so, the ¹³C peak at 170.2 ppm is the CO₂H group. The five carbons in the sp² region and protons at 8.0 and 8.4 suggest an aromatic ring, probably a pyridine. The mass spectrum gives an even molecular ion (182) so there must be another nitrogen atom beyond the one in the pyridine. The two sets of aliphatic protons are coupled and the large shift of the ¹H signal at 4.57 ppm suggests a proton between CO₂H and NH₃⁺ (pH <1). We have these fragments:

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/495ba9372316ba887901d63ef9802787deced0717f6a876cf8071767f5356a48.jpg]]

Presumably the aliphatic part must be X or Y, and that leaves just one oxygen atom for a formula of C₈H₁₀N₂O₃ = 182. Only six of the ten H atoms show up in the NMR because the OH, NH₃⁺, and CO₂H protons all exchange rapidly at pH <1.

■ The details of the structure and spectra are in S. Inouye et al., Chem. Pharm. Bull., 1975, 23, 2669; S. R. Schow et al., J. Org. Chem., 1994, 59, 6850 and B. Ye and T. R. Burke, J. Org. Chem., 1995, 60, 2640.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_1-199_images/58c2b162e26cb5600f69a0d71e84e3695b2915436702e96ae3942cc99ad0a4cd.jpg]]

**中文解析**：

关键解析步骤：

1. **溶解性分析**：化合物可从水中结晶，且在酸和碱中形成不同的结晶盐 → 同时含酸性基团（COOH）和碱性基团（NH₂），天然产物特征
2. **质谱分析**：M⁺ = 182（偶数分子离子）→ 含偶数个氮原子（氮规则）；碎片 109 为吡啶部分，74 为含氮侧链
3. **¹H NMR 分析（D₂O, pH<1）**：
   - δ 8.02 (2H, m) + 8.37 (1H, m)：sp² 区域 3 个芳香氢 → 吡啶环
   - δ 4.57 (1H, t, J=7 Hz)：化学位移很大，位于两个吸电子基团之间（COOH 和 NH₃⁺）
   - δ 3.67 (2H, d, J=7 Hz)：与 δ 4.57 的 CH 偶合 → CH₂-CH 结构片段
4. **¹³C NMR 分析**：8 个碳信号，其中 5 个在 sp² 区域（吡啶环碳），170.2 ppm 为 COOH，33.5 和 52.8 为脂肪碳
5. **结论**：结构为含吡啶环的氨基酸类抗生素（pyridylalanine 类），分子式 C₈H₁₀N₂O₃

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[波谱综合解析]] | 综合质谱、¹H NMR、¹³C NMR 确定天然产物结构 | 直接 |
| [[NMR谱学]] | pH<1 条件下活泼氢交换导致部分信号消失 | 直接 |
| [[质谱]] | 偶数分子离子（氮规则）判断含氮原子数目 | 直接 |
| [[氨基酸化学]] | α-氨基酸片段的 NMR 特征位移 | 间接 |

## 解题思路

1. **读题定位**：天然产物 + 两性（酸碱盐）→ 氨基酸类；M⁺ = 182 偶数 → 偶数 N
2. **🔑 关键转换**：¹H NMR 在 pH<1 下仅见 6H（共 10H）→ OH、NH₃⁺、CO₂H 均快速交换不显信号；δ 4.57 的 CH 位于两个吸电子基团之间 → α-氨基酸骨架
3. **验证**：吡啶环（5 个 sp² 碳 + 3 个芳香氢）+ NH₂-CH(COOH)-CH₂-吡啶片段 → C₈H₁₀N₂O₃ = 182，完全吻合

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将 δ 8.0-8.4 信号归属为苯环 | 仅 3 个芳香氢，苯环单取代应有 5 个 | 3 个芳香氢 + 5 个 sp² 碳 → 吡啶环（含 1 个氮原子） | 为什么吡啶环只产生 3 组 ¹H 信号？ |
| 忽略 pH<1 条件下活泼氢交换 | 未注意 D₂O 中酸性条件 | NH₃⁺、CO₂H、OH 质子在 D₂O/pH<1 下全部交换，不出现信号 | 如果在 DMSO-d₆ 中测量，能看到几个额外信号？ |
| 仅凭质谱碎片推断结构 | 未结合 NMR 定量信息 | 质谱碎片提供官能团线索，但必须用 NMR 验证连接方式和空间关系 | m/z 109 和 74 分别对应什么结构片段？ |