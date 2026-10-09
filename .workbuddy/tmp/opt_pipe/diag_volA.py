# -*- coding: utf-8 -*-
"""定位 A/F 类命中：打印 卡题面图上下文 + 学生版对应题段落。"""
import io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(ROOT, "04-题库")
PLAN = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe")
TITLE = re.compile(r"^### 第 (\d+) 题（", re.M)
IMG_EMBED = re.compile(r"!\[\[([^\]\|\\]+)")
IMG_MD = re.compile(r"!\[\]\(images/([^)\s]+)\)")

v = sys.argv[1]
nos = [int(x) for x in sys.argv[2].split(",")]
plan = json.load(open(os.path.join(PLAN, "vol_plan_%s.json" % v), encoding="utf-8"))
cards = [c["path"] for _m, lst in plan for c in lst]
stu = io.open(os.path.join(QB, "初赛模拟卷%s（非有机·学生版）.md" % v), encoding="utf-8-sig").read()
idx = [m.start() for m in TITLE.finditer(stu)] + [len(stu)]
segs = {int(TITLE.match(stu[a:b]).group(1)): stu[a:b] for a, b in zip(idx, idx[1:])}

for n in nos:
    path = cards[n - 1]
    t = io.open(os.path.join(ROOT, path), encoding="utf-8-sig").read()
    front = t.split("\n## 参考答案")[0]
    print("=" * 78)
    print("题 %d  卡=%s" % (n, path.split("/")[-1]))
    print("--- 卡「题目」段的每个图引用上下文 ---")
    for m in IMG_MD.finditer(front):
        s = max(0, m.start() - 90)
        print("   [%s…]" % front[s:m.start()].replace("\n", "⏎")[-90:])
        print("   ▸ ![](images/%s)" % m.group(1)[:24])
        nxt = front[m.end():m.end() + 70].replace("\n", "⏎")
        print("     后文: %s" % nxt)
    print("--- 学生版题 %d 的图 ---" % n)
    seg = segs.get(n, "")
    for m in IMG_EMBED.finditer(seg):
        s = max(0, m.start() - 70)
        print("   [%s…] ▸ %s…" % (seg[s:m.start()].replace("\n", "⏎")[-70:], m.group(1)[:24]))
    if not IMG_EMBED.search(seg):
        print("   （无图）")
    print("--- 学生版题 %d 题面前 220 字 ---" % n)
    print("   " + seg.split("#### 答案")[0][:220].replace("\n", "⏎"))
