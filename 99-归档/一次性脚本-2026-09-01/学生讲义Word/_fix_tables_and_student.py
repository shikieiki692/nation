#!/usr/bin/env python3
"""
Convert list-formatted data to tables and generate student-only version.
"""

import re
import sys

INPUT = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（完整版）.md"
OUTPUT_TABLES = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（完整版）.md"
OUTPUT_STUDENT = r"C:\Obsidion\妙妙屋\04-课件\专题课\第一轮结构化学专题课-学生用合集（学生版-无解析）.md"

with open(INPUT, "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# PART 1: Convert list-formatted data to tables
# ============================================================

# 1. Solvent classification (lines ~220-224)
old_solvent = """**溶剂分类（考纲§11.2）：**
- 极性质子溶剂：$H_{2}$O, C$H_{3}$OH（有H可形成氢键）
- 极性非质子溶剂：DMSO, DMF（有偶极但无活泼H）
- 非极性溶剂：己烷, CC$l_{4}$
- 相似相溶原理：极性溶质溶于极性溶剂"""

new_solvent = """**溶剂分类（考纲§11.2）：**

| 类型 | 特点 | 示例 |
|:---|:---|:---|
| 极性质子溶剂 | 有H可形成氢键 | $H_{2}$O, C$H_{3}$OH |
| 极性非质子溶剂 | 有偶极但无活泼H | DMSO, DMF |
| 非极性溶剂 | 无偶极 | 己烷, CC$l_{4}$ |

> **相似相溶原理**：极性溶质溶于极性溶剂"""

if old_solvent in content:
    content = content.replace(old_solvent, new_solvent)
    print("[OK] Converted solvent classification to table")

# 2. gauche vs anti comparison (lines ~694-696)
old_gauche = """- **gauche**：C-H与C-F\*处于有利重叠 → 超共轭 → 稳定化
- **anti**：C-H与C-F\*重叠较差 → 超共轭较弱
- 这就是gauche效应的微观机制"""

new_gauche = """| 构象 | C-H与C-F\*重叠 | 超共轭 | 结果 |
|:---:|:---:|:---:|:---|
| **gauche** | 有利重叠 | 强 | 稳定化 |
| **anti** | 重叠较差 | 较弱 | 稳定化较弱 |

> 这就是gauche效应的微观机制"""

if old_gauche in content:
    content = content.replace(old_gauche, new_gauche)
    print("[OK] Converted gauche vs anti to table")

# 3. SP vs MC (lines ~744-746)
old_sp = """- **SP结构**：s$p^{3}$螺碳**打断共轭** → 两个芳香环π体系独立 → 共轭小 → ΔE大 → 吸收在紫外区
- **MC结构**：C-O断裂后螺碳变s$p^{2}$ → 共轭链连续 → 共轭扩展 → ΔE小 → 吸收在可见区
- SP → MC：共轭增大 → ΔE减小 → λ增大 → **红移**"""

new_sp = """| 结构 | 螺碳杂化 | 共轭体系 | ΔE | 吸收区 |
|:---:|:---:|:---|:---:|:---:|
| **SP** | s$p^{3}$ | 打断，两芳香环独立 | 大 | 紫外区 |
| **MC** | s$p^{2}$ | 连续，共轭扩展 | 小 | 可见区 |

> SP → MC：共轭增大 → ΔE减小 → λ增大 → **红移**"""

if old_sp in content:
    content = content.replace(old_sp, new_sp)
    print("[OK] Converted SP vs MC to table")

# 4. Structure characteristics (lines ~1136-1144) - 7 types
old_struct = """**每种结构的"一句话特征"**：

- **NaCl型**：两个互相穿插的fcc格子，N$a^{+}$占八面体空隙的一半
- **CsCl型**：简单立方格子，C$l^{-}$在顶点、C$s^{+}$在体心（或反过来）
- **闪锌矿型**：$S^{2-}$做fcc堆积，Z$n^{2+}$占据**一半四面体空隙**（交替占据）
- **萤石型**：C$a^{2+}$做fcc堆积，$F^{-}$占据**全部四面体空隙**（8个）→ 配位比8:4
- **金红石型**：T$i^{4+}$在八面体中心，$O^{2-}$形成八面体，每个$O^{2-}$被3个T$i^{4+}$共用
- **钙钛矿型**：A离子在顶点（12配位），B离子在体心（6配位，八面体），$O^{2-}$在面心
- **NiAs型**：As做hcp堆积，Ni占据**全部八面体空隙**"""

new_struct = """**每种结构的"一句话特征"**：

| 结构 | 一句话特征 |
|:---|:---|
| **NaCl型** | 两个互相穿插的fcc格子，N$a^{+}$占八面体空隙的一半 |
| **CsCl型** | 简单立方格子，C$l^{-}$在顶点、C$s^{+}$在体心（或反过来） |
| **闪锌矿型** | $S^{2-}$做fcc堆积，Z$n^{2+}$占据**一半四面体空隙**（交替占据） |
| **萤石型** | C$a^{2+}$做fcc堆积，$F^{-}$占据**全部四面体空隙**（8个）→ 配位比8:4 |
| **金红石型** | T$i^{4+}$在八面体中心，$O^{2-}$形成八面体，每个$O^{2-}$被3个T$i^{4+}$共用 |
| **钙钛矿型** | A离子在顶点（12配位），B离子在体心（6配位，八面体），$O^{2-}$在面心 |
| **NiAs型** | As做hcp堆积，Ni占据**全部八面体空隙** |"""

if old_struct in content:
    content = content.replace(old_struct, new_struct)
    print("[OK] Converted structure characteristics to table")

# 5. Coordination bond basics (lines ~2384-2388)
old_coord = """**配位键基本概念（§12.1）：**
- 配位键 = 一方提供孤对电子，另一方提供空轨道
- 配体：提供孤对电子的分子或离子
- 中心原子/离子：接受孤对电子的金属离子
- 配位数：直接与中心原子成键的配位原子数"""

new_coord = """**配位键基本概念（§12.1）：**

| 概念 | 定义 |
|:---|:---|
| 配位键 | 一方提供孤对电子，另一方提供空轨道 |
| 配体 | 提供孤对电子的分子或离子 |
| 中心原子/离子 | 接受孤对电子的金属离子 |
| 配位数 | 直接与中心原子成键的配位原子数 |"""

if old_coord in content:
    content = content.replace(old_coord, new_coord)
    print("[OK] Converted coordination bond basics to table")

# 6. Chelate effect (lines ~2390-2394)
old_chelate = """**螯合效应（§12.2）：**
- 螯合物 = 含多齿配体的配合物（en=二齿, EDTA=六齿）
- 螯合效应：螯合物比同类单齿配体配合物更稳定
- 本质：**熵驱动**——螯合反应释放更多配体分子，ΔS > 0
- 例：[Ni(N$H_{3}$)₆]²⁺ + 3en → [Ni(en)₃]²⁺ + 6N$H_{3}$，K >> 1"""

new_chelate = """**螯合效应（§12.2）：**

| 概念 | 说明 |
|:---|:---|
| 螯合物 | 含多齿配体的配合物（en=二齿, EDTA=六齿） |
| 螯合效应 | 螯合物比同类单齿配体配合物更稳定 |
| 本质 | **熵驱动**——螯合反应释放更多配体分子，ΔS > 0 |
| 示例 | [Ni(N$H_{3}$)₆]²⁺ + 3en → [Ni(en)₃]²⁺ + 6N$H_{3}$，K >> 1 |"""

if old_chelate in content:
    content = content.replace(old_chelate, new_chelate)
    print("[OK] Converted chelate effect to table")

# 7. Intermolecular forces (line ~207) - this is a ranking, keep as is (not table-suitable)

# 8. IE anomalies (lines ~183-186) - keep as list (prose-like)

# 9. Boiling point comparison (lines ~214-218) - keep as numbered list (procedural)

# Save the table-fixed version
with open(OUTPUT_TABLES, "w", encoding="utf-8") as f:
    f.write(content)
print(f"\n[SAVED] Table-fixed MD: {OUTPUT_TABLES}")

# ============================================================
# PART 2: Generate student-only version (no answers)
# ============================================================

lines = content.split("\n")
student_lines = []
skip = False
in_solution = False
current_section = ""
in_blockquote_solution = False

i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Detect "### 解析" headers - skip everything until next ### or ## or ---
    if stripped.startswith("### 解析") or stripped.startswith("**解析**"):
        skip = True
        i += 1
        continue

    # Detect answer sections: "**X.X.X 答案**" or "**答案**"
    if re.match(r'\*\*\d+[\.\d]*\s*答案\*\*', stripped) or stripped == "**答案**":
        skip = True
        i += 1
        continue

    # Detect "### 真题N" or "## " or "---" or "### 工具" or "### 补充" - stop skipping
    if skip:
        if (stripped.startswith("### 真题") or
            stripped.startswith("## ") or
            stripped == "---" or
            stripped.startswith("### 工具") or
            stripped.startswith("### 补充") or
            stripped.startswith("# ") or
            stripped.startswith("> **")):
            skip = False
        else:
            i += 1
            continue

    # Skip 易错提醒 blocks
    if "⚠️ **易错提醒**" in stripped:
        # Skip until next empty line or next section
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line == "" or next_line.startswith("#") or next_line.startswith("###"):
                break
            i += 1
        continue

    # Skip "**关键易错**" blocks
    if "**关键易错**" in stripped:
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line == "" or next_line.startswith("#") or next_line.startswith("###"):
                break
            i += 1
        continue

    student_lines.append(line)
    i += 1

student_content = "\n".join(student_lines)

# Clean up excessive blank lines (more than 2 consecutive)
student_content = re.sub(r'\n{4,}', '\n\n\n', student_content)

# Save student version
with open(OUTPUT_STUDENT, "w", encoding="utf-8") as f:
    f.write(student_content)
print(f"[SAVED] Student-only MD: {OUTPUT_STUDENT}")

# Count stats
orig_tables = content.count("\n|:")
student_tables = student_content.count("\n|:")
print(f"\n[STATS]")
print(f"  Table-fixed MD: {len(content)} chars, {content.count(chr(10))} lines")
print(f"  Student-only MD: {len(student_content)} chars, {student_content.count(chr(10))} lines")
print(f"  Tables in full version: {orig_tables}")
print(f"  Tables in student version: {student_tables}")
