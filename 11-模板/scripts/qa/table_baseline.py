# -*- coding: utf-8 -*-
"""全库表格健康度基线快照（供后续回归对照）。
输出：09-审计报告/表格健康度基线-2026-09-20.md + .workbuddy/tmp/table_baseline.json
只读扫描。
"""
import os, re, sys, io, json, collections
out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
VAULT = r"C:\Obsidion\妙妙屋"
TMP = os.path.join(VAULT, ".workbuddy", "tmp")

TABLE_PAT = re.compile(r"<table\b.*?</table>", re.I | re.S)
ROW_PAT   = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.I | re.S)
CELL_ATTR = re.compile(r"<t[dh]\b([^>]*)>(.*?)</t[dh]>", re.I | re.S)
SPAN_COL  = re.compile(r"colspan\s*=\s*[\"']?(\d+)", re.I)
SPAN_ROW  = re.compile(r"rowspan\s*=\s*[\"']?(\d+)", re.I)
TAG_PAT   = re.compile(r"<[^>]+>")
ENTITY_PAT = re.compile(r"&(nbsp|amp|lt|gt|quot|#\d+);", re.I)
PIPE_SEP  = re.compile(r"^\s*\|[\s:|-]+\|\s*$")

REDLINE = ("04-题库", "05-真题库", "_归档")
ACTIVE = ("04-课件", "07-资料提炼")
DEAD = ("09-AI工作区",)

def zone(top):
    if top in REDLINE: return "红线区"
    if top in ACTIVE: return "活跃线"
    if top in DEAD: return "废弃归档"
    return "无主区"

def norm_cell(s):
    s = TAG_PAT.sub("", s).replace("\u00a0", " ").strip()
    return re.sub(r"[ \t]+", " ", s)

def classify(block):
    """与主转换器判据一致"""
    low = block.lower()
    if "<img" in low: return "img"
    if ENTITY_PAT.search(block): return "entity"
    rows = []
    for tr in ROW_PAT.findall(block):
        r = []
        for m in CELL_ATTR.finditer(tr):
            a, c = m.group(1), m.group(2)
            cm = SPAN_COL.search(a); rm = SPAN_ROW.search(a)
            r.append((norm_cell(c), int(rm.group(1)) if rm else 1,
                      int(cm.group(1)) if cm else 1))
        if r: rows.append(r)
    if not rows: return "norows"
    if any(rs > 1 for r in rows for _, rs, _ in r) or "rowspan" in low:
        # rowspan：判「能否下拉填充为矩形」
        grid = []
        for ri, r in enumerate(rows):
            while len(grid) <= ri: grid.append([])
            for (txt, rs, cs) in r:
                ci = 0
                while ci < len(grid[ri]) and grid[ri][ci] is not None: ci += 1
                for k in range(cs):
                    while ci + k >= len(grid[ri]): grid[ri].append(None)
                    grid[ri][ci + k] = txt if k == 0 else ""
                if rs > 1:
                    for rr in range(ri+1, ri+rs):
                        while len(grid) <= rr: grid.append([])
                        for k in range(cs):
                            while ci+k >= len(grid[rr]): grid[rr].append(None)
                            grid[rr][ci+k] = txt if k == 0 else ""
        per = [len(g) for g in grid]
        if len(set(per)) != 1: return "rowspan-irregular"
        width = per[0] if per else 0
    else:
        width = max(sum(cs for _, _, cs in r) for r in rows)
    if width == 0 or width > 8: return f"width{width}"
    if width <= 2: return f"narrow{width}"
    flat = []
    for r in rows:
        for t, _, _ in r:
            flat.append(t)
    avg = sum(len(c) for c in flat) / max(1, len(flat))
    if avg > 40: return f"prose{int(avg)}"
    for c in flat:
        if c.replace("\\$", "").count("$") % 2 == 1: return "halfwrap"
    return "CONVERTIBLE"

stat = collections.Counter()
zone_stat = collections.defaultdict(collections.Counter)
file_has_table = collections.Counter()
pipe_count = 0
nfiles = 0

for root, dirs, files in os.walk(VAULT):
    rel = os.path.relpath(root, VAULT).replace("\\", "/")
    top = rel.split("/")[0] if rel != "." else "(根)"
    dirs[:] = [d for d in dirs if d not in (".git", ".obsidian", "node_modules", "媒体仓库", ".workbuddy")]
    for f in files:
        if not f.endswith(".md"): continue
        nfiles += 1
        p = os.path.join(root, f)
        try: text = open(p, encoding="utf-8").read()
        except Exception: continue
        z = zone(top)
        # pipe table 计数
        lines = text.split("\n")
        for i in range(len(lines) - 1):
            if lines[i].lstrip().startswith("|") and PIPE_SEP.match(lines[i+1]):
                pipe_count += 1
        if "<table" not in text.lower(): continue
        for m in TABLE_PAT.finditer(text):
            b = m.group(0)
            if b.count("<td") + b.count("<th") == 0: continue
            c = classify(b)
            stat[c] += 1
            zone_stat[z][c] += 1
            file_has_table[top] += 1

total = sum(stat.values())
print(f"== 全库表格健康度基线（{nfiles} md 文件）==", file=out)
print(f"  仍为 HTML 形态的表: {total}", file=out)
print(f"  Markdown pipe table 块: {pipe_count}", file=out)
print("\n== 按判据 ==", file=out)
for k, v in stat.most_common():
    print(f"  {k:<22} {v:>5}  ({v*100//max(1,total)}%)", file=out)
print("\n== 按作用域 ==", file=out)
for z in ("无主区", "活跃线", "红线区", "废弃归档"):
    c = zone_stat[z]
    t = sum(c.values())
    print(f"  {z:<8} 总{t:>5}  可转 {c.get('CONVERTIBLE',0):>5}  "
          f"rowspan {c.get('rowspan-irregular',0)+c.get('CONVERTIBLE',0) and 0 or 0:>3}", file=out)
    for k, v in c.most_common(6):
        print(f"      {k:<22} {v}", file=out)

json.dump(dict(nfiles=nfiles, html_tables=total, pipe_blocks=pipe_count,
               by_verdict=dict(stat), by_zone={z: dict(c) for z, c in zone_stat.items()}),
          open(os.path.join(TMP, "table_baseline.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"\n→ .workbuddy/tmp/table_baseline.json", file=out)
out.flush()
