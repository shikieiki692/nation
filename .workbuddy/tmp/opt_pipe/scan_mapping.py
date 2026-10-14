# -*- coding: utf-8 -*-
"""为 32 张活跃任务卡取映射证据：status / updated / completed / 正文完成信号"""
import io, os, re, subprocess

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/活跃任务'

def rd(p): return io.open(p, encoding='utf-8-sig').read()
def fm(t):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', t, re.S)
    return m.group(1) if m else ''
def get(s, k):
    m = re.search(r'^%s:[ \t]*(.*)$' % re.escape(k), s, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else None

SIG = ['已完成', '已收口', '已收官', '已闭环', '已办结', '关闭', '暂停', '暂缓', '待授权', '等待']

print('%-6s %-9s %-9s %-10s %s' % ('状态', 'updated', 'completed', '完成信号', '卡片'))
for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    p = os.path.join(D, f)
    t = rd(p)
    s = fm(t)
    if get(s, 'type') != '活跃任务卡':
        continue
    body = t[len(s) + 8:] if s else t
    hit = [k for k in SIG if k in body][:4]
    print('%-6s %-9s %-9s %-10s %s' % (
        get(s, 'status'), (get(s, 'updated') or '-')[:9], (get(s, 'completed') or '-')[:9],
        '/'.join(hit) or '-', f[:46]))
