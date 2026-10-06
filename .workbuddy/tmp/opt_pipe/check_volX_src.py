# -*- coding: utf-8 -*-
"""核验卷X 实际选中的 16 题 -> 原 PDF 可达性。只读。"""
import os, re, json, difflib
from collections import defaultdict

ROOT = r"C:\Obsidion\妙妙屋"
OCR = os.path.join(ROOT, "06-外部资料导入", "OCR", "01-题目")

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
            idx[b].append(os.path.join(dp, f)); nidx[norm(b)].append(os.path.join(dp, f))
keys = list(nidx.keys())

FM = re.compile(r'^source_file:[ \t]*(.*?)[ \t]*$', re.M)
plan = json.load(open(os.path.join(ROOT, ".workbuddy/tmp/opt_pipe/vol_plan_X.json"), encoding="utf-8"))
cards = [c["path"] for _, lst in plan for c in lst]
print(f"卷X 选题数: {len(cards)}\n")
ok = 0
for cp in cards:
    full = os.path.join(ROOT, cp)
    head = open(full, encoding="utf-8-sig").read(3000)
    m = FM.search(head)
    sf = m.group(1).strip().strip('"') if m else ""
    base = os.path.splitext(os.path.basename(sf))[0]
    way, pdf = "✗不可达", ""
    if idx.get(base): way, pdf = "L0", idx[base][0]
    elif nidx.get(norm(base)):
        way, pdf = "L1", nidx[norm(base)][0]
    else:
        c = difflib.get_close_matches(norm(base), keys, n=1, cutoff=0.86)
        if c: way, pdf = "L2", nidx[c[0]][0]
    if way != "✗不可达": ok += 1
    print(f"[{way}] {os.path.basename(cp)[:26]:<28} -> {os.path.relpath(pdf, OCR) if pdf else sf}")
print(f"\n★ 卷X 可回源: {ok}/{len(cards)} = {ok/len(cards)*100:.0f}%")
