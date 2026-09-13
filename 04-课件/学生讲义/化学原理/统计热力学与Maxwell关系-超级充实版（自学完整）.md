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
  - "[[04-课件/学生讲义/化学原理/物化综合计算-超级充实版（自学完整）]]"
  - "[[04-课件/学生讲义/化学原理/热力学初步-超级充实版（自学完整）]]"
  - "[[04-专题与题型/专题/专题-热力学初步]]"
tags: [学生讲义, 超级充实版, 物理化学, 第四轮, 统计热力学, Maxwell关系, 自学完整]
created: 2026-08-04
has_images: false
image_count: 0
updated: 2026-08-07
last_audit: "2026-08-04 新建（S2）：承接决赛04 热力学深半（Maxwell 初步 + 统计热力学配分函数），补物化综合计算 §〇 未覆盖部分；全篇 $E^\\theta$ 规范；图片以 📌 占位标记（待补 3 处）；2026-08-07 R4教材审计：补 Boltzmann 分布推导链（构型/Stirling/最概然/Lagrange/β热力学身份）与配分函数连乘原理（Atkins 主题13A-B）；2026-08-07 R5原文级复核：修正 §3.2 Gibbs-Helmholtz 积分式符号 −→+；2026-08-07 R8语言打磨+教材审计：ΔA°→ΔG° 平衡常数式统一；去 Atkins/13A/13F 章节标签；补 Kirchhoff 定律、Debye T³ 微观解释、配分函数求平衡常数完整式"
template_version: 自学完整版 v3.0
stage: published
sources:
  - "[[07-资料提炼/书籍提炼/提炼-Atkins物理化学-主题2-3-热力学定律]]"
  - "[[07-资料提炼/书籍提炼/提炼-Atkins物理化学-主题13-14-统计热力学与分子相互作用]]"
problems: []
exercise_count: 15
exercise_levels:
  - "基础巩固 5 题"
  - "竞赛入门 5 题"
  - "真题挑战 5 题"
module: 化学原理
---

# 第四轮·4-7 统计热力学与 Maxwell 关系（冲刺班 · 自学完整）

<!-- ============ 教师向信息区+规划区（学生不可见，Word/PDF 导出自动忽略） ============
> 课型：冲刺专题（1-2 × 90 min）　|　轮次：第四轮　|　定位：决赛04 热力学深半（4-7 物化线第三讲义）
> **承接考纲**：[[决赛04-热力学]]——物化综合计算 §〇 已覆盖化学势/van't Hoff/Clausius-Clapeyron 中段，本讲补**Maxwell 关系初步 + 统计热力学（配分函数）**深半。
> **前置知识**：第一轮热力学初步（ΔH/ΔS/ΔG、ΔG=ΔH−TΔS）；物化综合计算 §〇（化学势）
> **对应专题页**：[[04-专题与题型/专题/专题-热力学初步]]（深化链上一站）

> **本讲定位**：本讲是**决赛理论补完**，不是计算压轴。决赛要求的是"知道四大方程、会用 Maxwell 关系做偏导数变换、理解配分函数是所有热力学量的母函数"。**不展开**：正则系综严格推导、配分函数算平衡常数的完整处理、统计热力学的量子统计细节。

============================================================================= -->

---

<!-- ============ 教师向规划区（学生不可见，Word/PDF 导出自动忽略） ============
**主线导航（教师向规划）**

| 站 | 主题 | 核心武器 | 锚点 |
|:--:|:---|:---|:---|
| ① | 四大基本方程 + Legendre | dU=TdS−pdV 家族 | 决赛04 |
| ② | Maxwell 关系 | 四条 + 记忆口诀 | 决赛04 |
| ③ | Gibbs-Helmholtz | (∂(G/T)/∂T)_p=−H/T² | 决赛04 |
| ④ | Boltzmann 分布与配分函数 | q = $Σg·e^{−βε}$ | 决赛04 |
| ⑤ | 由配分函数求热力学量 | U = NkT²(∂lnq/∂T)_V | 决赛04 |
| ⑥ | 统计熵应用 | Sackur-Tetrode / 残余熵 | 决赛04 |

============================================================================= -->

---

## 学习目标（可测量）

| # | 目标 | 达成判据 |
|:--:|:---|:---|
| 1 | 从 dU=TdS−pdV 经 Legendre 变换得到四大基本方程 | 能写出 U/H/A/G 的全微分 |
| 2 | 记住四条 Maxwell 关系并会用记忆口诀 | 能由任一基本方程推出对应 Maxwell 式 |
| 3 | 用 Maxwell 关系推导热容差 $C_p$−$C_V$ 公式 | ≥ 85% 正确 |
| 4 | 理解配分函数 q 的定义与分解 | 能写 q=$q_T$·$q_R$·$q_V$·$q_E$ |
| 5 | 由 q 求内能 U 和熵 S | 定域/离域熵差 Nk·ln(e/N) 脱口而出 |

---

## 认知冲突（本讲最值得停下来想的地方）

> [!abstract] 冲突一：Maxwell 关系不是"新知识"，是"同一批偏导数的不同写法"
> 你觉得四条 Maxwell 关系是要背的四个新公式。**错**——它们是从四大基本方程（全是 dU=TdS−pdV 的变形）用"二阶混合偏导数相等"推出来的。背会四大基本方程 → 四条 Maxwell 自动出来。突破：**先背 1 条（dU=TdS−pdV），其余靠推导**。

> [!abstract] 冲突二：配分函数是"统计热力学的宝典"
> 你也许会问"配分函数到底有什么用"。**它是一台母机**：内能、熵、Helmholtz 自由能、压强、平衡常数全部能从 q 求出来。竞赛只需记住"U 和 S 怎么从 q 求"两条主线。突破：把 q 看成"一张牌"，U、S、A 都是从它翻出来的"牌面"。

> [!abstract] 冲突三：S=k·lnΩ 与热力学熵是"同一件事"
> 你也许会把统计熵和热力学熵当成两个概念。**它们是同一个熵**：统计熵是"微观起源"，热力学熵是"宏观测量"。Clausius 的 dS=δq_rev/T 与 Boltzmann 的 S=k·lnΩ 描述同一个量。突破：残余熵就是两者连接的证据（0 K 下热力学熵趋 0 而统计熵不为 0）。

> [!abstract] 冲突四：定域子与离域子的熵差"Nk·ln(e/N)"
> 同温同压下 1 mol 固体（定域）与 1 mol 理想气体（离域）的熵公式差一项 Nk·ln(e/N)——离域粒子"不可区分"（全同粒子），除以 N! 使熵减小这一项——是 Gibbs 悖论（混合熵消失）的解法。

---

<!-- ============ 教师向规划区（学生不可见，Word/PDF 导出自动忽略） ============
**深度分层（教师向边界）**

| 层级 | 内容 | 说明 |
|:---:|:---|:---|
| 📝 **决赛必会** | 四大基本方程；四条 Maxwell 关系及记忆口诀；$C_p$−$C_V$=α²TV/κ_T；Gibbs-Helmholtz 微分/积分式；Boltzmann 分布；配分函数定义与分解；U、S 由 q 求；定域/离域熵差 | 决赛04 核心，动手必练 |
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

> 每次变换**换掉一个自变量**，新函数 = 原函数 −（要换掉的变量 × 其共轭量）。

| 新函数 | 定义 | 自然变量 | 换掉的变量 |
|:---|:---|:---|:---|
| 焓 H | U + pV | (S, p) | V → p |
| Helmholtz 自由能 A | U − TS | (T, V) | S → T |
| Gibbs 自由能 G | H − TS = U + pV − TS | (T, p) | S→T、V→p |

### 1.3 四大基本方程

$$dU = T\,dS - p\,dV \qquad dH = T\,dS + V\,dp$$
$$dA = -S\,dT - p\,dV \qquad dG = -S\,dT + V\,dp$$

从这四个方程可直接读出对应偏导数（如 $(\partial G/\partial p)_T = V$、$(\partial G/\partial T)_p = -S$）。

> [!note] 热力学四边形 (Born Square) 与 Maxwell 关系
> U/H/A/G 四角方阵：左上 U(S,V) → 右上 H(S,p)（Legendre V→p）；左下 A(T,V)（Legendre S→T）→ 右下 G(T,p)。四条边标注自然变量，对角箭头标注 Maxwell 关系推导方向。


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

> 决赛考点：**能把不可测偏导数换成可测偏导数**——这就是 Maxwell 关系的全部价值。

---

## 三、Gibbs-Helmholtz 方程

### 3.1 微分形式

$$\left(\frac{\partial (G/T)}{\partial T}\right)_p = -\frac{H}{T^2}$$

等价形式：$\left(\frac{\partial G}{\partial T}\right)_p = \frac{G - H}{T}$（由 $G=H-TS$、$(\partial G/\partial T)_p=-S$ 推出）。

### 3.2 变温应用

对反应：$\Delta_r G^\theta$ 随温度变化

$$\frac{\Delta G^\theta(T_2)}{T_2} - \frac{\Delta G^\theta(T_1)}{T_1} = +\Delta H^\theta\left(\frac{1}{T_2} - \frac{1}{T_1}\right)$$

- 已知某温度 $T_1$ 的 $\Delta G^\theta$，可用上式求另一温度 $T_2$ 的 $\Delta G^\theta$（假设 $\Delta H^\theta$ 不随温度变）。
- 若 $\Delta H^\theta$ 随温度变化，先用 **Kirchhoff 定律** $\Delta_r H^\theta(T_2)=\Delta_r H^\theta(T_1)+\int_{T_1}^{T_2}\Delta_r C_p^\theta\,dT$ 求出对应温度的 $\Delta H^\theta$，再代回上式。
- 与 van't Hoff 的关系：$K$ 随温度由 $\Delta H^\theta$ 决定（物化综合计算 §〇 已讲），两者是**同一件事**在"自由能语言"与"平衡常数语言"下的表达。

---

## 四、Boltzmann 分布与配分函数

### 4.1 Boltzmann 分布

$$\frac{N_i}{N} = \frac{g_i\, e^{-\beta \varepsilon_i}}{q}, \qquad \beta = \frac{1}{kT}$$

- $N_i$：处于能级 $\varepsilon_i$（简并度 $g_i$）的分子数；
- $q$：**分子配分函数**（归一化因子），$q = \sum_j g_j e^{-\beta\varepsilon_j}$；
- 物理意义：低温/高能级 → 占据数指数衰减；高温 → 各能级趋于均匀。

**推导链（为什么是 Boltzmann 分布）**：

1. **构型与权重**：把 $N$ 个分子分配到能级 $\{\varepsilon_1, \varepsilon_2, \dots\}$，占据数 $\{N_1, N_2, \dots\}$ 称为一个**构型**；该构型的**权重**（微观状态数）$W = \dfrac{N!}{N_1!\,N_2!\,\cdots}$。
2. **Stirling 近似**：$\ln n! \approx n\ln n - n$，故 $\ln W \approx N\ln N - \sum_j N_j\ln N_j$。
3. **最概然分布**：等概率原理 → 宏观平衡态对应**微观状态数最多**的构型；$N$ 极大时最概然分布几乎必然出现，即观测分布 = 使 $W$ 最大的分布。
4. **Lagrange 乘子法**：在约束 $\sum_j N_j = N$（粒子守恒）、$\sum_j N_j\varepsilon_j = U$（能量守恒）下最大化 $\ln W$，引入乘子 $\alpha,\ \beta$：
$$\frac{\partial}{\partial N_j}\left[\ln W - \alpha\sum_j N_j - \beta\sum_j N_j\varepsilon_j\right] = 0 \;\Longrightarrow\; \frac{N_j}{N} = \frac{e^{-\beta\varepsilon_j}}{\sum_i e^{-\beta\varepsilon_i}}$$
5. **简并度修正**：能级 $\varepsilon_j$ 若有简并度 $g_j$，其微观状态数扩 $g_j$ 倍 → $N_j \propto g_j e^{-\beta\varepsilon_j}$，即
$$\frac{N_j}{N} = \frac{g_j\, e^{-\beta\varepsilon_j}}{\sum_i g_i e^{-\beta\varepsilon_i}} = \frac{g_j\, e^{-\beta\varepsilon_j}}{q}$$
6. **$\beta$ 的热力学身份**：对比 $U - U(0) = NkT^2\left(\frac{\partial\ln q}{\partial T}\right)_V$ 与 $S = k\ln W$ 可证 $\beta = 1/(kT)$——**温度是分布参数**（温度的统计本质）。

> [!tip] 记忆锚
> 三个数：$\beta = 1/kT$、$q = \sum_j g_j e^{-\beta\varepsilon_j}$、$N_j/N = g_j e^{-\beta\varepsilon_j}/q$。推导只考思路（构型 → 最概然 → 乘子），不要求背 Lagrange 细节。

分子能量近似可分解为平动 + 转动 + 振动 + 电子：

$$q = q^T \cdot q^R \cdot q^V \cdot q^E$$

**为什么能连乘？** 能量可加 → $\varepsilon = \varepsilon^T + \varepsilon^R + \varepsilon^V + \varepsilon^E$，指数相乘 $e^{-\beta\varepsilon} = e^{-\beta\varepsilon^T}\cdot e^{-\beta\varepsilon^R}\cdot e^{-\beta\varepsilon^V}\cdot e^{-\beta\varepsilon^E}$；对全部能级求和后交叉项完全分离，$q$ 分解为四支**独立相乘**。每支只需知道该模式的“能量量子化方式”：平动靠容器 $V$、转动靠转动常数 $\tilde{B}$、振动靠波数 $\tilde{\nu}$、电子靠基态简并度与激发态能差。

> [!note] 分子配分函数 q 的分解与依赖变量
> q = q^T·q^R·q^V·q^E（四支独立相乘）
> - 平动 q^T：依赖 V、T（热波长 Λ）
> - 转动 q^R：依赖 T、σ、B̃
> - 振动 q^V：依赖 T、ν̃
> - 电子 q^E：依赖基态简并度 g₀


### 4.3 各模式配分函数（了解会用）

| 模式 | 配分函数 | 关键参数 |
|:---|:---|:---|
| 平动 | $q^T = \dfrac{V}{\Lambda^3}$，$\Lambda = \dfrac{h}{(2\pi mkT)^{1/2}}$ | 热波长 Λ |
| 转动 | $q^R = \dfrac{kT}{\sigma hc\tilde{B}}$ | 对称数 σ、转动常数 $\tilde{B}$ |
| 振动 | $q^V = \dfrac{1}{1 - e^{-\beta hc\tilde{\nu}}}$ | 振动波数 $\tilde{\nu}$ |
| 电子 | $q^E = g_0 + g_1 e^{-\beta\Delta\varepsilon}$ | 基态简并度 g₀ |

> 竞赛只需**会用**：知道平动 q^T 与 V、T 的关系，振动 q^V 在高温时趋于 kT/hcν̃，转动 q^R 与 T 成正比。

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
- 微观解释：0 K 附近晶格热容服从 **Debye T³ 定律**（$C_V \propto T^3$），温度越低振动自由度冻结越彻底，故完美晶体 0 K 熵趋于 0；取向无序不受此限，留下残余熵。

> [!note] Sackur-Tetrode 方程与残余熵
> 离域子平动熵：$S = nR\ln\!\left(V_\mathrm{m}\,e^{5/2}\,/\,N_\mathrm{A}\Lambda^3\right)$
> 残余熵：CO 晶体 0K 下 S₀ = k·ln(2^N) = R·ln2
> Debye T³ 定律解释完美晶体 0K 熵→0


---

## 七、竞赛级综合视角

> 本讲把"宏观热力学"与"微观统计"缝合在一起：

| 宏观量 | 微观来源 | 桥梁 |
|:---|:---|:---|
| 热力学熵 S | $S = k\ln\Omega$ | Boltzmann |
| 内能 U | $U = NkT^2(\partial\ln q/\partial T)_V$ | 配分函数 |
| 自由能 A | $A = -NkT\ln q$ | 配分函数 |
| 热容 C | $\partial U/\partial T$ | 配分函数 |
| 平衡常数 K | $\Delta G^\theta = -RT\ln K$ | 配分函数 → 平衡常数 |

> **一句话**：宏观热力学解决"能发生什么"（判据），统计热力学解释"为什么"（微观起源）。Maxwell 关系是热力学内部的"变形金刚"，配分函数是宏观-微观的"翻译机"。

---

## 本讲速查

| 概念 | 公式 | 竞赛要点 |
|:---|:---|:---|
| 母方程 | $dU = TdS - pdV$ | 其余三个方程由 Legendre 变换得 |
| 四大基本方程 | dU/dH/dA/dG | 直接读偏导数 |
| Maxwell 口诀 | 同侧同号，异侧异号 | 最常用第 3、4 条 |
| 热容差 | $C_p-C_V = \alpha^2TV/\kappa_T$ | 理想气体 = nR |
| Gibbs-Helmholtz | $(\partial(G/T)/\partial T)_p = -H/T^2$ | 变温求 $\Delta G^\theta$ |
| Boltzmann | $N_i/N = g_i e^{-\beta\varepsilon_i}/q$ | β=1/kT |
| 配分函数 | $q = \sum g e^{-\beta\varepsilon}$ | 分解 q^T·q^R·q^V·q^E |
| 内能 | $U-U(0) = NkT^2(\partial\ln q/\partial T)_V$ | 各自由度能量加和 |
| 熵 | 定域 $S=(U-U(0))/T+Nk\ln q$；离域 −Nk ln N | 差 $Nk\ln(e/N)$ |
| 自由能 | $A-A(0) = -NkT\ln q$ | 母函数 |
| Sackur-Tetrode | $S = nR\ln(V_m e^{5/2}/N_A\Lambda^3)$ | 单原子理想气体绝对熵 |
| 残余熵 | $S_0 = k\ln W_0$ | CO 晶体 = R·ln2 |

---

## 小结

- **四大基本方程**全由 dU=TdS−pdV 经 Legendre 变换而来；
- **Maxwell 关系** = 二阶混合偏导相等 → 把不可测偏导换成可测偏导；
- **配分函数 q** 是统计热力学的母函数：U、S、A 都能从它求；
- **定域/离域熵差** Nk·ln(e/N) 来自全同粒子；
- **Sackur-Tetrode / 残余熵**把统计熵与热力学熵（第三定律）缝合。

**一句话记忆**：先背 dU=TdS−pdV，其余全靠"变换 + 求导"；统计侧只需"q 一出，U/S/A 全有"。

---

## 核心公式速查

> 考前一张纸：按模块查公式。

### 热力学关系

| 公式 / 规则 | 适用条件 / 要点 | 易错提醒 |
|:---|:---|:---|
| Maxwell 关系 | 由四大基本方程二阶混合偏导推出 | 当成独立新公式背是错的；「同侧同号，异侧异号」 |
| $C_p-C_V = \alpha^2TV/\kappa_T$ | 理想气体 = nR | 忘除以 $\kappa_T$ |
| Gibbs-Helmholtz：$(\partial(G/T)/\partial T)_p = -H/T^2$ | 变温求 $\Delta G^\theta$ | 分子是 H 不是 G |

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

## 三级练习（15 题）

### 基础巩固（5 题）

1. 写出四大基本方程，并直接从 dG 读出 $(\partial G/\partial p)_T$ 和 $(\partial G/\partial T)_p$。
2. 由 dA = −SdT − pdV 用二阶混合偏导推导 Maxwell 第 3 条：$(\partial S/\partial V)_T = (\partial p/\partial T)_V$。
3. 写出 Boltzmann 分布与分子配分函数 q 的定义式，说明 β 的物理意义。
4. 单原子理想气体，$N=1.0\times10^{23}$，$T=300$ K，$V=1.0$ L，$m=6.6\times10^{-26}$ kg。求热波长 Λ 与平动配分函数 q^T。
5. 理想气体 $C_p$−$C_V$ = nR：用 $\alpha=1/T$、$\kappa_T=1/p$ 代入热容差公式验证。

### 竞赛入门（5 题）

6. 用 Maxwell 第 4 条 $(\partial S/\partial p)_T = -(\partial V/\partial T)_p$，由状态方程 $pV=nRT$ 求 $(\partial S/\partial p)_T$。
7. 已知 298K 某反应 $\Delta G^\theta = +50.0$ kJ/mol，$\Delta H^\theta = -20.0$ kJ/mol（不随温度变）。用 Gibbs-Helmholtz 求 350K 的 $\Delta G^\theta$。
8. 双原子分子 CO，$\tilde{B}=1.93$ cm⁻¹，对称数 σ=1，$T=300$ K。求转动配分函数 q^R（$hc\tilde{B}$ 单位换算：$hc\tilde{B}/k \approx 2.78$ K）。
9. 由配分函数求内能：某分子在 300K 时 $(\partial\ln q/\partial T)_V = 0.01$ K⁻¹，$N=1$ mol。求 $U-U(0)$。
10. 比较：同温同压下，1 mol 离域理想气体的熵比"把同样 N 个粒子当定域处理"的熵小多少？（用公式说明）

### 真题挑战（5 题）

11. **Sackur-Tetrode**：Ar（$M=39.95$ g/mol，单原子），300K、1 atm，求摩尔绝对熵 $S_m$（已知 $N_A\Lambda^3/V_m$ 计算结果，代入公式）。
12. **残余熵**：CO 晶体在 0 K 每个分子 2 种取向无序，求 1 mol CO 晶体的残余熵（用 $S_0 = Nk\ln2$）。
13. **Boltzmann 分布应用**：某分子基态简并度 1、第一激发态 $\varepsilon=2.0\times10^{-20}$ J、简并度 3。300K 时求激发态占据比例。
14. **Maxwell 综合**：证明理想气体 $C_p-C_V = nR$ 用热容差公式 + 理想气体状态方程。
15. **拓展**：说明为何配分函数能求平衡常数（$K \propto q_{产物}/q_{反应物}$），并指出其适用条件（理想气体、独立粒子）。
- 参考完整式：$K=\dfrac{(q_{产物}/V)^{\nu_{产物}}}{(q_{反应物}/V)^{\nu_{反应物}}}\times\left(\dfrac{RT}{p^\theta}\right)^{\Delta\nu}$（$\Delta\nu$ 为产物计量数之和减反应物计量数之和）

---

## 参考答案与提示（15 题）

> 使用建议：**先独立做完 15 题再对照**。计算题统一保留 3 位有效数字；若你取 $R=8.314$、$k=1.381\times10^{-23}$ 之外的常数精度，末位允许 ±1 的差异。
> 常数：$h=6.626\times10^{-34}$ J·s，$k=1.381\times10^{-23}$ J·K⁻¹，$N_A=6.022\times10^{23}$ mol⁻¹，$R=8.314$ J·K⁻¹·mol⁻¹，$hc/k=1.4388$ cm·K。

### 基础巩固（5 题）

**1. 四大基本方程**

$$dU = T\,dS - p\,dV \qquad dH = T\,dS + V\,dp$$
$$dA = -S\,dT - p\,dV \qquad dG = -S\,dT + V\,dp$$

由 $dG = -S\,dT + V\,dp$（自然变量为 $T$ 与 $p$）直接读系数：

$$\left(\frac{\partial G}{\partial p}\right)_T = V \qquad \left(\frac{\partial G}{\partial T}\right)_p = -S$$

> 通法：把微分式写成 $dG=(\ )_p\,dT+(\ )_T\,dp$ 的形式，两个括号里就是对应的偏导数——**先认清自然变量，再读系数**。

**2. Maxwell 第 3 条的推导**

$A=A(T,V)$，由 $dA=-S\,dT-p\,dV$ 有 $-S=(\partial A/\partial T)_V$、$-p=(\partial A/\partial V)_T$。二阶混合偏导与求导次序无关：

$$\frac{\partial}{\partial V}\left(\frac{\partial A}{\partial T}\right)_V = \frac{\partial}{\partial T}\left(\frac{\partial A}{\partial V}\right)_T \;\Longrightarrow\; -\left(\frac{\partial S}{\partial V}\right)_T = -\left(\frac{\partial p}{\partial T}\right)_V$$

即

$$\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial p}{\partial T}\right)_V$$

> 易错：负号在两边**同时出现、同时约掉**；常见错误是只在左边留负号。

**3. Boltzmann 分布与配分函数**

$$\frac{N_i}{N} = \frac{g_i\,e^{-\beta\varepsilon_i}}{q} \qquad q = \sum_j g_j\,e^{-\beta\varepsilon_j} \qquad \beta = \frac{1}{kT}$$

- $q$ 是**归一化分母**（全部能级的 $g_je^{-\beta\varepsilon_j}$ 之和），不是某一个能级的玻尔兹曼因子；
- $\beta$ 的物理意义：$\beta=1/kT$ 是"每单位热运动能量"的倒数量纲，$\beta\varepsilon$ 即**能级间距与热运动能量 $kT$ 的比值**。$\beta$ 越大（温度越低），分布越向低能级集中；$\beta$ 越小（温度越高），各能级占据趋于均匀。$\beta=1/kT$ 这个身份由统计熵公式与热力学关系对比确立——**这就是温度的统计定义**。

**4. 热波长与平动配分函数**

$$\Lambda = \frac{h}{\sqrt{2\pi mkT}} = \frac{6.626\times10^{-34}}{\sqrt{2\pi\times6.6\times10^{-26}\times1.381\times10^{-23}\times300}} = 1.60\times10^{-11}\ \text{m} = 16.0\ \text{pm}$$

$$q^T = \frac{V}{\Lambda^3} = \frac{1.0\times10^{-3}\ \text{m}^3}{(1.60\times10^{-11}\ \text{m})^3} = \frac{1.0\times10^{-3}}{4.09\times10^{-33}} = 2.45\times10^{29}$$

> 自检：$q^T/N = 2.45\times10^{6}\gg 1$，经典（非简并）极限成立，用 $q^T=V/\Lambda^3$ 合法。若 $q^T\lesssim N$（低温高密度），必须改用量子统计，此式失效。
> 注意：$q^T$ 是**单分子**平动配分函数；$N$ 个全同离域粒子的总配分函数是 $Q=(q^T)^N/N!$。

**5. 热容差公式验证**

$$C_p - C_V = \frac{\alpha^2 T V}{\kappa_T} = \frac{(1/T)^2\,T\,V}{1/p} = \frac{pV}{T} = \frac{nRT}{T} = nR$$

与理想气体结论一致。最后一步用的就是 $pV=nRT$ 本身，所以这是**自洽检验**而非新结论。

### 竞赛入门（5 题）

**6. Maxwell 第 4 条**

$V=nRT/p \Rightarrow (\partial V/\partial T)_p = nR/p$，代入：

$$\left(\frac{\partial S}{\partial p}\right)_T = -\left(\frac{\partial V}{\partial T}\right)_p = -\frac{nR}{p} = -\frac{V}{T}$$

> 物理含义：等温加压使熵减小。积分可得 $\Delta S = -nR\ln(p_2/p_1)$，即**压强每翻一倍，熵减小 $nR\ln 2$**。

**7. Gibbs-Helmholtz 变温**

$$\frac{\Delta G^\theta(350)}{350} = \frac{50.0}{298} + (-20.0)\times\left(\frac{1}{350}-\frac{1}{298}\right) = 0.16779 + 0.00997 = 0.17776\ \text{kJ·mol}^{-1}\text{·K}^{-1}$$

$$\Delta G^\theta(350) = 0.17776\times350 = +62.2\ \text{kJ·mol}^{-1}$$

> **交叉校验**：先算 $\Delta S^\theta = (\Delta H^\theta-\Delta G^\theta_{298})/298 = -70.0/298 = -0.2349$ kJ·mol⁻¹·K⁻¹，则 $\Delta G^\theta(350) = \Delta H^\theta - 350\Delta S^\theta = -20.0 + 82.2 = +62.2$ kJ·mol⁻¹，两法一致。
> 结论：$\Delta H^\theta<0$（放热）时升温使 $\Delta G^\theta$ 变大、$K$ 变小——与 van't Hoff 方程同源，是同一件事的两种语言。

**8. 转动配分函数**

$$\Theta_R = \frac{hc\tilde{B}}{k} = 1.4388\ \text{cm·K}\times1.93\ \text{cm}^{-1} = 2.777\ \text{K}$$

$T=300\ \text{K}\gg\Theta_R$，可用高温极限式：

$$q^R = \frac{kT}{\sigma hc\tilde{B}} = \frac{T}{\sigma\Theta_R} = \frac{300}{1\times2.777} = 1.08\times10^{2}$$

> CO 是异核双原子分子，对称数 $\sigma=1$；若是 N₂ 等同核双原子分子，$\sigma=2$，$q^R$ 减半（约 54）。

**9. 由配分函数求内能**

$$U-U(0) = NkT^2\left(\frac{\partial\ln q}{\partial T}\right)_V = nRT^2\times0.01 = 1\times8.314\times300^2\times0.01 = 7.48\times10^{3}\ \text{J} = 7.48\ \text{kJ}$$

> 自检：$(\partial\ln q/\partial T)_V$ 若呈 $a/T$ 型（配分函数为 $T^a$ 形式），则 $a = 0.01\times300 = 3$，$U-U(0)=a\,nRT=3nRT$——相当于 6 个平方项自由度（振动已激发）的贡献，量级自洽。
> 易错：题目给 $N=1$ mol，$Nk$ 要换成 $nR$，不要代 $k$ 再乘 $N_A$（结果一样但多一步换算易错）。

**10. 定域 / 离域熵差**

$$S_{\text{定域}} = \frac{U-U(0)}{T} + Nk\ln q \qquad S_{\text{离域}} = \frac{U-U(0)}{T} + Nk\ln\frac{qe}{N}$$

$$S_{\text{离域}} - S_{\text{定域}} = Nk\ln\frac{e}{N} = Nk\,(1-\ln N)$$

1 mol 时 $N=N_A$、$Nk=R$、$\ln N_A = 54.75$：

$$S_{\text{离域}} - S_{\text{定域}} = 8.314\times(1-54.75) = -4.47\times10^{2}\ \text{J·K}^{-1}\text{·mol}^{-1}$$

即：把同样的 $N$ 个粒子当作气体（离域、不可分辨）处理，熵比当作定域处理**小约 447 J·K⁻¹·mol⁻¹**；反过来说，误用定域公式会**高估** 447 J·K⁻¹·mol⁻¹。这一项来自全同粒子的 $N!$ 校正，正是 Gibbs 悖论（同种气体混合熵为 0）的解法。

### 真题挑战（5 题）

**11. Sackur-Tetrode：Ar 摩尔绝对熵**

$$m = \frac{M}{N_A} = \frac{39.95\times10^{-3}}{6.022\times10^{23}} = 6.634\times10^{-26}\ \text{kg}$$

$$\Lambda = \frac{h}{\sqrt{2\pi mkT}} = 1.595\times10^{-11}\ \text{m} \qquad \Lambda^3 = 4.055\times10^{-33}\ \text{m}^3 \qquad N_A\Lambda^3 = 2.442\times10^{-9}\ \text{m}^3\text{·mol}^{-1}$$

$$V_m = \frac{RT}{p} = \frac{8.314\times300}{1.013\times10^{5}} = 2.462\times10^{-2}\ \text{m}^3\text{·mol}^{-1} = 24.6\ \text{L·mol}^{-1}$$

$$S_m = R\ln\frac{V_m e^{5/2}}{N_A\Lambda^3} = 8.314\times\left[\ln\left(1.008\times10^{7}\right) + 2.5\right] = 8.314\times18.626 = 154.9\ \text{J·K}^{-1}\text{·mol}^{-1}$$

> **可信度校验**：把条件改成 298.15 K、1 bar 重算，得 $154.8$ J·K⁻¹·mol⁻¹，与 Ar 标准摩尔熵的文献值 $154.8$ J·K⁻¹·mol⁻¹ 完全吻合——说明公式、常数、单位三者都对上了。
> 易错：量纲必须是 m³·mol⁻¹ 与 m³ 同级（1 L = 10⁻³ m³ 不能忘换）；指数上 $e^{5/2}$ 因子漏掉会少算 $2.5R\approx20.8$ J·K⁻¹·mol⁻¹。

**12. 残余熵**

每个分子 2 种取向，$N$ 个分子的微观状态数 $W_0 = 2^{N}$：

$$S_0 = k\ln W_0 = Nk\ln 2 = R\ln 2 = 8.314\times0.6931 = 5.76\ \text{J·K}^{-1}\text{·mol}^{-1}$$

> 这正是量热熵（按第三定律在 0 K 归零）与统计熵之间的差额，是"统计熵与热力学熵是同一个熵"的直接证据；完美晶体（无取向无序）此项为 0。

**13. Boltzmann 占据比例**

$$kT = 1.381\times10^{-23}\times300 = 4.142\times10^{-21}\ \text{J} \qquad \beta\varepsilon = \frac{2.0\times10^{-20}}{4.142\times10^{-21}} = 4.83$$

$$q = g_0 + g_1 e^{-\beta\varepsilon} = 1 + 3\times e^{-4.83} = 1 + 3\times7.997\times10^{-3} = 1.0240$$

$$\frac{N_1}{N} = \frac{g_1 e^{-\beta\varepsilon}}{q} = \frac{0.02399}{1.0240} = 2.34\times10^{-2}$$

即激发态约占 **2.34%**（约 1/43），基态占 97.66%。

> 三个易错点：①分子必须乘简并度 $g_1=3$；②分母 $q$ 必须含激发态贡献（虽只有 2.4%，漏掉会让结果偏大 2.4%）；③也可直接用比值式 $N_1/N_0=(g_1/g_0)e^{-\beta\varepsilon}=0.0240$ 反推，两法互校。

**14. 证明 $C_p-C_V = nR$**

把熵看作 $S=S(T,V)$，用 Maxwell 第 3 条改写第二项：

$$dS = \left(\frac{\partial S}{\partial T}\right)_V dT + \left(\frac{\partial S}{\partial V}\right)_T dV = \frac{C_V}{T}\,dT + \left(\frac{\partial p}{\partial T}\right)_V dV$$

在恒 $p$ 条件下对 $T$ 求导，并乘 $T$：

$$C_p = T\left(\frac{\partial S}{\partial T}\right)_p = C_V + T\left(\frac{\partial p}{\partial T}\right)_V\left(\frac{\partial V}{\partial T}\right)_p$$

代入 $V=nRT/p$：$(\partial p/\partial T)_V = nR/V$，$(\partial V/\partial T)_p = nR/p$，故

$$C_p - C_V = T\cdot\frac{nR}{V}\cdot\frac{nR}{p} = T\cdot\frac{n^2R^2}{nRT} = nR$$

> 这正是热容差公式 $C_p-C_V=\alpha^2TV/\kappa_T$ 在 $\alpha=1/T$、$\kappa_T=1/p$ 下的特例（第 5 题）。**$\alpha/\kappa_T$ 形式是"可测量"版本，$(\partial p/\partial T)_V(\partial V/\partial T)_p$ 形式是"状态方程"版本，两者等价**——前者的价值在于 $\alpha$、$\kappa_T$ 都能直接实验测定（液体/固体也适用），后者只在有状态方程时才好用。

**15. 配分函数求平衡常数**

**为什么能求**：化学平衡条件是 $\sum_i \nu_i\mu_i = 0$。理想气体中单组分化学势可由配分函数给出（离域子 $\mu_i = -kT\ln(q_i/N_i)$），代入即得

$$\prod_i\left(\frac{N_i}{V}\right)^{\nu_i} = \prod_i\left(\frac{q_i}{V}\right)^{\nu_i}$$

再用 $N_i/V = p_i/(kT)$ 换成压强，并除以标准压 $p^\theta$ 化为无量纲：

$$K = \prod_i\left(\frac{p_i}{p^\theta}\right)^{\nu_i} = \left(\frac{kT}{p^\theta}\right)^{\Delta\nu}\prod_i\left(\frac{q_i}{V}\right)^{\nu_i}$$

若各 $q_i$ 按**摩尔口径**计算（$V$ 取 $V_m$、粒子数按 $N_A$ 计），上式中的 $kT$ 换成 $RT$，即讲义所列形式：

$$K = \frac{(q_{\text{产物}}/V)^{\nu_{\text{产物}}}}{(q_{\text{反应物}}/V)^{\nu_{\text{反应物}}}}\times\left(\frac{RT}{p^\theta}\right)^{\Delta\nu}$$

**适用条件（缺一不可）**：

| # | 条件 | 破坏后的后果 |
|:--:|:---|:---|
| 1 | 理想气体（无分子间相互作用） | 有作用时 $q$ 不能分解为单分子之积，须引入位形积分 |
| 2 | 独立粒子、能量可加 | 否则 $q\neq q^T q^R q^V q^E$，连乘失效 |
| 3 | 体系处于热平衡（Boltzmann 分布成立） | 非平衡体系根本无"平衡常数"可言 |
| 4 | 非简并（$q^T\gg N$） | 低温高密度须改用 Bose-Einstein / Fermi-Dirac 统计 |
| 5 | 各运动模式解耦（Born-Oppenheimer 近似） | 电子-振动强耦合时须整体处理，不能分别求 $q$ |

> 补充：各组分的 $q_i$ 必须使用**统一的能量零点**；若取自不同零点，上式还要再乘 $\exp(-\Delta\varepsilon_0/kT)$（$\Delta\varepsilon_0$ 为按计量数加权的零点能差）。

---

## 延伸阅读

- [[03-知识点/决赛要求/物理化学深化/Boltzmann统计初步]] — 配分函数/统计熵完整 KP（含 2 道例题解答）
- [[03-知识点/决赛要求/物理化学深化/麦克斯韦关系式]] — Maxwell 四条 + 记忆口诀 + 热容差 + Joule-Thomson
- [[03-知识点/决赛要求/物理化学深化/热力学四大基本方程]]、[[03-知识点/决赛要求/物理化学深化/吉布斯-亥姆霍兹方程]]
- [[07-资料提炼/书籍提炼/提炼-Atkins物理化学-主题2-3-热力学定律]] — Maxwell/Gibbs-Helmholtz 提炼
- [[07-资料提炼/书籍提炼/提炼-Atkins物理化学-主题13-14-统计热力学与分子相互作用]] — 统计热力学提炼
- [[04-课件/学生讲义/化学原理/物化综合计算-超级充实版（自学完整）]] — 4-7 物化线姊妹讲义（§〇 化学势/van't Hoff 中段）
- Atkins《Physical Chemistry》第11版 主题 2-3、13A-13E；傅献彩《物理化学》下册 §统计热力学

---


