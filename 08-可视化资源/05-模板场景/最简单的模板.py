"""
最简单的 Blender 模板创建脚本
================================
直接复制下面的代码到 Blender 的 Scripting 工作区运行

使用方法：
1. 打开 Blender
2. 点击顶部的 "Scripting" 标签
3. 点击 "New" 创建新脚本
4. 复制下面的代码粘贴进去
5. 点击 "Run Script" 按钮（▶）
"""

# 清空场景
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 创建主光
bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
bpy.context.object.data.energy = 250

# 创建补光
bpy.ops.object.light_add(type='AREA', location=(-3, -3, 3))
bpy.context.object.data.energy = 100

# 创建背光
bpy.ops.object.light_add(type='AREA', location=(0, 5, 3))
bpy.context.object.data.energy = 150

# 创建相机
bpy.ops.object.camera_add(location=(0, -10, 3))
bpy.context.scene.camera = bpy.context.object

# 设置渲染
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128
bpy.context.scene.render.resolution_x = 2000
bpy.context.scene.render.resolution_y = 1500

print("Done!")
