---
title: 动画脚本
type: 资源索引
purpose: Blender / VESTA Python 动画脚本管理
created: 2026-08-01
updated: 2026-08-01
tags: [可视化, 动画, Python, 脚本]
---

# 动画脚本

> 存放用于生成化学教学动画的 Python 脚本。

## 使用方式

### Blender 脚本
```bash
# 命令行渲染（无需打开 GUI）
blender --background --python script.py
```

### VESTA 脚本
VESTA 内置 Python 支持：
```
VESTA → Utilities → Script → 选择 .py 文件
```

## 脚本分类

### 晶体结构类
| 脚本 | 功能 | 工具 | 状态 |
|:-----|:-----|:-----|:-----|
| vesta_batch_export.py | VESTA 批量导出 CIF → PNG | VESTA | ✅ 已创建 |

### 分子结构类
| 脚本 | 功能 | 工具 | 状态 |
|:-----|:-----|:-----|:-----|
| blender_molecule_render.py | Blender 分子渲染（含CPK配色） | Blender | ✅ 已创建 |

### 动画类
| 脚本 | 功能 | 工具 | 状态 |
|:-----|:-----|:-----|:-----|
| blender_rotation_animation.py | Blender 旋转动画生成 | Blender | ✅ 已创建 |

## 常用脚本模板

### 模板1：VESTA 批量导出图片
```python
# VESTA Python 脚本模板
# 用于批量打开 CIF 文件并导出图片

import subprocess
import os

cif_dir = "./CIF文件"
output_dir = "./渲染图片"

for cif_file in os.listdir(cif_dir):
    if cif_file.endswith(".cif"):
        # VESTA 命令行导出（示例）
        print(f"处理: {cif_file}")
        # 实际使用时需要根据 VESTA 版本调整
```

### 模板2：Blender 分子渲染
```python
# Blender Python 脚本模板
# 用于渲染分子结构

import bpy

def setup_scene():
    """清空场景并设置基本环境"""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # 设置渲染引擎
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    
    # 设置分辨率
    bpy.context.scene.render.resolution_x = 2000
    bpy.context.scene.render.resolution_y = 1500
    
    # 添加灯光
    bpy.ops.object.light_add(type='AREA', location=(3, -3, 5))
    light = bpy.context.object
    light.data.energy = 100

def import_molecule(filepath):
    """导入分子结构"""
    # 根据文件格式选择导入方式
    if filepath.endswith('.pdb'):
        bpy.ops.import_scene.pdb(filepath=filepath)
    elif filepath.endswith('.xyz'):
        # 需要 Molecular Nodes 插件
        pass

def render_output(output_path):
    """渲染并保存"""
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

# 主程序
setup_scene()
# import_molecule("molecule.pdb")
# render_output("output.png")
```

### 模板3：旋转动画
```python
# Blender 旋转动画脚本

import bpy
import math

def create_rotation_animation(object_name, rotations=1, frames=250):
    """为指定物体创建旋转动画"""
    obj = bpy.data.objects[object_name]
    
    # 设置帧范围
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = frames
    
    # 在第1帧设置初始旋转
    bpy.context.scene.frame_set(1)
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert(data_path="rotation_euler", frame=1)
    
    # 在最后一帧设置终止旋转
    bpy.context.scene.frame_set(frames)
    obj.rotation_euler = (0, 0, 2 * math.pi * rotations)
    obj.keyframe_insert(data_path="rotation_euler", frame=frames)
    
    # 设置线性插值
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'
```

## 注意事项

1. **Blender 版本**：脚本基于 Blender 4.x 编写，旧版本可能不兼容
2. **插件依赖**：部分脚本需要 Molecular Nodes 插件
3. **渲染时间**：Cycles 渲染较慢，建议先用 Eevee 预览
4. **路径问题**：Windows 路径使用反斜杠或原始字符串
