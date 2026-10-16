# -*- coding: utf-8 -*-
"""Q2 差异诊断：卷答案版第2题段的 32 张图 vs 源卡 11 张，找出 21 张「多出来」的在哪。"""
import io, os, re

R = r"C:\Obsidion\妙妙屋"
CARD = os.path.join(R, r"04-题库/2026机构初赛模拟题/清北营/题-QBY-13-05-51德国马克斯普朗克煤炭研究.md")
VOL = os.path.join(R, r"04-题库/初赛模拟卷O1（有机·答案版）.md")

IMG = re.compile(r"!\[\[([^\]]+)\]\]")
IMGMD = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def clean(n):
    return re.split(r"\\?\|", n, maxsplit=1)[0].strip()


def base(n):
    return os.path.basename(clean(n))


card = io.open(CARD, encoding="utf-8-sig").read()
vol = io.open(VOL, encoding="utf-8-sig").read()
parts = re.split(r"(?m)^### 第 (\d+) 题", vol)
sec = ""
for i in range(1, len(parts), 2):
    if parts[i] == "2":
        sec = parts[i + 1]
        break

c = [base(x) for x in IMG.findall(card) + IMGMD.findall(card)]
v = [base(x) for x in IMG.findall(sec) + IMGMD.findall(sec)]
print("源卡 %d 张:" % len(c))
for x in c:
    print("   ", x[:24])
print("卷答案段 %d 张:" % len(v))
for x in v:
    print("   ", x[:24], "" if x in c else "  ← 卡中无")
