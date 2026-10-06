# -*- coding: utf-8 -*-
"""把「源确缺答案」的卡（①组）统一改标：参考答案区改为标准标记 + FM 补 quality_warning。
①组 = noans_list 中**答案册确实不存在**的卡（排除 ②③ 可回收组）。
用法：python mark_source_missing.py [--apply]
"""
import os, re, sys, csv

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv

# 可回收组的 source_file 关键字（这些**不改标**）
RECOVERABLE = [
    '春季-有机专题1试卷已优化', '春季-有机专题1试卷(已优化)',
    '化英社2026第40届决赛物化专题2试卷', '决赛夏季模拟试题1', '夏季模拟试题3',
    '夏季初赛模拟13', '模拟试题14',
    '4thZCHEM-UChO-Tour1', '4thZCHEM-UChO-Tour2',
    '5thZCHEM-UChO-Tour1', '5thZCHEM-UChO-Tour2',
    'XeChem模拟三（晶体）答案', 'XeChem模拟四答案', 'XeChem模拟五答案',
    '化学试卷-初赛模拟试题4+答案', '第41届chemy联赛',
    '伽马化学2026年五一模拟1-讲稿', '伽马化学2026年五一模拟2-讲稿',
    '伽马化学2026年五一模拟4-讲稿', '伽马化学2026年五一模拟5',
    '伽马化学2026年五一模拟6-讲稿',
]
MARK = ('⛔ **源确缺答案**：源资料中确无本题解答（2026-10-06 逐卷核验，非提取遗漏）。\n'
        '\n'
        '> 本卡**不可组卷**；如需答案请另找外部资料。\n')
QW = '源确缺答案（源资料无本题解答，2026-10-06 核验）；组卷不可用'

rows = list(csv.DictReader(open('.workbuddy/tmp/opt_pipe/noans_list.csv', encoding='utf-8-sig')))
sel, skip = [], []
for r in rows:
    if any(k in r['source_file'] for k in RECOVERABLE):
        skip.append(r); continue
    sel.append(r)

print('无答案卡 %d ⇒ 可回收(跳过) %d ，改标 %d' % (len(rows), len(skip), len(sel)))


def rewrite(path):
    raw = open(path, 'rb').read()
    bom = raw[:3] == b'\xef\xbb\xbf'
    t = raw.decode('utf-8-sig').replace('\r\n', '\n')
    ia = t.find('## 参考答案'); ik = t.find('## 知识点映射')
    assert ia > 0 and ik > ia, path
    new = t[:ia] + '## 参考答案\n\n' + MARK + '\n' + t[ik:]
    # FM: 补/换 quality_warning
    m = re.match(r'^---\n(.*?)\n---\n', new, re.S)
    if m:
        fm = m.group(1)
        line = 'quality_warning: "%s"' % QW
        if re.search(r'^quality_warning:[ \t]*.*$', fm, re.M):
            fm2 = re.sub(r'^quality_warning:[ \t]*.*$', line, fm, count=1, flags=re.M)
        else:
            fm2 = fm + '\n' + line
        new = '---\n' + fm2 + '\n---\n' + new[m.end():]
    if APPLY:
        open(path, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + new.encode('utf-8'))
    return new


n = 0
for r in sel:
    rewrite(r['path'])
    n += 1
print('处理 %d 卡  %s' % (n, '[APPLY]' if APPLY else '[DRY-RUN]'))
