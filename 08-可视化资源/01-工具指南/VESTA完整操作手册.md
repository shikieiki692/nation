---
title: VESTA完整操作手册
type: 操作手册
purpose: VESTA软件所有功能的详细操作指南
created: 2026-08-02
updated: 2026-08-02
tags: [VESTA, 操作手册, 晶体结构, 可视化, 教程]
version: 1.0
---

# VESTA完整操作手册

> VESTA（Visualization for Electronic and STructural Analysis）是一款免费的3D晶体结构可视化软件。
> 本手册覆盖VESTA的所有核心功能，适合化学竞赛教学使用。

---

## 一、VESTA简介

### 1.1 什么是VESTA

VESTA是由日本科学家Koichi Momma和Fujio Izumi开发的免费3D可视化软件，主要用于：
- 晶体结构可视化
- 电子密度显示
- 磁结构可视化
- 晶体形态分析

### 1.2 下载与安装

**官方下载地址**：https://jp-minerals.org/vesta/

**安装步骤**：
1. 下载对应操作系统的版本（Windows/Mac/Linux）
2. 解压到任意目录
3. 双击 `VESTA.exe` 启动

### 1.3 界面概览

```
VESTA界面布局：
┌─────────────────────────────────────────────┐
│  菜单栏：File, Edit, Utilities, Style, Help │
├─────────────────────────────────────────────┤
│  工具栏：常用操作快捷按钮                    │
├──────────────┬──────────────────────────────┤
│  对象面板    │                              │
│  - 原子      │      3D视图窗口              │
│  - 键        │      （显示晶体结构）         │
│  - 多面体    │                              │
│  - 晶面      │                              │
├──────────────┴──────────────────────────────┤
│  状态栏：显示当前操作信息                    │
└─────────────────────────────────────────────┘
```

---

## 二、文件操作

### 2.1 打开文件

#### 方法1：菜单打开
```
File → Open → 选择CIF文件 → 打开
```

#### 方法2：拖拽打开
直接将CIF文件拖入VESTA窗口

#### 方法3：最近文件
```
File → Open Recent → 选择最近打开的文件
```

### 2.2 支持的文件格式

| 格式 | 扩展名 | 说明 |
|:-----|:-------|:-----|
| CIF | .cif | 晶体学信息文件（最常用） |
| XYZ | .xyz | 简单分子坐标格式 |
| POSCAR | POSCAR/CONTCAR | VASP输入/输出文件 |
| MOL | .mol | MDL分子文件 |
| SHELX | .ins, .res | SHELX格式 |
| Gaussian | .gjf, .com, .log | Gaussian输入/输出 |
| Cube | .cube | 体积数据文件 |
| XSF | .xsf | XCrySDen格式 |

### 2.3 保存文件

```
File → Save As → 选择格式 → 保存
```

**保存格式**：
- `.vesta`：VESTA原生格式（保留所有设置）
- `.cif`：导出为CIF格式

### 2.4 导入数据

```
File → Import Data → 选择文件类型 → 选择文件 → 导入
```

**导入选项**：
- 作为新结构导入
- 合并到当前结构
- 替换当前结构

---

## 三、基本操作

### 3.1 视图操作

| 操作 | 方法 | 说明 |
|:-----|:-----|:-----|
| 旋转 | 鼠标左键拖动 | 旋转晶体结构 |
| 平移 | 鼠标中键拖动 | 平移视图 |
| 缩放 | 鼠标滚轮 | 放大/缩小 |
| 重置视角 | 双击左键 | 恢复默认视角 |
| 适合窗口 | Home键 | 自动调整大小 |

### 3.2 快捷键

| 快捷键 | 功能 |
|:-------|:-----|
| Ctrl+O | 打开文件 |
| Ctrl+S | 保存文件 |
| Ctrl+Z | 撤销 |
| Ctrl+Y | 重做 |
| Ctrl+B | 编辑键 |
| Delete | 删除选中对象 |
| Home | 适合窗口 |
| F5 | 刷新显示 |

### 3.3 鼠标操作

| 按键 | 操作 | 功能 |
|:-----|:-----|:-----|
| 左键 | 拖动 | 旋转 |
| 中键 | 拖动 | 平移 |
| 右键 | 拖动 | 缩放 |
| 滚轮 | 滚动 | 缩放 |
| 左键 | 双击 | 重置视角 |

---

## 四、编辑功能

### 4.1 Edit Data（编辑数据）

```
Edit → Edit Data → 选择编辑内容
```

#### 4.1.1 Unit Cell（晶胞参数）

**位置**：Edit → Edit Data → Unit Cell

**功能**：
- 查看和编辑晶胞参数（a, b, c, α, β, γ）
- 设置空间群
- 转换晶系

**操作步骤**：
1. 点击 Edit → Edit Data → Unit Cell
2. 查看晶胞参数
3. 修改参数（如需要）
4. 点击 OK 保存

#### 4.1.2 Atoms（原子位置）

**位置**：Edit → Edit Data → Atoms

**功能**：
- 查看原子坐标（分数坐标/笛卡尔坐标）
- 添加/删除原子
- 编辑原子属性

**操作步骤**：
1. 点击 Edit → Edit Data → Atoms
2. 查看原子列表
3. 双击编辑原子坐标
4. 点击 Add 添加新原子
5. 点击 Delete 删除原子

#### 4.1.3 Bonds（键）

**位置**：Edit → Edit Data → Bonds

**功能**：
- 定义原子间的键
- 设置键长范围
- 添加/删除键

**操作步骤**：
1. 点击 Edit → Edit Data → Bonds
2. 点击 Add 添加新键
3. 选择原子对
4. 设置键长范围（Min/Max）
5. 点击 OK 保存

**常用键长范围**：
| 键类型 | 典型键长(Å) | 建议范围 |
|:-------|:-----------|:---------|
| C-C | 1.54 | 1.2-1.8 |
| C=O | 1.23 | 1.0-1.5 |
| Na-Cl | 2.82 | 2.5-3.2 |
| Fe-O | 2.00 | 1.8-2.5 |

#### 4.1.4 Polyhedra（多面体）

**位置**：Edit → Edit Data → Polyhedra

**功能**：
- 定义配位多面体
- 选择中心原子和配位原子
- 设置多面体样式

**操作步骤**：
1. 点击 Edit → Edit Data → Polyhedra
2. 点击 Add 添加新多面体
3. 选择中心原子（如 Na⁺）
4. 选择配位原子（如 Cl⁻）
5. 设置多面体颜色和透明度
6. 点击 OK 保存

#### 4.1.5 Lattice Planes（晶面）

**位置**：Edit → Edit Data → Lattice Planes

**功能**：
- 添加晶面
- 设置密勒指数 (h k l)
- 调整晶面样式

**操作步骤**：
1. 点击 Edit → Edit Data → Lattice Planes
2. 点击 New 添加新晶面
3. 输入密勒指数（如 1 0 0）
4. 设置颜色和透明度
5. 设置显示范围
6. 点击 OK 保存

**常见晶面**：
| 晶面 | 密勒指数 | 用途 |
|:-----|:---------|:-----|
| (100) | 1 0 0 | 观察面心立方结构 |
| (110) | 1 1 0 | 观察体心立方结构 |
| (111) | 1 1 1 | 观察密排面 |
| (001) | 0 0 1 | 观察层状结构 |

#### 4.1.6 Vectors（矢量）

**位置**：Edit → Edit Data → Vectors

**功能**：
- 添加矢量显示（如磁矩）
- 设置矢量方向和大小
- 调整矢量样式

**操作步骤**：
1. 点击 Edit → Edit Data → Vectors
2. 点击 Add 添加新矢量
3. 选择原子
4. 输入矢量分量 (x, y, z)
5. 设置矢量颜色和长度
6. 点击 OK 保存

### 4.2 Style（样式设置）

#### 4.2.1 显示样式

**位置**：Edit → Style

**样式选项**：

| 样式 | 说明 | 适用场景 |
|:-----|:-----|:---------|
| Ball-and-stick | 球棍模型 | 分子结构、配合物 |
| Space-filling | 空间填充模型 | 分子体积、堆积 |
| Polyhedral | 多面体模型 | 配位环境、晶体结构 |
| Wireframe | 线框模型 | 简单显示 |
| Polyhedra & Ball-and-stick | 复合显示 | 复杂结构 |

**操作步骤**：
1. 点击 Edit → Style
2. 选择显示样式
3. 调整参数（如原子半径、键半径）
4. 点击 OK 应用

#### 4.2.2 原子样式

**位置**：Edit → Style → Atoms

**设置选项**：
- **Radius**：原子半径
- **Color**：原子颜色
- **Transparency**：透明度
- **Display**：显示/隐藏

**CPK配色标准**：
| 元素 | 颜色 | RGB值 |
|:-----|:-----|:------|
| H | 白色 | 255, 255, 255 |
| C | 灰色 | 128, 128, 128 |
| N | 蓝色 | 48, 80, 248 |
| O | 红色 | 255, 13, 13 |
| S | 黄色 | 255, 255, 48 |
| P | 橙色 | 255, 128, 0 |
| Cl | 绿色 | 31, 240, 31 |
| Fe | 棕色 | 224, 102, 51 |
| Na | 紫色 | 171, 92, 255 |
| Ca | 绿色 | 61, 255, 0 |

#### 4.2.3 键样式

**位置**：Edit → Style → Bonds

**设置选项**：
- **Radius**：键半径
- **Color**：键颜色
- **Display**：显示/隐藏

#### 4.2.4 多面体样式

**位置**：Edit → Style → Polyhedra

**设置选项**：
- **Color**：多面体颜色
- **Opacity**：不透明度
- **Edge**：边缘显示
- **Transparency**：透明度

### 4.3 Boundary（边界设置）

**位置**：Edit → Boundary

**功能**：
- 设置显示范围
- 创建超胞
- 控制显示的晶胞数量

**操作步骤**：
1. 点击 Edit → Boundary
2. 设置各轴的范围（如 [-1, 2]）
3. 设置重复次数
4. 点击 OK 应用

**示例**：
- 显示1个晶胞：a [0, 1], b [0, 1], c [0, 1]
- 显示2×2×2超胞：a [0, 2], b [0, 2], c [0, 2]
- 显示负方向：a [-1, 1], b [0, 1], c [0, 1]

### 4.4 Element Colors（元素颜色）

**位置**：Edit → Element Colors

**功能**：
- 自定义元素颜色
- 恢复默认颜色
- 保存颜色方案

### 4.5 Move Objects（移动对象）

**位置**：Edit → Move Objects

#### 4.5.1 Parallel to Viewing Direction（沿视线方向移动）

**位置**：Edit → Move Objects → Parallel to Viewing Direction

**功能**：
- 沿当前视线方向移动对象
- 用于调整原子或结构的位置

#### 4.5.2 Along the X/Y/Z Axis（沿坐标轴移动）

**位置**：Edit → Move Objects → Along the X/Y/Z Axis

**功能**：
- 沿X、Y或Z轴移动对象
- 精确控制移动方向

### 4.6 Preferences（偏好设置）

**位置**：Edit → Preferences

**功能**：
- 设置VESTA的全局参数
- 配置显示、行为、路径等

**主要设置项**：

#### 4.6.1 General（常规）

| 设置项 | 说明 | 默认值 |
|:-------|:-----|:-------|
| Language | 界面语言 | English |
| Recent Files | 最近文件数量 | 10 |
| Auto Save | 自动保存 | 关闭 |

#### 4.6.2 Display（显示）

| 设置项 | 说明 | 默认值 |
|:-------|:-----|:-------|
| Background Color | 背景颜色 | White |
| Rendering Quality | 渲染质量 | High |
| Anti-aliasing | 抗锯齿 | 开启 |

#### 4.6.3 Bonds（键）

| 设置项 | 说明 | 默认值 |
|:-------|:-----|:-------|
| Default Bond Radius | 默认键半径 | 0.15 |
| Max Bond Length | 最大键长 | 3.0 Å |

#### 4.6.4 Atoms（原子）

| 设置项 | 说明 | 默认值 |
|:-------|:-----|:-------|
| Max Radius | 最大原子半径 | 1.5 Å |
| Default Style | 默认样式 | Ball-and-stick |

---

## 五、显示控制

### 5.1 Objects面板

**位置**：左侧边栏

**标签页**：
- **Atoms**：原子显示控制
- **Bonds**：键显示控制
- **Polyhedra**：多面体显示控制
- **Lattice Planes**：晶面显示控制
- **Vectors**：矢量显示控制

**操作**：
- 点击眼睛图标 👁️ 切换显示/隐藏
- 双击编辑属性
- 拖动调整顺序

### 5.2 显示选项

#### 5.2.1 Style菜单

**位置**：Style菜单

**样式选项**：

| 样式 | 说明 | 适用场景 |
|:-----|:-----|:---------|
| Ball-and-stick | 球棍模型 | 分子结构、配合物 |
| Space-filling | 空间填充模型（CPK） | 分子体积、堆积 |
| Polyhedral | 多面体模型 | 配位环境、晶体结构 |
| Wireframe | 线框模型 | 简单显示 |
| Stick | 棒状模型 | 简单结构 |
| Ball-and-stick & Polyhedra | 球棍+多面体复合 | 复杂结构 |

**操作步骤**：
1. 点击 Style 菜单
2. 选择显示样式
3. 调整参数（如原子半径、键半径）
4. 应用

#### 5.2.2 单位晶胞

**位置**：Style → Unit Cell

**选项**：
- 显示/隐藏晶胞边框
- 设置晶胞边框颜色
- 设置边框宽度
- 显示/隐藏晶轴

#### 5.2.3 原子标签

**位置**：Style → Labels

**选项**：
- 显示/隐藏原子标签
- 设置标签样式（元素符号、原子序号等）
- 设置标签大小
- 设置标签颜色

#### 5.2.4 对称操作

**位置**：Style → Symmetry

**选项**：
- 显示对称元素（旋转轴、镜面等）
- 显示对称操作
- 显示空间群符号
- 显示Wyckoff位置

#### 5.2.5 晶轴

**位置**：Style → Axes

**选项**：
- 显示/隐藏晶轴
- 设置晶轴颜色
- 设置晶轴长度
- 标注晶轴方向（a, b, c）

#### 5.2.6 原点

**位置**：Style → Origin

**选项**：
- 设置原点位置
- 移动原点到指定原子

#### 5.2.7 投影

**位置**：Style → Projection

**选项**：
- 透视投影（Perspective）
- 正交投影（Orthographic）

#### 5.2.8 渲染

**位置**：Style → Rendering

**选项**：
- 渲染质量（Low/Medium/High）
- 抗锯齿（Anti-aliasing）
- 光照设置

### 5.3 视图控制

#### 5.3.1 旋转

**方法1：鼠标拖动**
- 左键拖动：自由旋转
- Shift+左键：绕垂直轴旋转
- Ctrl+左键：绕水平轴旋转

**方法2：菜单旋转**
```
Style → Rotation → 输入旋转角度
```

#### 5.3.2 视角设置

**标准视角**：
```
Style → Rotation → Standard Orientations
```

**常用视角**：
| 视角 | 说明 | 用途 |
|:-----|:-----|:-----|
| [001] | 沿c轴 | 观察ab面 |
| [010] | 沿b轴 | 观察ac面 |
| [100] | 沿a轴 | 观察bc面 |
| [110] | 沿[110] | 观察对角线 |
| [111] | 沿[111] | 观察体对角线 |

---

## 六、测量功能

### 6.1 测量键长

**位置**：Edit → Bonds

**方法1：通过菜单**
1. 点击 Edit → Bonds
2. 点击 Add
3. 选择两个原子
4. 查看键长

**方法2：通过工具栏**
1. 点击工具栏的测量按钮
2. 点击第一个原子
3. 点击第二个原子
4. 查看测量结果

### 6.2 测量键角

**位置**：Edit → Angles

**操作步骤**：
1. 点击 Edit → Angles（或工具栏按钮）
2. 点击第一个原子（顶点）
3. 点击第二个原子
4. 点击第三个原子
5. 查看键角

### 6.3 测量二面角

**位置**：Edit → Dihedral Angles

**操作步骤**：
1. 点击 Edit → Dihedral Angles
2. 依次点击四个原子
3. 查看二面角

### 6.4 测量距离

**位置**：Utilities → Distance

**操作步骤**：
1. 点击 Utilities → Distance
2. 点击第一个原子
3. 点击第二个原子
4. 查看距离

---

## 七、Utilities（实用工具）

### 7.1 结构操作工具

#### 7.1.1 Remove Symmetry Relations（移除对称关系）

**位置**：Utilities → Remove Symmetry Relations

**功能**：
- 移除对称相关的原子
- 只保留不对称单元中的原子

**用途**：
- 简化结构显示
- 只显示独特的原子

#### 7.1.2 Merge Atoms（合并原子）

**位置**：Utilities → Merge Atoms

**功能**：
- 合并重叠的原子
- 修复对称操作导致的原子重叠

#### 7.1.3 Remove Symmetry（移除对称性）

**位置**：Utilities → Remove Symmetry

**功能**：
- 移除所有对称操作
- 将结构转换为P1空间群

**用途**：
- 创建超胞前的准备
- 简化结构分析

#### 7.1.4 Convert to P1（转换为P1）

**位置**：Utilities → Convert to P1

**功能**：
- 将结构转换为P1空间群
- 生成所有对称等价原子

#### 7.1.5 Expand（扩展）

**位置**：Utilities → Expand

**功能**：
- 应用对称操作生成所有等价原子
- 扩展显示范围

#### 7.1.6 Reduce（缩减）

**位置**：Utilities → Reduce

**功能**：
- 移除对称等价原子
- 简化结构

### 7.2 键分析工具

#### 7.2.1 Search Bonds（搜索键）

**位置**：Utilities → Search Bonds

**功能**：
- 根据原子间距离自动搜索键
- 设置键长范围

**操作步骤**：
1. 点击 Utilities → Search Bonds
2. 设置最小和最大键长
3. 点击 Search
4. 自动添加符合条件的键

#### 7.2.2 Bond Classification（键分类）

**位置**：Utilities → Bond Classification

**功能**：
- 根据键长和类型对键进行分类
- 区分单键、双键、三键等

#### 7.2.3 Bond Valence（键价）

**位置**：Utilities → Bond Valence

**功能**：
- 计算键价和
- 验证结构合理性

**用途**：
- 检查晶体结构的化学合理性
- 验证价态平衡

#### 7.2.4 Bond Paths（键路径）

**位置**：Utilities → Bond Paths

**功能**：
- 管理键路径
- 显示/隐藏键路径

#### 7.2.5 Bond Strain Analysis（键应变分析）

**位置**：Utilities → Bond Strain Analysis

**功能**：
- 分析键的应变
- 计算键长偏差

### 7.3 结构特征工具

#### 7.3.1 Lattice Planes（晶面）

**位置**：Utilities → Lattice Planes

**功能**：
- 定义和管理晶面
- 设置密勒指数

#### 7.3.2 Polyhedra（多面体）

**位置**：Utilities → Polyhedra

**功能**：
- 定义和管理配位多面体
- 设置中心原子和配位原子

#### 7.3.3 Nuclear/Atomic Displacements（原子位移）

**位置**：Utilities → Nuclear/Atomic Displacements

**功能**：
- 处理热椭球参数
- 显示原子位移

### 7.4 数据导入导出

#### 7.4.1 Import Data（导入数据）

**位置**：Utilities → Import Data

**功能**：
- 从外部文件导入结构数据
- 支持CIF、XYZ、POSCAR等格式

#### 7.4.2 Export Data（导出数据）

**位置**：Utilities → Export Data

**功能**：
- 导出结构数据
- 支持多种格式（VRML、OBJ、STL等）

#### 7.4.3 Edit Style（编辑样式）

**位置**：Utilities → Edit Style

**功能**：
- 编辑键、多面体等的显示样式
- 设置颜色、宽度等参数

### 7.5 其他工具

#### 7.5.1 Structure Parameters（结构参数）

**位置**：Utilities → Structure Parameters

**功能**：
- 查看详细的结构信息
- 导出结构数据
- 复制结构参数

#### 7.5.2 Simulation（模拟）

**位置**：Utilities → Simulation

**功能**：
- 模拟X射线衍射
- 模拟电子衍射
- 模拟中子衍射

#### 7.5.3 Powder Pattern（粉末图谱）

**位置**：Utilities → Powder Pattern

**功能**：
- 生成粉末衍射图谱
- 导出图谱数据

#### 7.5.4 CIF Report（CIF报告）

**位置**：Utilities → CIF Report

**功能**：
- 生成CIF格式报告
- 导出结构数据

---

## 八、导出功能

### 8.1 导出图片

**位置**：File → Export Raster Image

**操作步骤**：
1. 点击 File → Export Raster Image
2. 选择保存位置和文件名
3. 设置图片参数
4. 点击保存

**图片参数设置**：

| 参数 | 说明 | 建议值 |
|:-----|:-----|:-------|
| Format | 图片格式 | PNG（推荐） |
| Width | 宽度（像素） | 2000-3000 |
| Height | 高度（像素） | 1500-2400 |
| DPI | 分辨率 | 300（打印） |
| Background | 背景色 | White |

**图片格式对比**：
| 格式 | 优点 | 缺点 | 适用场景 |
|:-----|:-----|:-----|:---------|
| PNG | 无损、透明 | 文件较大 | 通用 |
| TIFF | 无损、专业 | 文件很大 | 论文发表 |
| JPEG | 文件小 | 有损压缩 | 网页展示 |
| BMP | 简单 | 文件很大 | 不推荐 |

### 8.2 导出矢量图

**位置**：File → Export Vector Image

**格式**：
- EPS：适用于论文发表
- SVG：适用于网页展示

### 8.3 导出3D文件

**位置**：File → Export Data

**格式**：
- VRML (.wrl)：3D虚拟现实格式
- OBJ (.obj)：3D模型格式
- STL (.stl)：3D打印格式
- XSF (.xsf)：XCrySDen格式

**3D打印导出步骤**：
1. 点击 File → Export Data
2. 选择 STL 或 OBJ 格式
3. 设置缩放比例（1 Å = 1 mm）
4. 保存文件
5. 导入3D打印软件

---

## 九、高级功能

### 9.1 电子密度显示

**前置条件**：需要导入体积数据文件（如CHGCAR、cube）

**操作步骤**：
1. 导入体积数据文件
2. 在Objects面板找到Isosurfaces
3. 设置等值面数值
4. 调整颜色和透明度

### 9.2 磁结构显示

**前置条件**：需要导入包含磁矩信息的CIF文件

**操作步骤**：
1. 导入磁CIF文件
2. 在Edit → Vectors中查看磁矩
3. 调整矢量显示样式

### 9.3 动画制作

**位置**：Utilities → Animation

**功能**：
- 制作旋转动画
- 制作结构变化动画
- 导出GIF动画

**操作步骤**：
1. 设置起始和结束角度
2. 设置帧数
3. 预览动画
4. 导出GIF

### 9.4 超胞创建

**位置**：Edit → Edit Data → Unit Cell → Transformation

**操作步骤**：
1. 点击 Edit → Edit Data → Unit Cell
2. 选择 Transformation 标签
3. 输入变换矩阵
4. 点击 Apply

**变换矩阵示例**：
| 目标 | 矩阵 |
|:-----|:-----|
| 2×2×2超胞 | [[2,0,0],[0,2,0],[0,0,2]] |
| 2×1×1超胞 | [[2,0,0],[0,1,0],[0,0,1]] |
| 沿[110]拉伸 | [[1,1,0],[0,1,0],[0,0,1]] |

---

## 十、化学竞赛常用操作

### 10.1 显示NaCl岩盐结构

**步骤**：
1. File → Open → 选择 NaCl-Fm-3m.cif
2. Edit → Edit Data → Style → Polyhedral
3. 调整视角
4. File → Export Raster Image → 保存PNG

### 10.2 显示CsCl结构

**步骤**：
1. File → Open → 选择 CsCl-Pm-3m.cif
2. Edit → Edit Data → Style → Ball-and-stick
3. 调整视角
4. File → Export Raster Image → 保存PNG

### 10.3 显示ZnS闪锌矿结构

**步骤**：
1. File → Open → 选择 ZnS-F-43m.cif
2. Edit → Edit Data → Style → Polyhedral
3. 显示Zn²⁺的四面体配位
4. File → Export Raster Image → 保存PNG

### 10.4 显示CaF₂萤石结构

**步骤**：
1. File → Open → 选择 CaF2-Fm-3m.cif
2. Edit → Edit Data → Style → Polyhedral
3. 显示Ca²⁺的立方体配位
4. File → Export Raster Image → 保存PNG

### 10.5 显示晶面

**步骤**：
1. 打开晶体结构文件
2. Edit → Edit Data → Lattice Planes
3. 点击 New
4. 输入密勒指数（如 1 0 0）
5. 设置颜色和透明度
6. 点击 OK
7. File → Export Raster Image → 保存PNG

### 10.6 测量配位数

**步骤**：
1. 打开晶体结构文件
2. Edit → Edit Data → Bonds
3. 点击 Add
4. 选择中心原子
5. 设置键长范围（包含所有配位键）
6. 查看配位数

---

## 十一、常见问题

### Q1：VESTA打不开CIF文件？

**可能原因**：
- CIF文件格式错误
- 文件编码问题
- 文件损坏

**解决方案**：
1. 用文本编辑器检查CIF文件
2. 确保文件编码为UTF-8
3. 从可靠来源重新下载

### Q2：如何显示配位多面体？

**操作步骤**：
1. Edit → Edit Data → Polyhedra
2. 点击 Add
3. 选择中心原子
4. 选择配位原子
5. 点击 OK

### Q3：如何测量键角？

**操作步骤**：
1. Edit → Angles（或工具栏按钮）
2. 依次点击三个原子
3. 查看测量结果

### Q4：如何导出高清图片？

**推荐设置**：
- Format: PNG
- Width: 3000 pixels
- Height: 2400 pixels
- DPI: 300

### Q5：如何创建超胞？

**操作步骤**：
1. Edit → Edit Data → Unit Cell
2. 选择 Transformation 标签
3. 输入变换矩阵
4. 点击 Apply

---

## 十二、参考资源

### 官方资源

| 资源 | 链接 |
|:-----|:-----|
| VESTA官网 | https://jp-minerals.org/vesta/ |
| VESTA手册 | 安装目录下 help 文件夹 |
| VESTA教程 | https://jp-minerals.org/vesta/tutorial/ |

### 视频教程

| 平台 | 搜索关键词 |
|:-----|:-----------|
| YouTube | "VESTA tutorial crystal structure" |
| B站 | "VESTA教程 晶体结构" |

### 学术文献

> K. Momma and F. Izumi, "VESTA 3 for three-dimensional visualization of crystal, volumetric and morphology data", *J. Appl. Crystallogr.* **44**, 1272–1276 (2011).

---

## 十三、附录

### 附录A：常用快捷键

| 快捷键 | 功能 |
|:-------|:-----|
| Ctrl+O | 打开文件 |
| Ctrl+S | 保存 |
| Ctrl+Z | 撤销 |
| Ctrl+Y | 重做 |
| Ctrl+B | 编辑键 |
| Delete | 删除 |
| Home | 适合窗口 |
| F5 | 刷新 |
| 鼠标左键拖动 | 旋转 |
| 鼠标中键拖动 | 平移 |
| 鼠标滚轮 | 缩放 |

### 附录B：CPK配色表

| 元素 | 颜色 | RGB |
|:-----|:-----|:----|
| H | 白色 | 255,255,255 |
| He | 青色 | 217,255,255 |
| Li | 紫色 | 204,128,255 |
| Be | 绿色 | 194,255,0 |
| B | 棕色 | 255,181,181 |
| C | 灰色 | 128,128,128 |
| N | 蓝色 | 48,80,248 |
| O | 红色 | 255,13,13 |
| F | 黄绿 | 144,224,80 |
| Na | 紫色 | 171,92,255 |
| Mg | 绿色 | 138,255,0 |
| Al | 银灰 | 191,166,166 |
| Si | 棕色 | 240,200,160 |
| P | 橙色 | 255,128,0 |
| S | 黄色 | 255,255,48 |
| Cl | 绿色 | 31,240,31 |
| K | 紫色 | 143,61,255 |
| Ca | 绿色 | 61,255,0 |
| Ti | 灰色 | 191,194,199 |
| Cr | 蓝灰 | 138,153,166 |
| Mn | 粉色 | 156,122,199 |
| Fe | 棕色 | 224,102,51 |
| Co | 蓝色 | 240,144,160 |
| Ni | 绿色 | 80,208,80 |
| Cu | 棕色 | 200,128,51 |
| Zn | 蓝灰 | 125,128,176 |
| Ag | 银灰 | 192,192,192 |
| Au | 金色 | 255,209,35 |
| Pt | 灰色 | 208,208,224 |

### 附录C：晶系参数

| 晶系 | 参数约束 | 示例 |
|:-----|:---------|:-----|
| 立方 | a=b=c, α=β=γ=90° | NaCl, Cu |
| 四方 | a=b≠c, α=β=γ=90° | TiO₂, BaTiO₃ |
| 正交 | a≠b≠c, α=β=γ=90° | FeS₂, I₂ |
| 六方 | a=b≠c, α=β=90°, γ=120° | Mg, Zn |
| 三方 | a=b=c, α=β=γ≠90° | Al₂O₃, CaCO₃ |
| 单斜 | a≠b≠c, α=γ=90°≠β | NaHCO₃ |
| 三斜 | a≠b≠c, α≠β≠γ | - |
