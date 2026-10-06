# -*- coding: utf-8 -*-
"""OCR 题号定位器：对**无文字层扫描件**逐页 OCR（rapidocr），产出带 y 坐标的块索引（缓存 JSON），
用于按「第N题」精确裁区。
用法：python ocr_index.py <pdf> <tag> [dpi]
输出：.workbuddy/tmp/opt_pipe/ocr_loc/<tag>.json
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
    except Exception:
        pass
except Exception:
    fitz = None
OUT = '.workbuddy/tmp/opt_pipe/ocr_loc'


def main():
    pdf, tag = sys.argv[1], sys.argv[2]
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
    os.makedirs(OUT, exist_ok=True)
    cache = os.path.join(OUT, tag + '.json')
    if os.path.exists(cache):
        print('缓存命中 %s' % cache)
        return
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    doc = fitz.open(pdf)
    data = []
    for i in range(doc.page_count):
        pg = doc[i]
        pix = pg.get_pixmap(dpi=dpi)
        tmp = os.path.join(OUT, '_tmp.png')
        pix.save(tmp)
        res, _ = ocr(tmp)
        blocks = []
        for box, txt, sc in (res or []):
            y = float(min(p[1] for p in box)); x = float(min(p[0] for p in box))
            blocks.append(dict(y=round(y, 1), x=round(x, 1), t=txt))
        blocks.sort(key=lambda b: (b['y'], b['x']))
        data.append(dict(page=i + 1, w=pix.width, h=pix.height, scale=dpi / 72.0, blocks=blocks))
        mk = [b['t'] for b in blocks if re.search(r'第\s*\d+\s*题', b['t'].replace(' ', ''))]
        print('  p%-3d 块%-3d  %s' % (i + 1, len(blocks), mk[:3]))
    json.dump(data, open(cache, 'w', encoding='utf-8'), ensure_ascii=False)
    if os.path.exists(os.path.join(OUT, '_tmp.png')):
        os.remove(os.path.join(OUT, '_tmp.png'))
    print('索引 → %s' % cache)


if __name__ == '__main__':
    main()
