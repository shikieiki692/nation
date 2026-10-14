# -*- coding: utf-8 -*-
"""为缺字段的卡提取候选取值（正文 wikilink 分类）"""
import io, os, re

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
    return bool(re.search(r'^%s:' % re.escape(k), s, re.M))

WL = re.compile(r'\[\[([^\]|#]+)')

def classify(link):
    l = link.strip()
    if l.startswith('09-审计报告/'):
        return 'E'
    if l.startswith('00-首页/工作日志/'):
        return 'E'
    if '规范' in l or 'SOP' in l or l.startswith('11-模板/') or '总纲' in l or 'README' in l:
        return 'S'
    if l.startswith('00-首页/活跃任务'):
        return 'R'
    return None

for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    t = rd(os.path.join(D, f)); s, b = fmsplit(t)
    if get(s, 'type') != '活跃任务卡':
        continue
    need = [k for k in ('source_notes', 'related_notes', 'evidence') if not has_block(s, k)]
    if not need:
        continue
    links = WL.findall(b)
    seen = []
    for l in links:
        l = l.strip()
        if l and l not in seen:
            seen.append(l)
    S = [l for l in seen if classify(l) == 'S']
    R = [l for l in seen if classify(l) == 'R']
    E = [l for l in seen if classify(l) == 'E']
    print('◆ %s' % f[:56])
    print('   缺: %s' % need)
    print('   S(规范): %s' % (S[:4] if S else '—'))
    print('   R(关联卡): %s' % (R[:4] if R else '—'))
    print('   E(证据): %s' % (E[:4] if E else '—'))
    # 也看看有无 related: 旧字段
    if re.search(r'^related:', s, re.M):
        print('   ⚠️ 已有旧字段 related:')
    print()
