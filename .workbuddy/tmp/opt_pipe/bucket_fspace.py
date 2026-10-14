# -*- coding: utf-8 -*-
r"""给 `fspace` 的 474 处按「左侧语境」分桶，判定哪些是真缺陷（只读）。"""
import os, re, glob, collections
os.chdir(r'C:\Obsidion\妙妙屋')
R = r'C:\Obsidion\妙妙屋'
ROOTS = ["04-题库/教材习题", "04-题库/真题", "04-题库/化学原理", "04-题库/有机化学"]
RX = re.compile(r'([A-Za-z0-9])[ \t]+\$[_^]\{')

buckets = collections.Counter()
samples = collections.defaultdict(list)
files = []
for root in ROOTS:
    files += glob.glob(os.path.join(R, root, '**', '题-*.md'), recursive=True)

for fp in sorted(set(files)):
    t = open(fp, encoding='utf-8-sig').read()
    for m in RX.finditer(t):
        base = m.group(1)
        pre2 = t[max(0, m.start() - 2):m.start()]          # 基底左侧 2 字符
        pre1 = pre2[-1] if pre2 else ''
        # 分桶
        if base.isdigit() and (pre1 in '-./、' or re.search(r'\d[-.]$', pre2)):
            k = 'A 题号尾部（8-4 $…）→ 合法'
        elif base.isdigit() and pre1.isalpha():
            k = 'B 字母+数字（H2 $…）→ 可疑'
        elif base.isalpha() and pre1.isalpha():
            k = 'C 字母+字母（CH $…）→ 可疑'
        elif base.isalpha() and (pre1 in '-—（）()' or pre1 == '' or pre1 == ' '):
            k = 'D 词首字母（如 M $…）→ 可疑'
        else:
            k = 'E 其它'
        buckets[k] += 1
        if len(samples[k]) < 4:
            s = max(0, m.start() - 26)
            samples[k].append(t[s:m.end() + 14].replace('\n', '⏎'))

for k, v in buckets.most_common():
    print('%-30s %3d 处' % (k, v))
    for s in samples[k]:
        print('      …%s…' % s)
    print()
