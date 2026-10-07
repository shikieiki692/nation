---
title: "题-HZ-02-07-核苷二磷酸激酶NDPK是生物"
aliases: ["题-HZ-02-07·长沙冲刺物化2"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "汇智 长沙冲刺物化2 第 7 题"
module: "2026机构初赛模拟题"
source_subject: 化学原理
syllabus_codes: [57, 6]
knowledge_points:
  - "[[酶催化]]"
  - "[[化学动力学]]"
  - "[[化学热力学]]"
tags: [化竞, 题目, 初赛, 机构模拟题, 汇智]
updated: 2026-09-26
status: 已填充
exam_stage: 初赛
subject_module: 化学原理
pack: 综合模拟卷
submodule: 汇智
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_tier: 2
source_norm: "汇智-长沙冲刺物化2"
source_file: "2026机构初赛模拟题/08-汇智/长沙冲刺物化2.md"
pool_scope: 有机化学
---

# 题-HZ-02-07-核苷二磷酸激酶NDPK是生物

## 题目

### 第 7 题（23 分，占 8%）核苷二磷酸激酶的催化动力学

核苷二磷酸激酶（NDPK）是生物体内普遍存在的磷酸转移酶，催化核苷三磷酸与核苷二磷酸之间的磷酸基团转移，严格遵循乒乓机理。其催化的典型反应为：

$$
\mathrm{ATP} + \mathrm{GDP} = \mathrm{ADP} + \mathrm{GTP}
$$

7-1 看到 ATP，大家第一反应可能是其水解的热力学。已知其水解的摩尔吉布斯自由能变为 -30.5 kJ/mol（pH = 7，温度为 $37^{\circ}$ C）其反应式如下所示：

$$
\mathrm{ATP} + \mathrm{H} _ {2} \mathrm{O} \rightarrow \mathrm{ADP} + \mathrm{HPO} _ {4} ^ {2 -} + \mathrm{H} ^ {+}
$$

式中并未示出部分物种的电荷。

已知一体系 pH = 7.4，ATP 为 4 mmol/L，ADP 为 0.4 mmol/L，无机磷酸总浓度为 3 mmol/L，且磷酸的 $pK_{a1} = 2.12$ 、 $pK_{a2} = 7.21$ 、 $pK_{a3} = 12.67$ 。求出温度为 $37^{\circ}C$ 时该体系水解的摩尔吉布斯自由能变。

7-2 研究发现 NDPK 存在两种活性构象：游离酶 E 只能结合 ATP 及其结构类似物；磷酸化酶 E-P 只能结合 GDP 及其结构类似物。据此，针对题干中的反应，提出了如下的机理：

$$
\begin{array}{r l} & {\mathbf {E} + \mathbf {S} _ {1} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathbf {E S} _ {1}} \\ & {\mathbf {E S} _ {1} \xrightarrow {k _ {2}} \mathbf {E} ^ {*} + \mathbf {P} _ {1}} \\ & {\mathbf {E} ^ {*} + \mathbf {S} _ {2} \xrightarrow [ k _ {- 3} ]{k _ {3}} \mathbf {E} ^ {*} \mathbf {S} _ {2}} \\ & {\mathbf {E} ^ {*} \mathbf {S} _ {2} \xrightarrow {k _ {4}} \mathbf {E} + \mathbf {P} _ {2}} \end{array}
$$

7-2-1 根据实验结果，选择 $S_{1}$ 、 $S_{2}$ 、 $P_{1}$ 、 $P_{2}$ 的化学式。

$$
(a). \mathrm{ATP}; (b). \mathrm{ADP}; (c). \mathrm{GTP}; (d). \mathrm{GDP}
$$

7-2-2 定义总酶浓度为 $[E]_{0}$ ，假设最后一步为反应的决速步，可以得到乒乓机理的酶促反应动力学方程具有以下形式：

$$
\frac {d [ \mathbf {P} _ {2} ]}{d t} = \frac {[ \mathbf {E} ] _ {0} [ \mathbf {S} _ {1} ] [ \mathbf {S} _ {2} ]}{p _ {1} [ \mathbf {S} _ {2} ] + p _ {2} [ \mathbf {S} _ {1} ] [ \mathbf {S} _ {2} ] + p _ {3} [ \mathbf {S} _ {1} ]}
$$

通过推导给出参数 $p_1, p_2, p_3$ 的表达式与 $[\mathbf{E}^*]$ 、 $[\mathbf{E}^*\mathbf{S}_2]$ 的表达式。（用 $k_2, k_4, K_{M1}, K_{M2}$ 表达，其中 $K_{M1} = \frac{k_{-1} + k_2}{k_1}, K_{M2} = \frac{k_{-3} + k_4}{k_3}$ ）

7-3 酶动力学中的另外一个研究重点是抑制剂的作用。已知：ADP 是 ATP 的竞争性抑制剂（仅结合 E，与 ATP 竞争同一活性位点）；化合物 X 是混合型非竞争性抑制剂（既能结合 E，也能结合 E-P，且不影响底物与酶的结合，但形成的 E-X 和 E-P-X 均无催化活性。在下面的推导中，沿用 7-2-2 中的米氏常数等符号体系。

7-3-1 推导仅存在竞争性抑制剂 ADP（其浓度记为 $[I_1]$ ）时的速率方程。已知抑制常数为：

$$
K _ {i 1} = \frac {[ \mathbf {E} ] [ \mathrm{ADP} ]}{[ \mathbf {E} \cdot \mathrm{ADP} ]}
$$

7-3-2 推导仅存在非竞争性抑制剂 X（其浓度记为 $[I_{1}]$ ）时的速率方程。已知 X 与 E 和 E-P 形成复合物的解离常数均为 $K_{i2}$ 。

## 汇智起航 2026 年暑假（冲刺班）物理化学初赛模拟试题 2 答案

## 参考答案

核苷二磷酸激酶（NDPK）是生物体内普遍存在的磷酸转移酶，催化核苷三磷酸与核苷二磷酸之间的磷酸基团转移，严格遵循乒乓机理。其催化的典型反应为：

$$
\mathrm{ATP} + \mathrm{GDP} = \mathrm{ADP} + \mathrm{GTP}
$$

7-1 看到 ATP，大家第一反应可能是其水解的热力学。已知其水解的摩尔吉布斯自由能变为 -30.5 kJ/mol（pH = 7，温度为 $37^{\circ}$ C）其反应式如下所示：

$$
\mathrm{ATP} + \mathrm{H} _ {2} \mathrm{O} \rightarrow \mathrm{ADP} + \mathrm{HPO} _ {4} ^ {2 -} + \mathrm{H} ^ {+}
$$

式中并未示出部分物种的电荷。

已知一体系 pH = 7.4，ATP 为 4 mmol/L，ADP 为 0.4 mmol/L，无机磷酸总浓度为 3 mmol/L，且磷酸的 $pK_{a1} = 2.12$ 、 $pK_{a2} = 7.21$ 、 $pK_{a3} = 12.67$ 。求出温度为 $37^{\circ}C$ 时该体系水解的摩尔吉布斯自由能变。

$$
\begin{array}{r l} & {\text {由酸常数计算得} [ \mathrm{HPO} _ {4} ^ {2 -} ] = 1.823 \mathrm{mmol/L(2分)}} \\ & {\Delta G = \Delta G ^ {a} + R T \ln Q = - 30.5 + 2.578 \times \ln (7.255 \times 10 ^ {- 5}) = - 55.1 \mathrm{kJ/mol(2分)}} \\ & {\quad (\text {共} 4 \text {分})} \end{array}
$$

7-2 研究发现 NDPK 存在两种活性构象：游离酶 E 只能结合 ATP 及其结构类似物；磷酸化酶 E-P 只能结合 GDP 及其结构类似物。据此，针对题干中的反应，提出了如下的机理：

$$
\begin{array}{r l} & \mathbf {E} + \mathbf {S} _ {1} \xrightarrow [ k _ {- 1} ]{k _ {1}} \mathbf {E S} _ {1} \\ & \mathbf {E S} _ {1} \xrightarrow {k _ {2}} \mathbf {E} ^ {*} + \mathbf {P} _ {1} \\ & \mathbf {E} ^ {*} + \mathbf {S} _ {2} \xrightarrow [ k _ {- 3} ]{k _ {3}} \mathbf {E} ^ {*} \mathbf {S} _ {2} \\ & \mathbf {E} ^ {*} \mathbf {S} _ {2} \xrightarrow {k _ {4}} \mathbf {E} + \mathbf {P} _ {2} \end{array}
$$

7-2-1 根据实验结果，选择 $S_{1}$ 、 $S_{2}$ 、 $P_{1}$ 、 $P_{2}$ 的化学式。

(a). ATP; (b). ADP; (c). GTP; (d). GDP



S1: (a)

S2: (d)

P1: (b) $P_{2}$ : (c)(4分,各1分)



7-2-2 定义总酶浓度为 $[\mathbf{E}]_0$ ，假设最后一步为反应的决速步，可以得到乒乓机理的酶促反应动力学方程具有以下形式：

$$
\frac {d [ \mathbf {P} _ {2} ]}{d t} = \frac {[ \mathbf {E} ] _ {0} [ \mathbf {S} _ {1} ] [ \mathbf {S} _ {2} ]}{p _ {1} [ \mathbf {S} _ {2} ] + p _ {2} [ \mathbf {S} _ {1} ] [ \mathbf {S} _ {2} ] + p _ {3} [ \mathbf {S} _ {1} ]}
$$

通过推导给出参数 $p_{1}$ 、 $p_{2}$ 、 $p_{3}$ 的表达式与 $[E^{*}]$ 、 $[E^{*}S_{2}]$ 的表达式。（用 $k_{2}$ 、 $k_{4}$ 、 $K_{M1}$ 、 $K_{M2}$ 表达，其中 $K_{M1} = \frac{k_{-1} + k_{2}}{k_{1}}$ 、 $K_{M2} = \frac{k_{-3} + k_{4}}{k_{3}}$ ）

对 $\mathbf{ES}_1$ 、 $\mathbf{E}^*$ 、 $\mathbf{E}^{*}\mathbf{S}_{2}$ 进行稳态近似：

$$
\frac {d [ \mathbf {E S} _ {1} ]}{d t} = k _ {1} [ \mathbf {E} ] [ \mathbf {S} _ {1} ] - (k _ {- 1} + k _ {2}) [ \mathbf {E S} _ {1} ] = 0
$$

$$
\frac {d [ \mathbf {E} ^ {*} ]}{d t} = k _ {2} [ \mathbf {E S} _ {1} ] - k _ {3} [ \mathbf {E} ^ {*} ] [ \mathbf {S} _ {2} ] + k _ {- 3} [ \mathbf {E} ^ {*} \mathbf {S} _ {2} ] = 0
$$

$$
\frac {d [ \mathbf {E} ^ {*} \mathbf {S} _ {2} ]}{d t} = k _ {3} [ \mathbf {E} ^ {*} ] [ \mathbf {S} _ {2} ] - (k _ {- 3} + k _ {4}) [ \mathbf {E} ^ {*} \mathbf {S} _ {2} ] = 0
$$

解得:

$$
\left\{ \begin{array}{l} [ \mathbf {E S} _ {1} ] = \frac {1}{K _ {\mathrm{M} 1}} [ \mathbf {S} _ {1} ] [ \mathbf {E} ] \\ [ \mathbf {E} ^ {*} ] = \frac {k _ {2} K _ {\mathrm{M} 2}}{k _ {4} K _ {\mathrm{M} 1}} \frac {[ \mathbf {S} _ {1} ]}{[ \mathbf {S} _ {2} ]} [ \mathbf {E} ] \\ [ \mathbf {E} ^ {*} \mathbf {S} _ {2} ] = \frac {k _ {2}}{k _ {4} K _ {\mathrm{M} 1}} [ \mathbf {S} _ {1} ] [ \mathbf {E} ] \end{array} \right.
$$

由酶总量守恒：

$$
\begin{array}{r l} {[ \mathbf {E} ] _ {0} = [ \mathbf {E} ] + [ \mathbf {E} ^ {*} ] + [ \mathbf {E S} _ {1} ] + [ \mathbf {E} ^ {*} \mathbf {S} _ {2} ]} \\ & {\quad (1 \text {分})} \end{array}
$$

解得

$$
[ \mathbf {E} ] = \frac {[ \mathbf {E} ] _ {0}}{1 + \frac {k _ {2} K _ {\mathrm{M2}}}{k _ {4} K _ {\mathrm{M1}}} \frac {[ \mathbf {S} _ {1} ]}{[ \mathbf {S} _ {2} ]} + \frac {1}{K _ {\mathrm{M1}}} [ \mathbf {S} _ {1} ] + \frac {k _ {2}}{k _ {4} K _ {\mathrm{M1}}} [ \mathbf {S} _ {1} ]}
$$

$$
= \frac {[ \mathbf {E} ] _ {0}}{[ \mathbf {S} _ {2} ] + \frac {k _ {2} K _ {\mathrm{M2}}}{k _ {4} K _ {\mathrm{M1}}} [ \mathbf {S} _ {1} ] + \left(\frac {1}{K _ {\mathrm{M1}}} + \frac {k _ {2}}{k _ {4} K _ {\mathrm{M1}}}\right) [ \mathbf {S} _ {1} ] [ \mathbf {S} _ {2} ]}
$$

(2 分)

因此：

$$
\begin{array}{l} \left[ \mathbf {E} ^ {*} \right] = \frac {\frac {k _ {2} K _ {\mathrm{M} 2}}{k _ {4} K _ {\mathrm{M} 1}} [ \mathbf {E} ] _ {0} [ \mathbf {S} _ {1} ]}{[ \mathbf {S} _ {2} ] + \frac {k _ {2} K _ {\mathrm{M} 2}}{k _ {4} K _ {\mathrm{M} 1}} [ \mathbf {S} _ {1} ] + \left(\frac {1}{K _ {\mathrm{M} 1}} + \frac {k _ {2}}{k _ {4} K _ {\mathrm{M} 1}}\right) [ \mathbf {S} _ {1} ] [ \mathbf {S} _ {2} ]} \\ = \frac {k _ {2} K _ {\mathrm{M} 2} [ \mathbf {E} ] _ {0} [ \mathbf {S} _ {1} ]}{k _ {4} K _ {\mathrm{M} 1} [ \mathbf {S} _ {2} ] + (k _ {4} + k _ {2}) [ \mathbf {S} _ {1} ] [ \mathbf {S} _ {2} ] + k _ {2} K _ {\mathrm{M} 2} [ \mathbf {S} _ {1} ]} \end{array}
$$

$$
\begin{array}{r l} & {[ \mathbf {E} * \mathbf {S _ {2}} ] = \frac {\frac {k _ {2}}{k _ {4} K _ {\mathrm{M1}}} [ \mathbf {E} ] _ {0} [ \mathbf {S _ {1}} ] [ \mathbf {S _ {2}} ]}{[ \mathbf {S _ {2}} ] + \frac {k _ {2} K _ {\mathrm{M2}}}{k _ {4} K _ {\mathrm{M1}}} [ \mathbf {S _ {1}} ] + \left(\frac {1}{K _ {\mathrm{M1}}} + \frac {k _ {2}}{k _ {4} K _ {\mathrm{M1}}}\right) [ \mathbf {S _ {1}} ] [ \mathbf {S _ {2}} ]}} \\ & {= \frac {k _ {2} [ \mathbf {E} ] _ {0} [ \mathbf {S _ {1}} ] [ \mathbf {S _ {2}} ]}{k _ {4} K _ {\mathrm{M1}} [ \mathbf {S _ {2}} ] + (k _ {4} + k _ {2}) [ \mathbf {S _ {1}} ] [ \mathbf {S _ {2}} ] + k _ {2} K _ {\mathrm{M2}} [ \mathbf {S _ {1}} ]}} \\ & {\qquad \qquad (2 \text {分,各} 1 \text {分})} \end{array}
$$

故：

$$
\begin{array}{r l} & {\frac {d [ \mathbf {P _ {2}} ]}{d t} = k _ {4} [ \mathbf {E} ^ {*} \mathbf {S _ {2}} ] = \frac {k _ {2} k _ {4} [ \mathbf {E} ] _ {0} [ \mathbf {S _ {1}} ] [ \mathbf {S _ {2}} ]}{k _ {4} K _ {\mathrm{M1}} [ \mathbf {S _ {2}} ] + (k _ {4} + k _ {2}) [ \mathbf {S _ {1}} ] [ \mathbf {S _ {2}} ] + k _ {2} K _ {\mathrm{M2}} [ \mathbf {S _ {1}} ]}} \\ & {= \frac {[ \mathbf {E} ] _ {0} [ \mathbf {S _ {1}} ] [ \mathbf {S _ {2}} ]}{\frac {K _ {\mathrm{M1}}}{k _ {2}} [ \mathbf {S _ {2}} ] + \left(\frac {1}{k _ {2}} + \frac {1}{k _ {4}}\right) [ \mathbf {S _ {1}} ] [ \mathbf {S _ {2}} ] + \frac {K _ {\mathrm{M2}}}{k _ {4}} [ \mathbf {S _ {1}} ]}} \end{array}
$$

对比得:

$$
\left\{ \begin{array}{l} p _ {1} = \frac {K _ {\mathrm{M1}}}{k _ {2}} \\ p _ {2} = \frac {1}{k _ {2}} + \frac {1}{k _ {4}} \\ p _ {3} = \frac {K _ {\mathrm{M2}}}{k _ {4}} \end{array} \right.
$$

(3 分，各 1 分)

(共11分)

7-3 酶动力学中的另外一个研究重点是抑制剂的作用。已知：ADP 是 ATP 的竞争性抑制剂（仅结合 E，与 ATP 竞争同一活性位点）；化合物 X 是混合型非竞争性抑制剂（既能结合 E，也能结合 E-P，且不影响底物与酶的结合，但形成的 E-X 和 E-P-X 均无催化活性。在下面的推导中，沿用 7-2-2 中的米氏常数等符号体系。

7-3-1 推导仅存在竞争性抑制剂 ADP（其浓度记为 $[\mathbf{I}_1]$ ）时的速率方程。已知抑制常数为：

$$
K _ {i 1} = \frac {[ \mathbf {E} ] [ \mathrm{ADP} ]}{[ \mathbf {E} \cdot \mathrm{ADP} ]}
$$

酶总量守恒更改为：

$$
\begin{array}{r l} {[ \mathbf {E} ] _ {0} = [ \mathbf {E} ] (1 + \frac {[ \mathbf {I} _ {1} ]}{K _ {i 1}}) + [ \mathbf {E} ^ {*} ] + [ \mathbf {E S} _ {1} ] + [ \mathbf {E} ^ {*} \mathbf {S} _ {2} ]} \\ & {\quad (1 \text {分})} \end{array}
$$

同理可得：

$$
\frac {d [ \mathbf {P _ {2}} ]}{d t} = \frac {[ \mathbf {E} ] _ {0} [ \mathbf {S _ {1}} ] [ \mathbf {S _ {2}} ]}{\frac {K _ {\mathrm{M1}}}{k _ {2}} (1 + \frac {[ \mathbf {I _ {1}} ]}{K _ {i 1}}) [ \mathbf {S _ {2}} ] + \left(\frac {1}{k _ {2}} + \frac {1}{k _ {4}}\right) [ \mathbf {S _ {1}} ] [ \mathbf {S _ {2}} ] + \frac {K _ {\mathrm{M2}}}{k _ {4}} [ \mathbf {S _ {1}} ]}   (\text {1分})   (\text {共2分})
$$

7-3-2 推导仅存在非竞争性抑制剂 X（其浓度记为 $[I_{1}]$ ）时的速率方程。已知 X 与 E 和 E-P 形成复合物的解离常数均为 $K_{i2}$ 。

酶总量守恒更改为：

$$
[ \mathbf {E} ] _ {0} = [ \mathbf {E} ] (1 + \frac {[ \mathbf {I} _ {2} ]}{K _ {i 2}}) + [ \mathbf {E} ^ {*} ] (1 + \frac {[ \mathbf {I} _ {2} ]}{K _ {i 2}}) + [ \mathbf {E S} _ {1} ] + [ \mathbf {E} ^ {*} \mathbf {S} _ {2} ]
$$

(1 分)

同理可得：

$$
\frac {d [ \mathbf {P} _ {2} ]}{d t} = \frac {[ \mathbf {E} ] _ {0} [ \mathbf {S} _ {1} ] [ \mathbf {S} _ {2} ]}{\frac {K _ {\mathrm{M1}}}{k _ {2}} (1 + \frac {[ \mathbf {I} _ {2} ]}{K _ {i 2}}) [ \mathbf {S} _ {2} ] + \left(\frac {1}{k _ {2}} + \frac {1}{k _ {4}}\right) [ \mathbf {S} _ {1} ] [ \mathbf {S} _ {2} ] + \frac {K _ {\mathrm{M2}}}{k _ {4}} (1 + \frac {[ \mathbf {I} _ {2} ]}{K _ {i 2}}) [ \mathbf {S} _ {1} ]}
$$

(1 分)

(共2分)

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**（OCR 原文逐字转录，可能保留原卷笔误）。