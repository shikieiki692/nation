---
title: 题-534-Clayden-Ch41-P11-手性靶分子高效合成路线
type: 题目
fidelity: 原书逐字
submodule: 不对称合成
exam_stage: 决赛
subject: 有机化学
difficulty: 4
teaching_level: 竞赛拔高
syllabus_codes: ["21"]
knowledge_points: ["[[不对称合成]]", "[[逆合成分析]]"]
tags: [化竞, Clayden, 有机化学, 不对称合成, 药物合成, Evans助剂]
updated: 2026-07-25
aliases: [Clayden-Ch41-P11]
source: Clayden Organic Chemistry 2nd Ed. Chapter 41 Problem 11
cross_references: ["[[题-292-Clayden-Ch14-P2-旋光值区分]]", "[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]", "[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
---
# 题-534: 手性靶分子高效合成路线

## 题目

This compound was developed by the Nutrasweet company as an artificial sweetener. Propose a strategy for its synthesis. Would your proposed approach still be suitable if the compound had turned out to be a successful product, required in multi-tonne quantities?

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/4b70eb2c1a766b75fe5b6314543c5fa7d73dd6452157c773e18c265bc3dfa76f.jpg]]

**原文题目**：This compound was developed by the Nutrasweet company as an artificial sweetener. Propose a strategy for its synthesis. Would your proposed approach still be suitable if the compound had turned out to be a successful product, required in multi-tonne quantities?

## 参考答案

**Answer (English)**: The target can be best disconnected into three fragments at the amide bonds. The aminopyridine can be made by the standard methods of heterocycle synthesis, so we are more interested in the other two chiral fragments. The middle one is an amino acid, and you should recognize it as a member of the chiral pool, (S)-glutamic acid, so this poses no problem of synthesis. The final fragment is a simple chiral carboxylic acid, so we need a method for its asymmetric synthesis. The most obvious choice is probably an asymmetric alkylation using Evans' oxazolidinone auxiliary.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/709190b06689d8828ad7c66b83efa86d01b5df1455b7009687da2ec904f69a81.jpg]]

If this compound were needed on the tonne scale then auxiliary chemistry is no good, however efficient recycling may be. A good alternative for the synthesis of compounds with unfunctionalized chiral centres adjacent to carboxylic acids or alcohols is the use of ruthenium-catalysed hydrogenation.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/7204ce8e1159631d8eda97b4fd40d22432588e10b3363943ab50493f1c014425.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/69dafe18e2073d350a1c391f937f6997c493bed028fd776dfa2e56dd1d6afafe.jpg]]

**中文解析**：

**整体策略分析**：
本题是竞赛拔高题，要求设计一个包含三个片段的复杂手性目标分子的合成路线，并评估路线在实验室规模（克级）和工业规模（吨级）下的适用性。这需要综合运用逆合成分析、手性池策略、手性助剂法和催化不对称方法，并理解不同规模下合成策略的选择原则。

**逆合成分析——三片段切断**：
目标分子可通过两个酰胺键切断为三个片段：
1. **片段A**：氨基吡啶——通过杂环合成标准方法制备（第30章内容）
2. **片段B**：中间体氨基酸——**(S)-谷氨酸（glutamic acid）**
3. **片段C**：手性羧酸——需要不对称合成

**片段B——(S)-谷氨酸**：
- 这是手性池化合物，天然存在，光学纯度100%
- 作为谷氨酸家族的天然氨基酸，价格低廉
- 需要适当保护以形成正确的酰胺键
- **无需不对称合成**——手性池策略的典型应用

**片段C——手性羧酸的不对称合成（实验室规模）**：
- **首选方法：Evans手性噁唑烷酮助剂法**
  - 路线：(a) 己酸与Evans噁唑烷酮形成酰亚胺；(b) 用NaHMDS生成烯醇盐；(c) MeI烷基化（非对映选择性）；(d) 移除助剂，释放手性羧酸
  - Evans助剂的噁唑烷酮环上的苄基/异丙基控制烷基化的面选择性
  - ee值通常>95%
  - 适合克级到百克级制备

**工业规模（吨级）的策略转换**：
- **Evans助剂法不适合吨级生产**：即使助剂回收率高，化学计量使用手性助剂在吨级下成本过高
- **替代方案：Ru催化不对称氢化**
  - 对于未官能团化的手性中心（邻近羧酸或醇），Ru催化氢化是优秀的工业方法
  - 催化量的手性配体（如BINAP-Ru）即可实现高ee值
  - 原子经济性高，催化剂可以回收再利用
  - 适合吨级生产

**两种规模策略的对比**：

| 特征 | 实验室规模（克级） | 工业规模（吨级） |
|------|---------------------|---------------------|
| 手性源 | Evans噁唑烷酮助剂（化学计量） | Ru催化氢化（催化量） |
| ee值 | >95% | >95% |
| 成本考虑 | 助剂成本可接受 | 助剂成本不可接受 |
| 优势 | 方法可靠，底物范围广 | 原子经济性高，催化剂可回收 |

**关键教学要点**：
- 合成策略必须考虑生产规模——实验室方法不一定适用于工业生产
- 手性助剂法适合小规模（高选择性但需化学计量手性源）
- 催化不对称方法适合大规模（催化量手性源，原子经济性高）
- 手性池策略在有合适天然原料时始终是首选

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[不对称合成]] | 实验室vs工业规模的策略选择 | 直接 |
| [[逆合成分析]] | 三片段切断和手性中心的来源 | 直接 |
| [[药物合成]] | 药物中间体的合成路线设计和规模评估 | 直接 |
| [[手性助剂]] | Evans噁唑烷酮助剂法的非对映选择性烷基化 | 间接 |
| [[不对称催化还原]] | Ru催化不对称氢化的工业应用 | 间接 |
| [[手性池合成]] | 天然(S)-谷氨酸的利用 | 间接 |

## 解题思路

1. **读题定位**：题目要求设计合成策略，并评估克级→吨级的适用性。关键词：人工甜味剂、策略、multi-tonne、Nutrasweet
2. **🔑 关键转换**：三片段切断→片段B是手性池(S)-谷氨酸→片段C用Evans助剂法（实验室）/Ru催化氢化（工业）→片段A是杂环合成
3. **验证**：(a) 每个片段的合成方法是否可靠？(b) 酰胺键连接是否可行？(c) 工业规模下成本是否合理？

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 不识别(S)-谷氨酸为手性池化合物 | 对常见氨基酸的手性池应用不熟 | 天然氨基酸是最重要的手性池来源，(S)-谷氨酸无需不对称合成 | 手性池策略有什么优势和局限？ |
| 认为Evans助剂法适合所有规模 | 没有考虑工业成本 | 化学计量手性助剂在吨级下成本过高，应转用催化不对称方法 | 催化不对称方法相比手性助剂法的核心优势是什么？ |
| 不知道如何评估规模适用性 | 缺乏工业化学思维 | 评估标准：手性源是否催化量、原子经济性、催化剂回收性、总步骤数 | 什么因素决定一个方法能否放大到吨级？ |
| 忘记需要保护谷氨酸的官能团 | 没有考虑化学选择性 | 谷氨酸有两个羧基和一个氨基，需要选择性保护才能形成正确的酰胺键 | 如何选择性保护谷氨酸的α-羧基？ |