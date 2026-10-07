# -*- coding: utf-8 -*-
"""看 CM-17-05 / QBY-02-05 的题面是否含被删块的内容。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

for k in ['题-CM-17-05-51在气相的硫单质', '题-QBY-02-05-本题记丙酮']:
    fs = glob.glob('04-题库/2026机构初赛模拟题/**/%s*.md' % k, recursive=True)
    if not fs:
        print('未找到', k); continue
    p = fs[0]
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); kk = t.find('## 知识点映射')
    print('=' * 100)
    print(os.path.basename(p)[:60])
    print(' 题面区 %d 字 / 答案区 %d 字' % (len(t[i:j]), len(t[j:kk])))
    print(' --- 题面区（前 1100）---')
    print(re.sub(r'\n{2,}', '\n', t[i:j])[:1100])
    print(' --- 答案区（前 500）---')
    print(re.sub(r'\n{2,}', '\n', t[j:kk])[:500])
