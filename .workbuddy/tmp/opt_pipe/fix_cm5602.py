# -*- coding: utf-8 -*-
r"""CM-56-02：按 32 届答案 PDF p47 原文重写 2-2-2 的 ω(N2) 公式块（源验证）。"""
import io, os, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
B = chr(92); D = B + 'Delta'
p = '04-题库/2026机构初赛模拟题/chemy/题-CM-56-02-近日美国普林斯顿大学的研究人.md'
bak = '.workbuddy/tmp/opt_pipe/_bak/cm5602_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
shutil.copy2(p, os.path.join(bak, os.path.basename(p)))

t = io.open(p, encoding='utf-8-sig').read()
i = t.find('2-2-2')
j = t.find('## 知识点映射', i)
print('--- 卡内原块 ---')
print(repr(t[i:j]))

old = ('$$' + '\n-\n-\n-\n'
       + B + 'begin{array} { r } { ' + B + 'omega _{ ' + B + 'mathrm { ' + D + B + 'phi } ( N _{ 2 } ) } = '
       + B + 'frac { n _{ ' + B + 'mathrm { ' + D + '( } N _{ 2 } ) } } { n _{ ' + B + 'mathrm { ' + D + B + 'xi } } } '
       + B + 'times 100 ' + B + '% = ' + B + 'frac { P _{ ' + B + 'mathrm { ' + D + '( } N _{ 2 } ) } } { P _{ ' + B + 'mathrm { ' + D + B + 'xi } } } '
       + B + 'times 100 ' + B + '% = ' + B + 'frac { 26.375 ' + B + 'mathrm { kpa } } { 101.325 ' + B + 'mathrm { kpa } } '
       + B + 'times 100 ' + B + '% = 26.03 ' + B + '% } ' + B + 'end{array}' + '\n' + '$$')
new = ('$$' + '\n'
       + B + 'omega_{(N_2)} = ' + B + 'frac{n_{(N_2)}}{n_{' + B + 'text{总}}} ' + B + 'times 100' + B + '% = '
       + B + 'frac{P_{(N_2)}}{P_{' + B + 'text{总}}} ' + B + 'times 100' + B + '% = '
       + B + 'frac{26.375' + B + ',' + B + 'mathrm{kPa}}{101.325' + B + ',' + B + 'mathrm{kPa}} ' + B + 'times 100' + B + '% = 26.03' + B + '%'
       + '\n' + '$$')
print()
print('命中次数:', t.count(old))
assert t.count(old) == 1, '未按预期命中，未写盘'
t2 = t.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='').write(t2)
print('✅ 已修 %d → %d 字节' % (len(t), len(t2)))
print('残留 Delta 数:', t2.count(D))
k = t2.find('2-2-2')
print('复验:', t2[k:k + 300].replace('\n', '⏎'))
