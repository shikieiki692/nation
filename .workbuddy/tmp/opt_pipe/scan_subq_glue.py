# -*- coding: utf-8 -*-
"""scan_subq_glue.py —— 扫描卷 XIV 源卡「题面区」同一行出现 ≥2 个小问号（粘连）的缺陷。"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = r"C:\Obsidion\妙妙屋"
SUBQ = re.compile(r"(?<![\d\-])(\d{1,2}(?:-\d{1,2}){1,3})(?=\s|[^\d])")


def main():
    cards = [l.strip() for l in open(os.path.join(HERE, 'xiv_cards.txt'), encoding='utf-8') if l.strip()]
    for i, rel in enumerate(cards, 1):
        p = os.path.join(ROOT, rel.replace('/', os.sep))
        t = open(p, encoding='utf-8-sig').read()
        m = re.search(r"##\s*题目\s*\n([\s\S]*?)(?=\n##\s)", t)
        q = m.group(1) if m else ""
        print("\n=== 第%d题 %s ===" % (i, os.path.basename(rel)))
        for ln_no, ln in enumerate(q.split("\n"), 1):
            ms = list(SUBQ.finditer(ln))
            if len(ms) >= 2:
                print("  ⚠ 行内 %d 个小问号: %s" % (len(ms), [x.group(1) for x in ms]))
                print("     ", ln[:150])


if __name__ == "__main__":
    main()
