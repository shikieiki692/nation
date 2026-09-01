---
title: Appel反应
aliases:
  - Appel卤化
  - Appel Reaction
  - 三苯基膦四氯化碳卤化
type: 知识点
subject: 有机化学
module: 官能团转化
submodule: 醇的卤代
syllabus_stage: 提高
parent_overview: 中国化学奥林匹克基本要求-总览
parent_module:
syllabus_code: []
syllabus_module: []
tags: [化竞, 有机化学, 人名反应, 醇活化, SN2, 膦化学]
related: [SN2反应, 亲核取代, Mitsunobu反应, 离去基与pKa, Walden翻转, 膦化合物]
prerequisite: [醇, SN2反应, 亲核体与亲电体]
problem_types: []
difficulty: 3
importance: 3
status: 已填充
sources: ["Clayden 有机化学", "ABOC 第4章"]
source_type: [教材]
review_cycle: 30d
has_images: false
image_count: 0
images_priority: low
images_note: ""
key_images: []
template_version: v1.3
updated: 2026-09-01
teaching_ready: false
---

# Appel反应

- 总览：[[中国化学奥林匹克基本要求-总览]]
- 上位框架：[[亲核取代]] · [[SN2反应]]
- 同位比较：[[Mitsunobu反应]] · [[Swern氧化]]

## 一、定义

**Appel反应** 是三苯基膦（$\mathrm{PPh_3}$）与四卤化碳（常用 $\mathrm{CCl_4}$，制溴用 $\mathrm{CBr_4}$）协同作用，把**醇转化为卤代烷**的方法：

$$\mathrm{R{-}OH \xrightarrow[\text{或 } CBr_4]{PPh_3,\ CCl_4} R{-}Cl\ (或\ R{-}Br)}$$

它的化学意义是：**把很难离去的 $\mathrm{OH^-}$ 就地转变为一个极好的离去基团（膦氧鎓），再由卤离子做分子内 SN2 顶掉**。反应条件中性、温和，不发生碳正离子重排。

## 二、试剂体系与变体

| 目标产物 | 卤源 | 备注 |
|:---|:---|:---|
| $\mathrm{R{-}Cl}$ | $\mathrm{CCl_4}$ | 最经典；$\mathrm{CCl_4}$ 兼作溶剂 |
| $\mathrm{R{-}Br}$ | $\mathrm{CBr_4}$、$\mathrm{CHBr_3}$、$\mathrm{Br_2}$ | $\mathrm{CBr_4}$ 最常用 |
| $\mathrm{R{-}I}$ | $\mathrm{CH_3I}$、$\mathrm{I_2}$/咪唑 | 碘代需更强活化条件 |

$\mathrm{CCl_4}$ 因毒性与环境限制，实验室常用 **六氯丙酮** 或 $\mathrm{CBr_4}$/$\mathrm{PPh_3}$ 组合替代。

## 三、反应机理（四步）

**总驱动力**：生成 $\mathrm{P{=}O}$ 键（键能约 540 kJ·mol⁻¹），热力学上极为有利，把整条链不可逆地拉向右方。

### 第 1 步：生成鏻盐（活化试剂）

$$\mathrm{PPh_3 + CCl_4 \longrightarrow [Ph_3P{-}CCl_3]^+\,Cl^-}$$

$\mathrm{PPh_3}$ 作为**亲核体**进攻 $\mathrm{CCl_4}$，生成三氯甲基鏻盐。此时 $\mathrm{P}$ 带正电，成为后续醇的进攻目标。

> 注意这一步的"角色反转"：$\mathrm{CCl_4}$ 通常是惰性溶剂，这里却是**卤源兼活化剂**，被膦活化后才具有反应性。

### 第 2 步：醇进攻膦，形成烷氧基鏻

醇氧的孤对电子进攻缺电子的 $\mathrm{P}$，同时 $\mathrm{CCl_3^-}$ 作为碱夺走醇的质子：

$$\mathrm{R{-}OH + [Ph_3P{-}CCl_3]^+\,Cl^- \longrightarrow [Ph_3P{-}OR]^+\,Cl^- + CHCl_3}$$

副产物 **$\mathrm{CHCl_3}$** 由此产生。此时 $\mathrm{OH}$ 已变成 $\mathrm{\overset{+}{P}Ph_3{-}OR}$ —— 一个**极好的离去基团**（离去后生成稳定的 $\mathrm{Ph_3P{=}O}$）。

### 第 3 步：卤离子的 SN2 进攻（决速步）

$$\mathrm{Cl^- + [Ph_3P{-}OR]^+ \longrightarrow R{-}Cl + Ph_3P{=}O}$$

$\mathrm{Cl^-}$ 从**背面**进攻与氧相连的碳，一步完成断 $\mathrm{C{-}O}$、成 $\mathrm{C{-}Cl}$。

### 第 4 步：驱动力兑现

$\mathrm{Ph_3P{=}O}$ 的 $\mathrm{P{=}O}$ 键极强，是整个反应的热力学"支付方"。正因如此，膦氧键形成后反应不可逆，也不能再回头。

### 为什么 $\mathrm{OH^-}$ 本来不能离去

$\mathrm{OH^-}$ 的共轭酸 $\mathrm{H_2O}$ 的 $\mathrm{p}K_\mathrm{a} \approx 15.7$，是很差的离去基团（见 [[离去基与pKa]]）。Appel 的巧妙之处在于**不把它换成卤素再取代，而是先把氧"挂"到一个愿意带着电子对离开的基团上**（膦），$\mathrm{Ph_3P{=}O}$ 中性且稳定，于是 $\mathrm{C{-}O}$ 键得以断裂。

## 四、立体化学

第 3 步是 **SN2**，因此：

- **手性中心的醇 → 构型完全翻转**（[[Walden翻转]]）
- **不发生重排**：无碳正离子中间体，这与 $\mathrm{SOCl_2}$ 无碱条件（SNi 途径）或 $\mathrm{HX}$ 取代（可能经 $\mathrm{S_N1}$）形成对比

**实例**：$(S)$-2-辛醇 $\xrightarrow{\mathrm{PPh_3/CCl_4}}$ $(R)$-2-氯辛烷

这一点与 [[Mitsunobu反应]] 完全一致——两者都借助 $\mathrm{PPh_3}$，都经 SN2，都得翻转。差别在于**亲核体是谁**：Appel 是卤离子，Mitsunobu 是外加的羧酸/酚/酰亚胺等。

## 五、适用范围与限制

| 底物 | 结果 |
|:---|:---|
| 一级醇 | ✅ 最佳 |
| 二级醇 | ✅ 良好（翻转） |
| 三级醇 | ❌ 易消除成烯（SN2 通道被位阻堵死） |
| 烯丙醇 / 苄醇 | ✅ 良好 |
| 含酸敏感基团（缩醛、Boc 等）的底物 | ✅ 优势明显——条件中性 |
| 羧酸 | 可经同体系生成**酰氯**（Appel 型活化） |

**两大实用缺点**：

1. **原子经济性差**：副产 $\mathrm{CHCl_3}$ 与等物质的量 $\mathrm{Ph_3P{=}O}$
2. **纯化麻烦**：$\mathrm{Ph_3P{=}O}$ 极性大、量大，常需柱层析；工业上不经济

## 六、与其他醇活化方法的对比

| | **Appel** | **Mitsunobu** | **SOCl₂** | **PBr₃** |
|:---|:---|:---|:---|:---|
| 试剂 | $\mathrm{PPh_3}$ + $\mathrm{CCl_4}$/$\mathrm{CBr_4}$ | $\mathrm{PPh_3}$ + DEAD/DIAD + 亲核体 | $\mathrm{SOCl_2}$（±吡啶） | $\mathrm{PBr_3}$ |
| 产物 | 卤代烷 | 酯/醚/胺等（多样） | 氯代烷 | 溴代烷 |
| 条件 | **中性** | **中性** | 酸性（通常加碱） | 中性偏酸 |
| 立体化学 | **翻转** | **翻转** | 取决于是否加碱¹ | **翻转** |
| 是否重排 | 否 | 否 | 否 | 否 |
| 主要副产 | $\mathrm{Ph_3P{=}O}$ + $\mathrm{CHCl_3}$ | $\mathrm{Ph_3P{=}O}$ + 肼二甲酸酯 | $\mathrm{SO_2\uparrow}$ + $\mathrm{HCl\uparrow}$ | $\mathrm{H_3PO_3}$ |

> ¹ $\mathrm{SOCl_2}$ 的立体化学：**不加碱**时经 $\mathrm{S_Ni}$（内返）途径得**构型保持**；**加吡啶**时释放自由 $\mathrm{Cl^-}$ 走 SN2，得**构型翻转**。（[[Mitsunobu反应]] 页的对照表对此作了简化，以本表为准。）

**选型建议**：
- 只要卤代、分子其它部分怕酸 → **Appel**
- 需要引入非卤亲核体（成酯/成醚/成胺）→ **Mitsunobu**
- 简单底物、追求后处理方便（气体副产）→ $\mathrm{SOCl_2}$（翻转需加吡啶）
- 制溴代 → $\mathrm{PBr_3}$ 更省事

## 七、竞赛考点

Appel 的考法通常不要求背试剂名，而是考**机理迁移**：给一个"$\mathrm{PPh_3}$ + 多卤代物 + 底物"的组合，要求判断

1. 哪一端的键被活化（膦先进攻谁）
2. 谁是最终亲核体（卤离子 vs 外加的其它负离子）
3. 立体化学结果（翻转）

> 相关题：[[题-032-9-C-F键断裂原因]]（第 32 届初赛，以 Appel 型活化类比讨论 C–F 键断裂的机理）

## 八、常见误区

| 误区 | 纠正 |
|:---|:---|
| 认为 $\mathrm{PPh_3}$ 是还原剂 | 此处 $\mathrm{PPh_3}$ 是**亲核体/氧接受体**，被氧化为 $\mathrm{Ph_3P{=}O}$ |
| 认为 $\mathrm{CCl_4}$ 只是溶剂 | 它是**卤源兼活化剂**，先与膦成鏻盐 |
| 认为反应经过碳正离子 | 关键步是 **SN2**，无碳正离子，故不重排 |
| 认为三级醇也能做 | 位阻堵死 SN2，主要得消除产物 |
| 忽略 $\mathrm{CHCl_3}$ 副产 | 第 2 步 $\mathrm{CCl_3^-}$ 夺醇质子生成 $\mathrm{CHCl_3}$，写方程式要配上 |
| 认为与 Mitsunobu 机理无关 | 两者共用"$\mathrm{PPh_3}$ 活化 + SN2 翻转"骨架，只换亲核体 |
