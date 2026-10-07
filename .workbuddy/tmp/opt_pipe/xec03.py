# -*- coding: utf-8 -*-
"""看 XeChem 模拟三（晶体）的 试题 vs 答案（第4题附近）+ 现卡内容。"""
import os, re, sys, csv
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Obsidion\妙妙屋'
D = os.path.join(ROOT, '2026机构初赛模拟题', '03-XeChem')

Q = os.path.join(D, 'Xechem模拟三（晶体）.md')
A = os.path.join(D, 'Xechem模拟三（晶体）答案.md')
for lbl, p in (('试题', Q), ('答案', A)):
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    print('=' * 100)
    print('%s  %d 字' % (lbl, len(t)))
    for m in list(re.finditer(r'(?m)^#{1,6} .*$', t))[:14]:
        print('   @%6d %s' % (m.start(), m.group(0)[:70]))

# 现卡
rows = list(csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')))
r = [x for x in rows if 'XeC-03-04' in os.path.basename(x['path'])][0]
cp = os.path.join(ROOT, r['path'])
t = open(cp, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
print('=' * 100)
print('现卡 %s' % os.path.basename(cp))
print('  题面区 %d 字：' % len(t[i:j]))
print(re.sub(r'\n{2,}', '\n', t[i:j])[:800])
print('  答案区 %d 字：' % len(t[j:k]))
print(re.sub(r'\n{2,}', '\n', t[j:k])[:500])
