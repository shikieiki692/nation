#!/usr/bin/env python3
"""修复铁律表格 + 检查所有残留问题"""
import os

hd = r'C:\Obsidion\妙妙屋\04-课件\学生讲义'
path = os.path.join(hd, '原子结构-超级充实版（自学完整）.md')

with open(path, encoding='utf-8') as f:
    src = f.read()

# 1. 铁律表格 → bullet list
old_table = '> **好答案 vs 坏答案对比**：'
if old_table in src:
    # 找到整块表格
    start = src.find(old_table)
    end = src.find('\n>\n', start)
    if end == -1:
        end = src.find('\n\n', start)
    if end > start:
        table_block = src[start:end]
        new_block = '''**好答案 vs 坏答案对比**：

- **碱金属密度为什么不单调？**
  ❌ "因为原子半径和质量相互影响"
  ✅ "密度 = 质量/体积。同族向下质量增加快于半径增大——因此密度先减后增"
- **卤素电子亲和能为什么 F<Cl？**
  ❌ "因为 F 半径小，排斥大"
  ✅ "F 价层电子云密度极高，加电子后电子间排斥强烈——放能反而低于 Cl"
- **铁系金属熔点为什么从左到右递减？**
  ❌ "因为金属键减弱"
  ✅ "Fe→Co→Ni：反键电子数增加（6→7→8）→ 净成键电子数减少 → 键能下降 → 熔点递减"'''

        src = src[:start] + new_block + src[end:]
        print('✅ 铁律表格→bullet list')
else:
    print('⏭ 铁律表格未找到')

# 2. 检查残留的 J_dd (应该已经被替换)
for old in ['J_dd', 'J_ds', 'J_ss']:
    if old in src:
        # 检查是否在 LaTeX 公式内
        idx = src.find(old)
        context = src[max(0,idx-30):idx+30]
        print(f'  ⚠️ 残留 J_: {context.strip()[:60]}')

# 3. 检查 Œ 和 ź
for ch in ['Œ', 'ź']:
    if ch in src:
        print(f'  ⚠️ 残留 {ch}: {src[src.find(ch):src.find(ch)+30]}')

# 4. 检查 4+0.7 类似公式
import re
for m in re.finditer(r'\d+[+]\d+[.]\d', src):
    print(f'  ⚠️ 可能公式: {m.group()}')

# 5. 检查空括号 （）
empty = len(re.findall(r'（\s*）', src))
if empty > 0:
    src = re.sub(r'（\s*）', '', src)
    print(f'  ✅ 清理空括号: {empty}处')

# 6. 检查 ź 在 Ga 排布式中的上下文
for m in re.finditer(r'Ga.*?\]\S+', src):
    print(f'  ⚠️ Ga排布式: {m.group()[:50]}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(src)
print('✅ 完成')
