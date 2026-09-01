# -*- coding: utf-8 -*-
"""ABOC 无匹配题解剖：题库侧编号形态 vs 解析节实际标题形态"""
import os, io, re, sys, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

s = io.open("mineru/03-教材书籍/ABOC有机化学/ABOC202505_200-397.md", encoding="utf-8-sig", errors="replace").read()
i0 = s.find("# 习题解析")
sec = s[i0:]

# 1) 解析节里所有"看起来像题号"的行首形态（放宽）
forms = collections.Counter()
for ln in sec.splitlines():
    ln = ln.strip()
    m = re.match(r"^(自学练习|习题|例题|FINAL ?TEST|期末|第[一二三四五六七八九十]+章|Chapter|Ch\.?)\s*(.{0,18})", ln)
    if m:
        forms[f"{m.group(1)} {m.group(2)[:14]}"] += 1
print("--- 解析节标题形态（前30）---")
for k, v in forms.most_common(30):
    print(f"  {v:3d}  {k}")

# 2) 无匹配占位题的题号来源分布
d = "04-题库/教材习题/ABOC"
blocks_codes = set(re.findall(r"(?m)^(?:自学练习|习题|例题)\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-[0-9]+[A-Za-z]?)?)", sec))
nomatch = []
for dp, dn, fs in os.walk(d):
    for fn in fs:
        if not fn.endswith(".md"):
            continue
        p = os.path.join(dp, fn)
        c = io.open(p, encoding="utf-8-sig", errors="replace").read()
        if not re.search(r"## 解题思路\s*\n+\s*（待补充）", c):
            continue
        name = os.path.basename(p)
        has = False
        m = re.search(r"Ch(\d+)-([0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-[0-9]+[A-Za-z]?)?)", name)
        if m and m.group(2) in blocks_codes:
            has = True
        if has:
            continue
        nomatch.append((name, re.search(r"(?m)^source:\s*(.{0,60})", c.split("---")[1]).group(1) if c.startswith("---") else ""))
print(f"\n--- 无匹配占位题 {len(nomatch)} 条的文件名/source 形态（前25）---")
for n, sr in nomatch[:25]:
    print(f"  {n[:56]}")
    print(f"      src: {sr[:70]}")
