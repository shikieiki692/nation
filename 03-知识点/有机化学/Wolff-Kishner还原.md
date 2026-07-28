---
title: Wolff-Kishner还原
aliases: [Wolff-Kishner Reduction, Wolff-Kishner-Huang Reduction, 黄鸣龙还原, Huang Minlon, 沃尔夫-基希纳-黄鸣龙]
type: 知识点
template_version: v1.3
subject: 有机化学
module: 有机化学
submodule: 具体反应
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-有机化学
syllabus_code: [47, 51]
syllabus_module: [有机还原, 名称反应, 有机合成]
tags:
  - 化竞
  - 有机还原反应
  - 名称反应
  - 黄鸣龙改良
  - 一锅法
related: [Shapiro反应, Clemmensen还原, 重氮化合物, 肼, 1,2-迁移与重排]
prerequisite: [有机还原反应, 亲核加成, 反应机理表示法]
problem_types: [题型-还原反应判断, 题型-机理推断]
difficulty: 3
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
source_extracts:
  - source_file: "[[07-资料提炼/书籍提炼/提炼-Clayden-第23章-化学选择性和保护基]]"
    asset_id: "Clayden-第23章-化学选择性和保护基"
    asset_type: "书籍提炼"
    asset_summary: "Wolff-Kishner还原相关内容"
  - source_file: "[[07-资料提炼/书籍提炼/提炼-上海中学竞赛课程-第四分册-芳香烃]]"
    asset_id: "上海中学竞赛课程-第四分册-芳香烃"
    asset_type: "书籍提炼"
    asset_summary: "Wolff-Kishner还原相关内容"
  - source_file: "[[07-资料提炼/网课资料/Zchem 基础有机化学/资料提炼-Zchem基础有机化学-批次Z-G-综合复习与例题]]"
    asset_id: "Zchem基础有机化学-批次Z-G-综合复习与例题"
    asset_type: "网课资料"
    asset_summary: "Wolff-Kishner还原相关内容"
---
# Wolff-Kishner 还原（Wolff-Kishner-黄鸣龙还原）
- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-有机化学]]
- 对应考纲条目：47-氧化反应、[[51-金属有机]]

## 一、定义
**Wolff-Kishner 还原**：将羰基化合物（醛/酮）的 C=O 还原为 **CH₂**（亚甲基）的反应。两步法：先与肼（NH₂NH₂）形成腙，再在强碱下加热脱 N₂ 得到亚甲基产物。

通式：
$$\ce{R^1-C(=O)-R^2 ->[NH2NH2,\,KOH,\,\Delta] R^1-CH2-R^2 + N2}$$

> **黄鸣龙改良**（1946）：将传统的两步分离过程合并为"一锅法"——直接在乙二醇中加热反应，使该反应成为最实用的羰基还原至甲烯的方法。

## 二、考纲对应
- 对应考纲条目：47-氧化反应、[[51-金属有机]]
- 所属模块：[[基础要求-有机化学]]
- 本知识点在考纲中的作用：经典名称反应，与 [[Clemmensen还原]] 互补，是碱性条件下"羰基 → 甲烯"的标准方法。竞赛考察机理填空与底物兼容性判断。

## 三、核心原理

### 3.1 总反应方程式（黄鸣龙改良条件）
腙在乙二醇 + 强碱（KOH 或 NaOH）下加热到约 200 ℃，N₂ 离去，烯醇质子化得到亚甲基产物：

!

#### 步骤 2：异构化为偶氮（C 上质子化）
腙负离子的 N⁻ 推电子，异构成"二亚胺式"碳负离子，然后在 C 上质子化：

!

> 这步把负电荷从 N 移到 C 上——为后续脱 N₂ 做准备。

#### 步骤 3：再次去质子化
α-CH 又被强碱去质子，得到与重氮甲烷类似的"碳-N=N⁻"中间体：

!

#### 步骤 4：N₂ 离去，生成碳负离子
$$\ce{R^1R^2C=N-N: ^- -> R^1R^2C: ^- + N2}$$

或更准确地说：α-碳上的 H 离开 + 同步 N₂ 离去（E1cb 类型机理）→ 形成 R₁R₂CH⁻ 碳负离子：

!

#### 步骤 5：碳负离子被质子化得到产物 CH₂
碳负离子在乙二醇/水中迅速被质子化：
$$\ce{R^1R^2CH^- + H2O -> R^1R^2CH2 + OH^-}$$

最终产物：羰基 → CH₂，N₂ 已脱去。

### 3.3 驱动力分析
- **N₂ 形成的稳定性**：N₂ 的键能 ≈ 945 kJ/mol，离去后释放大量稳定化能
- **强碱条件**：保持腙处于去质子化形式，便于推电子机理
- **高温**：克服第 4 步的活化能

## 四、关键结论

### 4.1 适用底物
- **酮和醛**：均可
- 含有酸性 α-H 的酮反应良好
- 能耐受 -OH、-OR、-NR₂、-Cl、-NO₂、-CN 等基团

### 4.2 与 Clemmensen 还原的互补
| 项 | Wolff-Kishner | Clemmensen |
|---|---|---|
| **试剂** | NH₂NH₂ + KOH/HOCH₂CH₂OH | Zn(Hg) + 浓 HCl |
| **条件** | 强碱性（pH > 12） | 强酸性（pH < 1） |
| **温度** | 高温（180–220 ℃） | 中等（70–80 ℃） |
| **底物兼容** | 不耐酸性基团（缩醛、酸敏） | 不耐碱性基团（酯、酰胺） |
| **机理** | E1cb-像（脱 N₂） | 不完全清楚（含锌离子催化） |

> 选择规则：含**碱敏官能团**（如酯）选 Clemmensen；含**酸敏官能团**（如缩醛）选 Wolff-Kishner。

### 4.3 与 Shapiro 反应的对比
- **Wolff-Kishner**：腙 + 碱 + 热 → 烷烃（羰基 → CH₂）
- **Shapiro**：对甲苯磺酰腙（tosylhydrazone）+ 强碱（n-BuLi）→ 烯烃（C=O → C=C）
- 两者都涉及肼/腙化学，但 Shapiro 的 N₂ 离去同时生成乙烯负离子（vinyl carbanion），加质子或加亲电体得到烯烃产物。

### 4.4 黄鸣龙改良的意义
原始 Wolff-Kishner（1911-1912）需要：
1. 先分离腙
2. 再封闭管中加热到 200 ℃ 以上
3. 极不安全且难操作

**黄鸣龙改良**（1946）：
1. 将腙形成与脱氮合并为**一锅法**
2. 用乙二醇/KOH 体系
3. 室压加热，操作大幅简化

> 这一改良使该反应从仅有理论价值变为**重要的实用合成方法**——是中国有机化学家对世界最重要的贡献之一。

## 五、常见分类或情形

### 5.1 简单酮的还原
$$\ce{C6H5-CO-CH3 ->[NH2NH2,\,KOH,\,HOCH2CH2OH,\,200℃] C6H5-CH2-CH3}$$

### 5.2 醛的还原
$$\ce{C6H5-CHO ->[NH2NH2,\,KOH,\,HOCH2CH2OH,\,200℃] C6H5-CH3}$$

### 5.3 酸敏底物（缩醛、烯醇醚）
有缩醛（如糖类衍生物）的酮可以用 Wolff-Kishner（不会去保护），但不可用 Clemmensen（强酸会水解缩醛）。

### 5.4 多功能底物的选择性
若同一分子有酮 + 酯，Wolff-Kishner 选择性还原酮，酯保留：
$$\ce{R-CO-CH2-CO-OEt ->[\text{Wolff-Kishner}] R-CH2-CH2-CO-OEt}$$

## 六、适用条件与限制

### 适用条件
- ✓ 酮、醛
- ✓ 强碱稳定的官能团：-OH、-OR、-NR₂、-Cl、-Br、-NO₂、-CN
- ✓ 大量黄鸣龙反应在 200 ℃ 实施

### 限制
- ✗ 容易在强碱下消除（β-OH 或 β-X）的底物
- ✗ 容易在高温下水解（酯、酰胺有时会水解）
- ✗ α 位有重要基团需保留时——会丢质子参与异构

## 七、常见比较与易混点

### 1. Wolff-Kishner vs Clemmensen
（见 4.2 节比较表）

### 2. Wolff-Kishner vs Mozingo（脱硫）
- Wolff-Kishner：羰基 + 肼 → CH₂
- Mozingo：羰基 → 二硫缩硫醛（mercaptal）→ Raney Ni → CH₂
- Mozingo 适用于全部羰基，包括酯、酸；条件相对温和

### 3. Wolff-Kishner vs Shapiro
（见 4.3 节）

### 4. 腙的两种共振形式
- N⁻=N (二亚胺式)
- N=N⁻ (重氮甲烷式)
- 两者电子分布不同，影响机理书写。书写机理时通常画成由 N 上推电子驱动 H+ 转移到 C。

### 5. 不要混淆"腙"与"腙的负离子"
- 腙：R₁R₂C=N-NH₂（中性，胺氮上有 H）
- 腙的负离子：R₁R₂C=N-NH⁻（去质子化的）
- Wolff-Kishner 机理涉及多步去质子-质子化，必须明确每一步的状态

## 八、与其他知识点的联系
- 前置知识：[[亲核加成]]、[[反应机理表示法]]、[[有机酸碱性]]、[[E1cb反应]]
- 相关知识：[[Clemmensen还原]]、Shapiro反应、[[重氮化合物]]、[[1,2-迁移与重排]]
- 应用知识：[[51-金属有机]]、47-氧化反应

## 九、典型题型
- 题型-还原反应判断
- 题型-机理推断
- 决赛"Wolff-Kishner vs Clemmensen 选择题"
- 决赛"用 Wolff-Kishner 还原写出多步合成路线"

## 十、例题

### 例题 1：基础应用
**题目：** 将 2-苯基环戊酮还原为 1-苯基环戊烷，写反应方程式与试剂条件。
**分析：**
- 基本思路：羰基 → CH₂
- 选择 Wolff-Kishner 还原
**解答：**
$$\ce{2-Ph-Cyclopentanone ->[NH2NH2,\,KOH,\,HOCH2CH2OH,\,200℃] 1-Ph-Cyclopentane + N2 + H2O}$$

### 例题 2：含酯基底物的选择性
**题目：** 化合物 PhCH(CO₂Me)-CO-Ph 用 Wolff-Kishner 处理。预测产物。
**分析：**
- 酮羰基 → CH₂
- 酯基（虽然碱不稳定，但反应温度下若控制时间，可选择性保留）
- 实际上长时间加热会水解酯
**解答：** 短时间反应：PhCH(CO₂Me)-CH₂-Ph（产物 A）
长时间反应：PhCH(COOH)-CH₂-Ph（产物 B，酯水解为酸）
> 此题考察"反应时间"对选择性的影响。

### 例题 3：机理填空
**题目：** 写出 Wolff-Kishner 还原中"腙 → 碳负离子"的关键三步。
**解答：**
1. 强碱去质子化 NH 质子 → 腙阴离子
2. 异构化（推电子到 C）+ C 上加质子 → 偶氮中间体
3. 再次去质子化（α-CH 上）+ 同步脱 N₂ → 碳负离子

## 十一、易错点
- 用 Wolff-Kishner 时使用"水"作溶剂——温度不够（沸点 100 ℃），需要乙二醇
- 误以为 Wolff-Kishner 在酸性条件下可行——实际是**强碱条件**
- 忘记 N₂ 是离去的（写成 NH₃ 或 N₂H₂）
- 将 Wolff-Kishner 与 Wolff 重排混淆——前者还原，后者重排到烯酮
- 忽视黄鸣龙改良——这是真正的实用条件
- 在含醛的多羰基化合物中没有意识到醛会先反应

## 十二、竞赛拓展
- **新型一锅法 Wolff-Kishner**：用 t-BuOK/DMSO 在更低温度下进行
- **不对称 Wolff-Kishner**：手性肼控制还原立体化学
- **黄鸣龙的研究背景**：留法回国后改良条件，发表于 J. Am. Chem. Soc. **1946**，是中国有机化学的标志性贡献
- **酮还原的合成树**：
  - 酸性官能团兼容 → Wolff-Kishner（含黄鸣龙改良）
  - 碱性官能团兼容 → Clemmensen
  - 中性 → Mozingo（脱硫）

## 十三、外部资料出处
- 主要来源：**Abhik Ghosh & Steffen Berg, *Arrow Pushing in Inorganic Chemistry*, Wiley, 2014, §5A.8 "Imines and Related Functional Groups: The Wolff-Kishner Reduction and the Shapiro Reaction"**
- 索引：[[Arrow Pushing in Inorganic Chemistry-总索引]]
- 经典文献：
  - Kishner, N. *J. Russ. Phys. Chem. Soc.* **1911**, *43*, 582
  - Wolff, L. *Justus Liebigs Ann. Chem.* **1912**, *394*, 86
  - **Huang, M.-L. (黄鸣龙) *J. Am. Chem. Soc.* 1946, 68, 2487**（黄鸣龙改良）

## 十四、待完善项
- [x] 补充黄鸣龙改良前后的对比表：见下方 §14.1
- [x] 补充 Wolff-Kishner 在天然产物合成中的实例：见下方 §14.2
- [x] 补充与 NaBH₄/LiAlH₄ 的"目标官能团"比较表：见下方 §14.3

### 14.1 黄鸣龙改良法 vs 经典 Wolff-Kishner

| 特征 | 经典 W-K (1912) | 黄鸣龙改良 (1946) |
|:---|:---|:---|
| 条件 | 高温高压封管 (200°C) | 常压回流 (180-200°C) |
| 溶剂 | 无水乙醇 | 二甘醇 (DEG) |
| 碱 | Na 或 NaOEt | NaOH 或 KOH |
| 肼 | 无水 N₂H₄ | 85% N₂H₄·H₂O |
| 操作 | 需高压釜 | 常压，安全简便 |
| 产率 | 50-70% | 70-90% |

### 14.2 天然产物合成中的 W-K 实例

- **类固醇合成**：甾体酮的 C=O → CH₂ 是 W-K 还原的经典应用
- **萜类化合物**：天然萜类中的酮基还原
- **Corey 前列腺素合成**：关键中间体酮基通过 W-K 还原

### 14.3 还原剂"目标官能团"对比表

| 还原剂 | 醛 | 酮 | 酯 | 羧酸 | 酰胺 | 烯烃 | C=O→CH₂ |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| NaBH₄ | Y | Y | N | N | N | N | N |
| LiAlH₄ | Y | Y | Y | Y | Y | N | N |
| DIBAL-H | Y | Y | Y(→醛) | N | N | N | N |
| H₂/Pd | Y | N | N | N | N | Y | N |
| W-K | Y | Y | N | N | N | N | Y |
| Clemmensen | Y | Y | N | N | N | N | Y |

**W-K vs Clemmensen**：W-K 碱性条件，适合对酸敏感底物；Clemmensen 酸性条件，适合对碱敏感底物。两者互补。

---

```dataview
TABLE file.name AS "文件名", year AS "年份", type AS "题型", difficulty AS "难度"
FROM "04-题库"
WHERE contains(knowledge_points, "Wolff-Kishner还原")
SORT year DESC, difficulty ASC
```

## 十二、🎯 教学视角

## 十三、竞赛拓展

## 十四、外部资料出处

## 十五、待完善项
