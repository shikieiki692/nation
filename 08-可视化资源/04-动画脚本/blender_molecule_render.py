"""
Blender 分子渲染脚本模板
用途：导入分子/晶体结构并渲染高质量图片
使用方法：blender --background --python blender_molecule_render.py
"""

import bpy
import os
import sys

# ========== 配置区 ==========
# 输入文件（PDB/CIF/XYZ 格式）
INPUT_FILE = ""  # 留空则使用示例场景
# 输出图片路径
OUTPUT_PATH = r"C:\Obsidion\妙妙屋\08-可视化资源\03-渲染图片\output.png"
# 渲染引擎：'CYCLES' 或 'BLENDER_EEVEE'
RENDER_ENGINE = "CYCLES"
# 采样数（Cycles）
SAMPLES = 128
# 分辨率
RESOLUTION_X = 2000
RESOLUTION_Y = 1500
# ============================

# 元素颜色（CPK 配色方案）
ELEMENT_COLORS = {
    "H":  (1.0, 1.0, 1.0),   # 白色
    "C":  (0.4, 0.4, 0.4),   # 灰色
    "N":  (0.1, 0.1, 0.9),   # 蓝色
    "O":  (0.9, 0.1, 0.1),   # 红色
    "S":  (1.0, 1.0, 0.0),   # 黄色
    "P":  (1.0, 0.5, 0.0),   # 橙色
    "Cl": (0.0, 0.9, 0.0),   # 绿色
    "Na": (0.6, 0.3, 0.9),   # 紫色
    "Fe": (0.8, 0.5, 0.0),   # 棕色
    "Cu": (0.0, 0.6, 0.8),   # 蓝绿色
    "Zn": (0.5, 0.5, 0.5),   # 灰色
    "Ca": (0.3, 0.9, 0.3),   # 浅绿色
    "K":  (0.5, 0.2, 0.8),   # 紫色
    "Cs": (0.4, 0.1, 0.7),   # 深紫色
    "Ti": (0.6, 0.6, 0.7),   # 灰蓝色
    "F":  (0.6, 0.9, 0.1),   # 黄绿色
    "Br": (0.5, 0.2, 0.0),   # 深棕色
    "I":  (0.4, 0.0, 0.6),   # 深紫色
    "Si": (0.7, 0.7, 0.4),   # 黄灰色
}

# 元素原子半径（埃 → Blender单位，缩放因子0.3）
ELEMENT_RADII = {
    "H": 0.25, "C": 0.40, "N": 0.38, "O": 0.36,
    "S": 0.50, "P": 0.45, "Cl": 0.50, "Na": 0.55,
    "Fe": 0.50, "Cu": 0.45, "Zn": 0.45, "Ca": 0.55,
    "K": 0.60, "Cs": 0.70, "Ti": 0.50, "F": 0.35,
    "Br": 0.55, "I": 0.60, "Si": 0.45,
}

def clear_scene():
    """清空场景"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # 清除残留数据
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def setup_render():
    """设置渲染参数"""
    scene = bpy.context.scene
    
    # 渲染引擎
    scene.render.engine = RENDER_ENGINE
    
    if RENDER_ENGINE == "CYCLES":
        scene.cycles.samples = SAMPLES
        scene.cycles.use_denoising = True
    
    # 分辨率
    scene.render.resolution_x = RESOLUTION_X
    scene.render.resolution_y = RESOLUTION_Y
    scene.render.resolution_percentage = 100
    
    # 输出格式
    scene.render.image_settings.file_format = 'PNG'

def setup_lighting():
    """设置三点灯光"""
    # 主光
    bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
    key_light = bpy.context.object
    key_light.data.energy = 200
    key_light.name = "Key Light"
    
    # 补光
    bpy.ops.object.light_add(type='AREA', location=(-3, -3, 3))
    fill_light = bpy.context.object
    fill_light.data.energy = 80
    fill_light.name = "Fill Light"
    
    # 背光
    bpy.ops.object.light_add(type='AREA', location=(0, 5, 3))
    rim_light = bpy.context.object
    rim_light.data.energy = 120
    rim_light.name = "Rim Light"

def setup_camera():
    """设置相机"""
    bpy.ops.object.camera_add(location=(0, -8, 3))
    camera = bpy.context.object
    camera.name = "Camera"
    
    # 朝向原点
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = bpy.data.objects.get("Molecule") or bpy.data.objects.new("Empty", None)
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    bpy.context.scene.camera = camera

def create_material(name, color):
    """创建材质"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    # 设置基础颜色
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.3
        bsdf.inputs["Metallic"].default_value = 0.0
    
    return mat

def render_output():
    """渲染并保存"""
    bpy.context.scene.render.filepath = OUTPUT_PATH
    bpy.ops.render.render(write_still=True)
    print(f"渲染完成: {OUTPUT_PATH}")

def main():
    """主程序"""
    print("=" * 50)
    print("Blender 分子渲染脚本")
    print("=" * 50)
    
    # 清空场景
    clear_scene()
    
    # 设置渲染
    setup_render()
    
    # 设置灯光
    setup_lighting()
    
    # 如果有输入文件，导入结构
    if INPUT_FILE and os.path.exists(INPUT_FILE):
        print(f"导入文件: {INPUT_FILE}")
        # 根据文件类型选择导入方式
        if INPUT_FILE.endswith(".pdb"):
            bpy.ops.import_scene.pdb(filepath=INPUT_FILE)
        elif INPUT_FILE.endswith(".xyz"):
            # 需要 Molecular Nodes 插件
            print("XYZ 格式需要 Molecular Nodes 插件")
        elif INPUT_FILE.endswith(".cif"):
            # 需要 Molecular Nodes 插件
            print("CIF 格式需要 Molecular Nodes 插件")
    else:
        print("未指定输入文件，创建示例场景")
        # 创建示例：简单的双原子分子
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(-0.5, 0, 0))
        atom1 = bpy.context.object
        atom1.name = "Atom_1"
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(0.5, 0, 0))
        atom2 = bpy.context.object
        atom2.name = "Atom_2"
        
        # 创建键
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.0, location=(0, 0, 0))
        bond = bpy.context.object
        bond.name = "Bond"
        bond.rotation_euler = (0, 0, 1.5708)  # 90度旋转
        
        # 设置材质
        mat1 = create_material("Atom_1_Mat", (0.9, 0.1, 0.1))  # 红色
        mat2 = create_material("Atom_2_Mat", (0.1, 0.1, 0.9))  # 蓝色
        mat_bond = create_material("Bond_Mat", (0.5, 0.5, 0.5))  # 灰色
        
        atom1.data.materials.append(mat1)
        atom2.data.materials.append(mat2)
        bond.data.materials.append(mat_bond)
    
    # 设置相机
    setup_camera()
    
    # 渲染
    render_output()
    
    print("=" * 50)
    print("完成！")

if __name__ == "__main__":
    main()
