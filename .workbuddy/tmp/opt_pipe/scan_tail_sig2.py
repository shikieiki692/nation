# -*- coding: utf-8 -*-
"""扫「尾部串入」签名 v2：题面/答案区含**答案册标题**（排除 `## 参考答案` 本身）或他题题头。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'TT2', '--all-years']
import build_org as BO

# `## …答案…` 但排除 `## 参考答案`（本卡答案区标题）
ANS_HEAD = re.compile(r'(?m)^#{1,4}[ \t]*([^\n]{0,60}?答案[^\n]{0,30})$')


def ans_titles(seg):
    out = []
    for m in ANS_HEAD.finditer(seg):
        body = m.group(1).strip()
        if body in ('参考答案', '答案'):
            continue
        out.append(body)
    return out


cards = glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True)
hits = []
for p in cards:
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    i = t.find('## 题目'); j = t.find('## 参考答案'); k = t.find('## 知识点映射')
    if i < 0 or j < 0 or k < 0:
        continue
    qz, az = t[i:j], t[j:k]
    tags = []
    qt = ans_titles(qz)
    if qt:
        tags.append('题面:%s' % qt[0][:22])
    at = ans_titles(az)
    if at:
        tags.append('答案:%s' % at[0][:22])
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
print('命中 %d 张' % len(hits))
for p, tags in hits[:40]:
    print('  %-52s | %s' % (os.path.basename(p)[:50], ' / '.join(tags)))
