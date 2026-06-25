---
title: Arbuzov反应
aliases: [Arbuzov Reaction, Michaelis-Arbuzov Reaction, 阿尔布佐夫反应, 米凯利斯-阿尔布佐夫反应, 亚磷酸酯重排]
type: 知识点
template_version: v1.3
subject: 有机化学
module: 有机化学
submodule: 具体反应
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-有机化学
syllabus_code: [48, 51]
syllabus_module: [有机化学, 名称反应, 取代反应]
tags:
  - 化竞
  - 名称反应
  - 膦化合物
  - SN2反应
  - 烷基膦酸酯合成
related: [Wittig反应, Horner-Wadsworth-Emmons反应, 鏻盐, SN2反应, 主族元素无机箭头推动法]
prerequisite: [SN2反应, 反应机理表示法, 主族元素无机箭头推动法]
problem_types: [题型-机理推断, 题型-合成路线设计]
difficulty: 3
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

# Arbuzov 反应（Michaelis-Arbuzov Reaction）

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-有机化学]]
- 对应考纲条目：[[48-膦化合物]]、[[51-金属有机]]

## 一、定义
**Arbuzov 反应（Michaelis-Arbuzov 反应）**：**三烷基亚磷酸酯（trialkyl phosphite, P(OR)₃）**与**烷基卤（R'X）**经过两步连续 SN2 反应，生成**烷基膦酸酯（alkylphosphonate, R'-P(=O)(OR)₂）**与**新的烷基卤（R-X）**的反应。

通式：
$$\ce{R^1-X + P(OR^2)3 -> R^1-P(=O)(OR^2)2 + R^2-X}$$

> 关键特征：磷原子的孤对作为亲核体进攻 R'X；最终的 P=O 键形成是反应不可逆的驱动力，故是构建 **C–P(=O) 键**最经典的方法之一。

## 二、考纲对应
- 对应考纲条目：[[48-膦化合物]]、[[51-金属有机]]
- 所属模块：[[基础要求-有机化学]]
- 本知识点在考纲中的作用：是制备烷基膦酸酯（HWE 试剂的前体）的核心方法；亦是磷化学"P=O 驱动力"原则的代表。

## 三、核心原理

### 3.1 反应总方程式
$$\ce{R^1-X + P(OR^2)3 ->[\Delta] R^1-P(=O)(OR^2)2 + R^2-X}$$

> 注意：起始磷酸酯中 P 处于 +3 氧化态（P(III)），产物中 P 处于 +5 氧化态（P(V)）。反应是磷的氧化重排过程，但**没有外加氧化剂**——氧来自原有的 OR 基团。

### 3.2 详细机理（两步 SN2）

#### 步骤 1：第一次 SN2（磷作亲核体）
P(OR²)₃ 的磷孤对进攻 R¹X 的 α 碳，X⁻ 离去，形成**烷基鏻盐中间体**：

$$\ce{(R^2O)3P: + R^1-X -> [(R^2O)3P-R^1]^+ X^-}$$

中间体特征：磷已被烷基化，形成四配位 P(IV)⁺ 鏻盐，但仍带 OR² 基团（高度反应性）。

#### 步骤 2：第二次 SN2（卤离子作亲核体）
游离的 X⁻ 进攻其中一个 OR² 基的烷基碳，使该 R² 离开为 R²X，同时 OR² 的氧上电子推回 P，形成 P=O 键：

$$\ce{[(R^2O)3P-R^1]^+ X^- -> (R^2O)2P(=O)-R^1 + R^2-X}$$

> 这一步是**双重 SN2**：X⁻ 进攻 R²-O 的 R² 端，O 同时把电子推回 P 形成 P=O。

### 3.3 驱动力分析
**P=O 键的形成是反应的根本驱动力**：
- P=O 键能 ≈ **544 kJ/mol**（远高于 P–O 单键 ≈ 335 kJ/mol、P–C 键 ≈ 264 kJ/mol）
- 烷基膦酸酯远比烷基亚磷酸酯稳定（差距约 200 kJ/mol）
- 第一步 SN2 是热力学可逆的（鏻盐能"反向"释放 R¹X）
- 第二步 SN2 一旦发生，P=O 形成后**不可逆**

### 3.4 化学计量与原子平衡
反应中**没有原子损失**——R²X 是副产物，但若 R¹ 与 R² 相同，则净结果为：
$$\ce{R-X + P(OR)3 -> R-P(=O)(OR)2 + R-X}$$
即 R-X 起"催化"作用（实际上"消耗" + "生成"等量的 R-X）——这种情况下反应可以用催化量的 R-X 启动。

## 四、关键结论

### 4.1 适用底物
- **烷基卤**：一级 > 二级 ≫ 三级（SN2 选择性）
- **碘 > 溴 > 氯**（卤的离去能力）
- **磷酸酯**：P(OMe)₃、P(OEt)₃、P(OⁱPr)₃ 等都适用

### 4.2 重要应用：HWE 试剂的合成
通过 Arbuzov 反应可合成 [[Horner-Wadsworth-Emmons反应]] 用的稳定型磷酸酯叶立德前体：
$$\ce{Br-CH2-CO2Et + P(OEt)3 -> (EtO)2P(=O)-CH2-CO2Et + EtBr}$$

得到的 (EtO)₂P(=O)-CH₂-CO₂Et 经 NaH 去质子后即为 HWE 试剂。

### 4.3 与 Wittig 试剂合成的对比
| 项 | Wittig 试剂合成 | Arbuzov + HWE |
|---|---|---|
| **试剂** | Ph₃P + R-X | P(OR')₃ + R-X |
| **产物形式** | 鏻盐 [Ph₃P-R]⁺X⁻ | 烷基膦酸酯 (R'O)₂P(=O)-R |
| **氧化态** | P(IV)⁺（盐） | P(V) |
| **后续步骤** | 强碱去质子 | 强碱去质子 |
| **副产物分离** | Ph₃P=O 难分 | (R'O)₂P(=O)O⁻ 水溶性好 |

## 五、常见分类或情形

### 5.1 标准烷基化（合成简单膦酸酯）
$$\ce{CH3I + P(OEt)3 ->[\Delta] CH3-P(=O)(OEt)2 + EtI}$$

### 5.2 含吸电子基的活泼烷基卤
$$\ce{Br-CH2-CO2Et + P(OEt)3 ->[\Delta] (EtO)2P(=O)-CH2-CO2Et + EtBr}$$

> 含 -CO₂R、-CN、-CHO 等吸电子基的 α-溴化物在 Arbuzov 中反应顺利——这些产物后续可用于 HWE。

### 5.3 苄基/烯丙基卤
$$\ce{PhCH2Br + P(OMe)3 ->[\Delta] PhCH2-P(=O)(OMe)2 + MeBr}$$

### 5.4 例题中的醛-α-溴化物
书中习题 5B.14：
$$\ce{P(OEt)3 + Br-CH2-CHO -> (EtO)2P(=O)-CH2-CHO + EtBr}$$

> 这类产物可直接用于 HWE 反应（与 Wittig 互补，主产 E-烯）。

## 六、适用条件与限制

### 适用条件
- ✓ 加热（80–160 ℃，无溶剂或苯/甲苯）
- ✓ 一级烷基卤（最佳）
- ✓ 含吸电子基的二级烷基卤（活化）
- ✓ 卤离子离去能力：I > Br > Cl

### 限制
- ✗ 三级烷基卤：SN2 受阻，倾向 E2 消除
- ✗ 烯基卤、芳基卤：SN2 不可发生
- ✗ 含质子源（OH、NH）的底物：磷酸酯水解
- ✗ 对位阻很大的"新戊基"型 R-X：反应缓慢

### 副反应
- 烯醇互变（如果 R-X 含 α-CH 与酸性官能团）
- 过度烷基化（少见）

## 七、常见比较与易混点

### 1. Arbuzov vs Wittig 试剂合成
- **Arbuzov**：P(OR)₃ + RX → 烷基膦酸酯（产生 P=O）
- **Wittig 鏻盐合成**：Ph₃P + RX → [Ph₃P-R]⁺X⁻（不变 P 氧化态）
- **共同点**：都是 P 上孤对 SN2 进攻 R-X

### 2. Arbuzov vs Perkow 反应
- **Arbuzov**：P(OR)₃ + RX（一般烷基卤）→ 烷基膦酸酯（C-P(=O) 键）
- **Perkow**：P(OR)₃ + α-卤代羰基 → 烯醇磷酸酯（O-P(=O) 键）
- **机理差异**：Perkow 中 P 进攻 C=O 的氧而非 α-碳；α-卤代羰基的特殊电子结构使两条路径并存。

### 3. Arbuzov 中 R¹ 与 R²
- 注意三个 OR² 基团**等价**
- 第二步 SN2 中 X⁻ 可进攻任意一个 OR² 的 R² 端
- 若 R¹ = R²，反应自洽；若不同，则净结果是用 R¹ 替换一个 R² 并释放 R²X

### 4. P 氧化态变化
- 起始：P(OR)₃ 中 P 是 +3 氧化态（每个 P-O 算 +1）
- 产物：R-P(=O)(OR)₂ 中 P 是 +5 氧化态
- **没有外加氧化剂**——氧化是分子内发生的（O 从 R-O-P 转到 P=O）

## 八、与其他知识点的联系
- 前置知识：[[SN2反应]]、[[反应机理表示法]]、[[主族元素无机箭头推动法]]
- 相关知识：[[Wittig反应]]、[[Horner-Wadsworth-Emmons反应]]、[[鏻盐]]、[[亚磷酸酯]]
- 应用知识：[[48-膦化合物]]、[[51-金属有机]]

## 九、典型题型
- 题型-机理推断
- 题型-合成路线设计
- 决赛"由膦酸酯反向推 Arbuzov 反应物"
- 决赛"两步 SN2 机理填空"

## 十、例题

### 例题 1：基础 Arbuzov 反应
**题目：** 写出 EtI + P(OMe)₃ 加热条件下的反应方程式与机理。
**分析：**
- P(OMe)₃ 的磷孤对作亲核体进攻 EtI 的乙基碳
- 形成 [(MeO)₃P-Et]⁺I⁻ 鏻盐中间体
- I⁻ 进攻其中一个 OMe 的甲基，MeI 离去
- 同时 OMe 的氧推电子回 P，形成 P=O 键
**解答：**
$$\ce{EtI + P(OMe)3 ->[\Delta] Et-P(=O)(OMe)2 + MeI}$$

### 例题 2：HWE 试剂合成
**题目：** 设计一条合成 (EtO)₂P(=O)-CH₂-CO₂Et 的路线。
**分析：**
- 目标分子骨架：(EtO)₂P(=O)-CH₂-CO₂Et
- 切断 P-CH₂ 键 → P(OEt)₃ + Br-CH₂-CO₂Et
- 用 Arbuzov 反应连接
**解答：**
$$\ce{P(OEt)3 + Br-CH2-CO2Et ->[\Delta,\,140℃] (EtO)2P(=O)-CH2-CO2Et + EtBr}$$
此产物经 NaH 去质子后即为标准 HWE 试剂。

### 例题 3：机理填空
**题目：** 在 P(OR)₃ + RX → R-P(=O)(OR)₂ + RX 中，写明两步的箭头推动。
**解答：**
- 第一步：P 的孤对推向 R-X 的 R-C，X 离去（SN2）
- 第二步：X⁻ 进攻 OR 的 R 端，OR 的 O 推电子回 P 形成 P=O（SN2 + 共振）

## 十一、易错点
- 把"Arbuzov 反应"误解为只是单步 SN2——必须强调**两步**
- 忘记第二步中 X⁻ 进攻的是 OR 的 R 端而不是其他位置
- 写错产物：把 R-P(=O)(OR)₂ 写成 R-P(OR)₃ 或 R₂-P(OR)₂
- 忽视 P=O 键形成是驱动力——只看 SN2 易让人觉得反应可逆
- 用三级卤代烃尝试反应——SN2 不通，会消除而非进攻

## 十二、竞赛拓展
- **Perkow 反应**：α-卤代羰基底物的特殊路径（O-P 键 vs C-P 键）
- **Pudovik 反应**：H-膦酸酯加成到 C=O（亲核加成而非取代）
- **Atherton-Todd 反应**：H-膦酸酯 + R-OH/R-NH₂ → 磷酸酯/磷酰胺（CCl₄ 介导）
- **Mitsunobu 反应**：R-OH + R'-Y + DIAD + Ph₃P → R-Y + ... （磷化学的另一典型应用）
- **金属催化的 Arbuzov 类反应**：Pd 催化的 ArX + P(OR)₃ → ArP(=O)(OR)₂

## 十三、外部资料出处
- 主要来源：**Abhik Ghosh & Steffen Berg, *Arrow Pushing in Inorganic Chemistry*, Wiley, 2014, §5B.8 "The Arbuzov Reaction"**
- 索引：[[Arrow Pushing in Inorganic Chemistry-总索引]]
- 经典文献：
  - Michaelis, A.; Kaehne, R. *Ber.* **1898**, *31*, 1048（最早报道）
  - Arbuzov, A. E. *J. Russ. Phys. Chem. Soc.* **1906**, *38*, 687（机理研究）
- 经典综述：Bhattacharya, A. K.; Thyagarajan, G. *Chem. Rev.* **1981**, *81*, 415–430

## 十四、待完善项
- [ ] 补充 Perkow 反应的具体例子与判据
- [ ] 补充 Arbuzov 在 PROTAC 类配体合成中的应用
- [ ] 补充金属催化版本的反应条件与底物范围

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
WHERE contains(knowledge_points, "Arbuzov反应")
SORT year DESC, difficulty ASC
```
