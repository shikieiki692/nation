---
title: Dess-Martin氧化
aliases: [Dess-Martin Periodinane, DMP, IBX, 戴斯-马丁高碘烷, 2-碘酰基苯甲酸, λ⁵-iodane氧化]
type: 知识点
template_version: v1.3
subject: 有机化学
module: 有机化学
submodule: 具体反应
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-有机化学
syllabus_code: [40, 50]
syllabus_module: [有机化学, 元素化学]
tags: [化竞, 有机化学, 氧化反应, 醇氧化, 高价碘试剂, 名称反应, 主族无机]
related: [Swern氧化, 高价碘试剂, 过碘酸氧化, 醇的氧化, 有机氧化反应]
prerequisite: [醇的氧化, 有机氧化反应, 高价碘试剂]
problem_types: [题型-氧化反应试剂选择, 题型-机理推断]
difficulty: 3
importance: 4
status: 已填充
stage: published
sources: [Arrow Pushing in Inorganic Chemistry-总索引]
source_type: [书籍]
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

# Dess–Martin 氧化（IBX 与 DMP）

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-有机化学]]、[[基础要求-无机和结构化学]]
- 对应考纲条目：[[40-氧化还原反应]]、[[50-有机合成]]、[[13-元素化学]]
- 外部资料：[[Arrow Pushing in Inorganic Chemistry-总索引]] §7.12

## 一、定义
**Dess–Martin 氧化**：使用 **Dess–Martin Periodinane (DMP)** 或 **2-碘酰基苯甲酸 (IBX)** 这两类 **λ⁵-碘烷（hypervalent I(V) iodane）** 在温和条件下将伯醇/仲醇分别氧化为醛/酮的反应。

$$
\ce{RCH2OH ->[\text{IBX or DMP}] RCHO} \qquad \ce{R^1R^2CHOH ->[\text{IBX or DMP}] R^1R^2C=O}
$$

- 伯醇 → 醛（**不会过氧化为羧酸**）
- 仲醇 → 酮
- 副产物：相应的 **λ³-碘烷**（2-碘代苯甲酸 IBA）+ AcOH（DMP 释放）+ H₂O
- 操作条件：**室温，无水二氯甲烷**，5–30 min 完成

## 二、考纲对应
- 对应考纲条目：[[40-氧化还原反应]]、[[50-有机合成]]、[[13-元素化学]]（高价主族碘的化学）
- 所属模块：[[基础要求-有机化学]]
- 本知识点在考纲中的作用：**温和、室温、不过氧化**的现代醇氧化方法，是 Cr(VI)、Swern、Pfitzner-Moffatt 之后的主流选择。其机理体现"高价主族 + 五元环协同消除"的范式，与 [[Swern氧化]] 的硫叶立德机理形成对照。

## 三、核心原理

### 3.1 试剂的合成
IBX 与 DMP 由 **2-碘苯甲酸 (2-iodobenzoic acid)** 与 **过氧硫酸氢钾 (Oxone, KHSO₅)** 氧化获得 IBX，再用乙酸酐乙酰化得到 DMP：

![[ArrowPushinginInorganicChemistry_231-336_images/df9c22ab6b5f4518b6712588ee59c2b499162381a07d976434a0b63d4f8a2a1c.jpg]]

> 关键：
> - I(I) → I(V)：KHSO₅ 提供两个 O，碘从 −1/+1 价升至 +5；
> - DMP = IBX 的"乙酰化激活版"，在有机溶剂中**溶解度高**很多。

### 3.2 IBX 氧化机理（2 步：配位 → 协同环消除）

**第 1 步：醇配位至 I(V)**

醇的氧亲核进攻 IBX 的 I 中心，置换掉一个 OH（属 SN2-Si 类的"重元素亲核取代"，详见 [[SN2-Si机理]]）：

![[ArrowPushinginInorganicChemistry_231-336_images/c721cf2250289e48a1f73ad25c890b11502b4f83dd9ab88c228682f68b88ea69.jpg]]

形成的 **烷氧基-λ⁵-碘烷中间体** $\ce{R-O-I(V)}$ 是关键中间体。

**第 2 步：五元环协同过渡态**

烷氧基-λ⁵-碘烷经过 **五元环过渡态**：碘上的氧（属于 IBX 的羰基 O）拔取醇 α-H，同时 C–O–I 键断裂、I 还原为 I(III)。一步生成醛/酮 + 2-碘代苯甲酸（aryl-λ³-iodane）：

![[ArrowPushinginInorganicChemistry_231-336_images/704ec006b8a19fea2b615cc51017b09b1457f35c1ecc8466b19be9ba697e1414.jpg]]

> 这一步与 [[Swern氧化]] 第 4 步（叶立德五元环 [2,3]-σ 重排）**机理同构**：都是"在 X(高价) 上配位的 R-O-，借助 X 上的 base 拔 α-H，协同还原 X、生成 C=O"。

### 3.3 DMP 氧化机理（3 步：SN2-Si 配位 → α-H 消除 → 终产物）

**第 1 步：醇取代 DMP 的一个 OAc 基**

醇配位 I(V)，以 SN2-Si 类机理推走一个乙酸根，生成烷氧基-DMP 中间体：

![[ArrowPushinginInorganicChemistry_231-336_images/3e0907800be3c173c28106d9a02eb4d71247c080cbc9d7c091388eba9b712ae0.jpg]]

**第 2 步：剩余的 OAc⁻ 拔 α-H**

剩余的乙酸根（或新生成的醋酸盐内层亲核体）拔取烷氧 α-H，I(V) → I(III)，生成酮 + 2-碘代苯甲酸 + 2 AcOH：

![[ArrowPushinginInorganicChemistry_231-336_images/c833ae7ca0e2b0414e46af507b9b3f3ee5737fc8f06604159ce01614631b3ec9.jpg]]

> 注意：DMP 与 IBX 的本质相同（都是 λ⁵-碘烷氧化醇），区别仅在于"基底碘上挂的是 OAc 还是 OH"。

## 四、关键结论

- **氧化中心**：I(V) → I(III)，是主族高价化合物分子内氧化还原的典型例子。
- **不会过氧化醛为酸**：因为反应一旦生成 C=O，就没有 α-OH 可继续氧化（与 [[Swern氧化]] 同根同源）。
- **DMP vs IBX**：DMP 在 CH₂Cl₂ 中可溶，操作友好；IBX 仅 DMSO 可溶，且加热条件下使用。
- **反应温和**：室温即可，对烯醇化倾向底物（如 β-酮醇、α,β-不饱和醇）比 Swern 更温和。
- **副反应极少**：相比 PCC、Cr(VI) 类强氧化剂，无重金属污染、无过氧化、无脱水副反应。

## 五、常见分类或情形

| 试剂 | 缩写 | 氧化中心 | 溶解性 | 典型条件 | 备注 |
|---|---|---|---|---|---|
| **2-iodoxybenzoic acid** | **IBX** | I(V) | 仅 DMSO 可溶 | DMSO, 20–60 °C | 加热使用，价格便宜 |
| **Dess–Martin periodinane** | **DMP** | I(V) | CH₂Cl₂ 可溶 | CH₂Cl₂, RT | 室温友好，价格较贵 |
| **改良 IBX**（如 mIBX、SIBX） | — | I(V) | 各异 | 视情况 | 规避 IBX 的爆炸性 |
| **PhIO**（碘酰苯） | — | I(III/V) | — | 不同 | 单价 λ³-iodane |

> **IBX 安全提示**：纯 IBX **易爆**，受热/撞击会分解（含高能 I=O 键），实验室通常采用 SIBX（稳定化版本）。DMP 没有这个问题。

## 六、适用条件与限制

### 6.1 适用范围
- 一级醇（→ 醛）、二级醇（→ 酮）
- **不会过氧化为羧酸**（关键优势）
- 兼容大多数官能团：烯、炔、酯、酰胺、醚、卤代物、缩醛、TBS、Bn
- 兼容易烯醇化底物（比 Swern 更友好）
- IBX 在加热条件下还能将 1,2-二醇氧化裂解为二羰基（特殊条件，竞赛少见）

### 6.2 限制
- **DMP 价格较贵**，不适合大规模合成
- IBX **爆炸性**：纯品需小心处理
- 含硫底物（如硫醇、硫醚）会被氧化（副反应）
- 富电子芳烃（酚类）可能被进一步氧化（生成醌等）

## 七、常见比较与易混点

### 7.1 Dess–Martin (DMP) vs Swern

| 对比项 | DMP | [[Swern氧化]] |
|---|---|---|
| 氧化中心 | I(V) → I(III) | S(IV) → S(II) |
| 温度 | 室温 | −78 °C |
| 操作 | 简单 | 复杂、忌水 |
| 副产物气味 | AcOH + 2-碘代苯甲酸 | DMS（恶臭） |
| 对烯醇化倾向底物 | 通常更好 | 偶尔有问题 |
| 成本 | DMP 较贵，IBX 中等 | 试剂便宜 |
| 大规模可用 | 一般 | 较好 |

### 7.2 DMP vs Jones（CrO₃）vs PCC

| 对比项 | DMP / IBX | Jones | PCC |
|---|---|---|---|
| 伯醇产物 | 醛 | **羧酸**（过氧化） | 醛 |
| 选择性 | 高 | 低 | 中 |
| 重金属污染 | 无 | 含铬 | 含铬 |
| 后处理 | 简便 | 复杂 | 中等 |

### 7.3 IBX vs DMP 内部对比
- IBX 有 **未乙酰化的 OH**，在 DMSO 中溶解；
- DMP 通过 **3 个乙酰基** 提高有机溶剂溶解性；
- 二者的 **氧化机理本质相同**，均为 λ⁵-碘烷介导的"协同消除"。

### 7.4 与 [[过碘酸氧化]] 的本质区别
- **HIO₄（H₅IO₆）** 是 I(VII) → I(V)，主要用于 **顺式 1,2-二醇的氧化裂解**；
- **DMP/IBX** 是 I(V) → I(III)，主要用于 **醇 → 醛/酮**；
- 二者均利用 **环状碘酸酯过渡态**，但 HIO₄ 走"两个 O 同时取代"，DMP/IBX 走"一个 O 取代 + 一个 α-H 拔取"。

## 八、与其他知识点的联系
- 前置知识：[[醇的氧化]]、[[有机氧化反应]]、[[SN2-Si机理]]、[[高价化合物的成键]]
- 相关知识：
  - [[Swern氧化]]（同样温和的 S(IV) 介导氧化）
  - [[过碘酸氧化]]（I(VII) 氧化裂解 1,2-二醇）
  - [[高价碘试剂]]（λ³ 与 λ⁵-碘烷的总览）
- 应用知识：[[有机合成]]、[[保护基化学]]、[[多步合成路线]]

## 九、典型题型
- 题型-氧化反应试剂选择：从底物特征选 DMP/Swern/Jones/HIO₄
- 题型-机理推断：写出 IBX 或 DMP 的氧化机理（2–3 步）
- 题型-合成设计：在多步路线中选择 DMP 替代 PCC

## 十、例题

### 例题 1：机理写出
**题目：** 写出 IBX 将伯醇 RCH₂OH 氧化为 RCHO 的完整机理（2 步）。

**分析：**
- 第 1 步：RCH₂OH 配位 IBX 的 I(V)，OH⁻ 离去 → 烷氧基-λ⁵-碘烷 RCH₂-O-I(=O)(OH)Ar
- 第 2 步：五元环协同过渡态：I 上的 O（羰基 O）拔取 RCH₂- 的 α-H，同时 C–O–I 断裂 → RCHO + 2-碘代苯甲酸 + H₂O

**反思：**
注意"五元环"是 R—C—H...O=I-O 环路，是协同消除而非分步。

### 例题 2：试剂选择
**题目：** 在合成路线中需把 PhCH(OH)CH=CH₂ 氧化为肉桂醛（PhCH=CHCHO，含烯醇化倾向）。比较 PCC、Jones、DMP、Swern 的适用性。

**分析：**
- Jones：会过氧化为 PhCH(OH)CH=CHCOOH，**不行**；
- PCC：可行，但易引发烯醇化副反应；
- Swern：低温下可行，但若底物量大、操作繁琐；
- **DMP：室温友好，对烯醇化温和，最优**。

**解答：** 选 DMP / CH₂Cl₂ / RT。

## 十一、易错点
- ❌ 误以为 DMP/IBX 会过氧化醛为酸：**不会**，I(V) → I(III) 之后无更多电子流可流。
- ❌ 误以为 IBX 与 DMP 机理不同：**机理相同**，区别仅在底物溶解性和反应温度。
- ❌ 把 DMP 与 [[过碘酸氧化]] 混淆：DMP 用于醇 → 醛/酮，HIO₄ 用于二醇裂解。
- ❌ 误以为 I(V) 是稀有：本族 I 高价化合物在 IBX、IO₃⁻、HIO₄ 中都常见，与"惰性对效应"无矛盾（碘价稳定 +1, +3, +5, +7）。
- ❌ 操作 IBX 不知爆炸性：纯 IBX 受热易爆，实验室用 SIBX 或就地用 KHSO₅ 制备。

## 十二、竞赛拓展
- **Koser 试剂** $\ce{PhI(OH)OTs}$：另一类 λ³-碘烷，用于 α-羟基化、α-酮化（详见 [[高价碘试剂]]）；
- **Togni 试剂**：含 -CF₃ 的 λ³-iodane，亲电三氟甲基化试剂；
- **TPAP / NMO 氧化**：另一种"温和、不过氧化"现代方法（Ru 催化）；
- IBX 在 DMSO/加热条件下还能 **氧化苄位 C-H** 为羰基（"benzylic oxidation"）；
- IBX/DMP 与 [[β-硅基效应]]、[[硅基保护基]] 等保护基化学搭配，是现代多步合成的标配。

## 十三、外部资料出处
- [[Arrow Pushing in Inorganic Chemistry-总索引]] **§7.12 λ⁵-Iodanes: IBX and Dess–Martin Periodinane**（pp. 295-298）
- 经典文献：
  - Dess, D. B.; Martin, J. C. *J. Org. Chem.* **1983**, *48*, 4155.
  - Dess, D. B.; Martin, J. C. *J. Am. Chem. Soc.* **1991**, *113*, 7277.
  - Frigerio, M.; Santagostino, M. *Tetrahedron Lett.* **1994**, *35*, 8019.（IBX 改良）
- Wirth, T. (Ed.) *Hypervalent Iodine Chemistry*, Springer, 2003.

## 十四、待完善项
- [ ] 补充 IBX 在加热条件下的"二醇裂解"应用
- [ ] 补充 IBX 与 DMP 的环境与工艺规模评估
- [ ] 补充 SIBX、mIBX 等改良试剂的对比

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
WHERE contains(knowledge_points, "Dess-Martin氧化")
SORT year DESC, difficulty ASC
```
