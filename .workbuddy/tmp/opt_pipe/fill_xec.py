# -*- coding: utf-8 -*-
"""XeChem 模拟三/四/五 答案回填：把 `重新ocr/` 已有的答案裁页 PDF → PNG → 回填卡。
选卡：source_file 前缀 + 卡 ID 末段题号（安全，避 ID 撞车）。
用法：python fill_xec.py [--apply]
"""
import os, re, sys, glob

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
R = '06-外部资料导入/OCR/重新ocr/'
IMG = '04-题库/2026机构初赛模拟题/XeChem/images'

# (source_file 前缀, 题号, [裁页 PDF], 说明)
JOBS = [
    ('XeChem模拟三（晶体）答案', 4, ['模拟三_第4题_答案卷内印题面__p07.pdf'], '模拟三 第4题'),
    ('XeChem模拟四答案', 7, ['模拟四_第7题_p05_rot.pdf', '模拟四_第7题_p06_rot.pdf'], '模拟四 第7题'),
    ('XeChem模拟四答案', 8, ['模拟四_第8题_p07_rot.pdf', '模拟四_第8题_p08.pdf'], '模拟四 第8题'),
    ('XeChem模拟五答案', 2, ['模拟五_第2题_p01_rot.pdf', '模拟五_第2题_p02_rot.pdf',
                             '模拟五_第2题_p03_rot.pdf'], '模拟五 第2题'),
]
os.makedirs(IMG, exist_ok=True)
done = 0
for src, q, pdfs, note in JOBS:
    cards = []
    for p in glob.glob('04-题库/2026机构初赛模拟题/XeChem/题-*.md'):
        t = open(p, encoding='utf-8-sig').read().replace('\r\n', '\n')
        m = re.search(r'^source_file:[ \t]*(.*?)[ \t]*$', t, re.M)
        sf = m.group(1) if m else ''
        mid = re.search(r'题-XeC-\d+-(\d+)-', os.path.basename(p))
        if src in sf and mid and int(mid.group(1)) == q:
            cards.append((p, t))
    if not cards:
        print('!! 无卡 %s 第%d题' % (src, q)); continue
    outs = []
    for pdf in pdfs:
        d = fitz.open(os.path.join(R, pdf))
        tagname = re.sub(r'[^0-9A-Za-z]+', '', pdf)[:16]
        for i in range(d.page_count):
            pix = d[i].get_pixmap(dpi=200)
            name = 'xec_%s_q%02d_%s_p%02d.png' % (src.replace('XeChem', 'xc').replace('答案', ''),
                                                  q, tagname, i + 1)
            pix.save(os.path.join(IMG, name)); outs.append(name)
    md = ('（源：XeChem %s 答案裁页，前轮已裁；本轮回填）\n\n' % note
          + '\n'.join('![](images/%s)' % o for o in outs)
          + '\n\n> 📌 据 `重新ocr/` 已裁答案页回填。\n')
    for p, t in cards:
        ia = t.find('## 参考答案'); ik = t.find('## 知识点映射')
        new = t[:ia] + '## 参考答案\n\n' + md + '\n' + t[ik:]
        if APPLY:
            open(p, 'w', encoding='utf-8', newline='\n').write(new)
        done += 1
    print('%-18s 第%d题 → %d 图 → %d 卡' % (src[:18], q, len(outs), len(cards)))
print('回填 %d 卡  %s' % (done, '[APPLY]' if APPLY else '[DRY-RUN]'))
