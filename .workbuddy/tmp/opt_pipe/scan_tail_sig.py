# -*- coding: utf-8 -*-
"""扫「尾部串入」签名：题面/答案区里出现 **答案册标题**（`## …答案…`）或「另一题」题头。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'TAIL', '--all-years']
import build_org as BO

ANS_HEAD = re.compile(r'(?m)^#{1,4}[ \t]*[^\n]{0,60}?答案[^\n]{0,30}$')
cards = glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
hits = []
for p in cards:
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
    if i < 0 or j < 0 or k < 0:
        continue
    qz, az = t[i:j], t[j:k]
    tags = []
    if ANS_HEAD.search(qz):
        tags.append('题面含答案册标题')
    if ANS_HEAD.search(az):
        tags.append('答案区含答案册标题')
    # 题面内出现「另一题」题头（`## 第M题` M≠own）
    own = BO.own_qno(t, p)
    c = BO.X.extract(p)
    q = BO.html_table_to_md(BO.conv_imgs(BO.clean_q(c['question'])))
    for m in re.finditer(r'(?m)^#{1,4}[ \t]*第\s*([0-9一二三四五六七八九十]+)\s*题', q):
        n = BO._cn2int(m.group(1))
        if n and own and n != own:
            tags.append('题面含第%s题头' % m.group(1))
            break
    if tags:
        hits.append((p, tags))
print('签名命中 %d 张' % len(hits))
for p, tags in hits[:40]:
    print('  %-32s | %s' % (','.join(tags), os.path.basename(p)[:52]))
