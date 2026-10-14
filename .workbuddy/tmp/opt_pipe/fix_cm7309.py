# -*- coding: utf-8 -*-
r"""CM-73-09：`\mathrm{\Delta}^{2}$ -` → `^{2-}$`（电荷上标，由同题参考答案区佐证）。"""
import io, os, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
B = chr(92); D = B + 'Delta'
p = '04-题库/2026机构初赛模拟题/chemy/题-CM-73-09-簇合物在主族元素发展中起着比.md'
bak = '.workbuddy/tmp/opt_pipe/_bak/cm7309b_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
shutil.copy2(p, os.path.join(bak, os.path.basename(p)))

t = io.open(p, encoding='utf-8-sig').read()
old = B + 'mathrm{' + D + '}^{2}$ -'
new = '^{2-}$'
n = t.count(old)
print('命中 %d 次' % n)
assert n == 1, '命中数不为 1，未写盘'
t2 = t.replace(old, new)
# 断言：新串无 \mathrm{\Delta}，且 $ 数不变
assert B + 'mathrm{' + D + '}' not in t2
assert t.count('$') == t2.count('$')
io.open(p, 'w', encoding='utf-8', newline='').write(t2)
print('✅ 已修：%d → %d 字节' % (len(t), len(t2)))
i = t2.find('9-1-1')
print('复验片段:', t2[i:i + 80].replace('\n', '⏎'))
