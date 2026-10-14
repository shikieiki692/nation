# -*- coding: utf-8 -*-
r"""卷内图 × 图升级配对表 交叉分析（只读）。"""
import json, io, os, re
os.chdir(r'C:\Obsidion\妙妙屋')

# 1) 卷内图引用
vol_imgs = {}   # name -> [(卷,版), ...]
for V in ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']:
    for tag in ['学生版', '答案版']:
        md = '04-题库/初赛模拟卷%s（非有机·%s）.md' % (V, tag)
        if not os.path.isfile(md):
            continue
        t = io.open(md, encoding='utf-8-sig').read()
        for m in re.finditer(r'!\[\[([^\]]+)\]\]', t):
            nm = os.path.basename(m.group(1))
            vol_imgs.setdefault(nm, []).append('%s/%s' % (V, tag))
print('卷内图引用：去重 %d 张' % len(vol_imgs))

# 2) lib_analysis
la = json.load(io.open('.workbuddy/tmp/chemy_site/lib_analysis.json', encoding='utf-8'))
la_by = {}
for it in la:
    b = os.path.basename(it.get('lib', ''))
    if b:
        la_by[b] = it
# 3) match_final
mf = json.load(io.open('.workbuddy/tmp/chemy_site/img_match_final.json', encoding='utf-8'))
mf_by = {}
for it in mf:
    b = os.path.basename(it.get('lib_img', ''))
    if b:
        mf_by.setdefault(b, it)
# 4) candidates
cd = json.load(io.open('.workbuddy/tmp/chemy_site/img_candidates.json', encoding='utf-8'))
cd_by = {}
for it in cd:
    b = os.path.basename(it.get('lib_img', ''))
    if b:
        cd_by[b] = it
# 5) 已换 314
rep = json.load(io.open('04-题库/2026机构初赛模拟题/chemy/_图片升级清单-2026-10-14.json', encoding='utf-8'))['replaced']
rep_set = {os.path.basename(x['lib_img']) for x in rep}
print('分析表 %d ｜ 配对表 %d ｜ 候选 %d ｜ 已换 %d' % (len(la_by), len(mf_by), len(cd_by), len(rep_set)))
print()

in_la = [n for n in vol_imgs if n in la_by]
mapped = [n for n in in_la if la_by[n].get('mapped')]
in_mf = [n for n in vol_imgs if n in mf_by]
in_cd = [n for n in vol_imgs if n in cd_by]
in_rep = [n for n in vol_imgs if n in rep_set]
print('卷内图 ∩ 分析表     : %d' % len(in_la))
print('  其中 mapped=true  : %d' % len(mapped))
print('卷内图 ∩ 配对表     : %d' % len(in_mf))
print('卷内图 ∩ 候选(护栏) : %d' % len(in_cd))
print('卷内图 ∩ 已换314    : %d' % len(in_rep))
print()
print('=== 卷内图中有站点配对的（前 20）===')
for n in in_mf[:20]:
    a = la_by.get(n, {})
    print('  %s  卷=%s  lib %sx%s  站=%s' % (n[:20], ','.join(vol_imgs[n])[:22], a.get('w'), a.get('h'), mf_by[n].get('e2') or mf_by[n].get('e1')))
