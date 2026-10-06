# -*- coding: utf-8 -*-
"""质心 UChO 4th/5th 答案回填：手写稿 OCR 定位「第N题」，按 Tour 分段避免题号重置串卷。
用法：python fill_ucho.py [--apply]
"""
import os, re, sys, glob, json

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Obsidion\妙妙屋')
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None
APPLY = '--apply' in sys.argv
LOC = '.workbuddy/tmp/opt_pipe/ocr_loc'
IMG = '04-题库/2026机构初赛模拟题/质心UChO/images'
ANS = '06-外部资料导入/OCR/01-题目/质心合集新/UChO模拟试题合集答案/'
PDF = {'UChO4': ANS + '4th ZCHEM-UChO 答案.pdf', 'UChO5': ANS + '5th ZCHEM-UChO 答案.pdf'}
MARK = re.compile(r'第\s*(\d+)\s*题')
PH = re.compile(r'源池(无|仅|未见)|源答案缺失|源无答案|无独立文字答案|答案缺失|题答逐问交错'
                r'|云端 ?OCR 产物的公式与配图保持原样|未逐字校对|源确缺答案')


def no_answer(t):
    i = t.find('## 参考答案')
    e = t.find('\n## 知识点映射', i)
    a = t[i:(e if e > 0 else len(t))] if i >= 0 else ''
    if re.search(r'!\[|<img', a):
        return False
    keep = [l for l in a.split('\n') if '校勘' not in l and not PH.search(l)]
    body = re.sub(r'(?m)^#{1,6}.*$', '', '\n'.join(keep))
    return len(re.sub(r'\s+', '', body)) < 12


def marks(data):
    out = []
    for pg in data:
        for b in pg['blocks']:
            s = b['t'].replace(' ', '')
            m = MARK.match(s)
            if m:
                out.append((pg['page'] - 1, b['y'], pg['scale'], int(m.group(1))))
    return out


def main():
    os.makedirs(IMG, exist_ok=True)
    cache = {}
    for tag in PDF:
        cache[tag] = json.load(open(os.path.join(LOC, tag + '.json'), encoding='utf-8'))
    ms = {t: marks(cache[t]) for t in cache}
    tour2 = {}
    for t in ms:
        firsts = [p for p, y, s, q in ms[t] if q == 1]
        tour2[t] = firsts[1] if len(firsts) > 1 else len(cache[t])
    print('Tour2 起始页：', {t: v + 1 for t, v in tour2.items()})

    cards = []
    for p in glob.glob('04-题库/2026机构初赛模拟题/质心UChO/题-*.md'):
        t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
        m = re.search(r'^source_file:[ \t]*(.*?)[ \t]*$', t, re.M)
        sf = m.group(1) if m else ''
        tag = 'UChO4' if '4thZCHEM' in sf else ('UChO5' if '5thZCHEM' in sf else None)
        if not tag:
            continue
        if not no_answer(t):          # ★ 只补无答案卡，绝不覆盖已有答案
            continue
        tour = 2 if 'Tour2' in sf else 1
        mid = re.search(r'题-UChO-\d+-(\d+)-', os.path.basename(p))
        cards.append((p, tag, tour, int(mid.group(1)), t))
    print('命中卡 %d' % len(cards))
    done = 0
    for p, tag, tour, q, t in cards:
        data = cache[tag]
        lo, hi = (0, tour2[tag]) if tour == 1 else (tour2[tag], len(data))
        sc = data[0]['scale']
        hit = [(pg, y) for pg, y, _, qq in ms[tag] if qq == q and lo <= pg < hi]
        if hit:
            start = (hit[0][0], hit[0][1])
        else:
            # 兜底：用相邻题界推断（OCR 漏识别手写题号时）
            prev = [pg for pg, y, _, qq in ms[tag] if qq < q and lo <= pg < hi]
            if prev:
                start = (max(prev) + 1, 0.0)
            elif lo == 0:
                start = (0, 0.0)
            else:
                print('  !! 无法推断 %s T%d 第%d题' % (tag, tour, q)); continue
            print('    （兜底推断 第%d题 起始 p%d）' % (q, start[0] + 1))
        pa, ya = start
        nxt = [(pg, y) for pg, y, _, qq in ms[tag] if qq > q and lo <= pg < hi]
        if nxt:
            pb, yb = min(nxt)
        else:
            pb, yb = hi - 1, 10 ** 9
        doc = fitz.open(PDF[tag])
        outs = []
        for pi in range(pa, pb + 1):
            pg = doc[pi]; R = pg.rect
            y0 = max(R.y0, ya / sc - 4) if pi == pa else R.y0 + 26
            y1 = min(R.y1, yb / sc + 4) if (pi == pb and nxt) else R.y1 - 22
            if y1 - y0 < 10:
                continue
            pix = pg.get_pixmap(dpi=200, clip=fitz.Rect(R.x0 + 22, y0, R.x1 - 22, y1))
            name = 'ucho_%s_t%d_q%02d_p%02d.png' % (tag.lower(), tour, q, pi + 1)
            pix.save(os.path.join(IMG, name)); outs.append(name)
        if not outs:
            continue
        md = ('（源：质心 %s 官方答案（手写稿）· Tour%d 第 %d 题；按原册裁区）\n\n' % (tag, tour, q)
              + '\n'.join('![](images/%s)' % o for o in outs)
              + '\n\n> 📌 据源答案册裁区回填（OCR 定位题界）。\n')
        ia = t.find('## 参考答案'); ik = t.find('## 知识点映射')
        new = t[:ia] + '## 参考答案\n\n' + md + '\n' + t[ik:]
        if APPLY:
            open(p, 'w', encoding='utf-8', newline='\n').write(new)
        done += 1
        print('  ✓ %s T%d 第%d题 → %d 图  %s' % (tag, tour, q, len(outs), os.path.basename(p)[:28]))
    print('回填 %d / %d  %s' % (done, len(cards), '[APPLY]' if APPLY else '[DRY-RUN]'))


if __name__ == '__main__':
    main()
