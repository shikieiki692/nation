---
title: 题-363-化学能力测试-Ch5A-8-甲醇PEMFC与CO氧化动力学
type: 题目
aliases:
  - 甲醇 PEMFC CO 氧化
source_subject: 化学竞赛能力测试·第5章A卷
submodule: 甲醇重整与 CO 氧化动力学
subject_module: 化学原理
exam_stage: 初赛
question_type:
  - 计算
  - 作图
  - 机理
difficulty: 5
teaching_level: 竞赛
fidelity: 原书逐字
knowledge_points:
  - "[[反应热与盖斯定律]]"
  - "[[反应速率]]"
  - "[[吸附]]"
  - "[[Gibbs自由能]]"
  - "[[热力学第一定律]]"
concepts:
  - "工艺(a) CH₃OH+H₂O→CO₂+3H₂ ΔH=+48.97 kJ/mol（吸热）"
  - "工艺(b) CH₃OH+½O₂→CO₂+2H₂ ΔH=−192.85 kJ/mol（放热）"
  - "副反应 CO₂+H₂→CO+H₂O"
  - "CO 氧化 对 CO 负一级、对 O₂ 正一级；r_CO = k p_O₂/p_CO"
  - "机理：CO 强吸附 θ_CO≈1，速率控制步骤表面反应"
  - "PEMFC 效率 η(a)=83.0%（H₂O(l)）/η(b)=94.5%（H₂O(g)），473 K η(b)=91.3%"
pack: 模块习题集
tags:
  - 化竞
  - 教材习题
  - 化学能力测试
  - 第5章
created: 2026-09-03
updated: 2026-09-03
source: 化学竞赛能力测试·第5章 化学热力学初步知识·A卷第8题
source_file: "[[化学竞赛教程/（已压缩）化学竞赛能力测试]]"
status: 已填充
---

# 甲醇 PEMFC 与 CO 氧化动力学

> **来源**：化学竞赛能力测试·第5章·A卷第8题（10 分）

车载甲醇质子交换膜燃料电池(PEMFC)将甲醇蒸气转化为氢气的工艺有两种：

① 水蒸气变换（重整）法；② 空气氧化法。两种工艺都得到副产品 CO。

**8-1** 分别写出这两种工艺的化学方程式，通过计算，说明这两种工艺的优缺点。

![[c597b71930454724dd554881f142add5704f2acead4389ed274a0e1036b6a27b.jpg]]

![[4921402e472f22874818e1254fedde437191370087ccac8090db5dd402641c27.jpg]]

有关资料（298.15 K）列于下表：

| 物质 | ΔfH^θₘ / kJ·mol⁻¹ | S^θₘ / J·K⁻¹·mol⁻¹ |
|---|---|---|
| CH₃OH(g) | −200.66 | 239.81 |
| CO₂(g) | −393.51 | 213.64 |
| CO(g) | −110.52 | 197.91 |
| H₂O(g) | −241.82 | 188.83 |
| H₂(g) | 0 | 130.59 |

**8-2** 上述两种工艺产生的少量 CO 会吸附在燃料电池的 Pt 或其他贵金属催化剂表面，阻碍 H₂ 的吸附和电氧化，引起燃料电池放电性能急剧下降，为此，开发了除去 CO 的方法。现有一组实验结果（500 K）如下：

$$\mathrm{CO(g) + \tfrac{1}{2}O_2(g) \longrightarrow CO_2(g)}$$

| p_CO/p^θ | p_O₂/p^θ | r_CO/(分子数·Ru 位⁻¹ s⁻¹) | p_CO/p^θ | p_O₂/p^θ | r_CO |
|---|---|---|---|---|---|
| 0.005 | 0.01 | 20.5 | 0.01 | 0.010 | 7 |
| 0.010 | 0.01 | 7.0 | 0.01 | 0.070 | 50 |
| 0.017 | 0.01 | 5.0 | 0.01 | 0.090 | 65 |
| 0.048 | 0.01 | 2.0 | 0.01 | 0.12 | 80 |
| 0.080 | 0.01 | 1.1 | | | |

(1) 求催化剂 Ru 上 CO 氧化反应分别对 CO 和 O₂ 的反应级数（取整数），写出速率方程。

(2) 假设 CO 和 O₂ 的吸附与脱附互不影响，且表面均匀，θ 表示覆盖度，气体的吸附速率与气体压力和空活性位数成正比。研究提出机理：

$$\mathrm{CO + M \underset{k_{\mathrm{CO,des}}}{\overset{k_{\mathrm{CO,ads}}}{\rightleftharpoons}} OC-M}$$

$$\mathrm{O_2 + 2M \xrightarrow{k_{\mathrm{O_2,ads}}} 2O-M}$$

$$\mathrm{OC-M + O-M \longrightarrow CO_2 + 2M}$$

其中 CO 在 Ru 活性位的吸附比 O₂ 强得多。试根据上述反应机理推导 CO 氧化反应的速率方程（不考虑 O₂ 脱附；也不考虑产物 CO₂ 的吸附），并与实验结果比较。

**8-3** 有关物质的热力学函数（298.15 K）如下：

| 物质 | ΔfH^θₘ / kJ·mol⁻¹ | S^θₘ / J·K⁻¹·mol⁻¹ |
|---|---|---|
| H₂(g) | 0 | 130.59 |
| O₂(g) | 0 | 205.03 |
| H₂O(g) | −241.82 | 188.83 |
| H₂O(l) | −285.84 | 69.94 |

在 373.15 K、100 kPa 下，水的蒸发焓 ΔvapH^θₘ = 40.64 kJ·mol⁻¹，在 298.15~373.15 K 间水的等压热容为 75.6 J·K⁻¹·mol⁻¹。

(1) 将工艺得到的富氢气体作为 PEMFC 的燃料。燃料电池的理论效率是指电池所能做的最大电功相对于燃烧反应焓变的效率。在 298.15 K、100 kPa 下，当 1 mol H₂ 燃烧分别生成 H₂O(l) 和 H₂O(g) 时，计算燃料电池工作的理论效率，并分析两者存在差别的原因。

(2) 若燃料电池在 473.15 K、100 kPa 下工作，其理论效率又为多少（可忽略焓变和熵变随温度的变化）？

(3) 说明 (1) 和 (2) 中的同一反应有不同理论效率的原因。

<details>
<summary>📖 查看答案与解析</summary>

**8-1** 化学方程式：

甲醇水蒸气变换（重整）：

$$\mathrm{CH_3OH(g) + H_2O(g) = CO_2(g) + 3H_2(g)} \quad \text{(a)}$$

甲醇部分氧化：

$$\mathrm{CH_3OH(g) + \tfrac{1}{2}O_2(g) = CO_2(g) + 2H_2(g)} \quad \text{(b)}$$

以上两种工艺都有副反应：

$$\mathrm{CO_2(g) + H_2(g) = CO(g) + H_2O(g)} \quad \text{(c)}$$

热效应计算：

$$\Delta_\mathrm{r}H^\theta_\mathrm{m}(\mathrm{a}) = -393.51 + 200.66 + 241.82 = +48.97\ \mathrm{kJ\cdot mol^{-1}}$$

$$\Delta_\mathrm{r}H^\theta_\mathrm{m}(\mathrm{b}) = -393.51 + 200.66 = -192.85\ \mathrm{kJ\cdot mol^{-1}}$$

反应 (a) 吸热需提供热源（缺点）；H₂ 收率高（优点）。

反应 (b) 放热可自行维持（优点）；H₂ 收率较低，且被空气中 N₂ 稀释使产品 H₂ 浓度较低（缺点）。

**8-2**

(1) 速率方程：$r_\mathrm{CO} = k p_\mathrm{CO}^\alpha p_{\mathrm{O_2}}^\beta$

将数据作 $\ln r_\mathrm{CO} \sim \ln p_\mathrm{CO}$ 与 $\ln r_\mathrm{CO} \sim \ln p_{\mathrm{O_2}}$ 图，得斜率 $\alpha \approx -1$，$\beta \approx 1$。速率方程：

$$-\mathrm{d}p_\mathrm{CO}/\mathrm{d}t = k p_{\mathrm{O_2}}/p_\mathrm{CO}$$

(2) 机理推导：吸附/脱附平衡：

$$r_\mathrm{CO,ads} = k_{\mathrm{CO,ads}} p_\mathrm{CO} \theta_\mathrm{V}$$

$$r_{\mathrm{O_2,ads}} = k_{\mathrm{O_2,ads}} p_{\mathrm{O_2}} \theta_\mathrm{V}^2$$

$$r_\mathrm{CO,des} = k_\mathrm{CO,des} \theta_\mathrm{CO}$$

稳态近似 + 表面反应速率控制 + CO 强吸附 $\theta_\mathrm{CO} \approx 1$：

$$r_{\mathrm{CO_2}} = 2k_{\mathrm{O_2,ads}} p_{\mathrm{O_2}} \theta_\mathrm{V} = \frac{2k_{\mathrm{O_2,ads}} k_{\mathrm{CO,des}}}{k_{\mathrm{CO,ads}}} \cdot \frac{p_{\mathrm{O_2}}}{p_\mathrm{CO}}$$

令 $k = 2k_{\mathrm{O_2,ads}}k_{\mathrm{CO,des}}/k_{\mathrm{CO,ads}}$：

$$r_\mathrm{CO} = k p_{\mathrm{O_2}}/p_\mathrm{CO}$$

与实验结果一致。

**8-3**

(1) H₂(g) + ½O₂(g) → H₂O(l)：

$$\Delta_\mathrm{r}H^\theta_\mathrm{m}(\mathrm{a}) = -285.84\ \mathrm{kJ\cdot mol^{-1}}$$

$$\Delta_\mathrm{r}S^\theta_\mathrm{m}(\mathrm{a}) = 69.94 - 130.59 - \tfrac{1}{2}\times 205.03 = -163.17\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$$

$$\Delta_\mathrm{r}G^\theta_\mathrm{m}(\mathrm{a}) = -285.84 - 298.15\times (-163.17)\times 10^{-3} = -237.19\ \mathrm{kJ\cdot mol^{-1}}$$

$$\eta(\mathrm{a}) = \Delta_\mathrm{r}G^\theta_\mathrm{m}(\mathrm{a})/\Delta_\mathrm{r}H^\theta_\mathrm{m}(\mathrm{a}) = 83.0\%$$

H₂(g) + ½O₂(g) → H₂O(g)：

$$\Delta_\mathrm{r}H^\theta_\mathrm{m}(\mathrm{b}) = -241.82\ \mathrm{kJ\cdot mol^{-1}}$$

$$\Delta_\mathrm{r}S^\theta_\mathrm{m}(\mathrm{b}) = 188.83 - 130.59 - 205.03/2 = -44.28\ \mathrm{J\cdot K^{-1}\cdot mol^{-1}}$$

$$\Delta_\mathrm{r}G^\theta_\mathrm{m}(\mathrm{b}) = -241.82 - 298.15\times (-44.28)\times 10^{-3} = -228.63\ \mathrm{kJ\cdot mol^{-1}}$$

$$\eta(\mathrm{b}) = \Delta_\mathrm{r}G^\theta_\mathrm{m}(\mathrm{b})/\Delta_\mathrm{r}H^\theta_\mathrm{m}(\mathrm{b}) = 94.5\%$$

两反应 ΔG^θₘ 接近（最大电能相近），ΔH^θₘ 相差大（释放热能不同），故 η 不同。

(2) 在 473.15 K 下（忽略 ΔH^θ、ΔS^θ 随温度变化）：

$$\Delta_\mathrm{r}G^\theta_\mathrm{m}(\mathrm{b}) = -241.82 + 473.15\times 44.28\times 10^{-3} = -220.88\ \mathrm{kJ\cdot mol^{-1}}$$

$$\eta(\mathrm{b}, 473\ \mathrm K) = -220.88/-241.82 = 91.3\%$$

(3) 燃料电池理论效率随工作温度而变化；温度降低则 η 升高。ΔG^θₘ 随温度变化主要由 TΔS^θₘ 引起。

</details>

<!-- 校勘注: ①8-1 ΔrH(a) 验算：-393.51+200.66+241.82=48.97 ✓ 吸热（CO₂+3H₂ 产物侧能量高于 CH₃OH+H₂O 反应物侧，需外加热源）；②8-2 速率方程机理推导 r_CO = k p_O₂/p_CO 与实验对 CO 负一级、对 O₂ 正一级吻合；③8-3 ΔΔH = ΔrH^θ(b) − ΔrH^θ(a) = -241.82 − (-285.84) = 44.02 kJ/mol ≈ H₂O 蒸发焓 40.64 kJ/mol（题给）+CpΔT = 75.6×75 = 5670 J ≈ 5.7 kJ/mol 之和 46.3 kJ/mol，源答案 44.0 与精确 46.3 略有偏差，按源答案照录。 -->

## 知识点映射

| 知识点 | 本题应用 |
|---|---|
| [[反应热与盖斯定律]] | ΔrH^θ 计算 |
| [[反应速率]] | 速率方程对 CO/O₂ 级数判定 |
| [[吸附]] | Langmuir 吸附等温线 + 表面机理推导 |
| [[Gibbs自由能]] | ΔG^θ=−RT ln K、燃料电池效率 |
| [[热力学第一定律]] | ΔH^θ/ΔS^θ/ΔG^θ 关系 |