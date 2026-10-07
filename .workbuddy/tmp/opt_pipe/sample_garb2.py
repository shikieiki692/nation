#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sample_garb2.py —— 独立复算「答案可用闸」命中并抽样（验真伪）。"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
BASE = os.path.join(R, "04-题库/2026机构初赛模拟题")
SCOREMARK = re.compile(r"(?<![\d.])\d{1,2}(?:\.\d)?\s*['\u2032\u2019]")


def contain_ratio(inner, outer):
    if len(inner) < 8:
        return 1.0 if inner and inner in outer else 0.0
    gs = [inner[i:i + 8] for i in range(0, len(inner) - 7, 4)]
    return sum(1 for g in gs if g in outer) / len(gs) if gs else 0.0


garb, echo = [], []
for p in sorted(glob.glob(os.path.join(BASE, "**", "题-*.md"), recursive=True)):
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    a = t[j:k] if j > 0 and k > j else ""
    i = t.find("## 题目")
    q = t[i:j] if i >= 0 and j > i else ""
    if "![[" in a or "![" in a:
        continue
    an = re.sub(r"\s+", "", a); qn = re.sub(r"\s+", "", q)
    if len(an) >= 25 and contain_ratio(an, qn) >= 0.75:
        echo.append((os.path.basename(p), round(contain_ratio(an, qn), 2), len(an)))
    elif len(SCOREMARK.findall(a)) >= 3:
        garb.append((os.path.basename(p), len(SCOREMARK.findall(a)), SCOREMARK.findall(a)[:4]))

print("手写乱码型 %d 卡（前 20）：" % len(garb))
for n, c, ex in garb[:20]:
    print("   %-44s 评分符%-3d %s" % (n[:44], c, ex))
print("\n仅题干回显型 %d 卡（前 20）：" % len(echo))
for n, r, l in echo[:20]:
    print("   %-44s echo=%-4s len=%d" % (n[:44], r, l))
