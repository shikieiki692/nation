# -*- coding: utf-8 -*-
"""find_page.py —— 用「题面特征串」在 PDF 文字层全文检索，精确定位题目页。

用法: python -X utf8 find_page.py <卡路径> <pdf路径>
原理：从卡 `## 题目` 抽 长度≥12 的连续汉字串，在每页文字层里找命中，
      按「命中串数 / 串总长度」打分，输出前 3 页。
"""
import os
import re
import sys

import fitz

HZ = re.compile(r"[\u4e00-\u9fff]{12,}")


def main():
    card, pdf = sys.argv[1], sys.argv[2]
    t = open(card, encoding="utf-8-sig").read()
    q = re.search(r"##\s*题目\s*\n([\s\S]*?)(?=\n##\s)", t)
    qt = q.group(1) if q else t
    a = re.search(r"##\s*参考答案\s*\n([\s\S]*?)(?=\n##\s)", t)
    at = a.group(1) if a else ""
    d = fitz.open(pdf)
    pages = [d[i].get_text("text") for i in range(d.page_count)]

    def score(text):
        seqs = HZ.findall(text)
        if not seqs:
            return 0.0, 0, len(seqs)
        hit = [s for s in seqs if any(s in p for p in pages)]
        return (sum(len(s) for s in hit) / max(sum(len(s) for s in seqs), 1),
                len(hit), len(seqs))

    for tag, txt in (("题面", qt), ("答案", at)):
        seqs = HZ.findall(txt)
        if not seqs:
            print("%s: 无长汉字串" % tag)
            continue
        per = []
        for i, p in enumerate(pages):
            c = sum(1 for s in seqs if s in p)
            if c:
                per.append((c, i + 1))
        per.sort(key=lambda x: -x[0])
        cov, nh, ns = score(txt)
        print("%s：长串 %d 条；覆盖 %.2f；命中页(按命中串数) %s" % (tag, ns, cov, per[:4]))
    print("PDF 页数:", d.page_count)
    d.close()


if __name__ == "__main__":
    main()
