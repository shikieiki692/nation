"""
Avogadro Python 批处理脚本模板
用途：批量构建、优化、导出分子结构
前提：需要安装 Avogadro 2 和 Python 支持
使用方法：python avogadro_batch_molecules.py
"""

import os
import subprocess
import json

# ========== 配置区 ==========
# 输出目录
OUTPUT_DIR = r"C:\Obsidion\妙妙屋\08-可视化资源\02-CIF文件库\00-分子结构"
# 图片输出目录
IMAGE_DIR = r"C:\Obsidion\妙妙屋\08-可视化资源\03-渲染图片\02-分子结构"
# ============================

# 教学常见分子列表
MOLECULES = {
    # 无机分子
    "H2O": {"smiles": "O", "name": "水", "category": "无机分子"},
    "NH3": {"smiles": "N", "name": "氨", "category": "无机分子"},
    "CH4": {"smiles": "C", "name": "甲烷", "category": "无机分子"},
    "BF3": {"smiles": "FB(F)F", "name": "三氟化硼", "category": "无机分子"},
    "SF6": {"smiles": "FS(F)(F)(F)F", "name": "六氟化硫", "category": "无机分子"},
    "PCl5": {"smiles": "ClP(Cl)(Cl)(Cl)Cl", "name": "五氯化磷", "category": "无机分子"},
    "XeF2": {"smiles": "FXeF", "name": "二氟化氙", "category": "无机分子"},
    "XeF4": {"smiles": "FXe(F)(F)F", "name": "四氟化氙", "category": "无机分子"},
    "CO2": {"smiles": "O=C=O", "name": "二氧化碳", "category": "无机分子"},
    "SO2": {"smiles": "O=S=O", "name": "二氧化硫", "category": "无机分子"},
    
    # 有机分子
    "ethane": {"smiles": "CC", "name": "乙烷", "category": "有机分子"},
    "ethylene": {"smiles": "C=C", "name": "乙烯", "category": "有机分子"},
    "acetylene": {"smiles": "C#C", "name": "乙炔", "category": "有机分子"},
    "benzene": {"smiles": "c1ccccc1", "name": "苯", "category": "有机分子"},
    "cyclohexane": {"smiles": "C1CCCCC1", "name": "环己烷", "category": "有机分子"},
    "ethanol": {"smiles": "CCO", "name": "乙醇", "category": "有机分子"},
    "acetone": {"smiles": "CC(=O)C", "name": "丙酮", "category": "有机分子"},
    "toluene": {"smiles": "Cc1ccccc1", "name": "甲苯", "category": "有机分子"},
    "phenol": {"smiles": "Oc1ccccc1", "name": "苯酚", "category": "有机分子"},
    "aniline": {"smiles": "Nc1ccccc1", "name": "苯胺", "category": "有机分子"},
    
    # 常见离子
    "carbonate": {"smiles": "[O-]C(=O)[O-]", "name": "碳酸根", "category": "离子"},
    "nitrate": {"smiles": "[O-][N+](=O)[O-]", "name": "硝酸根", "category": "离子"},
    "sulfate": {"smiles": "[O-]S(=O)(=O)[O-]", "name": "硫酸根", "category": "离子"},
    "phosphate": {"smiles": "[O-]P(=O)([O-])[O-]", "name": "磷酸根", "category": "离子"},
}

def create_output_dirs():
    """创建输出目录"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_xyz_content(name, smiles):
    """
    生成 XYZ 文件内容（示例框架）
    实际使用时需要调用 Avogadro 的 Python API
    """
    # 这只是示例，实际需要用 Avogadro API
    content = f"""# {name}
# SMILES: {smiles}
# 生成方式：Avogadro 力场优化
# 
# 使用方法：
# 1. 打开 Avogadro
# 2. Edit → Input Molecule → SMILES
# 3. 输入: {smiles}
# 4. Extensions → Molecular Mechanics → Quick Optimization
# 5. File → Save As → XYZ 格式
"""
    return content

def create_molecule_script(name, smiles, category):
    """为每个分子创建操作脚本"""
    script = f"""# Avogadro 操作脚本 - {name}
# 化学式：{name}
# SMILES：{smiles}
# 类别：{category}

## 操作步骤
1. 打开 Avogadro 2
2. Edit → Input Molecule → SMILES
3. 输入：{smiles}
4. 点击 OK
5. Extensions → Molecular Mechanics → Quick Optimization
6. 验证结构：
   - 选择 Measure 工具 (M)
   - 测量键长和键角
7. File → Save As → XYZ 格式
   保存到：{OUTPUT_DIR}/{name}.xyz
8. File → Export → Image
   保存到：{IMAGE_DIR}/{name}.png
"""
    return script

def main():
    """主程序"""
    print("=" * 60)
    print("Avogadro 分子构建批处理脚本")
    print("=" * 60)
    
    # 创建输出目录
    create_output_dirs()
    
    # 生成每个分子的操作脚本
    script_dir = os.path.join(OUTPUT_DIR, "_操作脚本")
    os.makedirs(script_dir, exist_ok=True)
    
    for name, info in MOLECULES.items():
        script = create_molecule_script(name, info["smiles"], info["category"])
        script_path = os.path.join(script_dir, f"{name}_操作步骤.txt")
        
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script)
        
        print(f"✓ {name} ({info['name']}) - 操作脚本已生成")
    
    # 生成汇总文件
    summary_path = os.path.join(OUTPUT_DIR, "_分子清单.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# 待构建分子清单\n\n")
        f.write("| 分子 | SMILES | 名称 | 类别 | 状态 |\n")
        f.write("|:-----|:-------|:-----|:-----|:-----|\n")
        
        for name, info in MOLECULES.items():
            f.write(f"| {name} | `{info['smiles']}` | {info['name']} | {info['category']} | 待构建 |\n")
    
    print(f"\n✓ 分子清单已生成: {summary_path}")
    print(f"✓ 操作脚本目录: {script_dir}")
    print("\n" + "=" * 60)
    print("完成！请按照操作脚本在 Avogadro 中逐个构建分子。")
    print("=" * 60)

if __name__ == "__main__":
    main()
