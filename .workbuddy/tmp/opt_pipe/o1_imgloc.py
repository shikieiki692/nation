# -*- coding: utf-8 -*-
"""O1 回源定位 v3：对文字层失效（cov=0）的卡，用「卡内图片 sha256 ↔ PDF 页图片 sha256」定位。

原理（SOP ④-e 同款判据）：建卡时的图是从源 PDF 切出来的，内容哈希一致。
输出：每卡命中的页码清单（按命中图数排序），并把命中的图导出供目检。
"""
import os, re, sys, glob, hashlib
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import locate_source_pdf as L

ROOT = L.ROOT
QB = os.path.join(ROOT, "04-题库", "2026机构初赛模拟题")


def card_imgs(card_path):
    """卡内引用的图 → {hash: 绝对路径}（题面+答案都算）。"""
    t = open(card_path, encoding="utf-8-sig", errors="replace").read()
    hs = set(re.findall(r'images/([0-9a-f]{64}\.(?:jpg|png))', t))
    hs |= set(re.findall(r'!\[\[([0-9a-f]{64}\.(?:jpg|png))\]\]', t))
    out = {}
    for h in hs:
        p = os.path.join(os.path.dirname(card_path), "images", h)
        if os.path.exists(p):
            out[h] = p
    return out


def file_sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def pdf_page_img_shas(pdf):
    """{page_no(1-based): set(sha)}（流式提取各页内嵌图）。"""
    res = {}
    with fitz.open(pdf) as d:
        for i in range(d.page_count):
            shas = set()
            for img in d[i].get_images(full=True):
                xref = img[0]
                try:
                    raw = d.extract_image(xref)
                    shas.add(hashlib.sha256(raw["image"]).hexdigest())
                except Exception:
                    pass
            if shas:
                res[i + 1] = shas
    return res


cards = [l.strip() for l in open(os.path.join(HERE, "o1_cards.txt"), encoding="utf-8") if l.strip()]
for rel in cards:
    cp = os.path.join(ROOT, rel.replace("/", os.sep))
    tag = re.sub(r"^题-", "", os.path.basename(rel))[:22]
    imgs = card_imgs(cp)
    if not imgs:
        print("== %s | 卡内无图（跳过图片定位）" % tag)
        continue
    shas = {file_sha(p): h for h, p in imgs.items()}
    qpdf = L.locate_pdf(L.get_source_file(cp), *L.norm_pdf_index())[0]
    if not qpdf:
        print("== %s | 未定位 PDF" % tag)
        continue
    pages = pdf_page_img_shas(qpdf)
    hit = {}
    for pg, shas_p in pages.items():
        n = len(shas.keys() & shas_p)
        if n:
            hit[pg] = n
    hit_s = sorted(hit.items(), key=lambda kv: -kv[1])
    print("== %s | 卡图 %d 张（实存 %d）| PDF %s" % (
        tag, len(imgs), len(shas), os.path.basename(qpdf)))
    print("   图命中页:", hit_s[:6] if hit_s else "无")
