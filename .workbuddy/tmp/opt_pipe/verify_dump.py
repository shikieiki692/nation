# -*- coding: utf-8 -*-
"""verify_dump.py —— 卷X 回源三元核验辅助：为每张卡渲染「题面页 + 答案页」。

用法: python -X utf8 verify_dump.py <卡路径...>
      python -X utf8 verify_dump.py --cards volX_cards.txt

输出: .workbuddy/tmp/opt_pipe/locate_out/<tag>/{q,a}_pNN.png
      <tag> = 卡文件名去掉「题-」前缀后的前 22 字符（与 locate_source_pdf 一致）
      另打印每题命中页，便于直接打开。
"""
import os
import re
import sys
import glob
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import locate_source_pdf as L   # noqa: E402

ROOT = L.ROOT
OUT = os.path.join(HERE, "locate_out")
DPI = 130


def hanzi(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s)


def section(txt, *names):
    for nm in names:
        m = re.search(r"^##[ \t]*" + nm + r"[ \t]*\n(.*?)(?=^##[ \t]*\S|\Z)", txt, re.S | re.M)
        if m:
            return m.group(1)
    return txt


def q_hanzi(txt):
    body = section(txt, "题目")
    body = re.sub(r"!\[\[?[^\]]*\]?\]", " ", body)
    body = re.sub(r"\$\$.*?\$\$", " ", body, flags=re.S)
    body = re.sub(r"\$[^$]*\$", " ", body)
    return hanzi(body)


def a_hanzi(txt):
    body = section(txt, "参考答案", "答案")
    body = re.sub(r"!\[\[?[^\]]*\]?\]", " ", body)
    body = re.sub(r"\$\$.*?\$\$", " ", body, flags=re.S)
    body = re.sub(r"\$[^$]*\$", " ", body)
    return hanzi(body)


def grams(s, k=8):
    return [s[i:i + k] for i in range(0, max(1, len(s) - k + 1), k)]


def rank(pages_h, text, topn=2):
    gs = grams(text)
    sc = [(sum(1 for g in gs if g in ph), i) for i, ph in enumerate(pages_h)]
    sc.sort(reverse=True)
    return [i for s, i in sc[:topn] if s > 0], sc[:5]


def render(d, pno, tag, kind):
    os.makedirs(os.path.join(OUT, tag), exist_ok=True)
    pix = d[pno - 1].get_pixmap(dpi=DPI)
    fp = os.path.join(OUT, tag, "%s_p%02d.png" % (kind, pno))
    pix.save(fp)
    return fp


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
    for cp in cards:
        txt = open(cp, encoding="utf-8-sig").read()
        sf = L.get_source_file(cp)
        pdf, way = L.locate_pdf(sf, idx, nidx, keys)
        tag = os.path.basename(cp)[2:24]
        print("=" * 100)
        print("[%s] %s" % (way, os.path.basename(cp)))
        print("    PDF:", os.path.relpath(pdf, ROOT) if pdf else "(无)")
        if not pdf:
            continue
        with fitz.open(pdf) as d:
            n = d.page_count
            ph = [hanzi(d[i].get_text()) for i in range(n)]
        full = "".join(ph)
        has_text = len(full.strip()) > 80
        print("    页数=%d 文字层=%s" % (n, "有" if has_text else "无(扫描件)"))
        if has_text:
            qpg, qsc = rank(ph, q_hanzi(txt))
            apg, asc = rank(ph, a_hanzi(txt))
            print("    题面命中页:", [p + 1 for p in qpg], "| 答案命中页:", [p + 1 for p in apg])
            with fitz.open(pdf) as d:
                for p in qpg:
                    print("      q", render(d, p + 1, tag, "q"))
                for p in apg:
                    print("      a", render(d, p + 1, tag, "a"))
        else:
            # 扫描件：渲染全部页缩略（每 6 页一张拼版由调用方人工翻）
            with fitz.open(pdf) as d:
                for p in range(n):
                    pix = d[p].get_pixmap(dpi=60)
                    fp = os.path.join(OUT, tag, "thumb_p%02d.png" % (p + 1))
                    os.makedirs(os.path.dirname(fp), exist_ok=True)
                    pix.save(fp)
            print("      扫描件：已出 %d 张缩略图 → locate_out/%s/thumb_pNN.png" % (n, tag))


if __name__ == "__main__":
    main()
