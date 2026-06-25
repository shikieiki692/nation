---
title: Nernst方程
aliases: [Nernst Equation, 能斯特方程]
type: 知识点
template_version: v1.3
subject: 化学原理
module: 化学原理
submodule: 电化学
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-化学原理
syllabus_code: [8, 决赛10]
syllabus_module: [化学原理]
tags: [化竞, 电化学]
related: [标准电极电势, Gibbs自由能, 平衡常数, 原电池, 电解池]
prerequisite: [氧化还原, Gibbs自由能, 平衡常数]
problem_types: [题型-电极电势计算, 题型-电动势计算]
difficulty: 4
importance: 5
status: 已填充
stage: published
sources: [提炼-普化原理-第10章-氧化还原电化学, 教学逻辑提炼-周坤无机新课-酸碱理论与电化学-第一轮, 专题-氧化还原与电化学, 专题-电化学计算]
source_type: [书籍提炼, 教学逻辑提炼, 专题归纳, 专题归纳]
source_notes:
  - "[[提炼-普化原理-第10章-氧化还原电化学]]"
  - "[[教学逻辑提炼-周坤无机新课-酸碱理论与电化学-第一轮]]"
  - "[[专题-氧化还原与电化学]]"
  - "[[专题-电化学计算]]"
  - "[[04-课件/新授课/2026-06-02-电化学-基础班]]"
review_cycle: 30d
has_images: false
image_count: 0
images_priority: low
images_note: 建议配图：Nernst方程变量示意、浓差电池示意、pH/浓度改变导致电势变化的直观图。当前可先由板书推导与课件数轴承担。
teaching_ready: false
key_images: []
teaching_insight: "[[教学洞察-Nernst方程]]"
updated: 2026-06-01
source_extracts:
  - source_file: "[[教学逻辑提炼-周坤无机新课-酸碱理论与电化学-第一轮]]"
    asset_id: "B2-9"
    asset_type: "实例资产"
    asset_summary: "沉淀对电极电势的影响：Ag+/Ag (0.7996 V) -> AgCl/Ag (0.2223 V)，经典演示"
    target_section: "§十二"
  - source_file: "[[教学逻辑提炼-Zchem-电化学-第一轮]]"
    asset_id: "12"
    asset_type: "机理资产"
    asset_summary: "Nernst方程推导链：ΔG=-nFE 与 ΔG=ΔG°+RTlnQ 联立得到 E=E°-(RT/nF)lnQ，适合放在课堂推导主线。"
    target_section: "§三"
    date: "2026-06-18"
    status: "已回流"
---

# Nernst 方程

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-化学原理]]
- 对应考纲条目：[[08-氧化还原与电化学]]

## 一、定义
**Nernst 方程**描述了**非标准态下**电极电势与浓度的关系：

$$E = E^\circ - \frac{RT}{nF} \ln Q$$

25°C 时：
$$E = E^\circ - \frac{0.0592}{n} \lg Q$$

## 二、考纲对应
- 对应考纲条目：[[08-氧化还原与电化学]]
- 所属模块：[[基础要求-化学原理]]
- 本知识点在考纲中的作用：连接标准电极电势、原电池/电解池与平衡常数计算，是第一轮电化学计算的核心公式页。

## 三、核心原理

### 推导：从 ΔG 到 E
$$\Delta_r G = \Delta_r G^\circ + RT \ln Q$$
$$\Delta_r G = -nFE$$
$$\Rightarrow E = E^\circ - \frac{RT}{nF} \ln Q$$

### 对于电极反应
$a\mathrm{Ox} + ne^- \rightleftharpoons b\mathrm{Red}$：
$$E = E^\circ - \frac{0.0592}{n} \lg\frac{[\mathrm{Red}]^b}{[\mathrm{Ox}]^a}$$

或等价地：
$$E = E^\circ + \frac{0.0592}{n} \lg\frac{[\mathrm{Ox}]^a}{[\mathrm{Red}]^b}$$

## 四、关键结论

### 浓度对电动势的影响
- 浓度商（反应物/产物比）↑ → E ↑
- pH 影响含 H⁺/OH⁻ 的半反应

### 浓差电池
- 两个相同电极在不同浓度下的电池
- $E_\text{cell} = \frac{0.0592}{n} \lg\frac{c_\text{浓}}{c_\text{稀}}$（无标准电势项）

### Nernst 方程求 K
平衡时 E = 0：
$$\lg K = \frac{nE^\circ}{0.0592}$$
$$K = 10^{nE^\circ / 0.0592}$$

### 竞赛常见考法
- 用 Nernst 方程判断氧化剂/还原剂强弱随 pH 的变化
- 用 Nernst 方程分析沉淀/络合对电极电势的影响
- 计算非标准条件下的电池电动势

## 五、常见分类或情形

### 按应用场景
| 场景 | Nernst 方程形式 | 典型题型 |
|------|------|------|
| 单电极电势 | $E = E^\circ \pm \frac{0.0592}{n}\lg\frac{[\text{Ox}]}{[\text{Red}]}$ | 浓度/分压对 E 的影响 |
| 电池电动势 | $E_\text{cell} = E_\text{cell}^\circ - \frac{0.0592}{n}\lg Q$ | 非标态电池计算 |
| 浓差电池 | $E = \frac{0.0592}{n}\lg\frac{c_1}{c_2}$ | 同种电极不同浓度 |
| 求平衡常数 | $\lg K = \frac{nE^\circ}{0.0592}$ | Ksp, Kf, Ka 的电化学测定 |

### pH 对电极电势的影响
对于含 H⁺ 或 OH⁻ 的半反应：
- 氧化型含 H⁺：pH↑ → E↓（酸性条件下氧化性更强）
- 还原型含 H⁺：pH↑ → E↑（碱性条件下还原性更强）
- 实例：MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O，E 随 pH 降低显著升高

### 沉淀剂/络合剂的影响
- 加入沉淀剂降低某离子浓度 → E 改变（用 Nernst 方程配合 Ksp）
- 加入络合剂降低某离子浓度 → E 改变（用 Nernst 方程配合 Kf）
- 这是竞赛中判断氧化还原反应方向变化的核心方法

## 六、适用条件与限制
- ✅ 适用于稀溶液（活度 ≈ 浓度）
- ✅ 适用于可逆电极过程
- ⚠️ 浓溶液中需用活度代替浓度（竞赛一般不要求）
- ⚠️ 不可逆电极（如 Fe²⁺/Fe³⁺ 在 Pt 电极上）实际电势可能偏离计算值
- ⚠️ 气体用分压（bar），纯固体/液体活度为 1
- ⚠️ 25°C 时系数为 0.0592，其他温度需重新计算（RT/F·ln10）

## 七、常见比较与易混点
| 易混点 | 区分 |
|------|------|
| E vs E° | E°是标准态（1 mol/L, 1 bar, 25°C），E 是任意条件 |
| Nernst 方程的两种写法 | $E = E^\circ - \frac{0.0592}{n}\lg Q$ 和 $E = E^\circ + \frac{0.0592}{n}\lg\frac{[\text{Ox}]}{[\text{Red}]}$ 等价，注意 Q 的定义 |
| 电池电动势 vs 电极电势 | $E_\text{cell} = E_\text{正} - E_\text{负}$，各自用 Nernst 方程计算 |
| 浓差电池的 E° | 浓差电池的 E°=0（两电极相同），电动势完全来自浓度差 |
| Nernst 方程 vs ΔG | ΔG < 0 判断自发方向；E > 0 等价于 ΔG < 0 |

## 八、与其他知识点的联系
- 前置知识：[[氧化态]]、[[氧化还原反应方程式配平]]、[[Gibbs自由能]]、[[平衡常数]]
- 相关知识：[[标准电极电势]]、[[原电池]]、[[电解池]]、[[反应商]]
- 应用知识：[[溶度积]]（Ksp 的测定）、[[稳定常数]]（Kf 的测定）、[[酸碱平衡]]（pH 对氧化还原的影响）

## 九、典型题型
- 题型-电极电势计算
- 题型-电池电动势计算
- 题型-氧化还原方向判断
- 题型-沉淀/络合对电势的影响

## 十、例题
### 例题 1：非标态电极电势
**题目：** 计算 [Zn²⁺] = 0.010 mol/L 时 Zn²⁺/Zn 电极的电极电势（25°C，E° = −0.763 V）。

**分析：** Zn²⁺ + 2e⁻ → Zn。n = 2。还原型 Zn 为固体，活度 = 1。

**解答：**
$$E = E^\circ + \frac{0.0592}{2}\lg[Zn^{2+}] = -0.763 + 0.0296 \times (-2) = -0.822 \text{ V}$$

**反思：** Zn²⁺ 浓度降低 → 还原倾向减弱 → E 变得更负。符合 Le Châtelier 原理。

### 例题 2：Nernst 方程求 Ksp
**题目：** 已知 Ag⁺/Ag E° = +0.799 V，AgCl/Ag E° = +0.222 V。求 AgCl 的 Ksp。

**分析：** AgCl/Ag 的 E° 对应 [Cl⁻] = 1 mol/L 时 [Ag⁺] = Ksp。将此 [Ag⁺] 代入 Nernst 方程。

**解答：**
Ag⁺ + e⁻ → Ag：$E = 0.799 + 0.0592\lg[Ag^+]$
当 [Cl⁻] = 1，[Ag⁺] = Ksp 时，E = E°(AgCl/Ag) = 0.222：
$$0.222 = 0.799 + 0.0592\lg K_{sp}$$
$$\lg K_{sp} = \frac{0.222 - 0.799}{0.0592} = -9.75$$
$$K_{sp} = 1.8 \times 10^{-10}$$

**反思：** 这是电化学测定 Ksp 的标准方法——利用两个相关电极的 E° 差值。

### 例题 3：pH 对氧化能力的影响
**题目：** 计算 pH = 5 时 MnO₄⁻/Mn²⁺ 的电极电势（[MnO₄⁻] = [Mn²⁺] = 1 mol/L, E° = +1.51 V）。

**分析：** MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O。n = 5，H⁺ 参与反应。

**解答：**
$$E = 1.51 + \frac{0.0592}{5}\lg\frac{[MnO_4^-][H^+]^8}{[Mn^{2+}]}$$
$$= 1.51 + \frac{0.0592}{5}\lg(10^{-5})^8 = 1.51 + \frac{0.0592}{5} \times (-40)$$
$$= 1.51 - 0.474 = 1.04 \text{ V}$$

**反思：** pH 从 0 升到 5，E 下降了约 0.47 V——酸性减弱显著降低 MnO₄⁻ 的氧化性。这在分析化学中选择反应条件时至关重要。

## 十一、易错点
- **❌ 错：** 混淆 Nernst 方程中 ± 号 → 氧化型在分子 / 还原型在分母 → E = E° + (0.0592/n)lg([Ox]/[Red])
- **❌ 错：** 忘记气体用分压、纯固体/液体活度为 1
- **❌ 错：** 电池电动势直接用浓度代入 → 应先分别算两个电极的 E，再相减
- **❌ 错：** 浓差电池也带 E° 项 → E° 相消为零
- **❌ 错：** 在非 25°C 时仍用 0.0592 → 系数 = RT/F·ln10，随温度变化

> **来源标注（B2-9）**：以下沉淀对电极电势影响的实例来源于周坤 2020 无机新课课堂笔记（第 13 讲），是 Nernst 方程灵活应用的经典演示。

### 沉淀对电极电势的影响实例

**Ag⁺/Ag 电对受 Cl⁻ 沉淀的影响**

已知：$E°(\mathrm{Ag^+/Ag}) = +0.7996\ \mathrm{V}$

当溶液中加入 Cl⁻ 使 Ag⁺ 沉淀为 AgCl 时：
$$\mathrm{AgCl + e^- \rightleftharpoons Ag + Cl^-} \quad E°(\mathrm{AgCl/Ag}) = +0.2223\ \mathrm{V}$$

**电势变化分析**：
- Ag⁺ 被沉淀后，游离 [Ag⁺] 急剧下降
- 根据 Nernst 方程：$E = E°(\mathrm{Ag^+/Ag}) + 0.0592\lg[\mathrm{Ag^+}]$
- 当 [Cl⁻] = 1 mol/L 时，[Ag⁺] = Ksp(AgCl)/[Cl⁻] = 1.8×10⁻¹⁰ mol/L
- $E = 0.7996 + 0.0592\lg(1.8\times10^{-10}) = 0.7996 - 0.577 = +0.222\ \mathrm{V}$
- 与 AgCl/Ag 的标准电极电势一致

**教学意义**：此例直观展示了 Nernst 方程的灵活性——沉淀反应通过改变离子浓度来调控电极电势，是竞赛中"电化学 + 沉淀平衡"联用计算的典型模型。

## 十二、竞赛拓展
- **Pourbaix 图（E-pH 图）**：以 pH 为横坐标、E 为纵坐标，显示某元素各物种的稳定区域。竞赛中常给图要求分析。
- **Frost 图与 Latimer 图**：Frost 图（nE° vs 氧化态）和 Latimer 图（逐步电势链），用于判断歧化/归中反应。
- **离子选择性电极**：玻璃电极（pH 计）的原理就是 Nernst 方程——膜电势与 H⁺ 浓度对数成正比。

## 十三、外部资料出处
- [[提炼-普化原理-第10章-氧化还原电化学]]
- [[教学逻辑提炼-周坤无机新课-酸碱理论与电化学-第一轮]]
- [[教学逻辑提炼-Zchem-电化学-第一轮]]
- [[专题-氧化还原与电化学]]
- [[专题-电化学计算]]

## 十四、待完善项
- [ ] 补充 Pourbaix 图的读图例题
- [ ] 补充 Latimer 图/Frost 图的使用方法
- [ ] 补充初赛/决赛真题 3 道

---

## 相关真题

```dataview
TABLE file.name AS "文件名", year AS "年份", type AS "题型", difficulty AS "难度"
FROM "04-题库"
WHERE contains(knowledge_points, "Nernst方程")
SORT year DESC, difficulty ASC
```
