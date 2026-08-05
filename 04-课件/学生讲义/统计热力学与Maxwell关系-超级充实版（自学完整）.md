---
title: 学生讲义-统计热力学与Maxwell关系（超级充实版·自学完整）
type: 学生讲义
source_book: "自编（备课大纲+KP+真题综合）; Atkins《物理化学》第11版; 傅献彩《物理化学》"
chapter: 第四轮·4-7（物化线）
serve_rounds: [第四轮]
serve_topics: [热力学四大基本方程, Legendre变换, Maxwell关系, Gibbs-Helmholtz方程, Boltzmann分布, 配分函数, 统计熵, Sackur-Tetrode方程, 残余熵]
difficulty_level: 决赛
related_notes:
  - "[[03-知识点/决赛要求/物理化学深化/麦克斯韦关系式]]"
  - "[[03-知识点/决赛要求/物理化学深化/Boltzmann统计初步]]"
  - "[[03-知识点/决赛要求/物理化学深化/热力学四大基本方程]]"
  - "[[03-知识点/决赛要求/物理化学深化/吉布斯-亥姆霍兹方程]]"
  - "[[04-课件/学生讲义/物化综合计算-超级充实版（自学完整）]]"
  - "[[04-课件/学生讲义/热力学初步-超级充实版（自学完整）]]"
  - "[[04-专题与题型/专题/专题-热力学初步]]"
tags: [学生讲义, 超级充实版, 物理化学, 第四轮, 统计热力学, Maxwell关系, 自学完整]
created: 2026-08-04
has_images: true
image_count: 3
updated: 2026-08-04
last_audit: "2026-08-04 新建（S2）：承接决赛04 热力学深半（Maxwell 初步 + 统计热力学配分函数），补物化综合计算 §〇 未覆盖部分；全篇 $E^\\theta$ 规范；图片以 📌 占位标记（待补 3 处）"
template_version: 自学完整版 v3.0
stage: published
sources:
  - "[[07-资料提炼/书籍提炼/提炼-Atkins物理化学-主题2-3-热力学定律]]"
  - "[[07-资料提炼/书籍提炼/提炼-Atkins物理化学-主题13-14-统计热力学与分子相互作用]]"
problems: []
exercise_count: 15
exercise_levels: "基础5 + 进阶5 + 挑战5"
---

# 第四轮·4-7 统计热力学与 Maxwell 关系（冲刺班 · 自学完整）

> 课型：冲刺专题（1-2 × 90 min）　|　轮次：第四轮　|　定位：决赛04 热力学深半（4-7 物化线第三讲义）
> **承接考纲**：[[决赛04-热力学]]——物化综合计算 §〇 已覆盖化学势/van't Hoff/Clausius-Clapeyron 中段，本讲补**Maxwell 关系初步 + 统计热力学（配分函数）**深半。
> **前置知识**：第一轮热力学初步（ΔH/ΔS/ΔG、ΔG=ΔH−TΔS）；物化综合计算 §〇（化学势）
> **对应专题页**：[[04-专题与题型/专题/专题-热力学初步]]（深化链上一站）

> ⚠️ **R4 定位**：本讲是**决赛理论补完**，不是计算压轴。决赛要求的是"知道四大方程、会用 Maxwell 关系做偏导数变换、理解配分函数是所有热力学量的母函数"。**不展开**：正则系综严格推导（Atkins 13D）、配分函数算平衡常数的完整处理（13F）、统计热力学的量子统计细节。

---

<!-- ============ 教师向规划区（学生不可见，Word/PDF 导出自动忽略） ============
**主线导航（教师向规划）**

| 站 | 主题 | 核心武器 | 锚点 |
|:--:|:---|:---|:---|
| ① | 四大基本方程 + Legendre | dU=TdS−pdV 家族 | 决赛04 |
| ② | Maxwell 关系 | 四条 + 记忆口诀 | 决赛04 |
| ③ | Gibbs-Helmholtz | (∂(G/T)/∂T)_p=−H/T² | 决赛04 |
| ④ | Boltzmann 分布与配分函数 | q = Σg·e^{−βε} | 决赛04 |
| ⑤ | 由配分函数求热力学量 | U = NkT²(∂lnq/∂T)_V | 决赛04 |
| ⑥ | 统计熵应用 | Sackur-Tetrode / 残余熵 | 决赛04 |

============================================================================= -->

---

## 🎯 学习目标（可测量）

| # | 目标 | 达成判据 |
|:--:|:---|:---|
| 1 | 从 dU=TdS−pdV 经 Legendre 变换得到四大基本方程 | 能写出 U/H/A/G 的全微分 |
| 2 | 记住四条 Maxwell 关系并会用记忆口诀 | 能由任一基本方程推出对应 Maxwell 式 |
| 3 | 用 Maxwell 关系推导热容差 C_p−C_V 公式 | ≥ 85% 正确 |
| 4 | 理解配分函数 q 的定义与分解 | 能写 q=q_T·q_R·q_V·q_E |
| 5 | 由 q 求内能 U 和熵 S | 定域/离域熵差 Nk·ln(e/N) 脱口而出 |

---

## ⚡ 认知冲突（本讲最值得停下来想的地方）

> [!abstract] 冲突一：Maxwell 关系不是"新知识"，是"同一批偏导数的不同写法"
> 学生觉得四条 Maxwell 关系是要背的四个新公式。**错**——它们是从四大基本方程（全是 dU=TdS−pdV 的变形）用"二阶混合偏导数相等"推出来的。背会四大基本方程 → 四条 Maxwell 自动出来。突破：**先背 1 条（dU=TdS−pdV），其余靠推导**。

> [!abstract] 冲突二：配分函数是"统计热力学的宝典"
> 学生问"配分函数到底有什么用"。**它是一台母机**：内能、熵、Helmholtz 自由能、压强、平衡常数全部能从 q 求出来。竞赛只需记住"U 和 S 怎么从 q 求"两条主线。突破：把 q 看成"一张牌"，U、S、A 都是从它翻出来的"牌面"。

> [!abstract] 冲突三：S=k·lnΩ 与热力学熵是"同一件事"
> 学生把统计熵和热力学熵当两个概念。**它们是同一个熵**：统计熵是"微观起源"，热力学熵是"宏观测量"。Clausius 的 dS=δq_rev/T 与 Boltzmann 的 S=k·lnΩ 描述同一个量。突破：残余熵就是两者连接的证据（0 K 下热力学熵趋 0 而统计熵不为 0）。

> [!abstract] 冲突四：定域子与离域子的熵差"Nk·ln(e/N)"
> 同温同压下 1 mol 固体（定域）与 1 mol 理想气体（离域）的熵公式差一项 Nk·ln(e/N)。学生常忘。突破：离域粒子"不可区分"（全同粒子），除以 N! 使熵减小这一项——是 Gibbs 悖论（混合熵消失）的解法。

---

<!-- ============ 教师向规划区（学生不可见，Word/PDF 导出自动忽略） ============
**深度分层（教师向边界）**

| 层级 | 内容 | 说明 |
|:---:|:---|:---|
| 📝 **决赛必会** | 四大基本方程；四条 Maxwell 关系及记忆口诀；C_p−C_V=α²TV/κ_T；Gibbs-Helmholtz 微分/积分式；Boltzmann 分布；配分函数定义与分解；U、S 由 q 求；定域/离域熵差 | 决赛04 核心，动手必练 |
| 🌟 **了解会用** | Sackur-Tetrode 方程；残余熵计算；Legendre 变换思想；各模式配分函数（q^T/q^R/q^V/q^E） | 会用即可，不深究推导 |
| 🔒 **后置延伸** | 正则系综（13D）；配分函数算平衡常数（13F）；量子统计（Bose-Einstein/Fermi-Dirac）；统计热力学在光谱/吸附中的应用 | 超出决赛，大学物化再学 |

============================================================================= -->

---

## 一、热力学四大基本方程与 Legendre 变换

### 1.1 从 dU=TdS−pdV 出发

热力学第一定律（可逆）+ 第二定律合并：**dU = TdS − pdV**——这是热力学的"母方程"。

- U 的自然变量是 (S, V)：U = U(S, V)。
- 但实际过程常在恒 T 或恒 p 下进行，直接以 S、V 为变量不方便 → 用 **Legendre 变换**换自变量。

### 1.2 Legendre 变换表

> 💡 每次变换**换掉一个自变量**，新函数 = 原函数 −（要换掉的变量 × 其共轭量）。

| 新函数 | 定义 | 自然变量 | 换掉的变量 |
|:---|:---|:---|:---|
| 焓 H | U + pV | (S, p) | V → p |
| Helmholtz 自由能 A | U − TS | (T, V) | S → T |
| Gibbs 自由能 G | H − TS = U + pV − TS | (T, p) | S→T、V→p |

### 1.3 四大基本方程

$$dU = T\,dS - p\,dV \qquad dH = T\,dS + V\,dp$$
$$dA = -S\,dT - p\,dV \qquad dG = -S\,dT + V\,dp$$

从这四个方程可直接读出对应偏导数（如 $(\partial G/\partial p)_T = V$、$(\partial G/\partial T)_p = -S$）。

> ![[4139b1fc7b31fe6f3b88daa5f719beaf05521ab0f86196d4c1d9259f7e76ca44.jpg]]
*图 1 热力学四边形 (Born Square) 与 Maxwell 关系转换*：热力学四边形——U/H/A/G 四角，相邻函数关系，箭头标注 Legendre 变换方向，自然变量标注在边上。

---

## 二、Maxwell 关系

### 2.1 四条关系式

由四大基本方程的**二阶混合偏导数相等**（如 $\frac{\partial^2 U}{\partial S\partial V} = \frac{\partial^2 U}{\partial V\partial S}$）自动推出：

$$\left(\frac{\partial T}{\partial V}\right)_S = -\left(\frac{\partial p}{\partial S}\right)_V \qquad \left(\frac{\partial T}{\partial p}\right)_S = \left(\frac{\partial V}{\partial S}\right)_p$$
$$\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial p}{\partial T}\right)_V \qquad \left(\frac{\partial S}{\partial p}\right)_T = -\left(\frac{\partial V}{\partial T}\right)_p$$

### 2.2 记忆口诀

> **同侧同号，异侧异号**：横着看每个方程，若两个偏导数的"固定量"（下标）与被求偏导的变量在函数符号（T/S/p/V）上**同侧**则同号，**异侧**则异号。
>
> 最常用的是 **第 3、4 条**（把难以实验测量的 $(\partial S/\partial V)_T$、$(\partial S/\partial p)_T$ 换成可测的 $(\partial p/\partial T)_V$、$(\partial V/\partial T)_p$）——竞赛不要求背 4 条，但要求会用这 2 条。

### 2.3 应用：热容差与 Joule-Thomson

**热容差公式**（Maxwell 第 3 条 + 熵的全微分）：

$$C_p - C_V = T\left(\frac{\partial p}{\partial T}\right)_V\left(\frac{\partial V}{\partial T}\right)_p = \frac{\alpha^2 T V}{\kappa_T}$$

其中 $\alpha = \frac{1}{V}(\partial V/\partial T)_p$（体膨胀系数），$\kappa_T = -\frac{1}{V}(\partial V/\partial p)_T$（等温压缩系数）。理想气体 $\alpha=1/T$、$\kappa_T=1/p$ → $C_p-C_V=nR$。

**Joule-Thomson 系数**（Maxwell 第 4 条）：$\mu_{JT} = \left(\frac{\partial T}{\partial p}\right)_H = \frac{V}{C_p}(\alpha T - 1)$——判断节流膨胀致冷/致热。

> 💡 决赛考点：**能把不可测偏导数换成可测偏导数**——这就是 Maxwell 关系的全部价值。

---

## 三、Gibbs-Helmholtz 方程

### 3.1 微分形式

$$\left(\frac{\partial (G/T)}{\partial T}\right)_p = -\frac{H}{T^2}$$

等价形式：$\left(\frac{\partial G}{\partial T}\right)_p = \frac{G - H}{T}$（由 $G=H-TS$、$(\partial G/\partial T)_p=-S$ 推出）。

### 3.2 变温应用

对反应：$\Delta_r G^\circ$ 随温度变化

$$\frac{\Delta G^\circ(T_2)}{T_2} - \frac{\Delta G^\circ(T_1)}{T_1} = -\Delta H^\circ\left(\frac{1}{T_2} - \frac{1}{T_1}\right)$$

- 已知某温度 $T_1$ 的 $\Delta G^\circ$，可用上式求另一温度 $T_2$ 的 $\Delta G^\circ$（假设 $\Delta H^\circ$ 不随温度变）。
- 与 van't Hoff 的关系：$K$ 随温度由 $\Delta H^\circ$ 决定（物化综合计算 §〇 已讲），两者是**同一件事**在"自由能语言"与"平衡常数语言"下的表达。

---

## 四、Boltzmann 分布与配分函数

### 4.1 Boltzmann 分布

$$\frac{N_i}{N} = \frac{g_i\, e^{-\beta \varepsilon_i}}{q}, \qquad \beta = \frac{1}{kT}$$

- $N_i$：处于能级 $\varepsilon_i$（简并度 $g_i$）的分子数；
- $q$：**分子配分函数**（归一化因子），$q = \sum_j g_j e^{-\beta\varepsilon_j}$；
- 物理意义：低温/高能级 → 占据数指数衰减；高温 → 各能级趋于均匀。

### 4.2 配分函数的分解

分子能量近似可分解为平动 + 转动 + 振动 + 电子：

$$q = q^T \cdot q^R \cdot q^V \cdot q^E$$

> ![[55b591c48a387bf35292cc9de8a74c38ed5e9f7a5a22d1df7c1d1f05f19fd13d.jpg]]
*图 2 分子配分函数 q 的分解与依赖变量关系图*：配分函数分解树——分子 q 分为 平动/转动/振动/电子 四支，每支标注其依赖的量（T、σ、ν̃ 等）。

### 4.3 各模式配分函数（了解会用）

| 模式 | 配分函数 | 关键参数 |
|:---|:---|:---|
| 平动 | $q^T = \dfrac{V}{\Lambda^3}$，$\Lambda = \dfrac{h}{(2\pi mkT)^{1/2}}$ | 热波长 Λ |
| 转动 | $q^R = \dfrac{kT}{\sigma hc\tilde{B}}$ | 对称数 σ、转动常数 $\tilde{B}$ |
| 振动 | $q^V = \dfrac{1}{1 - e^{-\beta hc\tilde{\nu}}}$ | 振动波数 $\tilde{\nu}$ |
| 电子 | $q^E = g_0 + g_1 e^{-\beta\Delta\varepsilon}$ | 基态简并度 g₀ |

> 💡 竞赛只需**会用**：知道平动 q^T 与 V、T 的关系，振动 q^V 在高温时趋于 kT/hcν̃，转动 q^R 与 T 成正比。

---

## 五、从配分函数到热力学量

### 5.1 内能

$$U - U(0) = NkT^2\left(\frac{\partial \ln q}{\partial T}\right)_V$$

- 每个自由度贡献：平动 $\frac{3}{2}kT$、转动 $kT$（线性分子）、振动高温极限 $kT$。
- 记忆：**能量 = 粒子数 × 温度 × ln q 对温度的导数**。

### 5.2 熵（定域 vs 离域）

$$\text{定域子：}\quad S = \frac{U-U(0)}{T} + Nk\ln q \qquad \text{离域子：}\quad S = \frac{U-U(0)}{T} + Nk\ln\frac{qe}{N}$$

- 差项 $Nk\ln(e/N)$ 来自全同粒子的 $N!$ 校正（Gibbs 悖论解法）。
- 定域子（晶体中原子的可分辨位点）用前式；离域子（气体分子不可区分）用后式。

### 5.3 Helmholtz 自由能

$$A - A(0) = -NkT\ln q$$

- 由 $A$ 可再得 $p = -(\partial A/\partial V)_T$、$S = -(\partial A/\partial T)_V$——**所有热力学量都可从 q 求**（这就是"宝典"）。

---

## 六、统计熵的应用

### 6.1 Sackur-Tetrode 方程（单原子理想气体绝对熵）

将 $q^T$ 代入离域子熵公式：

$$S = Nk\left[\ln\frac{V}{N\Lambda^3} + \frac{5}{2}\right] = nR\left[\ln\frac{V_m e^{5/2}}{N_A \Lambda^3}\right]$$

- 用途：**计算理想气体的绝对熵**（无需量热实验）。
- 竞赛只要会代入：已知 $m$（原子质量）、$T$、$V$、$N$ → 求 $S$。

### 6.2 残余熵

- 第三定律说 0 K 时完美晶体熵为 0；但实际晶体（如 CO、冰、N₂O）在 0 K 仍有 **残余熵**——因为分子取向/位置无序冻结。
- 残余熵 $S_0 = k\ln W_0$（$W_0$ 为 0 K 时的微观状态数）。
- 例：CO 晶体每个分子有 2 种取向 → $W_0 = 2^{N}$ → $S_0 = Nk\ln 2 = R\ln 2$。
- 意义：**统计熵与热力学熵在 0 K 的差异证据**（认知冲突三的落点）。

> ![[126fa04ad01b7940961ac90eff61f58a5fc39c1b9d03988f7b788ab5b0ea90f2.jpg]]
*图 3 Sackur-Tetrode 方程：平动熵随 T 和 V 变化关系*：Sackur-Tetrode 熵随温度/体积变化示意；或残余熵示意（CO 分子取向无序）。

---

## 七、竞赛级综合视角

> 本讲把"宏观热力学"与"微观统计"缝合在一起：

| 宏观量 | 微观来源 | 桥梁 |
|:---|:---|:---|
| 热力学熵 S | $S = k\ln\Omega$ | Boltzmann |
| 内能 U | $U = NkT^2(\partial\ln q/\partial T)_V$ | 配分函数 |
| 自由能 A | $A = -NkT\ln q$ | 配分函数 |
| 热容 C | $\partial U/\partial T$ | 配分函数 |
| 平衡常数 K | $\Delta A^\circ = -RT\ln K$ | 配分函数（拓展 13F） |

> 💡 **一句话**：宏观热力学解决"能发生什么"（判据），统计热力学解释"为什么"（微观起源）。Maxwell 关系是热力学内部的"变形金刚"，配分函数是宏观-微观的"翻译机"。

---

## 📌 本讲速查

| 概念 | 公式 | 竞赛要点 |
|:---|:---|:---|
| 母方程 | $dU = TdS - pdV$ | 其余三个方程由 Legendre 变换得 |
| 四大基本方程 | dU/dH/dA/dG | 直接读偏导数 |
| Maxwell 口诀 | 同侧同号，异侧异号 | 最常用第 3、4 条 |
| 热容差 | $C_p-C_V = \alpha^2TV/\kappa_T$ | 理想气体 = nR |
| Gibbs-Helmholtz | $(\partial(G/T)/\partial T)_p = -H/T^2$ | 变温求 ΔG° |
| Boltzmann | $N_i/N = g_i e^{-\beta\varepsilon_i}/q$ | β=1/kT |
| 配分函数 | $q = \sum g e^{-\beta\varepsilon}$ | 分解 q^T·q^R·q^V·q^E |
| 内能 | $U-U(0) = NkT^2(\partial\ln q/\partial T)_V$ | 各自由度能量加和 |
| 熵 | 定域 $S=(U-U(0))/T+Nk\ln q$；离域 −Nk ln N | 差 $Nk\ln(e/N)$ |
| 自由能 | $A-A(0) = -NkT\ln q$ | 母函数 |
| Sackur-Tetrode | $S = nR\ln(V_m e^{5/2}/N_A\Lambda^3)$ | 单原子理想气体绝对熵 |
| 残余熵 | $S_0 = k\ln W_0$ | CO 晶体 = R·ln2 |

---

## 📋 小结

- **四大基本方程**全由 dU=TdS−pdV 经 Legendre 变换而来；
- **Maxwell 关系** = 二阶混合偏导相等 → 把不可测偏导换成可测偏导；
- **配分函数 q** 是统计热力学的母函数：U、S、A 都能从它求；
- **定域/离域熵差** Nk·ln(e/N) 来自全同粒子；
- **Sackur-Tetrode / 残余熵**把统计熵与热力学熵（第三定律）缝合。

**一句话记忆**：先背 dU=TdS−pdV，其余全靠"变换 + 求导"；统计侧只需"q 一出，U/S/A 全有"。

---

## 核心公式速查

> 考前一张纸：按模块查公式。易错提醒与正文各节 [!warning] 呼应。

### 热力学关系

| 公式 / 规则 | 适用条件 / 要点 | 易错提醒 |
|:---|:---|:---|
| Maxwell 关系 | 由四大基本方程二阶混合偏导推出 | 当成独立新公式背是错的；「同侧同号，异侧异号」 |
| $C_p-C_V = \alpha^2TV/\kappa_T$ | 理想气体 = nR | 忘除以 $\kappa_T$ |
| Gibbs-Helmholtz：$(\partial(G/T)/\partial T)_p = -H/T^2$ | 变温求 $\Delta G^\circ$ | 分子是 H 不是 G |

### 配分函数与统计熵

| 公式 / 规则 | 适用条件 / 要点 | 易错提醒 |
|:---|:---|:---|
| Boltzmann：$N_i/N = g_i e^{-\beta\varepsilon_i}/q$ | q 是分母（归一化）| 与 q 混淆；忘乘简并度 $g_i$ |
| $\Lambda = h/(2\pi mkT)^{1/2}$ | 平动 q^T | 用错 Λ |
| $U = NkT^2(\partial\ln q/\partial T)_V$ | 各自由度能量加和 | 忘乘 N |
| 定域/离域熵差 $Nk\ln(e/N)$ | 气体离域必须 $-Nk\ln N$ | 定域/离域用错 |

### 熵的两种来源

| 公式 / 规则 | 适用条件 / 要点 | 易错提醒 |
|:---|:---|:---|
| Sackur-Tetrode：$S = nR\ln(V_m e^{5/2}/N_A\Lambda^3)$ | 单原子理想气体绝对熵 | 忘 $e^{5/2}$ 因子 |
| 残余熵：$S_0 = k\ln W_0$ | 0 K 非完美晶体（CO = R ln2）| 忽略残余熵 |
| 统计熵 = 热力学熵 | 同一熵的微观/宏观两面 | 视为两个不同概念是错的 |

---

## 🏋️ 三级练习（15 题）

### 🌱 基础巩固（5 题）

1. 写出四大基本方程，并直接从 dG 读出 $(\partial G/\partial p)_T$ 和 $(\partial G/\partial T)_p$。
2. 由 dA = −SdT − pdV 用二阶混合偏导推导 Maxwell 第 3 条：$(\partial S/\partial V)_T = (\partial p/\partial T)_V$。
3. 写出 Boltzmann 分布与分子配分函数 q 的定义式，说明 β 的物理意义。
4. 单原子理想气体，$N=1.0\times10^{23}$，$T=300$ K，$V=1.0$ L，$m=6.6\times10^{-26}$ kg。求热波长 Λ 与平动配分函数 q^T。
5. 理想气体 C_p−C_V = nR：用 $\alpha=1/T$、$\kappa_T=1/p$ 代入热容差公式验证。

### 🔥 竞赛入门（5 题）

6. 用 Maxwell 第 4 条 $(\partial S/\partial p)_T = -(\partial V/\partial T)_p$，由状态方程 $pV=nRT$ 求 $(\partial S/\partial p)_T$。
7. 已知 298K 某反应 $\Delta G^\circ = +50.0$ kJ/mol，$\Delta H^\circ = -20.0$ kJ/mol（不随温度变）。用 Gibbs-Helmholtz 求 350K 的 $\Delta G^\circ$。
8. 双原子分子 CO，$\tilde{B}=1.93$ cm⁻¹，对称数 σ=1，$T=300$ K。求转动配分函数 q^R（$hc\tilde{B}$ 单位换算：$hc\tilde{B}/k \approx 2.78$ K）。
9. 由配分函数求内能：某分子在 300K 时 $(\partial\ln q/\partial T)_V = 0.01$ K⁻¹，$N=1$ mol。求 $U-U(0)$。
10. 比较：同温同压下，1 mol 离域理想气体的熵比"把同样 N 个粒子当定域处理"的熵小多少？（用公式说明）

### 🏆 真题挑战（5 题）

11. **Sackur-Tetrode**：Ar（$M=39.95$ g/mol，单原子），300K、1 atm，求摩尔绝对熵 $S_m$（已知 $N_A\Lambda^3/V_m$ 计算结果，代入公式）。
12. **残余熵**：CO 晶体在 0 K 每个分子 2 种取向无序，求 1 mol CO 晶体的残余熵（用 $S_0 = Nk\ln2$）。
13. **Boltzmann 分布应用**（Atkins 13A.1 类）：某分子基态简并度 1、第一激发态 $\varepsilon=2.0\times10^{-20}$ J、简并度 3。300K 时求激发态占据比例。
14. **Maxwell 综合**：证明理想气体 $C_p-C_V = nR$ 用热容差公式 + 理想气体状态方程。
15. **拓展（13F 简要）**：说明为何配分函数能求平衡常数（$K \propto q_{产物}/q_{反应物}$），并指出其适用条件（理想气体、独立粒子）。

---

## 🔗 延伸阅读

- [[03-知识点/决赛要求/物理化学深化/Boltzmann统计初步]] — 配分函数/统计熵完整 KP（含 2 道例题解答）
- [[03-知识点/决赛要求/物理化学深化/麦克斯韦关系式]] — Maxwell 四条 + 记忆口诀 + 热容差 + Joule-Thomson
- [[03-知识点/决赛要求/物理化学深化/热力学四大基本方程]]、[[03-知识点/决赛要求/物理化学深化/吉布斯-亥姆霍兹方程]]
- [[07-资料提炼/书籍提炼/提炼-Atkins物理化学-主题2-3-热力学定律]] — Maxwell/Gibbs-Helmholtz 提炼
- [[07-资料提炼/书籍提炼/提炼-Atkins物理化学-主题13-14-统计热力学与分子相互作用]] — 统计热力学提炼
- [[04-课件/学生讲义/物化综合计算-超级充实版（自学完整）]] — 4-7 物化线姊妹讲义（§〇 化学势/van't Hoff 中段）
- Atkins《Physical Chemistry》第11版 主题 2-3、13A-13E；傅献彩《物理化学》下册 §统计热力学

---

*本讲义依据 [[模板-学生讲义]] 自学完整版 v3.0 生成，承接 [[决赛04-热力学]]，4-7 物化线第三讲义。*

*深度边界：不展开正则系综（Atkins 13D）、配分函数算平衡常数完整推导（13F）、量子统计、Debye 理论完整推导。*
