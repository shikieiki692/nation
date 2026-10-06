---
title: "题-GM-06-02-有机电致发光OLED是指有机"
aliases: ["题-GM-06-02·五一杭州6"]
type: 题目
fidelity: 原书逐字
difficulty: 4
teaching_level: 竞赛
source: "伽马 五一伽马杭州6 第 2 题"
module: "2026机构初赛模拟题"
source_subject: 结构化学
syllabus_codes: [50, 15, 57]
knowledge_points:
  - "[[有机合成]]"
  - "[[晶体结构]]"
  - "[[化学动力学]]"
  - "[[材料化学]]"
tags: [化竞, 题目, 初赛, 机构模拟题, 伽马]
updated: 2026-09-26
status: 已填充
exam_stage: 初赛
subject_module: 结构化学
pack: 综合模拟卷
submodule: 伽马
source_category: 竞赛导向·竞赛教辅
source_grade: A
source_tier: 2
source_norm: "伽马-五一伽马杭州6"
source_file: "2026机构初赛模拟题/06-伽马/五一伽马杭州6.md"
---

# 题-GM-06-02-有机电致发光OLED是指有机

## 题目

### 第 2 题（25分， $12\%$ ）有机电致发光

有机电致发光（OLED）是指有机材料通电后，电子与空穴结合释放能量、转化为光子的发光现象。它具备轻薄柔性、色彩丰富、能耗低、可大面积制备的特点，无需背光模块，响应速度快。应用于柔性屏、可穿戴设备、新型照明等领域，是极具潜力的下一代显示与发光技术。

2020年，中国科学家发现了一种高效和稳定的有机电致发光分子5Cz-TRZ，其合成路线如下：（下图反应式未配平，虚框内基团可缩写成Ar）

![](images/c7b0c892dab2d8feccf75db76cf6a36d255fde5daa775fc7c3c823a9959fe105.jpg)

![](images/760e66a16c0bf2bd2d300bd4a8df32a88ffe5f0393ca3173fef7bcf8a9be1ee1.jpg)

2-1 给出 A 和 5Cz-TRZ 的结构。

2-2 该晶体属于三斜晶系，晶胞参数 $a = 971.4 \mathrm{pm}, b = 2475 \mathrm{pm}, c = 2531 \mathrm{pm}, \alpha = 85.13^{\circ}, \beta = 80.70^{\circ}, \gamma = 85.65^{\circ}$ ，晶胞的结构基元是 4 个 5Cz-TRZ 分子。通过计算，给出该晶体的密度。提示：三斜晶系 $V = abc \sqrt{1 - \cos^{2} \alpha - \cos^{2} \beta - \cos^{2} \gamma + 2 \cos \alpha \cos \beta \cos \gamma}$ ，若未能给出 5Cz-TRZ 分子的结构，可以在此问中假设它的相对分子质量为 1000。

2-3 空穴迁移率是决定 OLED 等电池发光器件性能的核心参数。理想情况的 Mott-Gurney 公式给出了其理想情况下电压与电流密度的关系：

$$
J _ {S C L C} = \frac {9 \varepsilon_ {0} \varepsilon_ {r} \mu V ^ {m}}{8 L ^ {3}}
$$

其中， $J_{SCLC}$ 是电流密度，由电流除以截面积计算得到； $\varepsilon_0$ 是真空介电常数，为 $8.854 \times 10^{-12} \mathrm{~F} \mathrm{~m}^{-1}$ ； $\varepsilon_r$ 是材料的相对介电常数； $\mu$ 是电荷迁移率，在理想情况下为定值； $L$ 是器件有机功能层厚度； $V$ 是施加在器件两端的电压。 $m$ 在无电压或低电压下为1，其随电压的增大而增大，逐渐趋于一个定值。本器件相对介电常数为3.512，横截面积为 $4 \mathrm{~cm}^2$ ，有机功能层厚度为 $50 \mathrm{~nm}$ 。

2-3-1 在高电压下（提示：此时 m 为定值）测出了 4 组电流密度与电压的关系，如下：

<table><tr><td> $J_{SCLC}$ </td><td>107.0 mA cm $^{-2}$ </td><td>218.8 mA cm $^{-2}$ </td><td>315.2 mA cm $^{-2}$ </td><td>492.5 mA cm $^{-2}$ </td></tr><tr><td>V</td><td>7 V</td><td>10V</td><td>12V</td><td>15 V</td></tr></table>

通过计算, 给出器件的电荷迁移率, 以 $\mathrm{m}^{2} \mathrm{~V}^{-1} \mathrm{~s}^{-1}$ 为单位。

2-3-2 在不施加电压的情况下，该器件的电阻为多少？以 $\Omega$ 为单位。若未能求出电荷迁移率，此问可以使用 $\mu = 10^{-10} \mathrm{~m}^2 \mathrm{~V}^{-1} \mathrm{~s}^{-1}$ 。

2-4 器件中的有机功能层需要隔绝氧气，避免氧化。然而由于器件制备不良等因素，有机功能层的部分区域会逐渐被氧化，从而丧失作为 OLED 材料的电学特性，变为纯电阻。

2-4-1 将上述器件中有机功能层暴露在空气中进行测试，恒定器件两端的电压为 $20 \, V$ 。待电流稳定后，测得电流为 $50 \, mA$ 。给出完全氧化后有机功能层的电阻率 $\rho$ ，以 $\Omega \, m$ 为单位。
2-4-2 经测试发现，该器件氧化区横截面积与测试时间呈如下的关系：

$$
\frac {A _ {o x}}{A _ {0}} = - e x p (- k t) + 1
$$

在器件两端的电压保持 $10 \mathrm{~V}$ 的条件下对器件进行测试, 发现 $48 \mathrm{~h}$ 后, 电流随时间的变化率为 $-1.195 \mathrm{mAh}^{-1}$ 。通过计算, 给出该器件在此环境下的半衰期。若在前面任何一问未能求出结果, 此问可以使用 $\mu = 10^{-10} \mathrm{~m}^{2} \mathrm{~V}^{-1} \mathrm{~s}^{-1}, \rho = 4 \times 10^{6} \Omega \mathrm{~m}$ 。

## 参考答案

有机电致发光（OLED）是指有机材料通电后，电子与空穴结合释放能量、转化为光子的发光现象。它具备轻薄柔性、色彩丰富、能耗低、可大面积制备的特点，无需背光模块，响应速度快。应用于柔性屏、可穿戴设备、新型照明等领域，是极具潜力的下一代显示与发光技术。

2020 年，中国科学家发现了一种高效和稳定的有机电致发光分子 5Cz-TRZ，其合成路线如下：（下图反应式未配平，虚框内基团可缩写成 Ar）

![](images/617845f008ecd655f0a10dac05a10c464054578d6a17b0c40193ed1531c9676e.jpg)

![](images/af19aa144b180606b0d78d34eb176815d869e59e684ab4b52bdd8b29d42fba6a.jpg)

2-1 给出 A 和 5Cz-TRZ 的结构。

<table><tr><td colspan="2">(本小问共4分)</td></tr><tr><td>A:<img src="images/1d4810e9ffcc1813ce2fe3262d6eb3f13c58aab8494e18f6012853a67da2f9e3.jpg"/></td><td>5Cz-TRZ:<img src="images/5fb999b638e1905dad4128529435dbd0dfcd43029e87db1080caf6bed48f7b79.jpg"/></td></tr><tr><td colspan="2">(各2分)</td></tr></table>

2-2 该晶体属于三斜晶系，晶胞参数 $a = 971.4 \mathrm{pm}, b = 2475 \mathrm{pm}, c = 2531 \mathrm{pm}, \alpha = 85.13^{\circ}, \beta = 80.70^{\circ}, \gamma = 85.65^{\circ}$ ，晶胞的结构基元是 4 个 5Cz-TRZ 分子。通过计算，给出该晶体的密度。提示：三斜晶系 $V = abc \sqrt{1 - \cos^{2} \alpha - \cos^{2} \beta - \cos^{2} \gamma + 2 \cos \alpha \cos \beta \cos \gamma}$ ，若未能给出 5Cz-TRZ 分子的结构，可以在此问中假设它的相对分子质量为 1000。

(本小问共4分)
$1 - \cos^2\alpha - \cos^2\beta - \cos^2\gamma + 2\cos\alpha\cos\beta\cos\gamma = 0.9630$ $\rho = \frac{ZM}{N_AV} = \frac{4 \times 1142.5}{6.022 \times 10^{23} \times 971.4 \times 2475 \times 2531 \times 0.9630 \times 10^{-30}} g cm^{-3} = 1.295 g cm^{-3}$
(用1000计算，结果是 $1.133 g/cm^3$ ，也得全分）

2-3 空穴迁移率是决定 OLED 等电池发光器件性能的核心参数。理想情况的 Mott-Gurney 公式给出了其理想情况下电压与电流密度的关系：

$$
J _ {S C L C} = \frac {9 \varepsilon_ {0} \varepsilon_ {r} \mu V ^ {m}}{8 L ^ {3}}
$$

其中， $J_{SCLC}$ 是电流密度，由电流除以截面积计算得到； $\varepsilon_0$ 是真空介电常数，为 $8.854 \times 10^{-12} \mathrm{~F} \mathrm{~m}^{-1}$ ； $\varepsilon_r$ 是材料的相对介电常数； $\mu$ 是电荷迁移率，在理想情况下为定值； $L$ 是器件有机功能层厚度； $V$ 是施加在器件两端的电压。 $m$ 在无电压或低电压下为 1，其随电压的增大而增大，逐渐趋于一个定值。本器件相对介电常数为 3.512，横截面积为 $4 \mathrm{~cm}^2$ ，有机功能层厚度为 $50 \mathrm{~nm}$ 。

2-3-1 在高电压下（提示：此时 m 为定值）测出了 4 组电流密度与电压的关系，如下：

<table><tr><td>JSCLC</td><td>107.0 mA cm-2</td><td>218.8 mA cm-2</td><td>315.2 mA cm-2</td><td>492.5 mA cm-2</td></tr><tr><td>V</td><td>7 V</td><td>10V</td><td>12V</td><td>15 V</td></tr></table>

通过计算, 给出器件的电荷迁移率, 以 $\mathrm{m}^{2} \mathrm{~V}^{-1} \mathrm{~s}^{-1}$ 为单位。

$$
J _ {S C L C} = 21.90 \mathrm{Am} ^ {- 2} \mathrm{V} ^ {- 1} V ^ {2} - 2.662 \mathrm{Am} ^ {- 2}
$$

$$
\mu = \frac {8 L ^ {3}}{9 \varepsilon_ {0} \varepsilon_ {r}} \times 21.90 \mathrm{Am} ^ {- 2} \mathrm{V} ^ {- 1} = 7.825 \times 10 ^ {- 11} \mathrm{m} ^ {2} \mathrm{V} ^ {- 1} \mathrm{s} ^ {- 1}
$$

(电流密度与电压关系2分，结果3分)

2-3-2 在不施加电压的情况下, 该器件的电阻为多少? 以 $\Omega$ 为单位。若未能求出电荷迁移率, 此问可以使用 $\mu = 10^{- 10} \mathrm{~m}^{2} \mathrm{~V}^{- 1} \mathrm{~s}^{- 1}$

$$
J _ {S C L C} = \frac {9 \varepsilon_ {0} \varepsilon_ {r} \mu V}{8 L ^ {3}} \Rightarrow J _ {S C L C} = k V \Rightarrow R = \frac {V}{J _ {S C L C} A} = \frac {1}{k A} = \frac {1}{21.90 \mathrm{Am} ^ {- 2} \mathrm{V} ^ {- 1} \times 4 \mathrm{cm} ^ {2}} = 114.2 \Omega
$$

$$
10 ^ {- 10}
$$

$$
89.36 \Omega ,
$$

2-4 器件中的有机功能层需要隔绝氧气，避免氧化。然而由于器件制备不良等因素，有机功能层的部分区域会逐渐被氧化，从而丧失作为 OLED 材料的电学特性，变为纯电阻。
2-4-1 将上述器件中有机功能层暴露在空气中进行测试，恒定器件两端的电压为 $20 \, V$ 。待电流稳定后，测得电流为 $50 \, mA$ 。给出完全氧化后有机功能层的电阻率 $\rho$ ，以 $\Omega \, m$ 为单位。
(本小问共2分)

$$
R _ {o x} = \frac {V}{I} = 400 \Omega , \rho = \frac {R _ {o x} A}{L} = 3.2 \times 10 ^ {6} \Omega \mathrm{m}
$$

2-4-2 经测试发现，该器件氧化区横截面积与测试时间呈如下的关系：

$$
\frac {A _ {o x}}{A _ {0}} = - e x p (- k t) + 1
$$

在器件两端的电压保持 $10 \, V$ 的条件下对器件进行测试，发现 $48 \, h$ 后，电流随时间的变化率为 $-1.195 \, mAh^{-1}$ 。通过计算，给出该器件在此环境下的半衰期。若在前面任何一问未能求出结果，此问可以使用 $\mu = 10^{-10} \, m^{2} \, V^{-1} \, s^{-1}, \rho = 4 \times 10^{6} \, \Omega \, m$ 。

(本小问共6分)

$$
I = J _ {S C L C} A _ {S C L C} + J _ {o x} A _ {o x} = \frac {9 \varepsilon_ {0} \varepsilon_ {r} \mu V ^ {2}}{8 L ^ {3}} (A _ {0} - A _ {o x}) + \frac {\mathrm{V}}{\rho L} A _ {o x}
$$

$$
\frac {d I}{d t} = k A _ {0} \left(\frac {\mathrm{V}}{\rho L} - \frac {9 \varepsilon_ {0} \varepsilon_ {r} \mu V ^ {2}}{8 L ^ {3}}\right) e x p (- k t)
$$

代入数值（单位省略）：

$$
\frac {d I}{d t} = - 1.094 k e x p (- k t) \Rightarrow k = 1.155 \times 10 ^ {- 3} \mathrm{h} ^ {- 1}
$$

$$
\frac {A _ {o x}}{A _ {0}} = 0.5 \Rightarrow t = 600 \mathrm{h}
$$

(过程4分, 结果2分。使用 $10^{-10}$ 和 $4\times10^{6}$ 计算，结果k为 $1.132\times10^{-3}\ h^{-1}$ ，t为612.3h，也得全分。)

## 知识点映射

- （待人工校准）


> ⚠️ **自动拆卡标记**：`subject_module`/`difficulty` 为关键词粗判，答案数值与单位**尚未经人工复核**（OCR 原文逐字转录，可能保留原卷笔误）。