# -*- coding: utf-8 -*-
r"""6 卷「缺图题」核查 · 第 1 步：扫非法转义别名 + 汇总核验器结果。
别名形态：`![[xxx.jpg\|250]]`（`|` 前多反斜杠）—— 会让正则把 `\|250` 吃进图名 ⇒ 全部对不上。
"""
import io, os, re, glob

ROOT = r"C:\Obsidion\妙妙屋"
VOLS = ['X', 'XI', 'XIp', 'XIV', 'XV', 'XVI']

print('=' * 96)
print('第 1 步：非法转义别名扫描（`![[xxx.jpg\\|N]]`）')
print('=' * 96)
tot = 0
for v in VOLS:
    for tag in ['学生版', '答案版']:
        p = os.path.join(ROOT, '04-题库', '初赛模拟卷%s（非有机·%s）.md' % (v, tag))
        if not os.path.isfile(p):
            continue
        d = io.open(p, encoding='utf-8-sig').read()
        # 形如 ![[hash.ext\|数字]]
        hits = re.findall(r'!\[\[([^\]]+?\\(?:jpg|jpeg|png))\\\|(\d+)\]\]', d)
        # 更宽松：任何 jpg/png 后紧跟 \|
        loose = re.findall(r'\.(?:jpg|jpeg|png)\\\|(\d+)', d)
        if loose:
            tot += len(loose)
            vals = sorted({x for x in loose})
            print('  %-5s %-4s 非法别名 %d 处（宽度值 %s）' % (v, tag, len(loose), ','.join(vals)))
        # 其它反斜杠残留
        other = len(re.findall(r'!\[\[[^\]]*\\\\[^\]|]', d))
        if other:
            print('  %-5s %-4s ⚠ 其它反斜杠残留 %d 处' % (v, tag, other))
print('-' * 96)
print('合计非法别名 %d 处' % tot)
