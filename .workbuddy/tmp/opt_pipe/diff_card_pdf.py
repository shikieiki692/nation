# -*- coding: utf-8 -*-
"""diff_card_pdf.py —— 卡 vs PDF 页（双向）自动比对：找「卡有PDF无」与「PDF有卡无」的中文长串。

用法: python -X utf8 diff_card_pdf.py <卡路径> <pdf路径> <题面页,页...> [答案页,页...]
输出：题面/答案两侧各自的双向缺失清单（长度≥8 的汉字串）。
"""
import re
import sys

import fitz

HZ = re.compile(r"[\u4e00-\u9fff]{8,}")


def seqs(t):
    out = []
    for s in HZ.findall(t):
        out.append(s)
    return out


def norm(s):
    return re.sub(r"\s+", "", s)


def main():
    card, pdf = sys.argv[1], sys.argv[2]
    qp = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 and sys.argv[3] else []
    ap = [int(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 and sys.argv[4] else []
    t = open(card, encoding="utf-8-sig").read()
    m = re.search(r"##\s*题目\s*\n([\s\S]*?)(?=\n##\s)", t)
    cq = m.group(1) if m else ""
    m = re.search(r"##\s*参考答案\s*\n([\s\S]*?)(?=\n##\s)", t)
    ca = m.group(1) if m else ""
    d = fitz.open(pdf)
    for tag, pages, text in (("题面", qp, cq), ("答案", ap, ca)):
        if not pages:
            continue
        ptxt = norm("\n".join(d[p - 1].get_text("text") for p in pages))
        ctxt = norm(text)
        cs = seqs(ctxt)
        miss_card = [s for s in cs if s not in ptxt]
        ps = seqs(ptxt)
        miss_pdf = [s for s in ps if s not in ctxt]
        print(f"\n===== {tag}（PDF 页 {pages}）=====")
        print(f"卡侧汉字串 {len(cs)} 条，其中【卡有 PDF 无】{len(miss_card)} 条：")
        for s in miss_card[:14]:
            print("   ✗", s)
        print(f"PDF 侧汉字串 {len(ps)} 条，其中【PDF 有 卡无】{len(miss_pdf)} 条：")
        for s in miss_pdf[:14]:
            print("   +", s)
    d.close()


if __name__ == "__main__":
    main()
