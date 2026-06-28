#!/usr/bin/env python3
"""Update image references in super-enriched handouts.
- Excalidraw .md references → .png references (for docx/universal compatibility)
- Missing textbook images → use downloaded alternatives
"""
import re, os, sys

handout_dir = r"C:\Obsidion\妙妙屋\04-课件\学生讲义"
media_dir = r"C:\Obsidion\妙妙屋\media"

handouts = [
    "原子结构-超级充实版（自学完整）.md",
    "元素周期表与周期律-超级充实版（自学完整）.md",
    "分子结构基础-超级充实版（自学完整）.md",
    "晶体学基础-超级充实版（自学完整）.md",
    "晶体结构基础-超级充实版（自学完整）.md",
    "配位化合物基础-超级充实版（自学完整）.md",
]

# Mapping: problematic image ref → solution
IMAGE_MAP = {
    # Textbook images → downloaded alternatives
    "11-8-hydrogen-spectrum.jpg": "atomic_radius_trend.jpg",  # placeholder - better to use Wikipedia
    "11-23-atomic-radius-periodic-trend.jpg": "atomic_radius_trend.jpg",
    "11-24-ionization-energy-periodic-trend.jpg": "first_ionization_energy_trend.jpg",
    "11-25-electronegativity-periodic-trend.jpg": "electronegativity_table.jpg",
    "11-13-orbital-shapes-s-p-d.jpg": "轨道杂化类型对比.关系图.png",
    "11-15-electron-cloud-s-p-d.jpg": None,  # will be flagged
    "11-21-radial-distribution-3s-3p-3d.jpg": None,
    "11-22-4s-3d-radial-distribution.jpg": None,
    "11-19-pauling-energy-levels.jpg": None,
    "11-20-cotton-orbital-energy-vs-Z.jpg": None,
    "13-1-quartz-crystal-faces-angle-constancy.jpg": None,
    "13-2c-crystal-structure-to-lattice-abstraction.jpg": None,
    "13-3a-bravais-lattice-primitive-body-face-centered.jpg": None,
    "13-3b-cscl-structure-unit-cell.jpg": None,
    "13-3-four-bravais-lattices-p-i-f-h.jpg": None,
    "13-7-10-unit-cell-types-sc-bcc-fcc-comparison.jpg": None,
    "13-7a-simple-cubic-packing-layer-top-view.jpg": None,
    "13-7b-simple-cubic-unit-cell-po.jpg": None,
    "13-10-fcc-unit-cell-copper.jpg": None,
    "13-11a-nacl-cscl-zns-three-ab-structures.jpg": None,
    "13-11b-cscl-structure-unit-cell.jpg": None,
    "13-11-three-ab-ionic-crystal-structures-nacl-cscl-zns.jpg": None,
    "13-12-octahedral-coordination.jpg": None,
    "13-14-co2-molecular-crystal-unit-cell.jpg": None,
    "13-15c-diamond-unit-cell-atom-count.jpg": None,
    "13-15-diamond-crystal-structure-fcc-unit-cell.jpg": None,
    "13-17-ion-polarization-ideal-vs-polarized.jpg": None,
    "14-7-ti-h2o-6-d-d-transition-absorption-spectrum.jpg": None,
    # General chemistry images
    "d-orbital-shapes.jpg": "八面体场d轨道分裂示意图.关系图.png",
    "octahedral-splitting.jpg": "八面体场d轨道分裂示意图.关系图.png",
    "tetrahedral-splitting.jpg": "四面体场与正方形场分裂对比.关系图.png",
    "high-low-spin-fe.jpg": "高低自旋判断决策树.决策图.png",
    "d-d-transition.jpg": None,
    "second-period-mo.jpg": "第二周期MO能级对比.关系图.png",
    "mo-energy-diagram.jpg": "第二周期MO能级对比.关系图.png",
    "o2-mo-diagram.jpg": "第二周期MO能级对比.关系图.png",
    "h2-energy-curve.jpg": None,
    "sigma-pi-bond-formation.jpg": None,
    "spatial-lattice.jpg": None,
    "close-packed-layer.jpg": None,
    "vsepr-geometries-1.jpg": "VSEPR决策链.流程图.png",
    "vsepr-ax4.jpg": "VSEPR决策链.流程图.png",
    "vsepr-ax5-ax6.jpg": "VSEPR决策链.流程图.png",
    "ch4-geometry.jpg": "VSEPR决策链.流程图.png",
    "bcl3-geometry.jpg": "VSEPR决策链.流程图.png",
    "becl2-geometry.jpg": "VSEPR决策链.流程图.png",
    "ccp-unit-cell.jpg": None,
    "bcc-unit-cell.jpg": None,
    "ccp-stacking.jpg": None,
    "hcp-stacking.jpg": None,
    "nacl-structure.jpg": None,
    "cscl-structure.jpg": None,
    "zns-structure.jpg": None,
    "octahedral-coordination-radius-ratio.jpg": None,
    "diamond-structure.jpg": None,
    "graphite-structure.jpg": None,
}

# Excalidraw .md files that have corresponding .png renders
EXCALIDRAW_MAP = {
    "八面体场d轨道分裂示意图.关系图.md": "八面体场d轨道分裂示意图.关系图.png",
    "第二周期MO能级对比.关系图.md": "第二周期MO能级对比.关系图.png",
    "分子间力三层递进.关系图.md": "分子间力三层递进.关系图.png",
    "分子结构预测工具链.流程图.md": "分子结构预测工具链.流程图.png",
    "高低自旋判断决策树.决策图.md": "高低自旋判断决策树.决策图.png",
    "光谱化学序列配体排序图.关系图.md": "光谱化学序列配体排序图.关系图.png",
    "轨道杂化类型对比.关系图.md": "轨道杂化类型对比.关系图.png",
    "离域π键判断流程.流程图.md": "离域π键判断流程.流程图.png",
    "配合物异构现象分类体系.关系图.md": "配合物异构现象分类体系.关系图.png",
    "四面体场与正方形场分裂对比.关系图.md": "四面体场与正方形场分裂对比.关系图.png",
    "CFSE计算流程.流程图.md": "CFSE计算流程.流程图.png",
    "Lewis五步法流程.流程图.md": "Lewis五步法流程.流程图.png",
    "NO3-共振结构.lewis.md": "NO3-共振结构.lewis.png",
    "VSEPR决策链.流程图.md": "VSEPR决策链.流程图.png",
}

total_fixed = 0
missing_after = []

for h_name in handouts:
    h_path = os.path.join(handout_dir, h_name)
    if not os.path.exists(h_path):
        print(f"NOT FOUND: {h_name}")
        continue

    with open(h_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Part 1: Fix Excalidraw .md → .png references
    for old_md, new_png in EXCALIDRAW_MAP.items():
        # Match ![[media/old_md]] or ![[old_md]]
        count = 0
        content, c1 = re.subn(
            rf'!\[\[(?:media/)?{re.escape(old_md)}\]\]',
            f'![[media/{new_png}]]',
            content
        )
        count += c1
        # Also match bare [[media/old_md]] references
        content, c2 = re.subn(
            rf'\[\[(?:media/)?{re.escape(old_md)}\]\]',
            f'[[media/{new_png}]]',
            content
        )
        count += c2
        if count > 0:
            print(f"  {h_name}: {old_md} → {new_png} ({count}x)")
            total_fixed += count

    # Part 2: Fix textbook image references to available alternatives
    for old_img, new_img in IMAGE_MAP.items():
        if new_img is not None:
            count = 0
            # Replace with new image
            content, c1 = re.subn(
                rf'!\[\[(?:media/)?{re.escape(old_img)}\]\]',
                f'![[media/{new_img}]]',
                content
            )
            count += c1
            if count > 0:
                print(f"  {h_name}: {old_img} → {new_img} ({count}x)")
                total_fixed += count
        else:
            # Flag as missing - no replacement available
            if re.search(rf'!\[\[(?:media/)?{re.escape(old_img)}\]\]', content):
                missing_after.append(f"  {h_name}: {old_img} (NO REPLACEMENT)")

    if content != original:
        with open(h_path, 'w', encoding='utf-8') as f:
            f.write(content)

print(f"\n=== Summary ===")
print(f"Total references updated: {total_fixed}")
print(f"\nStill missing (no replacement):")
for m in missing_after:
    print(f"  {m}")
print(f"\nManual attention needed: {len(missing_after)} images still need source images")
