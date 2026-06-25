---
title: Horner-Wadsworth-Emmons反应
aliases: [HWE反应, Horner-Wadsworth-Emmons Reaction, Horner-Emmons反应, 膦酸酯烯化反应]
type: 知识点
template_version: v1.3
subject: 有机化学
module: 有机化学
submodule: 具体反应
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-有机化学
syllabus_code: [48]
syllabus_module: [膦化合物]
tags:
  - 化竞
  - 有机化学
  - 名称反应
  - 膦化合物
  - 烯烃合成
  - 羰基烯化
related: [Wittig反应, 羰基烯化反应, E2反应, 膦化合物, Peterson烯化反应, Julia烯化]
prerequisite: [Wittig反应, 羰基亲核加成, 膦化合物]
problem_types: [题型-产物预测, 题型-机理分析, 题型-合成设计, 题型-试剂选择]
difficulty: 4
importance: 3
status: 已填充
stage: published
sources: []
source_type: []
review_cycle: 30d
updated: 2026-05-17
teaching_ready: false

source_notes: []
key_images: []
---

<!-- 📚 标杆样板（v1.3）：复制本模板创建新 KP 前，先看至少 1-2 个标杆样板
- 化学原理范例：[[杂化轨道理论]]
- 无机/主族范例：[[稀有气体化合物]]
- 分析化学范例：暂无（可参考 [[03-知识点/分析化学]] 任一已填充 KP）
- 有机/机理范例：[[Lawesson试剂]]、[[Swern氧化]]、[[Wittig反应]]
教学视角段（十二）的填法可重点参考以上范例。
本注释在 KP 填充完成后保留即可（HTML 注释不渲染）。
-->

# Horner-Wadsworth-Emmons 反应（HWE 反应）

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-有机化学]]
- 对应考纲条目：[[48-膦化合物]]

## 一、定义

**Horner-Wadsworth-Emmons 反应（HWE 反应）**：醛（或酮）与**膦酸酯碳负离子**反应，生成**α,β-不饱和羰基化合物（或烯烃）**和**水溶性膦酸盐**的羰基烯化反应。

通式：
$$\ce{(RO)2P(O)CH2R' + Base -> (RO)2P(O)CH^-R' + R''CHO -> R''CH=CHR' + (RO)2P(O)O^-}$$

> HWE 反应是 [[Wittig反应]] 的重要改良版本，由 Horner（1958）、Wadsworth 和 Emmons（1961）分别独立发展。核心改进在于用**膦酸酯**替代**鏻叶立德**，解决了 Wittig 反应副产物难分离的问题。

## 二、考纲对应

| 考纲条目 | 对应内容 | 考查深度 |
|:---|:---|:---:|
| [[48-膦化合物]] | 膦酸酯试剂、HWE 反应机理与选择性 | 掌握 |

## 三、核心原理

### 3.1 试剂结构与制备

**HWE 试剂 = 膦酸酯（phosphonate）**，结构为 $\ce{(RO)2P(O)CHR'}$：

| 试剂类型 | 结构特征 | R' 取代基 | 稳定性 |
|:---|:---|:---|:---:|
| **稳定化 HWE 试剂** | $\ce{(RO)2P(O)CH2-CO2R''}$ | 吸电子基（CO₂R, CN, COR, SO₂R）| 高 |
| **非稳定化 HWE 试剂** | $\ce{(RO)2P(O)CH2R}$ | 烷基、芳基 | 较低 |
| **Still-Gennari 改良** | $\ce{(CF3CH2O)2P(O)CH2-CO2R}}$ | 吸电子基 + 三氟乙基 | 高 |

**制备方法**：
1. **Arbuzov 反应**：亚磷酸三酯 + 卤代烷 $\xrightarrow{\Delta}$ 膦酸酯
2. **Michaelis-Arbuzov 重排**：$\ce{P(OR)3 + R'X -> (RO)2P(O)R' + RX}$

### 3.2 反应机理

HWE 反应的机理与 Wittig 反应类似，但中间体不同：

#### 步骤 1：碳负离子形成
碱夺取膦酸酯 α-H，生成**碳负离子**（phosphonate carbanion）：
$$\ce{(EtO)2P(O)CH2CO2Et + NaH -> (EtO)2P(O)CH^-CO2Et + H2}$$

> 碳负离子受 P=O 的诱导效应和 d-π 共轭稳定化，亲核性适中。

#### 步骤 2：亲核加成
碳负离子进攻醛羰基碳，形成**氧负离子中间体**：
$$\ce{(EtO)2P(O)CH^-CO2Et + RCHO -> (EtO)2P(O)CH(CO2Et)-CH(R)-O^-}$$

#### 步骤 3：环化与消除（协同 [2+2] 逆切）
氧负离子与磷原子配位，形成**氧磷杂环丁烷（oxaphosphetane）**中间体，随后协同分解：

$$\ce{oxaphosphetane -> RCH=CHCO2Et + (EtO)2P(O)O^-}$$

> 与 Wittig 的关键区别：HWE 的 oxaphosphetane 分解更快、可逆性更低，导致**几乎完全的 E-选择性**。

### 3.3 驱动力分析

| 键 | 键能 (kJ/mol) | 说明 |
|:---|:---:|:---|
| P=O | ~540 | 极强，反应核心驱动力 |
| P–O | ~360 | 膦酸盐中稳定存在 |
| C=C | ~614 | 产物中获得 |
| C=O（醛）| ~745 | 反应物中断裂 |

**总反应放热**：~50–80 kJ/mol（视底物而定）

> 与 Wittig 相同，**P=O 键形成**是热力学驱动力。但 HWE 额外优势：副产物 $\ce{(RO)2P(O)O^-}$ 为**水溶性离子**，易水洗除去。

## 四、关键结论

### 4.1 立体化学——高 E-选择性

| 试剂类型 | 主产物 | 选择性来源 |
|:---|:---|:---|
| **标准 HWE**（稳定化试剂）| **E-烯烃**（反式）| 热力学控制，oxaphosphetane 分解前达到平衡 |
| **Still-Gennari 改良** | **Z-烯烃**（顺式）| 三氟乙基增加 P=O 亲电性，动力学控制 |

**E-选择性的原因**：
- 稳定化膦酸酯碳负离子的 oxaphosphetane 中间体寿命较长
- 热力学上，E-烯烃的过渡态位阻更小
- 大位阻取代基倾向于处于反式位置

### 4.2 与 Wittig 反应的核心对比

| 维度 | Wittig 反应 | HWE 反应 |
|:---|:---|:---|
| **试剂** | $\ce{Ph3P=CHR}$（鏻叶立德）| $\ce{(RO)2P(O)CHR^-}$（膦酸酯碳负离子）|
| **制备** | 两步（鏻盐 + 强碱）| 一步（膦酸酯 + 温和碱）|
| **副产物** | $\ce{Ph3P=O}$（难溶于水，难分离）| $\ce{(RO)2P(O)O^-}$（水溶性，易水洗除）|
| **E/Z 选择性** | 依赖叶立德稳定性（非稳定→Z；稳定→E）| **通常高 E-选择性**（稳定化试剂）|
| **底物范围** | 醛/酮均可 | 主要适用于**醛**（酮反应差）|
| **碱要求** | 强碱（n-BuLi, NaH）| 温和碱（NaH, NaOMe, $\ce{K2CO3}$, DBU）|
| **原子经济性** | 差（Ph₃P=O 分子量大）| 较好 |
| **工业应用** | 较少 | 较多（副产物易除）|

### 4.3 底物范围与限制

| 底物 | 反应性 | 说明 |
|:---|:---:|:---|
| **脂肪醛** | 优 | 高产率，快反应 |
| **芳香醛** | 优 | 标准底物 |
| **α,β-不饱和醛** | 可 | 1,2-加成为主 |
| **酮** | 差 | 位阻大，产率低 |
| **酯/酰胺** | 不反应 | 羰基亲电性不足 |

## 五、常见分类或情形

### 5.1 标准 HWE：醛 + 稳定化膦酸酯 → E-α,β-不饱和酯

$$\ce{PhCHO + (EtO)2P(O)CH2CO2Et ->[NaH, THF] PhCH=CHCO2Et\,(E) + (EtO)2P(O)O^-}$$

> 竞赛最常见场景：由醛制备 E-型 α,β-不饱和酯。

### 5.2 Still-Gennari 改良：Z-选择性 HWE

$$\ce{RCHO + (CF3CH2O)2P(O)CH2CO2Et ->[KHMDS, -78°C] RCH=CHCO2Et\,(Z)}$$

- 用**双(三氟乙基)膦酸酯**替代普通乙基膦酸酯
- 三氟乙基的强吸电子效应增加 P=O 亲电性
- 低温下动力学控制 → **高 Z-选择性**

### 5.3 Masamune-Roush 条件

- 用于对碱敏感的底物
- 碱：LiCl + DBU（非强碱条件）
- 溶剂：THF 或乙腈
- 特点：反应条件温和，官能团相容性好

### 5.4 非稳定化 HWE 试剂

$$\ce{(EtO)2P(O)CH2Ph + RCHO -> RCH=CHPh}$$

- α-碳无吸电子基团
- 选择性较差，E/Z 混合
- 应用较少

## 六、适用条件与限制

### 适用条件

| 条件 | 推荐 |
|:---|:---|
| **碱** | NaH（标准）、NaOMe、KHMDS（Still-Gennari）、DBU + LiCl（Masamune-Roush）|
| **溶剂** | THF、DMF、DMSO、乙腈 |
| **温度** | -78°C → rt（Still-Gennari 需低温）|
| **底物** | 醛（最佳）、活性酮（有限）|
| **无水** | 必需（碳负离子对水敏感）|

### 限制

| 限制 | 说明 |
|:---|:---|
| **酮反应性差** | 位阻大，产率低；脂肪酮尤其困难 |
| **非稳定化试剂选择性差** | E/Z 混合，合成价值有限 |
| **需要预先制备膦酸酯** | 比 Wittig 叶立德多一步试剂制备 |
| **α-手性中心可能消旋** | 若 α-位有手性中心，强碱条件下可能消旋 |

## 七、常见比较与易混点

### 7.1 HWE vs Wittig：如何选择？

| 场景 | 推荐反应 | 原因 |
|:---|:---|:---|
| 需要 **E-烯烃** | HWE | 高 E-选择性，副产物易除 |
| 需要 **Z-烯烃** | Still-Gennari HWE 或 非稳定 Wittig | Still-Gennari 给 Z；非稳定 Wittig 也给 Z |
| **大规模合成** | HWE | 副产物水溶性，易纯化 |
| **酮底物** | Wittig | HWE 对酮反应性差 |
| **复杂天然产物** | 视立体需求定 | 两者各有优势 |

### 7.2 HWE vs Peterson 烯化

| 维度 | HWE | Peterson |
|:---|:---|:---|
| 试剂 | 膦酸酯碳负离子 | β-硅基碳负离子 |
| 副产物 | 膦酸盐（水溶性）| 硅醇/硅氧烷 |
| 选择性 | 通常 E | 酸/碱条件可调控 E/Z |
| 机理 | oxaphosphetane | β-硅基氧负离子消除 |

### 7.3 稳定化 vs 非稳定化 HWE 试剂

| 特征 | 稳定化 | 非稳定化 |
|:---|:---|:---|
| 结构 | $\ce{(RO)2P(O)CH2-CO2R'}$ | $\ce{(RO)2P(O)CH2R'}$ |
| 碱要求 | 温和（NaH, K₂CO₃）| 较强碱 |
| 选择性 | **高 E-选择性** | E/Z 混合 |
| 竞赛频率 | **极高** | 较低 |

## 八、与其他知识点的联系

```
Horner-Wadsworth-Emmons反应
├── 前置知识
│   ├── [[Wittig反应]]（机理类比、选择性对比）
│   ├── [[羰基亲核加成]]（醛酮反应性基础）
│   ├── [[膦化合物]]（膦酸酯分类、P=O 驱动力）
│   └── [[E2反应]]（消除机理的立体化学基础）
├── 等价方法
│   ├── [[Wittig反应]]（鏻叶立德法）
│   ├── [[Peterson烯化反应]]（硅基法）
│   ├── [[Julia烯化]]（砜法）
│   └── [[Tebbe试剂]]（钛法）
├── 试剂制备
│   └── [[Arbuzov反应]]（亚磷酸酯 → 膦酸酯）
└── 应用场景
    ├── [[有机合成]]（α,β-不饱和羰基构建）
    ├── [[天然产物合成]]（E-烯烃骨架）
    └── [[Michael加成]]（制备 Michael 受体）
```

## 九、典型题型

| 题型 | 考查点 | 难度 | 示例 |
|:---|:---|:---:|:---|
| **产物预测** | 给定醛 + HWE 试剂，判断产物和 E/Z | ★★★ | 苯甲醛 + (EtO)₂P(O)CH₂CO₂Et |
| **试剂选择** | Wittig vs HWE 的场景选择 | ★★★★ | 大规模合成选哪个？ |
| **机理书写** | 碳负离子形成 → 加成 → 消除 | ★★★★ | 电子推动法写完整机理 |
| **立体化学分析** | 解释为何 HWE 高 E-选择性 | ★★★★ | oxaphosphetane 热力学控制 |
| **合成设计** | 由目标 E-烯酯倒推 HWE 试剂 | ★★★★★ | 逆合成分析 |

## 十、例题

### 例题 1：HWE 产物预测

**题目**：苯甲醛与 (EtO)₂P(O)CH₂CO₂Me 在 NaH/THF 条件下反应，写出主产物及其立体化学。

**解析**：
- 试剂为**稳定化 HWE 试剂**（α-位有酯基吸电子基）
- 稳定化试剂 → oxaphosphetane 中间体寿命较长，热力学控制
- 热力学上 E-异构体位阻更小，更稳定
- **主产物：(E)-肉桂酸甲酯（methyl cinnamate）**

$$\ce{PhCHO + (EtO)2P(O)CH2CO2Me ->[NaH] PhCH=CHCO2Me\,(E)}$$

**副产物**：(EtO)₂P(O)O⁻Na⁺，水溶性，水洗即可除去。

### 例题 2：Wittig vs HWE 选择

**题目**：工业上由甲醛制备丙烯酸甲酯（CH₂=CHCO₂Me），应选 Wittig 还是 HWE？

**解析**：
选 **HWE**：
- 试剂：(MeO)₂P(O)CH₂CO₂Me + NaH → 碳负离子 + HCHO
- 产物：CH₂=CHCO₂Me
- 原因：
  1. HWE 副产物为水溶性膦酸盐，易水洗除去
  2. Wittig 副产物 Ph₃P=O 难分离，成本高
  3. HWE 试剂更稳定，操作更简便

### 例题 3：Still-Gennari 改良的应用

**题目**：如何用 HWE 反应高选择性地制备 Z-型 α,β-不饱和酯？

**解析**：
使用 **Still-Gennari 改良**：
- 试剂：双(2,2,2-三氟乙基)膦酸乙酸酯 $\ce{(CF3CH2O)2P(O)CH2CO2Et}$
- 碱：KHMDS（强但非亲核性碱）
- 温度：-78°C（动力学控制）
- 结果：**高 Z-选择性**

**原理**：三氟乙基的强吸电子效应使 P=O 更亲电，oxaphosphetane 形成更快、分解更快，来不及达到热力学平衡，保留动力学产物 Z。

## 十一、易错点

| 错误 | 原因 | 纠正 | 课堂提问 |
|:---|:---|:---|:---|
| 把 HWE 当作 Wittig 的变体 | 概念混淆 | HWE 试剂是**膦酸酯碳负离子**，不是**鏻叶立德** | HWE 与 Wittig 的试剂结构有何不同？ |
| 认为 HWE 和 Wittig 选择性相同 | 未理解机理差异 | HWE 稳定化试剂几乎总是 **E-选择性**；Wittig 则依赖叶立德稳定性 | 为何 HWE 的 E-选择性比 Wittig 更可靠？ |
| 忽略副产物差异 | 不了解实验操作 | HWE 副产物水溶性，Wittig 副产物难除 | 工业上为何偏好 HWE？ |
| 对酮使用 HWE | 未掌握底物范围 | HWE 主要适用于**醛**，酮反应差 | 酮的烯化应选什么方法？ |
| 混淆 Still-Gennari 条件 | 记忆混乱 | Still-Gennari = 三氟乙基 + 强碱 + 低温 → **Z-选择性** | Still-Gennari 改良的核心是什么？ |
| 认为所有 HWE 试剂都高 E-选择性 | 未分类 | 仅**稳定化**试剂高 E-选择性；非稳定化试剂选择性差 | 稳定化与非稳定化 HWE 试剂的区别？ |

## 十二、🎯 教学视角

### 12.1 学习路径

```
前置：Wittig 反应机理 → 膦化合物分类 → 羰基亲核加成
                    ↓
本节：HWE 反应（试剂结构 → 机理 → 选择性 → 与 Wittig 对比）
                    ↓
后续：Still-Gennari 改良 → Peterson 烯化 → Julia 烯化
                    ↓
应用：有机合成中的双键构建策略
```

**建议课时**：1–1.5 课时
- HWE 试剂与 Wittig 试剂对比：0.3 课时
- 机理与 E-选择性解释：0.4 课时
- Still-Gennari 改良与应用：0.3 课时

### 12.2 认知误区

| 误区 | 学生典型想法 | 纠正策略 |
|:---|:---|:---|
| "HWE 就是另一种 Wittig" | 同功能 = 同机理 | 强调试剂结构差异：膦酸酯 vs 鏻盐；碳负离子 vs 叶立德 |
| "HWE 选择性总是 E" | 死记结论 | 解释 oxaphosphetane 的热力学平衡；提及 Still-Gennari 例外 |
| "P=O 驱动力只在 Wittig 中重要" | 孤立理解 | 强调 P=O 是**所有磷化学**的共同驱动力（Wittig、HWE、Arbuzov、Mitsunobu）|

### 12.3 入门例题

**最简 HWE 题**：
> 苯甲醛与 (EtO)₂P(O)CH₂CO₂Et 在 NaH 作用下反应，主产物是什么？E/Z 比例倾向？
> 
> 答案：(E)-肉桂酸乙酯；稳定化 HWE 试剂 → 高 E-选择性。

**进阶对比题**：
> 需要由对硝基苯甲醛制备 (Z)-3-(4-硝基苯基)丙烯酸甲酯，应选 Wittig、标准 HWE 还是 Still-Gennari？
> 
> 答案：**Still-Gennari HWE**——标准 HWE 和 Wittig（稳定化叶立德）都给 E；只有 Still-Gennari 给 Z。

## 十三、竞赛拓展

- **Masamune-Roush 条件**：LiCl + DBU，温和条件下实现 HWE，适用于对强碱敏感的底物
- **不对称 HWE**：手性膦酸酯或手性催化剂实现不对称烯化
- **串联反应**：HWE + Michael 加成一锅法构建复杂骨架
- **杂环合成**：HWE 产物为 α,β-不饱和羰基，是 Diels-Alder 反应和杂环合成的优良前体

## 十四、外部资料出处

- 经典综述：Wadsworth, W. S.; Emmons, W. D. *J. Am. Chem. Soc.* **1961**, *83*, 1733–1738
- Still-Gennari 改良：Still, W. C.; Gennari, C. *Tetrahedron Lett.* **1983**, *24*, 4405–4408
- Masamune-Roush 条件：Blanchette, M. A.; et al. *Tetrahedron Lett.* **1984**, *25*, 2183–2186
- 经典教材：March, J. *Advanced Organic Chemistry*, Chapter 16; Carey & Sundberg, *Advanced Organic Chemistry*, Part B, Chapter 2

## 十五、待完善项

- [ ] 补充 HWE 反应的动力学/热力学控制详细分析
- [ ] 补充 Masamune-Roush 条件的具体应用实例
- [ ] 补充不对称 HWE 的最新进展
- [ ] 补充 HWE 在天然产物全合成中的经典案例

---

```dataview
TABLE file.name AS "文件名", year AS "年份", type AS "题型", difficulty AS "难度"
FROM "04-题库"
WHERE contains(knowledge_points, "Horner-Wadsworth-Emmons反应")
SORT year DESC, difficulty ASC
```
