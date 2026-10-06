# -*- coding: utf-8 -*-
"""由 JSON 生成 MD 导航页（人读 + Agent 分流）"""
import json, collections, os, glob, re, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
os.chdir(ROOT)

json_path = '10-索引与统计/04-考点题源索引.json'
D = json.load(open(json_path, encoding='utf-8'))
meta, by_kp = D['meta'], D['by_kp']

# 全库 basename 索引（判歧义）＋ 03-知识点 实际相对路径
ALL = collections.defaultdict(list)
KP_PATH = {}
for p in glob.glob('**/*.md', recursive=True):
    if p.startswith('.'):
        continue
    b = os.path.basename(p)[:-3]
    ALL[b].append(p.replace('\\', '/'))
    if p.replace('\\', '/').startswith('03-知识点/'):
        KP_PATH.setdefault(b, p.replace('\\', '/'))

def mk(k):
    """歧义考点用带路径链接（表格内 `|` 须转义为 `\\|`），其余用短链"""
    if len(ALL.get(k, [])) > 1 and k in KP_PATH:
        return '[[%s\\|%s]]' % (KP_PATH[k][:-3], k)
    return '[[%s]]' % k

bymod = collections.defaultdict(list)
for k, v in by_kp.items():
    zhen_cnt = v['by_source'].get('真题', 0)
    mock_cnt = sum(cnt for s, cnt in v['by_source'].items() if s != '真题')
    bymod[v['module']].append((k, v['count'], zhen_cnt, mock_cnt))

today_str = datetime.date.today().isoformat()

L = []
A = L.append
A('---')
A('title: 考点题源索引')
A('type: 索引')
A('generated: %s' % today_str)
A('tags: [化竞, 索引, 题源, 组题, 外挂索引]')
A('updated: %s' % today_str)
A('status: 已填充')
A('---')
A('')
A('# 考点题源索引（外挂索引）')
A('')
A('> **定位**：服务**组题检索**的外挂索引——按考点找可用题源（真题＋机构模拟题）。')
A('> ⛔ **不入 `04-题库`（红线区）**；本页与同名 JSON 均可**重复生成**。')
A('> **数据**：%s。覆盖 **%d 个考点 / %d 条考点-题源引用**。' % (meta['scope'], meta['total_kps'], meta['total_refs']))
A('> **机器可读版**：`10-索引与统计/04-考点题源索引.json` —— 含每个考点的**逐题清单**（路径＋来源＋难度）。')
A('')
A('## Agent 调用三步法')
A('')
A('1. **定模块**：判断要组题的知识点属于哪个学科（见下表分流）。')
A('2. **查题源**：读本页对应模块表；需逐题清单则读 JSON 的 `by_kp[考点名]`。')
A('3. **取卡**：按 `problems[].path` 打开题卡；`src` 区分真题／机构模拟题，`difficulty` 为难度。')
A('')
A('> ⚠️ **真题定考法、模拟题扩变式**（库内既定口径）。')
A('> ℹ️ **收录范围**：已全量收录 13 家机构初赛模拟题（KP 锚点 100% 覆盖）与历年真题题卡。')
A('')
A('## 一、模块分流总览')
A('')
A('| 模块 | 考点数 | 题源引用 |')
A('|:--|--:|--:|')
MODORDER = ['化学原理', '有机化学', '无机和结构化学', '分析化学', '物理化学', '决赛要求', '综合', '数学工具', '高中化学基础', '初中化学基础']
for m in MODORDER + [x for x in bymod if x not in MODORDER]:
    if m not in bymod: continue
    rows = bymod[m]
    refs = sum(r[1] for r in rows)
    A('| %s | %d | %d |' % (m, len(rows), refs))
A('')
A('## 二、高频考点（题源 ≥ 20）')
A('')
A('| 考点 | 模块 | 合计 | 真题 | 机构 |')
A('|:--|:--|--:|--:|--:|')
for k, v in sorted(by_kp.items(), key=lambda x: -x[1]['count']):
    if v['count'] < 20: break
    zhen_cnt = v['by_source'].get('真题', 0)
    mock_cnt = sum(cnt for s, cnt in v['by_source'].items() if s != '真题')
    A('| %s | %s | %d | %d | %d |' % (mk(k), v['module'], v['count'], zhen_cnt, mock_cnt))
A('')
A('## 三、分模块考点表（题源 ≥ 3）')
A('')
for m in MODORDER + [x for x in bymod if x not in MODORDER]:
    if m not in bymod: continue
    rows = sorted(bymod[m], key=lambda x: -x[1])
    rows3 = [r for r in rows if r[1] >= 3]
    A('### %s（考点 %d，其中题源≥3 者 %d）' % (m, len(rows), len(rows3)))
    A('')
    A('| 考点 | 合计 | 真题 | 机构 |')
    A('|:--|--:|--:|--:|')
    for k, c, z, j in rows3:
        A('| %s | %d | %d | %d |' % (mk(k), c, z, j))
    A('')
A('---')
A('')
A('*本页为派生品，由 `04-考点题源索引.json` 生成；题卡锚点变更后重跑生成脚本即可刷新。*')

md_path = '10-索引与统计/04-考点题源索引.md'
open(md_path, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('MD: %.1f KB, %d 行' % (os.path.getsize(md_path) / 1024, len(L)))
print('模块分布:')
for m, v in bymod.items():
    print(f'  {m:12s}: 考点 {len(v):3d}, 题源引用 {sum(r[1] for r in v):5d}')
