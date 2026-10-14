# -*- coding: utf-8 -*-
r"""修 Cannizzaro 卡的 `\\mathrm` v2：支持内层花括号；断言正确；未通过则不写盘。"""
import io, os, re, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')

P = '04-题库/教材习题/ABOC/题-128-ABOC-Ch4-4.13.1-Cannizzaro 康尼查罗 反应是醛在强碱浓溶液中发生的.md'
BAK = '.workbuddy/tmp/opt_pipe/_bak/bs2_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(BAK, exist_ok=True)
shutil.copy2(P, os.path.join(BAK, os.path.basename(P)))

t = io.open(P, encoding='utf-8-sig').read()
RUN = re.compile(r'(\\+)mathrm')

def stats(s):
    d = {1: 0, 2: 0, 3: 0, '4+': 0}
    for m in RUN.finditer(s):
        k = len(m.group(1))
        d[k if k <= 3 else '4+'] += 1
    return d

before = stats(t)
# 支持一层内层花括号
PAT2 = re.compile(r'(?<!\\)\\\\(?!\\)mathrm\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}')

def rep(m):
    return r'\mathrm{%s}' % m.group(1).strip()
t2 = PAT2.sub(rep, t)
after = stats(t2)

print('修复前:', before)
print('修复后:', after)
print('字节 %d → %d' % (len(t), len(t2)))
if after[2] != 0:
    print('❌ 仍有 %d 处 2 反斜杠 ⇒ 不写盘' % after[2])
    raise SystemExit(1)
if after[3] != before[3] or after['4+'] != before['4+']:
    print('❌ 3/4+ 反斜杠被改动 ⇒ 不写盘')
    raise SystemExit(1)
io.open(P, 'w', encoding='utf-8', newline='').write(t2)
print('✅ 已写盘；备份', BAK)
