# -*- coding: utf-8 -*-
"""生成《2026-10-07-A类待换卡替代建议.md》：16 张待换卡 → 池内替代候选（同模块·KP 重合降序）。"""
import csv, os, re, sys, glob, json
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'C:\Obsidion\妙妙屋'
OUT = os.path.join(ROOT, '09-审计报告', '2026-10-07-A类待换卡替代建议.md')
rows = list(csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')))
NEED = {'题面泄露', '仅题干回显', '题面/答案过短', '假结构式'}
targets = [r for r in rows if r['reason'] in NEED]
pool = [r for r in rows if r['verdict'] == '入池']


def fmblk(p):
    t = open(p, encoding='utf-8-sig', errors='replace').read()
    return t.split('---', 2)[1] if t.startswith('---') else ''


def f1(blk, k):
    m = re.search(r'^' + k + r':[ \t]*(.*)$', blk, re.M)
    return m.group(1).strip().strip('"') if m else ''


def kps(p):
    blk = fmblk(p)
    m = re.search(r'^knowledge_points:[ \t]*\n((?:[ \t]*-[ \t]*.*\n)+)', blk, re.M)
    return set(re.findall(r'\[\[([^\]]+)\]\]', m.group(1))) if m else set()


used = set()
for f in glob.glob(os.path.join(ROOT, '.workbuddy/tmp/opt_pipe/vol_plan_*.json')):
    try:
        for mod, lst in json.load(open(f, encoding='utf-8')):
            for c in lst:
                used.add(os.path.basename(c['path']))
    except Exception:
        pass

# 预取池内卡的 module / kp
PC = []
for c in pool:
    cp = os.path.join(ROOT, c['path'])
    bn = os.path.basename(cp)
    if bn in used:
        continue
    b = fmblk(cp)
    PC.append((bn, c['inst'], f1(b, 'source_subject') or f1(b, 'subject_module'),
               kps(cp), f1(b, 'source')[:40]))

md = []
md.append('# A 类待换卡 · 池内替代建议（2026-10-07）\n')
md.append('> **用途**：A 类中「须换卡」的 **16 张**（12 真交错 ＋ 2 仅题干回显 ＋ 1 过短 ＋ 1 假结构式）'
          '逐张给出**池内替代候选**（同模块、`knowledge_points` 重合度降序）。\n')
md.append('> 候选已排除：**既往卷（X/XIp/XI）已用卡 %d 张**、A 类自身。\n' % len(used))
md.append('> ⚠️ 替代卡的最终选用仍需走 SOP「⓪回源视觉三元核验」；本表只做**候选排序**。\n')
for r in targets:
    p = os.path.join(ROOT, r['path'])
    b = fmblk(p)
    mod = f1(b, 'source_subject') or f1(b, 'subject_module')
    tk = kps(p)
    sc = []
    for bn, inst, m2, k2, src in PC:
        if m2 != mod:
            continue
        ov = len(tk & k2)
        if ov:
            sc.append((ov, bn, inst, sorted(tk & k2)))
    sc.sort(key=lambda x: -x[0])
    md.append('\n## `%s`\n' % os.path.basename(p)[:56])
    md.append('| 项 | 值 |\n|:--|:--|\n')
    md.append('| 原因 | %s |\n' % r['reason'])
    md.append('| 模块 | %s |\n' % mod)
    md.append('| 考点 | %s |\n' % ('、'.join(sorted(tk)) if tk else '—'))
    md.append('| 源 | %s |\n' % (f1(b, 'source')[:60] or '—'))
    md.append('\n**替代候选（同模块·考点重合）：**\n')
    if not sc:
        md.append('> （同模块内无考点重合候选 ⇒ 需放宽到「同模块任意卡」人工挑）\n')
        continue
    md.append('| # | 候选卡 | 机构 | 重合考点 |\n|--:|:--|:--|:--|\n')
    for i, (ov, bn, inst, common) in enumerate(sc[:5], 1):
        md.append('| %d | `%s` | %s | %s |\n' % (i, bn[:48], inst, '、'.join(common)[:34]))

open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(md) + '\n')
print('已生成 %s（%d 行）' % (OUT, len(md)))
print('目标 %d 张；池内候选 %d 张' % (len(targets), len(PC)))
