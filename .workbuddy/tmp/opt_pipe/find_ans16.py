#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""find_ans16.py —— 为 16 张「整本答案册」卡勘定答案 PDF（同目录找 答案/参考/解析）。"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
try:
    import fitz
    try:
        fitz.TOOLS.mupdf_display_errors(False)
    except Exception:
        pass
except Exception:
    fitz = None
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库", "2026机构初赛模拟题")

cards = []
for p in sorted(glob.glob(os.path.join(BASE, "**", "题-*.md"), recursive=True)):
    if "质心GChO" in p:
        continue
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    a = t[j:k] if j > 0 and k > j else ""
    if re.search(r"全部\s*\d+\s*页已随卡", a):
        cards.append(p)
print("整本册卡 %d 张" % len(cards))

seen = {}
for p in cards:
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    m = re.search(r"^source_file:[ \t]*(.*?)[ \t]*$", t, re.M)
    sf = m.group(1).strip().strip('"') if m else ""
    base = os.path.basename(sf)[:-3] if sf.endswith(".md") else os.path.basename(sf)
    d = os.path.join(R, "06-外部资料导入/OCR")
    hits = []
    for f in glob.glob(os.path.join(d, "**", base + "*.pdf"), recursive=True):
        hits.append(f)
    ans = [f for f in hits if re.search(r"答案|参考|解析|评分", os.path.basename(f))]
    tgt = ans[0] if ans else (hits[0] if hits else None)
    key = tgt
    tag = ""
    if tgt and tgt not in seen:
        dd = fitz.open(tgt)
        tl = sum(len(dd[i].get_text().strip()) for i in range(dd.page_count))
        seen[tgt] = (dd.page_count, tl)
        dd.close()
    print("  %-44s → %s %s" % (os.path.basename(p)[:44],
                               (os.path.basename(tgt)[:44] if tgt else "(未找到)"),
                               seen.get(tgt, "")))
print("\n去重后答案册 %d 份" % len(seen))
for f, (pg, tl) in seen.items():
    print("   %-52s 页%-3d 文字层%-6d %s" % (os.path.basename(f)[:52], pg, tl, "有" if tl > 200 else "扫描"))
