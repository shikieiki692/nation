# -*- coding: utf-8 -*-
"""输出 机构 -> OCR 源目录 的映射（按命中数排序），并统计不可达卡的集中度。只读。"""
import os, re, json
from collections import defaultdict

ROOT = r"C:\Obsidion\妙妙屋"
QBANK = os.path.join(ROOT, "04-题库", "2026机构初赛模拟题")
OCR = os.path.join(ROOT, "06-外部资料导入", "OCR", "01-题目")
SKIP = {"_待人工复核-空壳与重复卡"}

def norm(s):
    s = s.lower().replace("（", "(").replace("）", ")")
    s = re.sub(r"[_\- ]?\d+$", "", s)
    s = re.sub(r"已优化|参考答案|答案版|答案|解析|试题|试卷|题目|合集|讲稿|讲义|文字版|v\d+(\.\d+)*", "", s)
    return re.sub(r"[\s_\-\.·、,，:：()（）\[\]【】<>《》/\\'\"+]", "", s)

idx, nidx = defaultdict(list), defaultdict(list)
for dp, _, fs in os.walk(OCR):
    for f in fs:
        if f.lower().endswith(".pdf"):
            b = os.path.splitext(f)[0]
            idx[b].append(dp); nidx[norm(b)].append(dp)

FM = re.compile(r'^source_file:[ \t]*(.*?)[ \t]*$', re.M)
org2dir = defaultdict(lambda: defaultdict(int))
unreach_cnt = defaultdict(int)
for org in sorted(os.listdir(QBANK)):
    p = os.path.join(QBANK, org)
    if not os.path.isdir(p) or org in SKIP: continue
    for fn in os.listdir(p):
        if not fn.endswith(".md"): continue
        head = open(os.path.join(p, fn), encoding="utf-8-sig").read(3000)
        m = FM.search(head)
        sf = m.group(1).strip().strip('"').strip("'") if m else ""
        base = os.path.splitext(os.path.basename(sf))[0] if sf else ""
        d = None
        if idx.get(base): d = idx[base][0]
        elif nidx.get(norm(base)): d = nidx[norm(base)][0]
        if d: org2dir[org][os.path.relpath(d, OCR)] += 1
        else: unreach_cnt[os.path.basename(sf) or "(空)"] += 1

print("== 机构 -> OCR 源目录（命中数 top3）==")
for org in sorted(org2dir):
    ds = sorted(org2dir[org].items(), key=lambda x: -x[1])[:3]
    print(f"\n[{org}]  合计 {sum(org2dir[org].values())}")
    for d, n in ds: print(f"    {n:>4}  {d}")

print(f"\n== 不可达卡按 source_file 聚合（共 {sum(unreach_cnt.values())} 张）==")
for k, v in sorted(unreach_cnt.items(), key=lambda x: -x[1])[:15]:
    print(f"    {v:>4}  {k}")
