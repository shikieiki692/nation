---
title: 题-530-Clayden-Ch41-P7-设计自己的不对称合成
type: 题目
fidelity: 原书逐字
submodule: 不对称合成
exam_stage: 决赛
subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[不对称合成]]", "[[合成设计]]"]
tags: [化竞, Clayden, 有机化学, 不对称合成, 逆合成分析]
updated: 2026-07-25
aliases: [Clayden-Ch41-P7]
source: Clayden Organic Chemistry 2nd Ed. Chapter 41 Problem 7
cross_references: ["[[题-291-Clayden-Ch14-P1-五个分子手性判断]]", "[[题-477-Clayden-Ch27-P1-分子内硫叶立德共轭加成环丙烷化]]", "[[题-478-Clayden-Ch27-P2-硫叶立德化学区域和立体化学]]", "[[题-292-Clayden-Ch14-P2-旋光值区分]]"]
module: 有机化学
status: 已填充
---
# 题-530: 设计自己的不对称合成

## 题目

Suggest syntheses for single enantiomers of these compounds.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/86b8bb5e36587eb2b907022cb58bf52d59f4f34228461d8b5508ea442eab8bdb.jpg]]

**原文题目**：Suggest syntheses for single enantiomers of these compounds.

## 参考答案

**Answer (English)**: The first compound is an ester derived from a cyclic secondary alcohol that could be made from the corresponding enone by asymmetric reduction. Reduction with Corey's CBS reducing agent gave the alcohol in 93% ee.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/98be4563317de54355836cb061bb50aedbfcf992dac5732899c65c57ca42b3a5.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/2161062f994621105d4ac702b97c39e18349041d1a9bdca28670cffdf95c394a.jpg]]

The second compound could be made by a Wittig reaction with a stabilized ylid and the required diol aldehyde derived from an epoxy-alcohol and hence an allylic alcohol by Sharpless epoxidation.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/341c403c8b1d0c568a7fb449064932c2ce5e6c42ce81c87579a6a240a1eee64e.jpg]]

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_400-521_images/6105e944be540598da02b935ea8f7b1cda473a9c7059b0943237618227ba468a.jpg]]

**中文解析**：

**整体策略分析**：
本题要求为两个手性目标分子设计单一对映体的合成路线。需要进行逆合成分析，识别目标分子的关键结构特征，然后匹配合适的不对称合成方法。这考查的是将不对称合成知识综合应用于合成设计的能力。

**目标化合物1——环状手性酯**：

*逆合成分析*：
- 酯键切断 → 手性环状仲醇 + 酰氯/酸酐
- 手性环状仲醇 ← 不对称还原环状烯酮

*合成路线*：
1. 制备相应的环状烯酮底物
2. **Corey-Bakshi-Shibata (CBS)不对称还原**：使用CBS手性噁唑硼烷催化剂 + BH₃·THF，将环状烯酮还原为手性仲醇
3. ee值可达**93%**
4. 与相应的酸/酰氯进行酯化

*CBS还原的立体选择性原理*：
- CBS催化剂通过配位到羰基氧上，将BH₃定向传递到羰基的一个面
- 催化剂的手性噁唑硼烷环决定了H⁻传递的面选择性
- 这是催化不对称还原的经典应用

**参考文献**：E. J. Corey and A. V. Gaval, Tetrahedron Lett., 1988, 29, 3201。

**目标化合物2——含手性1,2-二醇和烯烃的链状化合物**：

*逆合成分析*：
- Wittig反应切断 → 醛组分 + 磷叶立德
- 醛 ← 环氧化物开环 → 烯丙醇 ← Sharpless不对称环氧化
- 烷基部分 ← 稳定化叶立德（Ph₃P=CHCO₂R）

*合成路线*：
1. 从简单的烯丙醇出发
2. **Sharpless不对称环氧化**：使用Ti(OiPr)₄、(+)-或(-)-DET、TBHP，选择性氧化烯丙醇的一个面，得到手性环氧化物
3. 环氧化物选择性开环 → 手性二醇醛
4. **Wittig反应**：稳定化叶立德（如Ph₃P=CHCO₂Et）与醛反应，得到含烯烃的目标化合物

*为什么选Sharpless环氧化*：
- 底物是烯丙醇——Sharpless环氧化的完美底物
- 两种DET对映体都可获得，因此两种产物对映体都可合成
- 引用：S. Masamune et al., J. Am. Chem. Soc. 1975, 97, 3512

**关键教学要点**：
- 不对称合成设计的核心是"结构特征→方法匹配"
- CBS还原适合手性仲醇，Sharpless环氧化适合手性环氧化物/1,2-二醇
- 两种方法都是催化不对称方法（高效率、高ee值）

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[不对称合成]] | 综合运用不对称还原和不对称环氧化设计合成路线 | 直接 |
| [[合成设计]] | 逆合成分析和目标分子切断 | 直接 |
| [[逆合成分析]] | 从目标分子倒推到可用原料 | 直接 |
| CBS还原 | 催化不对称还原制备手性仲醇 | 间接 |
| [[Sharpless不对称环氧化]] | 烯丙醇的催化不对称环氧化 | 间接 |

## 解题思路

1. **读题定位**：题目要求为两个手性化合物设计单一对映体的合成路线。关键词：单一对映体、合成设计
2. **🔑 关键转换**：(a) 环状仲醇→CBS不对称还原环状烯酮；(b) 含1,2-二醇链状化合物→Sharpless不对称环氧化烯丙醇→开环→Wittig反应
3. **验证**：(a) CBS还原得到93% ee的醇→酯化→目标1；(b) Sharpless环氧化→开环得手性醛→Wittig偶联→目标2

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 不知道用什么方法还原手性仲醇 | 没有将结构特征与方法匹配 | 环状手性仲醇→CBS不对称还原是最经典的方法 | CBS催化剂的结构是什么？ |
| 混淆Sharpless环氧化和双羟化 | 两类反应的底物和产物不同 | 烯丙醇→环氧化物（Sharpless环氧化），烯烃→邻二醇（Sharpless双羟化） | Sharpless环氧化需要什么底物（烯丙醇）？ |
| Wittig反应的叶立德选择不当 | 没有考虑立体化学 | 需要稳定化叶立德（有吸电子基）来构建目标烯烃 | 稳定化和非稳定化叶立德在Wittig反应中有什么区别？ |
| 忽略DET对映体的选择 | Sharpless环氧化可以合成两种对映体 | 使用(+)-DET或(-)-DET可以分别得到两种对映体的环氧化物 | 如何选择DET对映体来得到所需的产物？ |