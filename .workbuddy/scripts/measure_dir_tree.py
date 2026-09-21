# -*- coding: utf-8 -*-
"""量 04-题库 目录树的 md 计数（严格：只数 .md，排除 .git）"""
import os, io

R = r'C:\Obsidion\妙妙屋'
QB = os.path.join(R, '04-题库')

def md(p):
    c = 0
    for dp, dn, fn in os.walk(p):
        if '.git' in dp.split(os.sep):
            continue
        c += sum(1 for f in fn if f.endswith('.md'))
    return c

def subdirs(p):
    if not os.path.isdir(p):
        return []
    return sorted([d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d))])

print('==== 04-题库 顶层 ====')
top_files = [f for f in os.listdir(QB) if os.path.isfile(os.path.join(QB, f)) and f.endswith('.md')]
print('顶层 md 文件数 =', len(top_files))
tops = subdirs(QB)
grand = 0
for d in tops:
    n = md(os.path.join(QB, d))
    grand += n
    print('  %-22s %5d' % (d, n))
print('子目录合计 =', grand, ' 全库 md =', md(QB))

print()
print('==== 教材习题 一级子目录 ====')
T = os.path.join(QB, '教材习题')
sub = subdirs(T)
print('子目录数 =', len(sub))
tot = 0
for d in sub:
    n = md(os.path.join(T, d))
    tot += n
    print('  %-26s %5d' % (d, n))
print('小计 =', tot)
root_files = [f for f in os.listdir(T) if f.endswith('.md')]
print('根层 md =', len(root_files), root_files)
print('教材习题 全部 md =', md(T))

print()
print('==== 各学科模块 ====')
for m in ['化学原理', '有机化学', '物理化学', '分析化学', '元素化学']:
    p = os.path.join(QB, m)
    if not os.path.isdir(p):
        print('  %s 不存在' % m); continue
    print('  %-8s 全部 %4d  文件 %3d' % (m, md(p), len([f for f in os.listdir(p) if f.endswith('.md')])))
    for d in subdirs(p):
        print('      %-22s %4d' % (d, md(os.path.join(p, d))))

print()
print('==== 真题 ====')
Z = os.path.join(QB, '真题')
print('  全部 md =', md(Z), ' 一级子目录 =', len(subdirs(Z)))
for d in subdirs(Z):
    print('      %-24s %5d' % (d, md(os.path.join(Z, d))))

print()
print('==== 其他顶层目录 ====')
for m in ['元文件', '教学改编题', '经典例题', '真题（无答案）']:
    p = os.path.join(QB, m)
    if os.path.isdir(p):
        print('  %-14s %5d  子目录 %s' % (m, md(p), subdirs(p)[:8]))

print()
print('==== 05-真题库 ====')
F = os.path.join(R, '05-真题库')
print('  全部 md =', md(F))
