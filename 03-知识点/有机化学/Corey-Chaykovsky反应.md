---
title: Corey-Chaykovsky反应
aliases: [Johnson-Corey-Chaykovsky reaction, JCC reaction, Corey叶立德反应, 硫叶立德加成, 二甲基硫鎓甲叉, 二甲基亚砜鎓甲叉]
type: 知识点
template_version: v1.3
subject: 有机化学
module: 有机化学
submodule: 具体反应
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-有机化学
syllabus_code: [45, 50]
syllabus_module: [有机化学]
tags: [化竞, 有机化学, 名称反应, 硫叶立德, 环氧化物, 环丙烷, 含硫化合物]
related: [Wittig反应, 叶立德, 环氧化物, Swern氧化, 含硫化合物, Corey-Seebach反应]
prerequisite: [叶立德, 亲核加成, 含硫化合物]
problem_types: [题型-机理推断, 题型-合成设计]
difficulty: 4
importance: 4
status: 已填充
stage: published
sources: [Arrow Pushing in Inorganic Chemistry-总索引]
source_type: []
review_cycle: 30d
has_images: false
image_count: 0
images_priority: medium
images_note: "当前未嵌入图像文件；该主题具备一定可视化价值，后续备课时可优先补充结构示意图、关系图或谱图。"
teaching_ready: false
source_notes: []
key_images: []
updated: 2026-05-06
---

# Corey–Chaykovsky 反应（JCC 反应）

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-有机化学]]
- 对应考纲条目：[[45-亲核加成反应]]、[[50-有机合成]]
- 外部资料：[[Arrow Pushing in Inorganic Chemistry-总索引]] §6.10

## 一、定义
**Corey–Chaykovsky 反应（也称 Johnson-Corey-Chaykovsky / JCC 反应）**：硫叶立德（sulfur ylide）作为亲核体进攻醛/酮/亚胺/α,β-不饱和羰基化合物的羰基（或亚胺/双键）碳，**形成三元环**——通常是 **环氧化物**（环氧乙烷类）、**氮丙啶** 或 **环丙烷** 的反应。

$$
\ce{R^1R^2C=Z + Me2S^+-CH2^- -> \underset{(Z=O,NR \to 三元环)}{R^1R^2C\overset{Z}{<}CH2} + Me2S}
$$

- $\ce{Z=O}$（醛酮）：得 **环氧化物**
- $\ce{Z=NR}$（亚胺）：得 **氮丙啶**
- 对 **α,β-不饱和羰基**：
  - 二甲基硫鎓甲叉（$\ce{Me2S^+-CH2^-}$，sulfonium ylide）：1,2-加成 → **环氧化物**
  - 二甲基亚砜鎓甲叉（$\ce{Me2S(=O)^+-CH2^-}$，sulfoxonium ylide）：1,4-加成 → **环丙烷**

## 二、考纲对应
- 对应考纲条目：[[45-亲核加成反应]]、[[50-有机合成]]
- 所属模块：[[基础要求-有机化学]]
- 本知识点在考纲中的作用：是 [[Wittig反应]] 的"姊妹反应"——同样使用叶立德 + 羰基，但产物为三元环（环氧/氮丙啶/环丙烷）而非烯烃。其分支选择性（1,2 vs 1,4）是合成设计的高考点。

## 三、核心原理

### 3.1 叶立德的制备

**二甲基硫鎓甲叉（dimethylsulfonium methylide）**——四价 S 叶立德：

$$
\ce{Me3S^+I^- ->[\text{NaH, DMSO}] Me2S^+-CH2^-}
$$

> p$K_a \approx 16.3$（$\ce{Me2(PhCH2)PhS^+}$ 上的 α-H），与醇的 OH 相当，可被 NaH 拔取。

**二甲基亚砜鎓甲叉（dimethylsulfoxonium methylide）**——六价 S 叶立德：

$$
\ce{Me3S^+(O)I^- ->[\text{NaH, DMSO}] Me2S^{+}(=O)-CH2^-}
$$

> p$K_a \approx 18.2$。该叶立德 **更稳定、更软**，是 1,4-加成的来源。

### 3.2 与羰基的 JCC 反应机理（饱和酮）

![[ArrowPushinginInorganicChemistry_231-336_images/779201b48b97ac8c623dee17b3f0c77afa70b534b1f4428bf0b0981477a5d37b.jpg]]

**第 1 步**：叶立德的碳（带形式负电）亲核进攻羰基 C：

$$
\ce{R^1R^2C=O + ^{\ominus}CH2-S^+Me2 -> R^1R^2C(O^-)-CH2-S^+Me2}
$$

形成 **甜菜碱（betaine）** 中间体（带 −O 与 +SMe₂）。

**第 2 步**：氧上的 −O 反过来进攻含 S 的 α-C，**S–C 键作为离去基**断裂：

$$
\ce{R^1R^2C(O^-)-CH2-S^+Me2 -> R^1R^2C\overset{O}{<}CH2 + Me2S}
$$

得 **环氧化物 + DMS**（气体）。

> **关键热力学差异**：
> - 硫叶立德给出**环氧**（C-O 键形成 + S 离去），因为 $\ce{S^+-O^-}$ 键能仅 389 kJ/mol（DMSO 中），不利于直接生成烯烃；
> - 膦叶立德给出**烯烃**（[[Wittig反应]]），因为 $\ce{P^+-O^-}$ 键能高达 544 kJ/mol，驱动 oxaphosphetane 闭环 + 烯化。

### 3.3 与 α,β-不饱和羰基的反应：叶立德"硬度"决定 1,2 vs 1,4

| 叶立德 | 软硬程度 | 加成位点 | 产物 |
|---|---|---|---|
| **$\ce{Me2S^+-CH2^-}$（硫鎓甲叉）** | 较硬，反应快、动力学控制 | **1,2-加成**（直接攻 C=O） | **环氧化物** |
| **$\ce{Me2S(=O)^+-CH2^-}$（亚砜鎓甲叉）** | 较软，反应慢、热力学控制 | **1,4-共轭加成**（攻 β-C） | **环丙烷** |

> 为什么如此分流？
> - "硬"叶立德先攻硬的羰基 C；α-O⁻ 与 α-C 上的 SMe₂⁺ 几何上相邻，闭环为环氧；
> - "软"叶立德先攻软的 β-C（共轭加成）；产物烯醇负离子 → β-C 上的 −CH₂ 与 α-C 之间形成新键；闭环为环丙烷。

### 3.4 与亚胺反应：氮丙啶

$$
\ce{R^1R^2C=NR^3 + Me2S^+-CH2^- -> R^1R^2C\overset{NR^3}{<}CH2 + Me2S}
$$

机理与醛酮完全平行，仅 O 换成 N。

## 四、关键结论
- JCC 反应是 **"羰基/亚胺/烯酮 → 三元环"** 的最经典方法。
- 选择性源于：
  - **底物**：饱和 → 环氧/氮丙啶；α,β-不饱和 → 环氧或环丙烷视叶立德而定；
  - **叶立德**：硫鎓 → 1,2/动力学/环氧；亚砜鎓 → 1,4/热力学/环丙烷。
- 与 [[Wittig反应]] **机理同源、产物分流**：S 给三元环，P 给烯烃，根本原因在 P=O / S=O 键能差。
- 副产物 $\ce{Me2S}$ 或 $\ce{DMSO}$ 易回收，绿色程度高。

## 五、常见分类或情形

| 情形 | 叶立德 | 底物 | 产物 |
|---|---|---|---|
| 1 | $\ce{Me2S^+-CH2^-}$ | 醛/酮 | 环氧化物 |
| 2 | $\ce{Me2S^+-CH2^-}$ | 亚胺 | 氮丙啶 |
| 3 | $\ce{Me2S^+-CH2^-}$ | α,β-不饱和酮 | **环氧化物（1,2-加成）** |
| 4 | $\ce{Me2S(=O)^+-CH2^-}$ | 醛/酮 | 环氧化物（一般） |
| 5 | $\ce{Me2S(=O)^+-CH2^-}$ | α,β-不饱和酮 | **环丙烷（1,4-加成）** |
| 6 | $\ce{Me2S^+-CHR}$（非甲叉） | 醛酮 | 取代环氧 |

## 六、适用条件与限制

### 6.1 适用范围
- 醛、酮（含芳香醛/酮）
- 亚胺、亚硝酮
- α,β-不饱和酮（含 enone、烯醛、不饱和酯）
- 兼容大多数官能团：酯、酰胺、醚、保护基

### 6.2 限制
- 强酸性 α-H 底物（如 1,3-二酮）会被 NaH 优先脱质子，副反应多；
- 大位阻底物（如新戊基酮）反应慢；
- 易消旋化的手性 α-碳应避免高温。

## 七、常见比较与易混点

### 7.1 JCC vs [[Wittig反应]]

| 对比项 | JCC | Wittig |
|---|---|---|
| 叶立德 | $\ce{R3S^+-CR^1R^2^-}$ | $\ce{R3P^+=CR^1R^2}$ |
| 产物 | **三元环**（环氧/氮丙啶/环丙烷） | **烯烃** |
| 副产物 | $\ce{Me2S}$ 或 DMSO | $\ce{R3P=O}$ |
| 驱动力 | C–O 闭环 + S 离去 | P=O 形成（$\Delta H \approx -544$ kJ/mol） |
| 关键键能 | $\ce{S^+-O^-}$ (DMSO) ≈ 389 kJ/mol，**弱** | $\ce{P^+-O^-}$ ≈ 544 kJ/mol，**强** |

### 7.2 硫鎓 vs 亚砜鎓叶立德

| 对比项 | $\ce{Me2S^+-CH2^-}$ | $\ce{Me2S(=O)^+-CH2^-}$ |
|---|---|---|
| 硫价 | +4 | +6 |
| 稳定性 | 较低（用即制） | 较高（可分离） |
| 软硬 | 较硬 | 较软 |
| 与 enone 加成 | **1,2 → 环氧** | **1,4 → 环丙烷** |

### 7.3 容易混淆的"硫叶立德"
- **JCC 中的硫叶立德**：是 R₃S⁺=CR₂ 类（碳上负电，硫上正电），与 [[Swern氧化]] 第 3 步生成的硫叶立德 **同类**，但作用方式不同（一个是亲核加成 C=O，一个是 5 元环协同消除）。
- **1,3-二噻烷负离子**（[[Corey-Seebach反应]]）：是 **σ(C–S) 超共轭** 稳定的 sp³ 碳负离子，不是叶立德；但同属"硫稳定化的碳负离子"大家族。

## 八、与其他知识点的联系
- 前置知识：[[叶立德]]、[[亲核加成]]、[[含硫化合物]]
- 相关知识：
  - "[[Wittig反应]]（"姊妹反应"，机理同源、产物不同）"
  - "[[Corey-Seebach反应]]（1,3-二噻烷负离子的 umpolung 化学）"
  - "[[Swern氧化]]（同样使用硫叶立德的协同重排）"
  - "[[氧化物]]、[[环丙烷]] 的合成化学"
- 应用知识：[[多步合成路线]]、[[原子经济性与反应选择性]]

## 九、典型题型
- 题型-机理推断：写出 JCC 反应机理（2 步：加成 + 闭环）
- 题型-合成设计：选择硫鎓 or 亚砜鎓叶立德 → 控制 1,2 vs 1,4
- 题型-产物预测：判断 enone 与不同硫叶立德反应的产物

## 十、例题

### 例题 1：选择性
**题目：** 将 PhCH=CHCOMe（α,β-不饱和酮）分别用 (a) $\ce{Me2S^+-CH2^-}$ 和 (b) $\ce{Me2S(=O)^+-CH2^-}$ 反应。预测主产物。

**分析：**
- 硫鎓甲叉是较硬亲核体 → 1,2-加成攻 C=O → 得 **环氧化物** $\ce{PhCH=CH-C(O)(Me)\overset{O}{<}CH2}$（即 PhCH=CH 上 C(Me) 与 CH₂ 形成环氧）；
- 亚砜鎓甲叉是较软亲核体 → 1,4-加成攻 β-C(Ph) → 烯醇负离子中间体；闭环为 **环丙烷** $\ce{Ph\overset{}{<}CH-CH(COMe)<CH2}$（即 PhCH 与 CH 之间嵌入 CH₂）。

### 例题 2：机理写出
**题目：** 写出 PhCHO + $\ce{Me2S^+-CH2^-}$ → 苯基环氧乙烷的完整机理。

**解答：**
- 第 1 步：CH₂⁻ 攻 PhCHO 的 C → 甜菜碱 $\ce{Ph-CH(O^-)-CH2-S^+Me2}$
- 第 2 步：O⁻ 反向攻 α-C，S 离去 → $\ce{PhC<\!\!^{O}\!\!CH2}$ + $\ce{Me2S}$（环氧化物 + DMS）

### 例题 3：与 [[Wittig反应]] 的对比
**题目：** 解释为何 Wittig 给烯烃而 JCC 给三元环。

**分析：**
关键在 P=O vs S=O 键能。Wittig 的 oxaphosphetane 倾向于走"4 元环开环 → 烯烃 + R₃P=O"，因 P=O 键能极高（约 544 kJ/mol）。JCC 的甜菜碱中 S=O 键能仅 ~389 kJ/mol，开环成烯烃热力学上不利，于是 −O⁻ 反向 SN2 攻 α-C，S 作为离去基，得环氧化物。

## 十一、易错点
- ❌ 误以为硫叶立德也会"like Wittig"给烯烃：**不**，给三元环。
- ❌ 误以为 enone 都给环丙烷：取决于叶立德——硫鎓给环氧（1,2），亚砜鎓才给环丙烷（1,4）。
- ❌ 把 1,3-二噻烷负离子（Corey-Seebach）当成 JCC 叶立德：前者是 sp³ 碳负 + σ-超共轭稳定，后者是叶立德。
- ❌ 把氧化数搞错：硫鎓甲叉中 S 是 +4 价（共价 4 个键），亚砜鎓甲叉中 S 是 +6 价。
- ❌ 忽略软硬选择性：1,2 vs 1,4 的分流是 JCC 在合成设计中的核心。

## 十二、竞赛拓展
- **取代叶立德**：$\ce{Me2S^+-CHR}$（R = 烷基/芳基）可给取代环氧化物，立体化学多样；
- **手性硫叶立德**：Aggarwal 等人发展了手性硫鎓催化版本，用于不对称环氧化；
- **稳定叶立德**：含 EWG（COR、NO₂）的硫叶立德反应慢、立体化学好，可分离；
- 与 [[Pummerer重排]] 同源：都涉及 α-S 碳的形式氧化态变化；
- 与 [[Swern氧化]] 共享叶立德中间体的"5 元环消除"思想，但 JCC 不消除。

## 十三、外部资料出处
- [[Arrow Pushing in Inorganic Chemistry-总索引]] **§6.10 Sulfur Ylides and Sulfur-Stabilized Carbanions**（pp. 234-238）
- 经典文献：
  - Johnson, A. W.; LaCount, R. B. *J. Am. Chem. Soc.* **1961**, *83*, 417.
  - Corey, E. J.; Chaykovsky, M. *J. Am. Chem. Soc.* **1962**, *84*, 3782.
  - Corey, E. J.; Chaykovsky, M. *J. Am. Chem. Soc.* **1965**, *87*, 1353.
- Aggarwal, V. K. *Angew. Chem. Int. Ed.* **2001**, *40*, 1433.（手性硫叶立德综述）

## 十四、待完善项
- [ ] 补充 [[Corey-Seebach反应]] 单独成 KP（1,3-二噻烷 umpolung）
- [ ] 补充手性硫叶立德的不对称 JCC 应用例
- [ ] 补充 JCC 与 Darzens 缩合的对比（α-卤代酯 + 醛 → 环氧酯）

---

## 十二、🎯 教学视角

- [待填充]

## 十三、竞赛拓展

- [待填充]

## 十四、外部资料出处

- [待填充]

## 十五、待完善项

- [待填充]
```dataview
TABLE file.name AS "文件名", year AS "年份", type AS "题型", difficulty AS "难度"
FROM "04-题库"
WHERE contains(knowledge_points, "Corey-Chaykovsky反应")
SORT year DESC, difficulty ASC
```
