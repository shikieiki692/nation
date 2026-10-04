---
title: "题-QBY-10-06-在化学动力学中对于R与P间的"
aliases: ["题-QBY-10-06"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "清北营 春季模拟10 第 6 题"
module: "2026机构初赛模拟题"
source_subject: 化学原理
syllabus_codes: [57]
knowledge_points:
  - "[[化学动力学]]"
  - "[[稳态近似]]"
  - "[[碰撞理论与过渡态理论]]"
  - "[[速率方程]]"
tags: [化竞, 题目, 初赛, 机构模拟题, 清北营]
updated: 2026-09-26
status: 已填充
exam_stage: 初赛
subject_module: 化学原理
pack: 综合模拟卷
submodule: 清北营
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_tier: 2
source_norm: "清北营-春季模拟10"
source_file: "2026机构初赛模拟题/04-清北营/春季模拟10.md"
---

# 题-QBY-10-06-在化学动力学中对于R与P间的

## 题目

### 第 6 题（34分，占 $22\%$ ）可逆双相模型动力学

在化学动力学中，对于 R 与 P 间的单分子异构化反应，传统的过渡态理论假设反应经过一个过渡态，但该过渡态不可观测。近年来，研究人员提出了一种“可逆双相模型”，认为反应过程中存在一个可观测的过渡态物种 TS，该模型可以更准确地描述热中性或近热中性反应的动力学，其反应机理如下：

$$
\mathrm{R} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathrm{TS} \xrightarrow [ k _ {- 2} ]{k _ {2}} \mathrm{P}
$$

其中 $k_{1}$ 、 $k_{-1}$ 、 $k_{2}$ 、 $k_{-2}$ 为基元步骤的速率常数。本题假设初始时刻（ $i=0$ ）只有反应物 R（浓度为 $[\mathbf{R}]_{0}$ ），过渡态 TS 和产物 P 的浓度均近似于 0。定义达到平衡时各物种浓度为 $[\mathbf{R}]_{\mathrm{cq}}$ 、 $[\mathbf{TS}]_{\mathrm{cq}}$ 、 $[\mathbf{P}]_{\mathrm{cq}}$ ，偏离平衡的浓度差 $a(t) = [\mathbf{R}] - [\mathbf{R}]_{\mathrm{eq}}$ ， $b(t) = [\mathbf{TS}] - [\mathbf{TS}]_{\mathrm{cq}}$ 、 $c(t) = [\mathbf{P}] - [\mathbf{P}]_{\mathrm{cq}}$ 。

（1）指处于化学平衡的反应系统满足精细平衡原理，每个元反应与其逆向元反应速率相等。

(2) 对于关于 $x 、 y$ 的方程组 $\left\{ \begin{array}{l}px + qy = 0 \\ rx + sy = 0 \end{array} \right.$ , 其有非零解的条件为 $ps - qr = 0$ 。

(3) 速率常数 $k_{\alpha \to \beta} = \frac{k_B T}{h} \frac{q^\beta}{q^\alpha}$ , 其中 $\frac{q^\beta}{q^\alpha}$ 为在反应体系内发现 $\beta$ 与 $\alpha$ 的概率之比。

(4) Erying 方程: $k = \frac{k_{B} T}{h} e^{\frac{\Delta G^{\ddagger}}{R T}}$ , 其中 $\Delta G^{\ddagger}$ 为反应活化摩尔吉布斯自由能变。

6-1 用各速率常数和 $[\mathbf{R}]_0$ 表示平衡时各物种浓度 $[\mathbf{R}]_{\mathrm{cq}}$ 、 $[\mathbf{TS}]_{\mathrm{cq}}$ 、 $[\mathbf{P}]_{\mathrm{cq}}$ 。

6-2 用各速率常数和 $a(t)$ 、 $b(t)$ 表示 $\frac{da(t)}{dt}$ 与 $\frac{db(t)}{dt}$ 。

6-3 根据经验，偏离量按指数衰减，即 $a(t) = A_{1}\mathrm{e}^{-\lambda_{1}t} + A_{2}\mathrm{e}^{-\lambda_{2}t}$ 、 $b(t) = B_{1}\mathrm{e}^{-\lambda_{1}t} + B_{2}\mathrm{e}^{-\lambda_{2}t}$ 。用各速率常数

表示 $\lambda_{1}$ 与 $\lambda_{2}$ （已知 $\lambda_{1}$ 大于 $\lambda_{2}$ ）。提示：最后结果无需展开括号外的平方。

6-4 热中性（Thermoneutral）指的是总反应的 $\Delta G^{\circ} = 0$ 。若反应为热中性，定义 $\mathbf{R} \rightarrow \mathbf{P}$ 为反应正方向，近似认为反应开始后 TS 瞬间达到稳态，推导反应初始表观正反应速率常数 $k_{\mathrm{obs}}$ （即生成 P 的速率常数）与从 R 到 TS 的摩尔吉布斯自由能变 $\Delta G^{\ddagger}$ 之间的关系。提示：思考各速率常数间的关系。

6-5 研究人员研究了如下近热中性的异构化反应（定义左侧为底物，右侧为产物），通过 $^{13}\mathrm{C}$ NMR得到了一系列动力学数据，通过线性拟合得到了 $\ln (k / T)$ 随 $1 / T$ 变化的直线（其中 $k$ 为正反应表观速率， $T$ 为温度），其斜率为-2261、截距为23.17（回归所用物理量均被国际单位处理为无量纲量）。

![](images/e93fdf8c7476963601530e55bf97314b5928d709257709faea336b052dfcee52.jpg)

6-5-1 写出产物中与D原子相连手性中心的绝对构型。

6-5-2 计算可逆双相模型下的正反应摩尔活化焓 $\Delta H^1$ 与摩尔活化熵 $\Delta S^4$ 。该结果与通过Eyring方程得到的结果是否完全相同？如果相同，证明其等价性；如果不同，说明不同之处与产生该差异的本质原因。

![](images/dc47052de59ff2858b66168247dee4698f432730c080eace48c74ec7c12c9161.jpg)

# 清北营 2026 年春季化学竞赛高端 VIP 班（试卷 10）

物化专题 考试时间：2026年4月20日18:00\~21:00

## 参考答案

在化学动力学中, 对于 $\mathbf{R}$ 与 $\mathbf{P}$ 间的单分子异构化反应, 传统的过渡态理论假设反应经过一个过渡态,但该过渡态不可观测。近年来, 研究人员提出了一种 “可逆双相模型”, 认为反应过程中存在一个可观测的过渡态物种 TS, 该模型可以更准确地描述热中性或近热中性反应的动力学, 其反应机理如下:

$$
\mathrm{R} \xrightarrow [ k _ {1} ]{\Lambda_ {1}} \mathrm{TS} \xrightarrow [ k _ {2} ]{k _ {2}} \mathrm{P}
$$

其中 $A_{1}, A_{1}, A_{2}, k_{\alpha}$ 为基元步骤的速率常数。本题假设初始时刻（ $t=0$ ）只有反应拱 $\mathbf{R}$ （浓度为 $[\mathbf{R}]_{0}$ ），过渡态 TS 和产物 P 的浓度均近似于 0，定义达到平衡时各物种浓度为 $[\mathbf{R}]_{\sigma q}, [\mathbf{TS}]_{\sigma q}, [\mathbf{P}]_{\sigma q}$ ，偏离平衡的浓度差 $a(t) = [\mathbf{R}] - [\mathbf{R}]_{\sigma q}$ 、 $b(t) = [\mathbf{TS}] - [\mathbf{TS}]_{\sigma q}$ 、 $f(\xi) = [\mathbf{P}] - [\mathbf{P}]_{\sigma q}$ 。

提示：

（1）指处于化学平衡的反应系统满足精细平衡原理，每个元反应与其逆向元反应速率相等。

(2) 对于关于 $a$ 、 $y$ 的方程组 $\left\{ \begin{array}{l} px + qy = 0 \\ rx + sy = 0 \end{array} \right.$ ，其有非零解的条件为 $ps - qr = 0$ 。

（3）速率常数 $k_{\alpha \rightarrow \beta} = \frac{k_a\Gamma}{a}\frac{q^{\beta}}{q^{\alpha}}$ 其中 $\frac{q^{\alpha}}{q^{\alpha}}$ 为在反应体系内发现 $\beta$ 与 $a$ 的概率之比。

（4）Erying方程： $k = \frac{k_B r}{\hbar} e^{-\frac{\Delta G^{\ddagger}}{R T}}$ ，其中 $\Delta G^{\ddagger}$ 为反应活化摩尔吉布斯自由能变。

6-1 用各速率常数和 $[\mathbf{R}]_{\mathfrak{q}}$ 表示平衡时各物种浓度 $[\mathbf{R}]_{\mathfrak{cq}}$ 、 $[\mathbf{TS}]_{\mathfrak{cq}}$ 、 $[\mathbf{P}]_{\mathfrak{cq}}$ 。

6-1 平衡时满足精细平衡，可直接用 $\kappa_{1}k_{1}$ 、 $k_{2}/k_{3}$ 表示相应的平衡常数，即 $\frac{[\mathbf{R}]_{\alpha q}}{[\mathrm{TS}]_{\alpha q}} = \frac{k_{-1}}{k_{1}}$ 、 $\frac{[\mathrm{P}]_{\alpha q}}{[\mathrm{TS}]_{\alpha q}} = \frac{k_{7}}{k_{-2}}$ 。又由物料守恒 $[\overline{\mathbf{R}}]_{0} = [\mathbf{R}]_{\alpha q} + [\mathrm{TS}]_{\alpha q} + [\mathrm{P}]_{\alpha q}$ ，解得： $\left\{\begin{aligned}[R]_{\alpha q}&=\frac{k_{-1}k_{-2}[R]_{0}}{k_{1}k_{2}+k_{1}k_{-2}+k_{-1}k_{-2}}\\[TS]_{\alpha q}&=\frac{k_{1}k_{-2}[R]_{0}}{k_{1}k_{2}+k_{2}k_{-2}+k_{-1}k_{-2}}\\[P]_{\alpha q}&=\frac{k_{1}k_{2}[R]_{0}}{k_{1}k_{2}+k_{1}k_{-2}+k_{-1}k_{-2}}\end{aligned}\right.$

6-2 用各速率常数和 $a(t)$ 、 $b(t)$ 表示 $\frac{da(t)}{dt}$ 与 $\frac{db(t)}{dt}$ 。

6-2

由总浓度守恒，易得 $a(t)+b(t)\neq c(t)=0$ $\frac{da(t)}{dt}=\frac{d([R]-[R]_{cq})}{dt}=\frac{d[R]}{dt}=-k_{1}[R]+k_{-1}[TS]$ $=-k_{1}(a(t)+[R]_{cq})+k_{-1}(b(t)+[TS]_{cq})=-k_{1}a(t)+k_{-1}b(t)$ $\frac{db(t)}{dt}=\frac{d([TS]-[TS]_{cq})}{dt}=\frac{d[TS]}{dt}=k_{1}[R]-(k_{-1}+k_{2})[TS]-k_{-2}[P]$ $=k_{1}(a(t)+[R]_{cq})-(k_{-1}+k_{2})(b(t)+[TS]_{cq})-k_{-2}(c(t)+[P]_{cq})$ $=k_{1}a(t)-(k_{-1}+k_{2})b(t)-k_{-2}c(t)$ $=(k_{1}-k_{-2})a(t)-(k_{-1}+k_{2}+k_{-2})b(t)$

6-3 根据经验, 偏离量按指数衰减, 即 $a(t) = A_{1} \mathrm{e}^{-\lambda_{1} t} + A_{2} \mathrm{e}^{-\lambda_{2} t}$ 、 $b(t) = B_{1} \mathrm{e}^{-\lambda_{1} t} + B_{2} \mathrm{e}^{-\lambda_{2} t}$ 。用各速率常数表示 $\lambda_{1}$ 与 $\lambda_{2}$ (已知 $\lambda_{1}$ 大于 $\lambda_{2}$ )。提示: 最后结果无需展开括号外的平方。

6- 3

将 $a(t) = A_{1}e^{-\lambda_{1}t} + A_{2}e^{-\lambda_{2}t}$ 、 $b(t) = B_{1}e^{-\lambda_{1}t} + B_{2}e^{-\lambda_{2}t}$ 代入上述微分方程组： $\left\{ \begin{array}{l} -\lambda_1A_1e^{-\lambda_1t} + -\lambda_2d_2e^{-\lambda_2t} = -k_1(A_1e^{-\lambda_1t} + A_2e^{-b_2t}) + k_{-1}(B_1e^{-\lambda_1t} + B_2e^{-\lambda_2t})\\ -\lambda_1B_1e^{-\lambda_1t} - \lambda_2B_2e^{-\lambda_2t} = (k_1 - k_{-2})(A_1e^{-\lambda_1t} + A_2e^{-\lambda_1t}) - (k_{-1} + k_2 + k_{-2})(B_1e^{-\lambda_1t} + B_2e^{-\lambda_2t}) \end{array} \right.$

把指数不同的项分离，得到两组方程组：

$$
\left\{ \begin{array}{c} - \lambda_ {1} A _ {1} o ^ {- \lambda_ {1} t} = - k _ {1} A _ {1} o ^ {- \lambda_ {1} t} + k _ {- 1} B _ {1} o ^ {- \lambda_ {1} t} \\ - \lambda_ {1} B _ {1} e ^ {- \lambda_ {1} t} = (k _ {1} - k _ {- 2}) A _ {1} o ^ {- \lambda_ {1} t} - (k _ {- 1} + k _ {2} + k _ {- 2}) B _ {1} o ^ {- \lambda_ {2} t} \\ \left\{ \begin{array}{c} - \lambda_ {2} A _ {2} o ^ {- \lambda_ {2} t} = - k _ {1} A _ {2} o ^ {- \lambda_ {2} t} + k _ {- 1} B _ {\hat {z}} o ^ {- \lambda_ {3} t} \\ - \lambda_ {1} B _ {\hat {z}} o ^ {- \lambda_ {2} t} = (k _ {1} - k _ {- 2}) A _ {\hat {z}} o ^ {- \lambda_ {2} t} + (k _ {- 1} + k _ {\hat {z}} + k _ {- 2}) B _ {\hat {z}} o ^ {- \lambda_ {3} t} \end{array} \right. \end{array} \right.
$$

可化简为如下方程组：

$$
(k _ {1} - \lambda_ {1}) A _ {1} - k _ {2} B _ {1} = 0
$$

$$
\left(k _ {1} - k _ {- 2}\right) A _ {1} - \left(\lambda_ {1} - k _ {- 1} - k _ {2} - k _ {- 2}\right) B _ {1} = 0
$$

$$
\left(k _ {1} = \lambda_ {2}\right) A _ {2} - k _ {- 1} B _ {2} = 0
$$

$$
(k _ {1} - k _ {- 2}) A _ {2} = (\lambda_ {2} - k _ {- 1} - k _ {2} - k _ {- 2}) B _ {2} = 0
$$

欲使表达式有意义，系数 $A$ 、 $B$ 须存在非零解。

由于 $\lambda_{1} \neq \lambda_{2}$ , 故 $\lambda_{1}, \lambda_{2}$ 为同一个二次方程的两个根。

$$
\lambda^ {2} - (k _ {1} + k _ {- 1} + k _ {2} + k _ {- 2}) \lambda + (k _ {1} k _ {\overline {{{{2}}}}} + k _ {1} k _ {- 2} + k _ {- 1} k _ {- 2}) = \lambda^ {2} - \kappa \lambda + \gamma^ {2} = 0
$$

解得

$$
\lambda_ {1} = \frac {k _ {1} + k _ {- 1} + k _ {2} + k _ {- 2} + \sqrt {(k _ {1} + k _ {- 1} + k _ {2} + k _ {- 2}) ^ {2} - 4 (k _ {1} k _ {2} + k _ {1} k _ {- 2} + k _ {- 1} k _ {- 2}) ^ {2}}}{2}
$$

$$
\lambda_ {2} = \frac {k _ {1} + k _ {- 1} + k _ {2} + k _ {- 2} - \sqrt {(k _ {1} + k _ {- 1} + k _ {2} + k _ {- 2}) ^ {2} - 4 (k _ {1} k _ {2} + k _ {1} k _ {- 2} + k _ {- 1} k _ {- 2}) ^ {2}}}{2}
$$

6-4 热中性（Thermonectral）指的是总反应的 $\Delta G^{\circ} = 0$ 。若反应为热中性，定义 $\mathbf{R} \rightarrow \mathbf{P}$ 为反应正方向，近似认为反应开始后 TS 瞬间达到稳态，推导反应初始表观正反应速率常数 $k_{\mathrm{obt}}$ （即生成 P 的速率常数）与从 R 到 TS 的摩尔吉布斯自由能变 $\Delta G^{\prime}$ 之间的关系。提示：思考各速率常数间的关系。

64

由反应热中性与极示（3）可得 $k_{1}=k_{-2}\gamma,k_{-1}=k_{2}$ 对 TS 进行稳态近似

$$
\frac {d [ \mathrm{TS} ]}{d t} = - (k _ {- 1} + k _ {2}) [ \mathrm{TS} ] + k _ {1} [ \mathrm{R} ] + k _ {- 2} [ \mathrm{P} ] = 0
$$

$$
[ \mathrm{TS} ] = \frac {k _ {1} [ \mathrm{R} ] + k _ {- 2} [ \mathrm{P} ]}{k _ {- 1} + k _ {2}}
$$

由于初始 $\mathbf{P}$ 的浓度很小，故可近似忽略，即

$$
r _ {\mathrm{obs}} = k _ {2} [ \mathrm{TS} ] = \frac {k _ {1} k _ {2}}{k _ {- 1} + k _ {2}} [ \mathrm{R} ]
$$

综上可得:

$$
k _ {\mathrm{obs}} = \frac {k _ {1} k _ {2}}{k _ {- 1} + k _ {2}} = \frac {k _ {1}}{2} = \frac {1}{2} \frac {k _ {8} T}{h} \frac {q ^ {\mathrm{TS}}}{q ^ {\mathrm{R}}} = \frac {1}{2} \frac {k _ {B} T}{h} \mathrm{e} ^ {- \frac {\Delta G ^ {\ddagger}}{R T}}
$$

![](images/037cabdffb812fab353b7e42708f77f933400a4d39332c6ba3bdd02036c004d7.jpg)

6-5 研究人员研究了如下近热中性的异构化反应（定义左侧为底物，右侧为产物），通过 $^{13}\mathrm{C}$ NMR得到了一系列动力学数据，通过线性拟合得到了 $\ln (k / T)$ 随 $1 / T$ 变化的直线（其中 $k$ 为正反应表观速率， $T$ 为温度），其斜率为-2261、截距为23.17（回归所用物理量均被国际单位处理为无量纲量）。

![](images/d5c3c1bcac7bdbf735a8557c24b6796ce96b973049ff515b702b38d1aa15ab89.jpg)

6-5-1 写出产物中与 D 原子相连手性中心的绝对构型。

6-5-2 计算可逆双相模型下的正反应摩尔活化焓 $\Delta H^{\ddagger}$ 与摩尔活化熵 $\Delta S^{\ddagger}$ 。该结果与通过 Eyring 方程得到的结果是否完全相同？如果相同，证明其等价性；如果不同，说明不同之处与产生该差异的本质原因。

6-5-2

$$
k _ {\mathrm{obs}} = \frac {1}{2} \frac {k _ {B} T}{h} e ^ {\frac {\Delta G ^ {\ddagger}}{R T}} = \frac {1}{2} \frac {k _ {B} T}{h} e ^ {\frac {\Delta H ^ {\ddagger} - T \Delta S ^ {\ddagger}}{R T}}
$$

$$
\ln (\frac {k _ {\mathrm{obs}}}{T}) = \ln (\frac {1}{2} \frac {k _ {B}}{h} \mathrm{e} ^ {- \frac {\Delta H ^ {\ddagger} - T \Delta S ^ {\ddagger}}{R T}}) = - \frac {\Delta H ^ {\ddagger}}{R} \frac {1}{T} + \left[ \ln (\frac {1}{2} \frac {k _ {B}}{h}) + \frac {\Delta S ^ {\ddagger}}{R} \right]
$$

故

$$
- \frac {\Delta H ^ {\ddagger}}{R} = - 2261
$$

$$
\ln \left(\frac {1}{2} \frac {k _ {B}}{h}\right) + \frac {\Delta S ^ {\ddagger}}{R} = 23.17
$$

$$
\left\{ \begin{array}{c} \Delta H ^ {\ddagger} = 18.80 \mathrm{kJ/mol} \\ \Delta S ^ {\ddagger} = 0.8578 \mathrm {J / (mol\cdot K)} \end{array} \right.
$$

该结果与Eyring方程不完全相同。

摩尔活化焓相同而摩尔活化熵不同。

因为Eyring方程认为反应过程仅为越过一个势垒, 是瞬时、单向的; 而可逆双相模型认为反应经历了可观测的、具有一定寿命的中间体, 是可逆的, 因此不仅指数上的自由能变定义不同, 还多出了系数 $1 / 2$ 。

![](images/fe8388d18742a4c66adef7c8a5ba9d8eeb852b73b5a461cfc1c02fe3edb8b4cd.jpg)

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**（OCR 原文逐字转录，可能保留原卷笔误）。