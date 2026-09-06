---
title: Molecular Nodes 详细使用指南
type: 工具指南
tool: Molecular Nodes (Blender插件)
purpose: 化学分子和晶体结构的导入与可视化
created: 2026-08-01
updated: 2026-08-01
tags: [可视化, Blender, Molecular Nodes, 化学, 详细教程]
---

# Molecular Nodes 详细使用指南

> 本指南详细介绍如何使用 Molecular Nodes 在 Blender 中导入和可视化化学分子和晶体结构。

---

## 1. Molecular Nodes 是什么？

**Molecular Nodes** 是一个 Blender 插件，它可以：
- 从 PDB（蛋白质数据库）导入分子结构
- 从 CIF 文件导入晶体结构
- 使用 Geometry Nodes 系统显示原子、化学键
- 生成高质量的分子渲染图和动画

**核心优势**：
- ✅ 直接导入标准化学数据格式
- ✅ 自动生成原子和化学键
- ✅ 使用 Geometry Nodes，可自定义显示
- ✅ 渲染质量高（Cycles 引擎）

---

## 2. 安装 Molecular Nodes

### 2.1 下载
```
GitHub: https://github.com/BradyAJohnston/MolecularNodes
→ 点击 "Releases" → 下载最新版本的 MolecularNodes.zip
```

### 2.2 在 Blender 中安装
```
1. 打开 Blender
2. Edit → Preferences → Add-ons
3. 点击 "Install..." 按钮
4. 选择下载的 MolecularNodes.zip 文件
5. 点击 "Install Add-on"
```

### 2.3 启用插件
```
1. 在 Add-ons 面板中搜索 "Molecular"
2. 找到 "Molecular Nodes"
3. 勾选启用它
4. 点击 "Save Preferences"
```

### 2.4 验证安装
```
1. 关闭偏好设置
2. 在 3D Viewport 中按 N 键
3. 找到 "Molecular Nodes" 标签
4. 看到 Import 按钮 = 安装成功
```

---

## 3. 基本使用流程

### 3.1 导入分子结构

**方法一：从 PDB 导入（推荐）**
```
1. 按 N 键打开侧边栏
2. 点击 "Molecular Nodes" 标签
3. 点击 "Import" 按钮
4. 选择 "PDB" 选项
5. 输入 PDB ID（如 1CRN = 胰岛素）
6. 点击 "Import"
```

**方法二：从本地文件导入**
```
1. 按 N 键打开侧边栏
2. 点击 "Molecular Nodes" 标签
3. 点击 "Import" 按钮
4. 选择 "File" 选项
5. 浏览选择本地的 PDB/CIF/XYZ 文件
6. 点击 "Import"
```

**方法三：从 CIF 文件导入**
```
1. 按 N 键打开侧边栏
2. 点击 "Molecular Nodes" 标签
3. 点击 "Import" 按钮
4. 选择 "CIF" 选项
5. 浏览选择 .cif 文件
6. 设置晶胞重复次数（可选）
7. 点击 "Import"
```

---

## 4. 调整显示样式

### 4.1 选择显示模式

导入分子后，可以在 Geometry Nodes 编辑器中调整：

| 模式 | 说明 | 适用场景 |
|:-----|:-----|:---------|
| Ball and Stick | 球棍模型 | 分子结构展示（推荐） |
| Spacefill | 空间填充 | 展示分子体积 |
| Stick | 棒状 | 展示化学键骨架 |
| Ribbon | 带状 | 蛋白质二级结构 |
| Surface | 表面 | 分子表面形状 |

**切换方法**：
```
1. 选择导入的分子物体
2. 在 Properties → Modifier Properties 中
3. 找到 Molecular Nodes 修改器
4. 调整 "Style" 参数
```

### 4.2 调整原子大小

```
在 Geometry Nodes 编辑器中：
- 调整 "Atom Radius" 参数
- 默认值通常合适，可根据需要微调
```

### 4.3 调整化学键显示

```
在 Geometry Nodes 编辑器中：
- 调整 "Bond Radius" 参数
- 调整 "Bond Cutoff" 控制显示哪些键
```

---

## 5. 设置材质和颜色

### 5.1 自动配色（CPK配色）

Molecular Nodes 通常自动使用 CPK 配色：
| 元素 | 颜色 |
|:-----|:-----|
| H | 白色 |
| C | 灰色 |
| N | 蓝色 |
| O | 红色 |
| S | 黄色 |
| P | 橙色 |
| Cl | 绿色 |

### 5.2 手动修改颜色

```
1. 选择原子物体
2. 在 Properties → Material Properties 中
3. 找到对应的材质
4. 修改 "Base Color" 颜色
```

### 5.3 调整材质属性

```
Principled BSDF 参数：
- Base Color: 原子颜色
- Roughness: 0.3-0.5（光泽度）
- Metallic: 0.0（非金属）或 0.8-1.0（金属原子）
- Specular: 0.5（高光强度）
```

---

## 6. 设置灯光和渲染

### 6.1 添加灯光

**三点灯光（推荐）**：
```
1. Shift + A → Light → Area
   位置: (5, -5, 5)  强度: 250  ← 主光

2. Shift + A → Light → Area
   位置: (-3, -3, 3)  强度: 100  ← 补光

3. Shift + A → Light → Area
   位置: (0, 5, 3)  强度: 150  ← 背光
```

### 6.2 设置相机

```
1. Shift + A → Camera
2. 调整位置: (0, -10, 3)
3. 朝向分子（按 Ctrl+T 添加 Track To 约束）
4. 设置为当前相机（Ctrl+Numpad 0）
```

### 6.3 渲染设置

```
Properties → Render Properties:
- Render Engine: Cycles（高质量）或 Eevee（快速）
- Sampling → Render: 128-256
- Resolution: 1920×1080（屏幕）或 3000×2000（打印）
```

### 6.4 渲染图片

```
F12 → 渲染
Image → Save As → 选择 PNG 格式
```

---

## 7. 教学场景示例

### 示例1：蛋白质结构（胰岛素）

```
1. Molecular Nodes → Import → PDB ID: 4INS
2. 显示模式: Ribbon
3. 添加三点灯光
4. Cycles 渲染
5. 导出 PNG
```

### 示例2：小分子（水分子）

```
1. Molecular Nodes → Import → PDB ID: 1S72（水分子）
   或用本地 XYZ 文件
2. 显示模式: Ball and Stick
3. 调整视角
4. 渲染
```

### 示例3：晶体结构（NaCl）

```
1. Molecular Nodes → Import → CIF 文件: NaCl-Fm-3m.cif
2. 设置晶胞重复: 2×2×2
3. 显示模式: Ball and Stick
4. 添加晶胞边框
5. 渲染
```

### 示例4：配位化合物

```
1. 用 Avogadro 构建配合物 → 导出 PDB
2. Molecular Nodes → Import → 本地 PDB 文件
3. 调整显示样式
4. 设置中心原子和配体颜色
5. 渲染
```

---

## 8. Geometry Nodes 基础

### 8.1 什么是 Geometry Nodes？

Geometry Nodes 是 Blender 的节点系统，可以：
- 程序化生成几何体
- 控制原子、化学键的显示
- 创建动画效果

### 8.2 打开 Geometry Nodes 编辑器

```
1. 切换到 Geometry Nodes 工作区
   或
2. 在 3D Viewport 中切换编辑器类型为 "Geometry Node Editor"
```

### 8.3 Molecular Nodes 的节点结构

Molecular Nodes 会自动创建节点树，主要包括：
- **原子节点**: 控制原子的显示
- **化学键节点**: 控制键的显示
- **材质节点**: 控制颜色和材质

### 8.4 常用节点参数

| 参数 | 作用 | 调整建议 |
|:-----|:-----|:---------|
| Atom Radius | 原子大小 | 0.3-0.5 |
| Bond Radius | 键粗细 | 0.05-0.1 |
| Style | 显示模式 | Ball and Stick |
| Color Scheme | 配色方案 | CPK |

---

## 9. 动画制作

### 9.1 旋转动画

```
1. 选择分子物体
2. 在第1帧: R → 旋转到起始角度 → I → Rotation
3. 在第250帧: R → 旋转到终止角度 → I → Rotation
4. Space 播放动画
5. Render → Render Animation
```

### 9.2 关键帧动画

```
1. 在 Timeline 中选择帧
2. 选择物体 → 调整位置/旋转/缩放
3. I → Location / Rotation / Scale
4. 重复创建更多关键帧
```

---

## 10. 常见问题

| 问题 | 解决方案 |
|:-----|:---------|
| 导入失败 | 检查文件格式、网络连接 |
| 原子不显示 | 检查 Geometry Nodes 修改器 |
| 颜色不对 | 调整材质设置 |
| 渲染太慢 | 降低采样数或用 Eevee |
| 动画卡顿 | 简化场景或降低分辨率 |

---

## 11. 与其他工具的配合

| 工具 | 配合方式 |
|:-----|:---------|
| Avogadro | 构建分子 → 导出 PDB → MN 导入 |
| VESTA | 打开 CIF → 导出 VRML → Blender 导入 |
| Gaussian | 计算分子轨道 → Avogadro 读取 → 导出 PDB |
| PyMOL | 导出 PDB → MN 导入 |

---

## 12. 参考资源

| 资源 | 链接 |
|:-----|:-----|
| Molecular Nodes 官网 | [molecularnodes.com](https://molecularnodes.com/) |
| GitHub 文档 | [github.com/BradyAJohnston/MolecularNodes](https://github.com/BradyAJohnston/MolecularNodes) |
| Brady Johnston YouTube | [youtube.com/@BradyJohnston](https://www.youtube.com/@BradyJohnston) |
| Geometry Nodes 教程 | [docs.blender.org/manual](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/) |
