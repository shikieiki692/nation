# -*- coding: utf-8 -*-
"""
把当前校验报告里的「断链」全部抽出来，按可修复性分门别类。

分类口径（保守、宁可不动）：
  A. 路径错误   —— 目标文件在全库存在，但引用写的路径/名字不对（可自动改）
  B. 子编号多级 —— 形如 题-NN-M-K-标题，去掉一级或多级后能精确对上真实文件
  C. 真红链     —— 全库任何位置都没有同名 .md，只能新建笔记或人工判断
"""
import os, re, json, collections

VAULT = r"C:\Obsidion\妙妙屋"
REPORT = os.path.join(VAULT, r"09-审计报告\auto-validation\2026-09-01-validation.md")
OUT = os.path.join(VAULT, r".workbuddy\tmp\broken_links2.json")

RE_LINE = re.compile(
    r"^\s*-\s+`([^`]+)`\s*→\s*\[\[([^\]\|#\^]+?)\]\]\s*→\s*文件不存在\s*$")

# ---------- 1. 解析报告 ----------
items = []
for line in open(REPORT, encoding="utf-8"):
    m = RE_LINE.match(line.rstrip("\n"))
    if m:
        items.append({"src": m.group(1), "target": m.group(2).strip()})

# ---------- 2. 建立全库 md 名 → 路径 索引 ----------
md_by_stem = collections.defaultdict(list)   # 文件名主干 -> [相对路径]
md_by_path = {}                              # 相对路径(无扩展) -> 相对路径
SKIP = {".git", "node_modules", ".obsidian", "__pycache__", ".trash"}
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for fn in files:
        if not fn.lower().endswith(".md"):
            continue
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, VAULT).replace("\\", "/")
        stem = fn[:-3]
        md_by_stem[stem].append(rel)
        md_by_path[rel[:-3]] = rel

# ---------- 3. 分类 ----------
res = {"A_path": [], "B_subnum": [], "C_red": []}

RE_SUB = re.compile(r"^(题-\d+-\d+)-(\d+)-(.+)$")

for it in items:
    tgt = it["target"]
    # 目标带路径时取最后一段做 basename，记录目录
    if "/" in tgt:
        tgt_dir, _, tgt_name = tgt.rpartition("/")
    else:
        tgt_dir, tgt_name = "", tgt

    # A. 路径错误：同 basename 在别处存在（说明文件有，只是路径写错）
    if tgt_name in md_by_stem:
        res["A_path"].append(dict(it, tgt_name=tgt_name,
                                  real=md_by_stem[tgt_name]))
        continue

    # B. 子编号多级：逐级剥离子编号，找精确匹配，且要求同目录
    hit = None
    cur = tgt_name
    depth = 0
    while True:
        m = RE_SUB.match(cur)
        if not m:
            break
        cur = f"{m.group(1)}-{m.group(3)}"
        depth += 1
        if cur in md_by_stem:
            # 目录校验：若引用带了目录，候选必须在该目录下
            cands = md_by_stem[cur]
            if tgt_dir:
                ok = [c for c in cands
                      if os.path.dirname(c).replace("\\", "/") == tgt_dir]
            else:
                ok = cands
            if ok:
                hit = (cur, ok, depth)
                break
    if hit:
        res["B_subnum"].append(dict(it, tgt_name=tgt_name, new_name=hit[0],
                                    real=hit[1], depth=hit[2]))
        continue

    # C. 真红链：按最后一段再看一次去前缀匹配（有些人写了 题-38届初赛/ 这种目录）
    res["C_red"].append(dict(it, tgt_name=tgt_name, tgt_dir=tgt_dir,
                             stem_exists=tgt_name in md_by_stem))

# ---------- 4. 输出 ----------
print(f"断链总数: {len(items)}")
print(f"  A 路径错误（文件在别处）      : {len(res['A_path'])}")
print(f"  B 子编号多级（可精确剥离）    : {len(res['B_subnum'])}")
print(f"  C 真红链（全库无同名 md）     : {len(res['C_red'])}")

print("\n--- A 路径错误 ---")
for r in res["A_path"][:20]:
    print(f"  {r['src']}\n     [[{r['target']}]] → 实存 {r['real']}")

print("\n--- B 子编号多级 ---")
for r in res["B_subnum"][:30]:
    print(f"  {r['src']}\n     [[{r['target']}]] → [[{r['new_name']}]] (剥 {r['depth']} 级) @ {r['real'][0]}")

cnt = collections.Counter(r["tgt_name"] for r in res["C_red"])
print(f"\n--- C 真红链 top30（共 {len(cnt)} 个唯一目标）---")
for k, v in cnt.most_common(30):
    print(f"  {v:3d}  {k}")

json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n明细: {OUT}")
