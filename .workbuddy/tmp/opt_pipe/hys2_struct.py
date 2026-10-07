# -*- coding: utf-8 -*-
"""列答案册 第3题 区的 小问标记 + 行首，判断有无可机器切分边界。"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
D = r'C:\Obsidion\妙妙屋\2026机构初赛模拟题\07-化英社'
p = os.path.join(D, '第40届化英社化学奥林匹克决赛夏季模拟试题2参考答案.md')
t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
i = t.find('## 第3题')
j = t.find('## 第 5 题', i)
seg = t[i:j]
print('第3题段 %d 字' % len(seg))
print('--- 小问标记（3-x / ## N-x）---')
for m in re.finditer(r'(?m)^(#{0,4}[ \t]*)(\*{0,2})(3\s*[-－]\s*\d(?:\s*[-－]\s*\d)?)', seg):
    print('  @%5d %-58s' % (m.start(), (m.group(1) + m.group(2) + m.group(3))[:58]))
print('--- 疑「解答起始」标记 ---')
for pat in ['答案', '解析', '解：', '评分', '分）', '分,', '共']:
    n = len(re.findall(pat, seg))
    print('  %-6s %d' % (pat, n))
