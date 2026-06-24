---
title: Curtius重排
aliases: [Curtius Rearrangement, 库尔提乌斯重排, 酰基叠氮重排, 氮宾重排]
type: 知识点
template_version: v1.3
subject: 有机化学
module: 有机化学
submodule: 重排反应
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-有机化学
syllabus_code: [34, 39, 51]
syllabus_module: [有机活性中间体, 有机重排, 有机合成]
tags:
  - 化竞
  - 有机重排
  - 名称反应
  - 氮宾
  - 1,2-迁移
related: [1,2-迁移与重排, 卡宾, 重氮化合物, Hofmann重排, 重氮甲烷, 异氰酸酯]
prerequisite: [1,2-迁移与重排, 反应机理表示法, 卡宾]
problem_types: [题型-机理推断, 题型-重排产物判断]
difficulty: 4
importance: 5
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

# Curtius 重排（Curtius Rearrangement）

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-有机化学]]
- 对应考纲条目：[[34-有机活性中间体]]、[[39-重排反应]]、[[51-金属有机]]

## 一、定义
**Curtius 重排**：**酰基叠氮（acyl azide）**在加热（或光照）下脱去 N₂，发生 1,2-烷基（或芳基）迁移生成**异氰酸酯（isocyanate）**的重排反应。德国化学家 Theodor Curtius 于 1890 年发现。

通式：
$$\ce{R-C(=O)-N3 ->[\Delta\ \text{or}\ h\nu] R-N=C=O + N2}$$

> 关键特征：迁移基团（R）从碳迁移到氮上，同时 N₂ 离去——驱动力是 N₂ 的高稳定性。

## 二、考纲对应
- 对应考纲条目：[[34-有机活性中间体]]、[[39-重排反应]]、[[51-金属有机]]
- 所属模块：[[基础要求-有机化学]]
- 本知识点在考纲中的作用：是经典氮宾参与的 1,2-迁移重排，是酰基叠氮 → 胺/氨基甲酸酯/脲的链碳缩短（一碳链缩短）合成方法。

## 三、核心原理

### 3.1 氮宾（nitrene）的形成与定义
**氮宾（R-N:）** 是一价的氮活性中间体，氮原子上仅有 6 价电子（缺 2 个），与 [[卡宾]] 等电子。氮宾既可处于**单线态**（自旋成对）也可处于**三线态**（双自由基）：
$$\ce{R-N\overset{..}{:}}\,(单线态) \quad \ce{R-\overset{.}{N}\overset{.}{:}}\,(三线态)$$

氮宾极不稳定，仅作中间体存在，常通过叠氮分解生成：
$$\ce{R-N=N^+=N^- ->[\Delta] R-N: + N2}$$

### 3.2 Curtius 重排的两种机理

#### 机理 A：**协同迁移**（主流观点）
R 基团**带电子对**直接从 C 迁移到 N，同时 N₂ 离去，**不经过自由氮宾中间体**：
$$\ce{R-\underset{\underset{N=N=N}{\Big|}}{\overset{O}{C}} ->[\Delta,\,-N2] R-N=C=O}\quad \text{(协同)}$$

#### 机理 B：**经过氮宾**（次要可能性）
先生成酰基氮宾 R-C(=O)-N:，然后 R 迁移到 N 上：
$$\ce{R-C(=O)-N3 -> R-C(=O)-N: + N2 -> R-N=C=O}$$

> 同位素标记和动力学研究多数支持机理 A（协同）。但在某些底物（如取代芳基迁移）和某些条件下，机理 B 不可完全排除。

### 3.3 异氰酸酯的后续转化
异氰酸酯 R-N=C=O 通常不分离，直接在反应介质中被亲核体捕获：

#### 与水反应 → 一级胺（脱去一个 CO₂）
$$\ce{R-N=C=O + H2O -> R-NH-COOH -> R-NH2 + CO2}$$

#### 与醇反应 → 氨基甲酸酯（carbamate, R-NH-CO₂R'）
$$\ce{R-N=C=O + R'OH -> R-NH-C(=O)-OR'}$$

#### 与胺反应 → 脲（urea, R-NH-CO-NH-R'）
$$\ce{R-N=C=O + R'NH2 -> R-NH-C(=O)-NH-R'}$$

## 四、关键结论

### 4.1 反应链：从酰氯/酸到一级胺
完整的"链碳缩短一碳"合成路径：
$$\ce{R-COOH ->[1) SOCl2\,2) NaN3] R-CON3 ->[\Delta] R-N=C=O ->[H2O] R-NH2 + CO2}$$

> 合成意义：将一个 R-COOH（n 碳） → R-NH₂（n−1 碳），即**链碳缩短一碳的氨化反应**。

### 4.2 与其他相关重排的比较
| 重排 | 起始物 | 关键步骤 | 产物 | 缩短 |
|---|---|---|---|---|
| **Curtius** | 酰基叠氮 R-C(=O)-N₃ | R 迁移 + N₂ 离去 | 异氰酸酯 → 胺 | 减一个 C |
| **Hofmann** | 一级酰胺 R-CONH₂ + Br₂/OH⁻ | R 迁移 + Br⁻ 离去 | 异氰酸酯 → 胺 | 减一个 C |
| **Schmidt** | 酮 + HN₃/H⁺ | R 迁移 + N₂ 离去 | 酰胺 | 不变 |
| **Beckmann** | 肟 R₂C=N-OH | R 迁移 + H₂O 离去 | 酰胺 | 不变 |
| **Wolff** | 重氮酮 R-CO-CHN₂ | R 迁移 + N₂ 离去 | 烯酮 → 酸（[[1,2-迁移与重排]]） | 不变 |

### 4.3 立体化学：构型保留
**与所有 1,2-迁移一样**，Curtius 重排中迁移的 R 基团**带电子对**从 C 迁到 N，**保持构型**。如手性碳作为 R 迁移时，新形成的 R-N 键保持 R/S 构型。

### 4.4 驱动力分析
- **失去 N₂**：极稳定的氮气分子离去（ΔH ≈ −230 kJ/mol）
- **形成异氰酸酯**：C=N 双键 + N=O（异氰酸酯）键能均较高
- **协同/经氮宾**：路径不同，但热力学结局一样

## 五、常见分类或情形

### 5.1 标准 Curtius 重排
$$\ce{Ph-CO-N3 ->[\Delta\,\text{或}\,h\nu,\,\text{苯/二甲苯}] Ph-N=C=O ->[H2O] Ph-NH2 + CO2}$$

### 5.2 经过 Curtius 重排合成 BOC 保护胺（碳酸叔丁酯保护）
$$\ce{R-CO-N3 + (CH3)3C-OH ->[\Delta] R-NH-C(=O)-O-C(CH3)3}$$

> 这正是 Boc-NH-R 的常用合成方法之一（Curtius-Boc 保护一步法）。

### 5.3 经过 Curtius 重排合成异腈酸酯类除草剂、农药
许多药物分子（如某些杂环药）通过 Curtius 重排经由异氰酸酯中间体合成。

### 5.4 双 Curtius 重排
某些二酰基叠氮（如苯二甲酸的双叠氮）可同时双 Curtius，得到双胺产物。

## 六、适用条件与限制

### 适用条件
- ✓ 加热（80–150 ℃）或紫外光照
- ✓ 极性较低溶剂（苯、甲苯、二甲苯——避免叠氮的水解）
- ✓ R 基团：烷基、芳基、烯基都适用

### 限制
- ✗ 含强亲核体或质子源时酰基叠氮先水解
- ✗ 大位阻的 t-Bu、新戊基迁移困难
- ✗ 强 σ 键的 SP 碳（如炔基）迁移倾向差

### 安全提示
- 酰基叠氮在加热下不仅 Curtius 重排，也可能爆炸性分解
- 实验通常在惰性气氛下、稀溶液中进行
- **绝不**用 NaN₃ 与含有重金属（Cu、Hg）盐共热！

## 七、常见比较与易混点

### 1. Curtius vs Hofmann
- **Curtius**：起始为酰基叠氮（R-CO-N₃）
- **Hofmann**：起始为一级酰胺 + Br₂/NaOH
- **共同点**：都通过 R 迁移到 N 形成异氰酸酯
- **机理细节**：Hofmann 是先脱质子-溴化生成 R-CO-N(Br)⁻，然后 Br⁻ 离去 + R 迁移

### 2. Curtius vs Schmidt
- **Curtius**：从酰氯 → 叠氮酰 → 异氰酸酯 + N₂
- **Schmidt**：从酮 + HN₃/H⁺ → 酰胺 + N₂
- **化学原料**不同，机理上 Schmidt 经过羟胺类似的中间体

### 3. Curtius vs Wolff（Arndt-Eistert）
- **Curtius**：迁移到氮，得胺（链短一）
- **Wolff**（[[1,2-迁移与重排]]）：迁移到碳烯，得烯酮 → 酸（链长一）
- **化学计量**不同，但都涉及 N₂ 离去

### 4. 协同迁移 vs 自由氮宾路径
- 协同：迁移 + N₂ 同时进行（一步）
- 经氮宾：先得游离氮宾，再迁移（两步）
- 实验区分：动力学（一级 vs 多级）、立体保留度、捕获实验

## 八、与其他知识点的联系
- 前置知识：[[1,2-迁移与重排]]、[[卡宾]]、[[反应机理表示法]]、[[重氮化合物]]
- 相关知识：[[Hofmann重排]]、[[Schmidt重排]]、[[Beckmann重排]]、[[Wolff重排]]、[[异氰酸酯]]
- 应用知识：[[39-重排反应]]、[[51-金属有机]]、[[34-有机活性中间体]]

## 九、典型题型
- 题型-机理推断
- 题型-重排产物判断
- 决赛"由酰基叠氮预测 Curtius 重排产物"
- 决赛"R-COOH → R-NH₂ 的合成方法选择题"

## 十、例题

### 例题 1：苯甲酰叠氮的 Curtius 重排
**题目：** 写出 PhCON₃ 在加热条件下的 Curtius 重排产物及完整机理（包括捕获反应）。
**分析：**
- 加热脱 N₂，Ph 基带电子对从 C 迁移到 N
- 产物：苯异氰酸酯 PhNCO
- 在 H₂O 中水解 → 苯胺 + CO₂
**解答：**
$$\ce{Ph-CO-N=N=N ->[\Delta,\,-N2] Ph-N=C=O ->[H2O] Ph-NH-COOH -> Ph-NH2 + CO2}$$

### 例题 2：合成路线倒推
**题目：** 设计一条由乙酸（CH₃COOH）合成甲胺（CH₃NH₂）的路线。
**分析：**
- 乙酸 → 乙酰氯（SOCl₂）→ 乙酰叠氮（NaN₃）→ Curtius 重排 → 甲基异氰酸酯 → 水解
**解答：**
$$\ce{CH3COOH ->[SOCl2] CH3COCl ->[NaN3] CH3CON3 ->[\Delta] CH3-N=C=O ->[H2O] CH3NH2 + CO2}$$
注意：**链碳缩短了一个**（从 CH₃COOH 的 2C → CH₃NH₂ 的 1C）。

### 例题 3：Curtius 路径与 Hofmann 路径的对比
**题目：** 给定 R-CO-NH₂，分别用 Hofmann 重排与（先转 R-CO-N₃ 再）Curtius 重排，比较产物。
**分析：** 两种方法都得到 R-NH₂，机理相似但试剂条件不同：
- Hofmann：Br₂ + NaOH，水溶液，温和
- Curtius：先酰氯化、再 NaN₃、再加热
**解答：** 产物相同，但 Curtius 适用面更广（耐 OH⁻ 不耐的底物）。

## 十一、易错点
- 把异氰酸酯（R-N=C=O）写成异腈（R-N≡C）——前者是 N、C、O 三重态串联，后者是 N≡C 单基
- 忘记 N₂ 离去的"驱动力"——不写脱 N₂
- 把"链碳缩短一碳"误以为是产物变成羧酸——实际上 CO₂ 离开了
- 忘记 R 迁移**带电子对**（保留构型）
- Curtius 与 Wolff 混淆——前者迁移到 N，后者迁移到 C

## 十二、竞赛拓展
- **Bertho 修正**：芳基叠氮的 Curtius 类似重排
- **Smith 改良**：使用 DPPA（叠氮磷酸酯）从酸直接产生酰基叠氮
- **C-H 胺化**：金属催化的氮宾插入 C–H 键 ≠ Curtius
- **不对称 Curtius**：手性辅助控制 R 迁移立体化学
- **氮宾比卡宾稳定吗**？氮宾的孤对更倾向 sp²，比卡宾稍稳定

## 十三、外部资料出处
- 主要来源：**Abhik Ghosh & Steffen Berg, *Arrow Pushing in Inorganic Chemistry*, Wiley, 2014, §5A.10 "Nitrenes and Nitrenoids: The Curtius Rearrangement"**
- 索引：[[Arrow Pushing in Inorganic Chemistry-总索引]]
- 经典文献：
  - Curtius, T. *Ber.* **1890**, *23*, 3023（原始论文）
  - Stieglitz, J. *Am. Chem. J.* **1896**, *18*, 751（提出氮宾中间体）
- 经典综述：March, J. *Advanced Organic Chemistry*, Chapter 18

## 十四、待完善项
- [ ] 补充 Curtius vs Hofmann vs Schmidt 的实验区分判据
- [ ] 补充 DPPA-Curtius（Yamada 修正）的反应步骤
- [ ] 补充 Curtius 重排在天然产物全合成中的实例

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
WHERE contains(knowledge_points, "Curtius重排")
SORT year DESC, difficulty ASC
```
