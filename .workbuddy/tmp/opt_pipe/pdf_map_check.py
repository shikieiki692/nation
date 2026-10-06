# -*- coding: utf-8 -*-
"""核验：机构题的 source_file(OCR md) 能否映射到 06-外部资料导入/OCR/01-题目/ 下的原 PDF。
输出每个 md 名的命中情况 + 全库覆盖率。只读，不写盘。"""
import os, re, json
from collections import defaultdict

ROOT = r"C:\Obsidion\妙妙屋"
QBANK = os.path.join(ROOT, "04-题库", "2026机构初赛模拟题")
OCR = os.path.join(ROOT, "06-外部资料导入", "OCR", "01-题目")
SKIP = {"_待人工复核-空壳与重复卡"}

# 1) 建立 OCR 目录下所有 pdf 的 文件名(不含扩展名) -> 全路径 索引
pdf_idx = defaultdict(list)
for dirpath, _, files in os.walk(OCR):
    for f in files:
        if f.lower().endswith(".pdf"):
            pdf_idx[os.path.splitext(f)[0]].append(os.path.join(dirpath, f))

# 2) 遍历机构卡
FM_SF = re.compile(r'^source_file:[ \t]*(.*?)[ \t]*$', re.M)
rows = []
for org in sorted(os.listdir(QBANK)):
    p = os.path.join(QBANK, org)
    if not os.path.isdir(p) or org in SKIP:
        continue
    for fn in os.listdir(p):
        if not fn.endswith(".md"):
            continue
        with open(os.path.join(p, fn), encoding="utf-8-sig") as fh:
            head = fh.read(3000)
        m = FM_SF.search(head)
        sf = m.group(1).strip().strip('"').strip("'") if m else ""
        base = os.path.splitext(os.path.basename(sf))[0] if sf else ""
        rows.append((org, sf, base, len(pdf_idx.get(base, []))))

# 3) 汇总
tot = len(rows)
nobase = [r for r in rows if not r[2]]
hit = [r for r in rows if r[2] and r[3] > 0]
miss = [r for r in rows if r[2] and r[3] == 0]
multi = [r for r in rows if r[3] > 1]

print(f"机构卡总数(去空壳目录): {tot}")
print(f"  有 source_file: {tot - len(nobase)}   无: {len(nobase)}")
print(f"  能映射到原 PDF: {len(hit)}  ({len(hit)/tot*100:.1f}%)")
print(f"  映射不到 PDF: {len(miss)}")
print(f"  一 md 对多 PDF(需人工择一): {len(multi)}")

print("\n== 映射不到的 md 名（按机构聚合，去重）==")
byorg = defaultdict(set)
for org, sf, base, n in miss:
    byorg[org].add(base)
for org in sorted(byorg):
    print(f"\n[{org}] {len(byorg[org])} 个:")
    for b in sorted(byorg[org])[:12]:
        print("   -", b)

print("\n== 一 md 对多 PDF 的（前 10）==")
seen = set()
for org, sf, base, n in multi:
    if base in seen: continue
    seen.add(base)
    print(f"   {base}  -> {n} 个")
    for x in pdf_idx[base][:4]:
        print("        ", os.path.relpath(x, ROOT))
    if len(seen) >= 10: break

json.dump({"total": tot, "hit": len(hit), "miss": len(miss),
           "miss_list": sorted({r[2] for r in miss}),
           "nobase_list": sorted({r[1] for r in nobase})},
          open(os.path.join(os.path.dirname(__file__), "pdf_map_check.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n[saved] pdf_map_check.json")
