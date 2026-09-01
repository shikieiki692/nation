# -*- coding: utf-8 -*-
"""ABOC 填充 v2：行中切分边界（解决 OCR 标题并行），短块合并，超长块再次评估。dry-run 统计。"""
import os, io, re, sys, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

s = io.open("mineru/03-教材书籍/ABOC有机化学/ABOC202505_200-397.md", encoding="utf-8-sig", errors="replace").read()
i0 = s.find("# 习题解析")
sec = s[i0:]

# 行中切分：每个 "自学练习|习题|例题 N.N..." 出现处都是边界
pat = re.compile(r"(?:自学练习|习题|例题)\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-[0-9]+[A-Za-z]?)?)")
marks = [(m.start(), m.group(1)) for m in pat.finditer(sec)]
raw = []
for idx, (st, code) in enumerate(marks):
    en = marks[idx + 1][0] if idx + 1 < len(marks) else len(sec)
    raw.append([code, sec[st:en].strip()])
# 短块(<25字)合并回前一同一前缀块（误切保护：正文引用题号会切出短块）
blocks = collections.OrderedDict()
for code, body in raw:
    if len(re.sub(r"\s", "", body)) < 25 and blocks:
        last_code = list(blocks)[-1]
        blocks[last_code] = blocks[last_code] + "\n" + body
        continue
    blocks[code] = body  # 同码后块覆盖前块？——保留最长
for code in list(blocks):
    pass
# 同码取最长
best = collections.defaultdict(str)
for code, body in raw:
    if len(re.sub(r"\s", "", body)) >= 25:
        if len(body) > len(best[code]):
            best[code] = body

print("切分标记:", len(marks), "| 有效块:", len(best))
longs = [(c, len(b)) for c, b in best.items() if len(b) > 3000]
print("超长块:", longs)

# 占位题匹配统计（v2）
d = "04-题库/教材习题/ABOC"
stats = collections.Counter()
rows = []
for dp, dn, fs in os.walk(d):
    for fn in fs:
        if not fn.endswith(".md"):
            continue
        p = os.path.join(dp, fn)
        c = io.open(p, encoding="utf-8-sig", errors="replace").read()
        if not re.search(r"## 解题思路\s*\n+\s*（待补充）", c):
            continue
        name = os.path.basename(p)
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
            stats["无匹配(原书未解析)"] += 1
            continue
        body = re.sub(r"^\s*(?:自学练习|习题|例题)\s+" + re.escape(hit) + r"\s*", "", best[hit], count=1).strip()
        txt_len = len(re.sub(r"\s", "", re.sub(r"[#|>*$~-]", "", re.sub(r"!\[\[[^\]]+\]\]", "", body))))
        n_img = len(re.findall(r"!\[\[", body))
        if len(best[hit]) > 3000:
            stats["超长护栏"] += 1
            rows.append((name[:48], hit, f"超长{len(best[hit])}"))
        elif txt_len >= 20:
            stats["可写(文)"] += 1
            rows.append((name[:48], hit, f"文{txt_len}" + (f"+图{n_img}" if n_img else "")))
        elif n_img:
            stats["可写(纯图)"] += 1
            rows.append((name[:48], hit, f"纯图{n_img}"))
        else:
            stats["空块(原书无内容)"] += 1

print("--- v2 匹配分布 ---")
for k, v in stats.most_common():
    print(f"  {k}: {v}")
print("--- 可写与超长明细 ---")
for r in rows:
    print("  ", r)
