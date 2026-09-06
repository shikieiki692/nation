---
title: 题-577-Clayden-Ch31-P8-二维到三维立体化学
type: 题目
fidelity: 原书逐字
submodule: 立体电子效应
exam_stage: 初赛
source_subject: 有机化学
difficulty: 4
teaching_level: 拓展
syllabus_codes: ["21"]
knowledge_points: ["[[立体化学]]"]
tags: [化竞, Clayden, 有机化学, 偶合常数]
updated: 2026-07-25
aliases: [Clayden-Ch31-P8]
source: Clayden Organic Chemistry 2nd Ed. Chapter 31 Problem 8
cross_references: ["[[题-550-Clayden-Ch29-P1-杂环上亲电亲核取代产物预测]]", "[[题-551-Clayden-Ch29-P2-烷基吡啶LHMDS侧链延伸]]"]
module: 有机化学
status: 已填充
subject_module: 有机化学
pack: 模块习题集
source_category: 教材课后习题
---
# 题-577: 二维到三维立体化学+Karplus关系

## 题目

**【中文】**该醛与该酮（见图）在碱作用下反应，生成化合物 A，其质子 NMR 谱为：$\delta_{H}$ 1.10 (9H, s)、1.17 (9H, s)、6.4 (1H, d, J 15) 和 7.0 (1H, d, J 15)。它的结构是什么？（不要忘记立体化学！）当该化合物与 HBr 反应时生成化合物 B，其 NMR 谱为：$\delta_{H}$ 1.08 (9H, s)、1.13 (9H, s)、2.71 (1H, dd, J 1.9, 17.7)、3.25 (dd, J 10.0, 17.7) 和 4.38 (1H, dd, J 1.9, 10.0)。请提出 B 的结构，归属其谱图，并给出 B 形成的机理。

**【原文】**Reaction between this aldehyde and ketone in base gives a compound A with the proton NMR spectrum: $\delta_{H}$ 1.10 (9H, s), 1.17 (9H, s), 6.4 (1H, d, J 15), and 7.0 (1H, d, J 15). What is its structure? (Don't forget stereochemistry!). When this compound reacts with HBr it gives compound B with this NMR spectrum: $\delta_{H}$ 1.08 (9H, s), 1.13 (9H, s), 2.71 (1H, dd, J 1.9, 17.7), 3.25 (dd, J 10.0, 17.7), and 4.38 (1H, dd, J 1.9, 10.0). Suggest a structure, assign the spectrum, and give a mechanism for the formation of B.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/ab2547e775b6153493133b94fd8c603ca13aea44d412ea0b122760fa8d3dadd3.jpg]]

**原文题目**：Determine the structure of A and B from NMR, assign spectra, and give mechanism for B formation.

## 参考答案

**Answer (English)**: The structure of A is easy. It has a trans alkene with two H's (J 15) and two tertiary butyl groups. There isn't much else except a carbonyl group so it must be an aldol product between the enolizable ketone and the unenolizable aldehyde.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/7f8247649ccb3b25501619bc95eefd01653288bd5dd177eec1ef61334888683b.jpg]]

B is more difficult. The alkene has obviously gone (no signals beyond 4.48) and there is one extra H. It looks as though HBr has added. The 17.7 coupling cannot be a trans alkene as the chemical shifts are too small, so it must be geminal coupling. This means that the molecule must be chiral so that the two hydrogens on the same carbon are diastereotopic. In fact, the expected conjugate addition of HBr to the enone has occurred.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/78e563c650978128c5fc7ef0f1157ecfc6b4caa215195922d0de37cb193471a4.jpg]]

The three hydrogens form an ABX system: A and B are the diastereotopic CH₂ group ($J_\mathrm{AB}$ = 17.7) and X is the CHBr proton ($J_\mathrm{AX}$ = 10 and $J_\mathrm{BX}$ = 1.9). It is not normally possible to say which proton is A and which B but here the large groups, along with the big difference between the two coupling constants, allow us to surmise there is one favoured conformation with dihedral angles of about 180° and 60°.

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/195e618111e8c305016cfb4a4dd8ccbec8ffd42d10e516ab558ff7649f13f8db.jpg]]

favoured conformation has large groups antiperiplanar

![[06-外部资料导入/clayden 有机习题/课后习题答案及解析clayden-SolutionsManualtoAccompanyOrganicChemistry_200-399_images/5c7f8b5e548be9d276ef574697730feb1dd73ba4d53188b546caa4b39f312672.jpg]]

³J 1.9 Hz (60° angle)    (180° angle)

**中文解析**：

关键步骤：
1. **化合物A分析**：
   - 两个t-Bu单峰(9H each)→两个叔丁基
   - 6.4和7.0(d, J=15)→反式烯烃（J=15 Hz）
   - 羰基信号→A是醛和酮的醇醛缩合产物（反式烯酮）
2. **化合物B分析**：
   - 烯烃信号消失（无>4.48的信号）→HBr加成
   - 17.7 Hz偶合→同碳偶合²J(CH₂)（不是烯烃偶合，因化学位移太小）
   - ABX系统：A和B是CH₂的两个非对映体氢($J_\mathrm{AB}$=17.7)，X是CHBr($J_\mathrm{AX}$=10, $J_\mathrm{BX}$=1.9)
3. **Karplus关系应用**：
   - J=10 Hz→二面角~180°（反式共平面）→H与Br反式
   - J=1.9 Hz→二面角~60°（邻位交叉）→H与Br邻位交叉
   - 大基团倾向于反式共平面排列

> **注意**：17.7 Hz的同碳偶合只有在两个氢化学不等价（非对映体）时才能观察到——这证明分子是手性的。

## 知识点映射

| 关联 KP | 考查角度 | 直接/间接 |
|---|---|:---:|
| [[立体化学]] | 反式烯烃识别、非对映体CH₂的判断、ABX系统 | 直接 |
| [[NMR谱学]] | 醇醛缩合产物NMR分析、HBr加成产物的ABX系统 | 直接 |
| [[偶合常数]] | Karplus关系：J与二面角的对应（180°→大J，60°→小J） | 直接 |

## 解题思路

1. **读题定位**：两步反应——碱催化醇醛缩合得A，HBr加成得B；需要确定结构、归属NMR、写机理
2. **🔑 关键转换**：A=反式烯酮（J=15 Hz）→HBr共轭加成→B含ABX系统→Karplus关系判断CH₂与CHBr的相对构象
3. **验证**：检查A的碳数和氢数，B的ABX偶合常数是否与推定构象一致

## 易错分析

| 错误 | 原因 | 纠正 | 课堂提问 |
|------|------|------|----------|
| 将17.7 Hz误认为烯烃偶合 | 没有注意化学位移范围 | 2.71和3.25 ppm太小不可能是烯烃，必须是CH₂的同碳偶合 | 为什么同碳偶合能观察到？ |
| 忘记非对映体CH₂才能观察²J | 对非对映体概念不清 | 只有手性分子中CH₂的两个氢才化学不等价，才能观察到同碳偶合 | 如何判断CH₂是否非对映体？ |
| Karplus关系应用错误 | 混淆J值与角度的关系 | 180°→大J(10 Hz)，60°→小J(1.9 Hz)；90°→J≈0 | Karplus曲线的形状是什么？ |