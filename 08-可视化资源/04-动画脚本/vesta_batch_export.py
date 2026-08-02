"""
VESTA 批量导出图片脚本模板
用途：批量打开 CIF 文件并导出为 PNG 图片
使用方法：VESTA → Utilities → Script → 选择本文件
"""

import os
import subprocess

# ========== 配置区 ==========
# CIF 文件目录
CIF_DIR = r"C:\Obsidion\妙妙屋\08-可视化资源\02-CIF文件库"
# 输出图片目录
OUTPUT_DIR = r"C:\Obsidion\妙妙屋\08-可视化资源\03-渲染图片\01-晶体结构"
# 图片宽度（像素）
IMAGE_WIDTH = 2000
# 背景颜色（1=白色, 0=黑色）
BG_COLOR = 1
# ============================

def export_cif_to_png(cif_path, output_path):
    """
    打开 CIF 文件并导出为 PNG
    注意：VESTA 的 Python API 可能因版本不同而有差异
    """
    print(f"处理: {os.path.basename(cif_path)}")
    
    # VESTA 内部命令示例（需根据实际 VESTA 版本调整）
    # 这里只是示例框架，实际使用时需要参考 VESTA 文档
    try:
        # 打开文件
        # VESTA.open(cif_path)
        
        # 设置背景颜色
        # VESTA.setBackgroundColor(BG_COLOR)
        
        # 导出图片
        # VESTA.exportRasterImage(output_path, IMAGE_WIDTH)
        
        print(f"  ✓ 导出成功: {output_path}")
    except Exception as e:
        print(f"  ✗ 导出失败: {e}")

def batch_export():
    """批量导出所有 CIF 文件"""
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 遍历所有子目录
    for root, dirs, files in os.walk(CIF_DIR):
        for file in files:
            if file.endswith(".cif"):
                cif_path = os.path.join(root, file)
                
                # 生成输出文件名
                rel_path = os.path.relpath(root, CIF_DIR)
                category = rel_path.split(os.sep)[0] if rel_path != "." else "其他"
                png_name = file.replace(".cif", ".png")
                output_path = os.path.join(OUTPUT_DIR, png_name)
                
                export_cif_to_png(cif_path, output_path)

if __name__ == "__main__":
    print("=" * 50)
    print("VESTA 批量导出 CIF → PNG")
    print("=" * 50)
    batch_export()
    print("=" * 50)
    print("完成！")
