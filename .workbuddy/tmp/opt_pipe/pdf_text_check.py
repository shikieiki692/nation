# -*- coding: utf-8 -*-
"""pdf_text_check.py —— 卡 vs 原 PDF 文字层比对（题面 + 答案）。

对每张卡：
  ① 定位原 PDF（题面）→ 逐页与卡内「## 题目」汉字串做 8-gram 重叠 → 最佳页 + 覆盖率
  ② 按命名约定在某同目录找「…答案…」PDF → 同上对「## 参考答案」
  ③ 打印文字层有无、最佳页、覆盖率（∈[0,1]，≈1 表示该页文字与卡内一致）
用途：为人工核验快速指出「该翻哪一页」，并把「漏句/改字」这类缺陷以低覆盖率暴露出来。

用法: python -X utf8 pdf_text_check.py --cards volX_cards.txt
"""
import os
import re
import sys
import glob
import difflib
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import locate_source_pdf as L   # noqa: E402

ROOT = L.ROOT


def hanzi(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s or "")


def strip_math(x):
    x = x or ""
    x = re.sub(r"!\[\[?[^\]]*\]?\]", " ", x)
    x = re.sub(r"\$\$.*?\$\$", " ", x, flags=re.S)
    x = re.sub(r"\$[^$]*\$", " ", x)
    return hanzi(x)


def card_sections(txt):
    q = re.search(r"^##[ \t]*题目[ \t]*\n(.*?)(?=^##[ \t]*参考答案|^##[ \t]*答案|\Z)", txt, re.S | re.M)
    a = re.search(r"^##[ \t]*参考答案[ \t]*\n(.*)", txt, re.S | re.M)
    if not a:
        a = re.search(r"^##[ \t]*答案[ \t]*\n(.*)", txt, re.S | re.M)
    return strip_math(q.group(1) if q else ""), strip_math(a.group(1) if a else "")


def pages_of(pdf):
    with fitz.open(pdf) as d:
        return [d[i].get_text() for i in range(d.page_count)]


def coverage(pages, text, k=8):
    if not text or not pages:
        return [], 0.0
    gs = [text[i:i + k] for i in range(0, max(1, len(text) - k + 1), k)]
    denom = max(1, len(gs))
    ret = []
    for i, p in enumerate(pages):
        ph = hanzi(p)
        c = sum(1 for g in gs if g in ph) / denom
        ret.append((c, i + 1))
    ret.sort(reverse=True)
    return ret[:3], ret[0][0] if ret else 0.0


def find_answer_pdf(qpdf):
    d = os.path.dirname(qpdf)
    base = os.path.splitext(os.path.basename(qpdf))[0]
    key = L.norm(base)
    best, br = None, 0.0
    for f in os.listdir(d):
        if f.lower().endswith(".pdf") and "答案" in f:
            r = difflib.SequenceMatcher(None, L.norm(os.path.splitext(f)[0]), key).ratio()
            if r > br:
                br, best = r, f
    return (os.path.join(d, best) if best else None), br


def main():
    args = [a.strip() for a in sys.argv[1:] if not a.startswith("--")]
    if "--cards" in sys.argv:
        i = sys.argv.index("--cards")
        args = [l.strip() for l in open(os.path.join(ROOT, sys.argv[i + 1]), encoding="utf-8") if l.strip()]
    cards = []
    for a in args:
        p = a if os.path.isabs(a) else os.path.join(ROOT, a)
        if os.path.isdir(p):
            cards += sorted(glob.glob(os.path.join(p, "题-*.md")))
        elif p.endswith(".md"):
            cards.append(p)
    idx, nidx, keys = L.norm_pdf_index()
    print("%-42s | %-6s %-22s | %-6s %-22s" % ("卡", "题面", "题面命中页(cov)", "答案", "答案命中页(cov)"))
    print("-" * 120)
    for cp in cards:
        txt = open(cp, encoding="utf-8-sig").read()
        qh, ah = card_sections(txt)
        sf = L.get_source_file(cp)
        qpdf, way = L.locate_pdf(sf, idx, nidx, keys)
        name = os.path.basename(cp)[:40]
        if not qpdf:
            print("%-42s | 题面PDF未找到" % name); continue
        qp = pages_of(qpdf)
        qhit, qcov = coverage(qp, qh)
        qt = "有" if sum(len(hanzi(x)) for x in qp) > 80 else "扫描"
        apdf, ar = find_answer_pdf(qpdf)
        if apdf:
            ap = pages_of(apdf)
            ahit, acov = coverage(ap, ah)
            at = "有" if sum(len(hanzi(x)) for x in ap) > 80 else "扫描"
            astr = "p%s cov=%.2f [%s]" % ([p for _, p in ahit], acov, at)
        else:
            astr = "(无答案PDF)"
        qstr = "p%s cov=%.2f [%s]" % ([p for _, p in qhit], qcov, qt)
        print("%-42s | %-26s | %s" % (name, qstr, astr))


if __name__ == "__main__":
    main()
