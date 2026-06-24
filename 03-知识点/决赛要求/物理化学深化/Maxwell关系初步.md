---
title: Maxwell关系初步
aliases: [Maxwell Relations, Maxwell关系式, 热力学基本方程]
type: 知识点
template_version: v1.3
subject: 决赛要求
module: 决赛要求
submodule: 物理化学深化
syllabus_stage: 决赛
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module: 决赛要求-物理化学深化
syllabus_code: [决赛04]
syllabus_module: [物理化学深化]
tags: [化竞, 决赛, 物理化学, 热力学, Maxwell关系]
related: [化学热力学, 热力学第一定律深化, 热力学第二定律深化, 化学势与平衡]
prerequisite: [全微分, 偏导数, 热力学基本方程]
problem_types: [题型-推导证明, 题型-偏导数转换]
difficulty: 5
importance: 5
status: 已填充
stage: published
sources: []
source_type: []
source_notes: []
review_cycle: 30d
has_images: false
image_count: 0
images_priority: low
images_note: "当前以文字、公式或表格表达为主，暂未单独配置图像文件；后续备课如需增强直观性，再按需补图。"
teaching_ready: false
key_images: []
updated: 2026-06-14
---

# Maxwell关系初步

- 总览：[[决赛要求-总览]]
- 所属模块：[[决赛要求-物理化学深化]]
- 对应考纲条目：[[决赛04-热力学]]
- 综合笔记：[[化学热力学]]（§3.4–3.5）
- 关联提炼笔记：[[提炼-Atkins物理化学-主题2-3-热力学定律]]

## 一、定义



Maxwell关系是由热力学势函数的全微分性质导出的四组偏导数等式。它们将难以直接测量的热力学量（如熵随体积/压力的变化）转换为容易由实验测量的量（如热膨胀系数、等温压缩系数）。

## 二、考纲对应

- 对应 `[[决赛04-热力学]]` 中关于热力学势全微分、偏导变换与 Maxwell 关系应用的要求
- 决赛层面重点不是机械背四个式子，而是能根据**势函数 + 自然变量 + 二阶混合偏导相等**现场推出来

## 三、核心原理


### 2.1 热力学势与基本方程

| 热力学势 | 定义 | 自然变量 | 基本方程 |
|---------|------|---------|---------|
| 内能 $ | — | , V$ | $\mathrm{d}U = T\mathrm{d}S - p\mathrm{d}V$ |
| 焓 $ |  + pV$ | , p$ | $\mathrm{d}H = T\mathrm{d}S + V\mathrm{d}p$ |
| Helmholtz自由能 $ |  - TS$ | , V$ | $\mathrm{d}A = -S\mathrm{d}T - p\mathrm{d}V$ |
| Gibbs自由能 $ |  - TS = A + pV$ | , p$ | $\mathrm{d}G = -S\mathrm{d}T + V\mathrm{d}p$ |

### 2.2 Maxwell关系的推导

若  = f(x,y)$ 的全微分为 $\mathrm{d}z = M\mathrm{d}x + N\mathrm{d}y$，则必有：

\left(\frac{\partial M}{\partial y}\right)_x = \left(\frac{\partial N}{\partial x}\right)_y

将此应用于四个热力学势：

**第一组（来自 $）**：
\left(\frac{\partial T}{\partial V}\right)_S = -\left(\frac{\partial p}{\partial S}\right)_V

**第二组（来自 $）**：
\left(\frac{\partial T}{\partial p}\right)_S = \left(\frac{\partial V}{\partial S}\right)_p

**第三组（来自 $）**：
\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial p}{\partial T}\right)_V

**第四组（来自 $）**：
\left(\frac{\partial S}{\partial p}\right)_T = -\left(\frac{\partial V}{\partial T}\right)_p

### 2.3 记忆技巧

以 (T,p)$ 为例：
- $-S$ 对 $ 求偏导 = $ 对 $ 求偏导，注意负号
- 口诀：**"同侧同号，异侧异号"** — 看变量在基本方程中的位置

更系统的记忆：将 ,S$ 和 ,V$ 看作对角，利用Jacobian或循环关系推导。

### 2.4 竞赛中的典型应用

**应用1：证明 $\left(\frac{\partial U}{\partial V}\right)_T = T\left(\frac{\partial p}{\partial T}\right)_V - p$**

由 $\mathrm{d}U = T\mathrm{d}S - p\mathrm{d}V$，在等温下对 $ 求偏导：
\left(\frac{\partial U}{\partial V}\right)_T = T\left(\frac{\partial S}{\partial V}\right)_T - p = T\left(\frac{\partial p}{\partial T}\right)_V - p

对于理想气体， = nRT/V$，代入得 $\left(\frac{\partial U}{\partial V}\right)_T = 0$。

**应用2：熵随压力的变化**

\left(\frac{\partial S}{\partial p}\right)_T = -\left(\frac{\partial V}{\partial T}\right)_p = -\alpha V

其中 $\alpha$ 为体膨胀系数。由此可得：
\Delta S = -\int_{p_1}^{p_2} \alpha V \, \mathrm{d}p

对于凝聚相（$\alpha, V$ 近似常数）：$\Delta S \approx -\alpha V(p_2 - p_1)$

对于理想气体：$\Delta S = -nR\ln\frac{p_2}{p_1}$

**应用3： - C_V$ 的严格证明**

C_p - C_V = T\left(\frac{\partial p}{\partial T}\right)_V\left(\frac{\partial V}{\partial T}\right)_p = \frac{\alpha^2TV}{\kappa_T}

### 2.5 其他重要热力学关系

利用Maxwell关系还可导出：

\left(\frac{\partial H}{\partial p}\right)_T = V - T\left(\frac{\partial V}{\partial T}\right)_p = V(1 - \alpha T)

**Joule-Thomson系数**（另见[[热力学第一定律深化]]）：
\mu_{\mathrm{JT}} = \left(\frac{\partial T}{\partial p}\right)_H = \frac{1}{C_p}\left[T\left(\frac{\partial V}{\partial T}\right)_p - V\right]

## 四、关键结论

1. Maxwell 关系本质上来自热力学势是状态函数，因此混合二阶偏导相等
2. 它们最大的价值是把不易直接测量的熵偏导、内能偏导转换成压强、体积、温度等实验量
3. 真正解题核心不是死背公式，而是先认清用了哪个势、自然变量是什么
4. 一旦能熟练用 Maxwell 关系，很多热力学恒等式都能“拆公式”得到

## 五、常见分类或情形

- **直接推导情形**：由某个热力学势全微分直接写出对应 Maxwell 关系
- **偏导转换情形**：把熵或内能对某变量的偏导转成可测量量
- **证明恒等式情形**：如证明 $C_p-C_V$、Joule-Thomson 系数或某热力学偏导表达式
- **结合状态方程情形**：先用 Maxwell 关系转写，再代入理想气体或给定状态方程求值

## 六、适用条件与限制

- 前提是所用热力学势对相应变量可微且体系处于平衡态
- 使用时必须严格区分自然变量；若势函数选错，后续偏导关系全部会偏
- Maxwell 关系本身不提供具体数值，通常还需状态方程、热容公式或实验系数配合
- 多组分体系和化学反应体系中可进一步推广，但竞赛常见版本多为单组分简单压缩体系

## 七、常见比较与易混点

- **Maxwell 关系 vs 循环关系**：前者来自势函数二阶混合偏导，后者是一般偏导代数技巧
- **自然变量 vs 保持不变的下标**：两者紧密相关，但不能只看下标不看势函数来源
- **熵偏导 vs 热容公式**：热容描述沿特定路径的能量变化，Maxwell 关系则更偏变量变换工具
- **会背四个式子 vs 真会用**：真正解题时常常要从势函数现场恢复，而不是只从记忆中硬套

## 八、与其他知识点的联系

- 与[[化学热力学]]、[[热力学第一定律深化]]、[[热力学第二定律深化]]构成热力学推导主干
- 与[[化学势与平衡]]相连，可继续推广到多组分体系和 Gibbs 自由能偏导
- 与膨胀系数 $\alpha$、等温压缩系数 $\kappa_T$ 和热容差公式直接相连
- 与[[Boltzmann统计初步]]不同：后者从微观统计起步，这页属于纯宏观热力学工具

## 九、典型题型


1. **利用Maxwell关系证明热力学恒等式**
2. **将难测量量转换为可测量量**：如 $\left(\frac{\partial S}{\partial p}\right)_T \to \alpha$
3. **结合状态方程计算具体偏导数**

## 十、例题

**例**：证明对简单可压缩体系有
$$
\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial p}{\partial T}\right)_V
$$

**分析路径**：
1. 选择自然变量为 $(T,V)$ 的 Helmholtz 自由能 $A$
2. 写出 $\mathrm{d}A = -S\mathrm{d}T - p\mathrm{d}V$
3. 利用二阶混合偏导相等进行转换

**结论**：由 $\left(\frac{\partial A}{\partial T}\right)_V = -S$ 与 $\left(\frac{\partial A}{\partial V}\right)_T = -p$ 可直接推出上式。

**反思**：Maxwell 题最稳的套路就是“**先选势，再写全微分，再比混合偏导**”

## 十一、易错点


1. **符号错误**：第三、四组Maxwell关系有负号，极易遗漏
2. **混淆下标**：注意恒定的变量（下标）是什么
3. **自然变量混淆**：必须从正确的热力学势出发推导

## 十二、🎯 教学视角

- 这页最容易让学生觉得“纯公式”，教学上要把它讲成一个**变量翻译器**
- 课堂顺序建议固定：势函数表 → 自然变量 → 一条示范推导 → 两三个典型应用
- 学生最大的痛点通常不是数学，而是不知道该选 $U/H/A/G$ 中哪一个势
- 若只背结论不练推导，稍一换式子就会崩；因此最好至少现场推一遍来自 $A$ 和 $G$ 的两条关系

## 十三、竞赛拓展

- Jacobian 方法、循环关系和 Legendre 变换可以把 Maxwell 关系组织成更统一的偏导代数框架
- 多组分体系中可继续引入化学势，得到更一般的偏导恒等式
- Joule-Thomson 系数、Clapeyron 方程和热容差公式都可看成 Maxwell 思想的延伸应用
- 更高阶可继续连到统计热力学中自由能的微观表达式

## 十四、外部资料出处

- 可结合 Atkins 关于 thermodynamic potentials、Maxwell relations 与 measurable response functions 的章节阅读
- 与本库条目的直接关联：[[化学热力学]]、[[热力学第一定律深化]]、[[化学势与平衡]]

## 十五、待完善项

- [ ] 后续补一张“U/H/A/G 四势与 Maxwell 关系”总表

## 五、修订记录

| 日期 | 版本 | 修订内容 | 修订人 |
|-----|------|---------|-------|
| 2026-05-16 | v1.0 | 基于Atkins主题3创建，含推导、记忆技巧、竞赛应用 | AI助手 |
