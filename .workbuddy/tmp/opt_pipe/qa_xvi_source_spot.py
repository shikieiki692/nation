# -*- coding: utf-8 -*-
"""卷XVI 收口 QA：回源抽查（题面关键串 / 已修点）——缓存优先，缺则用 fitz 现取）。"""
import glob
import json
import os
import re

VAULT = r"C:\Obsidion\妙妙屋"
CACHE = os.path.join(VAULT, ".workbuddy/tmp/opt_pipe/locate_out/_ocr_cache")
PDFROOT = os.path.join(VAULT, "06-外部资料导入/OCR/01-题目")


def cache_text(pat):
    """按关键字取缓存页文本（合并）。"""
    hits = glob.glob(os.path.join(CACHE, f"*{pat}*.json"))
    hits = [h for h in hits if "_t.png" not in h]
    out = []
    for h in sorted(hits):
        try:
            d = json.load(open(h, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, list):
            out.append((os.path.basename(h), "\n".join(str(x) for x in d)))
    return out


def find(pdfname):
    r = []
    for root, _dirs, files in os.walk(PDFROOT):
        for f in files:
            if f == pdfname:
                r.append(os.path.join(root, f))
    return r


def pdf_text(path):
    import pymupdf
    doc = pymupdf.open(path)
    t = "\n".join(p.get_text() for p in doc)
    doc.close()
    return t


def show(title, text, keys, width=90):
    print(f"\n== {title}")
    if not text:
        print("   <无文本>")
        return
    flat = re.sub(r"\s+", "", text)
    for k in keys:
        kk = re.sub(r"\s+", "", k)
        i = flat.find(kk)
        if i < 0:
            print(f"   ✗ 未找到: {k}")
        else:
            print(f"   ✓ {k} → …{flat[max(0,i-40):i+len(kk)+60]}…")


# ── 1. HZ-01-06（Q6 · 汇智 长沙化学刷初赛模拟1）──────────────────
print("#" * 30, "Q6 HZ-01-06 · 汇智 长沙化学刷初赛模拟1")
cs = cache_text("长沙化学刷初赛模拟1")
if not cs:
    p = find("长沙化学刷初赛模拟1.pdf")
    cs = [(os.path.basename(p[0]), pdf_text(p[0]))] if p else []
for name, t in cs:
    print(f"  [缓存/PDF] {name}  ({len(t)} 字)")
merged = "\n".join(t for _n, t in cs)
show("题面关键串", merged, [
    "KCu(CN)2中含铜阴离子的结构",
    "目前制备CuCN的最好方法是",
    "DMSO",
    "Cu6(CN)8",
])
show("答案关键串（6-1-2 / 6-3）", merged, [
    "更温和",
    "避免",
    "正八面体",
    "配位数为4的Cu(I)越少",
])

# ── 2. CM-17-05（Q11 · chemy 模拟17：硫单质）──────────────────
print("\n" + "#" * 30, "Q11 CM-17-05 · chemy 第40届模拟17")
cs = cache_text("第40届chemy初赛模拟17")
for name, t in cs:
    print(f"  [缓存] {name}  ({len(t)} 字)")
merged = "\n".join(t for _n, t in cs)
show("题面关键串", merged, [
    "206pm",
    "基序",
    "S12",
    "液态硫",
])
show("答案关键串", merged, [
    "331",
    "448",
    "3.90",
])

# ── 3. XeC-40-02（Q7 · XeChem 模拟（十）：2014 年修复）────────
print("\n" + "#" * 30, "Q7 XeC-40-02 · XeChem 模拟（十）")
cs = cache_text("XeChem初赛模拟试题（十）") or cache_text("XeChem初赛模拟（十）")
for name, t in cs:
    print(f"  [缓存] {name}  ({len(t)} 字)")
merged = "\n".join(t for _n, t in cs)
show("修复点：2014 年", merged, ["2014年", "硅簇", "M4Si4", "CsNa9Si17"])

# ── 4. CM-12-05（Q3 · chemy 模拟12：DNA/回文）─────────────────
print("\n" + "#" * 30, "Q3 CM-12-05 · chemy 第40届模拟12")
cs = cache_text("第40届chemy初赛模拟12")
for name, t in cs:
    print(f"  [缓存] {name}  ({len(t)} 字)")
merged = "\n".join(t for _n, t in cs)
show("题面/答案关键串", merged, ["DLX", "回文", "三方晶系", "Hoechst"])
