# -*- coding: utf-8 -*-
"""O1 回源渲染 v2：按 pdf_text_check 的 8-gram 最佳页渲染（题面 + 答案）。

verify_dump 的命中页与 pdf_text_check 不一致（实测 GM-02-02 / GM-04-03 偏页）⇒
统一改用 pdf_text_check 的 coverage() 最佳页（含次佳），DPI 130，输出到
locate_out/O1V2/<tag>/q_pNN.png ／ a_pNN.png。
"""
import os, re, sys
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE)))
import pdf_text_check as P          # 复用 hanzi/card_sections/coverage/find_answer_pdf
import locate_source_pdf as L

ROOT = L.ROOT
OUT = os.path.join(HERE, "locate_out", "O1V2")
DPI = 130

cards = [l.strip() for l in open(os.path.join(HERE, "o1_cards.txt"), encoding="utf-8") if l.strip()]
for rel in cards:
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    tag = re.sub(r"^题-", "", os.path.basename(rel))[:22]
    od = os.path.join(OUT, tag)
    os.makedirs(od, exist_ok=True)
    txt = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    qtext, atext = P.card_sections(txt)
    qpdf = L.locate_pdf(L.get_source_file(p), *L.norm_pdf_index())[0]
    if not qpdf:
        print("[!!] 未定位 PDF:", tag); continue
    doc = fitz.open(qpdf)
    pages = [doc[i].get_text() for i in range(doc.page_count)]
    hits, cov = P.coverage(pages, qtext)
    print("== %s | 题面 %s cov=%.2f | %s" % (tag, [h[1] for h in hits], cov, os.path.basename(qpdf)))
    for c, pg in hits[:2]:
        pix = doc[pg - 1].get_pixmap(dpi=DPI)
        pix.save(os.path.join(od, "q_p%02d.png" % pg))
    # 答案页：同 PDF 或 答案 PDF
    apdf = P.find_answer_pdf(qpdf)[0] or qpdf
    if atext:
        adoc = doc if apdf == qpdf else fitz.open(apdf)
        apages = [adoc[i].get_text() for i in range(adoc.page_count)]
        ahits, acov = P.coverage(apages, atext)
        print("   答案 %s cov=%.2f | %s" % ([h[1] for h in ahits], acov, os.path.basename(apdf)))
        for c, pg in ahits[:2]:
            pix = adoc[pg - 1].get_pixmap(dpi=DPI)
            pix.save(os.path.join(od, "a_p%02d.png" % pg))
        if apdf != qpdf:
            adoc.close()
    doc.close()
print("DONE ->", OUT)
