# -*- coding: utf-8 -*-
r"""CM-56-02 v2：按索引定位 `$$` 块并整块替换（源验证）。"""
import io, os, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
B = chr(92); D = B + 'Delta'
p = '04-题库/2026机构初赛模拟题/chemy/题-CM-56-02-近日美国普林斯顿大学的研究人.md'
bak = '.workbuddy/tmp/opt_pipe/_bak/cm5602b_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
shutil.copy2(p, os.path.join(bak, os.path.basename(p)))

t = io.open(p, encoding='utf-8-sig').read()
# 定位：`2-2-2` 之后的第一个 `$$`
a = t.find('2-2-2')
s = t.find('$$', a)
e = t.find('$$', s + 2)
assert s > 0 and e > s, '定位失败'
block = t[s:e + 2]
print('--- 原块（%d 字符）---' % len(block))
print(block)

new = ('$$\n'
       + B + 'omega_{(N_2)} = ' + B + 'frac{n_{(N_2)}}{n_{' + B + 'text{总}}} ' + B + 'times 100' + B + '% = '
       + B + 'frac{P_{(N_2)}}{P_{' + B + 'text{总}}} ' + B + 'times 100' + B + '% = '
       + B + 'frac{26.375' + B + ',' + B + 'mathrm{kPa}}{101.325' + B + ',' + B + 'mathrm{kPa}} '
       + B + 'times 100' + B + '% = 26.03' + B + '%'
       + '\n$$')
t2 = t[:s] + new + t[e + 2:]
io.open(p, 'w', encoding='utf-8', newline='').write(t2)
print('✅ 已修 %d → %d 字节' % (len(t), len(t2)))
print('残留 Delta 数:', t2.count(D))
k = t2.find('2-2-2')
print('复验:', t2[k:k + 320].replace('\n', '⏎'))
