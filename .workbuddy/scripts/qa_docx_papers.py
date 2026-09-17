# -*- coding: utf-8 -*-
"""对两套新卷子的 docx 做质检：公式 OMML / LaTeX 泄漏 / 图片数 / 学生版答案泄漏。"""
import io
import os
import re
import sys
import zipfile
import glob
import collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
os.chdir(r"C:\Obsidion\妙妙屋")

PAIRS = [
    ("00-首页/题组Word/第一轮·竞赛教材版", "04-课件/习题集/第一轮·竞赛教材版"),
    ("00-首页/题组Word/第一轮·综合套卷", "04-课件/习题集/第一轮·综合套卷"),
]

WT = re.compile(r"<w:t[^>]*>([^<]*)</w:t>")
IMGREF = re.compile(r"!\[\[([^\]|]+)")


def docx_probe(p):
    z = zipfile.ZipFile(p)
    xml = z.read("word/document.xml").decode("utf-8", "replace")
    media = [n for n in z.namelist() if n.startswith("word/media/")]
    text = "".join(WT.findall(xml))
    return {
        "omml": xml.count("<m:oMath"),
        "media": len(media),
        "text": text,
        "size": os.path.getsize(p),
    }


# LaTeX 宏明文（泄漏判据）
LATEX_LEAK = re.compile(r"\\(?:frac|sqrt|mathrm|text|ce|Delta|alpha|beta|rightleftharpoons|times|cdot|approx)\b")
rows = []
summ = collections.Counter()
for outdir, srcdir in PAIRS:
    for p in sorted(glob.glob(outdir + "/*.docx")):
        r = docx_probe(p)
        stem = os.path.basename(p)[:-5]
        # 对应 md（去掉 -教师版/-学生版 后再加括号形式）
        md = None
        for cand in (
            os.path.join(srcdir, stem.replace("-教师版", "（教师版）").replace("-学生版", "（学生版）") + ".md"),
            os.path.join(srcdir, "_总索引.md") if stem == "总索引" else "",
        ):
            if cand and os.path.exists(cand):
                md = cand
                break
        mds = io.open(md, encoding="utf-8", errors="replace").read() if md else ""
        n_img_md = len({x.strip() for x in IMGREF.findall(mds)})
        # 去重后 md 的图（docx media 会按引用次数嵌，故用引用总数更贴）
        n_img_ref = len(IMGREF.findall(mds))
        leak_math = bool(LATEX_LEAK.search(r["text"]))
        leak_dollar = "$$" in r["text"]
        stu = "学生版" in stem
        ans_leak = stu and ("参考答案" in r["text"])
        bad = leak_math or leak_dollar or ans_leak or (n_img_ref and r["media"] == 0)
        summ["files"] += 1
        summ["omml_total"] += r["omml"]
        if leak_math:
            summ["latex_leak"] += 1
        if leak_dollar:
            summ["dollar_leak"] += 1
        if ans_leak:
            summ["answer_leak"] += 1
        if n_img_md and r["media"] == 0:
            summ["img_lost"] += 1
        if bad:
            rows.append((os.path.basename(outdir)[:14], stem, r["omml"], r["media"], n_img_md,
                         "latex" if leak_math else "", "$$" if leak_dollar else "", "答案" if ans_leak else ""))
        if n_img_md:
            summ["img_ok" if r["media"] >= n_img_md else "img_short"] += 1

print("=== 汇总（%d 个 docx）===" % summ["files"])
print("  公式对象(m:oMath) 合计: %d" % summ["omml_total"])
print("  LaTeX 明文泄漏文件: %d" % summ["latex_leak"])
print("  `$$` 明文泄漏文件 : %d" % summ["dollar_leak"])
print("  学生版答案泄漏文件: %d" % summ["answer_leak"])
print("  图片全丢的文件    : %d" % summ["img_lost"])
print("  有图的文件（按去重图集比对）: 够数 %d / 少于 %d" % (summ["img_ok"], summ["img_short"]))
print()
if rows:
    print("=== 问题文件 ===")
    for r in rows[:20]:
        print("   %-14s | %-40s | oMath=%-4d media=%-2d md图=%-2d %s %s %s" % r)
else:
    print("=== 无问题文件 ===")
