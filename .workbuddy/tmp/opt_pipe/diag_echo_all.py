# -*- coding: utf-8 -*-
"""全库机构模拟题：strip_q_echo 旧/新对比 —— 量化「答案被当回显整段删」的缺陷。
只读。输出：旧逻辑丢答案的卡清单 + 新逻辑复检。"""
import io, os, re, difflib, sys

ROOT = r'C:\Obsidion\妙妙屋\04-题库\2026机构初赛模拟题'


def nz(s):
    return re.sub(r'[#\s{}]', '', s)


def _layer1(a, qsegs):
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
            out.append(a[last:]); a = "".join(out)
    return a


def _difflib_hit(pn, qsegs):
    if len(pn) < 40:
        return False
    br = 0.0
    for s in qsegs:
        if abs(len(s) - len(pn)) > 0.5 * len(pn):
            continue
        r = difflib.SequenceMatcher(None, pn, s).ratio()
        if r > br:
            br = r
    return br >= 0.82


def strip_old(q, a):
    qsegs = [nz(p) for p in re.split(r'\n{2,}', q)]
    qsegs = [s for s in qsegs if len(s) >= 12]
    a = _layer1(a, qsegs)
    keep = []
    for p in re.split(r'\n{2,}', a):
        pn = nz(p)
        if len(pn) >= 12:
            if any((pn in s) or (s in pn and len(pn) <= 1.6 * len(s)) for s in qsegs):
                continue
            if _difflib_hit(pn, qsegs):
                continue
        keep.append(p)
    return re.sub(r'\n{3,}', '\n\n', '\n\n'.join(keep)).strip('\n')


def strip_new(q, a):
    qsegs = [nz(p) for p in re.split(r'\n{2,}', q)]
    qsegs = [s for s in qsegs if len(s) >= 12]
    a = _layer1(a, qsegs)
    keep = []
    for p in re.split(r'\n{2,}', a):
        pn = nz(p)
        if len(pn) >= 12:
            pure, excise = False, None
            for s in qsegs:
                if pn in s:
                    pure = True; break
                if s in pn and len(pn) <= 1.6 * len(s):
                    if len(pn) - len(s) < 12:       # 残余可忽略 ⇒ 纯回显
                        pure = True; break
                    if excise is None or len(s) > len(excise):
                        excise = s
            if pure:
                continue
            if excise is not None:                   # ★ 只挖掉回显部分，保留答案残余
                try:
                    pat = re.compile(r'[ \t\n{}]*'.join(map(re.escape, excise)))
                    m = pat.search(p)
                    if m and (m.end() - m.start()) <= 4 * len(excise) + 40:
                        p = (p[:m.start()] + p[m.end():]).strip()
                except re.error:
                    pass
            if _difflib_hit(nz(p), qsegs):
                continue
        keep.append(p)
    return re.sub(r'\n{3,}', '\n\n', '\n\n'.join(keep)).strip('\n')


ANS = re.compile(r'(?m)^[ \t]*解答[ \t]*[:：]')


def answer_units(a):
    """抽出「解答：」后同段内的非空内容行（＝该小问答案正文）。"""
    units = []
    for m in ANS.finditer(a):
        tail = a[m.end():]
        chunk = re.split(r'\n{2,}', tail)[0]
        lines = [l.strip() for l in chunk.split('\n') if l.strip()]
        if lines:
            units.append(lines)
    return units


def lost(a_out, units, qsegs=None):
    """返回在新文本中找不到的**真答案**单元（排除本就是题面回显的行）。"""
    on = nz(a_out)
    bad = []
    for lines in units:
        for l in lines:
            ln = nz(l)
            if len(ln) < 4:
                continue
            if qsegs and any(ln in s or s in ln for s in qsegs):
                continue          # 本身是题面回显 ⇒ 被删属正常
            if ln not in on:
                bad.append(l); break
    return bad


files = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if f.startswith('题-') and f.endswith('.md'):
            files.append(os.path.join(dp, f))
files.sort()
print('卡数', len(files))

old_bad, new_bad = [], []
for fp in files:
    try:
        t = io.open(fp, encoding='utf-8-sig').read()
    except Exception:
        continue
    j = t.find('## 参考答案')
    if j < 0:
        continue
    q, a = t[:j], t[j:]
    qsegs = [nz(p) for p in re.split(r'\n{2,}', q)]
    qsegs = [s for s in qsegs if len(s) >= 12]
    units = answer_units(a)
    if not units:
        continue
    lo = lost(strip_old(q, a), units, qsegs)
    if lo:
        old_bad.append((fp, lo))
    ln_ = lost(strip_new(q, a), units, qsegs)
    if ln_:
        new_bad.append((fp, ln_))

print('=== 旧逻辑丢答案的卡数:', len(old_bad))
for fp, lo in old_bad[:60]:
    print('  ', os.path.relpath(fp, ROOT), '|', (lo[0] or '')[:60])
print('=== 新逻辑丢答案的卡数:', len(new_bad))
for fp, lo in new_bad[:60]:
    print('  ', os.path.relpath(fp, ROOT), '|', (lo[0] or '')[:60])

# 新旧输出差异面
diff_cards = []
for fp in files:
    try:
        t = io.open(fp, encoding='utf-8-sig').read()
    except Exception:
        continue
    j = t.find('## 参考答案')
    if j < 0:
        continue
    q, a = t[:j], t[j:]
    o, n = strip_old(q, a), strip_new(q, a)
    if o != n:
        diff_cards.append((fp, len(o), len(n), n, o))
print('=== 新旧输出不同的卡数:', len(diff_cards))
for fp, lo, ln, n, o in diff_cards[:5]:
    print('  ', os.path.relpath(fp, ROOT), 'len', lo, '->', ln)

