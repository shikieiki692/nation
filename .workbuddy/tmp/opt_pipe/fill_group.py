# -*- coding: utf-8 -*-
"""按「卷」批量回填③组答案（**安全选卡**：按 source_file 匹配 + 仅补无答案卡）。
用法：python fill_group.py <answer_pdf> <ocr_tag> <out_imgdir> <src_substr> <dest_prefix> <label> [--apply]
 - 选卡：04-题库/2026机构初赛模拟题/**/题-*.md 且 source_file 含 src_substr 且答案区无实质内容
 - 题号：取卡文件名 ID 的末段数字（`题-HYS-01-03-…` → 3）
 - 裁区：用 ocr_index 的 <ocr_tag>.json 定位「第q题 .. 第q+1题」
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
LOC = '.workbuddy/tmp/opt_pipe/ocr_loc'
MARK = re.compile(r'第\s*(\d+)\s*题')
PH = re.compile(r'源池(无|仅|未见)|源答案缺失|源无答案|无独立文字答案|答案缺失|题答逐问交错'
                r'|云端 ?OCR 产物的公式与配图保持原样|未逐字校对|源确缺答案')


def ans_sec(t):
    i = t.find('## 参考答案')
    if i < 0:
        return ''
    e = t.find('\n## 知识点映射', i)
    return t[i:(e if e > 0 else len(t))]


def no_answer(t):
    a = ans_sec(t)
    if re.search(r'!\[|<img', a):
        return False
    keep = [l for l in a.split('\n') if '校勘' not in l and not PH.search(l)]
    body = re.sub(r'(?m)^#{1,6}.*$', '', '\n'.join(keep))
    body = re.sub(r'!\[\[?[^\]]*\]?\]', '', body)
    return len(re.sub(r'\s+', '', body)) < 12


def find_mark(data, q, after=None):
    for pg in data:
        for b in pg['blocks']:
            s = b['t'].replace(' ', '')
            m = MARK.search(s)
            if not m or int(m.group(1)) != q:
                continue
            if s.index('第') > 8:
                continue
            if after and (pg['page'] - 1, b['y']) <= after:
                continue
            return pg['page'] - 1, b['y'], pg['scale']
    return None


def main():
    pdf, tag, out_dir, sub, prefix, label = sys.argv[1:7]
    APPLY = '--apply' in sys.argv
    data = json.load(open(os.path.join(LOC, tag + '.json'), encoding='utf-8'))
    doc = fitz.open(pdf)
    os.makedirs(out_dir, exist_ok=True)
    cards = []
    for p in glob.glob('04-题库/2026机构初赛模拟题/**/题-*.md', recursive=True):
        t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
        m = re.search(r'^source_file:[ \t]*(.*?)[ \t]*$', t, re.M)
        if not m or sub not in m.group(1):
            continue
        if not no_answer(t):
            continue
        mid = re.search(r'题-[A-Za-z0-9]+-\d+-(\d+)-', os.path.basename(p))
        if not mid:
            print('  !! 取不到题号', os.path.basename(p)); continue
        cards.append((p, int(mid.group(1)), t))
    print('命中无答案卡 %d 张' % len(cards))
    done = 0
    for p, q, t in cards:
        a = find_mark(data, q)
        if not a:
            print('  !! 未定位 第%d题  %s' % (q, os.path.basename(p)[:30])); continue
        pa, ya, sc = a
        b = find_mark(data, q + 1, after=(pa, ya))
        pb, yb = (b[0], b[1]) if b else (len(data) - 1, 10 ** 9)
        outs = []
        for pg_i in range(pa, pb + 1):
            pg = doc[pg_i]; R = pg.rect
            y0 = max(R.y0, (ya / sc) - 4) if pg_i == pa else R.y0 + 30
            y1 = min(R.y1, (yb / sc) + 4) if (pg_i == pb and b) else R.y1 - 26
            if y1 - y0 < 10:
                continue
            pix = pg.get_pixmap(dpi=200, clip=fitz.Rect(R.x0 + 26, y0, R.x1 - 26, y1))
            d = os.path.join(out_dir, '%s_q%02d_p%02d.png' % (prefix, q, pg_i + 1))
            pix.save(d); outs.append(os.path.basename(d))
        if not outs:
            continue
        md = ('（源：%s · 第 %d 题；按原册裁区，保留结构图与公式）\n\n' % (label, q)
              + '\n'.join('![](images/%s)' % o for o in outs)
              + '\n\n> 📌 据源答案册裁区回填（OCR 定位题界）。\n')
        ia = t.find('## 参考答案'); ik = t.find('## 知识点映射')
        new = t[:ia] + '## 参考答案\n\n' + md + '\n' + t[ik:]
        if APPLY:
            open(p, 'w', encoding='utf-8', newline='\n').write(new)
        done += 1
        print('  ✓ 第%d题 → %d 图  %s' % (q, len(outs), os.path.basename(p)[:34]))
    print('回填 %d / %d  %s' % (done, len(cards), '[APPLY]' if APPLY else '[DRY-RUN]'))


if __name__ == '__main__':
    main()
