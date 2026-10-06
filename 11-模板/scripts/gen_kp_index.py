# -*- coding: utf-8 -*-
"""生成「考点→题源」外挂索引（JSON 全量）；MD 由 gen_kp_index_md.py 生成"""
import re, os, glob, json, collections, datetime

# 定位知识库根目录
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
os.chdir(ROOT)

FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.S)

pages = []
for p in glob.glob('03-知识点/**/*.md', recursive=True):
    b = os.path.basename(p)[:-3]
    if b in ('README', '知识点'):
        continue
    raw = open(p, encoding='utf-8-sig', errors='ignore').read()
    m = FM_RE.match(raw)
    mod = p.replace('\\', '/').split('03-知识点/')[1].split('/')[0]
    pages.append((b, m.group(1) if m else '', mod))

LABEL = {b: b for b, _, _ in pages}
MOD = {b: mod for b, _, mod in pages}
DEP = {}
for b, fm, mod in pages:
    if re.search(r"^status\s*:\s*deprecated", fm, re.M):
        DEP[b] = True
    tm = re.search(r'^title\s*:\s*"?(.*?)"?\s*$', fm, re.M)
    if tm and tm.group(1).strip():
        LABEL.setdefault(tm.group(1).strip(), b)
    ab = re.search(r"^aliases\s*:[ \t]*\n((?:(?:[ \t]*-.*)?\n)*)", fm, re.M)
    am = re.search(r"^aliases\s*:[ \t]*(.*)$", fm, re.M)
    seg = ab.group(1) if ab else (am.group(1) if am else '')
    for a in re.findall(r'[\-\s]*["\']?([^,\[\]"\'\n]+?)["\']?\s*(?:,|$)', seg):
        a = a.strip().strip('"\'')
        if a:
            LABEL.setdefault(a, b)

def kp_items(fm):
    m = re.search(r"^knowledge_points\s*:[ \t]*(.*)$", fm, re.M)
    blk = re.search(r"^knowledge_points\s*:[ \t]*\n((?:(?:[ \t]*-.*)?\n)*)", fm, re.M)
    seg = blk.group(1) if blk else (m.group(1) if m else '')
    return [v.strip() for v in re.findall(r'\[\[([^\]|]+)\]\]', seg)]

def getf(fm, k):
    m = re.search(r"^%s\s*:[ \t]*(.*)$" % k, fm, re.M)
    return m.group(1).strip().strip('"\'') if m else ''

# 动态获取 2026机构初赛模拟题 下全部机构目录（排除以 . 和 _ 开头的目录）
base_mock = '04-题库/2026机构初赛模拟题'
mock_orgs = sorted([d for d in os.listdir(base_mock)
                    if os.path.isdir(os.path.join(base_mock, d)) and not d.startswith(('.', '_'))])

SOURCES = [(org, f'{base_mock}/{org}/**/*.md') for org in mock_orgs]
SOURCES.append(('真题', '04-题库/真题/**/*.md'))

by_kp = collections.defaultdict(lambda: {'count': 0, 'src': collections.Counter(), 'probs': []})
stat = {}
for src, pat in SOURCES:
    n = 0
    for f in glob.glob(pat, recursive=True):
        bn = os.path.basename(f)
        # 护栏1: 必须是以 '题-' 开头的题卡，排除 README 和台账文件
        if bn == 'README.md' or not bn.startswith('题-'):
            continue
        raw = open(f, encoding='utf-8-sig', errors='ignore').read()
        m = FM_RE.match(raw)
        if not m:
            continue
        fm = m.group(1)
        n += 1
        path = f.replace('\\', '/')
        diff = getf(fm, 'difficulty')
        seen = set()
        for k in kp_items(fm):
            # 护栏2: LABEL 映射与 DEP 过滤
            tgt = LABEL.get(k)
            if not tgt or DEP.get(tgt) or tgt in seen:
                continue
            # 护栏3: seen 去重（同一卡同 KP 仅计一次）
            seen.add(tgt)
            d = by_kp[tgt]
            d['count'] += 1
            d['src'][src] += 1
            d['probs'].append({'src': src, 'path': path, 'difficulty': diff})
    stat[src] = n

today_str = datetime.date.today().isoformat()
mock_total = sum(v for k, v in stat.items() if k != '真题')
zhen_total = stat.get('真题', 0)
mock_detail = ' + '.join([f'{k} {v}' for k, v in stat.items() if k != '真题'])
scope_desc = f'13家机构模拟题 {mock_total}（{mock_detail}）+ 真题 {zhen_total}（有 KP 者）'

out = {'meta': {'title': '考点-题源外挂索引',
                'generated': today_str,
                'scope': scope_desc,
                'total_kps': len(by_kp),
                'total_refs': sum(v['count'] for v in by_kp.values()),
                'sources_breakdown': stat,
                'note': '外挂索引：不入 04-题库（红线），可重复生成；服务组题检索。'},
       'by_kp': {k: {'module': MOD.get(k, '?'), 'count': v['count'],
                     'by_source': dict(v['src']), 'problems': v['probs']}
                 for k, v in by_kp.items()}}

target_json = '10-索引与统计/04-考点题源索引.json'
json.dump(out, open(target_json, 'w', encoding='utf-8', newline='\n'),
          ensure_ascii=False, indent=1)

print('=== 索引生成完成 ===')
print('JSON: %d 考点 / %d 引用 / %.1f KB' %
      (len(by_kp), out['meta']['total_refs'], os.path.getsize(target_json) / 1024))
print('题源统计 (共 %d 个机构/源):' % len(stat))
for k, v in stat.items():
    print(f'  {k:12s}: {v:4d} 张题卡')
