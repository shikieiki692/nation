# -*- coding: utf-8 -*-
"""答案册定位器：为 noans_list.csv 中每张无答案卡，在 OCR 全树中模糊匹配「题目 PDF」与「答案 PDF」。
策略：
  1) 索引 OCR 全树 .pdf（跳过 _mineru_out 的中间产物）
  2) 对每张卡的 source_file 卷名 → 与 PDF 名做 difflib 相似度
  3) 同时给出「同目录/同前缀的 答案/解析/参考 PDF」作为答案候选
输出：noans_answer_candidates.csv
"""
import os, re, sys, csv, glob, difflib, collections

sys.stdout.reconfigure(encoding='utf-8')
OCR = '06-外部资料导入/OCR'
ANS_PAT = re.compile(r'答案|解析|参考|讲评|评分')

# 1) 索引 PDF
pdfs = []
for p in glob.glob(os.path.join(OCR, '**', '*.pdf'), recursive=True):
    if '_mineru_out' in p.replace('\\', '/') or '/auto/' in p.replace('\\', '/'):
        continue
    pdfs.append(p.replace(os.sep, '/'))
print('OCR PDF 索引：%d 份' % len(pdfs))


def norm(s):
    s = s.lower()
    s = re.sub(r'[\s\(\)（）\[\]【】\-_\.、,，:：;；!！?？\'"“”‘’]+', '', s)
    return s


PIN = {p: norm(os.path.splitext(os.path.basename(p))[0]) for p in pdfs}


def best_pdf(key, rest=None):
    nk = norm(key)
    out = []
    for p, npn in PIN.items():
        r = difflib.SequenceMatcher(None, nk, npn).ratio()
        # 子串加成
        if nk and (nk in npn or npn in nk):
            r += 0.3
        out.append((r, p))
    out.sort(reverse=True)
    return out[:6]


rows = list(csv.DictReader(open('.workbuddy/tmp/opt_pipe/noans_list.csv', encoding='utf-8-sig')))

# 按 (inst, source_file) 归组
groups = collections.OrderedDict()
for r in rows:
    groups.setdefault((r['inst'], r['source_file']), []).append(r)

print('源卷组数：%d' % len(groups))
print()
out_rows = []
for (inst, sf), cards in groups.items():
    vol = os.path.splitext(os.path.basename(sf))[0]
    cands = best_pdf(vol)
    # 找答案候选：在候选同目录找 答案类
    ans_c = []
    for sc, p in cands:
        d = os.path.dirname(p)
        for q in pdfs:
            if os.path.dirname(q) == d and ANS_PAT.search(os.path.basename(q)):
                ans_c.append(q)
    ans_c = sorted(set(ans_c))
    top = cands[0] if cands else (0, '')
    print('### [%s] %s  （%d 卡）' % (inst, vol, len(cards)))
    print('   题面最佳: %.2f  %s' % (top[0], os.path.relpath(top[1], OCR) if top[1] else '-'))
    for q in ans_c[:4]:
        print('   同目录答案: %s' % os.path.relpath(q, OCR))
    if not ans_c:
        # 全树按卷名找答案
        fz = []
        nk = norm(vol)
        for p, npn in PIN.items():
            if ANS_PAT.search(os.path.basename(p)):
                r = difflib.SequenceMatcher(None, nk, npn).ratio()
                if nk and (nk[:6] in npn or npn[:6] in nk):
                    r += 0.2
                if r > 0.35:
                    fz.append((r, p))
        fz.sort(reverse=True)
        for sc, p in fz[:3]:
            print('   全树候选答案: %.2f %s' % (sc, os.path.relpath(p, OCR)))
    print()
    out_rows.append(dict(inst=inst, vol=vol, ncards=len(cards),
                         top_pdf=top[1] if top[1] else '', top_score='%.2f' % top[0],
                         ans_candidates=' | '.join(ans_c[:4])))

with open('.workbuddy/tmp/opt_pipe/noans_answer_candidates.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
    w.writeheader()
    w.writerows(out_rows)
print('CSV → .workbuddy/tmp/opt_pipe/noans_answer_candidates.csv')
