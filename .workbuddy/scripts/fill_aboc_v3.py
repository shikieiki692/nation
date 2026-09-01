# -*- coding: utf-8 -*-
"""ABOC 填充 v3：行中切分 + 同码取最长 + # 标题截断 + 图落媒体仓库。dry-run/--write"""
import os, io, re, sys, shutil, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(VAULT)
WRITE = "--write" in sys.argv
EXCLUDE = {"题-117-ABOC-Ch3-3.10-解释以下反应产物的选择性.md"}  # 块混入思考题，留人工

s = io.open("mineru/03-教材书籍/ABOC有机化学/ABOC202505_200-397.md", encoding="utf-8-sig", errors="replace").read()
i0 = s.find("# 习题解析")
sec = s[i0:]
pat = re.compile(r"(?:自学练习|习题|例题)\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-[0-9]+[A-Za-z]?)?)")
marks = [(m.start(), m.group(1)) for m in pat.finditer(sec)]
best = collections.defaultdict(str)
for idx, (st, code) in enumerate(marks):
    en = marks[idx + 1][0] if idx + 1 < len(marks) else len(sec)
    body = sec[st:en].strip()
    if len(body) > len(best[code]):
        best[code] = body

n_ok = n_img = n_skip = 0
log = []
d = "04-题库/教材习题/ABOC"
for dp, dn, fs in os.walk(d):
    for fn in sorted(fs):
        if not fn.endswith(".md"):
            continue
        p = os.path.join(dp, fn)
        name = os.path.basename(p)
        c = io.open(p, encoding="utf-8-sig", errors="replace").read()
        if not re.search(r"## 解题思路\s*\n+\s*（待补充）", c) or name in EXCLUDE:
            continue
        codes = set()
        m = re.search(r"Ch(\d+)-([0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-[0-9]+[A-Za-z]?)?)", name)
        if m:
            codes.add(m.group(2))
        fms = c.split("---")[1] if c.startswith("---") else ""
        srcm = re.search(r"(?m)^source:\s*(.+)$", fms)
        if srcm:
            for mm in re.finditer(r"([0-9]+\.[0-9]{1,2}(?:\.[0-9]+)?(?:-[0-9]+[A-Za-z]?)?)", srcm.group(1)):
                codes.add(mm.group(1))
        hit = next((cd for cd in codes if cd in best), None)
        if not hit:
            n_skip += 1
            continue
        if len(best[hit]) > 3000:
            n_skip += 1
            log.append((fn[:50], f"超长{len(best[hit])}护栏"))
            continue
        b = re.sub(r"(?s)\n# .*", "", best[hit])  # 遇章节标题截断
        body = re.sub(r"^\s*(?:自学练习|习题|例题)\s+" + re.escape(hit) + r"\s*", "", b).strip()
        txt_len = len(re.sub(r"\s", "", re.sub(r"[#|>*$~-]", "", re.sub(r"!\[\[[^\]]+\]\]", "", body))))
        if txt_len < 20:
            n_skip += 1
            continue
        # 图落库
        for rel in re.findall(r"!\[\[(ABOC202505_200-397_images/[^]|]+?)(?:\|[^\]]*)?\]\]", body):
            srcp = os.path.join("mineru/03-教材书籍/ABOC有机化学", rel)
            dstp = os.path.join("媒体仓库", os.path.basename(rel))
            if not os.path.exists(dstp):
                if os.path.exists(srcp):
                    if WRITE:
                        shutil.copyfile(srcp, dstp)
                    n_img += 1
                else:
                    log.append((fn[:50], "图缺失跳过"))
                    body = ""
                    break
        if not body:
            n_skip += 1
            continue
        new_body = re.sub(r"!\[\[ABOC202505_200-397_images/([^]|]+?)(?:\|[^\]]*)?\]\]", r"![[\1]]", body)
        note = "\n\n> 来源：ABOC 原书「习题解析」节逐字转录（OCR）。如与纸质原书有出入，以原书为准。"
        newc = re.sub(r"(## 解题思路\s*\n+)\s*（待补充）", lambda mm: mm.group(1) + "\n" + new_body + note, c, count=1)
        if newc == c:
            n_skip += 1
            continue
        n_ok += 1
        log.append((fn[:50], f"文{txt_len}" + (f"+图" if "![[" in new_body else "")))
        if WRITE:
            io.open(p, "w", encoding="utf-8", newline="").write(newc)

print(f"v3 可写: {n_ok} | 图复制: {n_img} | 跳过: {n_skip}")
for r in log:
    print("  ", r)
