---
title: Gaussian 完整指南
type: 工具指南
tool: Gaussian
purpose: 量子化学计算从入门到进阶
created: 2026-08-02
updated: 2026-08-02
tags: [可视化, Gaussian, 量子化学, 完整指南]
---

# Gaussian 完整指南

> 本指南合并了 Gaussian 的所有使用内容，从入门到进阶，一页掌握。

---

## 1. Gaussian 简介

### 1.1 什么是 Gaussian？

Gaussian 是量子化学计算软件，可以：
- 计算分子能量
- 优化分子结构
- 计算振动频率
- 分析分子轨道
- 预测光谱

### 1.2 何时需要 Gaussian？

| 场景 | 是否需要 | 替代方案 |
|:-----|:---------|:---------|
| 日常教学图片 | ❌ | Avogadro / VESTA |
| 精确分子轨道 | ✅ | — |
| 反应能垒 | ✅ | — |
| 光谱预测 | ✅ | — |

---

## 2. Avogadro + Gaussian 工作流

### 步骤1：Avogadro 构建分子

```
1. 打开 Avogadro
2. 构建分子（Draw 工具或 SMILES）
3. 力场优化
```

### 步骤2：生成 Gaussian 输入文件

```
1. Extensions → Quantum Chemistry → Set up Calculation
2. 选择方法：B3LYP
3. 选择基组：6-31G*
4. 选择计算类型：Optimization
5. 生成输入文件 → 保存为 .gjf
```

### 步骤3：运行 Gaussian

```bash
g16 < input.gjf > output.log
```

### 步骤4：读取结果

```
1. 打开 Avogadro
2. Extensions → Quantum Chemistry → Open Result File
3. 选择 .log 文件
4. 查看分子轨道、振动模式
```

---

## 3. 常用计算类型

### 3.1 几何优化（Opt）

```
#p B3LYP/6-31G* Opt

Title

0 1
O  0.000000  0.000000  0.117370
H  0.000000  0.756950 -0.469483
H  0.000000 -0.756950 -0.469483
```

### 3.2 频率计算（Freq）

```
#p B3LYP/6-31G* Freq

Title

0 1
O  0.000000  0.000000  0.117370
H  0.000000  0.756950 -0.469483
H  0.000000 -0.756950 -0.469483
```

### 3.3 单点能（SP）

```
#p B3LYP/6-311G** SP

Title

0 1
O  0.000000  0.000000  0.117370
H  0.000000  0.756950 -0.469483
H  0.000000 -0.756950 -0.469483
```

### 3.4 分子轨道

```
#p B3LYP/6-31G* Pop=Full

Title

0 1
O  0.000000  0.000000  0.117370
H  0.000000  0.756950 -0.469483
H  0.000000 -0.756950 -0.469483
```

---

## 4. 方法和基组

### 4.1 常用方法

| 方法 | 精度 | 速度 | 推荐 |
|:-----|:-----|:-----|:-----|
| HF | 低 | 快 | 教学演示 |
| B3LYP | 中 | 中 | 日常计算 |
| MP2 | 高 | 慢 | 高精度 |

### 4.2 常用基组

| 基组 | 大小 | 推荐 |
|:-----|:-----|:-----|
| STO-3G | 小 | 快速测试 |
| 6-31G* | 中 | 日常计算 |
| 6-311G** | 大 | 高精度 |

### 4.3 推荐组合

| 场景 | 推荐 |
|:-----|:-----|
| 教学演示 | HF/STO-3G |
| 日常计算 | B3LYP/6-31G* |
| 高精度 | B3LYP/6-311G** |

---

## 5. 输入文件格式

### 5.1 标准格式

```
%mem=4GB
%nproc=4
#p B3LYP/6-31G* Opt

Title

0 1
Atom1  x  y  z
Atom2  x  y  z
```

### 5.2 关键词

| 关键词 | 用途 |
|:------|:-----|
| `%mem=4GB` | 内存 |
| `%nproc=4` | CPU核心数 |
| `Opt` | 几何优化 |
| `Freq` | 频率计算 |
| `SP` | 单点能 |
| `Pop=Full` | 分子轨道 |

---

## 6. 输出文件分析

### 6.1 关键信息

| 信息 | 位置 |
|:-----|:-----|
| 优化后坐标 | "Standard orientation" |
| 能量 | "SCF Done" |
| 频率 | "Frequencies" |
| 分子轨道 | "Molecular Orbital Coefficients" |

### 6.2 常见错误

| 错误 | 解决方案 |
|:-----|:---------|
| SCF 未收敛 | 增加迭代次数 |
| 优化失败 | 调整初始结构 |
| 内存不足 | 增加 %mem |

---

## 7. 教学应用

### 7.1 比较 H₂O 和 H₂S

```
1. 分别计算
2. 比较 HOMO/LUMO 能量
3. 讨论电负性影响
```

### 7.2 NH₃ 振动频率

```
1. 频率计算
2. 查看红外光谱
3. 识别振动模式
```

### 7.3 苯的共振能

```
1. 计算苯能量
2. 计算假想环己三烯能量
3. 比较差值
```

---

## 8. 与其他工具配合

### 工作流1：Avogadro → Gaussian → Avogadro

```
Avogadro 构建 → Gaussian 计算 → Avogadro 可视化
```

### 工作流2：Gaussian → Blender

```
Gaussian 输出 → 提取坐标 → 导出 XYZ → Blender 渲染
```

---

## 9. 快速参考

### 常用命令

| 命令 | 用途 |
|:-----|:-----|
| `g16` | 运行 Gaussian 16 |
| `g09` | 运行 Gaussian 09 |

### 输出文件

| 文件 | 内容 |
|:-----|:-----|
| .log | 文本输出 |
| .chk | 检查点文件 |
| .fchk | 格式化检查点 |

---

## 参考资源

| 资源 | 链接 |
|:-----|:-----|
| Gaussian 官网 | [gaussian.com](https://gaussian.com/) |
| Avogadro Gaussian 集成 | [avogadro.cc/wiki/Gaussian](https://avogadro.cc/wiki/Gaussian) |
| Computational Chemistry Wiki | [ccl.net/chemistry](http://www.ccl.net/chemistry/) |
