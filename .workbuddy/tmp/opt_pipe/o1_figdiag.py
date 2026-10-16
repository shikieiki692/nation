# -*- coding: utf-8 -*-
"""诊断：题1（HYS-40-07）源卡 26 图 vs 卷 O1 第1题 图，找出「缺」的图在卡的哪一段。"""
import io, os, re, hashlib

R = r"C:\Obsidion\妙妙屋"
CARD = os.path.join(R, r"04-题库/2026机构初赛模拟题/化英社/题-HYS-40-07-早在1979年研究人员就报道.md")
VOL = os.path.join(R, r"04-题库/初赛模拟卷O1（有机·答案版）.md")
IMGDIR = os.path.join(R, r"04-题库/2026机构初赛模拟题/化英社/images")

IMGMD = re.compile(r"!\[[^\]]*\]\((?:(?:\.\./)?images/)?([0-9a-f]{16,}\.jpg)\)")
IMGWIKI = re.compile(r"!\[\[([0-9a-f]{16,}\.jpg)")


def ck(rel):
    p = os.path.join(IMGDIR, os.path.basename(rel))
    if os.path.isfile(p):
        return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]
    return "??" + os.path.basename(rel)[:10]


card = io.open(CARD, encoding="utf-8-sig").read()
vol = io.open(VOL, encoding="utf-8-sig").read()
# 卷第 1 题段
m = re.split(r"(?m)^### 第 (\d+) 题", vol)
sec = ""
for i in range(1, len(m), 2):
    if m[i] == "1":
        sec = m[i + 1]
        break

c_imgs = IMGMD.findall(card)
v_imgs = IMGWIKI.findall(sec)
c_set = {ck(x) for x in c_imgs}
v_set = {ck(x) for x in v_imgs}
print("卡图 %d 张（unique %d）｜卷题1图 %d 张（unique %d）" % (len(c_imgs), len(c_set), len(v_imgs), len(v_set)))
missing = [x for x in dict.fromkeys(c_imgs) if ck(x) not in v_set]
print("缺 %d 张；逐张定位在卡的哪一段：" % len(missing))

# 卡内分段：题面区 / 答案区
ai = card.find("## 参考答案")
if ai < 0:
    ai = card.find("<details>")
head, tail = card[:ai], card[ai:]
for x in missing:
    b = os.path.basename(x)
    loc = []
    for ln, line in enumerate(card.split("\n"), 1):
        if b in line:
            loc.append(ln)
    where = "题面区" if all(l * 1 <= card[:ai].count("\n") + 1 for l in loc) else "答案区"
    # 精确些
    seg = "题面区" if (head.find(b) >= 0) else ("答案区" if tail.find(b) >= 0 else "?")
    print("   %s  %s  行%s" % (ck(x), b[:20], loc))
print()
print("卡内 '## 参考答案' 位置:", ai, " 存在:", ai > 0)
print("卡内 <details> 数:", card.count("<details>"))
