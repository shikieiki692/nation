# -*- coding: utf-8 -*-
"""诊断：build_org.strip_q_echo 是否吞掉「题面回显＋末小问答案」合并段。
复制 strip_q_echo 逻辑（读自 build_org.py），对 O1 十卡复算。只读。"""
import io, os, re, json, difflib

R = r'C:\Obsidion\妙妙屋'
plan = json.load(io.open(os.path.join(R, r'.workbuddy\tmp\opt_pipe\vol_plan_O1.json'), encoding='utf-8'))
cards = [it.get('path') for g, items in plan for it in items]


def strip_q_echo(q, a):
    def nz(s):
        return re.sub(r'[#\s{}]', '', s)
    qsegs = [nz(p) for p in re.split(r'\n{2,}', q)]
    qsegs = [s for s in qsegs if len(s) >= 12]
    for seg in sorted(qsegs, key=len, reverse=True):
        try:
            pat = re.compile(r'[ \t{}]*'.join(map(re.escape, seg)))
        except re.error:
            continue
        limit = 4 * len(seg) + 40
        out, last, hit = [], 0, False
        for m in pat.finditer(a):
            if (m.end() - m.start()) > limit:
                continue
            out.append(a[last:m.start()]); last = m.end(); hit = True
        if hit:
            out.append(a[last:])
            a = "".join(out)
    keep, dropped = [], []
    for p in re.split(r'\n{2,}', a):
        pn = nz(p)
        if len(pn) >= 12:
            if any((pn in s) or (s in pn and len(pn) <= 1.6 * len(s)) for s in qsegs):
                dropped.append(p); continue
            if len(pn) >= 40:
                best, br = None, 0.0
                for s in qsegs:
                    if abs(len(s) - len(pn)) > 0.5 * len(pn):
                        continue
                    r = difflib.SequenceMatcher(None, pn, s).ratio()
                    if r > br:
                        br, best = r, s
                if br >= 0.82:
                    dropped.append(p); continue
        keep.append(p)
    return re.sub(r'\n{3,}', '\n\n', '\n\n'.join(keep)).strip('\n'), dropped


KEY = re.compile(r'解答[ \t]*[:：]')
for i, cp in enumerate(cards, 1):
    p = os.path.join(R, cp)
    t = io.open(p, encoding='utf-8-sig').read()
    j = t.find('## 参考答案')
    if j < 0:
        print('%2d %s : 无「## 参考答案」' % (i, os.path.basename(p))); continue
    q, a = t[:j], t[j:]
    a2, dropped = strip_q_echo(q, a)
    print('%2d %-40s 题面%d字 答案%d->%d字  丢段%d'
          % (i, os.path.basename(cp)[:38], len(q), len(a), len(a2), len(dropped)))
    for d in dropped:
        tag = '⚠️含解答' if KEY.search(d) else '  '
        print('   %s 丢[%3d字]: %s' % (tag, len(re.sub(r'\s', '', d)), d.replace('\n', ' / ')[:150]))
