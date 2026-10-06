---
title: "题-2ChO-04-04-表面活性剂分子surfact"
aliases: ["题-2ChO-04-04"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "2ChO 第4届2ChO化学奥林匹克联考 第 4 题"
module: "2026机构初赛模拟题"
source_subject: 化学原理
syllabus_codes: [3, 57]
knowledge_points:
  - "[[临界胶束浓度]]"
  - "[[胶束]]"
  - "[[化学动力学]]"
  - "[[活化能]]"
tags: [化竞, 题目, 初赛, 机构模拟题, 2ChO]
updated: 2026-09-26
status: 已填充
exam_stage: 初赛
subject_module: 化学原理
pack: 综合模拟卷
submodule: 2ChO
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_tier: 2
source_norm: "2ChO-第4届2ChO化学奥林匹克联考"
source_file: "2026机构初赛模拟题/11-2ChO/第4届2ChO化学奥林匹克联考试题.md"
---

# 题-2ChO-04-04-表面活性剂分子surfact

## 题目

### 第 4 题 胶束化动力学 (17 分)

表面活性剂分子(surfactant molecule)在环境、制药、石油采集等众多行业中至关重要。在表面活性剂分子超过一定浓度时，能够自发结合，形成具有明确几何形状的胶束，这一浓度被称为临界胶束浓度(critical micelle concentration, CMC)。

研究发现，理论计算得到的长疏水链表面活性剂的 CMC 与实验数据有显著差异。考察其中一种表面活性剂 $Gem_{n}EO_{m}$ (分子式表示为 $\mathrm{H}(\mathrm{CH}_{2})_{n-2}\mathrm{CHCH}_{2}\mathrm{O}(\mathrm{CH}_{2}\mathrm{CH}_{2}\mathrm{O})_{m}\mathrm{H})_{2}(\mathrm{CH}_{2})_{6}$ )，发现当疏水尾链碳原子数 $n \geq 12$ 时，理论算得的平衡 $\mathrm{CMC}(\mathrm{CMC}_{\mathrm{eq}})$ 极低，但实验测得到达表观平衡时的胶束浓度 $(\mathrm{CMC}_{\mathrm{app}})$ 显著偏高。

![](images/e7ac1a25f715745d8533621fb3a97c3d2679e2ece17007f3491d25a62dbe4c4b.jpg)
$Gem_{12}EO_{15}$ 在胶束中的可能结构

4-1 与理论胶束形成时间 $T_{s}$ 主要相关时间 $T_{0}$ 由下式给出：

$$
T _ {0} = \frac {6 \pi \eta R _ {\mathrm{h}} ^ {3}}{M _ {\mathrm{eq}} k T}
$$

其中 $\eta$ 、 $R_{h}$ 、k、T 均为常数，聚集数 $M_{eq}$ 与尾链碳原子数 n 为线性关系。在 $25^{\circ}C$ 的水溶液中，有近似关系 $T_{0}=\frac{7.17}{M_{eq}}\times10^{-10}$ 。已知一系列不同 n 下的 $T_{0}$ 如下表所示。通过计算，用 n 表示 $M_{eq}$ （系数均保留至整数）。

<table><tr><td>n</td><td>12</td><td>13</td><td>14</td><td>15</td></tr><tr><td> $T_0(s)$ </td><td> $6.18\times 10^{-12}$ </td><td> $5.69\times 10^{-12}$ </td><td> $5.27\times 10^{-12}$ </td><td> $4.91\times 10^{-12}$ </td></tr></table>

4-2 建立 $T_{0}$ 与理论胶束形成时间 $T_{s}$ 关系如下:

$$
T _ {\mathrm{s}} = T _ {0} e ^ {F _ {\mathrm{a}}}
$$

其中 $F_{a}$ 为理论活化能垒，其经验公式为 $F_{a}=15n-130$ 。请计算 n=16 时胶束形成的理论平衡时间 $T_{s}$ (单位：秒)，并指出其是否可在实验室内观测。

4-3 已知表观临界胶束浓度 $CMC_{app}$ 与平衡 $CMC_{eq}$ 均满足关系式( $F_{a}^{app}$ 为表观活化能垒):

$$
\mathrm{CMC} _ {\text { app }} = k e ^ {- F _ {\mathrm{a}} ^ {\text { app }} / n}, \mathrm{CMC} _ {\text { eq }} = k e ^ {- F _ {\mathrm{a}} / n}
$$

若实验要求针对 $n = 16$ 的表面活性剂，可在 $1\mathrm{h}$ 内观测到胶束化现象，计算该条件下 $\mathrm{CMC_{app} / CMC_{eq}}$ 的值。

4-4 从化学反应原理的角度，解释 n 较大时的长链表面活性剂的表观临界浓度( $CMC_{app}$ )高于平衡 $CMC(CMC_{eq})$ 的原因。

## 参考答案

表面活性剂分子(surfactant molecule)在环境、制药、石油采集等众多行业中至关重要。在表面活性剂分子超过一定浓度时，能够自发结合，形成具有明确几何形状的胶束，这一浓度被称为临界胶束浓度(critical micelle concentration, CMC)。

研究发现，理论计算得到的长疏水链表面活性剂的 CMC 与实验数据有显著差异。考察其中一种表面活性剂 $Gem_{n}EO_{m}$ (分子式表示为 $\mathrm{H(CH_{2})_{n-2}CHCH_{2}O(CH_{2}CH_{2}O)_{m}H)_{2}(CH_{2})_{6}}$ )，发现当疏水尾链碳原子数 $n \geq 12$ 时，理论算得的平衡 $\mathrm{CMC(CMC_{eq})}$ 极低，但实验测得到达表观平衡时的胶束浓度 $(\mathrm{CMC}_{\mathrm{app}})$ 显著偏高。

![](images/e15252766bedad9bbb693b7d4c580fb480e2e4eed9de794e46f936af565ee3cf.jpg)

4-1 与理论胶束形成时间 $T_{s}$ 主要相关时间 $T_{0}$ 由下式给出：

$$
T _ {0} = \frac {6 \pi \eta R _ {\mathrm{h}} ^ {3}}{M _ {\mathrm{eq}} k T}
$$

其中 $\eta$ 、 $R_{h}$ 、k、T 均为常数，聚集数 $M_{eq}$ 与尾链碳原子数 n 为线性关系。在 $25^{\circ}C$ 的水溶液中，有近似关系 $T_{0}=\frac{7.17}{M_{eq}}\times10^{-10}$ 。已知一系列不同 n 下的 $T_{0}$ 如下表所示。通过计算，用 n 表示 $M_{eq}$ (系数均保留至整数)。

<table><tr><td>n</td><td>12</td><td>13</td><td>14</td><td>15</td></tr><tr><td> $T_0(s)$ </td><td> $6.18\times 10^{-12}$ </td><td> $5.69\times 10^{-12}$ </td><td> $5.27\times 10^{-12}$ </td><td> $4.91\times 10^{-12}$ </td></tr></table>

通过分析题干中“线性关系”以及典型的表格型二元数据关系，可以基本推断本题主要考查内容为数据处理与线性回归。那么解决本题的关键步骤就是厘清物理量之间的相互关系，可以发现本题涉及最重要的三个物理量为主要相关时间 $T_{0}$ 、聚集数 $M_{eq}$ 与尾链碳原子数 n，且其中 $T_{0}$ 与 $M_{eq}$ 、 $M_{eq}$ 与 n 的关系已经明确，只需做简单的变换就可以建立物理量之间的转换关系。下面以一种方法为例进行计算：

由 $M_{eq}$ 与尾链碳原子数、n 为线性关系可设：

$$
M _ {\mathrm{eq}} = a n + b
$$

对公式进行变换可得:

$$
T _ {0} = \frac {7.17}{a n + b} \times 10 ^ {- 10} \Rightarrow \frac {1}{T _ {0}} = \frac {a}{7.17} \times 10 ^ {10} n + \frac {b}{7.17} \times 10 ^ {10}
$$

对表中数据进行处理：

<table><tr><td>n</td><td>12</td><td>13</td><td>14</td><td>15</td></tr><tr><td> $\frac{1}{T_0}$ </td><td> $1.62\times 10^{11}$ </td><td> $1.76\times 10^{11}$ </td><td> $1.90\times 10^{11}$ </td><td> $2.04\times 10^{11}$ </td></tr></table>

线性回归得： $\frac{1}{T_0} = 1.40\times 10^{10}n - 6.00\times 10^9$

从而得到： $a = 10$ ， $b = -4$ ，因此 $M_{\mathrm{eq}} = 10n - 4$ （本题要求系数保留至整数）

当然，本题不只一种解法。若先回归得到 $n$ 与 $M_{\mathrm{eq}}$ 的关系列表，再进行回归计算，答案正确亦可得满分。

4-2 建立 $T_{0}$ 与理论胶束形成时间 $T_{s}$ 关系如下:

$$
T _ {\mathrm{s}} = T _ {0} e ^ {F _ {\mathrm{a}}}
$$

其中 $F_{a}$ 为理论活化能垒，其经验公式为 $F_{a}=15n-130$ 。请计算 n=16 时胶束形成的理论平衡时间 $T_{s}$ (单位：秒)，并指出其是否可在实验室内观测。

本题建立了理论形成时间 $T_{s}$ 与 $T_{0}$ 的关系式，并要求我们计算特定 n 下的 $T_{s}$ ，显然只需要将数据代入公式计算即可。

$$
n = 16 \text {   时,   } F _ {\mathrm{a}} = 15 n - 130 = 110
$$

由4-1得：

$$
T _ {0} = \frac {7.17}{M _ {e q}} \times 10 ^ {- 10} = \frac {7.17}{10 \times 16 - 4} \times 10 ^ {- 10} = 4.60 \times 10 ^ {- 12} \mathrm{s}
$$

因此：

$$
T _ {\mathrm{s}} = T _ {0} e ^ {F _ {\mathrm{a}}} = 2.72 \times 10 ^ {36} \mathrm{s}
$$

由于 $T_{s}$ 约等于 $3 \times 10^{31}$ 天（约等于 $9 \times 10^{28}$ 年），故无法在实验室中观测。

4-3 已知表观临界胶束浓度 $CMC_{app}$ 与平衡 $CMC_{eq}$ 均满足关系式( $F_{a}^{app}$ 为表观活化能垒):

$$
\mathrm{CMC} _ {\text { app }} = k e ^ {- F _ {\mathrm{a}} ^ {\text { app }} / n}, \mathrm{CMC} _ {\text { eq }} = k e ^ {- F _ {\mathrm{a}} / n}
$$

若实验要求针对 $n = 16$ 的表面活性剂，可在 $1\mathrm{h}$ 内观测到胶束化现象，计算该条件下 $\mathrm{CMC_{app} / CMC_{eq}}$ 的值。

本题相较 4-1 与 4-2 引入了“表观”的一系列物理量，即 $CMC_{app}$ 、 $F_{a}^{app}$ 以及表观胶束时间(1 h)。我们需要明确这些物理量“表观”的内涵，即通过实验手段确定的观测值。

接下来，我们利用题给的公式从所需求得的物理量反推：

$$
\mathrm{CMC} _ {\text { app }} / \mathrm{CMC} _ {\text { eq }} = e ^ {- (F _ {\mathrm{a}} ^ {\text { app }} - F _ {\mathrm{a}}) / n}
$$

这时我们会发现，n 与 $F_{a}$ 是已知量，而唯一未知的 $F_{a}^{app}$ 就成了解题的关键。而题目已知信息中还有表观胶束化时间 1 h 没有使用，这里显然需要建立表观活化能与表观时间的关系（需要迁移 4-2 当中的公式）：

$$
T _ {\mathrm{app}} = T _ {0} e ^ {F _ {\mathrm{a}} ^ {\mathrm{app}}} \Rightarrow F _ {\mathrm{a}} ^ {\mathrm{app}} = \ln \frac {T _ {\mathrm{app}}}{T _ {0}} = \ln \frac {3600 \mathrm{s}}{4.60 \times 10 ^ {- 12} \mathrm{s}} = 34.29
$$

从而有：

$$
\mathrm{CMC} _ {\text { app }} / \mathrm{CMC} _ {\text { eq }} = e ^ {- (F _ {\mathrm{a}} ^ {\text { app }} - F _ {\mathrm{a}}) / n} = e ^ {- (34.29 - 110) / 16} = 1.13 \times 10 ^ {2}
$$

4-4 从化学反应原理的角度，解释 n 较大时的长链表面活性剂的表观临界浓度( $CMC_{app}$ )高于平衡 $CMC(CMC_{eq})$ 的原因。

本题作为解释题，框定了答题角度——“化学反应原理”。阅卷中发现很多同学对于这一名词并不熟悉，试图从分子结构、反应机理等角度进行解释。然而事实上，这一名词背后的内涵应当归类于物理化学的范畴，在这道题目中主要是以热力学、动力学等角度体现的。

明确了答题角度，接下来则需要明确需要解释的物理量内涵。表观临界浓度在本题中代表，实验室中观测到胶束化现象平衡时，测得活性剂分子的浓度；而平衡 CMC 则是理论计算得到的，真实热力学平衡的活性剂分子浓度。

依据前三问计算结果不难发现，如需达到热力学平衡，所需时间 $T_{\mathrm{s}}$ 在惊人的 $10^{36}\mathrm{s}$ 数量级显然是无法实现“表观”这一要求的；对应的，表观平衡时，活性剂并没有全部胶束化，测得浓度也应当远大于热力学平衡时的浓度。

综上所示，总结本题表述如下：n 较大时，活化能 $F_{a}$ 增大， $T_{s}$ 近似呈指数增长，体系无法到达热力学平衡，只能到达表观平衡（即浓度近似不再变化），此时的活性剂分子浓度显著高于热力学平衡时的浓度。


## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**（OCR 原文逐字转录，可能保留原卷笔误）。