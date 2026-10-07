#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_gcho_crop.py —— 校验 GChO 裁图治理结果。
断言：① 备份存在且 FM/题面区逐字节不变；② 答案区＝手稿注记＋图；③ 图全部存在；
     ④ 答案区无残留乱码特征；⑤ 全库无断图。
"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
GDIR = os.path.join(R, "04-题库/2026机构初赛模拟题/质心GChO")
BK = os.path.join(R, ".workbuddy/tmp/opt_pipe/gcho_ans_backup")

GARB = re.compile(r"\\xlongequal|\\xrightarrow\s*\{\s*\d+\s*\}|(?<![\d.])\d{1,2}(?:\.\d)?\s*['′’]|\bawsl\b|∴|_\{n\}")
NOTE = re.compile(r"手写解析手稿")

n = 0; ok = 0; probs = []
for f in sorted(glob.glob(os.path.join(BK, "*.orig"))):
    name = os.path.basename(f)[:-5]
    card = os.path.join(GDIR, name)
    if not os.path.exists(card):
        probs.append((name, "卡丢失")); continue
    n += 1
    orig = open(f, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    new = open(card, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    # ① FM + 题面区不变
    i0 = orig.find("## 题目"); j0 = orig.find("## 参考答案")
    i1 = new.find("## 题目"); j1 = new.find("## 参考答案")
    if orig[:i0] != new[:i1]:
        probs.append((name, "FM/题面之前段变化"))
    if orig[i0:j0] != new[i1:j1]:
        probs.append((name, "题面区变化"))
    # ② 答案区
    k1 = new.find("## 知识点映射")
    a = new[j1:k1 if k1 > j1 else len(new)]
    if not NOTE.search(a):
        probs.append((name, "答案区无手稿注记"))
    ims = re.findall(r"!\[\]\(images/([^)]+)\)", a)
    if not ims:
        probs.append((name, "答案区无图"))
    for im in ims:
        if not os.path.exists(os.path.join(GDIR, "images", im)):
            probs.append((name, "缺图 " + im))
    # ④ 乱码残留
    if GARB.search(a):
        probs.append((name, "乱码残留: " + GARB.search(a).group(0)[:20]))
    if not probs or probs[-1][0] != name:
        ok += 1

print("校验卡 %d；通过 %d；问题 %d" % (n, ok, len(probs)))
for name, msg in probs[:40]:
    print("   ✗ %-42s %s" % (name[:42], msg))

# ⑤ 全 GChO 断图检查
disp = []
for p in glob.glob(os.path.join(GDIR, "**", "*.md"), recursive=True):
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    for im in re.findall(r"!\[\]\(images/([^)]+)\)", t):
        if not os.path.exists(os.path.join(GDIR, "images", im)):
            disp.append((os.path.basename(p), im))
print("\nGChO 断图：%d" % len(disp))
for a, b in disp[:10]:
    print("   ✗ %s → %s" % (a[:40], b))
