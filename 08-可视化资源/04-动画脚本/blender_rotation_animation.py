"""
Blender 旋转动画脚本
用途：创建分子/晶体结构的旋转展示动画
使用方法：blender --background --python blender_rotation_animation.py
"""

import bpy
import math

# ========== 配置区 ==========
# 输出目录
OUTPUT_DIR = r"C:\Obsidion\妙妙屋\08-可视化资源\03-渲染图片\animation"
# 动画帧数
TOTAL_FRAMES = 250
# 旋转圈数
ROTATIONS = 1
# 分辨率
RESOLUTION_X = 1920
RESOLUTION_Y = 1080
# 渲染引擎
RENDER_ENGINE = "BLENDER_EEVEE"  # Eevee 更快，Cycles 更高质量
# ============================

def setup_scene():
    """设置场景"""
    scene = bpy.context.scene
    
    # 帧范围
    scene.frame_start = 1
    scene.frame_end = TOTAL_FRAMES
    
    # 渲染设置
    scene.render.engine = RENDER_ENGINE
    scene.render.resolution_x = RESOLUTION_X
    scene.render.resolution_y = RESOLUTION_Y
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = OUTPUT_DIR
    
    if RENDER_ENGINE == "CYCLES":
        scene.cycles.samples = 64

def setup_lighting():
    """设置灯光"""
    # 主光
    bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
    light = bpy.context.object
    light.data.energy = 200
    
    # 补光
    bpy.ops.object.light_add(type='AREA', location=(-3, -3, 3))
    light = bpy.context.object
    light.data.energy = 80

def setup_camera():
    """设置相机（固定位置，旋转物体）"""
    bpy.ops.object.camera_add(location=(0, -10, 3))
    camera = bpy.context.object
    camera.name = "Camera"
    
    # 朝向原点
    bpy.context.scene.camera = camera

def create_rotation_animation(object_name):
    """为指定物体创建旋转动画"""
    obj = bpy.data.objects.get(object_name)
    if not obj:
        print(f"未找到物体: {object_name}")
        return
    
    # 在第1帧设置初始旋转
    bpy.context.scene.frame_set(1)
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert(data_path="rotation_euler", frame=1)
    
    # 在最后一帧设置终止旋转
    bpy.context.scene.frame_set(TOTAL_FRAMES)
    obj.rotation_euler = (0, 0, 2 * math.pi * ROTATIONS)
    obj.keyframe_insert(data_path="rotation_euler", frame=TOTAL_FRAMES)
    
    # 设置线性插值（匀速旋转）
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'
    
    print(f"已创建旋转动画: {object_name}")

def render_animation():
    """渲染动画"""
    bpy.ops.render.render(animation=True)
    print(f"动画渲染完成: {OUTPUT_DIR}")

def main():
    """主程序"""
    print("=" * 50)
    print("Blender 旋转动画脚本")
    print("=" * 50)
    
    # 设置场景
    setup_scene()
    setup_lighting()
    setup_camera()
    
    # 查找要旋转的物体
    # 优先选择 "Molecule" 或 "Crystal"，否则选择所有可见物体
    target = None
    for name in ["Molecule", "Crystal", "UnitCell"]:
        if name in bpy.data.objects:
            target = name
            break
    
    if not target:
        # 选择所有网格物体的父级
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.parent is None:
                target = obj.name
                break
    
    if target:
        create_rotation_animation(target)
        render_animation()
    else:
        print("未找到可旋转的物体")
        print("请先导入分子/晶体结构，或运行 blender_molecule_render.py 创建示例场景")
    
    print("=" * 50)
    print("完成！")

if __name__ == "__main__":
    main()
