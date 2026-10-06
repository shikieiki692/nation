# -*- coding: utf-8 -*-
"""qa_volX2.py —— 卷X 终检（结构 + 图片守恒 + 泄露 + 表格）。"""
import io, re, os, sys, glob, json, zipfile
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Obsidion\妙妙屋"
QB = os.path.join(ROOT, "04-题库")
OUT = os.path.join(ROOT, "00-首页", "题组Word", "初赛模拟卷")
sys.path.insert(0, os.path.join(ROOT, ".workbuddy", "tmp", "opt_pipe"))
import build_org as BO

bad = 0


def chk(cond, msg):
    global bad
    print(("  ✓ " if cond else "  ✗ ") + msg)
    if not cond:
        bad += 1


for tag in ("答案版", "学生版"):
    print("=" * 78)
    print(tag)
    mdp = os.path.join(QB, "初赛模拟卷X（非有机·%s）.md" % tag)
    md = io.open(mdp, encoding="utf-8").read()
    docxp = os.path.join(OUT, "初赛模拟卷X（非有机·%s）.docx" % tag)
    z = zipfile.ZipFile(docxp)
    doc = z.read("word/document.xml").decode("utf-8")
    media = [n for n in z.namelist() if n.startswith("word/media/")]

    imgs = re.findall(r"!\[\[\s*([0-9a-fA-F]{64}\.[A-Za-z0-9]+)", md)
    blips = len(re.findall(r"<a:blip", doc))
    chk(len(media) == len(imgs), "图守恒 md=%d media=%d" % (len(imgs), len(media)))
    chk(blips == len(imgs), "图守恒 blip=%d md=%d" % (blips, len(imgs)))

    # 结构
    chk(len(re.findall(r"^### 第 \d+ 题", md, re.M)) == 16, "16 题标题")
    chk(not re.search(r"<table>|</table>", md), "字面 <table> = 0")
    lit = [t for t in re.findall(r"<w:t[^>]*>(.*?)</w:t>", doc, re.S) if "$" in t]
    chk(not lit, "字面 $ = %d" % len(lit))

    # 泄露（题面区）
    parts = re.split(r"\n### 第 (\d+) 题（\d+ 分）[^\n]*\n", md)
    leaks = []
    for i in range(1, len(parts), 2):
        q = parts[i + 1].split("#### 答案")[0]
        q = re.sub(r"^## 第[一二三]部分[^\n]*\n", "", q, flags=re.M)
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
        # 紧跟在另一表行/分隔行之后的空行 = 表头或表体 ⇒ 只有「前面已有数据行」才是中段空行
        if prev.startswith("|") and ":-" not in prev:
            bad_empty.append((i + 1, l))
    chk(not bad_empty, "表体全空行 = %d %s" % (len(bad_empty), bad_empty[:3]))

    if tag == "答案版":
        sec = md.split("## 附：选题清单")[1]
        data = [l for l in sec.split("\n") if re.match(r"^\|\s*\d+\s*\|", l)]
        chk(len(data) == 16, "清单 16 行")
        chk(all(len(re.split(r"(?<!\\)\|", l.strip().strip("|"))) == 7 for l in data), "清单 7 列")
    else:
        chk("#### 答案" not in md, "学生版无答案区")
        chk("已撤题" not in md, "学生版无来源行")

print("=" * 78)
print("问题数：%d" % bad)
