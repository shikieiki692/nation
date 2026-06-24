---
title: pH
aliases: [pH值, pOH]
type: 知识点
template_version: v1.3
subject: 化学原理
module: 化学原理
submodule: 酸碱平衡
syllabus_stage: 基础
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 基础要求-化学原理
syllabus_code: [5]
syllabus_module: [化学原理]
tags: [化竞, 酸碱]
related: [Brønsted酸碱理论, 酸碱平衡, 缓冲溶液, pKa]
prerequisite: [Brønsted酸碱理论]
problem_types: [题型-pH计算]
difficulty: 2
importance: 5
status: 已填充
stage: published
sources:
  - 提炼-普化原理-第8章-酸碱平衡
  - 教学逻辑提炼-周坤无机新课-酸碱理论与电化学-第一轮
  - 专题-酸碱理论
source_type:
  - 教材提炼
  - 教学逻辑提炼
  - 专题归纳
review_cycle: 30d
has_images: false
image_count: 0
images_priority: low
images_note: "当前以文字、公式或表格表达为主，暂未单独配置图像文件；后续备课如需增强直观性，再按需补图。"
teaching_ready: true
source_notes:
  - "[[提炼-普化原理-第8章-酸碱平衡]]"
  - "[[教学逻辑提炼-周坤无机新课-酸碱理论与电化学-第一轮]]"
  - "[[专题-酸碱理论]]"
  - "[[04-课件/新授课/2026-06-02-酸碱理论-基础班]]"
updated: 2026-06-18
source_extracts:
  - source_file: "[[提炼-普化原理-第8章-酸碱平衡]]"
    asset_id: "Ch8-8.2"
    asset_type: "教材提炼"
    asset_summary: "给出 pH、pOH 与 pKw 的定义，强调 pH+pOH=pKw 而非永远等于 14，并列出 Kw 随温度变化的数据表。"
    target_section: "§一-§六"
  - source_file: "[[教学逻辑提炼-周坤无机新课-酸碱理论与电化学-第一轮]]"
    asset_id: "B2-关联"
    asset_type: "关联引用"
    asset_summary: "本KP未在周坤Batch 2资产清单中直接映射可提取资产，但pH概念与Brønsted理论共轭酸碱对密切相关"
    target_section: "—"
  - source_file: "[[专题-酸碱理论]]"
    asset_id: "专题-pH"
    asset_type: "专题归纳"
    asset_summary: "归纳了强酸强碱、弱酸弱碱、缓冲体系、两性物质和极稀溶液的 pH 计算路径。"
    target_section: "§四-§十"
key_images: []
---

# pH

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 所属模块：[[基础要求-化学原理]]
- 对应考纲条目：[[05-酸碱理论]]

## 一、定义
$$\mathrm{pH} = -\lg[\mathrm{H}^+] \quad \mathrm{pOH} = -\lg[\mathrm{OH}^-]$$

25°C 水溶液中：$\mathrm{pH} + \mathrm{pOH} = 14.00$

## 二、考纲对应
- 对应考纲条目：[[05-酸碱理论]]
- 要求层级：能正确理解 pH 的定义、温度条件、近似公式适用范围，并能完成常见酸碱体系的定量计算
- 课堂定位：作为 [[Brønsted酸碱理论]]、[[酸碱平衡]] 与 [[缓冲溶液]] 的运算落点，也是后续 [[酸碱滴定]] 的数值基础

## 三、核心原理
- pH 每差 1 → [H⁺] 差 10 倍（对数标度）
- Kw 随温度变化 → pH + pOH = pKw（非 25°C 时 ≠ 14）
- 25°C Kw = 1.0×10⁻¹⁴, pKw = 14.00

## 四、关键结论
### 各类溶液的 pH 公式（快速参考）
| 溶液 | 公式 |
|------|------|
| 强酸 c mol/L | pH = −lg c |
| 强碱 c mol/L | pH = 14 + lg c |
| 弱酸 HA | $[\ce{H+}] = \sqrt{K_a c}$（近似） |
| 弱碱 B | $[\ce{OH-}] = \sqrt{K_b c}$（近似） |
| 缓冲溶液 | $\mathrm{pH} = \mathrm{p}K_a + \lg\frac{[\mathrm{A}^-]}{[\mathrm{HA}]}$ |
| 两性物质 | $\mathrm{pH} = \frac{1}{2}(\mathrm{p}K_{a1} + \mathrm{p}K_{a2})$ |

## 五、常见分类或情形

### 1. 各类溶液的 pH 计算分类
| 溶液类型 | $\ce{[H3O+]}$ / $\ce{[OH-]}$ 公式 | 适用条件 |
|----------|------|------|
| 强酸（$c\ \mathrm{mol\cdot dm^{-3}}$） | $\ce{[H3O+]} = c$ | 完全电离 |
| 强碱（$c\ \mathrm{mol\cdot dm^{-3}}$） | $\ce{[OH-]} = c$ | 完全电离 |
| 一元弱酸 HA | $\ce{[H3O+]} = \sqrt{K_a c}$ | $c/K_a \geqslant 400$ |
| 一元弱碱 B | $\ce{[OH-]} = \sqrt{K_b c}$ | $c/K_b \geqslant 400$ |
| 缓冲溶液 | $\mathrm{pH} = \mathrm{p}K_a + \lg\frac{c(\text{共轭碱})}{c(\text{弱酸})}$ | 见 [[缓冲溶液]] |
| 两性物质 | $\ce{[H3O+]} = \sqrt{K_{a_1} \cdot K_{a_2}}$ | 见 [[酸碱平衡]] |
| 多元弱酸 | $\ce{[H3O+]} \approx \sqrt{K_{a_1} c}$ | $K_{a_1} \gg K_{a_2}$ |

### 2. 水的离子积 $K_w$ 与温度（教材表 8.3）
| $t / ^\circ\mathrm{C}$ | 0 | 10 | 20 | 25 | 50 | 100 |
|------|------|------|------|------|------|------|
| $K_w$ | $1.15\times 10^{-15}$ | $2.92\times 10^{-15}$ | $6.87\times 10^{-15}$ | $1.01\times 10^{-14}$ | $5.31\times 10^{-14}$ | $5.45\times 10^{-13}$ |

**室温近似**：一般工作时取 $K_w = 1.0\times 10^{-14}$。水的电离是**吸热**反应，温度越高 $K_w$ 越大。注意中性溶液的 $\mathrm{pH}$ 也随温度变化（$100^\circ\mathrm{C}$ 时中性 $\mathrm{pH} \approx 6.13$）。

### 3. pH 使用范围
- $\mathrm{pH}$ 和 $\mathrm{pOH}$ 使用范围一般在 $0\sim 14$ 之间
- 在这个范围以外，直接用浓度（$\mathrm{mol\cdot dm^{-3}}$）表示酸度和碱度反而更方便
- 室温条件：$\mathrm{pH} < 7$ 酸性，$\mathrm{pH} > 7$ 碱性，$\mathrm{pH} = 7$ 中性

### 4. 酸碱溶液中 $\ce{[H3O+]}$ 和 $\ce{[OH-]}$ 共存
不论酸性还是碱性溶液，$\ce{H3O+}$ 和 $\ce{OH-}$ 离子**同时存在**，浓度的乘积为常数 $K_w$。任何一个离子浓度随另一个浓度增大可以减小，但**不会等于零**。

**教材示例**：往纯水中加酸使 $[\ce{H3O+}] = 0.10\ \mathrm{mol\cdot dm^{-3}}$，则 $[\ce{OH-}] = K_w/[\ce{H3O+}] = 1.0\times 10^{-13}\ \mathrm{mol\cdot dm^{-3}}$。

### 5. pH 与水电离的抑制
弱酸（碱）电离出的 $\ce{H3O+}$（或 $\ce{OH-}$）会**抑制**水的自耦电离。如 $0.10\ \mathrm{mol\cdot dm^{-3}}$ HAc 溶液中，由水电离出的 $[\ce{H3O+}]$ 远小于 $10^{-7}\ \mathrm{mol\cdot dm^{-3}}$，与 HAc 电离的 $1.3\times 10^{-3}\ \mathrm{mol\cdot dm^{-3}}$ 相比完全可以忽略。

## 六、适用条件与限制

- $\mathrm{pH} + \mathrm{pOH} = 14$ **仅适用于 $25^\circ\mathrm{C}$**。在其他温度下 $K_w$ 不同，需用 $\mathrm{pH} + \mathrm{pOH} = \mathrm{p}K_w$。
- $\mathrm{pH}$ 的定义基于**活度**（$a_{\ce{H+}}$）而非浓度。教材中实验测定的 $\mathrm{pH}$ 与浓度计算值略有差别（见表 8.5 实验数据），正是因为溶液中存在离子间的相互作用。竞赛计算中一般忽略活度-浓度差异。
- 对于极浓的强酸或强碱溶液，$\mathrm{pH}$ 概念不适直接用（超出 $0\sim 14$ 范围），应改用浓度表示。
- 在非水溶剂中，$\mathrm{pH}$ 的定义需重新考虑（质子自递常数不同）。
- 简化公式 $[\ce{H3O+}] = \sqrt{K_a c}$ 仅在 $c/K_a \geqslant 400$（$\alpha \leqslant 5\%$）时有效，否则须精确求解二次方程。

## 七、常见比较与易混点

### 1. pH 与 pKa 的关系
- $\mathrm{pH}$ 描述**溶液**的酸度（$[\ce{H3O+}]$ 的对数）
- $\mathrm{p}K_a$ 描述**酸**的强度（$K_a$ 的对数）
- 二者通过 H-H 方程关联：$\mathrm{pH} = \mathrm{p}K_a + \lg([\ce{A-}]/[\ce{HA}])$
- 当 $[\ce{A-}] = [\ce{HA}]$ 时，$\mathrm{pH} = \mathrm{p}K_a$

### 2. pH 改变量与浓度改变量
$\mathrm{pH}$ 改变 $1$ 个单位 $\Longleftrightarrow$ $[\ce{H3O+}]$ 改变 $10$ 倍。这是经常被忽略的关键换算——小数的 $\mathrm{pH}$ 变化对应着较大的浓度变化。

### 3. 酸性溶液 vs 中性溶液的温度效应
- $25^\circ\mathrm{C}$：中性 $\mathrm{pH} = 7.00$
- $100^\circ\mathrm{C}$：中性 $\mathrm{pH} = -\lg\sqrt{5.45\times 10^{-13}} \approx 6.13$
- 判断酸碱性应以 $\mathrm{pH}$ 与当时温度下的中性 $\mathrm{pH}$ 比较，而非恒以 $7$ 为界

### 4. 计算 pH 时的常见误区
- 强酸极稀时（$c \lesssim 10^{-6}\ \mathrm{mol\cdot dm^{-3}}$），水的自耦电离不可忽略
- 多元弱酸的 $\mathrm{pH}$ 只由 $K_{a_1}$ 决定（前提是 $K_{a_1} \gg K_{a_2}$），初学者常误以为各步电离叠加
- 两性物质（如 $\ce{NaHCO3}$）的 $\mathrm{pH}$ 与浓度无关（近似条件下），初学者容易错误地用弱碱或弱酸公式计算

## 八、与其他知识点的联系
- 前置知识：[[Brønsted酸碱理论]]
- 相关知识：[[离去基与pKa]]、[[Kw]]、[[平衡常数]]
- 应用知识：[[酸碱平衡]]、[[缓冲溶液]]、[[酸碱滴定]]

## 九、典型题型
- 题型-pH计算
- 题型-弱酸弱碱近似条件判断
- 题型-缓冲体系 pH 估算
- 题型-极稀溶液与高温中性判断

## 十、例题
**例 1**：计算 $25^\circ\mathrm{C}$ 下 $0.0200\ \mathrm{mol\cdot dm^{-3}}$ 醋酸溶液的 pH。已知 $K_a(\mathrm{HAc})=1.75\times10^{-5}$。  
**思路**：先检验 $c/K_a\approx 1.14\times10^3>400$，可用弱酸近似：  
$$[\mathrm{H}^+]\approx\sqrt{K_a c}=\sqrt{1.75\times10^{-5}\times0.0200}=5.92\times10^{-4}$$
故 $\mathrm{pH}=3.23$。

**例 2**：$100^\circ\mathrm{C}$ 纯水的 pH 是否等于 7？  
**思路**：查表得 $K_w=5.45\times10^{-13}$，中性条件下 $[\mathrm{H}^+]=[\mathrm{OH}^-]=\sqrt{K_w}$，  
$$\mathrm{pH}=-\lg\sqrt{5.45\times10^{-13}}\approx 6.13$$
所以高温中性水不一定 pH=7。

## 十一、易错点
- 忘记 $25^\circ\mathrm{C}$ 时 $K_w = 1.0\times 10^{-14}$，$\mathrm{pH} + \mathrm{pOH} = 14$
- 极稀强酸（碱）忽略水的电离
- 用简化公式时不先判断 $c/K_a$ 是否满足条件
- 多元酸错误叠加各步电离来算 $[\ce{H+}]$

## 十二、🎯 教学视角

### 12.1 学生典型认知误区

| 误区 | 学生为什么会这么想 | 正确认识 | 口诀 |
|:---|:---|:---|:---|
| "pH=7 就是中性" | 初中化学入门记忆 | pH=7 是中性仅适用于 **25°C**！$K_w$ 随温度变——100°C 时 $K_w=5.5×10^{-13}$，中性 pH≈6.1 | "中性看温度，7不是万能" |
| "pH 可以小于 0 或大于 14" | 觉得 0-14 是硬性范围 | 浓 HCl（10 mol/L）pH = −1！pH 只在稀溶液（<1 mol/L）中方便使用，浓溶液直接用浓度 | "稀溶液看pH，浓溶液看浓度" |
| "pH 和 pOH 的关系总是 pH+pOH=14" | 把 25°C 下的 $K_w$ 当成永恒常数 | $\mathrm{p}K_w = \mathrm{pH} + \mathrm{pOH}$，但 $\mathrm{p}K_w$ 只在 25°C 时 = 14 | "pKw看温度，25度才14" |
| "[H⁺] 和 pH 可以直接用计算器换算" | 计算器思维 | pH 的有效数字规则特殊：小数点后位数 = $[\mathrm{H}^+]$ 的有效位数。pH=4.62 是 2 位有效 | "pH只看小数后，整数不算有效位" |

### 12.2 入门级例题

**题目**：
(1) 计算 $0.010\ \mathrm{mol\cdot L^{-1}}$ HCl 溶液的 pH（完全电离）。
(2) 计算 $0.010\ \mathrm{mol\cdot L^{-1}}$ NaOH 溶液的 pH（25°C，$K_w = 1.0 \times 10^{-14}$）。

**预期解答路径**：
1. HCl → $[\mathrm{H}^+] = 0.010$ → pH = $-\lg(0.010) = 2.00$（2 位有效 → 小数点后 2 位）
2. NaOH → $[\mathrm{OH}^-] = 0.010$ → pOH = 2.00 → pH = 14.00 − 2.00 = 12.00

**教师引导提问**：如果是 $1.0 \times 10^{-8}\ \mathrm{mol\cdot L^{-1}}$ HCl（极稀），pH 是多少？（学生容易答 8.00——但酸不可能变碱！极稀时必须考虑水的自耦电离 → 真实 pH≈6.98。这引出了"浓度极限"的概念）

### 12.3 与现实/直觉的连接

- **柠檬汁 (pH~2) vs 肥皂 (pH~9-10)**：pH 每差 1 意味着 $[\mathrm{H}^+]$ 差 10 倍——柠檬汁的酸性是可乐（pH≈3）的 10 倍，是纯水的 100,000 倍！
- **胃酸 (pH~1.5-3.5)**：胃壁细胞分泌的 HCl 使胃内保持强酸性——既能杀菌又能激活胃蛋白酶。胃酸返流到食道（pH~7）造成的灼烧感就是 pH 梯度在身体内的直观体验。
- **酸雨的 pH 阈值**：正常雨水因溶解 CO₂ 而呈微酸性（pH≈5.6），pH<5.6 才是酸雨。背后是 $\mathrm{CO_2 + H_2O \rightleftharpoons H_2CO_3 \rightleftharpoons H^+ + HCO_3^-}$ 的平衡计算。

## 十三、竞赛拓展
- 严格定义中 $\mathrm{pH}=-\lg a_{\mathrm{H}^+}$，活度系数在较高离子强度下不可忽略
- 多元酸体系可借助分布分数与主导平衡判断 pH，而不是机械联立全部电离方程
- 极稀强酸强碱可通过电荷守恒联立 $K_w$ 精确求解，作为“近似失效”的典型案例

## 十四、外部资料出处
- 主要来源：[[提炼-普化原理-第8章-酸碱平衡]]（《普通化学原理 第4版》第 8 章 8.2 节：水的自耦电离平衡）
- 《分析化学》——活度与 pH 的严格定义

## 十五、待完善项
- [ ] 补充极稀溶液 pH 计算的例题
- [ ] 补充高温下中性 pH 的计算示例

---

## 相关真题

```dataview
TABLE file.name AS "文件名", year AS "年份", type AS "题型", difficulty AS "难度"
FROM "04-题库"
WHERE contains(knowledge_points, "pH")
SORT year DESC, difficulty ASC
```
