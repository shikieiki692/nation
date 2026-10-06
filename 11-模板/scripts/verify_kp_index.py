# -*- coding: utf-8 -*-
"""校验索引 MD 内 wikilink 可解析 + JSON 合法 + 题卡物理路径有效性"""
import re, os, glob, json, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
os.chdir(ROOT)

# 全库 basename 索引（排除归档）
idx = collections.defaultdict(list)
for p in glob.glob('**/*.md', recursive=True):
    if p.startswith('.') or p.startswith('_归档') or '_archive' in p:
        continue
    idx[os.path.basename(p)[:-3]].append(p)

md_path = '10-索引与统计/04-考点题源索引.md'
md = open(md_path, encoding='utf-8').read()
links = re.findall(r'\[\[([^\]|#]+)\]\]', md)
bad = [l for l in links if l not in idx]
dup = [l for l in links if len(idx.get(l, [])) > 1]
print('=== MD 校验 ===')
print('MD wikilink: %d 条 | 不可解析 %d | 歧义 %d' % (len(links), len(bad), len(set(dup))))
if bad:
    print('  不可解析样例:', bad[:10])
if dup:
    print('  歧义样例:', list(set(dup))[:10])

json_path = '10-索引与统计/04-考点题源索引.json'
D = json.load(open(json_path, encoding='utf-8'))
meta = D['meta']
print('\n=== JSON 校验 ===')
print('JSON 合法 | title: %s | generated: %s' % (meta['title'], meta['generated']))
print('JSON scope: %s' % meta['scope'])
print('JSON 考点: %d | 题源引用总数: %d' % (len(D['by_kp']), meta['total_refs']))

# 检查题源物理路径有效性
missing_paths = []
total_problem_refs = 0
for k, v in D['by_kp'].items():
    for prob in v['problems']:
        total_problem_refs += 1
        p = prob['path']
        if not os.path.isfile(p):
            missing_paths.append((k, p))

print('\n=== 题卡物理路径校验 ===')
print('题卡引用总条数: %d | 物理文件缺失数: %d' % (total_problem_refs, len(missing_paths)))
if missing_paths:
    print('  缺失样例 (前5条):', missing_paths[:5])
else:
    print('  ✅ 所有题卡路径 100% 存在！')

# 抽查一条
k0 = next(iter(D['by_kp']))
print('\n抽查第一条考点 [%s]: 总引用 %d 次, 来源分布 %s' %
      (k0, D['by_kp'][k0]['count'], dict(D['by_kp'][k0]['by_source'])))
