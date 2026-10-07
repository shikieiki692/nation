# -*- coding: utf-8 -*-
"""插桩复现 strip_q_echo：定位是哪一层删掉了 HYS-02-07 答案的图。"""
import os, re, sys, csv, difflib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.workbuddy/tmp/opt_pipe')
sys.argv = ['x', '--vol', 'IN', '--all-years']
import build_org as BO

ROOT = r'C:\Obsidion\妙妙屋'
rows = list(csv.DictReader(open(os.path.join(ROOT, '09-审计报告/2026-10-07-不可组卷题目清单.csv'), encoding='utf-8-sig')))
p = [r for r in rows if os.path.basename(r['path']).startswith('题-HYS-02-07-万物')][0]
p = os.path.join(ROOT, p['path'])
c = BO.X.extract(p)
q0 = BO.conv_imgs(BO.clean_q(c['question']))
a = BO.flatten_layout_tables(BO.conv_imgs(c['answer']))


def nz(s):
    return re.sub(r'[#\s{}]', '', s)


qsegs = [nz(x) for x in re.split(r'\n{2,}', q0)]
qsegs = [s for s in qsegs if len(s) >= 12]
print('题面段数:', len(qsegs))

# ---- ① 字符级 ----
a1 = a
for seg in sorted(qsegs, key=len, reverse=True):
    pat = re.compile(r'[ \t{}]*'.join(map(re.escape, seg)))
    limit = 4 * len(seg) + 40
    out, last, hit = [], 0, False
    for m in pat.finditer(a1):
        if (m.end() - m.start()) > limit:
            continue
        out.append(a1[last:m.start()]); last = m.end(); hit = True
        print('  [①] seg(len%d) 命中 span=%d: %r' % (len(seg), m.end() - m.start(), a1[m.start():m.end()][:60]))
    if hit:
        out.append(a1[last:]); a1 = "".join(out)
print('① 后 图数=%d 字=%d' % (len(re.findall(r'!\[\[', a1)), len(nz(a1))))

# ---- ②③ 段落级 ----
keep = []
for seg_p in re.split(r'\n{2,}', a1):
    pn = nz(seg_p)
    reason = None
    if len(pn) >= 12:
        for s in qsegs:
            if pn in s:
                reason = '②pn-in-s'; break
            if s in pn and len(pn) <= 1.6 * len(s):
                reason = '②s-in-pn(len %d<=1.6*%d)' % (len(pn), len(s)); break
        if reason is None and len(pn) >= 40:
            br = 0.0
            for s in qsegs:
                if abs(len(s) - len(pn)) > 0.5 * len(pn):
                    continue
                r = difflib.SequenceMatcher(None, pn, s).ratio()
                br = max(br, r)
            if br >= 0.82:
                reason = '③sim=%.2f' % br
    if reason:
        print('  [%s] 删段(图%d): %r' % (reason, len(re.findall(r'!\[\[', seg_p)), seg_p[:70]))
    else:
        keep.append(seg_p)
print('②③ 后 图数=%d' % sum(len(re.findall(r'!\[\[', k)) for k in keep))
