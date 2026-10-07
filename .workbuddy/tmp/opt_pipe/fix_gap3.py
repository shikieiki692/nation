#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_gap3.py —— 对 3 张「题界无法定位」的 GChO 手写届卡：随卡其所在 gap 区
（上一题起点 → 下一题起点），并在注记中说明含相邻题内容。"""
import importlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
GC = importlib.import_module("gcho_crop")

TARGETS = [(6, 4), (6, 8), (7, 6), (23, 2), (25, 1), (34, 1), (34, 6)]

for rnd, qn in TARGETS:
    pdf = GC.find_manuscript(rnd)
    idx = GC.load_index(rnd, pdf)
    mks = GC.markers(idx, 150)
    aug = list(mks)
    qset = {t[0] for t in aug}
    if 1 not in qset:
        aug.append((1, 1, 0.0, 0.0, idx[0]["w"])); qset.add(1)
    for q, t in GC.sub_markers(idx).items():
        if q not in qset:
            aug.append(t); qset.add(q)
    aug.sort(key=lambda t: (t[1], GC._col(t[3], t[4]), t[2]))
    byq = {t[0]: i for i, t in enumerate(aug)}
    prev = qn - 1 if qn > 1 else 1          # 第1题：上界＝文档起始
    if prev not in byq or qn + 1 not in byq:
        print("届%d 第%d题：缺邻居（%s/%s），跳过" % (rnd, qn, prev in byq, qn + 1 in byq)); continue
    i0, i1 = byq[prev], byq[qn + 1]
    qq, slices = GC.crop_q(pdf, [aug[i0], aug[i1]], 0)
    if not slices:
        print("届%d 第%d题：gap 区为空，跳过" % (rnd, qn)); continue
    names = [GC.save_img(im) for _, im in slices]
    card = None
    for c in GC.cards_of(rnd):
        if GC.card_qno(c) == qn:
            card = c; break
    if not card:
        print("届%d 第%d题：未找到卡" % (rnd, qn)); continue
    t = open(card, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    if k < 0:
        k = len(t)
    bkf = os.path.join(GC.BK, os.path.basename(card) + ".orig")
    if not os.path.exists(bkf):
        open(bkf, "w", encoding="utf-8", newline="\n").write(t)
    newans = ["## 参考答案", "",
              "📎 **答案出处**：源卷**手写解析手稿**第 %d 题一带（p%s）已随卡；手写笔迹，"
              "**题界未能自动定位**，随卡图区含相邻题内容，文字化需人工转录。"
              % (qn, "、".join(str(p) for p, _ in slices)), ""]
    for n in names:
        newans += ["![](images/%s)" % n, ""]
    open(card, "w", encoding="utf-8", newline="\n").write(t[:j] + "\n".join(newans) + "\n" + t[k:])
    print("届%d 第%d题 → %d 片 %s" % (rnd, qn, len(names), [p for p, _ in slices]))
