import re
import sys
import datetime

file_path = r"c:\Obsidion\妙妙屋\04-课件\学生讲义\结构化学第一轮复习.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

captions = [
    "元素周期表分区图（s、p、d、ds、f 区分布）",
    "主族与过渡元素电负性变化趋势图（Pauling 标度）",
    "s、p、d 轨道空间形状与取向示意图",
    "多电子原子轨道能级图（Pauling 近似能级图）",
    "过渡元素电子排布及半满/全满稳定化特例示意图",
    "电子屏蔽效应与有效核电荷计算模型图",
    "第一电离能随核电荷数变化曲线及局部突跃点（反常点）",
    "第二、三周期元素第一电离能半满/全满反常倒挂现象",
    "共振式形式电荷分布与最优结构判断示例",
    "VSEPR 理论无孤对电子时的理想几何构型（AX₂~AX₆）",
    "含孤对电子分子的几何构型衍变及排斥力效应",
    "sp 杂化轨道形成过程与直线形空间取向",
    "sp² 杂化轨道形成过程与平面三角形空间取向",
    "sp³ 杂化轨道形成过程与正四面体空间取向",
    "涉及 d 轨道的杂化（sp³d/sp³d²）构型与成键特征",
    "同分异构体支链数与分子接触面积对色散力（沸点）的影响",
    "p 区元素氢化物沸点变化趋势与氢键导致的反常高沸点",
    "离子溶剂化过程与非极性分子水溶液中的疏水作用模型",
    "分子所属点群分类判断的标准流程（决策树）",
    "常见分子点群（C₂ᵥ、C₃ᵥ、D₃ₕ、T_d 等）对称元素示例",
    "四类基本晶体（离子/共价/金属/分子）微观结构特征对比",
    "七大晶系与 14 种布拉维（Bravais）点阵空间格子图示",
    "等径圆球的面心立方最密堆积（ccp）与六方最密堆积（hcp）结构",
    "密堆积结构中的四面体空隙（Td）分布与形成原理",
    "密堆积结构中的八面体空隙（Oh）分布与形成原理",
    "离子半径比（r⁺/r⁻）与阴阳离子配位多面体构型的关系",
    "离子晶体临界半径比（0.225、0.414、0.732）几何推导模型",
    "堆积方式与填隙类型推导离子晶体结构的通用判断逻辑",
    "常见二元离子晶体结构构型及其配位数对应关系",
    "NaCl 晶格能计算的 Born-Haber 热力学循环路径",
    "阴阳离子的相互极化与变形导致键型共价化及配位数降低",
    "NaCl 型晶胞结构图（面心立方堆积与八面体空隙全填满）",
    "CsCl 型晶胞结构图（简单立方点阵与体心填隙，非 bcc）",
    "立方 ZnS（闪锌矿）型晶胞结构图（面心立方与半数四面体填隙）",
    "CaF₂（萤石）型晶胞结构图（面心立方与全部四面体填隙）",
    "钙钛矿（ABO₃）型理想立方晶胞结构及离子占位示意图"
]

lines = content.split('\n')
new_lines = []
img_idx = 0

for line in lines:
    if "> 📌 **图位待补**：八面体场 d 轨道分裂能级图" in line:
        new_lines.append("![[b32a0ace276c8386086d52fbf9ce694176cbbd054d3297538a9191abf47b2574.jpg]]")
        new_lines.append("*图 37 八面体场中 d 轨道能级分裂图（球形电场→八面体场 t₂g/e_g 分裂，分裂能 Δ₀）*")
        continue

    new_lines.append(line)
    
    # Check if this line is an image insertion
    if line.strip().startswith('![[') and line.strip().endswith(']]'):
        if img_idx < len(captions):
            new_lines.append(f"*图 {img_idx + 1} {captions[img_idx]}*")
            img_idx += 1

new_content = '\n'.join(new_lines)
new_content = re.sub(r'image_count:\s*36', 'image_count: 37', new_content)
today = "2026-08-05" # Hardcode to today based on metadata
new_content = re.sub(r'updated:.*', f'updated: {today}', new_content)
new_content = re.sub(r'last_audit:.*', f'last_audit: {today}', new_content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Added {img_idx} captions and 1 new image.")
