# -*- coding: utf-8 -*-
"""O1 回源定位 v4：对 cov=0 的卡，用卡内独特关键词扫 PDF 文字层定位页码。"""
import os, re, sys
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import locate_source_pdf as L

ROOT = L.ROOT

KEYS = {
    "题-HYS-40-07-早在1979年研究人员就报道.md": ["1979", "费里尔", "吡喃糖"],
    "题-QBY-13-05-51德国马克斯普朗克煤炭研究.md": ["Ritter", "普朗克", "氨基酸衍生物"],
    "题-CM-21-08-氮杂环庚烷azepanes是.md": ["azepane", "丙咪嗪", "Imipramine"],
    "题-YJ-02-08-光化学在自然界和日常生活中扮.md": ["Zimmerman", "光重排", "激发态"],
    "题-HYS-01-08-耐甲氧西林金黄色葡萄球菌MR.md": ["甲氧西林", "MRSA", "阿贝卡星"],
    "题-YJ-12-06-61请按照酸性从强到弱给以下.md": ["酸性从强到弱", "烯丙"],
    "题-QBY-13-08-本题需注意立体化学Vinig.md": ["Vinigrol", "vinigrol"],
    "题-CM-199-08-200多年前化学家在印度的防己科.md": ["Picrotoxin", "防己"],
    "题-GM-02-02-乙酸丁酯是一种重要的有机溶剂.md": ["乙酸丁酯"],
    "题-GM-04-03-31几种分类311热塑性塑料.md": ["热塑性", "ADC"],
}

for fn, kws in KEYS.items():
    cp = os.path.join(ROOT, "04-题库", "2026机构初赛模拟题",
                      ("化英社" if fn.startswith("题-HYS") else
                       "清北营" if fn.startswith("题-QBY") else
                       "chemy" if fn.startswith("题-CM") else
                       "伽马" if fn.startswith("题-GM") else "壹尖培优"), fn)
    qpdf = L.locate_pdf(L.get_source_file(cp), *L.norm_pdf_index())[0]
    if not qpdf:
        print("== %s | 未定位 PDF" % fn[:30]); continue
    with fitz.open(qpdf) as d:
        hits = {}
        for i in range(d.page_count):
            t = d[i].get_text()
            ks = [k for k in kws if k in t]
            if ks:
                hits[i + 1] = ks
    print("== %s" % fn[:34])
    print("   PDF: %s" % os.path.basename(qpdf))
    print("   关键词命中页: %s" % (hits if hits else "无（文字层可能失效）"))
