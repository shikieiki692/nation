---
title: Wittig反应
aliases: [Wittig Reaction, Wittig 烯化, 维蒂希反应, 维蒂格反应, P-烯化]
type: 知识点
template_version: v1.3
subject: 有机化学
module: 有机化学
submodule: 具体反应
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-有机化学
syllabus_code: [48, 51]
syllabus_module: [有机化学, 名称反应]
tags:
  - 化竞
  - 有机化学
  - 名称反应
  - 膦化合物
  - 烯烃合成
related: [叶立德, Horner-Wadsworth-Emmons反应, 烯烃合成, 鏻盐, Arbuzov反应]
prerequisite: [叶立德, 亲核加成, 主族元素无机箭头推动法]
problem_types: [题型-叶立德反应, 题型-烯烃合成]
difficulty: 4
importance: 5
status: 已填充
stage: published
sources: [Arrow Pushing in Inorganic Chemistry-总索引]
source_type: []
review_cycle: 30d
has_images: false
images_priority: 结构/机理 medium，纯公式 low
images_note: 
teaching_ready: false
source_notes: []
key_images: []
updated: 2026-05-25
---
# Wittig 反应（Wittig Reaction）
- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-有机化学]]
- 对应考纲条目：[[48-膦化合物]]、[[51-金属有机]]

## 一、定义
**Wittig 反应**：羰基化合物（醛/酮）与三苯基膦叶立德（**Wittig 试剂**）反应，生成**烯烃**和**三苯基氧化膦**（Ph₃P=O）。

通式：
$$\ce{Ph3P=CHR^1 + R^2CHO -> R^1HC=CHR^2 + Ph3P=O}$$

> 这是定向合成 C=C 的最经典方法之一。Georg Wittig 因此获得 1979 年诺贝尔化学奖（与 H. C. Brown 共享）。

## 二、考纲对应
- 对应考纲条目：[[48-膦化合物]]、[[51-金属有机]]
- 所属模块：[[基础要求-有机化学]]
- 本知识点在考纲中的作用：是有机合成方法、磷化学、立体选择性的核心交点；竞赛常考反应物倒推、立体化学预测、机理填空。

## 三、核心原理

### 3.1 Wittig 试剂的制备
**两步法**：（1）三苯基膦 + 烷基卤 → 鏻盐；（2）强碱（n-BuLi、NaH）去质子化 → Wittig 试剂（叶立德）：

![[ArrowPushinginInorganicChemistry_101-230_images/b0353198f8488d07a1aea451c1bcbf47e9875bb08cf8fdfef77265147cf85128.jpg]]

叶立德的两个共振结构：
$$\ce{Ph3P^+ - CHR^- <-> Ph3P=CHR}$$

> 第一种偶极结构突出"叶立德"碳的**碳负离子性质**；第二种突出"半双键"性质。

### 3.2 反应总机理（4 步）

#### 步骤 1：亲核加成
叶立德碳作为强亲核体，进攻醛/酮羰基碳：

$$\ce{Ph3P^+-CHR^1 + R^2-CHO -> Ph3P^+-CHR^1-CHR^2-O^-}$$

得到的两性离子产物称为**甜菜碱（betaine）**。

#### 步骤 2：环化形成 4 元环
甜菜碱的 O⁻ 与 P⁺ 关闭成 4 元环——**氧鏻杂环丁烷（oxaphosphetane）**：

![[ArrowPushinginInorganicChemistry_101-230_images/31c4faf1da7c0115686a86708c5bb464890cd3a3b13e69f8a873ae804248d8c7.jpg]]

> 这是一个 P–O 键 + C–C 键 + C–O 键 + P–C 键的张力环——即将 [2+2] 逆切。

#### 步骤 3：环开裂（[2+2] 逆切）
张力环在反应条件下断裂，生成烯烃 + 三苯基氧化膦：

![[ArrowPushinginInorganicChemistry_101-230_images/92d7aafa5e837183c70d0232c14ce1060b124507b7e623aa1b265c90ae9470c4.jpg]]

#### 步骤 4：完成
最终产物 = 烯烃 + Ph₃P=O。

### 3.3 驱动力分析
**最终一步是热力学驱动**：
- P=O 键能 ≈ 544 kJ/mol（远高于 P–C 键 ≈ 264 kJ/mol、C=O 键 ≈ 740 kJ/mol、C=C 键 ≈ 614 kJ/mol）
- 总反应释放约 50–100 kJ/mol（视底物而定）

> "P–O 键形成"是几乎所有磷化学反应（[[Arbuzov反应]]、[[Horner-Wadsworth-Emmons反应]] 等）的驱动力。

## 四、关键结论

### 4.1 立体化学（顺反选择性）
| 试剂类型 | α-取代特点 | 主产物 |
|---|---|---|
| **非稳定**叶立德（α-H 强烈酸性，碱性碳负离子） | 烷基/无吸电子基 | **Z**-烯（顺式，动力学控制） |
| **稳定**叶立德（α-CO₂R、CN、Ph 等吸电子基稳定） | 吸电子基 | **E**-烯（反式，热力学控制） |
| **半稳定**叶立德 | 苄基、烯丙基等 | E + Z 混合 |

> 关键原理：稳定叶立德反应慢、可逆，最终走向更稳定的 E-异构；非稳定叶立德快速、不可逆，保留动力学产物 Z。

### 4.2 与其他烯化反应的比较
| 反应 | 试剂 | 主产物 | 特点 |
|---|---|---|---|
| **Wittig** | Ph₃P=CHR | Z 或 E（视稳定性） | 最经典 |
| **HWE**（[[Horner-Wadsworth-Emmons反应]]） | (RO)₂P(O)-CHR-CO₂R' | 主要 E | 试剂稳定性高 |
| **Peterson**（[[Peterson烯化反应]]） | R₃Si-CHR-Li | 视底物 | Si 替代 P |
| **Julia-Kocienski** | RSO₂-CHR-Li | 主要 E | 砜替代鏻 |

### 4.3 适用底物范围
- **C=O**：醛 ✓（高产率）、酮 ✓（中产率，受位阻影响）
- **不适用**：α,β-不饱和酮的 1,4-加成是副反应；高度位阻酮难反应
- **官能团相容性**：宽广（醇、酯、酰胺、醚等基本不影响）

## 五、常见分类或情形

### 5.1 醛 + 非稳定叶立德 → Z-烯
$$\ce{PhCHO + Ph3P=CH-CH3 -> Ph-CH=CH-CH3\,(Z) + Ph3P=O}$$

### 5.2 醛 + 稳定叶立德 → E-烯
$$\ce{PhCHO + Ph3P=CH-CO2Et -> Ph-CH=CH-CO2Et\,(E) + Ph3P=O}$$

### 5.3 酮 + 叶立德
酮反应慢于醛，需更长时间或更强叶立德。

### 5.4 复杂底物：天然产物合成
Wittig 是 β-胡萝卜素、维生素 A、前列腺素等合成的关键步骤，特别在保留多个手性中心时有不可替代性。

### 5.5 催化型 Wittig（绿色化学）
传统 Wittig 的最大缺陷是**原子经济性差**（Ph₃P=O 大分子副产）：
$$\%\text{原子经济} = \frac{\text{产物分子量}}{\text{反应物分子量之和}} \times 100\%$$

催化型设计：在反应中**还原 Ph₃P=O 回 Ph₃P**，使三苯基膦只需催化量。O'Brien 等（2009）发现 Ph₂SiH₂ 可在 100℃ 还原 R₃P=O：

![[ArrowPushinginInorganicChemistry_101-230_images/c22c0f896e2fb5140bf37a2fad4f40927c5904ea7f93ebce6e4aa44ca4e9baa5.jpg]]

## 六、适用条件与限制

### 适用条件
- ✓ 醛酮 + 强亲核叶立德
- ✓ 极性非质子溶剂（THF、Et₂O、DMSO）
- ✓ 无水无氧（避免叶立德质子化与水解）

### 限制
- ✗ 高度位阻底物（如新戊酮）反应缓慢
- ✗ Ph₃P=O 副产分离麻烦（极性接近产物时尤其困难）
- ✗ 原子经济性差（除非用催化版本）

## 七、常见比较与易混点

### 1. Wittig vs HWE
- **Wittig**：用 Ph₃P=CHR 叶立德；多数为 Z-烯（非稳定试剂）
- **HWE**（[[Horner-Wadsworth-Emmons反应]]）：用 (RO)₂P(O)-CHR-CO₂R' 磷酸酯负离子；几乎全为 E-烯
- 实验区别：HWE 副产 (RO)₂P(O)O⁻（水溶性好分离），Wittig 副产 Ph₃P=O（难分）

### 2. Wittig vs Peterson
- 两者机理类似（4 元环 [2+2] 逆切）
- Peterson（[[Peterson烯化反应]]）：4 元环含 Si–O 键
- Wittig：4 元环含 P–O 键
- Peterson 试剂便宜易得，但副产 Me₃SiOH 不利环境

### 3. 叶立德 vs 烯醇负离子
- 叶立德：α 碳负离子受 P⁺ 邻位稳定，不可与质子源接触
- 烯醇负离子：α 碳负离子受 C=O 共振稳定
- 两者机理上等同，但化学环境差异大

### 4. 顺反选择的机理来源
- 早期"betaine 假说"：4 元环优先形成 anti-betaine → Z-烯
- 现代"协同 [2+2] 加成"：四中心过渡态直接控制立体，cis-oxaphosphetane → Z-烯

## 八、与其他知识点的联系
- 前置知识：[[叶立德]]、[[亲核加成]]、[[反应机理表示法]]、[[主族元素无机箭头推动法]]
- 相关知识：[[Horner-Wadsworth-Emmons反应]]、[[Arbuzov反应]]、[[Peterson烯化反应]]、[[叶立德]]
- 应用知识：[[51-金属有机]]、[[48-膦化合物]]

## 九、典型题型
- 题型-叶立德反应
- 题型-烯烃合成
- 决赛"Wittig 反应产物的 E/Z 判断"
- 决赛"由目标烯烃倒推 Wittig 试剂与醛酮"

## 十、例题

### 例题 1：从产物倒推 Wittig 试剂
**题目：** 用 Wittig 反应合成 (E)-PhCH=CH-CO₂Et，给出反应物。
**分析：**
- 切断双键：PhCHO + Ph₃P=CH-CO₂Et（稳定叶立德 → 主产 E）
- 或：Ph₃P=CHPh + EtO₂C-CHO（半稳定 + 稳定底物）
**解答：** 推荐第一组；先合成 BrCH₂CO₂Et + Ph₃P → [Ph₃P-CH₂CO₂Et]Br⁻ → 稀 NaOH 去质子 → Ph₃P=CH-CO₂Et，与 PhCHO 反应即得目标产物 (E)。

### 例题 2：Wittig 反应机理写出
**题目：** 写出 Ph₃P=CH₂ + PhCHO 的完整机理。
**分析：**
- 叶立德 C 攻击 PhCHO 的 C
- 形成 betaine（zwitterion）
- 闭环为 oxaphosphetane（4 元杂环）
- [2+2] 逆切给烯烃 + Ph₃P=O
**解答：** 见 3.2 节图示步骤 1-4；产物为 PhCH=CH₂ + Ph₃P=O。

### 例题 3：催化版 Wittig
**题目：** 解释 Ph₂SiH₂ 在催化型 Wittig 中的作用。
**分析：**
- Ph₂SiH₂ 还原 R₃P=O 为 R₃P
- 同时 Si 形成稳定 Si–O 键（驱动力）
**解答：** Ph₂SiH₂ 通过 Si–H 与 P=O 的 σ-bond metathesis 把 P=O 还原为 P，同时生成 Ph₂Si=O（或继续聚合的硅氧），让 P 能再次循环参与 Wittig。

## 十一、易错点
- 把鏻盐误以为是 Wittig 试剂——必须经过去质子才是叶立德
- 选错碱：太弱去质子化不彻底，太强会进攻醛酮
- 忘记区分稳定/非稳定叶立德——立体化学搞反
- 把 4 元中间体误认为协同 [4+2]——它是 [2+2] 加成（PEriphery 4 中心）
- 把 P=O 与 N=O 混淆——只有 P=O 是 Wittig 的驱动力
- 直接对 α,β-不饱和酮做 Wittig 时应注意 1,2 vs 1,4 加成的竞争

## 十二、竞赛拓展
- **Bestmann-Ohira 试剂**：从醛 → 末端炔的"Wittig 类"反应
- **Brückner 改良**：在 Wittig 中用相转移催化使立体化学可调
- **不对称 Wittig**：用手性叶立德进行立体专一合成
- **Mitsunobu-Wittig 串联**：醇 + Ph₃P + Wittig → 直接烯化

## 十三、外部资料出处
- 主要来源：**Abhik Ghosh & Steffen Berg, *Arrow Pushing in Inorganic Chemistry*, Wiley, 2014, §5B.9 "The Wittig and Related Reactions: Phosphorus Ylides"**
- 索引：[[Arrow Pushing in Inorganic Chemistry-总索引]]
- 经典文献：
  - Wittig, G.; Schöllkopf, U. *Chem. Ber.* **1954**, *87*, 1318（原始论文）
  - O'Brien, C. J., et al. *Angew. Chem. Int. Ed.* **2009**, *48*, 6836–6839（催化版本）
- 经典综述：March, J. *Advanced Organic Chemistry*, Chapter 16

## 十四、待完善项
- [ ] 补充 Schlosser 改良（顺反控制）
- [ ] 补充 P=O 还原的具体条件与底物范围
- [ ] 补充 Bestmann-Ohira 在末端炔合成中的具体例子

---

```dataview
TABLE file.name AS "文件名", year AS "年份", type AS "题型", difficulty AS "难度"
FROM "04-题库"
WHERE contains(knowledge_points, "Wittig反应")
SORT year DESC, difficulty ASC
```

## 十二、🎯 教学视角

## 十三、竞赛拓展

## 十四、外部资料出处

## 十五、待完善项
