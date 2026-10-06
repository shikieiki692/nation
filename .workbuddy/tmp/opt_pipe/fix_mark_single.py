# -*- coding: utf-8 -*-
"""回修：把已改标卡的参考答案统一为**单行** MARK（首行即含「源确缺答案」，保证可被检测）。
识别依据：FM quality_warning 以「源确缺答案」开头。
用法：python fix_mark_single_line.py [--apply]
"""
import os, re, sys, glob

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
MARK = ('⛔ **源确缺答案**：源资料中确无本题解答（2026-10-06 逐卷核验，非提取遗漏）；'
        '本卡不可组卷，如需答案请另找外部资料。\n')

n = 0
for p in glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True):
    raw = open(p, 'rb').read()
    bom = raw[:3] == b'\xef\xbb\xbf'
    t = raw.decode('utf-8-sig').replace('\r\n', '\n')
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    if not m:
        continue
    if not re.search(r'^quality_warning:[ \t]*"源确缺答案', m.group(1), re.M):
        continue
    ia = t.find('## 参考答案'); ik = t.find('## 知识点映射')
    if not (ia > 0 and ik > ia):
        print('!! 结构异常', p); continue
    new = t[:ia] + '## 参考答案\n\n' + MARK + '\n' + t[ik:]
    if new != t:
        n += 1
        if APPLY:
            open(p, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + new.encode('utf-8'))
print('回修 %d 卡  %s' % (n, '[APPLY]' if APPLY else '[DRY-RUN]'))
