#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""match_by_content.py —— 用**题面内容**在源目录的所有 PDF（含「讲评/解析/答案」）里定位含该题的文件。
原理：8-gram 覆盖率 > 0.25 ⇒ 该 PDF 含此题。这是比文件名更可靠的匹配。"""
import csv, glob, os, re, sys, json, collections
sys.stdout.reconfigure(encoding="utf-8")
import fitz
try:
    fitz.TOOLS.mupdf_display_errors(False); fitz.TOOLS.mupdf_display_warnings(False)
except Exception:
    pass
R = r"C:\Obsidion\妙妙屋"
OCR = os.path.join(R, "06-外部资料导入/OCR")
sys.path.insert(0, os.path.join(R, ".workbuddy/tmp/opt_pipe"))
sys.argv = ["x", "--vol", "D3", "--all-years"]
import build_org as BO

CACHE = os.path.join(R, ".workbuddy/tmp/opt_pipe/pdf_text_cache.json")
cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}


def pdf_text(p):
    p = p.replace("\\", "/")
    if p in cache:
        return cache[p]
    try:
        d = fitz.open(p)
        t = "\n".join(d[i].get_text() for i in range(d.page_count))
        d.close()
    except Exception:
        t = ""
    cache[p] = t
    return t


def norm(s):
    s = re.sub(r"!\[[^\]]*\)?", "", s or "")
    s = re.sub(r"\$[^$]*\$", "", s)
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", s)


rows = [r for r in csv.DictReader(open(os.path.join(R, "09-审计报告/2026-10-07-不可组卷题目清单.csv"), encoding="utf-8-sig"))
        if r["reason"] == "无答案/占位"]
found, none = [], []
for r in rows:
    p = os.path.join(R, r["path"])
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    try:
        c = BO.X.extract(p)
    except Exception:
        continue
    qn = norm(c["question"])[:400]
    if len(qn) < 40:
        none.append((r["inst"], os.path.basename(p)[:34], "题面过短")); continue
    gs = [qn[k:k + 8] for k in range(0, len(qn) - 8, 6)]
    m = re.search(r'^source_file:\s*["\']?(.*?)["\']?\s*$', t, re.M)
    stem = re.sub(r"\.md$", "", os.path.basename(m.group(1) if m else ""))
    srcs = glob.glob(OCR + "/**/" + stem + "*.pdf", recursive=True)
    d = os.path.dirname(srcs[0]) if srcs else None
    if not d:
        none.append((r["inst"], os.path.basename(p)[:34], "源目录未定位")); continue
    best = (0.0, None)
    for f in os.listdir(d):
        if not f.lower().endswith(".pdf"):
            continue
        fp = os.path.join(d, f)
        txt = norm(pdf_text(fp))
        if len(txt) < 200:
            continue
        cov = sum(1 for g in gs if g in txt) / len(gs)
        if cov > best[0]:
            best = (cov, f)
    if best[0] >= 0.25:
        found.append((r["inst"], r["path"], r["qno"], os.path.basename(p)[:32], round(best[0], 2), best[1][:40]))
    else:
        none.append((r["inst"], os.path.basename(p)[:34], "最高覆盖 %.2f（%s）" % (best[0], (best[1] or "无")[:18])))
json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)

print("★ 内容匹配到含该题的文件：%d 张" % len(found))
for inst, path, qno, nm, cov, f in found:
    print("   %-8s %-32s 第%-3s题 覆盖%.2f ← %s" % (inst, nm, qno, cov, f))
print("\n未匹配：%d 张 %s" % (len(none), dict(collections.Counter(n[0] for n in none).most_common())))
for inst, nm, why in none[:12]:
    print("   %-8s %-34s %s" % (inst, nm, why))
json.dump([[f[1], f[2], f[5], f[4]] for f in found],
          open(os.path.join(R, ".workbuddy/tmp/opt_pipe/content_hits.json"), "w"), ensure_ascii=False)
