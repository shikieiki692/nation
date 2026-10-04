---
title: "题-QBY-11-01-已知VanderWaals气"
aliases: ["题-QBY-11-01"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "清北营 春季模拟11 第 1 题"
module: "2026机构初赛模拟题"
source_subject: 化学原理
syllabus_codes: [6]
knowledge_points:
  - "[[van der Waals方程]]"
  - "[[内能]]"
  - "[[Maxwell关系]]"
  - "[[热容与摩尔热容]]"
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
source_norm: "清北营-春季模拟11"
source_file: "2026机构初赛模拟题/04-清北营/春季模拟11.md"
---

# 题-QBY-11-01-已知VanderWaals气

## 题目

### 第 1 题（37分，占 $11\%$ ）Van der Waals气体的性质

已知 Van der Waals 气体的状态方程为

$$
\left. - \frac {a n ^ {2}}{V ^ {2}}\right) (V - n b) = n R T
$$

## 1-1 分别写出修正项 a 和 b 的物理含义。

1-2 假定气体由单原子分子构成, 其半径记为 $r$ 。考虑向边长为 $L$ 的正方体容器中逐个放入分子的过程,假定容器为边长 $L$ 的立方体。放入第一个分子时, 它与器壁的距离不小于 $r$ , 因此其自由活动的体积范围为:

$$
V _ {f, l} = (L - 2 r) ^ {3}
$$

求出每个分子平均能自由活动的范围，并通过适当的近似证明：

$$
b \propto N _ {\Delta} r ^ {3}
$$

然后求出比例系数。

1-3 假定某 Van der Waals 气体的恒容热容 $C_V$ 为定值。

1-3-1 推导其内能 $U$ 关于体积 $V$ 和温度 $T$ 的表达式，积分常数可以用 $U_{0}$ 表示。

1-3-2 推导其熵 $S$ 关于体积 $V$ 和温度 $T$ 的表达式，积分常数可以用 $S_0$ 表示。

1-3-3 推导该气体的恒压热容 $C_p$ （表达式中不含 $\mathfrak{p}$ ）。

可能需要用到的复合函数求偏微分的数学公式:

1. 令 $f = f(u, x)$ , $u = u(x, y)$ ，则有 $\left(\frac{\partial f}{\partial x}\right)_y = \left(\frac{\partial f}{\partial x}\right)_u + \left(\frac{\partial f}{\partial u}\right)_x \left(\frac{\partial u}{\partial x}\right)_y$ .

2. 令 $f(x, y, z) = 0$ ，则有 $\left(\frac{\partial x}{\partial y}\right)_z = -\left(\frac{\partial f}{\partial y}\right)_{x,z} / \left(\frac{\partial f}{\partial x}\right)_{y,z}$ 。

$$
\left(\frac {\partial S}{\partial V}\right) _ {T} = \left(\frac {\partial P}{\partial T}\right) _ {V}
$$

## 参考答案

$\left(p + \frac{an^2}{V^2}\right)(V - nb) = nRT$

1-1 分别写出修正项 $a$ 和 $b$ 的物理含义。

1-2 假定气体由单原子分子构成, 其半径记为 $r$ 。考虑向边长为 $L$ 的正方体容器中逐个放入分子的过程,假定容器为边长 $L$ 的立方体。放入第一个分子时, 它与器壁的距离不小于 $r$ , 因此其自由活动的体积范围为: $V_{\mathrm{m}} = (I - 2r)^{3}$

$$
V _ {f: l} = (L - 2 r) ^ {3}
$$

求出每个分子平均能自由活动的范围，并通过适当的近似证明：

$$
b \propto N _ {\Delta} r ^ {3}
$$

然后求出比例系数。

1-3 假定某 Van der Waals 气体的恒容热容 $C_V$ 为定值。

1-3-1 推导其内能 $U$ 关于体积 $V$ 和温度 $T$ 的表达式，积分常数可以用 $U_0$ 表示。

1-3-2 推导其熵 $S$ 关于体积 $V$ 和温度 $T$ 的表达式，积分常数可以用 $S_0$ 表示。

1-3-3 推导该气体的恒压热容 $C_p$ （表达式中不含 $\mathfrak{p}$ ）。

可能需要用到的复合函数求偏微分的数学公式：

1. 令 $f = f(u, x)$ ， $u = u(t(x, y))$ ，则有 $\left(\frac{\partial f}{\partial x}\right)_y = \left(\frac{\partial f}{\partial x}\right)_u + \left(\frac{\partial f}{\partial u}\right)_x \left(\frac{\partial u}{\partial x}\right)_y$ 。

2. 令 $f(x, y, z) = 0$ ，则有 $\left(\frac{\partial x}{\partial y}\right)_z = -\left(\frac{\partial f}{\partial y}\right)_{x, z} / \left(\frac{\partial f}{\partial x}\right)_{y, z}$ 。

$$
\left(\frac {\partial S}{\partial V}\right) _ {T} = \left(\frac {\partial P}{\partial T}\right) _ {V}
$$

<table><tr><td>1-1</td><td>a的物理含义:分子间引力修正b的物理含义:分子体积修正</td></tr><tr><td>1-2</td><td>放入第二个分子时,除去与器壁距离不小于r以外,与第一个分子之间的距离必须大于2r,于是其自由活动的体积范围为 $V_{f,2} = (L - 2r)^{3} - \frac{4}{3}\pi(2r)^{3}$ 同样地,对手放入的第i个分子有 $V_{f,i} = (L - 2r)^{3} - \frac{4}{3}\pi(2r)^{3}(i-1)$ 于是所有分子的自由活动范围的平均体积为 $\overline{V}_{f,i} = \frac{1}{N}\sum_{i=1}^{N}V_{f,i} = \frac{1}{N}\sum_{i=1}^{N}(L - 2r)^{3} - \frac{4}{3}\pi(2r)^{3}(i-1) = (L - 2r)^{3} - \frac{16\pi r^{3}(N-1)}{3}$ (在这一步近似也可以得分)</td></tr></table>

## 于是体积修正项

<table><tr><td></td><td>于是体积修正项 $b = \frac{V - \overline{V_f}}{n} = \frac{L^3 - (L - 2r)^3}{n} - \frac{16\pi r^3(nN_A - 1)}{3n} = \frac{L^3 - (L - 2r)^3}{n} - \frac{16\pi r^3}{3} \left( N_A - \frac{1}{n} \right)$ 由于  $r << L, N_A >> 1$ ,于是 $b = \frac{16\pi}{3} r^3 N_f$ </td></tr><tr><td>1-3-1</td><td>首先将U视作V和T的函数,微分可得 $\mathrm{d}U = \left( \frac{\partial U}{\partial T} \right)_V \mathrm{d}T + \left( \frac{\partial U}{\partial V} \right)_T \mathrm{d}V$ 根据恒容热容的定义可知 $C_V = \left( \frac{\partial U}{\partial T} \right)_V$ 根据热力学第一定律有 $\mathrm{d}U = T \mathrm{~d}S - p \mathrm{~d}V$ 于是保持温度T一定,对上式求V的偏导可得 $\left( \frac{\partial U}{\partial V} \right)_T = T \left( \frac{\partial S}{\partial V} \right)_T - p$ 根据Maxwell关系有 $\left( \frac{\partial S}{\partial V} \right)_T = \left( \frac{\partial p}{\partial T} \right)_V$ 于是 $\left( \frac{\partial U}{\partial V} \right)_T = T \left( \frac{\partial p}{\partial T} \right)_V - p$ 于是 $\mathrm{d}U = C_V \mathrm{~d}T + \left[ T \left( \frac{\partial p}{\partial T} \right)_V - p \right] \mathrm{d}V$ 对于Van der Waals气体而得 $p = \frac{nR T^2}{V - nb} - \frac{an^2}{V^2}$ 于是 $T \left( \frac{\partial p}{\partial T} \right)_V - p = T - \frac{nR}{V - nb} - \left( \frac{nR T^2}{V - nb} - \frac{an^2}{V^2} \right) = \frac{an^{2}}{V^2}$ 于是 $\mathrm{d}U = C_V \mathrm{~d}T + \frac{an^2}{V^2} \mathrm{~d}V$ ,两边积分可得 $U = C_V T - \frac{an^2}{V} + U_0$ </td></tr><tr><td>1-3-2</td><td>根据热力学第一定律有 $\mathrm{d}U = T \mathrm{~d}S - p \mathrm{~d}V$ 移项可得 $\mathrm{d}S = \frac{1}{T} \mathrm{~d}U + \frac{p}{T} \mathrm{~d}V$ 我们已经得到 $\mathrm{d}U = C_V \mathrm{~d}T + \left[ T \left( \frac{\partial p}{\partial T} \right)_P - p \right] \mathrm{d}V$ ,于是 $\mathrm{d}S = \frac{1}{T} (\mathrm{d}U + p \mathrm{~d}V) = \frac{1}{T} \left[ C_V \mathrm{~d}T + T \left( \frac{\partial p}{\partial T} \right)_V \mathrm{~d}V \right]$ 代入Van der Waals气体的状态方程就有 $\mathrm{d}S=C_{\mathrm{r}}\cdot\frac{\mathrm{d}T}{T}+\frac{nR}{V-nb}\mathrm{d}V$ 两边积分可得 $S=C_{v}\ln T+nR\ln(V-nb)+S_{0}$ </td></tr><tr><td>1-3-3</td><td>由焓的定义 $H=U+pV$ 可得 $C_{p}-C_{v}=\left(\frac{\partial(U+pV)}{\partial T}\right)_{p}=\left(\frac{\partial U}{\partial T}\right)_{v}=p\left(\frac{\partial V}{\partial T}\right)_{p}+\left(\frac{\partial U}{\partial T}\right)_{p}-\left(\frac{\partial U}{\partial T}\right)_{v}$ 根据复合函数求偏导的法则,可得 $\left(\frac{\partial U}{\partial T}\right)_{p}=\left(\frac{\partial U}{\partial T}\right)_{v}+\left(\frac{\partial U}{\partial V}\right)_{T}\left(\frac{\partial V}{\partial T}\right)_{p}$ 代回前式可得 $C_{p}-C_{v}=\left[p+\left(\frac{\partial U}{\partial V}\right)_{T}\right]\left(\frac{\partial V}{\partial T}\right)_{p}$ 对于Van der Waals气体,已经得出 $\left(\frac{\partial U}{\partial V}\right)_{T}=\frac{an^{2}}{V^{2}}$ 。令 $f(V,T)=\left(p+\frac{an^{2}}{V^{2}}\right)(V-nb)-nRT=0$ 则有 $\left(\frac{\partial V}{\partial T}\right)_{p}=-\frac{\left(\frac{\partial f}{\partial T}\right)_{v,p}}{\left(\frac{\partial f}{\partial V}\right)_{T,p}}=\frac{nR}{p-\frac{an^{2}}{V^{2}}+\frac{2abn^{3}}{V^{3}}}$ 于是 $C_{p}-C_{v}=\left(p+\frac{an^{2}}{V^{2}}\right)\frac{nR}{p-\frac{an^{2}}{V^{2}}+\frac{2abn^{3}}{V^{3}}}$ ,将 $p=\frac{nRT}{V-nb}-\frac{an^{2}}{V^{2}}$ 代入可得 $C_{p}-C_{v}=\frac{nR}{1-\frac{2an(V-nb)^{2}}{RTV^{3}}}$ </td></tr></table>

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**（OCR 原文逐字转录，可能保留原卷笔误）。