# -*- coding: utf-8 -*-
"""从 docx 的 document.xml 抽取含关键字的段落文本（oMath + w:t 混合），用于核实渲染符号。"""
import sys, zipfile, re
sys.stdout.reconfigure(encoding="utf-8")
docx = sys.argv[1]
keys = sys.argv[2:]
z = zipfile.ZipFile(docx)
doc = z.read("word/document.xml").decode("utf-8")
TK = re.compile(r"<m:t[^>]*>(.*?)</m:t>|<w:t[^>]*>(.*?)</w:t>", re.S)
for m in re.finditer(r"<w:p[ >].*?</w:p>", doc, re.S):
    seg = m.group(0)
    flat = "".join(a if a else (b or "") for a, b in TK.findall(seg))
    if any(k in flat for k in keys):
        print(repr(flat[:300]))
