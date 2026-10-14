# -*- coding: utf-8 -*-
"""卷族 docx 交付件完整性盘点：应有 vs 实有；标注哪几卷落后于卷 md。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/题组Word/初赛模拟卷/真题版式'
DOLD = '00-首页/题组Word/初赛模拟卷（老·I~IX）/真题版式'

VOLS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XIp',
        'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']
KINDS = ['学生版·真题版式', '答案与解析版·真题版式', '答题卡']

print('%-7s %-12s %-16s %-10s %s' % ('卷', '学生版', '答案版', '答题卡', '答案版 vs md'))
lack = []
for v in VOLS:
    md = '04-题库/初赛模拟卷%s（非有机·答案版）.md' % v
    mt = os.path.getmtime(md) if os.path.exists(md) else None
    row = []
    lag = ''
    for k in KINDS:
        p = os.path.join(D, '初赛模拟卷%s（非有机·%s）.docx' % (v, k))
        if os.path.exists(p):
            row.append('有')
            if k.startswith('答案') and mt:
                dt = os.path.getmtime(p)
                if dt < mt:
                    lag = '⚠️ 落后 %.0f 分' % ((mt - dt) / 60)
                else:
                    lag = '✅ 新于 md'
        else:
            row.append('—')
            lack.append((v, k))
    print('%-7s %-12s %-16s %-10s %s' % (v, row[0], row[1], row[2], lag))

print()
print('主目录 %s: %d 个 docx' % (D, len(glob.glob(D + '/*.docx'))))
print('老目录 %s: %d 个 docx' % (DOLD, len(glob.glob(DOLD + '/*.docx'))))
print()
print('缺失清单（%d 项）:' % len(lack))
for v, k in lack:
    print('   卷%-6s %s' % (v, k))
