# -*- coding: utf-8 -*-
"""
知识点→题目文件 的静默错位扫描

背景：validate_kb 的 wikilink 解析有 basename → title → aliases 三级兜底。
题目文件的 frontmatter 常把相关概念写进 aliases（如 题-033-2 的 aliases 含「过氧化氢」），
于是 [[过氧化氢]] 不会报断链，而是**静默解析到一个题目文件上**——
比红链更隐蔽，因为校验器报不出来。

本脚本：扫 03-知识点（及其他知识点类目录）正文里的 wikilink，
若解析目标的 frontmatter type ∈ {题目/真题/例题/题组/题目集}，判为「静默错位」。
"""
import sys, os, re, json, collections

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

import validate_kb as V  # noqa: E402

QB_TYPES = V.QB_TYPES
SCAN_DIRS = ["03-知识点", "04-专题与题型", "12-教学洞察"]

files = []
for d in SCAN_DIRS:
    files += V.collect_md_files(V.VAULT_ROOT, [d])
print(f"扫描 {len(files)} 个文件（{'/'.join(SCAN_DIRS)}）")

LINK = re.compile(r"\[\[([^\]\|#\^]+)")
_tcache = {}


def ftype(p):
    if p in _tcache:
        return _tcache[p]
    try:
        fm, _ = V.parse_frontmatter_from_file(p)
        t = fm.get("type", "")
    except Exception:
        t = ""
    _tcache[p] = t
    return t


mis = collections.defaultdict(list)   # target -> [(src, line)]
nlink = 0
for f in files:
    rel = f.relative_to(V.VAULT_ROOT).as_posix()
    try:
        txt = f.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    _fm, body = V.parse_frontmatter(txt)
    for i, line in enumerate(body.splitlines(), 1):
        for m in LINK.finditer(line):
            t = m.group(1).strip().rstrip(".")
            if not t or V.is_placeholder_target(t):
                continue
            nlink += 1
            tgt = V.find_wikilink_target(t, V.VAULT_ROOT)
            if tgt is None:
                continue
            ty = ftype(tgt)
            if ty in QB_TYPES:
                mis[t].append((rel, i, tgt.relative_to(V.VAULT_ROOT).as_posix(), ty))

print(f"正文 wikilink：{nlink}")
print(f"错位到题目文件的 unique 目标：{len(mis)}")
tot = sum(len(v) for v in mis.values())
print(f"错位引用总数：{tot}")

print("\n--- 按引用次数排序 ---")
for t, hits in sorted(mis.items(), key=lambda kv: -len(kv[1])):
    print(f"  [{len(hits):2d}] [[{t}]] → {hits[0][2]}  (type={hits[0][3]})")
    for src, ln, _p, _ty in hits[:3]:
        print(f"          ← {src}:{ln}")

out = {t: [{"src": a, "line": b, "target": c, "type": d} for a, b, c, d in v]
       for t, v in mis.items()}
json.dump(out, open(os.path.join(VAULT, ".workbuddy", "scripts",
                                 "kp_links_to_questions.json"), "w",
                    encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n已写出 kp_links_to_questions.json")
