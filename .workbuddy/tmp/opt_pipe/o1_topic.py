# -*- coding: utf-8 -*-
"""导出 O1 十卡的题面首段（去图/去公式压缩），供人工判主题分段。只读。"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], '--vol', 'O1', '--all-years', '--organic']
import build_org as BO

pool = BO.build_pool()
picks = BO.pick_vol(pool, set(), max_per_src=4, fps0=[])


def brief(t):
    i = t.find('## 题目')
    j = t.find('## 参考答案')
    q = t[i:j] if j > i > 0 else (t[i:] if i > 0 else t)
    q = re.sub(r'!\[\[[^\]]*\]\]', '〔图〕', q)
    q = re.sub(r'\$\$?[^$\n]{0,200}\$\$?', '〔式〕', q)
    q = re.sub(r'<[^>]{0,200}>', '', q)
    q = re.sub(r'^\s*[#>|*\-\s]*', '', q, flags=re.M)
    q = re.sub(r'\n{2,}', '\n', q).strip()
    return q[:420]


for k, (mod, lbl, need) in enumerate(BO.QUOTA):
    print("\n########## %s" % lbl)
    for c in picks[k][1]:
        t = open(os.path.join(r"C:\Obsidion\妙妙屋", c['path'].replace('/', os.sep)),
                 encoding='utf-8-sig', errors='replace').read()
        print("\n---- [%s] %s | 机判主题%d 分%s" % (c['src_dir'], os.path.basename(c['path']),
                                              c.get('otopic', -1), c.get('otopic_sc')))
        print(brief(t))
