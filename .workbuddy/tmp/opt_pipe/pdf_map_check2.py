# -*- coding: utf-8 -*-
"""二级核验：source_file(OCR md) -> 原 PDF 的可达率。
L0 同名直中；L1 归一化(去括号/空格/标点/常见后缀)后同名；L2 difflib 模糊(>=0.86)。
只读，不写盘。"""
import os, re, json, difflib
from collections import defaultdict

ROOT = r"C:\Obsidion\妙妙屋"
QBANK = os.path.join(ROOT, "04-题库", "2026机构初赛模拟题")
OCR = os.path.join(ROOT, "06-外部资料导入", "OCR", "01-题目")
SKIP = {"_待人工复核-空壳与重复卡"}

def norm(s):
    s = s.lower()
    s = s.replace("（", "(").replace("）", ")").replace("，", ",").replace("：", ":")
    # 去常见噪声后缀
    s = re.sub(r"[_\- ]?\d+$", "", s)          # 尾 _1 / -1
    s = re.sub(r"已优化|参考答案|答案版|答案|解析|试题|试卷|题目|合集|讲稿|讲义|文字版|v\d+(\.\d+)*", "", s)
    s = re.sub(r"[\s_\-\.·、,，:：()（）\[\]【】<>《》/\\'\"+]", "", s)
    return s

pdf_idx, pdf_norm = defaultdict(list), defaultdict(list)
for dp, _, files in os.walk(OCR):
    for f in files:
        if not f.lower().endswith(".pdf"): continue
        b = os.path.splitext(f)[0]
        pdf_idx[b].append(os.path.join(dp, f))
        pdf_norm[norm(b)].append((b, os.path.join(dp, f)))
all_norm_keys = list(pdf_norm.keys())

FM_SF = re.compile(r'^source_file:[ \t]*(.*?)[ \t]*$', re.M)
stat = defaultdict(int)
unreach, ways = [], defaultdict(int)
for org in sorted(os.listdir(QBANK)):
    p = os.path.join(QBANK, org)
    if not os.path.isdir(p) or org in SKIP: continue
    for fn in os.listdir(p):
        if not fn.endswith(".md"): continue
        with open(os.path.join(p, fn), encoding="utf-8-sig") as fh:
            head = fh.read(3000)
        m = FM_SF.search(head)
        sf = m.group(1).strip().strip('"').strip("'") if m else ""
        base = os.path.splitext(os.path.basename(sf))[0] if sf else ""
        if not base:
            stat["无source_file"] += 1; continue
        if pdf_idx.get(base):
            stat["L0同名直中"] += 1; ways["L0"] += 1; continue
        nb = norm(base)
        if pdf_norm.get(nb):
            stat["L1归一化命中"] += 1; ways["L1"] += 1; continue
        cand = difflib.get_close_matches(nb, all_norm_keys, n=1, cutoff=0.86)
        if cand:
            stat["L2模糊命中"] += 1; ways["L2"] += 1; continue
        stat["仍不可达"] += 1
        unreach.append((org, base))

tot = sum(v for k, v in stat.items())
print(f"机构卡总数: {tot}")
for k in ["L0同名直中", "L1归一化命中", "L2模糊命中", "仍不可达", "无source_file"]:
    v = stat.get(k, 0)
    print(f"  {k:<12}: {v:>5}  ({v/tot*100:5.1f}%)")
reach = stat["L0同名直中"] + stat["L1归一化命中"] + stat["L2模糊命中"]
print(f"\n★ 可定位到原 PDF 合计: {reach}/{tot} = {reach/tot*100:.1f}%")

print(f"\n== 仍不可达 {len(unreach)} 张，去重 md 名（按机构）==")
byorg = defaultdict(set)
for org, b in unreach: byorg[org].add(b)
for org in sorted(byorg):
    print(f"\n[{org}] {len(byorg[org])} 个:")
    for b in sorted(byorg[org])[:10]: print("   -", b)

json.dump({"total": tot, "stats": dict(stat),
           "unreach": sorted({b for _, b in unreach})},
          open(os.path.join(os.path.dirname(__file__), "pdf_map_check2.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n[saved] pdf_map_check2.json")
