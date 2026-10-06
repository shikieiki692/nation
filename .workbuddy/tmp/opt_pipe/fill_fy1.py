# -*- coding: utf-8 -*-
"""回填方圆 FY-01 六卡参考答案（图来自 有机化学测试题1 答案.pdf 裁区）。"""
import os, sys, glob

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
D = '04-题库/2026机构初赛模拟题/方圆/images/'
B = '04-题库/2026机构初赛模拟题/方圆/'
Q = {'FY-01-02': 2, 'FY-01-03': 3, 'FY-01-05': 5, 'FY-01-06': 6, 'FY-01-08': 8, 'FY-01-09': 9}

for cid, q in Q.items():
    fs = sorted(glob.glob(D + 'fy1_%s_*.png' % cid))
    if not fs:
        print('!! 无裁图 %s' % cid); continue
    imgs = '\n'.join('![](images/%s)' % os.path.basename(f) for f in fs)
    md = ('（源：方圆《有机化学测试题1》参考答案 · 第 %d 题；按原册裁区，保留结构图与答案）\n\n' % q
          + imgs + '\n\n> 📌 据源答案册逐题裁区回填。\n')
    card = glob.glob(B + '题-%s-*.md' % cid)[0]
    t = open(card, encoding='utf-8-sig').read().replace('\r\n', '\n')
    ia = t.find('## 参考答案'); ik = t.find('## 知识点映射')
    assert ia > 0 and ik > ia, card
    new = t[:ia] + '## 参考答案\n\n' + md + '\n' + t[ik:]
    if APPLY:
        open(card, 'w', encoding='utf-8', newline='\n').write(new)
    print('%-12s 第%d题  %d 图' % (cid, q, len(fs)))
print('%s' % ('[APPLY]' if APPLY else '[DRY-RUN]'))
