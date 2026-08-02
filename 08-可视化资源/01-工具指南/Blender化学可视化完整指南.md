---
title: Blender 化学可视化完整指南
type: 工具指南
tool: Blender 4.x + Molecular Nodes
purpose: 从零基础到高级渲染的完整教程
created: 2026-08-02
updated: 2026-08-02
tags: [可视化, Blender, Molecular Nodes, 完整指南, 化学]
---

# Blender 化学可视化完整指南

> 本指南合并了 Blender 的所有使用内容，从零基础到高级渲染，一页掌握。

---

## 1. 安装与配置

### 1.1 安装 Blender
- 下载：[blender.org](https://www.blender.org/)
- 推荐版本：Blender 4.0+

### 1.2 安装 Molecular Nodes

```
1. 下载 Molecular Nodes
   GitHub: https://github.com/BradyAJohnston/MolecularNodes
2. Blender → Edit → Preferences → Add-ons
3. Install → 选择下载的 .zip 文件
4. 启用 Molecular Nodes 插件
5. 重启 Blender
```

### 1.3 验证安装

```
1. 按 N 键打开侧边栏
2. 找到 "Molecular Nodes" 标签
3. 看到 Import 按钮 = 安装成功
```

---

## 2. 基础操作

### 2.1 视图操作

| 操作 | 快捷键 |
|:-----|:-------|
| 旋转视图 | 鼠标中键 |
| 平移视图 | Shift + 鼠标中键 |
| 缩放视图 | 鼠标滚轮 |
| 正交视图 | Numpad 1/3/7 |
| 聚焦物体 | Numpad . |

### 2.2 物体操作

| 操作 | 快捷键 |
|:-----|:-------|
| 选择物体 | 左键 |
| 全选 | A |
| 移动 | G |
| 旋转 | R |
| 缩放 | S |
| 确认 | 左键 |
| 取消 | 右键 |

### 2.3 添加物体

| 操作 | 快捷键 |
|:-----|:-------|
| 添加菜单 | Shift + A |
| 添加球体（原子） | Shift + A → Mesh → UV Sphere |
| 添加圆柱（键） | Shift + A → Mesh → Cylinder |
| 添加灯光 | Shift + A → Light → Area |
| 添加相机 | Shift + A → Camera |

---

## 3. 使用 Molecular Nodes

### 3.1 导入分子

**从 PDB 导入**：
```
1. 按 N 键 → Molecular Nodes 标签
2. Import → PDB → 输入 PDB ID（如 1CRN）
3. 点击 Import
```

**从 CIF 导入**：
```
1. 按 N 键 → Molecular Nodes 标签
2. Import → CIF → 选择 .cif 文件
3. 设置晶胞重复次数（可选）
4. Import
```

**从 XYZ 导入**：
```
1. 按 N 键 → Molecular Nodes 标签
2. Import → XYZ → 选择文件
3. Import
```

### 3.2 调整显示样式

| 模式 | 用途 |
|:-----|:-----|
| Ball and Stick | 分子结构（推荐） |
| Spacefill | 分子体积 |
| Ribbon | 蛋白质二级结构 |
| Surface | 分子表面 |

**切换方法**：
```
1. 选择导入的物体
2. Properties → Modifier Properties
3. 找到 Molecular Nodes 修改器
4. 调整 "Style" 参数
```

---

## 4. 手动创建分子

### 4.1 创建原子

```
1. Shift + A → Mesh → UV Sphere
2. S + 0.3 → 缩放到原子大小
3. Tab → 右键 → Smooth
4. Tab → 退出编辑模式
```

### 4.2 创建化学键

```
1. Shift + A → Mesh → Cylinder
2. 调整大小和位置
3. R → 旋转对齐
```

### 4.3 复制原子

```
1. 选择原子
2. Shift + D → 复制
3. G → 移动到新位置
```

---

## 5. 材质和颜色

### 5.1 添加材质

```
1. 选择物体
2. Properties → Material Properties
3. 点击 "New" 创建新材质
```

### 5.2 设置颜色

```
1. 找到 "Base Color"
2. 点击颜色块选择颜色
```

### 5.3 CPK 配色

| 元素 | 颜色 |
|:-----|:-----|
| H | 白色 |
| C | 灰色 |
| N | 蓝色 |
| O | 红色 |
| S | 黄色 |
| P | 橙色 |
| Cl | 绿色 |

### 5.4 材质参数

```
Principled BSDF:
- Base Color: 元素颜色
- Roughness: 0.3-0.5
- Metallic: 0.0（非金属）
```

---

## 6. 灯光设置

### 6.1 三点灯光（推荐）

| 灯光 | 位置 | 强度 |
|:-----|:-----|:-----|
| 主光 | (5, -5, 5) | 250 |
| 补光 | (-3, -3, 3) | 100 |
| 背光 | (0, 5, 3) | 150 |

### 6.2 添加灯光

```
1. Shift + A → Light → Area
2. 移动到位置
3. 调整强度
```

---

## 7. 相机设置

### 7.1 添加相机

```
1. Shift + A → Camera
2. 调整位置
3. Ctrl+T → Track To Constraint
4. Ctrl+Numpad 0 → 设为当前相机
```

### 7.2 调整视角

```
1. Numpad 0 → 相机视图
2. G → 移动相机
3. R → 旋转相机
```

---

## 8. 渲染设置

### 8.1 渲染引擎

| 引擎 | 特点 | 推荐 |
|:-----|:-----|:-----|
| Eevee | 实时，速度快 | 预览 |
| Cycles | 路径追踪，质量高 | 最终输出 |

### 8.2 设置参数

```
Properties → Render Properties:
- Render Engine: Cycles
- Samples: 128-256
- Resolution: 2000×1500
```

### 8.3 渲染图片

```
F12 → 渲染
Image → Save As → PNG
```

---

## 9. 动画制作

### 9.1 旋转动画

```
1. 选择物体
2. 第1帧: R → I → Rotation
3. 第250帧: R → I → Rotation
4. Space 播放
5. Render → Render Animation
```

### 9.2 关键帧动画

```
1. 选择帧
2. 调整物体
3. I → Location/Rotation/Scale
4. 重复创建更多关键帧
```

---

## 10. 教学场景示例

### 10.1 晶体结构

```
1. Molecular Nodes → Import → CIF
2. 显示模式: Ball and Stick
3. 添加晶胞边框
4. 渲染
```

### 10.2 分子结构

```
1. Molecular Nodes → Import → PDB
2. 显示模式: Ball and Stick
3. 设置 CPK 材质
4. 渲染
```

### 10.3 旋转动画

```
1. 导入结构
2. 设置旋转关键帧
3. 渲染动画
```

---

## 11. 常见问题

| 问题 | 解决方案 |
|:-----|:---------|
| Molecular Nodes 导入失败 | 检查版本兼容性 |
| 渲染太慢 | 降低采样数或用 Eevee |
| 材质颜色不对 | 调整 Base Color |
| 动画卡顿 | 简化场景 |

---

## 12. 快捷键速查

| 操作 | 快捷键 |
|:-----|:-------|
| 旋转视图 | 鼠标中键 |
| 移动 | G |
| 旋转 | R |
| 缩放 | S |
| 添加物体 | Shift + A |
| 渲染 | F12 |
| 编辑模式 | Tab |

---

## 13. 学习路径

| 阶段 | 内容 | 目标 |
|:-----|:-----|:-----|
| 第1天 | 界面、视图操作 | 熟悉 Blender |
| 第2天 | 物体操作、添加物体 | 能创建简单场景 |
| 第3天 | 材质、灯光 | 能设置渲染环境 |
| 第4天 | Molecular Nodes | 能导入分子 |
| 第5天 | 渲染、动画 | 能输出图片和视频 |

---

## 参考资源

| 资源 | 链接 |
|:-----|:-----|
| Blender 官方教程 | [blender.org/support/tutorials](https://www.blender.org/support/tutorials/) |
| Molecular Nodes | [molecularnodes.com](https://molecularnodes.com/) |
| Brady Johnston YouTube | [youtube.com/@BradyJohnston](https://www.youtube.com/@BradyJohnston) |
| Blender Python API | [docs.blender.org/api](https://docs.blender.org/api/current/) |
