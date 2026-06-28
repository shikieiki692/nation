#!/usr/bin/env python3
"""全面修复原子结构源文件 — 不破坏frontmatter"""
import re, os

hd = r'C:\Obsidion\妙妙屋\04-课件\学生讲义'
path = os.path.join(hd, '原子结构-超级充实版（自学完整）.md')

with open(path, encoding='utf-8') as f:
    src = f.read()

# 分离 frontmatter 和正文
fm_end = src.find('---\n', 3) + 4  # 第二个 ---
if src.startswith('---\n') and fm_end > 4:
    frontmatter = src[:fm_end]
    body = src[fm_end:]
else:
    frontmatter = ''
    body = src

log = []

# 修复1: J_dd → $J_{dd}$
for old, new in [('J_dd', '$J_{dd}$'), ('J_ds', '$J_{ds}$'), ('J_ss', '$J_{ss}$')]:
    c = body.count(old)
    if c > 0:
        body = body.replace(old, new)
        log.append(f'J_* → $J_{{*}}$: {c}处')

# 修复2: Œ0 / Œ → 分数线的 /
c = body.count('Œ0') + body.count('Œ')
if c > 0:
    body = body.replace('Œ0', '')  # 修复乱码
    body = body.replace('Œ', '/')
    log.append(f'Œ码 → /: {c}处')

# 修复3: ź 乱码
c = body.count('ź')
if c > 0:
    body = body.replace('ź', '')
    log.append(f'ź乱码已移除: {c}处')

# 修复4: LaTeX表格列分隔符 :--- 不要被替换
# 检查哪些 --- 在表格中 (紧挨 | 的行)
def replace_dashes_outside_tables(text):
    lines = text.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        # 表格行中的 --- 不替换（:--- 或 ---:）
        if stripped.startswith('|') or ':---' in stripped or '---:' in stripped:
            result.append(line)
        # 公式中的 --- 不替换
        elif stripped.startswith('$$') or stripped.endswith('$$'):
            result.append(line)
        # 正文 --- → ——
        elif '---' in line:
            result.append(line.replace('---', '——'))
        else:
            result.append(line)
    return '\n'.join(result)

body = replace_dashes_outside_tables(body)
log.append('正文 --- → —— (表格/公式中的保留)')

# 修复5: 铁律表格 → bullet list
old_table = '''| 题目 | ❌ 坏答案 | ✅ 好答案 |
|:---|:---|:---|
| 碱金属密度为什么不单调？ | "因为原子半径和质量相互影响" | "密度 = 质量/体积。同族向下，质量增加（+14→+16 AMU/周期）的速度快于半径增大（+30%→+15%/周期）的增速——因此密度先减后增" |
| 卤素电子亲和能为什么 F<Cl？ | "因为 F 半径小，排斥大" | "F 的价层电子云密度极高，加电子后新增电子受到已存在电子的强烈排斥——放出的能量反而低于 Cl" |
| 铁系金属熔点为什么从左到右递减？ | "因为金属键减弱" | "Fe→Co→Ni：3d 轨道中反键电子数增加（6→7→8）→ 金属键中的净成键电子数减少 → 键能下降 → 熔点递减" |'''

new_list = '''**好答案 vs 坏答案对比**：

- **碱金属密度为什么不单调？**
  ❌ "因为原子半径和质量相互影响"
  ✅ "密度 = 质量/体积。同族向下质量增加快于半径增大——因此密度先减后增"

- **卤素电子亲和能为什么 F<Cl？**
  ❌ "因为 F 半径小，排斥大"
  ✅ "F 价层电子云密度极高，加电子后电子间排斥强烈——放能反而低于 Cl"

- **铁系金属熔点为什么从左到右递减？**
  ❌ "因为金属键减弱"
  ✅ "Fe→Co→Ni：反键电子数增加（6→7→8）→ 净成键电子数减少 → 键能下降 → 熔点递减"'''

if old_table in body:
    body = body.replace(old_table, new_list)
    log.append('铁律表格 → bullet list')
else:
    # 尝试匹配简化版
    table_lines = [l for l in body.split('\n') if '坏答案' in l or '好答案' in l]
    if table_lines:
        log.append(f'铁律表格未精确匹配(共{len(table_lines)}行相关) —— 手动检查')
    else:
        log.append('铁律表格未找到')

# 修复6: 单独占一行的 --- 分隔符清理（保留 frontmatter 和表格的）
lines = body.split('\n')
new_lines = []
in_math = False
for line in lines:
    s = line.strip()
    if s.startswith('$$'):
        in_math = not in_math
    if not in_math and (s == '---' or s == '——'):
        # 保留表格分隔行
        continue
    new_lines.append(line)
body = '\n'.join(new_lines)
log.append('独立 --- 行清理')

# 拼接
result = frontmatter + body
with open(path, 'w', encoding='utf-8') as f:
    f.write(result)

print('=== 修复完成 ===')
for item in log:
    print(f'  ✅ {item}')
