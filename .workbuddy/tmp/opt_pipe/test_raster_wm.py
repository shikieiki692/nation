# -*- coding: utf-8 -*-
r"""测试「整页栅格」源的置空效果：置空后是否变空白（只读探查）。"""
import os, glob
import fitz
os.chdir(r'C:\Obsidion\妙妙屋')
OUT = '.workbuddy/tmp/opt_pipe/wmtest'
os.makedirs(OUT, exist_ok=True)

CASES = [
    ('清北营', '06-外部资料导入/OCR/01-题目/2026年清北营4月春季班/春季模拟1.pdf'),
    ('化英社', '06-外部资料导入/OCR/01-题目/2026年化英社4月春季班/第40届初赛模拟10（清晰版）.pdf'),
    ('汇智', '06-外部资料导入/OCR/01-题目/2026年汇智五一有机班/长沙化学刷初赛模拟1.pdf'),
]
for org, pat in CASES:
    fs = glob.glob(pat)
    if not fs:
        fs = glob.glob('06-外部资料导入/OCR/01-题目/*' + org + '*/**/*.pdf', recursive=True)
    if not fs:
        print('%s 未找到 PDF' % org); continue
    f = fs[0]
    d = fitz.open(f)
    pg = d[1] if d.page_count > 1 else d[0]
    imgs = pg.get_images(full=True)
    # 置空前渲染
    pg.get_pixmap(dpi=110).save(os.path.join(OUT, '%s_p2_before.png' % org))
    names = []
    for im in imgs:
        xref, w, h, name = im[0], im[2], im[3], im[7]
        names.append((xref, w, h, name))
        try:
            d.xref_set_key(pg.xref, 'Resources/XObject/%s' % name, 'null')
        except Exception as e:
            print('  %s 置空失败 %s: %s' % (org, name, e))
    pm = pg.get_pixmap(dpi=110)
    pm.save(os.path.join(OUT, '%s_p2_after.png' % org))
    # 墨迹量对比（暗像素占比）
    import numpy as np
    def dark(fp):
        a = np.frombuffer(fitz.Pixmap(fp).samples, dtype=np.uint8)
        return float((a < 128).mean())
    print('%-6s %d 页 ｜ 该页内嵌图 %d 个 %s' % (org, d.page_count, len(names), names[:2]))
    print('        置空前暗占比 %.4f → 置空后 %.4f' % (dark(os.path.join(OUT, '%s_p2_before.png' % org)), dark(os.path.join(OUT, '%s_p2_after.png' % org))))
    d.close()
