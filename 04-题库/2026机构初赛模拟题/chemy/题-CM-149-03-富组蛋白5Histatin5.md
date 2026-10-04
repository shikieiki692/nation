---
title: "题-CM-149-03-富组蛋白5Histatin5"
aliases: ["题-CM-149-03"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "chemy 第37届 决赛25 第 3 题"
module: "2026机构初赛模拟题"
source_subject: 结构化学
syllabus_codes: [6, 7, 15, 17]
knowledge_points:
  - "[[量热法]]"
  - "[[平衡常数]]"
  - "[[Gibbs自由能]]"
  - "[[CsCl型结构]]"
  - "[[晶胞]]"
tags: [化竞, 题目, 初赛, 机构模拟题, chemy]
updated: 2026-10-04
status: 已填充
exam_stage: 初赛
subject_module: 结构化学
pack: 综合模拟卷
submodule: chemy
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_tier: 2
source_norm: "chemy-第37届决赛模拟25"
source_file: "chemy试题/第37届Chemy题目合集..md"
---

# 题-CM-149-03-富组蛋白5Histatin5

## 题目

### 第 3 题

## 第 3 题（16 分，占 9%）反应平衡常数的测定

富组蛋白 5（Histatin 5，Hist5，结构为 DSHAKRHHGYKRKFHEKHHSHRGY）是存在于人类唾液中的一种抗菌肽，属于先天性免疫系统的一部分。Hist5 能结合 $Zn^{2+}$ 来调节其生理活性，以抵抗白色念珠菌 Candida albicans。使用等温滴定量热法 (isothermal titration calorimetry, ITC)，我们能测得该结合反应的平衡常数。

## 3-1 假设体系中仅有如下四个反应：

$$
\begin{array}{c c}\mathrm {Zn - Buffer^{2 + } \rightarrow Zn^{2 + } + Buffer}&- \Delta H _{\mathrm{Zn-Buff}}\\\mathrm {Zn^{2 + } + Peptide\rightarrow Zn - Peptide^{2 + }}&\Delta H _{\mathrm{Zn-Pep}}\\\mathrm {Peptide - (H^{+}) _{m} \rightarrow Peptide+ mH ^{+}}&- \Delta H _{\mathrm{Pep-H}}\\\mathrm {Buffer+ H ^{+} \rightarrow Buffer- H ^{+}}&\Delta H _{\mathrm{Buff-H}}\end{array}
$$

Buffer 为体系中的缓冲物质，写出滴定总反应 Peptide- $(\mathrm{H}^{+})_{m} + \mathrm{Zn}-\mathrm{Buffer}^{2+} + (m-1)\mathrm{Buffer} \rightarrow \mathrm{Zn}-\mathrm{Peptide}^{2+} + m\mathrm{Buffer}-\mathrm{H}^{+}$ 的焓变 $\Delta H_{ITC}$ 的表达式。

3-2 由于 $Zn^{2+}$ 和 Buffer 以及 $H^{+}$ 和 Buffer 的结合焓可以提前测得，因此可以通过线性回归的方式求得 $Zn^{2+}$ 与 Peptide 的结合焓。在 $25^{\circ}C$ ，pH = 7.4 时测得实验数据由下表所示。

<table><tr><td>Buffer</td><td> $\Delta H_{ITC}$  (kcal/mol)</td><td> $\Delta H_{Zn-Buff}$  (kcal/mol)</td><td> $\Delta H_{Buff-H}$  (kcal/mol)</td></tr><tr><td>PIPES</td><td>-7.03</td><td>0.46</td><td>-2.78</td></tr><tr><td>MOPS</td><td>-8.68</td><td>0.22</td><td>-5.01</td></tr><tr><td>HEPES</td><td>-8.69</td><td>0.30</td><td>-5.12</td></tr><tr><td>ACES</td><td>-7.66</td><td>-5.18</td><td>-9.34</td></tr></table>

根据上述数据求出 $m$ 和 $\Delta H_{\mathrm{Zn - Pep}} - \Delta H_{\mathrm{Pep - H}}$ 的值， $1\mathrm{cal} = 4.18\mathrm{J}$ 。

3-3 进一步测算可求得 $25^{\circ}C$ ，pH = 7.4 时 ACES 体系下 $\Delta H_{Zn-Pep} = -3.78 kcal/mol, -T\Delta S_{Zn-Pep} = -5.03 kcal/mol$ 。求 $K_{Zn-Pep}$ 。

3-4 控制 pH 不变，改变温度进行实验，发现滴定消耗的 $Zn^{2+}$ 逐渐上升，如下表所示。解释该现象。

<table><tr><td>T/°C</td><td>15</td><td>25</td><td>30</td><td>37</td></tr><tr><td> $n_{Zn}/n_{Hist5}$ </td><td>1.10</td><td>1.26</td><td>1.45</td><td>1.82</td></tr></table>

## 参考答案


$$
3 - 1 \Delta H _{\mathrm{ITC}} = - \Delta H _{\mathrm{Zn-Buff}} + \Delta H _{\mathrm{Zn-Pep}} - \Delta H _{\mathrm{Pep-H}} + m \Delta H _{\mathrm{Buff-H}} (3 \text {分})
$$

3-2 由 3-1 可知 $\Delta H_{\mathrm{ITC}} + \Delta H_{\mathrm{Zn - Buff}} = m\Delta H_{\mathrm{Buff - H}} + \Delta H_{\mathrm{Zn - Pep}} - \Delta H_{\mathrm{Pep - H}}$
回归可得 $y = 0.97x - 3.67, R^{2} = 0.99$ (2分)

故 m = 0.97， $\Delta H_{Zn-Pep} - \Delta H_{Pep-H} = -3.67 \, kcal/mol$ （2 分） $\Delta H_{Buff-H} (kcal/mol)$

![](images/250379b70d54ff617b3ddee729a83d47c0d9d5e7696bca9a5ce8ade98e5a2e5b.jpg)

$$
3 - 3 \Delta G _{\mathrm{Zn} - \text {Pep}} = \Delta H _{\mathrm{Zn} - \text {Pep}} - T \Delta S _{\mathrm{Zn} - \text {Pep}} = - 8.81 \mathrm{kcal/mol} = 36.8 \mathrm{kJ/mol} (2 \text {分})
\Delta G = - R T \ln K \rightarrow K = \exp (- \Delta G / R T) = 2.85 \times 10^{6} (3 \text {分})
$$

3-4 Hist5 能与 $Zn^{2+}$ 以 1:2 结合（2 分），且高温下该反应比 1:1 结合更有利（2 分）。

或答高温下 Hist5 与 $Zn^{2+}$ 会由 1:1 反应变为 1:2 反应。

第4题（15分，占 $8\%$ ）不同晶型的卤化物

4-1 卤化物 MX 某一晶型为氯化铯结构，最近的 M-X 距离为 3.339 Å，理论密度 D = 6.806 g·cm $^{-3}$ 。计算给出 M 和 X 的元素名称。

$$
4 - 1 a = 2 d / 3^{1 / 2} = 3.856 \mathrm{A} (1 \text {分})
M = D N _{\mathrm{A}} a ^{3} / Z = 234.8 \mathrm{g} \cdot \mathrm{mol} ^{- 1} (1 \text {分})
$$

计算得 M 为银，X 为碘（2 分）

4-2 该卤化物还有另一晶型属四方晶系，M 的堆积以简单立方堆积为基础，去掉一半的层，所有 M 均位于 X 构成的四面体空隙中。假设 X 形成的均为正四面体，不考虑空隙和填隙四面体大小区别，取 M 位于 $(0, 0, 0)$ ，X 位于 $(0.5, 0, 0.25)$ 的正当晶胞，写出该晶胞中其他所有原子的坐标，需指明为哪种原子。

4-2 M (0.5, 0.5, 0) (1 分), X (0, 0.5, 0.75) (1 分)

![](images/43655a95cabf5eeb8c1a54c566672ef23fb890b9f538bc476c57a881875b72f8.jpg)

4-3 在上述四方晶型卤化物基础上能衍生出一种快离子导体：有序移除一半的 M 原子，向两层 M 间的空层间填入数量为现在 M 一半的 N。已知 M 的质量分数为 23.35%，计算给出 N 的元素名称，写出该导体的化学式。

4-3 由题意导体组成为 $\mathbf{M}_2\mathbf{N}\mathbf{X}_4$ (1分)，代入质量分数求得 $M(\mathbf{N}) = 207.4\mathrm{g}\cdot \mathrm{mol}^{-1}$ (1分) $\mathbf{N}$ 为汞，导体化学式为 $\mathrm{Ag_2HgI_4}$ 。(2分)

4-4 该导体正当晶胞的 c 轴投影图不存在重叠的异种原子。假设 X 形成的均为正四面体，不考虑空隙和填隙四面体大小区别，取 N 位于 $(0, 0, 0)$ ，X 位于 $(0.25, 0.25, 0.25)$ 的正当晶胞，写出该晶胞中其他所有原子的坐标，需指明为哪种原子。

4-4 M (0.5, 0, 0.5), (0, 0.5, 0.5), X (0.75, 0.75, 0.25), (0.25, 0.75, 0.75), (0.75, 0.25, 0.75) (5 分)

![](images/9dcc878a8734d26954e104dba6df2aa724f62d5c85c3aa9e98c985c6da8398c3.jpg)

## 知识点映射

- （待人工校准）
