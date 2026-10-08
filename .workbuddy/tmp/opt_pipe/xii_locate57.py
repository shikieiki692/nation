# -*- coding: utf-8 -*-
"""按关键词在源 PDF 文字层定位页码（卷 XII 第 5、7 题回源核验用）。"""
import sys

sys.stdout.reconfigure(encoding="utf-8")
import pymupdf as fitz  # noqa: E402

O = r"C:\Obsidion\妙妙屋\06-外部资料导入\OCR"
JOBS = [
    (O + r"\01-题目\2026年XEchem寒假班\Xechem模拟四.pdf",
     ["掺杂的氧原子", "核反应堆中的氧化物", "3-1", "3-2", "3-3", "3-4"]),
    (O + r"\chemy\第35届中国化学奥林匹克Chemy题目合集..pdf",
     ["液态钠上方", "钠蒸气的平衡分压", "4-1", "4-2", "4-3", "4-4"]),
]
for pdf, keys in JOBS:
    d = fitz.open(pdf)
    print("=" * 92)
    print("%s（%d 页）" % (pdf.split("\\")[-1], d.page_count))
    for i in range(d.page_count):
        t = d[i].get_text()
        hit = [k for k in keys if k in t]
        if hit:
            print("   P%-4d 命中 %s" % (i + 1, hit))
