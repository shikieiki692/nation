"""
Blender 基础渲染模板 - 简化版
================================

使用方法：
1. 打开 Blender
2. 切换到 Scripting 工作区（顶部标签栏）
3. 点击 "Open" 按钮（文件夹图标）
4. 选择此文件
5. 点击 "Run Script" 按钮（▶ 播放图标）
6. 控制台会显示 "✓ 基础渲染模板创建完成！"

然后：
- 导入你的分子/晶体结构
- 按 F12 渲染图片
"""

import bpy

# ===== 清空场景 =====
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 删除默认立方体
for obj in bpy.data.objects:
    if obj.name == "Cube":
        bpy.data.objects.remove(obj)

# ===== 创建灯光 =====
# 主光
bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
bpy.context.object.name = "Key Light"
bpy.context.object.data.energy = 250
bpy.context.object.data.size = 2

# 补光
bpy.ops.object.light_add(type='AREA', location=(-3, -3, 3))
bpy.context.object.name = "Fill Light"
bpy.context.object.data.energy = 100
bpy.context.object.data.size = 3

# 背光
bpy.ops.object.light_add(type='AREA', location=(0, 5, 3))
bpy.context.object.name = "Rim Light"
bpy.context.object.data.energy = 150
bpy.context.object.data.size = 1.5

# ===== 创建相机 =====
bpy.ops.object.camera_add(location=(0, -10, 3))
bpy.context.object.name = "Main Camera"
bpy.context.scene.camera = bpy.context.object

# ===== 设置渲染 =====
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128
bpy.context.scene.render.resolution_x = 2000
bpy.context.scene.render.resolution_y = 1500

# ===== 完成 =====
print("=" * 50)
print("✓ 基础渲染模板创建完成！")
print("=" * 50)
print("")
print("接下来：")
print("1. 导入分子/晶体结构")
print("2. 调整视角")
print("3. 按 F12 渲染")
