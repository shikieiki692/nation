---
title: Gibbs自由能
aliases: [Gibbs Free Energy, G, 自由能, 吉布斯自由能]
type: 知识点
template_version: v1.3
subject: 化学原理
module: 化学原理
submodule: 热力学
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-化学原理
syllabus_code: [6]
syllabus_module: [化学原理]
tags: [化竞, 热力学]
related: [焓, 熵, 标准态, 平衡常数, 化学势, Nernst方程]
prerequisite: [焓, 熵]
problem_types: [题型-自发反应判断, 题型-ΔG计算]
difficulty: 4
importance: 5
status: 已填充
stage: published
sources:
  - 提炼-普化原理-第5章-化学热力学
  - 教学逻辑提炼-周坤无机新课-热力学与化学平衡-第一轮
  - 专题-热力学初步
source_type:
  - 教材提炼
  - 教学逻辑提炼
  - 专题归纳
source_notes:
  - "[[提炼-普化原理-第5章-化学热力学]]"
  - "[[07-资料提炼/教学逻辑提炼/无机化学-周坤-2020/教学逻辑提炼-周坤无机新课-热力学与化学平衡-第一轮]]"
  - "[[专题-热力学初步]]"
  - "[[04-课件/新授课/2026-06-02-热力学初步-基础班]]"
review_cycle: 30d
has_images: false
image_count: 0
images_priority: low
images_note: 纯公式与概念型 KP，文字表达足够。
teaching_ready: true
key_images: []
updated: 2026-06-18
source_extracts:
  - source_file: "[[提炼-普化原理-第5章-化学热力学]]"
    asset_id: "Ch5-G"
    asset_type: "教材提炼"
    asset_summary: "系统覆盖 ΔG=ΔH−TΔS、ΔG 与 K、ΔG 与最大非体积功及自发性判据，是热力学课堂主来源。"
    target_section: "§三-§十二"
  - source_file: "[[教学逻辑提炼-周坤无机新课-热力学与化学平衡-第一轮]]"
    asset_id: "B1-8"
    asset_type: "实例资产"
    asset_summary: "'吸热却自发'反例：NH₄Cl(s) + Ba(OH)₂·8H₂O(s)，经典演示实验"
    target_section: "§十二"
  - source_file: "[[教学逻辑提炼-周坤无机新课-热力学与化学平衡-第一轮]]"
    asset_id: "B1-9"
    asset_type: "实例资产"
    asset_summary: "'放热但不自发'反例：H₂ + ½O₂ 需点燃，笔记明确提及"
    target_section: "§十二"
---

# Gibbs 自由能

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-化学原理]]
- 对应考纲条目：[[06-热力学初步]]

## 一、定义
**Gibbs 自由能（G）**：$G = H - TS$。在恒温恒压且不做非体积功的条件下，**ΔG < 0 的反应自发进行**。

- ΔG < 0：自发（Exergonic）
- ΔG = 0：平衡
- ΔG > 0：非自发（Endergonic）

## 二、考纲对应
- 对应考纲条目：[[06-热力学初步]]
- 要求层级：理解 $\Delta G=\Delta H-T\Delta S$ 的意义，能用 $\Delta G$ 判断反应方向并与平衡常数、电化学联系
- 课堂定位：是 [[焓]]、[[熵]] 之后的总判据页，也是 [[平衡常数]]、[[Nernst方程]] 与 [[化学电源]] 的桥梁页

## 三、核心原理

### 定义与基本关系
Gibbs 自由能 $G$ 由 J. W. Gibbs 于 1876 年提出，定义为：

$$G = H - TS$$

在等温条件下，Gibbs 自由能变化为 **Gibbs-Helmholtz 方程**：

$$\Delta G = \Delta H - T\Delta S \tag{5.13}$$

### 自发性的判断（恒温恒压、不做非体积功）
- **$\Delta G < 0$**：正向自发（exergonic）
- **$\Delta G = 0$**：反应达到平衡
- **$\Delta G > 0$**：正向不自发，逆向自发（endergonic）

| $\Delta H$ | $\Delta S$ | $\Delta G$ 行为 | 自发条件 |
|:---:|:---:|------|------|
| − | + | 恒为 − | 任何温度正向自发 |
| + | − | 恒为 + | 任意温度正向不自发 |
| − | − | 高温 +，低温 − | 低温正向自发 |
| + | + | 高温 −，低温 + | 高温正向自发 |

**转变温度**（$\Delta G = 0$ 时）：$T_{\text{转}} = \dfrac{\Delta H}{\Delta S}$

### $\Delta G$ 的物理意义：最大有用功
在恒温恒压可逆过程中，$\Delta G$ 等于体系所做的**最大非体积功**（其他功 $W'$）：

$$\Delta G = W' \quad (\text{等温、等压})$$

- 若 $\Delta G < 0$，体系能对环境做有用功（如 $\mathrm{CH_4}$ 燃烧 $\Delta G^\circ = -818\ \mathrm{kJ \cdot mol^{-1}}$，理想燃料电池最多输出 $818\ \mathrm{kJ}$）
- 若 $\Delta G > 0$，环境需对体系做有用功（如 $\mathrm{H_2O}$ 电解 $\Delta G^\circ = +237\ \mathrm{kJ \cdot mol^{-1}}$，至少输入 $237\ \mathrm{kJ}$ 电功）

### $\Delta G$ 与平衡常数的关系
$$\Delta_{\mathrm{r}} G^\circ = -RT \ln K$$
$$\Delta_{\mathrm{r}} G = \Delta_{\mathrm{r}} G^\circ + RT \ln Q$$

$Q < K$ 时 $\Delta G < 0$，正向自发；$Q = K$ 时 $\Delta G = 0$，平衡；$Q > K$ 时 $\Delta G > 0$，逆向自发。

### $\Delta G$ 与电化学
$$\Delta_{\mathrm{r}} G^\circ = -nFE^\circ$$

这是连接热力学与电化学的桥梁。$E^\circ > 0$ 则 $\Delta G^\circ < 0$，反应自发。

## 四、关键结论

### 标准摩尔生成 Gibbs 自由能
在标态和温度 $T$ 条件下，由指定单质生成 $1\ \mathrm{mol}$ 某种物质时的 Gibbs 自由能变，符号 $\Delta_{\mathrm{f}}G_{\mathrm{m}}^{\ominus}(T)$，单位 $\mathrm{kJ \cdot mol^{-1}}$。指定单质的 $\Delta_{\mathrm{f}}G_{\mathrm{m}}^{\ominus} = 0$。

$$\Delta_{\mathrm{f}} G^\circ = \Delta_{\mathrm{f}} H^\circ - T\Delta_{\mathrm{f}} S^\circ$$

**规律**：绝大多数物质的 $\Delta_{\mathrm{f}}G_{\mathrm{m}}^{\ominus}$ 为负值（稳定化合物），只有少数为正（如 $\mathrm{NO_2}$、$\mathrm{HI}$ 等不稳定化合物），这与 $\Delta_{\mathrm{f}}H_{\mathrm{m}}^{\ominus}$ 的情况相似。

### 由标准生成 Gibbs 自由能计算反应 $\Delta_{\mathrm{r}}G^\circ$

$$\Delta_{\mathrm{r}} G_{\mathrm{m}}^{\ominus} = \sum \nu_i \Delta_{\mathrm{f}} G_{\mathrm{m}}^{\ominus} (\text{生成物}) - \sum \nu_i \Delta_{\mathrm{f}} G_{\mathrm{m}}^{\ominus} (\text{反应物}) \tag{5.14}$$

**课本实例**：298 K 标态下甲烷燃烧

$$\mathrm{CH_4(g) + 2O_2(g) \longrightarrow CO_2(g) + 2H_2O(l)}$$

$$\begin{aligned} \Delta G^\circ &= \Delta G_{\mathrm{f}}^\circ(\mathrm{CO_2,g}) + 2 \times \Delta G_{\mathrm{f}}^\circ(\mathrm{H_2O,l}) - \big[\Delta G_{\mathrm{f}}^\circ(\mathrm{CH_4,g}) + 2 \times \Delta G_{\mathrm{f}}^\circ(\mathrm{O_2,g})\big] \\ &= [-394.4 + 2 \times (-237.1) - (-50.5) + 0]\ \mathrm{kJ \cdot mol^{-1}} \\ &= -818.1\ \mathrm{kJ \cdot mol^{-1}} \end{aligned}$$

$\Delta G^\circ < 0$，说明在标态、298 K 条件下甲烷燃烧可以自发进行。

### Gibbs-Helmholtz 方程及其图解法
$$\Delta G = \Delta H - T\Delta S$$

以 $\Delta_{\mathrm{r}}G_{\mathrm{m}}^{\ominus}$ 对 $T$ 作图（如课本图 5.7：$\mathrm{CaCO_3 \to CaO + CO_2}$），得一直线：
- **截距** = $\Delta_{\mathrm{r}}H_{\mathrm{m}}^{\ominus}$（该反应为 $+179\ \mathrm{kJ \cdot mol^{-1}}$）
- **斜率** = $-\Delta_{\mathrm{r}}S_{\mathrm{m}}^{\ominus}$（该反应为 $-0.16\ \mathrm{kJ \cdot mol^{-1} \cdot K^{-1}}$）

### 耦合反应
- 将一个 $\Delta G > 0$ 的反应与 $\Delta G \ll 0$ 的反应耦合 $\to$ 总体可行
- 生化实例：ATP 水解（$\Delta G^{\circ\prime} \approx -30.5\ \mathrm{kJ \cdot mol^{-1}}$）驱动吸能反应

## 五、常见分类或情形

### 标态 $\Delta G^\circ$ 与非标态 $\Delta G$

| | $\Delta G^\circ$ | $\Delta G$ |
|:---|------|------|
| **条件** | 所有物质均处于标准状态 | 任意压力、浓度条件 |
| **标准状态定义** | 气体 $p = p^\ominus = 1 \times 10^5\ \mathrm{Pa}$ (1 bar)；溶液 $c \approx 1\ \mathrm{mol \cdot dm^{-3}}$；纯液体/固体为标压下纯物质 | — |
| **计算** | 由 $\Delta_{\mathrm{f}}G^\circ$ 计算 | $\Delta G = \Delta G^\circ + RT \ln Q$ |
| **用途** | 计算平衡常数 $K$，比较不同反应的自发倾向 | 判断实际条件（非标态）下反应方向 |

### 温度依赖性：四类反应（课本表 5.5）

| 类型 | $\Delta H^\circ$ | $\Delta S^\circ$ | 低温 | 高温 | 课本实例 |
|:---:|:---:|:---:|:---:|:---:|------|
| 1. 焓降熵增 | − | + | 自发 | 自发 | 丁烯氧化脱氢 $\mathrm{C_4H_8 + \frac{1}{2}O_2 \to C_4H_6 + H_2O}$，$\Delta H^\circ = -77$，$\Delta S^\circ = +72$ |
| 2. 焓增熵减 | + | − | 不自发 | 不自发 | CO 分解 $\mathrm{CO \to C + \frac{1}{2}O_2}$，$\Delta H^\circ = +111$，$\Delta S^\circ = -90$ |
| 3. 焓增熵增 | + | + | 不自发 | 自发 | $\mathrm{N_2 + O_2 \to 2NO}$，$\Delta H^\circ = +183$，$\Delta S^\circ = +25$，$T_{\text{转}} \approx 7300\ \mathrm{K}$ |
| 4. 焓降熵减 | − | − | 自发 | 不自发 | $\mathrm{N_2 + 3H_2 \to 2NH_3}$，$\Delta H^\circ = -91.8$，$\Delta S^\circ = -198$，$T_{\text{转}} \approx 464\ \mathrm{K}$ |

### 温度与压力的综合影响：$\mathrm{CaCO_3}$ 分解（课本表 5.4）

$$\mathrm{CaCO_3(s) \longrightarrow CaO(s) + CO_2(g)}$$

| $T$ / K | $p = 100$ kPa | $p = 1$ kPa | $p = 10^{-2}$ kPa | $p = 10^{-4}$ kPa |
|:---:|:---:|:---:|:---:|:---:|
| 298 | +132 | +121 | +109 | +98 |
| 673 | +72 | +47 | +20 | −5 |
| 873 | +40 | +8 | −27 | −60 |
| 1073 | +8 | −32 | −75 | −114 |
| 1273 | −24 | −71 | −122 | −169 |

规律：
- 温度升高，$\Delta G$ 减小（因 $\Delta S > 0$，分解产气体，熵增）
- 压力降低（抽走 $\mathrm{CO_2}$），$\Delta G$ 减小
- 敞口石灰窑约 1100 K（$p = 100$ kPa 时 $\Delta G \approx 0$）自发分解；若抽气降压，约 900 K 即可分解

## 六、适用条件与限制

### 恒温恒压条件
- $\Delta G < 0$ 作为自发判据**严格适用于恒温、恒压、不做非体积功**的封闭体系
- 若条件不满足，需使用更普遍的判据（如总熵判据 $\Delta S_{\text{总}} > 0$）

### 标准状态的约定
- 气体：$p = p^\ominus = 1 \times 10^5\ \mathrm{Pa}$（1 bar，IUPAC 推荐）
- 溶液：溶质活度 $a = 1$（稀溶液可近似为 $c = 1\ \mathrm{mol \cdot dm^{-3}}$ 或 $b = 1\ \mathrm{mol \cdot kg^{-1}}$）
- 纯液体、纯固体：标准压力下的纯物质
- 指定稳定态单质的 $\Delta_{\mathrm{f}}G_{\mathrm{m}}^{\ominus} = 0$（如 C(石墨) = 0, C(金刚石) = +2.9 kJ/mol）

### $\Delta G^\circ$ 判断的局限性
- $\Delta G^\circ < 0$ 仅表示**标态下**反应有自发倾向，不能直接用于非标态条件
- $\Delta G^\circ < 0$ 且 $|\Delta G^\circ|$ 不大时，改变 $Q$ 可使反应逆转（通过浓度/分压调控）
- $\Delta G^\circ < 0$ 不保证反应实际发生——还需考虑**动力学因素**（反应速率）
- 课本例：丁烯 + 氧气 $\Delta G^\circ < 0$，但常温常压下混合并不反应，需催化剂

### 热力学与动力学的区分
$\Delta G$ 回答"能不能"的问题（方向与限度），不回答"快不快"的问题（速率）。两个层面不可混淆。

## 七、常见比较与易混点

### $\Delta G$ vs $\Delta G^\circ$

| | $\Delta G$ | $\Delta G^\circ$ |
|:---|------|------|
| **条件** | 任意实际条件 | 反应物和生成物均在标态 |
| **关系式** | $\Delta G = \Delta G^\circ + RT \ln Q$ | $\Delta G^\circ = -RT \ln K$ |
| **物理意义** | 实际条件下推动反应的能力 | 衡量反应的"天然倾向"（$K$ 的大小） |
| **符号判断** | $\Delta G < 0 \to$ 正向自发 | $\Delta G^\circ \ll 0 \to K \gg 1$，平衡偏向产物 |

### 自发性 vs 平衡
- **$\Delta G < 0$**：在此条件下正向自发，宏观上正向进行
- **$\Delta G = 0$**：反应达平衡（$Q = K$），宏观上不再进行
- **$\Delta G > 0$**：正向不自发，逆向自发
- 自发过程：一旦引发，无需外力便可自动进行，直到达到平衡；非自发过程则需外界持续作用
- 自发性是热力学概念，与速率无关

### $\Delta G$ 与最大有用功
恒温恒压下，$\Delta G = W'$（可逆过程中的最大非体积功）：
- $\Delta G < 0$：体系可对外做有用功，$|\Delta G|$ 为理论上可获取的最大功
  - 例：$1\ \mathrm{mol\ CH_4}$ 燃烧 $\Delta G^\circ = -818\ \mathrm{kJ}$，理想燃料电池最多输出 $818\ \mathrm{kJ}$；内燃机实际仅约 $200\ \mathrm{kJ}$；高效燃料电池约 $700\ \mathrm{kJ}$
- $\Delta G > 0$：必须对体系做至少 $|\Delta G|$ 的功才能驱动反应
  - 例：$1\ \mathrm{mol\ H_2O}$ 电解 $\mathrm{H_2O \to H_2 + \frac{1}{2}O_2}$，$\Delta G^\circ = +237\ \mathrm{kJ \cdot mol^{-1}}$，至少输入 $237\ \mathrm{kJ}$ 电功

### $\Delta H$ 判据 vs $\Delta G$ 判据
- 19 世纪 Berthelot 和 Thomson 曾主张用 $\Delta H$ 判断反应方向（放热 = 自发），大量实例支持
- 但存在反例：吸热也能自发进行
  - $\mathrm{Ba(OH)_2 \cdot 8H_2O(s) + 2NH_4SCN(s) \to Ba(SCN)_2(s) + 2NH_3(g) + 10H_2O(l)}$（吸热自发，熵增驱动）
  - $\mathrm{NH_4Cl(s)}$ 溶于水（吸热自发，$\Delta S^\circ = +75.3\ \mathrm{J \cdot mol^{-1} \cdot K^{-1}}$）
- 一般情况下 $\Delta H$ 项比 $T\Delta S$ 项对 $\Delta G$ 贡献更大（特别是 $\Delta S$ 很小的反应），所以用 $\Delta H$ 判断有相当可行性，但不完备
- **$\Delta G = \Delta H - T\Delta S$ 是综合考虑焓和熵的正确判据**

### $\Delta G$ 与电化学
$$\Delta_{\mathrm{r}} G^\circ = -nFE^\circ$$
- $E^\circ > 0 \iff \Delta G^\circ < 0 \iff$ 反应自发
- 这是联系热力学与电化学的纽带

## 八、与其他知识点的联系
- 前置知识：[[焓]]、[[熵]]
- 相关知识：[[平衡常数]]、[[化学势]]、[[标准态]]
- 应用知识：[[Nernst方程]]、[[化学电源]]、[[Ellingham图]]

## 九、典型题型
- 题型-由 $\Delta H,\Delta S$ 判断自发区间
- 题型-由 $\Delta G^\circ$ 求平衡常数
- 题型-由电池电动势反推 $\Delta G^\circ$

## 十、例题
**例题**：已知某反应 $\Delta H^\circ = 80\ \mathrm{kJ\cdot mol^{-1}}$，$\Delta S^\circ = 200\ \mathrm{J\cdot mol^{-1}\cdot K^{-1}}$，判断 298 K 与 600 K 下反应能否自发进行。  
**答案要点**：先统一单位：
$$\Delta G^\circ=\Delta H^\circ-T\Delta S^\circ=80-0.200T\quad (\mathrm{kJ\cdot mol^{-1}})$$
298 K 时 $\Delta G^\circ=20.4>0$，不自发；600 K 时 $\Delta G^\circ=-40<0$，自发。该反应属于“焓增熵增型”，高温有利。

## 十一、易错点
- 把 $\Delta G^\circ<0$ 误当成“任何条件都自发”，忽略实际还要看 $Q$
- 把“自发”误当成“反应立刻发生”，混淆热力学与动力学
- 计算时忘记把 $\Delta S$ 从 $\mathrm{J}$ 换成 $\mathrm{kJ}$，导致数量级错误
- 将 $\Delta G=0$ 理解成“反应停止”，而不是“达到动态平衡”

## 十二、🎯 教学视角

### 12.1 课堂引入实例（B1-8 / B1-9）

周坤课堂在引入 Gibbs 自由能判据时，使用了两组**认知冲突实例**来打破"放热=自发"的直觉：

### 12.2 第一轮讲授抓手
- 第一轮最有效的组织方式是“先破除放热判据迷信，再引出焓熵综合判据”
- 板书最好固定成三层：$\Delta G=\Delta H-T\Delta S$、$\Delta G$ 的符号与自发性、以及它和 $K/E^\circ$ 的联系
- 这样学生更容易把热力学、平衡和电化学串成一条线

### 12.3 与现实/直觉的连接
- 冰融化、盐溶解、石灰石分解都适合说明“不是只有放热才会自发”
- 可把 $\Delta G$ 类比成“真正能拿出来做事的那部分能量”，帮助学生区别它与总能量变化

## 十三、竞赛拓展
- Ellingham 图本质上就是若干反应 $\Delta G^\circ-T$ 直线的集合，可直接比较高温下氧化物稳定性
- 化学势视角下，$\Delta G$ 是各组分化学势按化学计量数组合后的结果，是更一般的表述
- 生化中的 ATP 耦合、材料中的电池电压、冶金中的还原判据，本质上都在用 Gibbs 自由能

## 十四、外部资料出处
- 主要来源：[[提炼-普化原理-第5章-化学热力学]]
- 教学组织参考：[[教学逻辑提炼-周坤无机新课-热力学与化学平衡-第一轮]]
- 课堂归纳参考：[[专题-热力学初步]]

## 十五、待完善项
- [ ] 后续可补一页“Ellingham 图读图模板”
- [ ] 后续可补“热力学 vs 动力学”对照示意图

---

## 相关真题（Dataview）

```dataview
TABLE
  question_type AS 题型,
  difficulty AS 难度,
  teaching_level AS 教学层级,
  source AS 来源
FROM "04-题库"
WHERE type = "题目"
  AND contains(knowledge_points, "Gibbs自由能")
SORT difficulty ASC, year DESC
```
