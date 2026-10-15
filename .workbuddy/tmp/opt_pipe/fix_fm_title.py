# -*- coding: utf-8 -*-
"""修 09-审计报告/2026-10-07-换卡候选回源核验结论.md 的 FM title（内嵌裸双引号 ⇒ THROW）"""
import io, os, re, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
P = '09-审计报告/2026-10-07-换卡候选回源核验结论.md'
t = io.open(P, encoding='utf-8-sig').read()
m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---', t, re.S)
assert m, '无 FM'
fm = m.group(1)
old = 'title: "换卡候选回源核验结论（15 张 A 类"须换卡"）"'
assert fm.count(old) == 1, ('未按预期命中', fm.count(old))
new = "title: '换卡候选回源核验结论（15 张 A 类\"须换卡\"）'"
nfm = fm.replace(old, new)

# 备份
bak = '.workbuddy/tmp/opt_pipe/_bak/fm_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
shutil.copy2(P, os.path.join(bak, os.path.basename(P)))

rest = t[m.end():]
io.open(P, 'w', encoding='utf-8', newline='').write('---\n' + nfm + '\n---' + rest)
print('已修 FM title')
print('新 title 行:', [l for l in nfm.split('\n') if l.startswith('title:')][0])
print('备份:', bak)
