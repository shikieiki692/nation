#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_anspages.py —— 校验「纯答案页型」卡的答案图是否真的对应该卡题号。
判据：图内 OCR 文本 含「第X题」或 ≥2 处「X.K」子问号 ⇒ 判对；
      若含「第Y题」(Y≠X) 且无本卡题号 ⇒ 疑挂错。
"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Obsidion\妙妙屋"
CACHE = os.path.join(R, ".workbuddy/tmp/opt_pipe/ocr_loc/anspages.json")
os.makedirs(os.path.dirname(CACHE), exist_ok=True)

rows = []
for p in glob.glob(os.path.join(R, "04-题库/**/题-*.md"), recursive=True):
    t = open(p, encoding="utf-8-sig", errors="replace").read().replace("\r\n", "\n")
    j = t.find("## 参考答案"); k = t.find("## 知识点映射")
    a = t[j:k] if j > 0 and k > j else ""
    ims = re.findall(r"!\[\]\(images/([^)]+)\)", a)
    if not ims or not all(x.startswith("答案页-") for x in ims):
        continue
    m = re.search(r"题-[A-Z]+-\d+-(\d+)-", os.path.basename(p))
    q = int(m.group(1)) if m else None
    rows.append((p, q, ims))

if os.path.exists(CACHE):
    data = json.load(open(CACHE, encoding="utf-8"))
else:
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    data = {}
    todo = []
    for p, q, ims in rows:
        d = os.path.dirname(p)
        for n in ims:
            fp = os.path.join(d, "images", n)
            if fp not in data and os.path.exists(fp):
                todo.append((fp, n))
    print("待 OCR %d 图" % len(todo), flush=True)
    for i, (fp, n) in enumerate(todo):
        try:
            res, _ = ocr(fp)
            data[fp] = " ".join(x[1] for x in (res or []))
        except Exception as e:
            data[fp] = "!!ERR:%s" % e
        if i % 10 == 0:
            print("  %d/%d" % (i, len(todo)), flush=True)
            json.dump(data, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(data, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)

MARK = re.compile(r"第\s*(\d+)\s*题")
print("\n%-3s %-44s %s" % ("题", "卡", "判定"))
susp = []
for p, q, ims in sorted(rows, key=lambda r: (r[1] or -1)):
    d = os.path.dirname(p)
    texts = []
    for n in ims:
        texts.append(data.get(os.path.join(d, "images", n), ""))
    joined = " ".join(texts)
    qs = {int(m.group(1)) for m in MARK.finditer(joined.replace(" ", ""))}
    sub = len(re.findall(r"(?<!\d)%d\s*[\.．]\s*\d" % q, joined)) if q else 0
    if q is None:
        verdict = "题号未解析"
    elif q in qs:
        verdict = "✔ 含第%d题" % q
    elif sub >= 1:
        verdict = "✔ 含子问 %d.x ×%d" % (q, sub)
    elif qs:
        verdict = "⚠ 只含第%s题（疑挂错）" % ",".join(map(str, sorted(qs)))
        susp.append((p, q, sorted(qs)))
    else:
        verdict = "? 无题号信息"
    print("%-3s %-44s %s" % (q, os.path.basename(p)[:44], verdict))
print("\n疑似挂错 %d 张" % len(susp))
for p, q, qs in susp:
    print("   ", os.path.basename(p)[:60], "本卡第%d题 vs 图内第%s题" % (q, qs))
