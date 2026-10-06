# -*- coding: utf-8 -*-
"""pilot_verify.py —— 试点 ⓪ 回源三元核验：为每张卡渲染【题面页 + 答案页】拼版。

定位策略：① 有文字层 → 8-gram 覆盖率选页；② 无文字层（扫描件）→ rapidocr 逐页 OCR 后同法。
输出：locate_out/PILOT10/<tag>_QA.png（左列题面页、右列答案页）
"""
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

A = "06-外部资料导入/OCR/01-题目"
CONF = [
    ("HYS-40-05", 5,
     f"{A}/2026年化英社五一物化班/2026年化英社五一物化班/华英社 物化专题 2026五一期间/第40届化英社奥林匹克（决赛）模拟试题2 试卷（清晰）.pdf",
     f"{A}/2026年化英社五一物化班/2026年化英社五一物化班/华英社 物化专题 2026五一期间/第40届决赛模拟试题2答案（清晰版）.pdf"),
    ("QBY-01-06", 6,
     f"{A}/2026清北营夏令营/清北营高二试卷（前13套）/2026年清北营暑假高二班-试卷1.pdf",
     f"{A}/2026清北营夏令营/清北营高二试卷（前13套）/2026年清北营暑假高二班-试卷1-参考答案.pdf"),
    ("CM-10-05", 5,
     f"{A}/2026年chemy夏令营/第40届chemy夏季班/第40届chemy初赛模拟10/第40届chemy初赛模拟10试卷.pdf",
     f"{A}/2026年chemy夏令营/第40届chemy夏季班/第40届chemy初赛模拟10/第40届chemy初赛模拟10答案.pdf"),
    ("GM-07-03", 3,
     f"{A}/2026伽马暑假刷题班/伽马化学2026年暑期模拟7.pdf",
     f"{A}/2026伽马暑假刷题班/伽马化学2026年暑期模拟7答案.pdf"),
    ("YJ-02-08", 8,
     f"{A}/2026年壹尖广州寒假班/无机专题卷2.pdf",
     f"{A}/2026年壹尖广州寒假班/无机专题卷2答案.pdf"),
    ("HYS-13-05", 5,
     f"{A}/第40届化英社化学奥林匹克（初赛）夏季/第40届化英社化学奥林匹克（初赛）夏季初赛模拟13.pdf",
     f"{A}/第40届化英社化学奥林匹克（初赛）夏季/第40届化英社化学奥林匹克(初赛)夏季初赛模拟13参考答案_1.pdf"),
    ("QBY-10-04", 4,
     f"{A}/2026清北营夏令营/清北营高二试卷（前13套）/2026年清北营暑假高二班-试卷10.pdf",
     f"{A}/2026清北营夏令营/清北营高二试卷（前13套）/2026年清北营暑假高二班-试卷10-参考答案.pdf"),
    ("CM-15-03", 3,
     f"{A}/2026年chemy夏令营/第40届chemy夏季班/第40届chemy初赛模拟15/第40届chemy初赛模拟15试题.pdf",
     f"{A}/2026年chemy夏令营/第40届chemy夏季班/第40届chemy初赛模拟15/第40届chemy初赛模拟15答案.pdf"),
    ("GM-03-07", 7,
     f"{A}/2026伽马暑假刷题班/伽马化学2026年暑期模拟3.pdf",
     f"{A}/2026伽马暑假刷题班/伽马化学2026年暑期模拟3答案.pdf"),
    ("YJ-01-03", 3,
     f"{A}/2026年壹尖广州寒假班/无机专题卷1.pdf",
     f"{A}/2026年壹尖广州寒假班/无机专题卷1答案.pdf"),
]


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


def main():
    cards = [l.strip() for l in open(".workbuddy/tmp/opt_pipe/pilot_cards.txt", encoding="utf-8") if l.strip()]
    byid = {os.path.basename(c)[2:].split("-", 3)[:3].__str__(): c for c in cards}
    # 卡 ID → 路径（按题号匹配）
    idx = {}
    for c in cards:
        m = re.match(r"题-([A-Za-z0-9]+-\d+-\d+)-", os.path.basename(c))
        if m:
            idx[m.group(1)] = c
    for tag, n, qpdf, apdf in CONF:
        card = idx.get(tag)
        print("=" * 100)
        print("[%s] 第%d题  %s" % (tag, n, os.path.basename(qpdf)[:50]))
        if not card:
            print("  !! 未找到卡"); continue
        qh, ah = card_text(card)
        with fitz.open(qpdf) as dq:
            qt = page_texts(qpdf)
            qsc = sorted([(cov(qh, p), i) for i, p in enumerate(qt)], reverse=True)
            qsel = [i for s, i in qsc[:2] if s > 0.05] or [qsc[0][1]]
            qimgs = [render(dq, i, 140) for i in qsel]
        with fitz.open(apdf) as da:
            at = page_texts(apdf)
            asc = sorted([(cov(ah, p), i) for i, p in enumerate(at)], reverse=True)
            asel = [i for s, i in asc[:2] if s > 0.05] or [asc[0][1]]
            aimgs = [render(da, i, 140) for i in asel]
        print("  题面页 %s cov=%.2f | 答案页 %s cov=%.2f"
              % ([i + 1 for i in qsel], qsc[0][0], [i + 1 for i in asel], asc[0][0]))
        # 左列题面、右列答案
        W = 980
        def col(imgs):
            ims = [im.resize((W, int(im.height * W / im.width))) for im in imgs]
            h = sum(i.height for i in ims) + 24 * len(ims)
            c = Image.new("RGB", (W, h), "white"); y = 0
            for k, im in enumerate(ims):
                c.paste(im, (0, y + 22)); y += im.height + 24
            return c
        L, R = col(qimgs), col(aimgs)
        H = max(L.height, R.height)
        m = Image.new("RGB", (L.width + R.width + 20, H + 30), "white")
        m.paste(L, (0, 30)); m.paste(R, (L.width + 20, 30))
        dr = ImageDraw.Draw(m)
        dr.text((6, 8), "[题面] %s" % tag, fill="red")
        dr.text((L.width + 26, 8), "[答案] %s" % tag, fill="blue")
        p = os.path.join(OUT, "%s_QA.png" % tag)
        m.save(p)
        print("  →", p, m.size)


if __name__ == "__main__":
    main()
