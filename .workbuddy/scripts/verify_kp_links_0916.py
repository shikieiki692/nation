# -*- coding: utf-8 -*-
"""核验 7 份新提炼页 frontmatter 中所有 wikilink 目标存在且非 deprecated。"""
import os, re, glob, sys

ROOT = r"C:\Obsidion\妙妙屋"
KP = os.path.join(ROOT, "03-知识点")

# 建 KP 索引：basename -> fullpath
kp_index = {}
for dirpath, _, files in os.walk(KP):
    for fn in files:
        if fn.endswith(".md"):
            kp_index.setdefault(fn[:-3], os.path.join(dirpath, fn))

FILES = [
    "07-资料提炼/书籍提炼/提炼-上海中学竞赛课程-第二分册-电化学基础.md",
    "07-资料提炼/书籍提炼/提炼-上海中学竞赛课程-第二分册-离子反应.md",
    "07-资料提炼/书籍提炼/提炼-上海中学竞赛课程-第二分册-滴定分析.md",
    "07-资料提炼/书籍提炼/提炼-上海中学竞赛课程-第四分册-醛与酮.md",
    "07-资料提炼/书籍提炼/提炼-上海中学竞赛课程-第四分册-羧酸及其衍生物.md",
    "07-资料提炼/书籍提炼/提炼-上海中学竞赛课程-第四分册-杂环化合物.md",
    "07-资料提炼/书籍提炼/提炼-上海中学竞赛课程-第四分册-糖、氨基酸.md",
]

FM_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.S)
LINK_RE = re.compile(r"\[\[([^\]\|#]+)")

bad, total, seen = [], 0, set()
for rel in FILES:
    path = os.path.join(ROOT, rel.replace("/", os.sep))
    with open(path, "r", encoding="utf-8", newline="") as f:
        txt = f.read()
    m = FM_RE.match(txt)
    if not m:
        bad.append((rel, "<NO-FRONTMATTER>", "无 frontmatter")); continue
    fm = m.group(1)
    for raw in LINK_RE.findall(fm):
        tgt = raw.strip().strip('"').strip("'").rstrip("\\")
        total += 1
        if tgt in seen:
            continue
        seen.add(tgt)
        p = kp_index.get(tgt)
        if not p:
            bad.append((rel, tgt, "目标页不存在")); continue
        with open(p, "r", encoding="utf-8", errors="replace") as g:
            head = g.read(2000)
        if re.search(r"^status:\s*deprecated", head, re.M):
            bad.append((rel, tgt, "目标页 status: deprecated"))

print(f"frontmatter wikilink 出现 {total} 次 / 去重 {len(seen)} 个目标")
print(f"目标页缺失或弃用：{len(bad)}")
for rel, tgt, why in bad:
    print(f"  ❌ [{why}] {tgt}  ← {rel}")
if not bad:
    print("✅ 全部 wikilink 目标存在且非 deprecated")
