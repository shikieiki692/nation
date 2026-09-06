import re, os

INPUT = r"C:\Obsidion\妙妙屋\04-课件\学生讲义\第一轮结构化学复习讲义（学生用）.md"
OUTPUT = r"C:\Obsidion\妙妙屋\04-课件\学生讲义\第一轮结构化学复习讲义（学生用-带图片）.md"

INSERTIONS = [
    # Section 1
    ("**口诀：**\"进酒店走大厅（4s先填），退房也走大厅（4s先失）\"", "media/excalidraw-原子结构-电子排布三原则-1.png", "图1：电子排布三种顺序对比"),
    ("**五步法口诀：\"数→骨→填→检→标\"**", "media/lewis_5step.png", "图2：Lewis结构五步法流程"),
    ("**对角线相似：** Li~Mg, Be~Al, B~Si", "media/ionization_energy_trend.png", "图3：第一电离能周期性趋势"),
    # Section 2
    ("**第2步：查完整VSEPR表**", "media/vsepr-geometries-1.jpg", "图4：VSEPR几何构型可视化"),
    ("**两种能级图——45%的学生会选错！**", "media/second-period-mo.jpg", "图5：第二周期双原子分子MO能级图对比"),
    ("**核心原则：** VSEPR预测形状，杂化解释成因", "media/12-7a-hybrid-orbital-formation-sp-sp2-sp3.jpg", "图6：sp/sp²/sp³杂化轨道形成示意"),
    # Section 3
    ("**为什么不是BCC？**", "media/13-11-three-ab-ionic-crystal-structures-nacl-cscl-zns.jpg", "图7：NaCl、CsCl、ZnS三种典型离子晶体结构"),
    ("> **技巧：** 先找有没有", "media/图-七大晶系判定决策树.png", "图8：七大晶系判定决策树"),
    ("**空隙的几何性质：**", "media/13-8b-tetrahedral-void.jpg", "图9a：四面体空隙示意"),
    ("- 八面体空隙：被6个球包围", "media/13-8c-octahedral-void.jpg", "图9b：八面体空隙示意"),
    ("**金刚石与石墨（考纲要求）：**", "media/13-15-diamond-crystal-structure-fcc-unit-cell.jpg", "图10：金刚石晶体结构"),
    ("| 键型 | 全部C-C σ键 | 层内C-C σ+大π键，层间范德华力 |", "media/13-16-graphite-crystal-structure-layer-sp2.jpg", "图11：石墨晶体结构"),
    ("$$\\text{晶胞中原子数} = \\sum", "media/图-晶胞原子计数示意图.png", "图12：均摊法各位置占有率"),
    ("**完整计算示例——NaCl：**", "media/图-晶胞原子计数3D.png", "图13：NaCl晶胞三维结构"),
    # Section 4
    ("**什么是投影图？**", "media/图-分数坐标三维可视化.png", "图14：分数坐标三维可视化"),
    ("**⑥画d轨道分裂图——三步法：**", "media/八面体场d轨道分裂示意图.关系图.png", "图15：八面体场d轨道分裂示意图"),
    ("**⑦计算CFSE：**", "media/CFSE计算流程.流程图.png", "图16：CFSE计算流程"),
    ("**逐个固定法（fix-and-permute）：**", "media/配合物异构现象分类体系.关系图.png", "图17：配合物异构现象分类体系"),
    ("**实例——[MA₂B₂C₂]八面体配合物：**", "media/cis-complex.jpg", "图18a：cis-顺式异构体示意"),
    ("> **判断手性的快速规则：**", "media/fac-isomer.jpg", "图18b：fac-面式异构体示意"),
    ("38届真题考点。Cr-Cr之间存在**四重键**：", "media/sigma-pi-bond-formation.jpg", "图19：σ键和π键形成方式"),
    ("**d-d跃迁：** 电子从", "media/d-d-transition.jpg", "图20：d-d跃迁示意图"),
]

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
inserted = 0

for before_text, img_path, caption in INSERTIONS:
    found = False
    for i, line in enumerate(lines):
        if before_text in line:
            if i > 0 and ('![' in lines[i-1] or '![[' in lines[i-1]):
                continue
            img_block = f"\n![{caption}]({img_path})\n*{caption}*\n"
            lines.insert(i, img_block)
            inserted += 1
            print(f"OK: {caption}")
            found = True
            break
    if not found:
        print(f"MISS: {before_text[:40]}")

result = '\n'.join(lines)
result = re.sub(r'^---\n.*?\n---\n', '', result, flags=re.DOTALL)

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"\nInserted {inserted}/{len(INSERTIONS)} images")
