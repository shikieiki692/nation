#!/usr/bin/env python3
"""全面修复原子结构源文件"""
import os, re

hd = r'C:\Obsidion\妙妙屋\04-课件\学生讲义'
path = os.path.join(hd, '原子结构-超级充实版（自学完整）.md')

with open(path, encoding='utf-8') as f:
    src = f.read()

log = []

# === 1. 表格对齐线 ===
src = src.replace(':——:', ':---:')
src = src.replace('|:——', '|:---')
src = src.replace(':——|', ':---|')
log.append('表格对齐线 :—— → :---')

# === 2. ź 乱码 → 上标 ===
src = src.replace('ź', '¹')
log.append('ź → ¹ (上标)')

# === 3. m_l 格式 ===
# 在 $...$ 外部的 m_l → $m_l$
# 简单策略：把不在$$内的m_l包裹
import re as regex
parts = src.split('$$')
for i in range(0, len(parts), 2):
    parts[i] = re.sub(r'(?<!\$)m_l(?!\})', r'$m_l$', parts[i])
src = '$$'.join(parts)
log.append('m_l → $m_l$')

# === 4. 删除空括号 ===
src = re.sub(r'（\s*）', '', src)
log.append('空括号清理')

# === 5. 删除六、拓展与联系 章节 ===
# 匹配 ## 六、拓展与联系 到 ## 七、本节总结
src = re.sub(r'## 六、拓展与联系.*?(?=## 七、本节总结)', '', src, flags=re.DOTALL)
log.append('删除 六、拓展与联系')

# === 6. 缩小 七、本节总结·速查 表格为精简版 ===
# （保留内容但精简格式）
log.append('七、本节总结·速查 已保留')

# === 7. 延伸阅读只保留书籍 ===
idx = src.find('## 十、延伸阅读')
if idx > 0:
    end = src.find('##', idx + 5)
    if end == -1:
        end = src.find('\n*本讲义', idx)
    if end == -1:
        end = src.find('---', idx)
    if end > idx:
        # 只保留书籍行（包含无机化学/上海中学等）
        ext_sec = src[idx:end]
        new_ext = '## 十、延伸阅读\n\n'
        for line in ext_sec.split('\n'):
            if '《' in line or '教材' in line or '普化' in line or '上海中学' in line or '无机化学' in line:
                new_ext += line + '\n'
        if new_ext.strip() == '## 十、延伸阅读':
            new_ext += '- 普化原理第4版 Ch11\n- 宋天佑《无机化学》§5\n- 上海中学竞赛课程·化学·第一分册·第二讲\n'
        src = src[:idx] + new_ext + src[end:]
        log.append('延伸阅读精简')
    else:
        log.append('延伸阅读: 未找到结束位置')

# === 8. 铁律表格中的中文引号 ===
src = src.replace('“', '"')  # "
src = src.replace('”', '"')  # "

with open(path, 'w', encoding='utf-8') as f:
    f.write(src)

print('=== 修复完成 ===')
for item in log:
    print('  ' + item)

# 验证
src2 = open(path, encoding='utf-8').read()
checks = {'坏答案': 0, '好答案': 0, '«': 0, 'ź': 0, 'Œ': 0, ':——': 0}
for k in checks:
    checks[k] = src2.count(k)
    if checks[k] > 0:
        print(f'  残留 {k}: {checks[k]}处')
for k, v in checks.items():
    if v > 0:
        print(f'  ⚠️ {k} 仍有{v}处')
