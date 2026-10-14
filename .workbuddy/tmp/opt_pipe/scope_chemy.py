# -*- coding: utf-8 -*-
"""摸底：chemmy 卡里「内部培训资料」vs「公开合集」两条渠道，及卷内需改的来源行。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')

rows = []
for p in glob.glob('04-题库/2026机构初赛模拟题/chemy/题-*.md'):
    t = io.open(p, encoding='utf-8-sig').read()
    def g(k):
        m = re.search(r'^%s:\s*"?(.+?)"?\s*$' % k, t, re.M)
        return m.group(1) if m else ''
    rows.append((p, g('source'), g('source_norm'), g('source_file'), g('exam_stage')))

print('chemy 卡总数', len(rows))
print()
# 按 source_file 归组
byfile = collections.Counter(r[3] for r in rows)
print('=== source_file 分布（前 25）===')
for k, v in byfile.most_common(25):
    print('   %4d  %s' % (v, k or '(空)'))
print()
inner = [r for r in rows if r[3].startswith('2026机构初赛模拟题/10-chemy/')]
print('=== 内部资料（source_file 指向 10-chemy/）: %d 卡 ===' % len(inner))
c = collections.Counter(r[2] for r in inner)
for k, v in sorted(c.items()):
    print('   %3d  %s' % (v, k))
print()
print('=== 样例 source 字段（前 8）===')
for r in inner[:8]:
    print('   source     : %s' % r[1])
    print('   source_norm: %s' % r[2])
    print('   source_file: %s' % r[3])
    print()
print('=== source_file 是否真实存在（抽样 6）===')
for r in inner[:6]:
    for base in ['', '04-题库/', '06-外部资料导入/OCR/01-题目/2026年chemy夏令营/']:
        f = base + r[3].split('10-chemy/', 1)[-1] if '10-chemy/' in r[3] else None
        if f and os.path.exists(f):
            print('   HIT  %s' % f)
        elif f and os.path.exists('04-题库/2026机构初赛模拟题/10-chemy/'):
            pass
    print('   --- %s' % r[3])
