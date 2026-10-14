# -*- coding: utf-8 -*-
"""① 32 张卡的三字段缺口盘点；② 每卡正文 wikilink 的分类（供三字段取值）"""
import io, os, re, collections

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'
def rd(p): return io.open(p, encoding='utf-8-sig').read()
def fmsplit(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    return (m.group(1), t[m.end():]) if m else ('', t)
def get(s, k):
    m = re.search(r'^%s:[ \t]*(.*)$' % re.escape(k), s, re.M)
    return m.group(1).strip() if m else None
def has_block(s, k):
    return bool(re.search(r'^%s:[ \t]*$' % re.escape(k), s, re.M)) or bool(re.search(r'^%s:[ \t]*\[.*\]' % re.escape(k), s, re.M))

WL = re.compile(r'\[\[([^\]|#]+)')
SRC_PAT = ('11-模板/规范', '规范', 'SOP', '总纲', 'README')
EVID = ('09-审计报告', '00-首页/工作日志', '工作日志/')
REL_CARD = '00-首页/活跃任务/'

miss = collections.Counter()
print('%-52s %-8s %-8s %-8s' % ('卡片(type=活跃任务卡)', 'src', 'rel', 'evi'))
print('-' * 82)
for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    t = rd(os.path.join(D, f)); s, b = fmsplit(t)
    if get(s, 'type') != '活跃任务卡':
        continue
    hs, hr, he = has_block(s, 'source_notes'), has_block(s, 'related_notes'), has_block(s, 'evidence')
    for k, v in (('src', hs), ('rel', hr), ('evi', he)):
        if not v:
            miss[k] += 1
    print('%-52s %-8s %-8s %-8s' % (f[:52], '' if hs else '缺', '' if hr else '缺', '' if he else '缺'))
print()
print('缺 source_notes %d ｜ related_notes %d ｜ evidence %d' % (miss['src'], miss['rel'], miss['evi']))
