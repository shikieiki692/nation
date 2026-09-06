# -*- coding: utf-8 -*-
"""ABOC v4：超长块专项——先截断（遇行首 # 章节标题）再判长。只处理仍为（待补充）的题。dry-run/--write"""
import os, io, re, sys, shutil, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(VAULT)
WRITE = "--write" in sys.argv

s = io.open("mineru/03-教材书籍/ABOC有机化学/ABOC202505_200-397.md", encoding="utf-8-sig", errors="replace").read()
sec = s[s.find("# 习题解析"):]
pat = re.compile(r"(?:自学练习|习题|例题)\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-[0-9]+[A-Za-z]?)?)")
marks = [(m.start(), m.group(1)) for m in pat.finditer(sec)]
best = collections.defaultdict(str)
for idx, (st, code) in enumerate(marks):
    en = marks[idx + 1][0] if idx + 1 < len(marks) else len(sec)
    body = sec[st:en].strip()
    if len(body) > len(best[code]):
        best[code] = body

TARGETS = {"4.13.3", "5.12", "6.13", "7.6.2-2", "9.4.2"}
n_ok = n_img = 0
for code in TARGETS:
    raw = best.get(code, "")
    b = re.sub(r"(?s)\n# .*", "", raw)          # 遇行首 # 标题（章末习题/结语等）截断
    body = re.sub(r"^\s*(?:自学练习|习题|例题)\s+" + re.escape(code) + r"\s*", "", b).strip()
    txt_len = len(re.sub(r"\s", "", re.sub(r"[#|>*$~-]", "", re.sub(r"!\[\[[^\]]+\]\]", "", body))))
    print(f"{code}: 原块 {len(raw)} → 截后 {len(body)} 字（纯文 {txt_len}）")
    if txt_len < 15:
        print("  截后过短，跳过")
        continue
    # 找对应占位题
    d = "04-题库/教材习题/ABOC"
    for dp, dn, fs in os.walk(d):
        for fn in fs:
            if not fn.endswith(".md") or f"-{code}-" not in fn and not fn.startswith("题-"):
                continue
            if f"-{code}-" not in fn:
                continue
            p = os.path.join(dp, fn)
            c = io.open(p, encoding="utf-8-sig", errors="replace").read()
            if not re.search(r"## 解题思路\s*\n+\s*（待补充）", c):
                continue
            imgs = re.findall(r"!\[\[(ABOC202505_200-397_images/[^]|]+?)(?:\|[^\]]*)?\]\]", body)
            ok = True
            for rel in imgs:
                srcp = os.path.join("mineru/03-教材书籍/ABOC有机化学", rel)
                dstp = os.path.join("媒体仓库", os.path.basename(rel))
                if not os.path.exists(dstp):
                    if os.path.exists(srcp):
                        if WRITE:
                            shutil.copyfile(srcp, dstp)
                        n_img += 1
                    else:
                        ok = False
                        break
            if not ok:
                print(f"  {fn[:44]} 图缺失跳过")
                continue
            new_body = re.sub(r"!\[\[ABOC202505_200-397_images/([^]|]+?)(?:\|[^\]]*)?\]\]", r"![[\1]]", body)
            note = "\n\n> 来源：ABOC 原书「习题解析」节逐字转录（OCR）。如与纸质原书有出入，以原书为准。"
            newc = re.sub(r"(## 解题思路\s*\n+)\s*（待补充）", lambda mm: mm.group(1) + "\n" + new_body + note, c, count=1)
            if newc != c:
                n_ok += 1
                print(f"  -> 写入 {fn[:46]}（{len(new_body)} 字）")
                if WRITE:
                    io.open(p, "w", encoding="utf-8", newline="").write(newc)
            break

print(f"\n合计写入: {n_ok}，图复制: {n_img}")
