# -*- coding: utf-8 -*-
r"""o2_screen.py —— O2 十卡「题面/答案 ↔ 源件」覆盖率权威核验（修正 section 判据后）。

修正点（J28）：`section()` 结束前瞻必须「恰好两个 #」——原 `^##[ \t]*\S` 会匹配 `### 第 N 题`
⇒「## 题目」段截断为空 ⇒ 题面 8-gram 恒 0（假 0.00）。
"""
import os
import re
import sys

import fitz

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:/Obsidion/妙妙屋/.workbuddy/tmp/opt_pipe")
import o2_render as R  # noqa: E402  复用其 JOBS 与修正后的 section()

ROOT = r"C:/Obsidion/妙妙屋"


def hz(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s)


def best(ph, text):
    g = R.grams(hz(R.clean(text)))
    if not g:
        return 0.0, []
    sc = sorted(((sum(1 for x in g if x in p) / len(g), i) for i, p in enumerate(ph)), reverse=True)
    return sc[0][0], [i + 1 for s, i in sc[:3]]


print("%-42s | %-22s | %-22s" % ("卡", "题面(覆盖/命中页)", "答案(覆盖/命中页)"))
print("-" * 96)
worst = []
for card, qpdf, apdf in R.JOBS:
    name = os.path.basename(card).replace(".md", "")[:40]
    txt = open(os.path.join(ROOT, card), encoding="utf-8-sig").read()
    row = []
    for kind, pdf, secs in (("q", qpdf, ("题目",)), ("a", apdf, ("参考答案", "答案"))):
        with fitz.open(os.path.join(ROOT, pdf)) as d:
            ph = [hz(d[i].get_text()) for i in range(d.page_count)]
            if len("".join(ph).strip()) < 80:
                row.append("扫描件(无文字层)")
                continue
            cov, pgs = best(ph, R.section(txt, *secs))
            row.append("cov=%.2f %s" % (cov, pgs))
            if cov < 0.5:
                worst.append((name, kind, cov, pgs))
    print("%-42s | %-22s | %-22s" % (name, row[0], row[1]))

print("\n=== 低覆盖（<0.50）待人工目检 ===")
if not worst:
    print("  无")
for n, k, c, p in worst:
    print("  %-40s %s cov=%.2f 命中页=%s" % (n, k, c, p))
