---
title: "傅献彩《物理化学》（第六版上册）-第三章 热力学第二定律（二）：Maxwell关系式与规定熵"
type: 外部教材切片
source_book: "物理化学（第六版上册）-傅献彩"
syllabus_codes: [决赛-04]
created: 2026-09-25
updated: 2026-09-25
status: 已填充
---

## Maxwell 关系式及其应用

设 z 代表系统的任一状态函数, 且 z 是两个变量 x 和 y 的函数。由于状态函数 z 的变化与过程无关, 在数学上称 z 具有全微分的性质。

$$
\begin{array}{c} {z = f (x, y)} \\ {\mathrm{d} z = \left(\frac {\partial z}{\partial x}\right) _ {y} \mathrm{d} x + \left(\frac {\partial z}{\partial y}\right) _ {x} \mathrm{d} y = M \mathrm{d} x + N \mathrm{d} y} \end{array}
$$

在上式中令 $M = \left(\frac{\partial z}{\partial x}\right)_y, N = \left(\frac{\partial z}{\partial y}\right)_x, M$ 和 $N$ 也是 $x$ 和 $y$ 的函数。将 $M$ 对 $y$ 偏微分， $N$ 对 $x$ 偏微分，得

$$
\left(\frac {\partial M}{\partial y}\right) _ {x} = \frac {\partial^ {2} z}{\partial y \partial x} \quad \left(\frac {\partial N}{\partial x}\right) _ {y} = \frac {\partial^ {2} z}{\partial x \partial y}
$$

因此

$$
\left(\frac {\partial M}{\partial y}\right) _ {x} = \left(\frac {\partial N}{\partial x}\right) _ {y}\tag{3.63}
$$

把式 (3.63) 应用到式 (3.55) \~ 式 (3.58), 得到

$$
\left(\frac {\partial T}{\partial V}\right) _ {S} = - \left(\frac {\partial p}{\partial S}\right) _ {V}\tag{3.64}
$$

$$
\left(\frac {\partial T}{\partial p}\right) _ {S} = \left(\frac {\partial V}{\partial S}\right) _ {p}\tag{3.65}
$$

$$
\left(\frac {\partial S}{\partial V}\right) _ {T} = \left(\frac {\partial p}{\partial T}\right) _ {V}\tag{3.66}
$$

$$
\left(\frac {\partial S}{\partial p}\right) _ {T} = - \left(\frac {\partial V}{\partial T}\right) _ {p}\tag{3.67}
$$

式 (3.64)～式 (3.67) 四个关系式称为 Maxwell 关系式 (Maxwell's relations)。这些式子表示简单系统在平衡时，几个热力学函数之间的关系。这些关系式的一个用处是，可用容易由实验测定的偏微分来代替那些不易直接测定的偏微分。例如，在最后两个关系式中，可以根据状态方程式求出熵随 $V, p$ 的变化关系。下面介绍 Maxwell 关系式的某些应用。

(1) 求 U 随 V 的变化关系 自式 (3.55) $dU = T dS - p dV$ ，可得

$$
\left(\frac {\partial U}{\partial V}\right) _ {T} = T \left(\frac {\partial S}{\partial V}\right) _ {T} - p
$$

$\left(\frac{\partial S}{\partial V}\right)_{T}$ 不易直接测定。但是，根据式(3.66)，上式可写作

$$
\left(\frac {\partial U}{\partial V}\right) _ {T} = T \left(\frac {\partial p}{\partial T}\right) _ {V} - p\tag{3.68}
$$

对于理想气体, 有

$$
\left(\frac {\partial p}{\partial T}\right) _ {V} = \frac {n R}{V}
$$

代入上式后, 则得

$$
\left(\frac {\partial U}{\partial V}\right) _ {T} = 0
$$

对于非理想气体, 若知道状态方程就能求出 $\left(\frac{\partial U}{\partial V}\right)_{T}$ 的值。

(2) 求 H 随 p 的变化关系 自式 (3.56) $dH = T dS + V dp$ , 可得

$$
\left(\frac {\partial H}{\partial p}\right) _ {T} = T \left(\frac {\partial S}{\partial p}\right) _ {T} + V
$$

式中 $\left(\frac{\partial S}{\partial p}\right)_T$ 不易直接测定。但是，根据式(3.67)，上式可写作

$$
\left(\frac {\partial H}{\partial p}\right) _ {T} = V - T \left(\frac {\partial V}{\partial T}\right) _ {p}\tag{3.69}
$$

式 (3.68) 和式 (3.69) 等号右方的量, 可自状态方程式求得。因而, 式 (3.68) 和式 (3.69) 也称为热力学状态方程式 (thermodynamic equation of state), 这是两个很有用的公式。由此可求得实际气体在等温过程中的热力学能和焓的变化值。例如, 对于理想气体, 代入后, 得

$$
\left(\frac {\partial U}{\partial V}\right) _ {T} = 0 \quad \left(\frac {\partial H}{\partial p}\right) _ {T} = 0
$$

又如, 式 (3.68) 和式 (3.69) 可用来求当系统由状态 (1) $(p_{1}, V_{1}, T_{1})$ 变到状态 (2) $(p_{2}, V_{2}, T_{2})$ 时的 $\Delta U$ 和 $\Delta H$ , 即

$$
\begin{array}{r l r} {\text {状态} (1)} & {\xrightarrow {\Delta U , \Delta H}} & {\text {状态} (2)} \\ {(p _ {1}, V _ {1}, T _ {1})} & & {(p _ {2}, V _ {2}, T _ {2})} \end{array}
$$

若将 U 写作 T, V 的函数:

$$
\mathrm{d} U = \left(\frac {\partial U}{\partial T}\right) _ {V} \mathrm{d} T + \left(\frac {\partial U}{\partial V}\right) _ {T} \mathrm{d} V
$$

代入式 (3.68), 则

$$
\begin{array}{l} \mathrm{d} U = C _ {V} \mathrm{d} T + \left[ T \left(\frac {\partial p}{\partial T}\right) _ {V} - p \right] \mathrm{d} V \\ \Delta U = \int C _ {V} \mathrm{d} T + \int \left[ T \left(\frac {\partial p}{\partial T}\right) _ {V} - p \right] \mathrm{d} V \end{array}\tag{3.70}
$$

若将 H 写作 T, p 的函数:

$$
\mathrm{d} H = \left(\frac {\partial H}{\partial T}\right) _ {p} \mathrm{d} T + \left(\frac {\partial H}{\partial p}\right) _ {T} \mathrm{d} p
$$

代入式 (3.69), 则

$$
\begin{array}{l} \mathrm{d} H = C _ {p} \mathrm{d} T + \left[ V - T \left(\frac {\partial V}{\partial T}\right) _ {p} \right] \mathrm{d} p \\ \Delta H = \int C _ {p} \mathrm{d} T + \int \left[ V - T \left(\frac {\partial V}{\partial T}\right) _ {p} \right] \mathrm{d} p \end{array}\tag{3.71}
$$

知道状态方程就能求出上两式中等式右方的第二个积分项。

(3) $S$ 随 $p$ 或 $V$ 的变化关系 根据式 (3.67):

$$
\left(\frac {\partial S}{\partial p}\right) _ {T} = - \left(\frac {\partial V}{\partial T}\right) _ {p}
$$

定义等压热膨胀系数 (isobaric thermal expansivity):

$$
\alpha = \frac {1}{V} \left(\frac {\partial V}{\partial T}\right) _ {p}
$$

代入上式积分, 得

$$
\Delta S = S _ {2} - S _ {1} = - \int_ {p _ {1}} ^ {p _ {2}} \alpha V \mathrm{d} p\tag{3.72}
$$

若知道 $V, \alpha$ 与 p 的关系 (这可从状态方程式求得), 即可对上式积分。例如, 对于理想气体:

$$
p V = n R T \quad \left(\frac {\partial V}{\partial T}\right) _ {p} = \alpha V = \frac {n R}{p}
$$

所以

$$
\Delta S = - \int_ {p _ {1}} ^ {p _ {2}} n R \frac {\mathrm{d} p}{p} = n R \ln \frac {p _ {1}}{p _ {2}} = n R \ln \frac {V _ {2}}{V _ {1}}
$$

(4) 求 Joule-Thomson 系数 已知

$$
\mu_ {\mathrm{J-T}} = - \frac {1}{C _ {p}} \left(\frac {\partial H}{\partial p}\right) _ {T}
$$

代入式 (3.69) 后得

$$
\mu_ {\mathrm{J-T}} = - \frac {1}{C _ {p}} \left[ V - T \left(\frac {\partial V}{\partial T}\right) _ {p} \right]\tag{3.73}
$$

从状态方程式可以求得 $\mu_{J-T}$ 值, 并可解释何以 $\mu_{J-T}$ 的值有时为正, 有时为负。

## Gibbs 自由能与温度的关系——Gibbs-Helmholtz 方程

在讨论化学反应问题时, 常需自某一反应温度的 $\Delta_{\mathrm{r}}G_{\mathrm{m}}(T_{1})$ 求另一个温度时的 $\Delta_{\mathrm{r}}G_{\mathrm{m}}(T_{2})$ 。

根据热力学基本公式:

$$
\mathrm{d} G = - S \mathrm{d} T + V \mathrm{d} p \quad \left(\frac {\partial G}{\partial T}\right) _ {p} = - S
$$

则

$$
\left(\frac {\partial \Delta G}{\partial T}\right) _ {p} = - \Delta S
$$

式中左方表示反应的 $\Delta G$ 在压力恒定的条件下随温度的变化率。又已知在温度 T 时, 有

$$
\Delta G = \Delta H - T \Delta S \quad \text {或} \quad - \Delta S = \frac {\Delta G - \Delta H}{T}
$$

代入上式得

$$
\left(\frac {\partial \Delta G}{\partial T}\right) _ {p} = \frac {\Delta G - \Delta H}{T}\tag{3.74}
$$

上式可以写成易于积分的形式:

$$
\frac {1}{T} \left(\frac {\partial \Delta G}{\partial T}\right) _ {p} - \frac {\Delta G}{T ^ {2}} = - \frac {\Delta H}{T ^ {2}}
$$

上式的左方是 $\left(\frac{\Delta G}{T}\right)$ 对 $T$ 的微分, 所以

$$
\left[ \frac {\partial \left(\frac {\Delta G}{T}\right)}{\partial T} \right] _ {p} = - \frac {\Delta H}{T ^ {2}}\tag{3.75}
$$

式 (3.74) 和式 (3.75) 称为 Gibbs-Helmholtz 方程。

对式 $(3.75)$ 进行移项积分, 有

$$
\int \mathrm{d} \left(\frac {\Delta G}{T}\right) _ {p} = \int - \frac {\Delta H}{T ^ {2}} \mathrm{d} T
$$

若作不定积分, 则得

$$
\frac {\Delta G}{T} = - \int \frac {\Delta H}{T ^ {2}} \mathrm{d} T + I\tag{3.76}
$$

式中 I 为积分常数。

根据基本公式 $\mathrm{d}A = -S\mathrm{d}T - p\mathrm{d}V$ 和 $A = U - TS$ 的定义, 同样可以证明 (读者试自证之):

$$
\left[ \frac {\partial (\Delta A)}{\partial T} \right] _ {V} = \frac {\Delta A - \Delta U}{T}\tag{3.77}
$$

$$
\left[ \frac {\partial \left(\frac {\Delta A}{T}\right)}{\partial T} \right] _ {V} = - \frac {\Delta U}{T ^ {2}}\tag{3.78}
$$

式 (3.74)～式 (3.78) 均称为 Gibbs-Helmholtz 方程。

根据式 (3.75)，在等压下若已知任一反应在 $T_{1}$ 的 $\Delta_{\mathrm{r}}G_{\mathrm{m}}(T_{1})$ ，则可求得该反应在 $T_{2}$ 时的 $\Delta_{\mathrm{r}}G_{\mathrm{m}}(T_{2})$ 。在使用式 (3.75) 时，需先知道 $\Delta H$ 随温度的变化关系。

$C_{p}$ 一般可以写为温度的函数, 即

$$
C _ {p} = a + b T + c T ^ {2} + \dots
$$

产物与反应物的等压热容之差为

$$
\Delta C _ {p} = \Delta a + \Delta b T + \Delta c T ^ {2} + \dots
$$

所以

$$
\begin{array}{r l} \Delta H & = \int \Delta C _ {p} \mathrm{d} T + \Delta H _ {0} \\ & = \Delta H _ {0} + \int (\Delta a + \Delta b T + \Delta c T ^ {2} + \dots) \mathrm{d} T \\ & = \Delta H _ {0} + \Delta a T + \frac {1}{2} \Delta b T ^ {2} + \frac {1}{3} \Delta c T ^ {3} + \dots \end{array}\tag{3.79}
$$

式中 $\Delta H_{0}$ 是积分常数。代入式 (3.75)，得

$$
\begin{array}{r l} \left[ \frac {\partial \left(\frac {\Delta G}{T}\right)}{\partial T} \right] _ {p} & = \frac {- \Delta H}{T ^ {2}} \\ & = \frac {- \Delta H _ {0} - \Delta a T - \frac {1}{2} \Delta b T ^ {2} - \frac {1}{3} \Delta c T ^ {3} - \cdots}{T ^ {2}} \end{array}
$$

移项积分, 得

$$
\left(\frac {\Delta G}{T}\right) = \frac {\Delta H _ {0}}{T} - \Delta a \ln T - \frac {1}{2} \Delta b T - \frac {1}{6} \Delta c T ^ {2} + \dots + I\tag{3.80}
$$

I 是另一个积分常数。

上式也可写为

$$
\Delta G = \Delta H _ {0} - \Delta a T \ln T - \frac {1}{2} \Delta b T ^ {2} - \frac {1}{6} \Delta c T ^ {3} + \dots + I T\tag{3.81}
$$

根据热化学中 $C_{p}$ 与 T 的关系, 从某一温度下的反应焓变, 由式 (3.79) 先求得积分常数 $\Delta H_{0}$ , 然后可求得其他温度下的焓变值。如果又已知该反应在某一温度下的 $\Delta_{r}G_{m}$ 值, 则可以用式 (3.80) 或式 (3.81) 求出积分常数 I, 从而可以计算其他温度下的 $\Delta_{r}G_{m}(T)$ 值。

## 例3.10

氨的合成反应可表示为 $\frac{1}{2}\mathrm{N}_{2}(\mathrm{g})+\frac{3}{2}\mathrm{H}_{2}(\mathrm{g})=\mathrm{NH}_{3}(\mathrm{g})$ ，在 298 K 和各气体均处于标准压力时，已知该反应在 298 K 时的 $\Delta_{r}H_{m}^{\ominus}=-45.9\ kJ\cdot mol^{-1},\quad\Delta_{r}G_{m}^{\ominus}=-16.4\ kJ\cdot mol^{-1}$ ，试求 1000 K 时 $\Delta_{r}G_{m}^{\ominus}$ 的值。

解 查表得

<table><tr><td></td><td> $a/(J \cdot mol^{-1} \cdot K^{-1})$ </td><td> $b/(10^{-3} J \cdot mol^{-1} \cdot K^{-1})$ </td><td> $c/(10^{-5} J \cdot mol^{-1} \cdot K^{-1})$ </td></tr><tr><td> $N_{2}$ </td><td>27.313</td><td>5.2</td><td>-0.002</td></tr><tr><td> $H_{2}$ </td><td>28.948</td><td>0.6</td><td>2</td></tr><tr><td> $NH_{3}$ </td><td>24.192</td><td>40.1</td><td>-8</td></tr></table>

$$
\Delta a = - 3 2. 8 8 6 5 \quad \Delta b = 3. 8 4 \times 1 0 ^ {- 2} \quad \Delta c = - 1. 0 9 9 9 \times 1 0 ^ {- 5}
$$

所以

$$
\begin{array}{r l} \Delta C _ {p} & = [ - 3 2. 8 8 6 5 + 3. 8 4 \times 1 0 ^ {- 2} T / \mathrm{K} - 1. 0 9 9 9 \times 1 0 ^ {- 5} (T / \mathrm{K}) ^ {2} ] \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{K} ^ {- 1} \\ & \quad \Delta_ {\mathrm{r}} H _ {\mathrm{m}} = \int \Delta C _ {p} \mathrm{d} T + \Delta H _ {0} \end{array}
$$

代入 298 K 时的 $\Delta_{r}H_{m}$ 求 $\Delta H_{0}$ 。

$$
\begin{array}{r l} - 4 5. 9 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1} & = \left[ \Delta H _ {0} - 3 2. 8 8 6 5 T / \mathrm{K} + \frac {1}{2} \times 3. 8 4 \times 1 0 ^ {- 2} (T / \mathrm{K}) ^ {2} - \right. \\ & \left. \frac {1}{3} \times 1. 0 9 9 9 \times 1 0 ^ {- 5} (T / \mathrm{K}) ^ {3} \right] \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{K} ^ {- 1} \end{array}
$$

将 $T = 298\mathrm{K}$ 代入, 得

$$
\Delta H _ {0} = - 3 7. 7 0 8 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

所以

$$
\begin{array}{r l} \Delta_ {\mathrm{r}} H _ {\mathrm{m}} ^ {\ominus} (T) & = [ - 3 7 7 0 8 - 3 2. 8 8 6 5 T / \mathrm{K} + 1. 9 2 \times 1 0 ^ {- 2} (T / \mathrm{K}) ^ {2} \\ & - 3. 6 6 6 3 \times 1 0 ^ {- 6} (T / \mathrm{K}) ^ {3} ] \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{K} ^ {- 1} \end{array}
$$

将 $\Delta H_{0}$ 代入 Gibbs-Helmholtz 方程的积分式 (3.81), 得

$$
\begin{array}{r l} \Delta_ {\mathrm{r}} G _ {\mathrm{m}} = & [ - 3 7 7 0 8 + 3 2. 8 8 6 (T / \mathrm{K}) \ln (T / \mathrm{K}) - 1. 9 2 \times 1 0 ^ {- 2} (T / \mathrm{K}) ^ {2} + \\ & 1. 8 3 3 1 5 \times 1 0 ^ {- 6} (T / \mathrm{K}) ^ {3} ] \mathrm{J} \cdot \mathrm{mol} ^ {- 1} + I T \end{array}
$$

将 $T = 298\mathrm{K},\Delta_{\mathrm{r}}G_{\mathrm{m}}^{\ominus} = -16.4\mathrm{kJ}\cdot \mathrm{mol}^{-1}$ 代入，得

$$
I = - 1 1 0. 2 9 \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{K} ^ {- 1}
$$

所以

$$
\begin{array}{r l} \Delta_ {\mathrm{r}} G _ {\mathrm{m}} ^ {\ominus} (T) = & [ - 3 7 7 0 8 + 3 2. 8 8 6 (T / \mathrm{K}) \ln (T / \mathrm{K}) - 1. 9 2 \times 1 0 ^ {- 2} (T / \mathrm{K}) ^ {2} + \\ & 1. 8 3 3 1 5 \times 1 0 ^ {- 6} (T / \mathrm{K}) ^ {3} - 1 1 0. 2 9 T / \mathrm{K} ] \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \end{array}
$$

当 $T = 1000\mathrm{K}$ 时，代入上式，求得

$$
\Delta_ {\mathrm{r}} G _ {\mathrm{m}} ^ {\ominus} (1 0 0 0 \mathrm{K}) = 6 1. 8 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

这个结论说明, 在所给定的条件下, 在 298 K 时, 合成氨的反应是可能的, 而在 1000 K 时反应不能自发进行。

Gibbs 自由能与压力的关系

$$
\mathrm{从} \mathrm{d} G = - S \mathrm{d} T + V \mathrm{d} p \text {得}
$$

$$
\left(\frac {\partial G}{\partial p}\right) _ {T} = V\tag{3.82}
$$

移项积分, 得

$$
G (p _ {2}, T) - G (p _ {1}, T) = \int_ {p _ {1}} ^ {p _ {2}} V \mathrm{d} p
$$

把温度为 T, 压力为标准压力 (100 kPa) 时的纯物质选为标准态, 其 Gibbs 自由能用符号 $G^{\ominus}$ 表示, 则压力为 p 时的 Gibbs 自由能 $G(p,T)$ 为

$$
G (p, T) = G ^ {\ominus} \left(p ^ {\ominus}, T\right) + \int_ {p ^ {\ominus}} ^ {p} V \mathrm{d} p\tag{3.83}
$$

对于理想气体, 有

$$
G (p, T) = G ^ {\ominus} (p ^ {\ominus}, T) + n R T \ln \frac {p}{p ^ {\ominus}}
$$

## 例3.11

1 mol Hg(l) 在 298 K 时从 100 kPa 加压到 10100 kPa, 求 Gibbs 自由能的变化值。已知 Hg(l) 的密度 $\rho = 13.5 \times 10^{3} \, kg \cdot m^{-3}$ ，并设 $\rho$ 不随压力而变；Hg(l) 的摩尔质量 $M(\mathrm{Hg}) = 200.6 \times 10^{-3} \, \mathrm{kg} \cdot \mathrm{mol}^{-1}$ 。

解

$$
\begin{array}{r l} & V _ {\mathrm{m}} = \frac {M}{\rho} = \frac {2 0 0 . 6 \times 1 0 ^ {- 3} \mathrm{kg} \cdot \mathrm{mol} ^ {- 1}}{1 3 . 5 \times 1 0 ^ {3} \mathrm{kg} \cdot \mathrm{m} ^ {- 3}} = 1. 4 9 \times 1 0 ^ {- 5} \mathrm{m} ^ {3} \cdot \mathrm{mol} ^ {- 1} \\ & \Delta G = \int_ {p ^ {\ominus}} ^ {p} n V _ {\mathrm{m}} \mathrm{d} p = n \int_ {1 0 0 \mathrm{kPa}} ^ {1 0 1 0 0 \mathrm{kPa}} \frac {M}{\rho} \mathrm{d} p \\ & = 1 \mathrm{mol} \times 1. 4 9 \times 1 0 ^ {- 5} \mathrm{m} ^ {3} \cdot \mathrm{mol} ^ {- 1} \times (1 0 1 0 0 - 1 0 0) \mathrm{kPa} = 1 4 9 \mathrm{J} \end{array}
$$

## 3.14 热力学第三定律与规定熵

五个热力学函数 $(U, H, S, A, G)$ 的绝对值都是不知道的。在用以判断变化方向准则的几个判据中，熵判据是最根本的，因为所有的不等号都来源于熵判据的不等号。如果我们知道各种物质的熵的绝对值，并把它们列表备查，则求 $\Delta S$ 就很方便了，但实际上熵的绝对值也是不知道的。热力学第二定律只能告诉我们如何测量熵的变化值，但不能提供熵的绝对值。我们只能人为规定一些参考点作为零点，来求其相对值。这些相对值就称为规定熵（conventional entropy），其目的是便于计算 $\Delta S$ 。

零点在哪里呢？这就是热力学第三定律所要解决的问题。它是在非常低的温度下研究凝聚系统的熵变所外推出来的结果。

## 热力学第三定律

![](物理化学上（第六版）傅献彩等z-library.sk,1lib.sk,z-lib.sk_200-399_images/da7ca24ace5670e0e1a89107a8740153e92416b9a06f0e6972905441e274473a.jpg)  
图 3.12 凝聚系统的 $\Delta H$ 和 $\Delta G$ 与温度的关系 (示意图)

1902 年, T. W. Richard 研究了一些低温下电池反应的 $\Delta H$ 和 $\Delta G$ 与温度的关系, 发现当温度逐渐降低时, $\Delta H$ 与 $\Delta G$ 有趋于相等的趋势 (如图 3.12 所示)。可用公式表示为

$$
\lim _ {T \to 0 \mathrm{K}} (\Delta G - \Delta H) = 0\tag{3.84}
$$

根据公式 $\Delta G - \Delta H = -T\Delta S,$ 即使 $\Delta S \neq 0,$ 当 $T \to 0 K$ 时, 式 (3.84) 仍然成立。而根据

$$
\frac {\Delta G - \Delta H}{T} = - \Delta S = \frac {\partial (\Delta G)}{\partial T}\tag{3.85}
$$

当 $T \rightarrow 0 \, K$ 时, 上式成为 0/0, 这是一个不定式, 从数学上讲 $\Delta S$ 或 $\frac{\partial(\Delta G)}{\partial T}$ 应都没有确定的数值。

1906 年, H. W. Nernst 系统地研究了低温下凝聚系统的化学反应, 提出一个假定: 当温度趋于 0 K 时, 在等温过程中凝聚态反应系统的熵不变。即

$$
\lim _ {T \rightarrow 0 \mathrm{K}} \left(- \frac {\partial \Delta G}{\partial T}\right) _ {p} = \lim _ {T \rightarrow 0 \mathrm{K}} (\Delta S) _ {T} = 0\tag{3.86}
$$

这个假定的根据是, 从实验数据及 $\Delta H - T, \Delta G - T$ 的图形 (见图 3.12), 合理地推想在 $T \to 0\mathrm{K}$ 时, $\Delta H$ 与 $\Delta G$ 有公共的切线, 并且该切线与温度的坐标平行。这就是说在 $T \to 0\mathrm{K}$ 时, 非但 $\Delta H$ 与 $\Delta G$ 趋于一致, 并且 $\frac{\partial \Delta G}{\partial T}$ 与 $\frac{\partial \Delta H}{\partial T}$ 也趋于一致。前已指出, 当 $T \to 0\mathrm{K}$ 时, 式 (3.85) 成为不定式, 根据数学上的运算规则, 可以取分子和分母的微分, 即

$$
\begin{array}{r l} \left(\frac {\partial \Delta G}{\partial T}\right) _ {T \to 0 \mathrm{K}} & = \frac {\left(\frac {\partial \Delta G}{\partial T}\right) _ {T \to 0 \mathrm{K}} - \left(\frac {\partial \Delta H}{\partial T}\right) _ {T \to 0 \mathrm{K}}}{\left(\frac {\partial T}{\partial T}\right) _ {T \to 0 \mathrm{K}}} \\ & = \left(\frac {\partial \Delta G}{\partial T}\right) _ {T \to 0 \mathrm{K}} - \left(\frac {\partial \Delta H}{\partial T}\right) _ {T \to 0 \mathrm{K}} = 0 \end{array}
$$

因此, 式 (3.86) 是可以成立的。式 (3.86) 通常被称为 Nernst 热定理 (Nernst heat theorem)。用文字表述则为, 在温度趋于热力学温度 $0 \mathrm{~K}$ 的等温过程中, 系统的熵值不变。或者说当温度接近 $0 \mathrm{~K}$ 时, 任何处于平衡态系统的熵不变。也就是说 $T = 0 \mathrm{~K}$ 时的等温过程也是绝热过程, 即 $0 \mathrm{~K}$ 时的等温线与绝热线重合, 系统处于一种非常特殊的状态。但 Nernst 并没有明确提出 0 K 时纯物质的熵的绝对值是多少。

M. Planck 在 1912 年把热定理推进了一步, 他假定 0 K 时, 纯凝聚态的熵值等于零, 即

$$
\lim _ {T \to 0 \mathrm{K}} S = 0\tag{3.87}
$$

承认 Planck 的假定, 则热定理就成为必然的结果了。其实这是一个基态的选择问题, 正如由标准摩尔生成焓计算标准摩尔反应焓变一样。在 0 K 时, 反应物和产物都是由相同种类相同数目的单质所构成 (用通俗的比喻, 反应物和产物站在同一起跑线上)。对于这些基态, 其熵的数值如何选择都不会影响反应的 $\Delta S$ 的计算结果。当然, 最简单的选择是, 假定 0 K 时任一物质的熵等于零, 这也符合 Boltzmann 公式 $S = k_{B} \ln \Omega$ 。0 K 时物质已成为凝聚态, 内部的质点整齐排列, 混乱度必极小。

Lewis 和 Gibson 在 1920 年对式 (3.87) 重新作了界定, 指出式 (3.87) 的假定适用于完整的晶体。所谓完整晶体即晶体中的原子或分子只有一种有序排列形式 (例如 NO 可以有 NO 和 ON 两种排列形式, 所以不能认为是完整晶体, $N_{2}O$ 和 CO 也是如此)。至此, 热力学第三定律可以表示为, 在 0 K 时, 任何完整晶体的熵等于零。这个定律是概括了一些低温现象的实验事实而提出来的。

规定熵值

已知 $\mathrm{d}S = \frac{C_p\mathrm{d}T}{T}$ ，现从 $0\mathrm{K}\rightarrow T$ 积分，得

$$
S _ {T} = S _ {0 \mathrm{K}} + \int_ {0 \mathrm{K}} ^ {T} \frac {C _ {p} \mathrm{d} T}{T}\tag{3.88}
$$

![](物理化学上（第六版）傅献彩等z-library.sk,1lib.sk,z-lib.sk_200-399_images/a1a91ecd4678319a8c9ff0fd077cdd73033f7fe69e425c0f36da6e8fb12bb934.jpg)  
图 3.13 从图解积分求熵值

根据第三定律, $S_{0K}=0$ ,所以物质的熵值可由下式计算:

$$
S = \int_ {0 \mathrm{K}} ^ {T} \frac {C _ {p}}{T} \mathrm{d} T = \int_ {0 \mathrm{K}} ^ {T} C _ {p} \mathrm{d} \ln T\tag{3.89}
$$

测定各温度时的 $C_{p}$ ，以 $\frac{C_{p}}{T}$ 为纵坐标，T 为横坐标，作图解积分。图 3.13 阴影区的面积就是某物质在 40 K 时的熵值。这样求出来的熵值，就称为该物质的规定熵。也可以以 $C_{p}$ 为纵坐标， $\lg T$ 为横坐标，作图解积分，以求得熵值。

计算规定熵时, 通常必须考虑相变过程的熵变。设某物质从 0 K 升到温度为 T 的气态物质, 中间经过如下的过程:

$$
\begin{array}{r l} \mathrm{B(s)} & \xrightarrow {0 \mathrm{K} \to T _ {\mathrm{f}}} \mathrm{B(s)} \xleftarrow {T _ {\mathrm{f}}} \mathrm{B(l)} \xrightarrow {T _ {\mathrm{f}} \to T _ {\mathrm{b}}} \mathrm{B(l)} \xleftarrow {T _ {\mathrm{b}}} \mathrm{B(g)} \xrightarrow {T _ {\mathrm{b}} \to T} \mathrm{B(g)} \\ & \Delta S (T) = \Delta S (0 \mathrm{K}) + \int_ {0 \mathrm{K}} ^ {T _ {\mathrm{f}}} \frac {C _ {p} (\mathrm{s})}{T} \mathrm{d} T + \frac {\Delta_ {\mathrm{mel}} H}{T _ {\mathrm{f}}} + \\ & \int_ {T _ {\mathrm{f}}} ^ {T _ {\mathrm{b}}} \frac {C _ {p} (\mathrm{l})}{T} \mathrm{d} T + \frac {\Delta_ {\mathrm{vap}} H}{T _ {\mathrm{b}}} + \int_ {T _ {\mathrm{b}}} ^ {T} \frac {C _ {p} (\mathrm{g})}{T} \mathrm{d} T \end{array}\tag{3.90}
$$

即三个积分项加上两个相变熵, 即为所求的物质在温度 T 时的总熵值。由于在极低的温度范围内缺乏 $C_{p}$ 的数据, 故在极低的温度范围内可以用如下的 Debye (德拜) 公式来计算:

$$
C _ {V} = 1 9 4 3 \frac {T ^ {3}}{\theta^ {3}} (\theta \text {是物质的特性温度})\tag{3.91}
$$

在低温下 $C_p \approx C_V, \theta = \frac{h\nu}{k}$ , 式中 $\nu$ 是晶体中粒子的简正振动频率。

即在计算时, 从 $0 \mathrm{~K}$ 到 $T_{\mathrm{f}}$ 的 $\Delta S$ 常常需要拆成两项来计算:

$$
S = \Delta S (0 \mathrm{K} \rightarrow T ^ {\prime}) + \int_ {T ^ {\prime}} ^ {T _ {\mathrm{f}}} C _ {p} (\mathrm{s}) \mathrm{dln} T\tag{3.92}
$$

$T'$ 是在低温范围的某一温度, 在这个温度以下 $C_{p,m}$ 的数据难于测定, 须借助 Debye 公式来计算 $0\ K \sim T'$ 区间的熵值。

## 化学反应过程的熵变计算

任意物质 B 处在一定的 T, p 状态下的规定熵值 $S_{T}$ 可根据热力学第三定律进行计算。一些物质处于标准压力 $p^{\ominus}$ 和 298.15 K 时的摩尔熵值有表可查，部分列于附录中。我们可以根据这些熵值和物质的 $C_{p,m}$ 值及其状态方程式，来计算其在任意温度或压力下的熵值，从而可用来计算化学反应中的熵变。例如，在等压情况下，当温度改变时，有

$$
S ^ {\ominus} (T, p ^ {\ominus}) = S ^ {\ominus} (2 9 8. 1 5 \mathrm{K}, p ^ {\ominus}) + \int_ {2 9 8. 1 5 \mathrm{K}} ^ {T} \frac {C _ {p} \mathrm{d} T}{T}
$$

如果保持温度不变, 而改变压力, 根据 Maxwell 关系式:

$$
\left(\frac {\partial S}{\partial p}\right) _ {T} = - \left(\frac {\partial V}{\partial T}\right) _ {p}
$$

故得

$$
S (2 9 8. 1 5 \mathrm{K}, p) = S ^ {\ominus} (2 9 8. 1 5 \mathrm{K}, p ^ {\ominus}) + \int_ {p ^ {\ominus}} ^ {p} - \left(\frac {\partial V}{\partial T}\right) _ {p} \mathrm{d} p\tag{3.93}
$$

对任意的化学反应:

$$
0 = \sum_ {\mathrm{B}} \nu_ {\mathrm{B}} \mathrm{B}
$$

若化学反应是在标准压力 $p^{\ominus}$ 和温度为 298.15 K 时进行, 则

$$
\Delta_ {\mathrm{r}} S _ {\mathrm{m}} ^ {\ominus} (2 9 8. 1 5 \mathrm{K}) = \sum_ {\mathrm{B}} \nu_ {\mathrm{B}} S _ {\mathrm{m}} ^ {\ominus} (\mathrm{B}, 2 9 8. 1 5 \mathrm{K})\tag{3.94}
$$

如果在压力为 $p^{\ominus}$ 时, 要计算任意温度下化学反应的熵变, 则

$$
\Delta_ {\mathrm{r}} S _ {\mathrm{m}} ^ {\ominus} (T) = \Delta_ {\mathrm{r}} S _ {\mathrm{m}} ^ {\ominus} (2 9 8. 1 5 \mathrm{K}) + \int_ {2 9 8. 1 5 \mathrm{K}} ^ {T} \frac {\sum_ {\mathrm{B}} \nu_ {\mathrm{B}} C _ {p , \mathrm{m}} (\mathrm{B}) \mathrm{d} T}{T}\tag{3.95}
$$

## 例3.12

计算下述化学反应在标准压力 $p^{\ominus}$ 下, 分别在 298.15 K 及 398.15 K 时的熵变。设在该温度区间内各 $C_{p,m}$ 值是与 T 无关的常数。

$$
\mathrm{C} _ {2} \mathrm{H} _ {2} (\mathrm{g}, p ^ {\ominus}) + 2 \mathrm{H} _ {2} (\mathrm{g}, p ^ {\ominus}) = \mathrm{C} _ {2} \mathrm{H} _ {6} (\mathrm{g}, p ^ {\ominus})
$$

## 解 查附录表得

<table><tr><td></td><td> $S_{\mathrm{m}}^{\ominus}(298.15 \mathrm{~K})/(J \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1})$ </td><td> $C_{p,\mathrm{m}}(298.15 \mathrm{~K})/(J \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1})$ </td></tr><tr><td> $\mathrm{H}_{2}(\mathrm{g})$ </td><td>130.684</td><td>28.824</td></tr><tr><td> $\mathrm{C}_{2}\mathrm{H}_{2}(\mathrm{g})$ </td><td>200.9</td><td>44</td></tr><tr><td> $\mathrm{C}_{2}\mathrm{H}_{6}(\mathrm{g})$ </td><td>229.2</td><td>52.5</td></tr></table>

当反应在 298.15 K 进行时, 有

$$
\begin{array}{r l} \Delta_ {\mathrm{r}} S _ {\mathrm{m}} ^ {\ominus} (2 9 8. 1 5 \mathrm{K}) & = \sum_ {\mathrm{B}} \nu_ {\mathrm{B}} S _ {\mathrm{m}} ^ {\ominus} (\mathrm{B}, 2 9 8. 1 5 \mathrm{K}) \\ & = S _ {\mathrm{m}} ^ {\ominus} [ \mathrm{C} _ {2} \mathrm{H} _ {6} (\mathrm{g}, 2 9 8. 1 5 \mathrm{K}) ] - 2 S _ {\mathrm{m}} ^ {\ominus} [ \mathrm{H} _ {2} (\mathrm{g}, 2 9 8. 1 5 \mathrm{K}) ] - S _ {\mathrm{m}} ^ {\ominus} [ \mathrm{C} _ {2} \mathrm{H} _ {2} (\mathrm{g}, 2 9 8. 1 5 \mathrm{K}) ] \\ & = (2 2 9. 2 - 2 \times 1 3 0. 6 8 4 - 2 0 0. 9) \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{K} ^ {- 1} \\ & = - 2 3 3. 1 \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{K} ^ {- 1} \end{array}
$$

当反应在 398.15 K 进行时, 有

$$
\begin{array}{r l} \Delta_ {\mathrm{r}} S _ {\mathrm{m}} ^ {\ominus} (3 9 8. 1 5 \mathrm{K}) & = \Delta_ {\mathrm{r}} S _ {\mathrm{m}} ^ {\ominus} (2 9 8. 1 5 \mathrm{K}) + \int_ {2 9 8. 1 5 \mathrm{K}} ^ {3 9 8. 1 5 \mathrm{K}} \frac {\sum_ {\mathrm{B}} \nu_ {\mathrm{B}} C _ {p , \mathrm{m}} (\mathrm{B}) \mathrm{d} T}{T} \\ & = \left[ - 2 3 3. 1 + (5 2. 5 - 2 \times 2 8. 8 2 4 - 4 4) \ln \frac {3 9 8 . 1 5}{2 9 8 . 1 5} \right] \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{K} ^ {- 1} \\ & = - 2 4 7. 3 \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{K} ^ {- 1} \end{array}
$$

## \*3.15 绝对零度不能达到原理——热力学第三定律的另一种表述法

1912 年, Nernst 根据他的 Nernst 热定理, 提出了 “绝对零度不能达到原理”, 即 “不可能用有限的手续使一个物体的温度冷到热力学温标的零度”。后来被认为是热力学第三定律的另一种表述法。

Nernst 热定理指出, 在接近 0 K 时, 任何过程中的熵值不变, 它既是等熵过程, 又是绝热过程, 没有热量的交换 (如果有热量交换, $\Delta S$ 就不等于零)。因此, 任何凝聚态物质在接近 0 K 时, 无论进行什么热力学过程, 都不能通过释放热量而降低温度。又由于是凝聚态物质, 也不能靠绝热膨胀对环境做功而降低温度。所以, 系统的温度不可能继续降低, 从而达不到绝对零度。

从 Nernst 热定理推出 “绝对零度不能达到原理”，还可以采取如下的证明。

为简单计, 假设系统的状态可用两个状态参量 $(T, x)$ 来描述 (x 可以是除 T 外的其他变量), 考虑当某一系统在温度为 $T_{1}$ 时的状态为 $\mathrm{A}(T_{1}, x_{1})$ , 则根据熵的表示式, 有

$$
S _ {\mathrm{A}} = S (T _ {1}, x _ {1}) = S (0 \mathrm{K}, x _ {1}) + \int_ {0 \mathrm{K}} ^ {T _ {1}} \frac {C _ {x , 1}}{T} \mathrm{d} T
$$

式中 $C_{x,1}$ 是状态参量 $x_{1}$ 不变情况下的热容。如果系统经绝热可逆过程变到状态 $\mathrm{B}(T_{2}, x_{2})$ ，其温度为 $T_{2}$ ，相应的热容也由 $C_{x,1}$ 变为 $C_{x,2}$ ，则状态 B 的熵为

$$
S _ {\mathrm{B}} = S (T _ {2}, x _ {2}) = S (0 \mathrm{K}, x _ {2}) + \int_ {0 \mathrm{K}} ^ {T _ {2}} \frac {C _ {x , 2}}{T} \mathrm{d} T
$$

在绝热可逆过程中, 系统的熵不变, 即 $S_{A} = S_{B}$ , 因此

$$
S (0 \mathrm{K}, x _ {1}) + \int_ {0 \mathrm{K}} ^ {T _ {1}} \frac {C _ {x , 1}}{T} \mathrm{d} T = S (0 \mathrm{K}, x _ {2}) + \int_ {0 \mathrm{K}} ^ {T _ {2}} \frac {C _ {x , 2}}{T} \mathrm{d} T
$$

根据 Nernst 热定理, $S(0\ \mathrm{K}, x_{1}) = S(0\ \mathrm{K}, x_{2})$ , 所以

$$
\int_ {0 \mathrm{K}} ^ {T _ {1}} \frac {C _ {x , 1}}{T} \mathrm{d} T = \int_ {0 \mathrm{K}} ^ {T _ {2}} \frac {C _ {x , 2}}{T} \mathrm{d} T
$$

当 T > 0 时, $C_{x} > 0$ (例如, 实验发现, $C_{V}, C_{p}$ 均大于零), 所以上式左侧 (起始状态) 的积分值总大于零, 由此推测右方的 $T_{2}$ 不可能等于零。也就是说, 不论起始的温度 $T_{1}$ 有多么低, 只要 $T_{1} > 0$ , 等式右方就有一定的正值, 则 $T_{2}$ 就不能等于零。这表明 “不可能用为数有限的手续, 把任何物体的温度降到 0 K”, 这就是热力学第三定律的另一种表述法, 且曾被认为是一种标准的表达方式。于是, 热力学第一定律、第二定律和第三定律这三个定律在表达方式上就有了相同之处, 即都说的是某种不可能做到的事, 都是从负面的角度来表达的。其不同之处是, 热力学第一定律、第二定律确切地告诉人们应放弃第一类和第二类永动机的制作, 那是不可能的事, 而热力学第三定律却不排斥人们想方设法尽可能去接近 $0 \mathrm{~K}$ 温度 (注意, 这里用的是 “接近”, 而不是 “达到”), 现实情况正是如此 (根据有关文献报道, 在当代最先进的实验室里能达到的最低温度约为 $10^{-14} \mathrm{~K}$ 量级, 最高温度约为 $10^{12} \mathrm{~K}$ 量级)。

曾经有人认为热力学第三定律不是一个独立的定律, 而是热力学第二定律的推论。他们认为, 根据 Carnot 定理, 工作于 $T_{h}$ 和 $T_{c}$ 两个热源之间的任何可逆热机, 其效率最大, 即

$$
\eta = 1 + \frac {Q _ {\mathrm{c}}}{Q _ {\mathrm{h}}} = 1 - \frac {T _ {\mathrm{c}}}{T _ {\mathrm{h}}}
$$

当向低温热源放出的热 $Q_{\mathrm{c}} \rightarrow 0$ 时, $T_{\mathrm{c}}$ 也趋于 $0 \mathrm{~K}$ , 此时, $\eta = 1$ , 这意味着从单一的高温热源所吸的热全部转变为功, 这违反了热力学第二定律, 所以, $\eta$ 不能等于 1 。即低温热源的热力学温度 $T_{\mathrm{c}}$ 不能等于零。这种推论显然是一种不合理的遐想, 是一种过度的外推。事实上, 作为 Carnot 机中循环的工作物质, 在远离 $T_{\mathrm{c}} \rightarrow 0 \mathrm{~K}$ 之前, 早已不能工作了。这表明热力学第三定律是一个独立的定律, 而不是热力学第二定律的推论。

## \*3.16 不可逆过程热力学简介①

引言

热力学的发展经历了几个阶段, 每一阶段都有其突出的特点。第一阶段是平衡态热力学 (即经典热力学), 它主要研究在可逆过程中, 状态参数对封闭系统的影响, 它的主要基础是热力学第一定律和热力学第二定律。它根据物质结构和统计热力学的知识, 建立了平衡态统计热力学。这一阶段取得了许多成果, 在实际生产过程中曾经发挥并将继续发挥其作用。这个阶段经历了相当长的时间, 以百年计。第二阶段是把热力学的研究从平衡态推广到非平衡态的敞开系统，建立了不可逆过程热力学（或非平衡态热力学），它以近平衡态为研究对象，认为不可逆过程的发生是由于在广义力的推动下产生了广义流的结果，力和流的影响在近平衡态仍是线性的。在这一阶段有突出贡献的是 Onsagar 和 Prigogine 等人。第三阶段是 Prigogine 及其学派把不可逆过程热力学推广到远离平衡的状态，把不可逆过程热力学推广到非平衡非线性区，从而建立了非线性非平衡态热力学。第二阶段和第三阶段是交叉进行的，这两个阶段是当今热力学研究的前沿领域。

在本节以前的内容, 主要讨论的是平衡态或可逆过程热力学的问题, 对不可逆过程只是在始态和终态是平衡态的情况下, 根据热力学第二定律建立了一些热力学不等式, 借以判断过程进行的方向, 至于不可逆过程本身并未涉及。但是, 自然界进行的实际过程都是不可逆的, 所以有必要把热力学推广到近平衡态的非平衡的领域。非平衡态热力学是一门正在发展中的学科, 其完整性和系统性远逊于经典热力学。

根据非平衡态距离平衡态的远近, 把非平衡态分为近平衡态区和远平衡态区两类, 在这两个区所进行的相应的过程分别称为线性不可逆过程和非线性不可逆过程。我们只对近平衡区的线性不可逆过程作简单介绍。

经典热力学是以宏观现象所归纳出来的两个定律为基础而扩展出来的, 有高度的可靠性和普适性, 但它也有一定的局限性。它的局限性来源于它考虑问题的方法和研究方法。近代一些科学领域的研究方法, 通常是把研究对象越分越细, 而热力学的方法则与此相反, 它采取宏观的综合办法。它研究大量粒子 (或称之为基本结构单元) 所组合成的系统的宏观行为, 而不管它们的结构或服从于什么力学规律 (是经典力学还是量子力学)。它的结论不适用于少数粒子所构成的系统, 也不包含时间变量, 它所处理的对象是平衡系统或从一个平衡态过渡到另一个平衡态的过程, 而且限制在系统与环境之间不发生物质交换的封闭系统 (对于多相系统, 相与相之间可以有物质的交流, 但整个系统仍然是封闭的)。这些都构成了经典热力学的特点, 同时也反映出它的局限性。经典热力学认为: 系统总是自发地趋向于平衡, 趋向于无序。但是, 实际上趋向平衡、趋向无序并不是自然界的普遍规律。

经典热力学几乎都是对平衡态或连续的平衡态作研究, 它不研究过程中的传递现象。例如, 不研究单位表面的热流量、质量流量、电流量以及推动这些过程的力和流量之间的关系。因此, 经典热力学只能称为平衡态热力学或可逆过程热力学。

可逆过程是从许多程度不同的不可逆过程中建立起来的一个抽象概念,但它十分有用, 因为在可逆过程中可以做最大功。当我们将一个实际的不可逆过程与相应的可逆过程相比较时, 就知道如何去提高实际过程的效率。热力学函数都是状态函数, 其变化值对解决实际问题 (如工程设计等) 有重要作用, 而其变化值只有通过可逆过程才能计算。

经典热力学的建立至今已有一百多年的历史, 功莫大焉! 它深刻阐明了在平衡态下各种化学现象的规律, 确立了能量转换关系, 明确指出宏观过程的方向和极限, 为化工生产提供了理论基础。但经典热力学无法揭示实际的不可逆过程的内在规律。

不可逆过程热力学拓宽了经典热力学的研究范畴, 它包括有传递过程的系统 (研究系统的传递性质, 如导热系数、扩散系数等) 以及这些性质之间的联系。它的研究方法也有许多特点, 如描述系统的状态参数时, 需要考虑时间和空间的坐标。作为系统内部不可逆过程的特征, 并不仅仅是熵的增加, 而同时要考虑熵的增加速率。它的研究方法不是宏观的, 而是微观的。它处理问题是以局域平衡 (local equilibrium) 为基础的。

为了说明局域平衡, 先了解什么是弛豫过程。当平衡态稍有偏离时, 由于分子间的相互作用, 系统将向平衡态趋近, 这样由非平衡态自发地趋于平衡态的过程称为弛豫过程 (relaxation process), 弛豫过程所经历的时间称为弛豫时间 (relaxation time)。例如, 系统内部的温度由不一致趋于一致就是一个弛豫过程, 经历的时间就是弛豫时间。又如, 气体分子的速率分布可以偏离 Maxwell 分布, 温度或密度也可以瞬间偏离平衡分布, 从而又产生局域温度 (local temperature)、局域密度 (local density) 等概念。

## 局域平衡

经典热力学研究方法的主要优点在于它仅仅依靠几个热力学的基本定律, 以及它所导出的 U 和 S 两个函数, 并用物质的量 (n)、体积 (V)、压力 (p)、温度 (T) 等其中少数独立变量来描述系统的状态。而对于非平衡系统又将如何选择描述系统的状态呢? 对于一个非平衡系统, 例如气体的不可逆压缩过程, 系统可能是不均匀的, 难以对系统的压力给予明确的定义。如果我们抛开经典热力学所经常使用的那些变量, 另外定义出一套变量, 则这些变量之间的关系显然不能满足在平衡态时所满足的那些关系。这样就使问题变得更加复杂。

为了能继续采用经典热力学的一些变量和关系式, 并将其延伸到非平衡态, Brussel 学派的 Prigaogine 等人提出了局域平衡的假设 (assumption of local equilibrium)。

设想把所讨论的系统划分成许多体积很小的子系 (或称为体积元), 每个子系在宏观上看是足够小的, 小到它的性质可以用该体积内的某一点 (或某一点附近) 的性质来 “代表”, 即子系中内部的性质是均匀的。但所有的子系, 从微观上看它又是足够大的, 因为每个子系内部都包含有足够多的分子, 能满足统计处理的需要, 仍然可以看作一个宏观的热力学系统。子系统靠其内部粒子间的相互碰撞而达到平衡, 这样就系统整体而言, 它只是近平衡而不是平衡的。整个系统的热力学量是相应的子系统的热力学量之和, 对强度性质而言, 整个系统不是统一的数值, 这就是局域平衡的假设。有了这个假设, 平衡态热力学中有关熵等状态函数的关系就可以用到线性热力学中来了。这样, 就把一个非平衡态的不可逆过程化为许多局部平衡的子系统的问题来研究 (就像微积分中把一条曲线看作无数短直线段的组合一样)。

但是, 把一个非平衡态系统分解成许多具有平衡态性质的子系是有条件的, 即它必须满足:

$$
\tau \ll \Delta t \ll t
$$

式中 $\tau$ 是小子系的弛豫时间；t 是整个系统的弛豫时间； $\Delta t$ 是对系统的观察时间。意即在对系统观察时间的范围内，因整个系统的弛豫时间很长，看不出整个系统有什么变化，而小子系的弛豫时间很短，在这观察时间范围内可能已进行了很多次的变化，对小子系来说观察到的就是它的平均值。换言之，即在观察时间 $\Delta t$ 时，局域（即子系）已经变化很多次，可近似认为是处于平衡状态，而整个系统的状态是非平衡的。

于是, 从平衡态热力学中得到的一系列热力学关系式就可以推广应用到总体上处于非平衡态的系统。应该注意, 因为就整体来说系统处于非平衡态, 每个子系和它邻近的子系内的热力学量 (如温度、化学势等) 可能并不相同, 那些从平衡态热力学导出的热力学关系式仅仅适用于非平衡态系统中各局部小范围, 而不适用于整个非平衡态系统。

## 熵产生和熵流

为了说明力和流的关系, 先以封闭系统的热传导为例。如图 3.14 所示, 两个封闭相 a 和 b, 构成一个封闭系统。设各相内部维持均一的温度 $T^{a}$ 和 $T^{b}$ , 在两相界面处可发生热传导, 同时两相又分别与环境交换热量 (假定环境很大, 系统的温度不发生变化)。每相获得的热量可分为两部分: 一部分是系统内部通过界面 AB 所交换的热量 $\delta_{i}Q$ (下标 “i” 表示内部); 另一部分是系统与环境所交换的热量 $\delta_{e}Q$ (下标 “e” 表示外部)。

![](物理化学上（第六版）傅献彩等z-library.sk,1lib.sk,z-lib.sk_200-399_images/184472b3afda52791a5ef65458ab502645870cd646026872461f151adcefb94c.jpg)  
图 3.14 封闭系统的热传导

对 a 相来说, 获得的热量为

$$
\delta^ {a} Q = \delta_ {\mathrm{i}} ^ {a} Q + \delta_ {\mathrm{e}} ^ {a} Q\tag{3.96}
$$

对 b 相来说, 获得的热量为

$$
\delta^ {b} Q = \delta_ {\mathrm{i}} ^ {b} Q + \delta_ {\mathrm{e}} ^ {b} Q \quad (\text {其中} \delta_ {\mathrm{i}} ^ {a} Q = - \delta_ {\mathrm{i}} ^ {b} Q)\tag{3.97}
$$

由于 a, b 相内部温度是均匀的, 故有

$$
\mathrm{d} S = \mathrm{d} S ^ {a} + \mathrm{d} S ^ {b}\tag{3.98}
$$

式中

$$
\mathrm{d} S ^ {a} = \frac {\delta^ {a} Q}{T ^ {a}} \quad \mathrm{d} S ^ {b} = \frac {\delta^ {b} Q}{T ^ {b}}
$$

将式 (3.96) 和式 (3.97) 代入式 (3.98), 整理得

$$
\mathrm{d} S = \frac {\delta^ {a} Q}{T ^ {a}} + \frac {\delta^ {b} Q}{T ^ {b}} = \frac {\delta_ {\mathrm{e}} ^ {a} Q}{T ^ {a}} + \frac {\delta_ {\mathrm{e}} ^ {b} Q}{T ^ {b}} + \delta_ {\mathrm{i}} ^ {a} Q \left(\frac {1}{T ^ {a}} - \frac {1}{T ^ {b}}\right)\tag{3.99}
$$

令

$$
\mathrm {d_ {e} S = \frac {\delta_ {e} ^ {a} Q}{T^ {a}} + \frac {\delta_ {e} ^ {b} Q}{T^ {b}}} \quad \mathrm {d_ {i} S = \delta_ {i} ^ {a} Q\left(\frac {1}{T^ {a}} - \frac {1}{T^ {b}}\right)}\tag{3.100}
$$

则得

$$
\mathrm{d} S = \mathrm {d_ {e}} S + \mathrm {d_ {i}} S\tag{3.101}
$$

式 (3.101) 表明, 系统的熵变由两部分贡献而来, 一部分是由系统 $(a + b)$ 与环境交换热量而来的 $(\mathrm{d_e}S)$ , 另一部分是系统内部不可逆的热流而引起的熵变 $(\mathrm{d_i}S)$ , 后者称为熵产生 (entropy production)。

单位时间的熵产生称为熵产生率 ( $\sigma$ ):

$$
\sigma = \frac {\mathrm{d} _ {\mathrm{i}} S}{\mathrm{d} t} = \frac {\delta_ {\mathrm{i}} ^ {a} Q}{\mathrm{d} t} \left(\frac {1}{T ^ {a}} - \frac {1}{T ^ {b}}\right)\tag{3.102}
$$

如令

$$
J _ {\mathrm{h}} = \frac {\delta_ {\mathrm{i}} ^ {a} Q}{\mathrm{d} t}
$$

$$
X _ {\mathrm{h}} = \frac {1}{T ^ {a}} - \frac {1}{T ^ {b}}\tag{3.103}
$$

(3.104)

则式 (3.102) 可写作

$$
\sigma = \frac {\mathrm{d} _ {\mathrm{i}} S}{\mathrm{d} t} = J _ {\mathrm{h}} \cdot X _ {\mathrm{h}}\tag{3.105}
$$

式中下标“h”表示“热”。式(3.103)中 $\frac{\delta_{\mathrm{i}}^{a}Q}{\mathrm{d}t}$ 是热传导速率（即单位时间内热的流量），可通称为“流”或“通量”。对热传导来说，可用 $J_{\mathrm{h}}$ 表示。式(3.104)中$\frac{1}{T^{a}}-\frac{1}{T^{b}}$ 则决定热传导过程的方向和限度, 是推动不可逆过程走向平衡的 “力”。由式 (3.105) 可见, 熵产生率是 “力” 和 “流” 的乘积。

$$
\text { 当 } \delta_ {\mathrm{i}} ^ {a} Q > 0 \text { 时 }, T ^ {b} > T ^ {a}, \text { 即 } J _ {\mathrm{h}} > 0, X _ {\mathrm{h}} > 0
$$

$$
\text {当} \delta_ {\mathrm{i}} ^ {a} Q <   0 \text {时,} T ^ {b} <   T ^ {a}, \text {即} \qquad J _ {\mathrm{h}} <   0, X _ {\mathrm{h}} <   0
$$

$$
\text {当} \delta_ {\mathrm{i}} ^ {a} Q = 0 \text {时,} T ^ {b} = T ^ {a}, \text {即} \qquad J _ {\mathrm{h}} = 0, X _ {\mathrm{h}} = 0
$$

力和流总是同号的，并且熵产生率永远大于或等于零。

如把上述情况推广到敞开系统, 系统和环境之间既有能量交换也有物质交换。生物系统就是靠这样的交换以维持其生存的。我们把熵的变化如式 (3.101) 一样分为两部分: 一部分是由系统与外界环境间的相互作用而引起的 (即由物质和能量的交流而引起的), 这一部分熵变称为熵流 (entropy flux), 因与外部环境有关, 故仍用 $\mathrm{d_eS}$ 表示; 另一部分是由系统内部的不可逆过程产生的 (包括系统内部的扩散和化学反应等), 这部分熵变如前所述称为熵产生, 因这是敞开系统内部的变化, 故仍用 $\mathrm{d_iS}$ 表示。于是, 对敞开系统也有如下的关系式:

$$
\mathrm{d} S = \mathrm {d_ {e}} S + \mathrm {d_ {i}} S
$$

$d_{e}S$ 的值可大于零或小于零, 而 $d_{i}S$ 永远不会有负值, 当系统内经历可逆变化时为零, 而当系统内经历不可逆变化时则大于零, 即

$$
\mathrm{d} _ {\mathrm{i}} S \geqslant 0\tag{3.106}
$$

对于隔离系统, 系统和环境间没有任何物质和能量的交换, 同样没有熵的交流, 因而

$$
\mathrm{d} _ {\mathrm{e}} S = 0 \quad (\text {隔离系统})\tag{3.107}
$$

所以

$$
\mathrm{d} S _ {\mathrm{iso}} = \mathrm{d} _ {\mathrm{i}} S \geqslant 0 \quad (\text {隔离系统})\tag{3.108}
$$

式 (3.108) 正是热力学第二定律所采用的数学表达式, 并由此而被称为熵增加原理。对于封闭系统和敞开系统, 虽然式 (3.106) 仍然成立, 但由于 $\mathrm{d_e}S$ 没有确定的符号, 所以式 (3.108) 不适用于封闭系统或敞开系统。而式 (3.106) 则可适用于各种系统。所以, 热力学第二定律的最一般的数学表达式应该是式 (3.106), 而不是式 (3.108)。式 (3.106) 适用于宏观系统的任何一个部分。如果在系统中的同一区域内同时发生着两种不可逆过程, 如两类化学反应过程, 若用 $\mathrm{d_i}S(1)$ 代表第一过程引起的熵产生项, 用 $\mathrm{d_i}S(2)$ 代表第二种过程所引起的熵产生项, 而

$$
\begin{array}{l} \mathrm {d_ {i}} S (1) \geqslant 0 \quad \mathrm {d_ {i}} S (2) \leqslant 0 \\ \mathrm {d_ {i}} S = \mathrm {d_ {i}} S (1) + \mathrm {d_ {i}} S (2) \geqslant 0 \end{array}
$$

这种情况是可能的, 这便是不可逆过程之间的耦合。

将熵的改变分为 $d_{e}S$ 和 $d_{i}S$ 两项, 就能很容易区别隔离系统、封闭系统及敞开系统之间的差别。其差别表现在 $d_{e}S$ 项上。它包含着系统与环境之间有物质和能量交换所引起的影响。系统的熵是系统无序程度的量度, 熵越大, 越无序; 熵越小, 越有序。对于非平衡的敞开系统要出现有序的稳定状态, 则环境必须提供足够的负熵流才有可能。

对于一个正在成长的生物体, 基本上处于非平衡的稳定态 (正像一个流动系统的反应器一样, 物料有进有出, 反应器中不断进行着反应, 是非平衡的, 但整个反应器又处于稳定态)。在稳定态期间 $\Delta S \approx 0$ , 但由于体内发生化学反应、扩散、血液流动等不可逆过程, 所以熵产生 $d_{i}S > 0$ , 故必须有负熵流来抵消正的 $d_{i}S$ 。动物的食品中含有高度有序的低熵大分子, 如蛋白质、淀粉等, 在体内经过消化后, 排泄出较无序的高熵小分子; 摄入低熵而排出高熵, $d_{e}S$ 为负值, 这就相当于摄入了“负熵流”。

## 最小熵产生原理

根据热力学第二定律, 在隔离系统中, 系统是沿着熵增加的方向进行的。当系统的熵达到极大值时, 系统处于平衡状态, 达到最无序状态, 此时 $dS/dt = 0$ , 系统在宏观上的一切变化都停止进行。现在的问题是: 对于一个敞开系统, 它属于非平衡系统, 当系统处于近平衡区, 其变化遵从线性热力学的规律, 则它的熵又是如何变化的? 为说明这一问题, 先介绍稳定态的概念。

对于敞开系统, 由于系统与环境可以交换能量、物质和熵, 虽然系统内部的熵产生 $\mathrm{d_i}S > 0$ , 但系统可用外界所提供的负熵流而使系统的总熵值维持不变, 即 $\mathrm{d}S = \mathrm{d_i}S + \mathrm{d_e}S = 0$ , 这就是说虽然系统内部存在着不可逆过程, 但系统仍可以维持不变的低熵值, 也就是维持较为有序的稳定态。这个稳定态虽然不是最终的平衡态, 而是近平衡区中非平衡的稳定态, 我们把这种稳定态简称为定态 (steady state), 以区别于平衡态。稳定态与平衡态不同, 当系统处于平衡态时, 熵产生率为零, 从而系统没有宏观的输运过程。而对于处于非平衡定态的系统, 在系统内部稳定地进行着不可逆过程 (如热传导、扩散等), 此时系统的熵产生率 ( $\mathrm{d_i}S / \mathrm{dt}$ ) 最小, 但不等于零。如以 $p$ 代表熵产生率, 则有 $\mathrm{dp} / \mathrm{dt} \leqslant 0$ 。

图 3.15 示出了平衡态和线性区熵的变化情况。

最小熵产生原理表现在线性区, 系统因受扰动而暂时偏离定态, 但是最后仍回到相应于熵产生率最小的定态。所以, 线性区的定态是稳定的, 它具有接近平衡态的性质, 微小的干扰仍能在空间上和时间上维持原来的有序结构, 不会离开线性区。如果干扰过大, 系统将进入非线性区, 情况就完全不同, 干扰可能引起系

![](物理化学上（第六版）傅献彩等z-library.sk,1lib.sk,z-lib.sk_200-399_images/2f73154892160e55d6b027e5a1e169e45d4cbcc6f99663b004b1bdea572c0ab5.jpg)  
(a) 在平衡态熵随时间的变化

![](物理化学上（第六版）傅献彩等z-library.sk,1lib.sk,z-lib.sk_200-399_images/0495ad2a236bcc07fe97839de1da2beb1b830dfbf9cd7ff51d6aa359a4a5a976.jpg)  
(b) 在线性区熵产生率随时间的变化  
图 3.15 平衡态和线性区熵的变化情况

统较大的变化, 如产生新的有序结构等。

综上所述, 可知 $dp/dt \leqslant 0$ 的物理意义是, 线性非平衡区的系统随着时间的推移, 总是朝着熵产生率减少的方向进行, 直到一个定态。此时, 熵产生率不再随时间变化, $dp/dt = 0$ 。在线性非平衡区, 定态的熵产生达到极小值。Prigogine 于 1945 年提出, 把 $dp/dt \leqslant 0$ 称为 “最小熵产生原理”。 $dp/dt \leqslant 0$ 的作用, 保证了在线性非平衡区随着时间的推移, 系统总是趋向于定态。由于这种在线性区的规律作用, 系统在线性非平衡区就不可能出现新的时间或空间的有序结构 (例如, 耗散结构只能出现在远离平衡态的非线性区)。

Prigogine 因对非平衡不可逆过程热力学的贡献, 于 1977 年获诺贝尔化学奖。

限于本课程的基本要求, 也限于教材的篇幅, Prigogine 对这一问题的详细证明从略。

## Onsager 倒易关系

在系统内可能存在多种不可逆过程, 它们互有影响, 即一种 “力” 可产生多种 “流”, 一种 “流” 也可以对多种 “力” 产生影响。Onsager 研究了互为影响的关系, 指出这是一种耦合关系, 并推导出相关的关系式, 称为 Onsager 倒易关系式。

在不可逆过程中常把引起某种过程的原因称为该过程的“动力”，简称为力(或广义力)，用符号 X 表示。把在单位时间内通过系统单位面积的某种量称为该量的“流”(或广义流，流也代表流量)，用符号 J 表示，“流”是一个矢量。对于一般的输运过程，“力”和“流”的关系是线性关系，即

$$
J = L X\tag{3.109}
$$

式中 L 是不等于零的常数, 也称为唯象系数 (phenomenological coefficient)。式 (3.109) 是一种 “力” 和由它所引发的一种 “流” 之间的关系式。

热力学“力”可引起热力学的“流”。例如，温度梯度产生热量流，粒子浓度的梯度可引起物质的扩散流，它们分别形成热传导和扩散两种不可逆过程。其实各种不可逆过程间存在耦合(coupling)，即一种“力”可以引起多种“流”，一种“流”也可以是多种“力”所产生的效果。例如，在各向异性的晶体中，x方向的温度梯度不仅产生x方向的热量流，也可以引起y方向的热量流。又如，多组分系统中第i种组分的浓度梯度不仅产生第i种组分的粒子流，也可引起第j种组分的粒子流。温度梯度也可以引起粒子的扩散流。系统的浓度差不仅直接引起扩散流，而且可导致热量的流动。凡此种种，表明“力”和“流”之间具有交叉效应。为简单计，设一个在近平衡态所进行的过程，若同时存在两种流，如物质流动和热扩散，两个不可逆过程同时进行，令 $J_{1}, J_{2}$ 分别代表两种流， $X_{1}, X_{2}$ 分别代表两种力，并假定力和流的关系是线性的（对近平衡态的过程而言，这是合理的假定）。对于这两种力引发的过程，其速率方程可写为

$$
\begin{array}{l} J _ {1} = L _ {1 1} X _ {1} + L _ {1 2} X _ {2} \\ J _ {2} = L _ {2 1} X _ {1} + L _ {2 2} X _ {2} \end{array}\tag{3.110}
$$

假定 $J_{1}$ 是能量流, $X_{1}$ 是引发能量流的力 (即温度梯度), $J_{2}$ 是质量流, $X_{2}$ 是引发质量流的力 (即浓度梯度)。

从式 (3.110) 可以看出, 力和流是交叉的, 即一种流是由两种不同的力引发的。式中有四个唯象系数, 要解释它的物理意义是困难的。对于含有 $n$ 个流和力的速率方程, 则有

$$
\left. \begin{array}{c} J _ {1} = L _ {1 1} X _ {1} + L _ {1 2} X _ {2} + \dots + L _ {1 n} X _ {n} \\ J _ {2} = L _ {2 1} X _ {1} + L _ {2 2} X _ {2} + \dots + L _ {2 n} X _ {n} \\ \dots \dots \\ J _ {n} = L _ {n 1} X _ {1} + L _ {n 2} X _ {2} + \dots + L _ {n n} X _ {n} \end{array} \right\}\tag{3.111}
$$

Onsager 指出 $L_{jk}$ 间有如下的关系, 即

$$
L _ {j k} = L _ {k j}\tag{3.112}
$$

这个关系称为 Onsager 倒易关系 (Onsager reciprocal relation)。其物理意义是，第 j 个流 $J_{j}$ 与第 k 个力 $X_{k}$ 之间的比例常数 $L_{jk}$ 和第 k 个流 $J_{k}$ 与第 j 个力 $X_{j}$ 之间的比例常数 $L_{kj}$ 相等。

Onsager 从理论上论证了上述关系。Onsager 倒易关系是不可逆过程中一个基本关系。在式 (3.111) 中有很多唯象系数, 有了 Onsager 倒易关系后, 可以将唯象系数的个数减少一半, 对于求解不可逆过程的问题很有用。Onsager 因为此项研究成果对不可逆过程热力学作出重要贡献, 于 1968 年获诺贝尔化学奖。

## 耗散结构和自组织现象

处在线性区 (即近平衡区) 的非平衡系统与处在非线性区 (远平衡区) 的非平衡系统, 二者具有质的区别。前者系统随时间的变化趋于一个定态, 这个状态就是熵产生率最小的状态; 而后者系统的状态随时间的变化, 有可能建立一个有序结构, 即耗散结构 (dissipative structure)。

![](物理化学上（第六版）傅献彩等z-library.sk,1lib.sk,z-lib.sk_200-399_images/1846628c5982a607e7f90765404ad0a5c57ccb01b24db447b7f5e347ad18740c.jpg)  
图3.16 Bernard花样

为了说明耗散结构, 先举一个实例, 即 Bernard 的对流实验。在敞口的容器中放一薄层液体, 底部保持温度为 $T_{2}$ , 液体上部的温度为 $T_{1}, T_{2} > T_{1}$ , 热量将不断地通过液体从下部传到上部。当 $\Delta T (= T_{2} - T_{1})$ 较小时, 传热以导热的方式平稳进行, 液体从宏观上是静止的。但若增大上下温度的差别, 当差别大于某一极限值 $\Delta T_{c}$ (下标 c 代表 critical) 时, 液体发生突变, 变得不稳定, 出现对流, 并可发展成为排列非常整齐的六边形对流原胞 (convection cell), 如图 3.16 所示。

每个原胞中心液体向上流动, 边缘液体向下运动, 这

种规则的结构称为 Bernard 花样 (Bernard patten, 或称为 Bernard 图案)。Bernard 花样一旦形成, 只要 $\Delta T$ 保持不变, 即使系统受到微小的扰动, 不久系统仍能恢复到原来的花样, 这表示 Bernard 花样是稳定的。此时, 液体内亿万分子的运动步调非常一致, 整个液体各处都出现相同的对流原胞, 这表示花样的形成是一种高度有组织的自组织行为 (self-organization)。但如果 $\Delta T$ 继续增大, 则对流花样可发生多次分合。

从理论上来说, 这是一个系统的稳定性问题。在处于远离平衡的敞开系统中, 通过改变参量, 可使系统失稳, 并过渡到与原来定态结构完全不同的新的稳定态。这种建立在不稳定基础之上的新的有序稳定结构, 是依靠系统与外界交换物质与能量来维持的, 一旦供应停止, 这个耗散结构也必将终止 (有关稳定态的讨论, 涉及微分方程中的二级微商, 这里就不再讨论了)。

总之, 只有敞开系统远离平衡态时, 才可能出现耗散结构。耗散结构大大加深了人们对敞开系统中有序结构或自组织行为的认识。这个理论可应用于激光、化学反应、电子线路和生物体等。以生物体为例, 生物体不断地从外界摄入食物、水分及空气, 同时不断排泄废物, 这是一个敞开系统, 也是一个耗散结构, 它的形成和维持要靠不断地吸入负熵流, 并不断地进行自组织行为。

现代分子生物学表明, 每一个生物细胞中至少含有一个 DNA (脱氧核糖核酸) 或它的近亲 RNA (核糖核酸), 它们都是长链分子, 可能由 $10^{8} \sim 10^{10}$ 个原子组成, 先是由糖基 (s) 和磷酸基 (P) 交替组成两条长链, 然后由 4 种不同的核苷酸碱基 (即腺嘌呤、胸腺嘧啶、鸟嘌呤和胞嘧啶), 按不同的方式把两条长链连接起来, 形成一种双螺旋的结构。这是一个多么复杂神奇的结构, 而这种结构竟是由食物中那些混乱无序的原子所组成的, 整个从无序到有序的过程都是在生物体内进行的。

又如, 许多树叶、花朵、动物的皮毛乃至蝴蝶翅膀上的花纹等, 都呈现出美丽的颜色和规则的图案。生物有序不仅表现在空间的特点上, 也表现在时间的特点上。例如, 生物钟就是生物化学反应随时间而有规则地周期性振荡的结果。周期交替, 显然是一种有序现象。后来, 人们又发现无生命系统也有许多自发形成的宏观有序现象。例如, 水蒸气凝结成排列非常有序的雪花; 天空中的云有时呈现出鱼鳞状或条状的有序排列; 木星的大气层中有大规模的漩涡状有序结构; 有些有颜色变化的化学反应可以在两种不同的颜色之间做周期性的振荡 (化学振荡)。化学振荡也是耗散结构, 我们将在化学动力学一章予以讨论。

C. R. Darwin (达尔文) 1859 年出版了震动当时学术界的《物种起源》一书，指出地球上各种各样的生物都是经过漫长的时代由简单到复杂、由低级到高级进化而成的。如用现代的语言，就是由无序到有序，从有序到更加精确有序的发展过程。一些社会学家把这种概念延伸到人类社会的进化，也是逐渐由低级向更加完善更加有序的阶段发展。

综观热力学的发展过程, 大致是对热力学的研究从平衡区推广到非平衡区, 从平衡态热力学发展到线性热力学, 并得到一些新的理论, 这就是局域平衡、Onsager 倒易关系 (有时也称为 Onsager 定理) 以及最小熵产生原理等。然后, 从近平衡区的线性热力学再发展到远离平衡区的非线性热力学。在非线性区对系统微扰, 可以驱使系统离开不稳定的定态而进入一个新的稳定状态, 即耗散结构。有关耗散结构的形成机理及系统的涨落特性, 有待于非平衡统计物理学去完成。

## 混沌

混沌亦称作“浑沌”，这个词本是我国古人用以在开天辟地之前，对宇宙的形容，大概是一片模糊、混成一团不可分辨之意。这个词被近代科学工作者所借用，则另有其特殊意义。

如果我们把自然界物质的运动形态大致分为三种, 一种是遵从经典力学的规律, 呈有序的运动, 一种是彻底的随机性的混乱运动, 无章可循。混沌运动则是介于二者之间的有序的混乱, 即一种被限制在确定而且稳定的范围内的混乱运动, 此种运动且常具有不同周期性的特点, 这种状态就称为混沌 (chaos)。可以举一个

例子予以说明。

1967 年, 美国气象学家 Lorentz 建立了一个描述大气对流的数学模型, 称为 Lorentz 动力学方程, 共有三个公式, 即

$$
\begin{array}{l} \frac {\mathrm{d} x}{\mathrm{d} t} = \sigma (x - y) \\ \frac {\mathrm{d} y}{\mathrm{d} t} = - x z + \gamma x - y \\ \frac {\mathrm{d} z}{\mathrm{d} t} = x y - b z \end{array}
$$

式中 x, y, z 分别代表大气对流中的速度、温度和温度梯度，这三个量不含有任何随机项，故是确定性的。 $\sigma, \gamma$ 和 b 是三个控制参数，其初始值也可以给定，故也是确定性的。但是，由上述三个公式所描述的简单的确定性的系统，照理应该能够求解并确切地描述其运动轨迹，但实际上却出乎意料地出现了不可预测性，这个系统的运动轨迹描绘出一个奇特的形状，好像一个展开了双翅的蝴蝶（如图 3.17 所示）。

![](物理化学上（第六版）傅献彩等z-library.sk,1lib.sk,z-lib.sk_200-399_images/4c7c356f857e8ce3f20605e0a5e2f1dc4c878d25cf37107d4c1eb5311162a438.jpg)  
图3.17 Lorentz动力学方程的轨迹

在这个图形上, 确定性和随机性有机地结合在一起。一方面系统的轨迹以 $A, B$ 两点为中心缠绕着, 绝不会远离它们而去, 这是确定性的, 表明系统未来的轨迹被限制在一个明确的范围之内。另一方面, 运动的缠绕规则又是随机的, 轨迹绕 $A$ 若干圈后被甩到 $B$ 附近, 绕 $B$ 若干圈后, 又回到 $A$ 附近, 如此无穷往复。关键在于每次绕 $A$ 或 $B$ 的圈数和圈的大小都是随机的。这表明无法准确判定在某一时刻系统究竟是在 $A$ 圈还是在 $B$ 圈。于是, 不可预测性和随机性系统所具

(b) 高级分支现象

有的特性就出现在确定的系统之中。这种系统就被称为混沌系统。在混沌系统中，确定性和随机性并存，二者同时起着作用。这种状态只有在远离平衡的系统中才能出现。研究具有这种行为的热力学称为非线性非平衡态热力学，这是一门到目前为止还不很完善的学科，可以认为是热力学发展的第三阶段（前两个阶段是经典热力学和近平衡态不可逆过程热力学）。

这种混沌现象来源于状态的分支行为。

一般来说, 对远离平衡的定态, 其行为不能仅靠热力学的方法来确定, 同时还要研究系统的动力学行为。在图 3.18(a) 中, 横坐标 $x$ 代表外界对系统的控制参数 (如温度、压力等), 它的大小表示外界对系统影响的程度和系统偏离平衡的程度。纵坐标 $y$ 表征系统定态的某个参数, 不同的 $y$ 值表示不同的定态, 与 $x_0$ 对应的定态 $y_0$ 代表平衡态。随着 $x$ 的改变 (增加), 则 $y$ 也沿 $y_0$ 线段改变。曲线 (a) 是平衡态的延伸 (即近平衡定态), 其上的每一点所对应的状态的行为很类似于平衡态的行为 (如保持空间均匀性和时间不变性)。因此, 这一段叫作热力学分支。当 $x \geqslant x_c$ 时, 例如在 Bernard 流体加热实验中, 对流体加热的温度梯度超过某一定值时, 曲线 (a) 延长到 (b) 段。(b) 段代表远离平衡的非稳态, 较不稳定, 一个很小的扰动就可引起系统的突变, 离开 (b) 段, 而跃迁到另外两个稳定的分支 (c) 和 $(c')$ 段上。在分支上每一个点可能对应于某个时空有序状态而形成耗散结构, 所以 (c) 和 $(c')$ 段就称为耗散结构分支, 系统是在 $x_c$ 处发生分支现象 (或分岔现象)。

![](物理化学上（第六版）傅献彩等z-library.sk,1lib.sk,z-lib.sk_200-399_images/0527cae5c41faf011c473163266e15344a43d0911eebb1d90ecaf58ee55f2444.jpg)

![](物理化学上（第六版）傅献彩等z-library.sk,1lib.sk,z-lib.sk_200-399_images/996c993f34564da51e99af53bde37bb0ce20709dcec292c36380a3cbd2a586ce.jpg)  
图3.18 状态的分支行为

随着控制参数 x 的进一步改变 (增加), 各稳定分支又会变得不稳定而导致二级或更高级分支现象 [见图 3.18(b)]。高级分支现象表明, 系统在远离平衡态时分支越多, 有可能有多种可能的耗散结构, 系统究竟处于哪种耗散结构, 完全是随机的, 系统的瞬时状态不可预测, 这时系统又进入一种新的无序状态, 即混沌状态。

对于任何一个热力学系统, 由于系统内分子的无规则热运动, 系统的状态在局部上经常与宏观统计平均态有暂时的偏离。这种系统的各宏观平均值的瞬时值与平均值的偏差就称为涨落 (fluctuation)。对形成耗散结构和混沌状态来说, 涨落起了触发的作用。

## \*3.17 信息熵浅释

1864 年, Clausius 在热力学中引入了熵的概念 (也称为热力学熵或 Clausius 熵)。根据 Clausius 不等式, 可以判断自发不可逆过程进行的方向和限度, 并以熵达到最大值为准则。所以, 熵的数值可以表明系统接近平衡态的程度。1889 年, Boltzmann 把熵 (也称为 Boltzmann 熵) 与系统的微观状态数联系起来, 建立了 Boltzmann 关系式, 阐明了熵的统计意义, 把熵作为系统混乱度的量度。1948 年, C. E. Shannon 把 Boltzmann 熵的概念引入信息论中, 把熵 (称为信息熵或 Shannon 熵) 作为一个随机事件的不确定性或信息量的量度, 从而奠定了现代信息论的科学理论基础, 也促进了信息论的发展。信息熵是一个独立于热力学熵的概念, 但具有热力学熵的基本性质。信息或信息量是各行各业所需要的, 没有信息就会陷于盲目, 难以展开工作。从这个角度讲, 信息熵具有更广泛的实际意义。

什么是信息 (information)? 按通常的理解, 信息就是消息 (如实验数据、语言和文字资料、商业信息等, 其涵盖面极其广泛), 用信息论来量度信息的基本出发点, 是认为信息可以用来消除 “不确定性”。因此, 信息数量的多少可以用被清除的不确定性的多少来衡量。可以举如下的例子来说明信息和不确定性之间的关系。例如, 某人将一张扑克牌面朝下放在桌上, 要你猜是什么牌, 如果没有任何信息 (或提示), 则它可能是 52 张牌中的任何一张 (对这件事来说, 其不确定度最大)。如果告诉你是 “A”, 有了这个消息, 则可以断定它必定是 4 个 A 中的一张 (有了这个消息, 不确定性大大减少了)。如果又告知你这是一张黑桃 (又得到了一个信息), 则你就肯定知道这张牌是什么了 (其不确定性等于零)。所以, 增加信息量的效果就是减少情况的不确定性。

如何量度 (或衡量) 事件的不确定性呢?

设对某个事件进行探测或称为概率实验 (例如掷骰子或进行某个带有探索性的实验), 设它有 $n$ 个可能的结果出现, 即 $a_1, a_2, \cdots, a_n$ , 则每一个结果出现的概率分别为 $P_1, P_2, \cdots, P_n$ , 这些概率应满足 $0 \leqslant P_i \leqslant 1$ 及 $\sum_{i=1}^{n} P_i = 1 (i = 1, 2, \cdots, n)$ 的条件。显然, 可能的结果 $n$ 越大, 实验结果的不确定性也越大。所以, 实验的不确定度应是概率 $P_i$ 的单调上升函数。当其中某一个结果出现的概率 $P_i = 1$ 时, 则意味着这次实验只有这一个结果, 且是唯一的, 则这个实验没有悬念, 它的不确定度为零。

如果一个实验是由两个独立的事件 A 和 B 所组成的, 则构成一个复合实验 (例如, 同时掷两个骰子, 就相当于一个骰子掷两次的复合实验)。事件 A 的可能结果为 $P_{A}$ 个, 实验 B 的可能结果为 $P_{B}$ 个, 则复合事件的可能结果是 $P_{A}$ 和 $P_{B}$ 的乘积, 但复合实验的不确定度则是两个独立实验的不确定度之和。复合事件的不确定度是加和关系, 而复合事件的可能结果是相乘的关系, 这和熵与概率的关系有极其相似之处。

$$
\begin{array}{r l} & S _ {\mathrm{A}} = f (\varOmega_ {\mathrm{A}}) \qquad S _ {\mathrm{B}} = f (\varOmega_ {\mathrm{B}}) \\ & S = S _ {\mathrm{A}} + S _ {\mathrm{B}} = f (\varOmega) = f (\varOmega_ {\mathrm{A}}, \varOmega_ {\mathrm{B}}) \end{array}
$$

而

$$
f (\varOmega_ {\mathrm{A}}, \varOmega_ {\mathrm{B}}) \neq f (\varOmega_ {\mathrm{A}}) + f (\varOmega_ {\mathrm{B}})
$$

因此, 只有借助对数的关系把它们联系在一起, 即 $S = k \ln \Omega$ 。

由于概率实验带有不确定性, Shannon 根据热力学中熵的性质引入了另一个函数 $H_{n}$ , 即

$$
H _ {n} = H _ {n} (P _ {1}, P _ {2}, \dots , P _ {n}) = - k \sum_ {i = 1} ^ {n} P _ {i} \ln P _ {i}\tag{3.113}
$$

作为实验结果不确定性的量度, 式中 k 是大于零的常数, 所以 $H_{n} \geqslant 0$ , Shannon 称 $H_{n}$ 为信息熵 (或 Shannon 熵)。其意义是: 表示该实验结果的不确定性量度, 也是实验中所得到的信息量的量度。

如果把式中的常数选为 Boltzmann 常数 $k_{B}$ ，并且 S 表示系统的熵（有时也称为广义熵），则可得

$$
S = - k _ {\mathrm{B}} \sum_ {i = 1} ^ {n} P _ {i} \ln P _ {i}
$$

式中求和遍及系统所有的微观状态, 是统计物理学中最普遍的熵的表示式。

信息量越多, 不确定程度越少。所以, 信息量具有负熵的性质 (在一些专著中, 可以看到关于信息熵的详细论证, 本书只能作简要的定性说明)。

## Maxwell 妖与信息

1867 年, Maxwell 曾提出了一个设想, 用以对热力学第二定律进行挑战。他设想有一个能观察并分辨所有分子运动速度和轨迹的小精灵, 把守着装有气体的容器内隔板上一个小孔的闸门, 看到左边来的高速运动的分子, 就放开闸门让它到右边去, 看到右边来了低速运动的分子就打开闸门让它到左边去 (见图 3.19)。假定闸门是完全无摩擦力的, 于是小精灵无须做功, 就可以使高速运动的分子集中到右边, 低速运动的分子集中到左边, 其结果是左边的气体越来越冷, 右边的气体越来越热。冷者越冷, 热者越热, 这违反了热力学第二定律。人们把这个小精灵称为 Maxwell 妖 (Maxwell demon)。

![](物理化学上（第六版）傅献彩等z-library.sk,1lib.sk,z-lib.sk_200-399_images/8e8251912bdd0ee133fe3d823a44ee2e09fe3e64f8542b178561a5b60d902291.jpg)  
图 3.19 Maxwell 妖示意图

当时这一问题曾引起了热烈的讨论, 但都没得到圆满的结论。直到 1929 年, 匈牙利物理学家 L. Szilard 才有了满意的解答。他认为 Maxwell 妖具有非凡的分辨能力, 具有智慧, 他了解每一个分子运动速度的信息。为此, 他可能需要利用一个微光学系统去照亮分子, 以获取每个分子的运动信息, 然后通过大脑的活动, 去识别干扰它们, 这就需要耗费一定的能量, 并产生额外的熵。Maxwell 妖就以此为代价来获得分子运动的信息, 他依靠信息来干预系统, 使它逆着自然界的自发方向进行。其实, 有了 Maxwell 妖的存在, 系统就成为敞开系统, 他将负熵输入系统, 降低了系统的熵。因此, 从整体上看, 气体分子的反向集中并不违反热力学第二定律。从信息论的观点看, 信息就是负熵, Maxwell 所提出的设想实际上是负熵的引入。

## 拓展学习资源

<table><tr><td>重点内容及公式总结</td><td><img src="images/aca1c80b9f2b7957eda94f4f2329e15f8204ccf55845e5f7aa89d78ca37562a5.jpg"/></td></tr><tr><td>课外参考读物</td><td><img src="images/c7330b1778f9867e0e77c39e3ee8579c0a2a336de6d2972fbd406de7aa89aa0e.jpg"/></td></tr><tr><td>相关科学家简介</td><td><img src="images/f319c6c052be8f3e243762240d5246794d5f75664cc770e1e3783f36c7f0413d.jpg"/></td></tr><tr><td>教学课件</td><td><img src="images/9c55daced7ebe979649f97740a581ec58611657d25c0bd51eb5a5a57612d0375.jpg"/></td></tr></table>

## 复习题

3.1 指出下列公式的适用范围。

(1) $\Delta_{\mathrm{mix}}S = -R\sum_{\mathrm{B}}n_{\mathrm{B}}\ln x_{\mathrm{B}};$

(2) $\Delta S = nR\ln \frac{p_1}{p_2} + C_p\ln \frac{T_2}{T_1} = nR\ln \frac{V_2}{V_1} + C_V\ln \frac{T_2}{T_1};$

(3) $\mathrm{d}U = T\mathrm{d}S - p\mathrm{d}V;$

(4) $\Delta G = \int V\mathrm{d}p;$

(5) $\Delta S, \Delta A, \Delta G$ 作为判据时必须满足的条件。

3.2 判断下列说法是否正确，并说明原因。

(1) 不可逆过程一定是自发的, 而自发过程一定是不可逆的;

(2) 凡熵增加过程都是自发过程;

(3) 不可逆过程的熵永不减少;

(4) 系统达平衡时, 熵值最大, Gibbs 自由能最小;

(5) 当某系统的热力学能和体积恒定时, $\Delta S < 0$ 的过程不可能发生;

(6) 某系统从始态经过一个绝热不可逆过程到达终态, 现在要在相同的始态和终态之间设计一个绝热可逆过程;

(7) 在一个绝热系统中, 发生了一个不可逆过程, 系统从状态 1 变到了状态 2, 不论用什么方法, 系统再也无法回到原来的状态;

(8) 对于理想气体的等温膨胀过程, $\Delta U = 0$ , 系统所吸的热全部变成了功, 这与 Kelvin 的说法不符;

(9) 冷冻机可以从低温热源吸热放给高温热源, 这与 Clausius 的说法不符;

(10) $C_p$ 恒大于 $C_V$ 。

3.3 指出下列各过程的 $Q, W, \Delta U, \Delta H, \Delta S, \Delta A$ 和 $\Delta G$ 等热力学函数的变量中，哪些为零？哪些绝对值相等？

(1) 理想气体真空膨胀;

(2) 理想气体等温可逆膨胀;

(3) 理想气体绝热节流膨胀;

(4) 实际气体绝热可逆膨胀;

(5) 实际气体绝热节流膨胀;

(6) $\mathrm{H}_{2}(\mathrm{g})$ 和 $\mathrm{O}_{2}(\mathrm{g})$ 在绝热钢瓶中发生反应生成水;

(7) $\mathrm{H}_{2}(\mathrm{~g})$ 和 $\mathrm{Cl}_{2}(\mathrm{~g})$ 在绝热钢瓶中发生反应生成 $\mathrm{HCl}(\mathrm{g})$ ;

(8) $\mathrm{H}_2\mathrm{O}(1,373\mathrm{K},101\mathrm{kPa}) \rightleftharpoons \mathrm{H}_2\mathrm{O}(\mathrm{g},373\mathrm{K},101\mathrm{kPa})$ ;

(9) 在等温等压且不做非膨胀功的条件下, 下列反应达到平衡:

$$
3 \mathrm{H} _ {2} (\mathrm{g}) + \mathrm{N} _ {2} (\mathrm{g}) \rightleftharpoons 2 \mathrm{NH} _ {3} (\mathrm{g})
$$

(10) 绝热、恒压且不做非膨胀功的条件下, 发生了一个化学反应。

3.4 将下列不可逆过程设计为可逆过程。

(1) 理想气体从压力为 $p_1$ 向真空膨胀为 $p_2$ ;

(2) 将两块温度分别为 $T_{1}, T_{2}$ 的铁块 $(T_{1} > T_{2})$ 相接触, 最后终态温度为 $T$ ;

(3) 水真空蒸发为同温同压的水蒸气, 设水在该温度时的饱和蒸气压为 $p_{\mathrm{s}}$ :

$$
\mathrm{H} _ {2} \mathrm{O} (1, 3 0 3 \mathrm{K}, 1 0 0 \mathrm{kPa}) \longrightarrow \mathrm{H} _ {2} \mathrm{O} (\mathrm{g}, 3 0 3 \mathrm{K}, 1 0 0 \mathrm{kPa})
$$

(4) 理想气体从 $p_{1}, V_{1}, T_{1}$ 经不可逆过程到达 $p_{2}, V_{2}, T_{2}$ ，可设计几条可逆路线，画出示意图。

3.5 判断下列恒温恒压过程中, 熵值的变化, 是大于零, 小于零还是等于零? 为什么?

(1) 将食盐放入水中;

(2) $\mathrm{HCl(g)}$ 溶于水中生成盐酸;

(3) $\mathrm{NH_4Cl(s)}\longrightarrow \mathrm{NH_3(g)} + \mathrm{HCl(g)};$

(4) $\mathrm{H}_2(\mathrm{g}) + \frac{1}{2}\mathrm{O}_2(\mathrm{g})\longrightarrow \mathrm{H}_2\mathrm{O}(\mathrm{l});$

(5) $1\mathrm{dm}^3 (\mathrm{N}_2,\mathrm{g}) + 1\mathrm{dm}^3 (\mathrm{Ar},\mathrm{g})\longrightarrow 2\mathrm{dm}^3 (\mathrm{N}_2 + \mathrm{Ar},\mathrm{g});$

(6) $1\mathrm{dm}^3 (\mathrm{N}_2,\mathrm{g}) + 1\mathrm{dm}^3 (\mathrm{Ar},\mathrm{g})\longrightarrow 1\mathrm{dm}^3 (\mathrm{N}_2 + \mathrm{Ar},\mathrm{g});$

(7) $1\mathrm{dm}^3 (\mathrm{N}_2,\mathrm{g}) + 1\mathrm{dm}^3 (\mathrm{N}_2,\mathrm{g})\longrightarrow 2\mathrm{dm}^3 (\mathrm{N}_2,\mathrm{g});$

(8) $1\mathrm{dm}^3 (\mathrm{N}_2,\mathrm{g}) + 1\mathrm{dm}^3 (\mathrm{N}_2,\mathrm{g})\longrightarrow 1\mathrm{dm}^3 (\mathrm{N}_2,\mathrm{g})$

3.6 (1) 在 $298 \mathrm{~K}$ 和 $100 \mathrm{kPa}$ 时, 反应 $\mathrm{H}_{2} \mathrm{O}(\mathrm{l}) \longrightarrow \mathrm{H}_{2}(\mathrm{~g}) + \frac{1}{2} \mathrm{O}_{2}(\mathrm{~g})$ 的 $\Delta_{\mathrm{r}} G_{\mathrm{m}} > 0$ , 说明该反应不能自发进行。但在实验室内常用电解水的方法制备氢气, 这两者有无矛盾?

(2) 试将 Carnot 循环分别表达在以如下坐标表示的图上:

$$
T - p; \quad T - S; \quad S - V; \quad U - S; \quad T - H
$$

习题

## 3.1 对于 Carnot 机:

(1) 已知水在 $50p^{\ominus}$ 下沸点为 $265^{\circ}C, p^{\ominus}$ 下沸点为 $100^{\circ}C$ ，试比较：(a) 在 $p^{\ominus}$ 下，(b) 在 $50p^{\ominus}$ 下，工作于水的沸点的蒸汽机的理论效率。假定低温热源温度均为 $40^{\circ}C$ 。

(2) 在题 (1) 中, 若两种情况下都要对外做功 1000 J, 则必须从高温热源吸热各多少?

(3) 欲提高 Carnot 机效率, 是保持 $T_{1}$ 不变、升高 $T_{2}$ 好, 还是保持 $T_{2}$ 不变、降低 $T_{1}$ 好? 并说明理由。

3.2 一系统有 $2 \mathrm{~mol} \mathrm{~N}_{2}(\mathrm{~g})$ , 可当成理想气体处理, 已知 $\mathrm{N}_{2}(\mathrm{~g})$ 的 $C_{V,\mathrm{m}} = 2.5 R$ 。 $300 \mathrm{~K}$ 时, 该系统从 $100 \mathrm{kPa}$ 的始态出发, 经绝热可逆压缩至 $300 \mathrm{kPa}$ 后, 再真空膨胀至 $100 \mathrm{kPa}$ , 求整个过程的 $Q, W, \Delta U, \Delta H$ 和 $\Delta S$ 。

3.3 一系统有 $10 \mathrm{~mol} \mathrm{Ar}(\mathrm{g})$ , 可看作理想气体, 已知 $\mathrm{Ar}(\mathrm{g})$ 的 $C_{V,\mathrm{m}} = 1.5 R$ 。该系统从始态 $273 \mathrm{~K}, 100 \mathrm{kPa}$ 变到终态 $398 \mathrm{~K}, 1000 \mathrm{kPa}$ , 设计 3 种不同的路径, 分别计算该过程的熵变。比较结果, 说明什么问题?

3.4 在绝热容器中, 将 $0.10 \mathrm{~kg}, 263 \mathrm{~K}$ 的冰与 $0.50 \mathrm{~kg}, 353 \mathrm{~K}$ 的水混合, 求混合过程的熵变。设水的平均比热容为 $4.184 \, kJ \cdot kg^{-1} \cdot K^{-1}$ ，冰的平均比热容为 $2.067 \, kJ \cdot kg^{-1} \cdot K^{-1}$ ，冰的熔化热为 $333 \, kJ \cdot kg^{-1}$ 。

3.5 一个中间由导热隔板分开的盒子, 一边放 $0.2 \, \text{mol O}_{2}(\text{g})$ , 压力为 $20 \, kPa$ , 另一边放 $0.8 \, \text{mol N}_{2}(\text{g})$ , 压力为 $80 \, kPa$ 。在等温 (298 K) 下, 抽去隔板使两种气体混合, 试求:

(1) 混合后盒子中的压力;

(2) 混合过程的 $Q, W, \Delta U, \Delta S$ 和 $\Delta G$ ;

(3) 在等温情况下, 使混合后的气体再可逆地回到始态, 计算该过程的 $Q$ 和 $W$ 。

3.6 有一绝热箱子, 中间用绝热隔板分为两部分, 一边放 $1 \mathrm{~mol} 300 \mathrm{~K}$ , $100 \mathrm{kPa}$ 的单原子理想气体 $\mathrm{Ar(g)}$ , 另一边放 $2 \mathrm{~mol} 400 \mathrm{~K}, 200 \mathrm{kPa}$ 的双原子理想气体 $\mathrm{N}_{2}(\mathrm{g})$ 。若把绝热隔板抽去, 让两种气体混合达平衡, 求混合过程的熵变。

3.7 已知某气体的等容热容为 $C_{V} = g + hT$ ，其中 g 和 h 皆不是体积的函数，如果该气体服从 van der Waals 方程式，试求 1 mol 气体从状态 $(p_{1}, V_{1}, T_{1})$ 变化到状态 $(p_{2}, V_{2}, T_{2})$ 时熵变 $\Delta S$ 的表达式。

3.8 已知 25 K 时, 水的标准摩尔生成 Gibbs 自由能为 $-237.19 \, kJ \cdot mol^{-1}$ 。在 25 K, $p^{\ominus}$ 下, 用 2.200 V 的直流电使 1 mol 水电解变成氢气和氧气, 放热 139.0 kJ。求该反应的摩尔熵变。

3.9 1 mol 某气体在类似于 Joule-Thomson 实验的管中由 $100p^{\ominus}$ ， $25^{\circ}C$ 慢慢通过一多孔塞变成 $p^{\ominus}$ ，整个装置放在一个温度为 $25^{\circ}C$ 的特大恒温器中。实验中，恒温器从气体吸热 202 J。已知该气体的状态方程式 $p(V_{\mathrm{m}} - b) = RT$ ，其中 $b = 20 \times 10^{-6} \, m^{3} \cdot mol^{-1}$ 。试计算实验过程的 W, $\Delta U$ , $\Delta H$ 和 $\Delta S$ 。

3.10 实验室中有一个大恒温槽的温度为 400 K, 室温为 300 K, 因恒温槽绝热不良而有 4.0 kJ 的热传给了室内的空气, 用计算说明这一过程是否可逆。

3.11 有 $1\mathrm{mol}$ 过冷水, 从始态 $263\mathrm{K}, 101\mathrm{kPa}$ 变成同温同压的冰, 求该过程的熵变。并用计算说明这一过程的可逆性。已知水和冰在该温度范围内的平均摩尔定压热容分别为 $C_{p,\mathrm{m}}(\mathrm{H}_2\mathrm{O},\mathrm{l}) = 75.3\mathrm{J}\cdot \mathrm{mol}^{-1}\cdot \mathrm{K}^{-1}, C_{p,\mathrm{m}}(\mathrm{H}_2\mathrm{O},\mathrm{s}) = 37.7\mathrm{J}\cdot \mathrm{mol}^{-1}\cdot \mathrm{K}^{-1}$ ; 在 $273\mathrm{K}, 101\mathrm{kPa}$ 时水的摩尔凝固热为 $\Delta_{\mathrm{fus}}H_{\mathrm{m}}(\mathrm{H}_2\mathrm{O},\mathrm{s}) = -6.01\mathrm{kJ}\cdot \mathrm{mol}^{-1}$ 。

3.12 1 mol N₂(g) 可看作理想气体, 从始态 298 K, 100 kPa 经如下两个等温过程, 分别到达压力为 600 kPa 的终态, 分别求过程的 Q, W, ΔU, ΔH, ΔA, ΔG, ΔS 和 ΔS $_{iso}$ 。

(1) 等温可逆压缩;

(2) 等外压为 600 kPa 下压缩。

3.13 将 $1 \, \text{mol O}_{2}(\text{g})$ 从 298 K, 100 kPa 的始态, 绝热可逆压缩到 600 kPa 的终态, 试求该过程的 Q, W, $\Delta U$ , $\Delta H$ , $\Delta A$ , $\Delta G$ , $\Delta S$ 和 $\Delta S_{iso}$ 。设 $\mathrm{O}_{2}(\mathrm{~g})$ 为理想气体, 已知 $\mathrm{O}_{2}(\mathrm{~g})$ 的 $C_{p,m} = 3.5 R$ , $S_{\mathrm{m}}(\mathrm{O}_{2}, \mathrm{g}) = 205.14 \, \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}$ 。如果将该系统从 298 K, 100 kPa 的始态绝热可逆压缩到体积为 $5 \, dm^{3}$ 的终态, 试求终态的温度、压力和该过程的 Q, W, $\Delta U$ , $\Delta H$ 和 $\Delta S$ 。

3.14 1 mol $H_{2}$ 从 100 K, 4.1 dm $^{3}$ 加热到 600 K, 49.2 dm $^{3}$ , 若此过程是将气体置于 600 K 的炉中让其反抗 101.325 kPa 的恒外压以不可逆方式进行, 计算隔离系统的熵变。已知氢气的摩尔等容热容与温度的关系式是

$$
C _ {V, \mathrm{m}} = [ 2 0. 7 5 3 - 0. 8 3 6 8 \times 1 0 ^ {- 3} (T / \mathrm{K}) + 2 0. 1 1 7 \times 1 0 ^ {- 7} (T / \mathrm{K}) ^ {2} ] \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{K} ^ {- 1}
$$

3.15 已知在 353 K 和 101.3 kPa 下，苯的摩尔蒸发焓为 $\Delta_{vap}H_{m} = 30.77 kJ \cdot mol^{-1}$ ，设气体为理想气体。

(1) 1.0 mol 苯 $C_{6}H_{6}(l)$ 在正常沸点 353 K 和 101.3 kPa 下蒸发为苯蒸气, 计算该过程的 Q, W, $\Delta U$ , $\Delta H$ , $\Delta S$ , $\Delta A$ 和 $\Delta G$ 。

(2) 将 1.0 mol 苯 $C_{6}H_{6}(l)$ 在正常沸点 353 K 和 101.3 kPa 下, 向真空蒸发为同温同压的苯蒸气, 试求该过程的 Q, W, 摩尔蒸发熵 $\Delta_{vap}S_{m}$ 、摩尔蒸发 Gibbs 自由能 $\Delta_{vap}G_{m}$ 和环境的熵变 $\Delta S_{环}$ ; 并根据计算结果, 判断上述过程的可逆性。

3.16 某一化学反应, 在 298 K, $p^{\ominus}$ 下进行, 当反应进度为 1 mol 时, 放热 40.0 kJ。若使反应通过可逆电池来完成, 反应程度相同, 则吸热 4.0 kJ。

(1) 计算反应进度为 $1 \, mol$ 时的熵变 $\Delta_{r} S_{m}$ 。

(2) 当反应不通过可逆电池完成时, 求环境的熵变和隔离系统的总熵变, 从隔离系统的总熵变值说明了什么问题?

(3) 计算系统可能做的最大功。

3.17 1 mol 单原子理想气体, 从始态 273 K, 100 kPa, 分别经下列可逆变化到达各自的终态, 试计算各过程的 Q, W, $\Delta U$ , $\Delta H$ , $\Delta S$ , $\Delta A$ 和 $\Delta G$ 。已知该气体在 273 K, 100 kPa 下的摩尔熵 $S_{m} = 100 J \cdot mol^{-1} \cdot K^{-1}$ 。

(1) 恒温下压力加倍;

(2) 恒压下体积加倍;

(3) 恒容下压力加倍;

(4) 绝热可逆膨胀至压力减少一半;

(5) 绝热不可逆反抗 50 kPa 恒外压膨胀至平衡。

3.18 将 $1 \, \text{mol} \, \text{H}_{2}\text{O}(g)$ 从 $373 \, K, 100 \, kPa$ 的始态, 小心等温压缩, 在没有灰尘等凝聚中心存在下, 得到了 $373 \, K, 200 \, kPa$ 的介稳水蒸气, 但不久介稳水蒸

气全变成了液态水, 即

$$
\mathrm{H} _ {2} \mathrm{O} (\mathrm{g}, 3 7 3 \mathrm{K}, 2 0 0 \mathrm{kPa}) \longrightarrow \mathrm{H} _ {2} \mathrm{O} (1, 3 7 3 \mathrm{K}, 2 0 0 \mathrm{kPa})
$$

求该过程的 $\Delta H, \Delta G$ 和 $\Delta S$ 。已知在该条件下，水的摩尔蒸发焓为 $46.02 \, kJ \cdot mol^{-1}$ ，水的密度为 $1000 \, kg \cdot m^{-3}$ 。设气体为理想气体，液体体积受压力的影响可忽略不计。

## 3.19 用合适的判据证明:

(1) 在 373 K, 200 kPa 下, $H_{2}O(l)$ 比 $H_{2}O(g)$ 更稳定;

(2) 在 $263 \, K, 100 \, kPa$ 下, $H_{2}O(s)$ 比 $H_{2}O(l)$ 更稳定。

3.20 在 298 K, 100 kPa 下, 已知 C (金刚石) 和 C (石墨) 的摩尔熵、摩尔燃烧焓和密度数据如下:

<table><tr><td>物质</td><td> $S_{\mathrm{m}}/(J \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1})$ </td><td> $\Delta_{\mathrm{c}}H_{\mathrm{m}}/(kJ \cdot \mathrm{mol}^{-1})$ </td><td> $\rho/(kg \cdot \mathrm{m}^{-3})$ </td></tr><tr><td>C(金刚石)</td><td>2.377</td><td>-395.40</td><td>3513</td></tr><tr><td>C(石墨)</td><td>5.74</td><td>-393.51</td><td>2260</td></tr></table>

(1) 在 298 K, 100 kPa 下, C(石墨) $\longrightarrow$ C(金刚石) 的 $\Delta_{trs}G_{m}^{\ominus}$ ;

(2) 在 298 K, 100 kPa 下, 哪种晶体更为稳定?

(3) 增加压力能否使不稳定晶体向稳定晶体转化？如有可能，至少要加多大压力，才能实现这种转化？

3.21 某实际气体的状态方程式为 $(p + a/V^{2})V = RT$ ，其中 a 是常数。在压力不很大的情况下，有 1 mol 该气体由 $p_{1}, V_{1}$ 经恒温可逆过程变到 $p_{2}, V_{2}$ ，试写出 Q, W, $\Delta U, \Delta H, \Delta S, \Delta A$ 和 $\Delta G$ 的计算表示式。

3.22 在标准压力和 298 K 时, 计算如下反应的 $\Delta_{\mathrm{r}}G_{\mathrm{m}}^{\ominus}(298\mathrm{~K})$ , 从所得数值判断反应的可能性。

$$
\mathrm{(1)} \mathrm {CH_ {4} (g) + \frac {1}{2} O_ {2} (g)\longrightarrowCH_ {3} OH(l)}
$$

$$
(2) \mathrm{C} (\text {石墨}) + 2 \mathrm{H} _ {2} (\mathrm{g}) + \frac {1}{2} \mathrm{O} _ {2} (\mathrm{g}) \longrightarrow \mathrm{CH} _ {3} \mathrm{OH} (\mathrm{l})
$$

所需数据可从热力学数据表上查阅。

3.23 已知反应在 298 K 时标准摩尔反应焓如下:

$$
(1) \mathrm{Fe} _ {2} \mathrm{O} _ {3} (\mathrm{s}) + 3 \mathrm{C} (\text {石墨}) \longrightarrow 2 \mathrm{Fe} (\mathrm{s}) + 3 \mathrm{CO} (\mathrm{g}) \quad \Delta_ {\mathrm{r}} H _ {\mathrm{m}} ^ {\ominus} (1) = 4 8 9 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

$$
(2) 2 \mathrm{CO} (\mathrm{g}) + \mathrm{O} _ {2} (\mathrm{g}) \longrightarrow 2 \mathrm{CO} (\mathrm{g}) \quad \Delta_ {\mathrm{r}} H _ {\mathrm{m}} ^ {\ominus} (2) = - 5 6 4 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

$$
(3) \mathrm{C} (\text {石墨}) + \mathrm{O} _ {2} (\mathrm{g}) \longrightarrow \mathrm{CO} _ {2} (\mathrm{g}) \qquad \Delta_ {\mathrm{r}} H _ {\mathrm{m}} ^ {\ominus} (3) = - 3 9 3 \mathrm{kJ} \cdot \mathrm{mol} ^ {- 1}
$$

且 $\mathrm{O}_{2}(\mathrm{g}),\mathrm{Fe}(\mathrm{s}),\mathrm{Fe}_{2}\mathrm{O}_{3}(\mathrm{s})$ 的 $S_{\mathrm{m}}^{\ominus}(298\ \mathrm{K})$ 分别为 $205.03\ J\cdot mol^{-1}\cdot K^{-1},27.15\ J\cdot mol^{-1}\cdot K^{-1},90.0\ J\cdot mol^{-1}\cdot K^{-1}$ 。在 $298\ K,p^{\ominus}$ 下，空气能否使 $\mathrm{Fe}(\mathrm{s})$ 氧化为 $\mathrm{Fe}_{2}\mathrm{O}_{3}(\mathrm{s})$ ? (已知空气中氧含量为 20%。)

3.24 若令膨胀系数 $\alpha = \frac{1}{V}\left(\frac{\partial V}{\partial T}\right)_p$ ，压缩系数 $\beta = -\frac{1}{V}\left(\frac{\partial V}{\partial p}\right)_T$ 。试证明：

(1) $C_p - C_V = \frac{VT\alpha^2}{\beta}$

(2) $\left(\frac{\partial U}{\partial p}\right)_T = -\alpha TV + pV\beta$

3.25 对 van der Waals 实际气体, 试证明:

(1) $\left(\frac{\partial U}{\partial V}\right)_T = \frac{a}{V_{\mathrm{m}}^2}$

$$
\left(\frac {\partial V}{\partial T}\right) _ {A} \left(\frac {\partial T}{\partial G}\right) _ {p} \left(\frac {\partial S}{\partial V}\right) _ {U} = \frac {R}{p \left(V _ {\mathrm{m}} - b\right) + \frac {a}{V _ {\mathrm{m}}} - \frac {a b}{V _ {\mathrm{m}} ^ {2}}}
$$

3.26 对于理想气体, 试证明: $\frac{\left(\frac{\partial U}{\partial V}\right)_S\left(\frac{\partial H}{\partial p}\right)_S}{\left(\frac{\partial U}{\partial S}\right)_V} = -nR$ 。

3.27 在 600 K, 100 kPa 下, 生石膏的脱水反应为

$$
\mathrm{CaSO} _ {4} \cdot 2 \mathrm{H} _ {2} \mathrm{O} (\mathrm{s}) \longrightarrow \mathrm{CaSO} _ {4} (\mathrm{s}) + 2 \mathrm{H} _ {2} \mathrm{O} (\mathrm{g})
$$

试计算该反应进度为 1 mol 时的 Q, W, $\Delta U_{m}$ , $\Delta H_{m}$ , $\Delta S_{m}$ , $\Delta A_{m}$ 和 $\Delta G_{m}$ 。已知各物质在 298 K, 100 kPa 下的热力学数据如下:

<table><tr><td>物质</td><td> $\Delta_{\mathrm{f}}H_{\mathrm{m}}^{\ominus}/(\mathrm{kJ}\cdot\mathrm{mol}^{-1})$ </td><td> $S_{\mathrm{m}}^{\ominus}/(\mathrm{J}\cdot\mathrm{mol}^{-1}\cdot\mathrm{K}^{-1})$ </td><td> $C_{p,\mathrm{m}}/(\mathrm{J}\cdot\mathrm{mol}^{-1}\cdot\mathrm{K}^{-1})$ </td></tr><tr><td> $CaSO_{4}\cdot2H_{2}O(s)$ </td><td>-2021.12</td><td>193.97</td><td>186.20</td></tr><tr><td> $CaSO_{4}(s)$ </td><td>-1432.68</td><td>106.70</td><td>99.60</td></tr><tr><td> $H_{2}O(g)$ </td><td>-241.82</td><td>188.83</td><td>33.58</td></tr></table>

3.28 将 1 mol 固体碘 $I_{2}(s)$ 从 298 K, 100 kPa 的始态, 转变成 457 K, 100 kPa 的 $I_{2}(g)$ , 计算在 457 K 时 $I_{2}(g)$ 的标准摩尔熵和过程的熵变。已知 $I_{2}(s)$ 在 298 K, 100 kPa 时的标准摩尔熵为 $S_{\mathrm{m}}(\mathrm{I}_{2}, \mathrm{s}) = 116.14 \, \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}$ , 熔点为 387 K, 标准摩尔熔化焓 $\Delta_{\mathrm{fus}} H_{\mathrm{m}}^{\ominus}(\mathrm{I}_{2}, \mathrm{s}) = 15.66 \, \mathrm{kJ} \cdot \mathrm{mol}^{-1}$ 。设在 298 \~ 387 K 的温度区间内, 固体与液体碘的摩尔定压热容分别为 $C_{p,\mathrm{m}}(\mathrm{I}_{2}, \mathrm{s}) = 54.68 \, \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}$ , $C_{p,\mathrm{m}}(\mathrm{I}_{2}, \mathrm{l}) = 79.59 \, \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}$ , 碘在沸点 457 K 时的摩尔蒸发焓为 $\Delta_{\mathrm{vap}} H_{\mathrm{m}}(\mathrm{I}_{2}, \mathrm{l}) = 25.52 \, \mathrm{kJ} \cdot \mathrm{mol}^{-1}$ 。

3.29 保持压力为标准压力, 计算丙酮蒸气在 $1000 \mathrm{~K}$ 时的标准摩尔熵值。已知在 $298 \mathrm{~K}$ 时丙酮蒸气的标准摩尔熵值 $S_{\mathrm{m}}^{\ominus}(298 \mathrm{~K}) = 295.3 \mathrm{~J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}$ , 在 $273 \sim 1500 \mathrm{~K}$ 的温度区间内, 丙酮蒸气的摩尔定压热容 $C_{p,\mathrm{m}}^{\ominus}$ 与温度的关系式为

$$
C _ {p, \mathrm{m}} ^ {\ominus} = [ 2 2. 4 7 + 2 0 1. 8 \times 1 0 ^ {- 3} (T / \mathrm{K}) - 6 3. 5 \times 1 0 ^ {- 6} (T / \mathrm{K}) ^ {2} ] \mathrm{J} \cdot \mathrm{mol} ^ {- 1} \cdot \mathrm{K} ^ {- 1}
$$

3.30 对反应 $2\mathrm{Ag(s)} + \frac{1}{2}\mathrm{O}_2(\mathrm{g}) = \mathrm{Ag}_2\mathrm{O}(\mathrm{s})$ ，有

$$
\Delta_ {\mathrm{r}} G _ {\mathrm{m}} ^ {\ominus} (T) = \left[ - 3 2 3 8 4 - 1 7. 3 2 (T / \mathrm{K}) \lg (T / \mathrm{K}) + 1 1 6. 4 8 (T / \mathrm{K}) \right] \mathrm{J} \cdot \mathrm{mol} ^ {- 1}
$$

(1) 试写出该反应的 $\Delta_{\mathrm{r}}S_{\mathrm{m}}^{\ominus}, \Delta_{\mathrm{r}}H_{\mathrm{m}}^{\ominus}$ 与温度 $T$ 的关系式;

(2) 目前生产上用电解银作催化剂, 在 $600^{\circ}C$ , $p^{\ominus}$ 下将甲醇催化氧化成甲醛, 试说明在生产过程中 Ag(s) 是否会变成 $\mathrm{Ag}_{2}\mathrm{O}(s)$ 。

3.31 在文石 (aragonite) 转变为方解石 (calcite) 时, 体积增加 $2.75 \times 10^{-3} \mathrm{dm}^{3} \cdot \mathrm{mol}^{-1}$ , $\Delta G_{\mathrm{m}} = -795 \mathrm{~kJ} \cdot \mathrm{mol}^{-1}$ 。问 $25^{\circ} \mathrm{C}$ 时使文石成为稳定相所需要的压力是多少?

3.32 在 $-3^{\circ}C$ 时, 冰的蒸气压为 475.4 Pa。过冷水的蒸气压为 489.2 Pa。试求在 $-3^{\circ}C$ 时, 1 mol 过冷水转变为冰时的 $\Delta G$ 。

3.33 假定 $C_{6}H_{6}$ 在 100 kPa 和 25℃ 时是理想气体, 试由下列数据估计 $C_{6}H_{6}$ 的标准摩尔熵。25℃ 时 $C_{6}H_{6}(l)$ 的蒸气压为 12.68 kPa, 摩尔蒸发焓为 $33849\ J\cdot mol^{-1}$ , 在熔点 $5.53^{\circ}C$ 时的摩尔熔化焓为 $9866.3\ J\cdot mol^{-1}$ 。在熔点和 $25^{\circ}C$ 之间, 其 $C_{p,m}$ 的平均值为 $133.97\ J\cdot mol^{-1}\cdot K^{-1}$ 。从 $C_{p,m}\sim T$ 的关系式已经算出了在 $5.53^{\circ}C$ 时, $C_{6}H_{6}(s)$ 的 $S_{m}$ 为 $128.817\ J\cdot mol^{-1}\cdot K^{-1}$ 。

3.34 用 Debye 公式和图解积分法, 求得固态肼在熔点 $1.53^{\circ}$ C 时的摩尔熵为 $67.15 \, J \cdot mol^{-1} \cdot K^{-1}$ 。已知在该温度时固态肼的摩尔熔化焓为 $12657 \, J \cdot mol^{-1}$ 。在 $1.53 \sim 25^{\circ}C$ 时, 对液态肼可近似地应用公式, $C_{p,m}/(J \cdot mol^{-1} \cdot K^{-1}) = 97.78 + 0.0586(T/K - 280)$ 。在 $25^{\circ}C$ 时液态肼的摩尔蒸发焓为 $44769 \, J \cdot mol^{-1}$ 。液态肼的蒸气压遵从下面的方程:

$$
\lg (p / \mathrm{Pa}) = 9. 9 3 1 7 7 - \frac {1 6 8 0 . 7 4 5}{T / \mathrm{K} - 4 5 . 4 1}
$$

假定肼蒸气是理想气体, 试求在 $100 \mathrm{kPa}$ 和 $25^{\circ} \mathrm{C}$ 时气态肼的摩尔熵。

3.35 将 298 K, $p^{\ominus}$ 下的 $1 \, dm^{3} \, O_{2}(g)$ (作为理想气体) 绝热压缩到 $5p^{\ominus}$ ，耗费功 502 J。求终态的 $T_{2}$ 和 $S_{2}$ ，以及此过程中系统的 $\Delta H$ 和 $\Delta G$ 。已知 $\mathrm{O}_{2}(\mathrm{~g})$ 的 $S_{\mathrm{m}}^{\ominus}(298 \, \mathrm{K}) = 205.14 \, \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}$ ， $C_{p,\mathrm{m}}(\mathrm{O}_{2}, \mathrm{g}) = 29.36 \, \mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}$ 。

