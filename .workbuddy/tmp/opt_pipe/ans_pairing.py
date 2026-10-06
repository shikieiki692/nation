# -*- coding: utf-8 -*-
"""精确配对 v3：对每个源卷组，为「题面最佳 PDF」找最匹配的「答案 PDF」。
候选域 = 同目录 ∪ 02-讲义镜像目录(同相对路径) ∪ 全树(强模糊)
配对分 = difflib(题目名去噪, 答案名去噪) ；题目名里的「试卷/试题/+答案」等词先归一。
输出 ans_pairing.csv：可用/不可用 + 文字层长度。
"""
import os, re, sys, csv, glob, difflib, collections

sys.stdout.reconfigure(encoding='utf-8')
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False)
        fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None
OCR = '06-外部资料导入/OCR'
ANS_PAT = re.compile(r'答案|解析|参考|讲评|评分|手稿', re.I)


def norm(s):
    s = s.lower()
    s = re.sub(r'[\s\(\)（）\[\]【】\-_\.、,，:：;；!！?？\'"“”‘’]+', '', s)
    return s


def clean(s):
    """题面名去噪，便于与答案名比较"""
    s = norm(s)
    for w in ['试卷', '试题', '试卷版', '清晰版', '已优化', '优化', '答案', '讲稿', '题目合集']:
        s = s.replace(norm(w), '')
    return s


pdfs = [p.replace(os.sep, '/') for p in glob.glob(os.path.join(OCR, '**', '*.pdf'), recursive=True)
        if '_mineru_out' not in p.replace('\\', '/')]
PIN = {p: norm(os.path.splitext(os.path.basename(p))[0]) for p in pdfs}
PCLEAN = {p: clean(os.path.splitext(os.path.basename(p))[0]) for p in pdfs}
by_dir = collections.defaultdict(list)
for p in pdfs:
    by_dir[os.path.dirname(p)].append(p)


def mirror_dirs(top):
    """01-题目/<rel> → 同时看 02-讲义/<rel>"""
    d = os.path.dirname(top)
    ds = [d]
    rd = os.path.relpath(d, OCR).replace('\\', '/')
    if rd.startswith('01-题目/'):
        ds.append(os.path.join(OCR, '02-讲义', rd[len('01-题目/'):]).replace('\\', '/'))
    return ds


def tl(p):
    if fitz is None:
        return -1
    try:
        d = fitz.open(p)
        return sum(len(d[i].get_text()) for i in range(min(d.page_count, 60)))
    except Exception:
        return -2


def pick_answer(top):
    tc = PCLEAN[top]
    cands = []
    # 候选 PDF：所有答案类 PDF
    for q in pdfs:
        if not ANS_PAT.search(os.path.basename(q)):
            continue
        r = difflib.SequenceMatcher(None, tc, PCLEAN[q]).ratio()
        # 同目录 / 镜像目录加成
        boost = 0.0
        for md in mirror_dirs(top):
            if os.path.dirname(q) == md:
                boost = 0.25
                break
        # 关键数字（卷号）一致加成
        nt = set(re.findall(r'\d+', os.path.basename(top)))
        nq = set(re.findall(r'\d+', os.path.basename(q)))
        if nt and nq and (nt & nq):
            boost += 0.15
        cands.append((r + boost, q))
    cands.sort(reverse=True)
    return cands[:3]


rows = list(csv.DictReader(open('.workbuddy/tmp/opt_pipe/noans_list.csv', encoding='utf-8-sig')))
groups = collections.OrderedDict()
for r in rows:
    groups.setdefault((r['inst'], r['source_file']), []).append(r)

# 先定每个组的题面最佳 PDF
out = []
for (inst, sf), cards in groups.items():
    vol = os.path.splitext(os.path.basename(sf))[0]
    nk = norm(vol)
    best = None
    for p, npn in PIN.items():
        r = difflib.SequenceMatcher(None, nk, npn).ratio()
        if nk and (nk in npn or npn in nk):
            r += 0.3
        if best is None or r > best[0]:
            best = (r, p)
    top = best[1]
    ans = pick_answer(top)
    a0 = ans[0] if ans else (0, '')
    rows_out = dict(inst=inst, vol=vol, n=len(cards),
                    top=os.path.relpath(top, OCR),
                    ans=os.path.relpath(a0[1], OCR) if a0[1] else '',
                    score='%.2f' % a0[0], ans_textlen=tl(a0[1]) if a0[1] else -1)
    out.append(rows_out)

out.sort(key=lambda r: (r['inst'], -r['n']))
with open('.workbuddy/tmp/opt_pipe/ans_pairing.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader()
    w.writerows(out)

# 汇总
auto = [r for r in out if r['score'] and float(r['score']) >= 0.55 and r['ans_textlen'] > 500]
scan = [r for r in out if r['score'] and float(r['score']) >= 0.55 and 0 <= r['ans_textlen'] <= 500]
none = [r for r in out if not r['score'] or float(r['score']) < 0.55]
print('=== 可自动抽取(有文字层, 配对≥0.55)  %d 组 / %d 卡 ===' % (len(auto), sum(r['n'] for r in auto)))
for r in auto:
    print('  [%s] %-40s → %s (txtlen=%d, %.2f)' % (r['inst'], r['vol'][:40], os.path.basename(r['ans'])[:44], r['ans_textlen'], float(r['score'])))
print()
print('=== 需目视转录(扫描件, 配对≥0.55)  %d 组 / %d 卡 ===' % (len(scan), sum(r['n'] for r in scan)))
for r in scan:
    print('  [%s] %-40s → %s (%.2f)' % (r['inst'], r['vol'][:40], os.path.basename(r['ans'])[:44], float(r['score'])))
print()
print('=== 无答案源(配对<0.55)  %d 组 / %d 卡 ===' % (len(none), sum(r['n'] for r in none)))
for r in none:
    print('  [%s] %-46s (best %.2f %s)' % (r['inst'], r['vol'][:46], float(r['score'] or 0), os.path.basename(r['ans'])[:30]))
print()
print('CSV → .workbuddy/tmp/opt_pipe/ans_pairing.csv')
