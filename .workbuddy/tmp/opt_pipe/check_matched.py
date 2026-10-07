#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_matched.py —— 核验内容匹配到的 PDF 是否含答案（查关键词 + 定位题后内容）。"""
import json, os, re, sys, glob, collections
sys.stdout.reconfigure(encoding="utf-8")
import fitz
try:
    fitz.TOOLS.mupdf_display_errors(False)
except Exception:
    pass
R = r"C:\Obsidion\妙妙屋"
OCR = os.path.join(R, "06-外部资料导入/OCR")
hits = json.load(open(os.path.join(R, ".workbuddy/tmp/opt_pipe/content_hits.json"), encoding="utf-8"))
KW = ("答案", "解析", "参考解答", "评分标准", "评分细则", "解：", "【答案", "参考答案")
# 汇总用到的文件
files = collections.defaultdict(list)
for path, qno, f, cov in hits:
    for fp in glob.glob(OCR + "/**/" + f, recursive=True):
        files[fp].append((path, qno, cov))
        break
print("涉及文件 %d 个：\n" % len(files))
for fp, items in sorted(files.items(), key=lambda x: -len(x[1])):
    d = fitz.open(fp)
    full = "\n".join(d[i].get_text() for i in range(d.page_count))
    tl = len(full.strip())
    nkw = {k: full.count(k) for k in KW if k in full}
    print("### %s" % os.path.basename(fp)[:60])
    print("    页%d 字层%d 匹配 %d 张 | 关键词 %s" % (d.page_count, tl, len(items), nkw or "无"))
    d.close()
