# -*- coding: utf-8 -*-
"""放宽抽取：输出每张卡前 45 行里的「状态声明片段」"""
import io, os, re

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'
def rd(p): return io.open(p, encoding='utf-8-sig').read()
def fmsplit(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    return (m.group(1), t[m.end():]) if m else ('', t)
def get(s, k):
    m = re.search(r'^%s:[ \t]*(.*)$' % re.escape(k), s, re.M)
    return m.group(1).strip().strip('"') if m else None

PAT = re.compile(r'(?:状态|结论|status)[^\n]{0,24}?(completed|blocked|active|已完成|已收官|已闭环|已办结|已收口|保持\s*blocked|进行中)', re.I)

for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    t = rd(os.path.join(D, f)); s, b = fmsplit(t)
    if get(s, 'type') != '活跃任务卡':
        continue
    fmst = get(s, 'status')
    if fmst in ('active', 'blocked', 'completed'):
        continue
    head = '\n'.join([l for l in b.split('\n') if l.strip()][:45])
    hits = [m.group(0)[:70].replace('\n', ' ') for m in PAT.finditer(head)]
    print('◆ [FM=%s] %s' % (fmst, f[:52]))
    for h in hits[:3]:
        print('     ·', h)
    if not hits:
        print('     （45 行内无状态声明）')
