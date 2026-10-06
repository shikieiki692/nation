# -*- coding: utf-8 -*-
"""通用回填：按 TSV 映射把裁好的答案图写进各卡「## 参考答案」。
用法：python fill_from_crops.py <imgdir> <map.tsv> <src_label> [--apply]
TSV 行：<card_glob> \t <img_prefix> \t <小节说明>
（card_glob 可命中多张卡 —— 用于 ID 撞车下的同题多卡）
"""
import os, sys, glob

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
imgdir, mapf, label = sys.argv[1], sys.argv[2], sys.argv[3]
APPLY = '--apply' in sys.argv

n = 0
for line in open(mapf, encoding='utf-8'):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    parts = line.split('\t')
    card_glob, prefix = parts[0], parts[1]
    note = parts[2] if len(parts) > 2 else ''
    fs = sorted(glob.glob(os.path.join(imgdir, prefix + '_*.png')))
    if not fs:
        print('!! 无裁图 %s' % prefix); continue
    cards = glob.glob(card_glob)
    if not cards:
        print('!! 无卡 %s' % card_glob); continue
    md = ('（源：%s%s；按原册裁区，保留结构图与公式）\n\n' % (label, (' · ' + note) if note else '')
          + '\n'.join('![](images/%s)' % os.path.basename(f) for f in fs)
          + '\n\n> 📌 据源答案册逐题裁区回填（OCR 定位「第N题」边界）。\n')
    for card in cards:
        t = open(card, encoding='utf-8-sig').read().replace('\r\n', '\n')
        ia = t.find('## 参考答案'); ik = t.find('## 知识点映射')
        assert ia > 0 and ik > ia, card
        new = t[:ia] + '## 参考答案\n\n' + md + '\n' + t[ik:]
        if APPLY:
            open(card, 'w', encoding='utf-8', newline='\n').write(new)
        n += 1
    print('%-22s → %d 图 → %d 卡  %s' % (prefix[:22], len(fs), len(cards), note))
print('共回填 %d 卡  %s' % (n, '[APPLY]' if APPLY else '[DRY-RUN]'))
