# -*- coding: utf-8 -*-
"""严格校验本轮改动的 5 个 md 的 frontmatter（ruamel）＋ 检查新链接是否可解析。"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Obsidion\妙妙屋'
FILES = [
    '00-首页/状态摘要.md',
    '00-首页/活跃任务.md',
    '00-首页/工作日志.md',
    '00-首页/工作日志/2026-10-07.md',
    '00-首页/活跃任务/【直接复制】新会话提示词-2026-10-07-机构模拟题组卷线.md',
]
try:
    from ruamel.yaml import YAML
    y = YAML(typ='safe')
    HAVE = True
except Exception as e:
    HAVE = False
    print('ruamel 不可用:', e)

allnames = set()
for dp, dn, fn in os.walk(ROOT):
    if '.git' in dp.replace('\\', '/').split('/'):
        continue
    for f in fn:
        if f.endswith('.md'):
            allnames.add(f[:-3])

for rel in FILES:
    p = os.path.join(ROOT, rel)
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n')
    ok, keys = False, 0
    if t.startswith('---'):
        blk = t.split('---', 2)[1]
        if HAVE:
            try:
                d = y.load(blk)
                ok, keys = True, len(d or {})
            except Exception as e:
                print('  ❌ FM 解析失败 %s: %s' % (rel, str(e)[:80]))
        # 检查 knowledge_points 类字段格式
    # 新链接可解析性
    links = re.findall(r'\[\[([^\]|#]+)', t)
    bad = []
    for l in links:
        l2 = l.strip().rstrip('/')
        base = os.path.basename(l2)
        if base and base not in allnames and not os.path.exists(os.path.join(ROOT, l2 + '.md')):
            bad.append(l2)
    print('%-58s FM=%s(%d键) 链接=%d 不可解析=%d %s' % (
        rel[:56], 'OK' if ok else '—', keys, len(links), len(bad), bad[:3]))
