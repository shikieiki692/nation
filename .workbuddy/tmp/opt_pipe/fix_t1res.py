# -*- coding: utf-8 -*-
r"""T1 RESIDUAL：逐条人工定性的 14 处「删 Δ」（显式清单 + 断言 + 备份）。"""
import io, os, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
B = chr(92)
D = B + 'Delta'
BAK = '.workbuddy/tmp/opt_pipe/_bak/t1res_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(BAK, exist_ok=True)

BASE = '04-题库/2026机构初赛模拟题/chemy/'
# (文件, 原串, 新串, 说明)
FIX = [
 ('题-CM-150-03-采用吸光光度法研究氨苄西林A.md', '\\mathrm{' + D + '(A)}', '\\mathrm{(A)}', '吸光光度式：Δ(A)→(A)'),
 ('题-CM-158-13-化学人应该保持一颗赤子之心童.md', '\\mathrm { ' + D + ' J }', '\\mathrm { J }', 'NMR 偶合常数 ΔJ→J'),
 ('题-CM-165-02-顾名思义超酸是一类酸度极强的.md', '\\mathrm { ' + D + ' V }', '\\mathrm { V }', '钒原子 ΔV→V'),
 ('题-CM-165-04-4-1的制备思路与前人报道的.md', '\\mathrm { ' + D + ' V }', '\\mathrm { V }', 'V 字型 ΔV→V'),
 ('题-CM-169-07-7-2比较并解释A和B与PC.md', '\\mathrm { ' + D + ' S _{ N } 1 }', '\\mathrm { S _{ N } 1 }', 'ΔS_N1→S_N1'),
 ('题-CM-170-08-有科学家设计了一种双空腔离子.md', '\\mathrm { ' + D + ' pH = }', '\\mathrm { pH = }', 'ΔpH→pH'),
 ('题-CM-172-03-3-1芳基重氮盐是合成卤代芳.md', '\\mathrm { ' + D + ' S _{ 8 } }', '\\mathrm { S _{ 8 } }', '单质硫 ΔS8→S8'),
 ('题-CM-53-03-八元环化合物X摩尔质量可由同.md', '\\mathrm { ' + D + ' S _{ 8 } }', '\\mathrm { S _{ 8 } }', '评分注 ΔS8→S8'),
 ('题-CM-178-05-高压氮化物的结构.md', '\\mathrm { ' + D + ' N }', '\\mathrm { N }', '氮原子 ΔN→N'),
 ('题-CM-60-09-窗烷是指由一个碳原子的四根共.md', '\\mathrm { ' + D + ' TiCl _{ 4 } }', '\\mathrm { TiCl _{ 4 } }', '反应物 ΔTiCl4→TiCl4'),
 ('题-CM-73-06-最近的计算研究发现在特殊条件.md', '\\mathrm { ' + D + ' H }', '\\mathrm { H }', '氢负离子 ΔH-→H-'),
 ('题-CM-73-09-簇合物在主族元素发展中起着比.md', '\\mathrm { ' + D + ' N }', '\\mathrm { N }', '氮原子 ΔN→N'),
]
# 逐文件、逐串（replace all，并核对次数）
tot = 0
for fn, old, new, why in FIX:
    p = BASE + fn
    if not os.path.isfile(p):
        print('MISS', fn); continue
    t = io.open(p, encoding='utf-8-sig').read()
    n = t.count(old)
    if n == 0:
        print('⚠️ 未命中:', fn, repr(old)[:40]); continue
    dst = os.path.join(BAK, fn)
    if not os.path.exists(dst):
        shutil.copy2(p, dst)
    t2 = t.replace(old, new)
    io.open(p, 'w', encoding='utf-8', newline='').write(t2)
    tot += n
    print('%-46s %d 处  %s' % (fn[:44], n, why))
print()
print('共 %d 处；备份 %s' % (tot, BAK))
# 复验：D2 残留
import re
run = re.compile(r'(\\+)Delta')
print('--- 复验（各文件 Delta 残留，减 1 反斜杠）---')
for fn in sorted({f[0] for f in FIX}):
    p = BASE + fn
    t = io.open(p, encoding='utf-8-sig').read()
    print('  %-46s 残留 Delta %d' % (fn[:44], len(re.findall(r'\\Delta', t))))
