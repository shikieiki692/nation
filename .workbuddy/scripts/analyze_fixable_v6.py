# -*- coding: utf-8 -*-
"""
断链可修复性分析 v6

对 broken_links_v5.json 的 112 个 unique 目标，逐个尝试：
  A. basename 解析：去掉路径/子号后，全库有没有同名 md（→ 可重定向）
  B. 模糊匹配：编辑距离 / 子串包含（→ 人工确认候选）
  C. 判定为「应当新建知识点」还是「应当重定向」还是「留红链」

不写入任何文件，只输出候选供人工裁决。
"""
import sys, os, re, json, difflib

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

import validate_kb as V  # noqa: E402

with open(os.path.join(VAULT, ".workbuddy", "scripts", "broken_links_v5.json"),
          encoding="utf-8") as fh:
    data = json.load(fh)
targets = data["targets"]

# ── 构建全库 md 索引（含 resolution-only 目录）──
INDEX = {}   # basename(no ext) -> [relpath]
for f in V.iter_link_resolution_files(V.VAULT_ROOT):
    rel = f.relative_to(V.VAULT_ROOT).as_posix()
    INDEX.setdefault(f.stem, []).append(rel)
print(f"可解析链接目标索引：{len(INDEX)} 个 basename")


def kind(t):
    if re.match(r"^题-\d+", t):
        return "题号"
    if "/" in t:
        return "带路径"
    return "概念术语"


rows = []
for t, d in targets.items():
    k = kind(t)
    base = t.rsplit("/", 1)[-1]
    cand = None
    how = ""
    # A1 直接 basename
    if base in INDEX:
        cand, how = INDEX[base][0], "basename直解"
    else:
        # A2 去一层子号（题-036b-1-1-X → 题-036b-1-X）
        m = re.match(r"^(题-\d+\w*(?:-\d+)*)-(\d+)-(.+)$", base)
        if m:
            c2 = f"{m.group(1)}-{m.group(3)}"
            if c2 in INDEX:
                cand, how = INDEX[c2][0], "折叠子号"
        # A3 模糊：同长度相近
        if not cand:
            close = difflib.get_close_matches(base, INDEX.keys(), n=1, cutoff=0.86)
            if close:
                cand, how = INDEX[close[0]][0], f"模糊({close[0]})"
    rows.append({"t": t, "kind": k, "n": d["n"], "src": d["src"],
                 "cand": cand, "how": how})

json.dump(rows, open(os.path.join(VAULT, ".workbuddy", "scripts",
                                  "fixable_v6.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("\n" + "=" * 70)
for k in ["带路径", "题号", "概念术语"]:
    sub = [r for r in rows if r["kind"] == k]
    sub.sort(key=lambda r: -r["n"])
    fix = [r for r in sub if r["cand"]]
    print(f"\n### {k}  共 {len(sub)}  有候选 {len(fix)}  无候选 {len(sub)-len(fix)}")
    for r in sub:
        flag = "✔" if r["cand"] else " "
        print(f" {flag} [{r['n']:2d}] {r['t']}")
        if r["cand"]:
            print(f"        → {r['cand']}   ({r['how']})")
        print(f"        ← {r['src'][0]}")
