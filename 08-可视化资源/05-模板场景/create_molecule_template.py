"""
Blender 分子结构模板生成脚本
用途：自动创建分子结构可视化场景
使用方法：在 Blender 中运行此脚本
"""

import bpy
import os

# ========== 配置区 ==========
TEMPLATE_NAME = "分子结构模板"
OUTPUT_DIR = r"C:\Obsidion\妙妙屋\08-可视化资源\05-模板场景"
# ============================

def clear_scene():
    """清空场景"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
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
    # 主光
    bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
    key_light = bpy.context.object
    key_light.name = "Key Light"
    key_light.data.energy = 250
    key_light.data.size = 2
    
    # 补光
    bpy.ops.object.light_add(type='AREA', location=(-3, -3, 3))
    fill_light = bpy.context.object
    fill_light.name = "Fill Light"
    fill_light.data.energy = 100
    fill_light.data.size = 3
    
    # 背光
    bpy.ops.object.light_add(type='AREA', location=(0, 5, 3))
    rim_light = bpy.context.object
    rim_light.name = "Rim Light"
    rim_light.data.energy = 150
    rim_light.data.size = 1.5

def create_camera():
    """创建相机（透视视图，适合分子）"""
    bpy.ops.object.camera_add(location=(0, -8, 3))
    camera = bpy.context.object
    camera.name = "Molecule Camera"
    
    # 透视相机
    camera.data.type = 'PERSP'
    camera.data.lens = 50  # 50mm 焦距
    
    # 朝向原点
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    bpy.context.scene.camera = camera

def create_cpk_materials():
    """创建 CPK 配色材质"""
    element_colors = {
        "H": (1.0, 1.0, 1.0),
        "C": (0.4, 0.4, 0.4),
        "N": (0.1, 0.1, 0.9),
        "O": (0.9, 0.1, 0.1),
        "S": (1.0, 1.0, 0.0),
        "P": (1.0, 0.5, 0.0),
        "Cl": (0.0, 0.9, 0.0),
        "F": (0.6, 0.9, 0.1),
        "Br": (0.5, 0.2, 0.0),
        "I": (0.4, 0.0, 0.6),
    }
    
    for element, color in element_colors.items():
        mat = bpy.data.materials.new(name=f"{element}_Material")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.3
            bsdf.inputs["Metallic"].default_value = 0.0

def setup_render_settings():
    """设置渲染参数"""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128
    scene.render.resolution_x = 2000
    scene.render.resolution_y = 1500
    scene.render.image_settings.file_format = 'PNG'
    
    # 背景颜色（白色）
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

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
    
    clear_scene()
    create_three_point_lighting()
    create_camera()
    create_cpk_materials()
    setup_render_settings()
    save_template()
    
    print("=" * 60)
    print("✓ 分子结构模板创建完成！")
    print("=" * 60)
    print("\n使用方法：")
    print("1. 打开 Blender")
    print("2. File → Open → 选择 分子结构模板.blend")
    print("3. 导入分子（Molecular Nodes 或手动创建）")
    print("4. 应用 CPK 材质")
    print("5. F12 渲染")

if __name__ == "__main__":
    main()
