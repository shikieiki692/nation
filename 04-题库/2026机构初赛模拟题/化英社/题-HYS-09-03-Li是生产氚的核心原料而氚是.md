---
title: "题-HYS-09-03-Li是生产氚的核心原料而氚是"
aliases: ["题-HYS-09-03"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "化英社 第40届化英社化学奥林匹克初赛夏季初赛模拟9 第 3 题"
module: "2026机构初赛模拟题"
source_subject: 结构化学
syllabus_codes: [11, 12, 56]
knowledge_points:
  - "[[冠醚]]"
  - "[[同位素效应]]"
  - "[[氢键]]"
  - "[[Boltzmann统计初步]]"
tags: [化竞, 题目, 初赛, 机构模拟题, 化英社]
updated: 2026-09-26
status: 已填充
exam_stage: 初赛
subject_module: 结构化学
pack: 综合模拟卷
submodule: 化英社
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_tier: 2
source_norm: "化英社-第40届化英社化学奥林匹克初赛夏季初赛模拟9"
source_file: "2026机构初赛模拟题/07-化英社/第40届化英社化学奥林匹克初赛夏季初赛模拟9.md"
mixed_content: true   # 正文含相邻题段落（拆卡越界），勿整卡组卷
---

# 题-HYS-09-03-Li是生产氚的核心原料而氚是

## 题目

### 第 3 题锂同位素分离（14分，占 $10\%$ ）

$^{6}$ Li 是生产氚的核心原料，而氚是核聚变的关键燃料。该应用通常要求 $^{6}$ Li 的丰度超过 30%，在特定条件下甚至需要富集到 90%。 $^{7}$ Li 可用作钍基熔盐堆中的冷却剂以及核电站压水反应堆中的 pH 调节剂，其纯度通常要求不低于 99.9%，理想情况下需高于 99.99%。然而，天然锂的同位素丰度约为 7.52% $^{6}$ Li 和 92.48% $^{7}$ Li，远不能满足上述核级应用要求。由于二者的化学性质几乎完全相同，锂同位素分离成为一项需求迫切且极具挑战性的关键技术。

3-1 目前，锂汞齐法仍是唯一工业化的锂同位素分离工艺。该法基于如下交换反应：

$$
{ } ^ { 6 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) + { } ^ { 7 } \mathrm{Li} ( \mathrm{Hg} ) \rightleftharpoons { } ^ { 7 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) + { } ^ { 6 } \mathrm{Li} ( \mathrm{Hg} ) , \quad \alpha = \frac { [ { } ^ { 7 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) ] _ { \mathrm{c} } [ { } ^ { 6 } \mathrm{Li} ( \mathrm{Hg} ) ] _ { \mathrm{c} } } { [ { } ^ { 6 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) ] _ { \mathrm{c} } [ { } ^ { 7 } \mathrm{Li} ( \mathrm{Hg} ) ] _ { \mathrm{c} } } = 1.05
$$

以锂汞齐-氢氧化锂水溶液体系为例，锂同位素分离流程如图。锂汞齐和氢氧化锂水溶液在交换段（exchange section）通过连续的逆向流动和接触交换，使锂同位素丰度呈梯度分布。交换段两端设置上、下回流器（up/bottom refluxor）。在上回流器中，锂由溶液相经电解转入汞齐相；在下回流器中，锂由汞齐相经水解转入溶液相。天然丰度的氢氧化锂溶液作为馈料在交换段的相应丰度处加入，产品则在所需丰度处取出。

3-1-1 用于钍基熔盐堆冷却剂的锂同位素富集产品应在贫化端（dilution section）还是富集端（enrichment section）取得？

![](images/83686b70d9983104371fc843c741831236e2251eeeda92353450f4617ed00709.jpg)

3-1-2（思考题，不计入总分）为进一步理解该锂同位素分离流程，考虑如下简化模型：

系统中共有 $(2N+2)$ 个容器，分别记为 $u_{1} \sim u_{N}$ 、 $v_{1} \sim v_{N}$ 以及 DS 和 ES。其中，u 类容器盛装锂汞齐，v 类容器盛装氢氧化锂水溶液，且每个容器（无论盛装的是锂汞齐还是氢氧化锂水溶液）中总锂的物质的量均总是相等。按如下顺序进行操作：(1)使 $u_{i}$ 与 $v_{i}$ ( $i=1 \sim N$ ) 中的两相充分接触直至同位素交换平衡；(2)通过电解使 DS 中的氢氧化锂水溶液全部转化为锂汞齐，通过水解使 ES 中的锂汞齐全部转化为氢氧化锂水溶液；(3)平行地，将 DS 中的锂汞齐全部转移至 $u_{1}$ ，将 $u_{i}$ ( $i=1 \sim N-1$ ) 中的锂汞齐全部转移至 $u_{i+1}$ ，将 $u_{N}$ 中的锂汞齐全部转移至 ES，将 ES 中的氢氧化锂水溶液全部转移至 $v_{N}$ ，将 $v_{i}$ ( $i=2 \sim N$ ) 中的氢氧化锂水溶液全部转移至 $v_{i-1}$ ，以及将 $v_{1}$ 中的氢氧化锂水溶液全部转移至 DS。轮流进行以上操作，直至 DS 和 ES 中的锂同位素丰度不再随操作变化，此时锂同位素丰度依容器呈稳定梯度分布。

若要求此时 DS 和 ES 处分别富集的锂同位素的丰度均至少达到 99.9%, 求 N 的最小值。

3-1-3（思考题，不计入总分）关于锂汞齐法，下列说法中，哪个（些）是正确的？

(a) 同位素交换反应在两相界面上进行, 速率很快。同时, 该体系容易形成两相对流, 有利于工艺流程设计和级联操作;

(b) 锂汞齐-氢氧化锂水溶液体系可能因副反应生成氢气而导致不稳定。为克服这一问题，可在汞齐相中施加恒定电流，使锂离子重新回到汞齐中，以保持汞齐中锂的浓度恒定；

(c) 该体系的单级分离系数受多种因素影响, 包括但不限于阴离子、溶剂、温度和溶液浓度; 单级分离系数相同时, 理论上交换段越长, 富集端与贫化端的富集程度越高。

3-2 为克服汞基分离法的缺点, 人们开发了一系列替代性锂同位素分离技术, 其中溶剂萃取法备受关注。该法基于如下交换反应:

$$
{ } ^ { 6 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) + \mathrm{CE} \cdot { } ^ { 7 } \mathrm{Li} ^ { + } ( \mathrm{org.} ) \rightleftharpoons { } ^ { 7 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) + \mathrm{CE} \cdot { } ^ { 6 } \mathrm{Li} ^ { + } ( \mathrm{org.} )
$$

其中 CE 表示冠醚，本题以苯并-15-冠-5（B15C5）进行讨论。

尽管冠醚基体系已取得显著进展, 但如何合理设计和优化萃取体系仍是一大挑战。研究表明, 阴离子在该锂同位素分离过程中发挥着关键调控作用。当阴离子种类不同时, 分离因子 $\alpha$ 遵循如下顺序: $\mathrm{NTf}_{2}^{-} > \mathrm{ClO}_{4}^{-} > \Gamma^{-} > \mathrm{Br}^{-} > \mathrm{Cl}^{-}$ 。为揭示其微观机制, 有研究团队借助量子化学计算, 系统解析了阴离子对 $\mathrm{Li^{+}-B15C5}$ 的结构、分子振动特征以及配位环境的调控规律。3-2-1 计算研究表明, 阴离子的种类会影响 $\mathrm{Li^{+}-B15C5}$ 的结构——当阴离子为 $\mathrm{ClO}_{4}^{-}$ 时, $\mathrm{Li^{+}-B15C5}$ 中的锂离子被 $\mathrm{ClO}_{4}^{-}$ 直接配位; 而当阴离子为 $\mathrm{Cl}^{-}$ 时, $\mathrm{Li^{+}-B15C5}$ 中的锂离子则被水分子配位, $\mathrm{Cl}^{-}$ 通过某种分子间作用力与水分子结合。写出该分子间作用力。

3-2-2 上述交换反应的分离因子（即平衡常数）可通过统计热力学公式计算：

$$
\alpha = \frac {Q _ {7 \mathrm{Li} ^ {+} (\mathrm{nq.})} Q _ {\mathrm{CE} \cdot 6 \mathrm{Li} ^ {+} (\mathrm{org.})}}{Q _ {6 \mathrm{Li} ^ {+} (\mathrm{nq.})} Q _ {\mathrm{CE} \cdot 7 \mathrm{Li} ^ {+} (\mathrm{org.})}}
$$

其中 $Q$ 为总配分函数, 可分解为平动、转动、振动、电子和核自旋配分函数的乘积:

$$
Q = Q _ {\text { trans }} \cdot Q _ {\text { rot }} \cdot Q _ {\text { vib }} \cdot Q _ {\text { elec }} \cdot Q _ {\text { nuc }}
$$

对于同位素交换反应，振动配分函数 $Q_{\mathrm{vib}}$ 对分离因子的贡献最大，其它配分函数的同位素差异则非常微小。

3-2-2-1 谐振子近似下，分子中单个振动模式的振动能级为：

$$
E _ {n} = (n + \frac {1}{2}) l n v _ {i}, n = 0, 1, 2, \dots
$$

其中 $n$ 为振动量子数, $\nu_{i}$ 为该振动模式的振动频率 (与原子质量有关), 各能级简并度均为 1 。直接给出单个振动模式的振动配分函数 $Q_{\mathrm{vib}, i}$ , 要求最终表达式不包含量子数 $n$ 。 3-2-2-2 非线性多原子分子共有(3N-6)个振动模式, 其中 $N$ 为原子数, 故振动配分函数:

$$
Q _ {\mathrm{vib}} = \prod_ {i = 1} ^ {3 N - 6} Q _ {\mathrm{vib}, i}
$$

依据 Urey 模型，考虑同位素质量差异对振动频率的影响，定义约化配分函数比：

$$
\beta_ {6 _ {\mathrm{Li}} / 7 _ {\mathrm{Li}}} = \prod_ {i = 1} ^ {3 N - 6} \frac {\nu_ {6 _ {\mathrm{Li}} , i} Q _ {6 _ {\mathrm{Livib}} , i} ^ {i}}{\nu_ {7 _ {\mathrm{Li}} , i} Q _ {7 _ {\mathrm{Livib}} , i} ^ {i}}
$$

则上述交换反应的分离因子可由约化配分函数比近似计算:

$$
\alpha = \frac {\beta_ {6 _ {\mathrm{Li} / ^ {7} \mathrm{Li}}} (\mathrm{CE} : \mathrm{Li} ^ {+} (\text { org. }))}{\beta_ {6 _ {\mathrm{Li} / ^ {7} \mathrm{Li}}} (\mathrm{Li} ^ {+} (\text { aq. }))}
$$

实际上, 并非所有振动模式都对同位素分离有显著贡献。若仅考虑其中有显著贡献的共 $k$ 种振动模式, 则约化配分函数比可写为:

$$
\beta_ {6 _ {\mathrm{Li}} / ^ {7} \mathrm{Li}} = \prod_ {i = 1} ^ {k} \frac {\nu_ {6 _ {\mathrm{Li}} , i} ^ {6} Q _ {6 _ {\mathrm{Livib}} , i} ^ {6}}{\nu_ {7 _ {\mathrm{Li}} , i} ^ {7} Q _ {7 _ {\mathrm{Livib}} , i} ^ {7}}
$$

此时，上述交换反应的分离因子仍可由约化配分函数比依相同公式近似计算。

研究人员计算得到了 $298 \mathrm{~K}$ 下 $\mathrm{Li}^{+}(\mathrm{aq.})$ 和 $\mathrm{Li}^{+}-\mathrm{B}15 \mathrm{C} 5(\mathrm{org.})$ 在不同锂同位素下部分关键振动模式的波数, 其中阴离子为 $\mathrm{Cl}^{-}$ 时的结果如下表所示:

<table><tr><td>物种</td><td>振动模式</td><td> $\tilde{v}_{6\text{Li}}(\text{cm}^{-1})$ </td><td> $\tilde{v}_{7\text{Li}}(\text{cm}^{-1})$ </td></tr><tr><td rowspan="4"> $Li^{+}(aq.)$ </td><td>m1</td><td>407.0859</td><td>392.9023</td></tr><tr><td>m2</td><td>491.1423</td><td>477.5436</td></tr><tr><td>m3</td><td>470.1306</td><td>462.5832</td></tr><tr><td>m4</td><td>460.0323</td><td>452.9261</td></tr><tr><td rowspan="7"> $Li^{+}-B15C5(org.)$ </td><td>m1</td><td>502.6982</td><td>478.3300</td></tr><tr><td>m2</td><td>291.3250</td><td>282.6461</td></tr><tr><td>m3</td><td>228.3667</td><td>221.6920</td></tr><tr><td>m4</td><td>243.7586</td><td>239.7021</td></tr><tr><td>m5</td><td>526.3759</td><td>522.5399</td></tr><tr><td>m6</td><td>229.4120</td><td>225.9596</td></tr><tr><td>m7</td><td>251.8142</td><td>248.5153</td></tr></table>

根据以上数据，近似计算 $298 \mathrm{~K}$ 下阴离子为 $\mathrm{Cl}^{-}$ 时交换反应的分离因子，保留 4 位有效数字。

3-2-3 事实上，上一问（3-2-2-2）中由于选取的振动模式过少，近似计算结果与真实值存在显著偏差。研究人员通过计算软件对所有振动模式进行了完整计算，结果如下：

![](images/355a97dc279c7298f3ec0803ea6251da57774a14a55e391bb82a64723baeea5a.jpg)

![](images/1f6706afaa72f111e3f8b0229d8ede2dc43ada0f452d3aeb86751457f5161630.jpg)

![](images/385776c7cfa5bf12a166b7403d0fafdb3a0fb2ad7d930d5b7bf717fea935d933.jpg)

![](images/96e6e28fbd3dd36a86561bdb43dd44caafa754f453a9d3a7905c8824a2dbd4a7.jpg)

4-2-2-1 写出 D 的化学式。
4-2-2-2 晶体 D 属四方晶系，结构基元为 16 个化学式。
4-2-2-2-1 写出 D 的点阵形式。
4-2-2-2-2 写出 D 的特征对称元素。
4-3 M 的氮化物结构亦十分有趣。

![](images/3100984c6e5bb7716e908caf9c19756f318a81e160360f652d64cf9a19006486.jpg)

![](images/2b2df5d6766d38533cf9e648405bd11508a7dd01145e9bde1f6277e1da5ec5e6.jpg)

图(2-c)
![](images/b71b74b5b83be0f3e6e1f6646bcbd432b1d690950786c503e0bd77afc83ad420.jpg)
图(2-a)
4-3-1 图(1)是 M 的某种立方晶系氮化物 E 的晶胞沿 c 轴投影图。提示：其晶体结构与某种含铁矿物相似。
4-3-1-1 写出 E 的化学式和点阵形式。

(4-3-1-2)晶体 $\mathbf{E}$ 中, $\mathbf{M}$ 均为 6 配位, 且 $\mathbf{M}-\mathbf{N}$ 键长 (最短 $\mathbf{M}-\mathbf{N}$ 距离) 均为 $2.104 \mathrm{~A}$ , 次短 $\mathbf{M}-\mathbf{N}$ 距离为 $3.164 \mathrm{~Å}$ 。据此, 计算晶体 $\mathbf{E}$ 的密度。

![](images/95c95ee0f955bd7464b7d3ceb5811ed0605c173f71164a7214009c5c07d84bc8.jpg)

4-2-2-1 写出 D 的化学式。
4-2-2-2 晶体 D 属四方晶系，结构基元为 16 个化学式。
4-2-2-2-1 写出 D 的点阵形式。
4-2-2-2-2 写出 D 的特征对称元素。
4-3 M 的氮化物结构亦十分有趣。

图(2-a)

4-3-1 图(1)是 M 的某种立方晶系氮化物 E 的晶胞沿 c 轴投影图。提示：其晶体结构与某种含铁矿物相似。

4-3-1-1 写出 E 的化学式和点阵形式。

4-3-1-2 晶体 E 中，M 均为 6 配位，且 M-N 键长（最短 M-N 距离）均为 2.104 Å，次短 M-N 距离为 3.164 Å。据此，计算晶体 E 的密度。

4-3-2 图(2-c)和图(2-a)分别为 M 的某种正交晶系氮化物 F 的晶胞沿 c 轴和 a 轴的投影图。在晶体 F 中，所有的 M 形成同一种配位多面体，但该配位多面体在晶体中有不同的取向。
4-3-2-1 写出 F 中 M 的配位多面体。

4- 3- 2- 2 (思考题, 不计入总分) 分别写出晶体 $\mathbf{F}$ 中, $\mathbf{M}$ 有几种化学环境、几种空间环境。 4- 3- 2- 3 (思考题, 不计入总分) 写出 $\mathbf{F}$ 的化学式。

4-4 下图为 M 的某氮氧化物 G 的晶体结构。晶体 G 属单斜晶系， $\alpha=\gamma=90^{\circ}$ ， $\beta=99.56^{\circ}$ 。

![](images/abe8211fbc6d2f8b24eab22827e2d88a070225ef1dcb072e39788eff2d890d35.jpg)

4倍→4次
3黑→3配

$$
T a N O
$$

4-4-1 写出 $\mathbf{G}$ 的化学式。

4-4-2 写出晶体 $\mathbf{G}$ 中, $\mathbf{M}$ 有几种化学环境、几种空间环境。

## 参考答案

$^{6}$ Li 是生产氚的核心原料，而氚是核聚变的关键燃料。该应用通常要求 $^{6}$ Li 的丰度超过 30%，在特定条件下甚至需要富集到 90%。 $^{7}$ Li 可用作钍基熔盐堆中的冷却剂以及核电站压水反应堆中的 pH 调节剂，其纯度通常要求不低于 99.9%，理想情况下需高于 99.99%。然而，天然锂的同位素丰度约为 7.52% $^{6}$ Li 和 92.48% $^{7}$ Li，远不能满足上述核级应用要求。由于二者的化学性质几乎完全相同，锂同位素分离成为一项需求迫切且极具挑战性的关键技术。

3-1 目前，锂汞齐法仍是唯一工业化的锂同位素分离工艺。该法基于如下交换反应：

$$
{ } ^ { 6 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) + { } ^ { 7 } \mathrm{Li} ( \mathrm{Hg} ) \rightleftharpoons { } ^ { 7 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) + { } ^ { 6 } \mathrm{Li} ( \mathrm{Hg} ) \quad \alpha = \frac { [ { } ^ { 7 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) ] _ { \mathrm{c} } [ { } ^ { 6 } \mathrm{Li} ( \mathrm{Hg} ) ] _ { \mathrm{c} } } { [ { } ^ { 6 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) ] _ { \mathrm{c} } [ { } ^ { 7 } \mathrm{Li} ( \mathrm{Hg} ) ] _ { \mathrm{c} } } = 1.05
$$

以锂汞齐-氢氧化锂水溶液体系为例，锂同位素分离流程如图。锂汞齐和氢氧化锂水溶液在交换段（exchange section）通过连续的逆向流动和接触交换，使锂同位素丰度呈梯度分布。交换段两端设置上、下回流器（up/bottom refluxor）。在上回流器中，锂由溶液相经电解转入汞齐相；在下回流器中，锂由汞齐相经水解转入溶液相。天然丰度的氢氧化锂溶液作为馈料在交换段的相应丰度处加入，产品则在所需丰度处取出。

## 3-1-1 用于钛基熔盐堆冷却剂的锂同位素富集产品应在贫化端（dilution section）还是富集端（enrichment section）取得？

贫化端（2分）

![](images/8e2779d01d512f1a92ff16e234a781c07e12266f24c9280f904ad7567ca383c5.jpg)

3-1-2（思考题，不计入总分）为进一步理解该锂同位素分离流程，考虑如下简化模型：

系统中共有(2N+2)个容器, 分别记为 $\mathbf{u}_{1} \sim \mathbf{u}_{N}$ 、 $\mathbf{v}_{1} \sim \mathbf{v}_{N}$ 以及 DS 和 ES。其中, u 类容器盛装锂汞齐, v 类容器盛装氢氧化锂水溶液, 且每个容器 (无论盛装的是锂汞齐还是氢氧化锂水溶液) 中总锂的物质的量均总是相等。按如下顺序进行操作: (1)使 $\mathbf{u}_{i}$ 与 $\mathbf{v}_{i}$ ( $i=1 \sim N$ ) 中的两相充分接触直至同位素交换平衡; (2)通过电解使 DS 中的氢氧化锂水溶液全部转化为锂汞齐, 通过水解使 ES 中的锂汞齐全部转化为氢氧化锂水溶液; (3)平行地, 将 DS 中的锂汞齐全部转移至 $\mathbf{u}_{1}$ , 将 $\mathbf{u}_{i}$ ( $i=1 \sim N-1$ ) 中的锂汞齐全部转移至 $\mathbf{u}_{i+1}$ , 将 $\mathbf{u}_{N}$ 中的锂汞齐全部转移至 ES, 将 ES 中的氢氧化锂水溶液全部转移至 $\mathbf{v}_{N}$ , 将 $\mathbf{v}_{i}$ ( $i=2 \sim N$ ) 中的氢氧化锂水溶液全部转移至 $\mathbf{v}_{i-1}$ , 以及将 $\mathbf{v}_{1}$ 中的氢氧化锂水溶液全部转移至 DS。轮流进行以上操作, 直至 DS 和 ES 中的锂同位素丰度不再随操作变化, 此时锂同位素丰度依容器呈稳定梯度分布。

若要求此时DS和ES处分别富集的锂同位素的丰度均至少达到 $99.9\%$ ，求 $N$ 的最小值。

设此时容器 $\mathbf{u}_i$ 中 $^6\mathrm{Li}$ 丰度为 $u_{i}$ 容器 $\mathbf{v}_i$ 中 $^6\mathrm{Li}$ 丰度为 $v_{i}$

则容器 DS 中 ${}^{6}$ Li 丰度为 $v_{1}$ ，容器 ES 中 ${}^{6}$ Li 丰度为 $u_{N}$

每一次平衡后，

$$
\frac {u _ {i}}{1 - u _ {i}} / \frac {v _ {i}}{1 - v _ {i}} = \alpha
$$

分析可知，在 $\mathbf{u}_N$ 与 $\mathbf{v}_N$ 两相同位素交换平衡后， $^6\mathrm{Li}$ 丰度分别从 $u_{N-1}$ 和 $u_N$ 变为 $u_N$ 和 $v_N$

由于每个容器中总锂的物质的量均相等，故 $u_{N-1}=v_{N}$

$$
\text { 类似地，可以推得 } u _ {i - 1} = v _ {i} (i = 1 \sim N - 1)
$$

$$
\begin{array}{r l} \text {于是} \alpha^ {N} = & \frac {u _ {N}}{1 - u _ {N}} / \frac {\nu_ {1}}{1 - \nu_ {1}} \geq \frac {0.999}{1 - 0.999} / \frac {0.001}{1 - 0.001} \\ & \text {得} N \geq 283.1 \\ & N \text {的最小值为} 284 \end{array}
$$

3-1-3（思考题，不计入总分）关于锂汞齐法，下列说法中，哪个（些）是正确的？

(a) 同位素交换反应在两相界面上进行, 速率很快。同时, 该体系容易形成两相对流, 有利于工艺流程设计和级联操作;

(b) 锂汞齐-氢氧化锂水溶液体系可能因副反应生成氢气而导致不稳定。为克服这一问题，可在汞齐相中施加恒定电流，使锂离子重新回到汞齐中，以保持汞齐中锂的浓度恒定；

(c) 该体系的单级分离系数受多种因素影响, 包括但不限于阴离子、溶剂、温度和溶液浓度; 单级分离系数相同时, 理论上交换段越长, 富集端与贫化端的富集程度越高。

$$
(a) (b) (c)
$$

3-2 为克服汞基分离法的缺点, 人们开发了一系列替代性锂同位素分离技术, 其中溶剂萃取法备受关注。该法基于如下交换反应:

$$
{ } ^ { 6 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) + \mathrm{CE} \cdot { } ^ { 7 } \mathrm{Li} ^ { + } ( \mathrm{org.} ) \rightleftharpoons { } ^ { 7 } \mathrm{Li} ^ { + } ( \mathrm{aq.} ) + \mathrm{CE} \cdot { } ^ { 6 } \mathrm{Li} ^ { + } ( \mathrm{org.} )
$$

其中 CE 表示冠醚，本题以苯并-15-冠-5（B15C5）进行讨论。

尽管冠醚基体系已取得显著进展, 但如何合理设计和优化萃取体系仍是一大挑战。研究表明, 阴离子在该锂同位素分离过程中发挥着关键调控作用。当阴离子种类不同时, 分离因子 $\alpha$ 遵循如下顺序: $\mathrm{NTf}_{2}^{-} > \mathrm{ClO}_{4}^{-} > \Gamma^{-} > \mathrm{Br}^{-} > \mathrm{Cl}^{-}$ 。为揭示其微观机制, 有研究团队借助量子化学计算, 系统解析了阴离子对 $\mathrm{Li^{+}-B15C5}$ 的结构、分子振动特征以及配位环境的调控规律。3-2-1 计算研究表明, 阴离子的种类会影响 $\mathrm{Li^{+}-B15C5}$ 的结构——当阴离子为 $\mathrm{ClO}_{4}^{-}$ 时, $\mathrm{Li^{+}-B15C5}$ 中的锂离子被 $\mathrm{ClO}_{4}^{-}$ 直接配位; 而当阴离子为 $\mathrm{Cl}^{-}$ 时, $\mathrm{Li^{+}-B15C5}$ 中的锂离子则被水分子配位, $\mathrm{Cl}^{-}$ 通过某种分子间作用力与水分子结合。写出该分子间作用力。

3-2-2 上述交换反应的分离因子（即平衡常数）可通过统计热力学公式计算：

$$
\alpha = \frac {Q _ {\mathrm{Li} ^ {+} (\mathrm{nq.})} Q _ {\mathrm{CE} \cdot^ {6} \mathrm{Li} ^ {+} (\mathrm{org.})}}{Q _ {\mathrm{Li} ^ {+} (\mathrm{nq.})} Q _ {\mathrm{CE} \cdot^ {7} \mathrm{Li} ^ {+} (\mathrm{org.})}}
$$

其中 $Q$ 为总配分函数, 可分解为平动、转动、振动、电子和核自旋配分函数的乘积:

$$
Q = Q _ {\text { trans }} \cdot Q _ {\text { rot }} \cdot Q _ {\text { vib }} \cdot Q _ {\text { clec }} \cdot Q _ {\text { nuc }}
$$

对于同位素交换反应, 振动配分函数 $Q_{\mathrm{vib}}$ 对分离因子的贡献最大, 其它配分函数的同位素差异则非常微小。

3-2-2-1 谐振子近似下，分子中单个振动模式的振动能级为：

$$
E _ {n} = (n + \frac {1}{2}) l n v _ {i}, \quad n = 0, 1, 2, \dots
$$

其中 n 为振动量子数， $v_{i}$ 为该振动模式的振动频率（与原子质量有关），各能级简并度均为 1。直接给出单个振动模式的振动配分函数 $Q_{vib,i}$ ，要求最终表达式不包含量子数 n。

$$
Q _ {\text { vib }, i} = \sum_ {n = 0} e ^ {- \frac {E _ {n}}{k _ {\mathrm{B}} T}} = \sum_ {n = 0} e ^ {- \frac {(n + \frac {1}{2}) l n _ {i}}{k _ {\mathrm{B}} T}} = e ^ {- \frac {l n _ {i}}{2 k _ {\mathrm{B}} T}} \sum_ {n = 0} (e ^ {- \frac {l n _ {i}}{k _ {\mathrm{B}} T}}) ^ {n} = \frac {e ^ {- \frac {l n _ {i}}{2 k _ {\mathrm{B}} T}}}{1 - e ^ {- \frac {l n _ {i}}{k _ {\mathrm{B}} T}}} (= \frac {e ^ {\frac {l n _ {i}}{2 k _ {\mathrm{B}} T}}}{e ^ {\frac {l n _ {i}}{k _ {\mathrm{B}} T}} - 1}) \quad (3 \text { 分 })
$$

3-2-2-2 非线性多原子分子共有(3N-6)个振动模式，其中 N 为原子数，故振动配分函数

$$
Q _ {\mathrm{vib}} = \prod_ {i = 1} ^ {3 N - 6} Q _ {\mathrm{vib}, i}
$$

依据 Urey 模型，考虑同位素质量差异对振动频率的影响，定义约化配分函数比：

$$
\beta_ {6 \mathrm{Li} 7 \mathrm{Li}} = \prod_ {i = 1} ^ {3 N - 6} \frac {v _ {6 \mathrm{Li} i} Q _ {6 \mathrm{Livib} , i}}{v _ {7 \mathrm{Li} i} Q _ {7 \mathrm{Livib} , i}}
$$

则上述交换反应的分离因子可由约化配分函数比近似计算：

$$
\alpha = \frac {\beta_ {6 _ {\mathrm{Li} ^ {7} \mathrm{Li}}} (\mathrm{CE} \cdot \mathrm{Li} ^ {+} (\mathrm{org.}))}{\beta_ {6 _ {\mathrm{Li} ^ {7} \mathrm{Li}}} (\mathrm{Li} ^ {+} (\mathrm{aq.}))}
$$

实际上, 并非所有振动模式都对同位素分离有显著贡献。若仅考虑其中有显著贡献的共 $k$ 种振动模式, 则约化配分函数比可写为:

$$
\beta_ {6 _ {\mathrm{Li}} / ^ {7} \mathrm{Li}} = \prod_ {i = 1} ^ {k} \frac {v _ {6 _ {\mathrm{Li}} , i} Q _ {6 _ {\mathrm{Li}} \mathrm{vib.} i}}{v _ {7 _ {\mathrm{Li}} , i} Q _ {7 _ {\mathrm{Li}} \mathrm{vib.} i}}
$$

此时，上述交换反应的分离因子仍可由约化配分函数比依相同公式近似计算。

研究人员计算得到了 $298 \mathrm{~K}$ 下 $\mathrm{Li}^{+}(\mathrm{aq.})$ 和 $\mathrm{Li}^{+}-\mathrm{B} 15 \mathrm{C} 5(\mathrm{org.})$ 在不同锂同位素下部分关键振动模式的波数, 其中阴离子为 $\mathrm{Cl}^{-}$ 时的结果如下表所示:

<table><tr><td>物种</td><td>振动模式</td><td> $\tilde{v}_{\sigma_{Li}}(cm^{-1})$ </td><td> $\tilde{v}_{7Li}(cm^{-1})$ </td></tr><tr><td rowspan="4"> $Li^{+}(aq.)$ </td><td>m1</td><td>407.0859</td><td>392.9023</td></tr><tr><td>m2</td><td>491.1423</td><td>477.5436</td></tr><tr><td>m3</td><td>470.1306</td><td>462.5832</td></tr><tr><td>m4</td><td>460.0323</td><td>452.9261</td></tr><tr><td rowspan="7"> $Li^{+}-B15C5(org.)$ </td><td>m1</td><td>502.6982</td><td>478.3300</td></tr><tr><td>m2</td><td>291.3250</td><td>282.6461</td></tr><tr><td>m3</td><td>228.3667</td><td>221.6920</td></tr><tr><td>m4</td><td>243.7586</td><td>239.7021</td></tr><tr><td>m5</td><td>526.3759</td><td>522.5399</td></tr><tr><td>m6</td><td>229.4120</td><td>225.9596</td></tr><tr><td>m7</td><td>251.8142</td><td>248.5153</td></tr></table>

根据以上数据，近似计算 $298 \mathrm{~K}$ 下阴离子为 $\mathrm{Cl^-}$ 时交换反应的分离因子，保留 4 位有效数字。

$$
\begin{array}{r l} & {\beta_ {6 _ {\mathrm{Li}} / ^ {7} \mathrm{Li}} (^ {6} \mathrm{Li} ^ {+} (\mathrm{aq.})) = \prod_ {i = 1} ^ {4} \frac {\nu_ {6 _ {\mathrm{Li}} ^ {+} (\mathrm{nq.}) , i} Q _ {6 _ {\mathrm{Li}} ^ {+} (\mathrm{nq.}) \mathrm{vib} , i}}{\nu_ {7 _ {\mathrm{Li}} ^ {+} (\mathrm{nq.}) , i} Q _ {7 _ {\mathrm{Li}} ^ {+} (\mathrm{nq.}) \mathrm{vib} , i}} = 0.9663 (2 \text {分})} \\ & {\beta_ {6 _ {\mathrm{Li}} / ^ {7} \mathrm{Li}} (\mathrm{CE} \cdot \mathrm{Li} ^ {+} (\mathrm{org.})) = \prod_ {i = 1} ^ {7} \frac {\nu_ {\mathrm{CE} \cdot^ {6} \mathrm{Li} ^ {+} (\mathrm{org.}) , i} Q _ {\mathrm{CE} \cdot^ {6} \mathrm{Li} ^ {+} (\mathrm{org.}) \mathrm{vib} , i}}{\nu_ {\mathrm{CE} \cdot^ {7} \mathrm{Li} ^ {+} (\mathrm{org.}) , i} Q _ {\mathrm{CE} \cdot^ {7} \mathrm{Li} ^ {+} (\mathrm{org.}) \mathrm{vib} , i}} = 0.9634 (2 \text {分})} \\ & {\alpha = \frac {\beta_ {6 _ {\mathrm{Li}} / ^ {7} \mathrm{Li}} (\mathrm{CE} \cdot \mathrm{Li} ^ {-} (\mathrm{org.}))}{\beta_ {6 _ {\mathrm{Li}} / ^ {7} \mathrm{Li}} (\mathrm{Li} ^ {+} (\mathrm{aq.}))} = 0.9970 (1 \text {分})} \\ & {\quad (\text {共5分})} \end{array}
$$

3-2-3 事实上, 上一问 (3-2-2-2) 中由于选取的振动模式过少, 近似计算结果与真实值存在显著偏差。研究人员通过计算软件对所有振动模式进行了完整计算, 结果如下:

<table><tr><td>阴离子</td><td> $\beta_{6\text{Li}/7\text{Li}}(\text{CE}\cdot\text{Li}^{+}(\text{org.}))$ </td><td> $\beta_{6\text{Li}/7\text{Li}}(^{6}\text{Li}^{+}(\text{aq.}))$ </td><td>α计算值</td></tr><tr><td> $\text{Cl}^{-}$ </td><td>0.9530</td><td>0.9218</td><td>1.034</td></tr><tr><td> $\text{Br}^{-}$ </td><td>0.9533</td><td>0.9223</td><td>1.034</td></tr><tr><td> $\Gamma^{-}$ </td><td>0.9567</td><td>0.9224</td><td>1.037</td></tr><tr><td> $\text{BF}_{4}^{-}$ </td><td>0.9609</td><td>0.9227</td><td>1.041</td></tr><tr><td> $\text{ClO}_{4}^{-}$ </td><td>0.9619</td><td>0.9222</td><td>1.043</td></tr><tr><td> $\text{NTf}_{2}^{-}$ </td><td>0.9621</td><td>0.9232</td><td>1.042</td></tr></table>

研究人员对比了计算结果与真实值，如下左图所示。此外，他们还测量了不同阴离子体系下各结构的 $^{7}\mathrm{Li}$ NMR，如下右边图所示。

![](images/dcc5656477db3fd4196692aa3bf6c91f9420f8d4ac2d0fbeb4c0a494d9cdb328.jpg)

![](images/e52b8aa3a5bb59393746add01bcb2d1e41488d6e8a2f98787de9ff9f42e4c98f.jpg)
根据以上信息判断，下列说法中，哪个（些）是正确的。

(a) 分离因子的大小顺序 (NTf $_{2}^{-}$ >ClO $_{4}^{-}$ >Γ $^{-}$ >Br $^{-}$ >Cl $^{-}$ ) 与 Hofmeister 序列（阴离子盐析能力从大到小的顺序）一致，这表明阴离子种类影响分离因子的微观机制很可能涉及阴离子与水分子的相互作用。

(b) 小体积、电荷集中的阴离子会诱导竞争性水合, 并通过强的水介导相互作用破坏冠醚与锂离子的配位稳定性; 相反, 大体积、电荷分散的阴离子能有效剥离锂离子的水合层, 促进形成更对称的冠醚配位结构, 从而显著提高锂同位素分离性能。

(c) 由图可知, Urey 模型预测的分离因子存在较显著的高估, 这可能是由于静态团簇模型在处理动态溶剂方面的普遍局限性。尽管数值上存在偏移, 基于 Urey 模型的理论计算仍成功再现了不同阴离子体系中分离因子的大致变化趋势。

(d) 以上说法均错误。

(a)(b)(c)（3分，每个1分）

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**（OCR 原文逐字转录，可能保留原卷笔误）。