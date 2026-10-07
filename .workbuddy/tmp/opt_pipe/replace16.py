# -*- coding: utf-8 -*-
"""线2：为 A 类 16 张「须换卡」找池内替代（同模块 + knowledge_points 重合度排序）。"""
import csv, os, re, sys, glob, json, collections
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'R16', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
CSV = os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv')
rows = list(csv.DictReader(open(CSV, encoding='utf-8-sig')))
NEED = {'题面泄露', '仅题干回显', '题面/答案过短', '假结构式'}
targets = [r for r in rows if r['reason'] in NEED]
pool = [r for r in rows if r['verdict'] == '入池']


def fm(p):
    t = open(p, encoding='utf-8-sig', errors='replace').read()
    if not t.startswith('---'):
        return {}
    block = t.split('---', 2)[1]
    return block


def f1(block, k):
    m = re.search(r'^' + k + r':[ \t]*(.*)$', block, re.M)
    return m.group(1).strip().strip('"') if m else ''


def kps(p):
    """从 FM 的 knowledge_points 取（A 类卡的「知识点映射」节是「待人工校准」，无 wikilink）。"""
    t = open(p, encoding='utf-8-sig', errors='replace').read()
    if not t.startswith('---'):
        return set()
    blk = t.split('---', 2)[1]
    m = re.search(r'^knowledge_points:[ \t]*\n((?:[ \t]*-[ \t]*.*\n)+)', blk, re.M)
    if not m:
        return set()
    return set(re.findall(r'\[\[([^\]]+)\]\]', m.group(1)))


# 既往卷已用卡（排除）
used = set()
for f in glob.glob(os.path.join(ROOT, '.workbuddy/tmp/opt_pipe/vol_plan_*.json')):
    try:
        d = json.load(open(f, encoding='utf-8'))
        for mod, lst in d:
            for c in lst:
                used.add(os.path.basename(c['path']))
    except Exception:
        pass
print('既往卷已用卡 %d 张（从候选中排除）' % len(used))
print()

for r in targets:
    p = os.path.join(ROOT, r['path'])
    blk = fm(p)
    mod = f1(blk, 'source_subject') or f1(blk, 'subject_module')
    tgt_kp = kps(p)
    scored = []
    for c in pool:
        cp = os.path.join(ROOT, c['path'])
        if os.path.basename(cp) in used or c['inst'] == 'x':
            continue
        cb = fm(cp)
        if (f1(cb, 'source_subject') or f1(cb, 'subject_module')) != mod:
            continue
        ov = len(tgt_kp & kps(cp))
        if ov <= 0:
            continue
        scored.append((ov, os.path.basename(cp)[:52], c['inst']))
    scored.sort(reverse=True)
    print('=' * 104)
    print('原卡: %-46s | %-6s | %s | KP=%s' % (
        os.path.basename(p)[:44], r['reason'], mod, ','.join(sorted(tgt_kp))[:40]))
    print('  候选（同模块·KP重合 top5）：')
    for ov, bn, inst in scored[:5]:
        print('    重合%d | %-52s | %s' % (ov, bn, inst))
