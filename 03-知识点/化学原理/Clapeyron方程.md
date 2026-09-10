---
type: 知识点
template_version: v1.3
subject: 化学原理
module: 化学原理
title: Clapeyron方程
aliases: [克拉佩龙方程, 克拉佩隆方程, 克劳修斯-克拉佩隆方程, Clausius-Clapeyron,
  Clausius-Clapeyron方程, "Clausius-Clapeyron 方程", 蒸气压, 相变温度, 蒸气压测定深化]
created: 2026-07-18
updated: 2026-09-03
tags: [化竞, 化学原理, 热力学]
syllabus_code: [决赛05]
source_extracts:
  - source_file: "[[07-资料提炼/书籍提炼/提炼-Atkins物理化学-主题04-纯物质的物理转变]]"
    asset_id: "Atkins主题04"
    asset_type: "书籍提炼"
    asset_summary: "纯物质物理转变教材主干，含相变热力学、克拉佩隆方程、蒸气压"
  - source_file: "[[07-资料提炼/赵鑫光-热力学-竞赛题集]]"
    asset_id: "赵鑫光-热力学-竞赛题集"
    asset_type: "题集提炼"
    asset_summary: "Clapeyron方程相关内容"
  - source_file: "[[07-资料提炼/习题提炼/习题-普化原理-第2章-气体]]"
    asset_id: "普化原理-第2章-气体"
    asset_type: "习题提炼"
    asset_summary: "Clapeyron方程相关内容"
  - source_file: "[[07-资料提炼/书籍提炼/提炼-普化原理-第2章-气体]]"
    asset_id: "普化原理-第2章-气体"
    asset_type: "书籍提炼"
    asset_summary: "Clapeyron方程相关内容"
status: 已填充
importance: 4
difficulty: 3
---

# Clapeyron方程

## 核心概念

Clapeyron方程描述纯物质两相平衡时**压力随温度的变化关系**：$dp/dT = \Delta_{\text{trans}}H/(T\Delta_{\text{trans}}V)$。
Clausius-Clapeyron方程为其近似形式（假设气相为理想气体、忽略凝聚相体积）。

- 适用于**所有**两相平衡（固-液、固-气、液-气），不限于液-气
- 是 [[范特霍夫方程]] 在相平衡中的具体应用
- 可用于计算不同压力下的相变温度

## 关键公式/方程式

### 克拉佩隆方程（精确形式）
$$\frac{dp}{dT} = \frac{\Delta_{\text{trans}}H}{T \Delta_{\text{trans}}V}$$

### 克劳修斯-克拉佩隆方程（近似形式，气相体积远大于凝聚相）
$$\ln \frac{p_2}{p_1} = -\frac{\Delta_{\text{vap}}H}{R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right)$$

### 微分形式
$$\frac{d \ln p}{dT} = \frac{\Delta_{\text{vap}}H}{RT^2}$$

## 规律与趋势

- 升温使蒸气压增大（蒸气压曲线斜率为正）
- 汽化热越大，蒸气压随温度变化越剧烈
- 外压增大使沸点升高
- 高海拔地区气压低，水的沸点低于100°C

## 相图两相线的斜率符号规则（竞赛核心）

由 $\frac{dp}{dT} = \frac{\Delta_{\text{trans}}H}{T\,\Delta_{\text{trans}}V}$，$T>0$，斜率符号完全由 $\Delta_{\text{trans}}H$ 与 $\Delta_{\text{trans}}V$ 的符号决定：

| 相界线 | $\Delta H$ | $\Delta V$ | 斜率 | 说明 |
|:--|:--:|:--:|:--:|:--|
| 液-气（蒸气压曲线） | $>0$ | $>0$ | 恒正 | 任意物质均如此 |
| 固-气（升华曲线） | $>0$ | $>0$ | 恒正 | 同上，且因 $\Delta_{\text{sub}}H>\Delta_{\text{vap}}H$ 更陡 |
| 固-液（熔化曲线） | $>0$ | 多数 $>0$ | 多数为正 | **水、镓、铋等例外**：$\Delta_{\text{fus}}V<0$，斜率为负 |

- **水的负斜率**：冰密度 < 水密度，加压使冰熔化（滑冰原理、复冰效应）；冰 I–VII 多晶形使水相图高压区结构复杂
- **CO₂ 的特殊三相点**：三相点压力 5.11 atm > 1 atm，常压下不存在液态 CO₂——干冰直接升华，这是「干冰」名字的来源
- **水的三相点**：273.16 K / 611.65 Pa，是热力学温标的定义点，比冰点（被空气饱和、外压 1 atm）高约 0.01 K
- 三条两相线在三相点交汇：由两相线斜率可反推第三相界线的相对走向，是分析陌生相图（如 He 的负膨胀异常）的通用工具

## 特鲁顿规则（数量级估算工具）

多数非极性/非缔合液体的摩尔汽化熵近似为常数：

$$\Delta_{\text{vap}}S_m \approx \frac{\Delta_{\text{vap}}H_m}{T_b} \approx 85\ \mathrm{J\,mol^{-1}\,K^{-1}}$$

- 已知正常沸点 $T_b$ 即可估算 $\Delta_{\text{vap}}H_m \approx 85\,T_b$，代入 Clausius-Clapeyron 方程做数量级估算
- **失效场景**：氢键缔合液体（水 109、乙醇 111 J·mol⁻¹·K⁻¹，偏高）与正常沸点接近临界温度的液体（偏低）——竞赛判断题常考此例外

## 推导要点（从相平衡条件出发）

1. 纯物质两相平衡 $\iff$ 两相摩尔吉布斯自由能相等：$G_m(\alpha) = G_m(\beta)$
2. 沿两相线移动时保持相等，取微分：$\mathrm{d}G_m(\alpha) = \mathrm{d}G_m(\beta)$
3. 代入热力学基本方程 $\mathrm{d}G_m = -S_m\,\mathrm{d}T + V_m\,\mathrm{d}p$
4. 整理得 $(V_m^\beta - V_m^\alpha)\,\mathrm{d}p = (S_m^\beta - S_m^\alpha)\,\mathrm{d}T$，即 $\frac{dp}{dT} = \frac{\Delta_{\text{trans}}S}{\Delta_{\text{trans}}V}$
5. 可逆相变 $\Delta_{\text{trans}}S = \Delta_{\text{trans}}H / T$，代入即得 Clapeyron 方程——全程无近似，对任意两相平衡严格成立

## 典型应用

- 计算不同海拔高度水的沸点
- 由蒸气压数据求汽化热
- 竞赛中分析相图和相变条件

## 相关知识点

- [[范特霍夫方程]]
- [[相律与相图]]
- [[化学势与平衡]]
- [[熵变计算]]

## 相关题目

- [[03-02]]
- [[03-03]]
- [[03-04]]
- [[03-05]]

## 🎯 教学视角

### 学习路径建议
Clapeyron方程应在学习相平衡和热力学基本关系之后引入。先理解方程的推导（利用dG=0的相平衡条件），再掌握其物理意义（蒸气压随温度的变化率），最后学习Clausius-Clapeyron近似形式的应用。

进阶路线：先掌握 [[范特霍夫方程]] 中 $\ln K$ 与 $1/T$ 的关系，理解相平衡是化学平衡的特殊情形。它是分析相图的必备工具，建议结合实际相图一起学习。

### 学生易踩的认知误区
| 误区 | 正确理解 |
|:---|:---|
| Clapeyron方程只适用于液-气平衡 | 适用于所有两相平衡（固-液、固-气、液-气） |
| 蒸气压与温度是线性关系 | 蒸气压随温度指数增长，不是线性关系 |
| Clausius-Clapeyron方程是精确的 | 它假设气相为理想气体且忽略液相体积，是近似形式 |
| 克拉佩隆方程和克劳修斯-克拉佩隆方程是一样的 | 精确形式含 $\Delta V$，近似形式假设气相体积远大于凝聚相，两者适用范围不同 |
| 水的沸点在任何地方都是 100°C | 沸点与外界压力有关，高海拔气压低时沸点低于 100°C，高压锅内则高于 100°C |
| 冰的熔化曲线斜率为正 | 水是少数例外：固态密度小于液态，$\Delta V < 0$，熔化曲线斜率为负（冰面加压可降低熔点） |

### 入门级例题
**题目 1**：水在373K时蒸气压为1 atm，蒸发焓为40.68 kJ/mol。估算水在383K时的蒸气压。
**解答**：ln(P₂/P₁) = -(ΔvapH/R)(1/T₂ - 1/T₁) = -(40680/8.314)(1/383 - 1/373) = -4894×(-6.93×10⁻⁵) = 0.339。P₂ = 1.40 atm。

**题目 2**：水在 100°C 时的汽化热为 40.7 kJ/mol，求在海拔 3000 m 处（气压约 0.70 atm）水的沸点。
**解答**：由克劳修斯-克拉佩隆方程 $\ln(0.70/1.00) = -(40700/8.314)(1/T_2 - 1/373.15)$，解得 $T_2 \approx 364\,\text{K} = 91°C$。

### 与现实世界的联系
1. **气象学**：大气中水蒸气含量随温度的变化遵循Clausius-Clapeyron方程
2. **高海拔与高压锅**：海拔升高气压降低，水的沸点下降；高原地区用高压锅增大压力提高沸点，使食物更快煮熟
3. **蒸馏技术**：工业蒸馏塔利用不同物质蒸气压的温度依赖性差异进行分离，克拉佩隆方程用于计算不同压力下的沸点、优化分离条件

### 竞赛级例题

**题目 3（负斜率定量）**：0 °C 时冰的熔化焓为 6.01 kJ/mol，冰的摩尔体积 19.7 cm³/mol，水的摩尔体积 18.0 cm³/mol。估算每升高 1 atm 压力冰熔点变化多少。
**解答**：$\frac{dT}{dp} = \frac{T\,\Delta_{\text{fus}}V}{\Delta_{\text{fus}}H} = \frac{273.15 \times (18.0-19.7)\times10^{-6}}{6010}\ \mathrm{K/Pa} \approx -7.7\times10^{-8}\ \mathrm{K/Pa}$。换算 1 atm ≈ 1.013×10⁵ Pa，得 $\Delta T \approx -0.0075\ \mathrm{K/atm}$——熔点每升高 1 atm 降低约 0.0075 K，负号与水的负斜率一致；此微小数值也解释了为何熔化曲线在相图上近乎竖直。

**题目 4（特鲁顿规则 + 外推）**：某液体正常沸点 350 K，用特鲁顿规则估算其摩尔汽化热，并求 300 K 下的蒸气压。
**解答**：$\Delta_{\text{vap}}H \approx 85 \times 350 = 29.8\ \mathrm{kJ/mol}$。$\ln(p/101.3\,\mathrm{kPa}) = -\frac{29800}{8.314}\left(\frac{1}{300}-\frac{1}{350}\right) = -1.70$，$p \approx 18.3\ \mathrm{kPa}$。若该液体为氢键缔合型（如醇），实际 $\Delta_{\text{vap}}H$ 偏高，计算出的蒸气压会偏低——需按特鲁顿规则的失效条件修正判断。

### 与范特霍夫方程的对照

| 维度 | Clapeyron / Clausius-Clapeyron | 范特霍夫方程 |
|:--|:--|:--|
| 描述对象 | **相平衡**（纯物质两相） | **化学平衡**（多组分反应） |
| 平衡条件 | $\mu_\alpha = \mu_\beta$ | $\Delta_r G = 0$ |
| 数学结构 | $\frac{d\ln p}{dT} = \frac{\Delta_{\text{vap}}H}{RT^2}$ | $\frac{d\ln K}{dT} = \frac{\Delta_r H}{RT^2}$ |
| 竞赛处理 | 完全同构：会其一即会其二，替换 $p \leftrightarrow K$、$\Delta_{\text{vap}}H \leftrightarrow \Delta_r H$ 即可互推 |

## 📝 待完善项

- ⬜ 补充 He 相图（加压下液氩/液氦异常）作为负斜率的第二个实例（低优先级，现有内容已自洽）
