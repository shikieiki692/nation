"""
Blender 基础渲染模板生成脚本
用途：自动创建基础渲染场景（三点灯光 + 相机 + 背景）
使用方法：在 Blender 中运行此脚本
  Blender → Scripting 工作区 → 打开此文件 → 点击运行
"""

import bpy
import os

# ========== 配置区 ==========
TEMPLATE_NAME = "基础渲染模板"
OUTPUT_DIR = r"C:\Obsidion\妙妙屋\08-可视化资源\05-模板场景"
# ============================

def clear_scene():
    """清空场景"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # 清除残留数据
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.lights:
        if block.users == 0:
            bpy.data.lights.remove(block)

def create_three_point_lighting():
    """创建三点灯光"""
    # 主光 (Key Light)
    bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
    key_light = bpy.context.object
    key_light.name = "Key Light"
    key_light.data.energy = 250
    key_light.data.size = 2
    key_light.data.color = (1.0, 0.95, 0.9)  # 略暖色
    
    # 补光 (Fill Light)
    bpy.ops.object.light_add(type='AREA', location=(-3, -3, 3))
    fill_light = bpy.context.object
    fill_light.name = "Fill Light"
    fill_light.data.energy = 100
    fill_light.data.size = 3
    fill_light.data.color = (0.9, 0.95, 1.0)  # 略冷色
    
    # 背光 (Rim Light)
    bpy.ops.object.light_add(type='AREA', location=(0, 5, 3))
    rim_light = bpy.context.object
    rim_light.name = "Rim Light"
    rim_light.data.energy = 150
    rim_light.data.size = 1.5
    rim_light.data.color = (1.0, 1.0, 1.0)  # 白色
    
    print("✓ 三点灯光创建完成")

def create_camera():
    """创建相机"""
    bpy.ops.object.camera_add(location=(0, -10, 3))
    camera = bpy.context.object
    camera.name = "Main Camera"
    
    # 添加 Track To 约束，朝向原点
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = None  # 朝向原点
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    # 设置为当前相机
    bpy.context.scene.camera = camera
    
    print("✓ 相机创建完成")

def setup_render_settings():
    """设置渲染参数"""
    scene = bpy.context.scene
    
    # 渲染引擎
    scene.render.engine = 'CYCLES'
    
    # 采样数
    scene.cycles.samples = 128
    
    # 分辨率
    scene.render.resolution_x = 2000
    scene.render.resolution_y = 1500
    scene.render.resolution_percentage = 100
    
    # 输出格式
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    
    # 背景颜色（白色）
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs[0].default_value = (0.95, 0.95, 0.95, 1.0)  # 浅灰色
    
    print("✓ 渲染设置完成")

def setup_viewport():
    """设置视图"""
    # 切换到渲染预览模式
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'
    
    print("✓ 视图设置完成")

def save_template():
    """保存模板"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{TEMPLATE_NAME}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    print(f"✓ 模板已保存: {filepath}")

def main():
    """主程序"""
    print("=" * 60)
    print(f"创建 {TEMPLATE_NAME}")
    print("=" * 60)
    
    # 清空场景
    clear_scene()
    
    # 创建灯光
    create_three_point_lighting()
    
    # 创建相机
    create_camera()
    
    # 设置渲染
    setup_render_settings()
    
    # 设置视图
    setup_viewport()
    
    # 保存模板
    save_template()
    
    print("=" * 60)
    print("✓ 基础渲染模板创建完成！")
    print("=" * 60)
    print("\n使用方法：")
    print("1. 打开 Blender")
    print("2. File → Open → 选择 基础渲染模板.blend")
    print("3. 导入分子/晶体结构")
    print("4. 调整视角")
    print("5. F12 渲染")

if __name__ == "__main__":
    main()
