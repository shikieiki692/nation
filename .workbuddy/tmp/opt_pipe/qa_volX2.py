# -*- coding: utf-8 -*-
"""qa_volX2.py —— 卷终检（结构 + 图片守恒 + 泄露 + 表格）。

用法：python -X utf8 qa_volX2.py [--vol XIp] [--quota "结构化学=5,化学原理=5"] [--zhenti|--legacy]
  --zhenti（默认）：核 00-首页/题组Word/初赛模拟卷/真题版式/ 下的交付 docx
  --legacy        ：核 00-首页/题组Word/初赛模拟卷/ 下的旧式 docx
题数不写死，由 build_org.QUOTA 求和得出。
"""
import io
import os
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(ROOT, "04-题库")
DESK = os.path.join(ROOT, "00-首页", "题组Word", "初赛模拟卷")
sys.path.insert(0, os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe"))
import build_org as BO          # noqa: E402  （BO.QUOTA / BO.VOL 由 sys.argv 决定）

VOL = BO.VOL
# 题数优先取**固化计划**（vol_plan_<VOL>.json）；无计划才回退 QUOTA 求和
_PLAN = os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe", "vol_plan_%s.json" % VOL)
if os.path.exists(_PLAN):
    import json
    N = sum(len(lst) for _, lst in json.load(open(_PLAN, encoding="utf-8")))
    print("题数取自计划 %s：%d" % (os.path.basename(_PLAN), N))
else:
    N = sum(q for _, _, q in BO.QUOTA)
if "--legacy" in sys.argv:
    OUTDIR = DESK
    NAME = "初赛模拟卷%s（非有机·%s）.docx"
else:
    OUTDIR = os.path.join(DESK, "真题版式")
    NAME = "初赛模拟卷%s（非有机·%s·真题版式）.docx"
CMAP = {"答案版": ("答案与解析版" if "--legacy" not in sys.argv else "答案版"),
        "学生版": "学生版"}

bad = 0
print("卷 %s ｜ 题数 %d ｜ docx 目录 %s" % (VOL, N, os.path.relpath(OUTDIR, ROOT)))


def chk(cond, msg):
    global bad
    print(("  ✓ " if cond else "  ✗ ") + msg)
    if not cond:
        bad += 1


for tag in ("答案版", "学生版"):
    print("=" * 78)
    print(tag)
    mdp = os.path.join(QB, "初赛模拟卷%s（非有机·%s）.md" % (VOL, tag))
    md = io.open(mdp, encoding="utf-8").read()
    docxp = os.path.join(OUTDIR, NAME % (VOL, CMAP[tag]))
    if not os.path.exists(docxp):
        chk(False, "交付 docx 缺失：%s" % os.path.relpath(docxp, ROOT))
        continue
    z = zipfile.ZipFile(docxp)
    doc = z.read("word/document.xml").decode("utf-8")
    media = [n for n in z.namelist() if n.startswith("word/media/")]

    # ⚠️ 图引用须**同时认 64 位哈希与别名两种形态**（`xxx_ans_…jpg`），否则媒体数对不上会误报
    imgs = re.findall(r"!\[\[([^\]\|\\]+?)(?:\\?\|\d+)?\]\]", md)
    blips = len(re.findall(r"<a:blip", doc))
    chk(len(media) == len(imgs), "图守恒 md=%d media=%d" % (len(imgs), len(media)))
    chk(blips == len(imgs), "图守恒 blip=%d md=%d" % (blips, len(imgs)))

    # 结构
    chk(len(re.findall(r"^### 第 \d+ 题", md, re.M)) == N, "%d 题标题" % N)
    chk(not re.search(r"<table>|</table>", md), "字面 <table> = 0")
    lit = [t for t in re.findall(r"<w:t[^>]*>(.*?)</w:t>", doc, re.S) if "$" in t]
    chk(not lit, "字面 $ = %d" % len(lit))

    # 泄露（题面区）
    parts = re.split(r"\n### 第 (\d+) 题（\d+ 分）[^\n]*\n", md)
    leaks = []
    for i in range(1, len(parts), 2):
        q = parts[i + 1].split("#### 答案")[0]
        q = re.sub(r"^## 第[一二三四]部分[^\n]*\n", "", q, flags=re.M)
        q = re.sub(r"^> 来源：[^\n]*\n", "", q, flags=re.M)
        h = BO.LEAK.findall(q)
        if h:
            leaks.append((parts[i], sorted(set(h))[:3]))
    chk(not leaks, "题面泄露 = %d %s" % (len(leaks), leaks[:3]))

    # 表格：**表体中段**的全空行（表头留空是 layout_figs 的设计，不算缺陷）
    rows = md.split("\n")
    bad_empty = []
    for i, l in enumerate(rows):
        if not l.strip().startswith("|") or ":-" in l:
            continue
        cells = [c for c in re.split(r"(?<!\\)\|", l.strip().strip("|"))]
        if any(c.strip() for c in cells):
            continue
        prev = rows[i - 1].strip() if i else ""
        if prev.startswith("|") and ":-" not in prev:
            bad_empty.append((i + 1, l))
    chk(not bad_empty, "表体全空行 = %d %s" % (len(bad_empty), bad_empty[:3]))

    if tag == "答案版":
        sec = md.split("## 附：选题清单")[1]
        data = [l for l in sec.split("\n") if re.match(r"^\|\s*\d+\s*\|", l)]
        chk(len(data) == N, "清单 %d 行" % N)
        chk(all(len(re.split(r"(?<!\\)\|", l.strip().strip("|"))) == 7 for l in data), "清单 7 列")
    else:
        chk("#### 答案" not in md, "学生版无答案区")
        chk("已撤题" not in md, "学生版无来源行")

print("=" * 78)
print("问题数：%d" % bad)
