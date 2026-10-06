# -*- coding: utf-8 -*-
"""pilot_verify.py —— 试点 ⓪ 回源三元核验：为每张卡渲染【题面页 + 答案页】拼版。

定位策略：① 有文字层 → 8-gram 覆盖率选页；② 无文字层（扫描件）→ rapidocr 逐页 OCR 后同法。
输出：locate_out/PILOT10/<tag>_QA.png（左列题面页、右列答案页）
"""
import glob
import os
import re
import sys
import json

import fitz
from PIL import Image, ImageDraw

ROOT = r"C:\Obsidion\妙妙屋"
os.chdir(ROOT)
OUT = os.path.join(".workbuddy", "tmp", "opt_pipe", "locate_out", "PILOT10")
CACHE = os.path.join(".workbuddy", "tmp", "opt_pipe", "locate_out", "_ocr_cache")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)
try:
    fitz.TOOLS.mupdf_display_errors(False)
except Exception:
    pass

def hanzi(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s or "")


def grams(s, k=8):
    return [s[i:i + k] for i in range(0, max(1, len(s) - k + 1), k)]


def cov(hint, page_text):
    gs = grams(hint)
    if not gs:
        return 0.0
    return sum(1 for g in gs if g in page_text) / len(gs)


def page_texts(pdf):
    """返回 [每页汉字串]；无文字层则 rapidocr 逐页 OCR（带磁盘缓存）。"""
    key = os.path.join(CACHE, re.sub(r"[^\w]", "_", os.path.basename(pdf))[:60] + ".json")
    if os.path.exists(key):
        return json.load(open(key, encoding="utf-8"))
    with fitz.open(pdf) as d:
        raw = [d[i].get_text() for i in range(d.page_count)]
        total = sum(len(x.strip()) for x in raw)
        if total > 120:
            out = [hanzi(x) for x in raw]
        else:
            from rapidocr_onnxruntime import RapidOCR
            ocr = RapidOCR()
            out = []
            for i in range(d.page_count):
                pix = d[i].get_pixmap(dpi=135)
                tmp = os.path.join(CACHE, "_t.png")
                pix.save(tmp)
                res, _ = ocr(tmp)
                out.append(hanzi(" ".join(t for _, t, _ in (res or []))))
                print("    OCR %s p%d/%d" % (os.path.basename(pdf)[:24], i + 1, d.page_count))
    json.dump(out, open(key, "w", encoding="utf-8"), ensure_ascii=False)
    return out


def card_text(card):
    t = open(card, encoding="utf-8-sig").read().replace("\r\n", "\n")
    i = t.find("## 题目"); j = t.find("## 参考答案")
    q = re.sub(r"!\[\[?[^\]]*\]?\]", " ", t[i:j])
    a = re.sub(r"!\[\[?[^\]]*\]?\]", " ", t[j:])
    q = re.sub(r"\$[^$]*\$", " ", q); a = re.sub(r"\$[^$]*\$", " ", a)
    return hanzi(q)[:400], hanzi(a)[:400]


def render(doc, pi, dpi=140):
    pix = doc[pi].get_pixmap(dpi=dpi)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def _find_pdfs(card):
    """卡 → (题面PDF, 答案PDF)；答案册在同目录找「答案/参考/解析」，否则用题面 PDF 自身。"""
    import locale
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import locate_source_pdf as L
    idx, nidx, keys = L.norm_pdf_index()
    sf = L.get_source_file(card)
    qp, way = L.locate_pdf(sf, idx, nidx, keys)
    if not qp:
        return None, None, 'no-qpdf'
    d = os.path.dirname(qp)
    base = os.path.splitext(os.path.basename(qp))[0]
    cands = []
    for f in glob.glob(os.path.join(d, '*.pdf')):
        b = os.path.basename(f)
        if f == qp:
            continue
        if re.search(r'答案|参考|解析|评分|讲评', b):
            cands.append((len(os.path.commonprefix([base, os.path.splitext(b)[0]])), f))
    if cands:
        cands.sort(reverse=True)
        ap = cands[0][1]
    else:
        ap = qp
    return qp, ap, way


def main():
    cards = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
    for card in cards:
        m = re.match(r'题-([A-Za-z0-9]+-\d+-\d+)-', os.path.basename(card))
        tag = m.group(1) if m else os.path.basename(card)[:16]
        print('=' * 100)
        print('[%s] %s' % (tag, os.path.basename(card)[:60]))
        qpdf, apdf, way = _find_pdfs(card)
        if not qpdf:
            print('   !! 未定位题面 PDF'); continue
        print('  题面 PDF:', qpdf.replace(os.sep, '/')[-70:])
        print('  答案 PDF:', (apdf or '(无)').replace(os.sep, '/')[-70:])
        qh, ah = card_text(card)
        if not qh or not ah:
            print('   !! 卡内题目/答案区为空'); continue
        qimgs, aimgs, qsel, asel, qcov, acov = [], [], [], [], 0, 0
        try:
            qt = page_texts(qpdf)
            qsc = sorted([(cov(qh, p), i) for i, p in enumerate(qt)], reverse=True)
            qsel = [i for s, i in qsc[:2] if s > 0.05] or [qsc[0][1]]; qcov = qsc[0][0]
            with fitz.open(qpdf) as dq:
                qimgs = [render(dq, i, 140) for i in qsel]
        except Exception as e:
            print('   !! 题面渲染失败', e)
        try:
            at = page_texts(apdf)
            asc = sorted([(cov(ah, p), i) for i, p in enumerate(at)], reverse=True)
            asel = [i for s, i in asc[:2] if s > 0.05] or [asc[0][1]]; acov = asc[0][0]
            with fitz.open(apdf) as da:
                aimgs = [render(da, i, 140) for i in asel]
        except Exception as e:
            print('   !! 答案渲染失败', e)
        print('  题面页 %s cov=%.2f | 答案页 %s cov=%.2f'
              % ([i + 1 for i in qsel], qcov, [i + 1 for i in asel], acov))
        if not qimgs and not aimgs:
            continue
        W = 980
        def col(imgs):
            ims = [im.resize((W, int(im.height * W / im.width))) for im in imgs]
            h = sum(i.height for i in ims) + 24 * len(ims)
            c = Image.new('RGB', (W, max(1, h)), 'white'); y = 0
            for im in ims:
                c.paste(im, (0, y + 22)); y += im.height + 24
            return c
        L2 = col(qimgs or [Image.new('RGB', (W, 100), 'white')])
        R2 = col(aimgs or [Image.new('RGB', (W, 100), 'white')])
        H = max(L2.height, R2.height)
        mm = Image.new('RGB', (L2.width + R2.width + 20, H + 30), 'white')
        mm.paste(L2, (0, 30)); mm.paste(R2, (L2.width + 20, 30))
        dr = ImageDraw.Draw(mm)
        dr.text((6, 8), '[题面] %s' % tag, fill='red'); dr.text((L2.width + 26, 8), '[答案] %s' % tag, fill='blue')
        pp = os.path.join(OUT, '%s_QA.png' % tag); mm.save(pp)
        print('  →', pp)


if __name__ == '__main__':
    main()
