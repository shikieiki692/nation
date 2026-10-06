# -*- coding: utf-8 -*-
"""答案源清单 v2：对每个源卷组，取「题面最佳 PDF」的**严格同目录**内 PDF，
判定是否存在答案册 + 文字层长度（判断能否 fitz 抽取）。"""
import os, re, sys, csv, glob, difflib, collections

sys.stdout.reconfigure(encoding='utf-8')
try:
    import fitz
except Exception:
    fitz = None

OCR = '06-外部资料导入/OCR'
ANS_PAT = re.compile(r'答案|解析|参考|讲评|评分|手稿|key', re.I)


def norm(s):
    s = s.lower()
    return re.sub(r'[\s\(\)（）\[\]【】\-_\.、,，:：;；!！?？\'"“”‘’]+', '', s)


pdfs = [p.replace(os.sep, '/') for p in glob.glob(os.path.join(OCR, '**', '*.pdf'), recursive=True)
        if '_mineru_out' not in p.replace('\\', '/')]
by_dir = collections.defaultdict(list)
for p in pdfs:
    by_dir[os.path.dirname(p)].append(p)
PIN = {p: norm(os.path.splitext(os.path.basename(p))[0]) for p in pdfs}


def best_pdf(key):
    nk = norm(key)
    out = []
    for p, npn in PIN.items():
        r = difflib.SequenceMatcher(None, nk, npn).ratio()
        if nk and (nk in npn or npn in nk):
            r += 0.3
        out.append((r, p))
    out.sort(reverse=True)
    return out[0]


def tlen(p):
    if fitz is None:
        return -1
    try:
        d = fitz.open(p)
        n = sum(len(d[i].get_text()) for i in range(min(d.page_count, 40)))
        return n
    except Exception:
        return -2


rows = list(csv.DictReader(open('.workbuddy/tmp/opt_pipe/noans_list.csv', encoding='utf-8-sig')))
groups = collections.OrderedDict()
for r in rows:
    groups.setdefault((r['inst'], r['source_file']), []).append(r)
print('源卷组 %d\n' % len(groups))
res = []
for (inst, sf), cards in groups.items():
    vol = os.path.splitext(os.path.basename(sf))[0]
    sc, top = best_pdf(vol)
    d = os.path.dirname(top)
    sibs = [q for q in by_dir.get(d, []) if q != top]
    ans = [q for q in sibs if ANS_PAT.search(os.path.basename(q))]
    # 若题面 PDF 自身即答案文件（名字含答案）
    self_ans = bool(ANS_PAT.search(os.path.basename(top)))
    info = []
    for q in ans:
        info.append((os.path.basename(q), tlen(q)))
    res.append(dict(inst=inst, vol=vol, n=len(cards), top=os.path.relpath(top, OCR),
                    self_ans=self_ans, ans_cnt=len(ans), ans_info=' | '.join('%s(%d)' % (a, b) for a, b in info)))
    print('### [%s] %s  (%d卡)  score=%.2f%s' % (inst, vol, len(cards), sc, ' [源本身即答案]' if self_ans else ''))
    print('    dir: %s' % os.path.relpath(d, OCR))
    if ans:
        for a, b in info:
            print('    ✓答案: %s  [文字层=%d]' % (a, b))
    else:
        print('    ✗同目录无答案册')
    print()

with open('.workbuddy/tmp/opt_pipe/ans_source_inventory.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
    w.writeheader()
    w.writerows(res)
print('CSV → .workbuddy/tmp/opt_pipe/ans_source_inventory.csv')
