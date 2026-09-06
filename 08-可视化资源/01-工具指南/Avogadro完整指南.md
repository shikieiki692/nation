---
title: Avogadro 完整指南
type: 工具指南
tool: Avogadro 2
purpose: 分子构建、力场优化、构象分析、格式导出
created: 2026-08-02
updated: 2026-08-02
tags: [可视化, Avogadro, 分子建模, 完整指南]
---

# Avogadro 完整指南

> 本指南合并了 Avogadro 的所有使用内容，从入门到进阶，一页掌握。

---

## 1. 快速入门

### 1.1 安装
- 下载：[avogadro.cc](https://avogadro.cc/)
- 支持 Windows / macOS / Linux

### 1.2 基础操作

| 操作 | 快捷键 | 说明 |
|:-----|:-------|:-----|
| Draw 工具 | D | 构建分子 |
| Select 工具 | S | 选择原子 |
| Measure 工具 | M | 测量键长/键角 |
| 力场优化 | Extensions → Molecular Mechanics | 优化结构 |

---

## 3. 分子构建

### 3.1 手动绘制

```
1. 选择 Draw 工具 (D)
2. 点击空白处 → 添加原子（默认碳）
3. 点击已有原子 → 添加键
4. 数字键切换原子类型：
   - 6 = C, 7 = N, 8 = O, 16 = S, 15 = P
   - 9 = F, 17 = Cl, 35 = Br, 53 = I
```

### 3.2 SMILES 输入

```
1. Edit → Input Molecule → SMILES
2. 输入 SMILES 字符串
3. 点击 OK → 自动生成3D结构
```

### 3.3 常用 SMILES

| 分子 | SMILES | 分子 | SMILES |
|:-----|:-------|:-----|:-------|
| 水 | O | 甲烷 | C |
| 氨 | N | 苯 | c1ccccc1 |
| 乙醇 | CCO | 丙酮 | CC(=O)C |
| 乙酸 | CC(=O)O | 甲苯 | Cc1ccccc1 |
| 乙烯 | C=C | 乙炔 | C#C |
| 环己烷 | C1CCCCC1 | 苯酚 | Oc1ccccc1 |

### 3.4 有机分子构建示例

#### 烷烃

| 分子 | SMILES | 结构特点 |
|:-----|:-------|:---------|
| 甲烷 | C | 正四面体 |
| 乙烷 | CC | sp³杂化 |
| 丙烷 | CCC | 锯齿形 |
| 环己烷 | C1CCCCC1 | 椅式构象 |

#### 烯烃和炔烃

| 分子 | SMILES | 结构特点 |
|:-----|:-------|:---------|
| 乙烯 | C=C | 平面、sp²杂化 |
| 丙烯 | CC=C | 平面 |
| 乙炔 | C#C | 直线、sp杂化 |
| 丙炔 | CC#C | 直线 |

#### 芳香烃

| 分子 | SMILES | 结构特点 |
|:-----|:-------|:---------|
| 苯 | c1ccccc1 | 平面、离域π键 |
| 甲苯 | Cc1ccccc1 | 甲基取代 |
| 萘 | c1ccc2ccccc2c1 | 稠环芳香 |
| 苯酚 | Oc1ccccc1 | 羟基取代 |

#### 醇、醚、醛、酮

| 分子 | SMILES | 官能团 |
|:-----|:-------|:-------|
| 甲醇 | CO | 醇 |
| 乙醇 | CCO | 醇 |
| 二甲醚 | COC | 醚 |
| 甲醛 | C=O | 醛 |
| 乙醛 | CC=O | 醛 |
| 丙酮 | CC(=O)C | 酮 |

#### 羧酸和酯

| 分子 | SMILES | 官能团 |
|:-----|:-------|:-------|
| 甲酸 | C(=O)O | 羧酸 |
| 乙酸 | CC(=O)O | 羧酸 |
| 甲酸甲酯 | COC=O | 酯 |
| 乙酸乙酯 | CCOC(=O)C | 酯 |

#### 含氮化合物

| 分子 | SMILES | 官能团 |
|:-----|:-------|:-------|
| 甲胺 | CN | 胺 |
| 乙胺 | CCN | 胺 |
| 苯胺 | Nc1ccccc1 | 芳香胺 |
| 吡啶 | c1ccncc1 | 杂环 |
| 嘧啶 | c1ccncn1 | 杂环 |

---

## 4. 力场优化

### 3.1 快速优化

```
Extensions → Molecular Mechanics → Quick Optimization
```

### 3.2 选择力场

| 力场 | 适用范围 | 推荐 |
|:-----|:---------|:-----|
| UFF | 通用，支持所有元素 | ⭐⭐⭐⭐ |
| MMFF94 | 有机小分子 | ⭐⭐⭐⭐⭐ |
| GAFF | 有机小分子 | ⭐⭐⭐⭐ |

### 3.3 优化步骤

```
1. Extensions → Molecular Mechanics
2. 选择力场
3. 设置 Max Steps: 500-1000
4. 点击 Optimize Geometry
5. 观察能量变化，收敛后停止
```

---

## 4. 测量工具

### 4.1 测量键长

```
1. 选择 Measure 工具 (M)
2. 点击两个原子
3. 显示键长（Å）
```

### 4.2 测量键角

```
1. 选择 Measure 工具 (M)
2. 依次点击三个原子
3. 显示键角（°）
```

### 4.3 测量二面角

```
1. 选择 Measure 工具 (M)
2. 依次点击四个原子
3. 显示二面角（°）
```

---

## 5. 构象分析

### 5.1 乙烷构象

```
1. 构建乙烷：SMILES → "CC"
2. 力场优化
3. Measure 工具 → 点击 H-C-C-H
4. 记录二面角和能量
5. 旋转 C-C 键，重复测量
```

**预期数据**：
| 二面角 | 构象 | 能量 |
|:-------|:-----|:-----|
| 0° | 重叠式 | ~12 kJ/mol |
| 60° | 邻交叉式 | ~4 kJ/mol |
| 180° | 反交叉式 | 0 kJ/mol |

### 5.2 环己烷构象

```
1. 构建环己烷：SMILES → "C1CCCCC1"
2. 力场优化 → 椅式构象
3. Extensions → Conformer Search
4. 比较椅式 vs 船式
```

---

## 6. 格式导出

### 6.1 导出选项

| 格式 | 用途 | 导出方法 |
|:-----|:-----|:---------|
| XYZ | 通用格式，VESTA可用 | File → Save As → XYZ |
| PDB | Blender可用 | File → Save As → PDB |
| CIF | VESTA可用 | File → Save As → CIF |
| MOL | 化学软件通用 | File → Save As → MOL |

### 6.2 推荐工作流

```
Avogadro 构建 → 力场优化 → 导出 XYZ → VESTA 可视化
```

---

## 7. 教学应用

### 7.1 VSEPR 模型验证

```
1. 构建 H₂O, NH₃, CH₄, BF₃, SF₆
2. 力场优化
3. Measure 工具测量键角
4. 与 VSEPR 预测对比
```

### 7.2 杂化轨道比较

```
1. 构建乙烷(sp³), 乙烯(sp²), 乙炔(sp)
2. 力场优化
3. 测量键角和键长
4. 比较 C-H 键长差异
```

### 7.3 配位化合物

```
1. 构建 [Co(NH₃)₆]³⁺
2. 手动调整 Co-N 距离
3. 力场优化
4. 测量键角
```

### 7.4 手性分子

```
1. 构建乳酸的两种对映体
2. 力场优化
3. 比较镜像关系
4. 测量二面角确定 R/S 构型
```

---

## 8. 量子化学接口

### 8.1 生成输入文件

**支持的量子化学软件**：

| 软件 | 类型 | 推荐度 |
|:-----|:-----|:-------|
| Gaussian | 商业 | ⭐⭐⭐⭐⭐ |
| ORCA | 免费学术 | ⭐⭐⭐⭐⭐ |
| GAMESS | 免费 | ⭐⭐⭐⭐ |
| NWChem | 免费 | ⭐⭐⭐⭐ |
| Q-Chem | 商业 | ⭐⭐⭐ |
| MOPAC | 免费 | ⭐⭐⭐ |

### 8.2 Gaussian 输入

```
1. Extensions → Quantum Chemistry → Set up Calculation
2. 选择 Gaussian
3. 设置方法（如 B3LYP）和基组（如 6-31G*）
4. 选择计算类型（Opt, Freq, SP 等）
5. 保存 .gjf 文件
```

### 8.3 ORCA 输入

```
1. Extensions → Quantum Chemistry → Set up Calculation
2. 选择 ORCA
3. 设置方法和基组
4. 保存 .inp 文件
```

### 8.4 计算类型

| 类型 | 关键词 | 用途 |
|:-----|:-------|:-----|
| 几何优化 | Opt | 优化分子结构 |
| 频率计算 | Freq | 红外光谱、热力学校正 |
| 单点能 | SP | 精确能量 |
| 过渡态 | TS | 反应过渡态 |
| 分子轨道 | Pop=Full | HOMO/LUMO |

---

## 9. 轨道可视化

### 9.1 显示分子轨道

**前提**：需要先进行量子化学计算

```
1. 完成 Gaussian/ORCA 计算
2. Extensions → Quantum Chemistry → Open Result File
3. 选择输出文件
4. View → Molecular Orbitals
5. 选择轨道（如 HOMO, LUMO）
6. 调整等值面数值
```

### 9.2 轨道显示设置

| 设置项 | 说明 | 推荐值 |
|:-------|:-----|:-------|
| Isovalue | 等值面数值 | 0.02-0.05 |
| Opacity | 透明度 | 50-80% |
| Positive Color | 正相位颜色 | 蓝色 |
| Negative Color | 负相位颜色 | 红色 |

### 9.3 常用轨道

| 轨道 | 说明 | 用途 |
|:-----|:-----|:-----|
| HOMO | 最高占据轨道 | 亲核反应位点 |
| LUMO | 最低未占轨道 | 亲电反应位点 |
| HOMO-1 | 次高占据轨道 | 电子结构分析 |
| LUMO+1 | 次低未占轨道 | 电子结构分析 |

---

## 10. 对称性分析

### 10.1 识别点群

```
1. Extensions → Symmetry → Analyze Symmetry
2. 程序自动识别分子点群
3. 显示对称元素
```

### 10.2 常见点群

| 点群 | 对称元素 | 示例分子 |
|:-----|:---------|:---------|
| C₁ | 无 | CHFClBr |
| C₂ | C₂ | H₂O₂ |
| C₂ᵥ | C₂, 2σᵥ | H₂O, NH₃ |
| C₃ᵥ | C₃, 3σᵥ | NH₃, CH₃Cl |
| D₂ₕ | C₂, 2C₂, σₕ | C₂H₄ |
| D₃ₕ | C₃, 3C₂, σₕ | BF₃ |
| Tₐ | 4C₃, 3C₂, 3S₄, 6σₐ | CH₄ |
| Oₕ | 4C₃, 3C₄, 3C₂, 6C₂', 3σₕ, 6σₐ, i | SF₆ |

### 10.3 对称性应用

- 简化量子化学计算
- 预测IR/Raman活性
- 分析分子轨道对称性
- 判断手性

---

## 11. 表面可视化

### 11.1 电子密度表面

```
1. 构建分子
2. View → Display Style → Surface
3. Surface Type: Electron Density
4. 绑定到: Molecular Orbital (或 Density)
5. 调整 Iso Value (0.001-0.01)
```

### 11.2 静电势表面

```
1. 构建分子
2. View → Display Style → Surface
3. Surface Type: Electrostatic Potential
4. 绑定到: Electron Density
5. Color: 按静电势着色（红=负，蓝=正）
```

**教学应用**：

| 分子 | 静电势特征 | 教学要点 |
|:-----|:-----------|:---------|
| H₂O | O 端负，H 端正 | 极性分子 |
| HF | F 端负，H 端正 | 键极性 |
| NH₃ | N 端负 | 孤对电子 |
| CO₂ | 对称分布 | 非极性分子 |
| CH₄ | 均匀分布 | 非极性分子 |

### 11.3 分子轨道表面

```
1. 构建分子
2. View → Display Style → Surface
3. Surface Type: Molecular Orbital
4. 选择轨道编号 (HOMO=Highest Occupied)
5. 调整 Iso Value
```

---

## 12. 键级和共振结构

### 12.1 查看键级

```
1. 构建分子
2. Edit → Edit Data → Bonds
3. 查看每个键的键级
```

### 12.2 苯的共振结构

```
1. 构建苯：SMILES → "c1ccccc1"
2. 查看键级 → 所有C-C键级约为1.5
3. 说明：苯的π电子是离域的
```

### 12.3 碳酸根的共振结构

```
1. 构建CO₃²⁻
2. 查看键级 → 所有C-O键级约为1.33
3. 说明：碳酸根有3个共振结构
```

---

## 13. 分子性质计算

### 13.1 偶极矩

```
1. 构建分子
2. Extensions → Molecular Mechanics → Calculate Properties
3. 查看偶极矩
```

**常见分子偶极矩**：

| 分子 | 偶极矩(D) | 极性 |
|:-----|:----------|:-----|
| H₂O | 1.85 | 极性 |
| CO₂ | 0 | 非极性 |
| NH₃ | 1.47 | 极性 |
| CH₄ | 0 | 非极性 |
| HF | 1.82 | 极性 |

### 13.2 电荷分布

```
1. 构建分子
2. Extensions → Molecular Mechanics → Calculate Charges
3. 查看原子电荷
```

---

## 14. 配合物深入分析

### 14.1 配位键的形成

```
1. 构建 [Co(NH₃)₆]³⁺
2. 手动调整 Co-N 距离
3. 力场优化
4. 测量键长和键角
```

### 14.2 比较不同配位数

```
1. 构建四配位配合物（四面体/平面正方形）
2. 构建六配位配合物（八面体）
3. 比较键长、键角
```

### 14.3 晶体场理论可视化

```
1. 构建八面体配合物
2. 测量键角（90°/180°）
3. 说明d轨道分裂
```

---

## 15. 显示设置

### 11.1 显示样式

**位置**：View → Display Style

| 样式 | 说明 | 适用场景 |
|:-----|:-----|:---------|
| Ball and Stick | 球棍模型 | 通用（推荐） |
| Spacefill | 空间填充 | 分子体积 |
| Wireframe | 线框 | 简单结构 |
| Stick | 棒状 | 简单结构 |
| Custom | 自定义 | 特殊需求 |

### 11.2 颜色设置

**CPK配色**（默认）：

| 元素 | 颜色 |
|:-----|:-----|
| H | 白色 |
| C | 灰色 |
| N | 蓝色 |
| O | 红色 |
| S | 黄色 |
| P | 橙色 |
| F, Cl, Br, I | 绿色系列 |

### 11.3 背景颜色

**位置**：View → Background Color

- White：白色背景（推荐用于导出）
- Black：黑色背景
- Custom：自定义颜色

---

## 12. 插件系统

### 12.1 常用插件

| 插件 | 功能 | 用途 |
|:-----|:-----|:-----|
| Open Babel | 格式转换、力场 | 增强文件支持 |
| Orbital Viewer | 轨道可视化 | 显示分子轨道 |
| Molecular Mechanics | 力场优化 | 结构优化 |
| Quantum Chemistry | 量子化学接口 | 生成输入文件 |

### 12.2 管理插件

```
Tools → Plugin Manager
- 查看已安装插件
- 启用/禁用插件
- 安装新插件
```

---

## 13. 与其他工具配合

### 13.1 与VESTA配合

```
Avogadro 构建 → 导出 XYZ → VESTA 打开
```

### 13.2 与Blender配合

```
Avogadro 构建 → 导出 PDB → Blender + Molecular Nodes 导入
```

### 13.3 与Gaussian配合

```
Avogadro 构建 → Extensions → Quantum Chemistry → 生成 .gjf → Gaussian 计算
```

### 13.4 与ORCA配合

```
Avogadro 构建 → Extensions → Quantum Chemistry → 生成 .inp → ORCA 计算
```

---

## 14. 常见问题

| 问题 | 解决方案 |
|:-----|:---------|
| 力场优化失败 | 换用力场（UFF/MMFF94） |
| 结构不合理 | 手动调整后再优化 |
| 导出文件异常 | 检查原子坐标 |
| 测量不准确 | 确保选择了正确的原子 |
| 轨道不显示 | 检查计算是否完成 |
| 对称性识别错误 | 调整对称性容差 |

---

## 15. 参考资源

| 资源 | 链接 |
|:-----|:-----|
| Avogadro 官网 | [avogadro.cc](https://avogadro.cc/) |
| Avogadro 文档 | [doc.avogadro.cc](https://doc.avogadro.cc/) |
| Avogadro 教程 | [avogadro.cc/wiki/Tutorials](https://avogadro.cc/wiki/Tutorials) |
| Avogadro 2 | [two.avogadro.cc](https://two.avogadro.cc/) |
| OpenChemistry | [openchemistry.org](https://openchemistry.org/) |
