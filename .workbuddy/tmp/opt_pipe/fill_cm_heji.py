# -*- coding: utf-8 -*-
"""回收 chemy 第33/34/35/37届「题目合集」14 张无答案卡：按其答案合集 PDF 的
「分节 + 第N题」裁区回填（忠实保留公式/图）。
用法：python fill_cm_heji.py [--apply]
"""
import os, re, sys, glob

sys.stdout.reconfigure(encoding='utf-8')
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None
os.chdir(r'C:\Obsidion\妙妙屋')
APPLY = '--apply' in sys.argv
O = '06-外部资料导入/OCR/chemy/'
P = {
    '33': O + '第33届Chemy化学奥林匹克题目合集答案..pdf',
    '34': O + '第34届Chemy化学奥林匹克题目合集答案..pdf',
    '35': O + '第35届中国化学奥林匹克Chemy参考答案合集/第35届中国化学奥林匹克Chemy参考答案合集._1-199.pdf',
    '37': O + '第37届Chemy题目合集答案/第37届Chemy题目合集答案._1-199.pdf',
}
IMG = '04-题库/2026机构初赛模拟题/chemy/images'
CARD = '04-题库/2026机构初赛模拟题/chemy/题-%s-*.md'

# (卡ID, pdf键, 分节锚, 题号)
MAP = [
    ('CM-63-06', '33', '模拟试卷3 答案', 6),
    ('CM-64-01', '33', '模拟试卷4 答案', 1),
    ('CM-64-08', '33', '模拟试卷4 答案', 8),
    ('CM-65-07', '33', '模拟试卷5 答案', 7),
    ('CM-68-08', '33', '模拟试卷8 答案', 8),
    ('CM-70-09', '33', '有机化学专题1 答案', 9),
    ('CM-76-04', '34', '模拟试卷3 答案', 4),
    ('CM-79-06', '34', '模拟试卷6 答案', 6),
    ('CM-80-09', '34', '模拟试卷7 答案', 9),
    ('CM-81-06', '34', '模拟试卷8 答案', 6),
    ('CM-82-01', '34', '模拟试卷9 答案', 1),
    ('CM-91-01', '35', '模拟试题1 参考答案', 1),
    ('CM-97-07', '35', '（决赛）模拟试题8 参考答案', 7),
    ('CM-144-03', '37', '（初赛）模拟试题19 参考答案', 3),
]


def hits(pg, txt):
    out = []
    for v in dict.fromkeys([txt, txt.replace(' ', ''), txt.replace('  ', ' ')]):
        if v:
            out += pg.search_for(v)
    return out


def sec_end_page(doc, sp, cur):
    """分节上界：sp 之后第一个出现**不同**「第N届…答案」分节标题的页（不含）。
    跳过与当前节同名的重复页眉。防越界。"""
    rx = re.compile(r'第\s*\d+\s*届')
    curk = cur.replace(' ', '')
    for p in range(sp + 1, doc.page_count):
        for line in doc[p].get_text().split('\n'):
            ln = line.strip()
            if not ln or len(ln) > 60 or '...' in ln or '…' in ln:
                continue
            if 8 <= len(ln) <= 50 and rx.search(ln) and '答案' in ln and ('模拟' in ln or '专题' in ln):
                if curk and curk in ln.replace(' ', ''):
                    continue                    # 同一分节的重复页眉
                return p
    return doc.page_count


def find_section_page(doc, section):
    """定位分节首页：整行含分节名、且**非目录行**（目录行有点线/页码，长度长）。"""
    key = section.replace(' ', '')
    for p in range(doc.page_count):
        for line in doc[p].get_text().split('\n'):
            ln = line.strip()
            if not ln or len(ln) > 60 or '...' in ln or '…' in ln:
                continue                      # 目录行
            if key in ln.replace(' ', ''):
                return p
    return None


def crop_question(doc, section, q, dest_prefix, dpi=200, margin=6):
    sp = find_section_page(doc, section)
    if sp is None:
        return [], 'sec-not-found'
    r = hits(doc[sp], section)
    sy = min(x.y0 for x in r) if r else 0.0
    hi = sec_end_page(doc, sp, section)   # ★ 只在本节内裁，防跨节越界
    start, end = '第%d 题' % q, '第%d 题' % (q + 1)
    sp2 = sy2 = None
    for p in range(sp, hi):
        for x in hits(doc[p], start):
            if p == sp and x.y0 <= sy + 2:
                continue
            sp2, sy2 = p, x.y0; break
        if sp2 is not None:
            break
    if sp2 is None:
        return [], 'q-not-found'
    ep2 = ey2 = None
    for p in range(sp2, hi):
        for x in hits(doc[p], end):
            if p == sp2 and x.y0 <= sy2 + 2:
                continue
            ep2, ey2 = p, x.y0; break
        if ep2 is not None:
            break
    if ep2 is None:
        ep2 = min(hi - 1, sp2); ey2 = doc[ep2].rect.y1 - 40
    outs = []
    for p in range(sp2, ep2 + 1):
        pg = doc[p]; R = pg.rect
        y0 = (sy2 - margin) if p == sp2 else (R.y0 + 34)
        y1 = (ey2 + margin) if p == ep2 else (R.y1 - 34)
        if y1 - y0 < 12:
            continue
        pix = pg.get_pixmap(dpi=dpi, clip=fitz.Rect(R.x0 + 40, max(R.y0, y0), R.x1 - 40, min(R.y1, y1)))
        d = os.path.join(IMG, '%s_p%02d.png' % (dest_prefix, p + 1))
        pix.save(d); outs.append((os.path.basename(d), pix.width, pix.height))
    return outs, 'ok'


def rewrite(card, ans):
    t = open(card, encoding='utf-8-sig').read().replace('\r\n', '\n')
    ia = t.find('## 参考答案'); ik = t.find('## 知识点映射')
    assert ia > 0 and ik > ia, card
    new = t[:ia] + '## 参考答案\n\n' + ans + '\n\n' + t[ik:]
    if APPLY:
        open(card, 'w', encoding='utf-8', newline='\n').write(new)


summary = []
for cid, pk, sec, q in MAP:
    fs = glob.glob(CARD % cid)
    if not fs:
        print('!! 卡未找到 %s' % cid); continue
    card = fs[0]
    doc = fitz.open(P[pk])
    outs, st = crop_question(doc, sec, q, 'cm_heji_' + cid)
    doc.close()
    print('%-12s [%s届] %s  第%d题 → %s  %s'
          % (cid, pk, sec[:20], q, st, ' '.join(o[0] for o in outs)))
    if st != 'ok':
        continue
    md = ('（源：chemy 第%s届题目合集答案 · %s · 第 %d 题；按原册裁区，保留公式与图）\n\n' % (pk, sec, q)
          + '\n'.join('![](images/%s)' % o[0] for o in outs)
          + '\n\n> 📌 据源答案合集逐题裁区回填。\n')
    rewrite(card, md)
    summary.append((cid, len(outs)))

print('\n成功 %d / %d' % (len(summary), len(MAP)))
print('%s' % ('[APPLY] 已写盘' if APPLY else '[DRY-RUN]'))
