# -*- coding: utf-8 -*-
"""
真断链清单 v5 —— 直接复用校验器自身逻辑（口径 100% 对齐）

教训：自己重扫全库 md 会得到 33,392 条"断链"，因为
  - 校验器只扫 INCLUDE_DIRS 的【正文】，frontmatter 单独归到 断链-frontmatter
  - 校验器排除 09-审计报告 / 06-外部资料导入 / 00-首页 / .obsidian 等
  - 校验器跳过模板占位符、图片按 basename 解析、目录链接视为有效
结论：不要自己重写正则，直接 import validate_kb 复用 scan_file。

输出：按目标聚合的真断链清单 + 分类 + 每个目标的真实引用来源文件。
"""
import sys, os, re, json, collections

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

import validate_kb as V  # noqa: E402

files = V.collect_md_files(V.VAULT_ROOT, V.INCLUDE_DIRS)
print(f"受检文件（校验器口径）：{len(files)}")

report = V.Report()
for f in files:
    if not f.exists() or not f.is_file():
        continue
    try:
        V.scan_file(f, report, quick=False)
    except Exception as e:
        print(f"  !! {f.name}: {e}")

print(f"Error {len(report.errors)} / Warning {len(report.warnings)}")

# 只取正文断链
brk = [(f, d) for f, c, d in report.warnings if c == "断链"]
print(f"正文断链条数：{len(brk)}")

TGT = re.compile(r"\[\[(.+?)\]\] → 文件不存在")
agg = collections.defaultdict(list)
for f, d in brk:
    m = TGT.match(d)
    if m:
        agg[m.group(1)].append(f)

print(f"unique 目标：{len(agg)}")


def kind(t: str) -> str:
    if re.match(r"^题-\d+", t):
        return "题号"
    if "/" in t:
        return "带路径"
    if re.search(r"\.(jpg|png|jpeg|gif|webp|svg)$", t, re.I):
        return "图片"
    return "概念术语"


by_kind = collections.Counter(kind(t) for t in agg)
print("\n按类型：")
for k, n in by_kind.most_common():
    print(f"  {k:8s} {n}")

# v4 的 10 条候选目标
v4 = [
    "题-036b-1-1-铝铁合金制备方程式",
]
print("\n--- v4 候选 10 条是否在此清单里 ---")
v4json = os.path.join(VAULT, ".workbuddy", "scripts", "fix_body_redlinks_v4.json")
if os.path.exists(v4json):
    with open(v4json, encoding="utf-8") as fh:
        data = json.load(fh)
    cands = data if isinstance(data, list) else data.get("collapsible", data.get("plan", []))
    if cands and isinstance(cands[0], (list, tuple)):
        cands = [c[0] for c in cands]
    for c in cands:
        hits = agg.get(c, [])
        print(f"  {'✅在' if hits else '❌不在'}  {c}   ({len(hits)} 处引用)")
        for h in hits[:3]:
            print(f"        ← {h}")

out = {
    "files_checked": len(files),
    "errors": len(report.errors),
    "warnings": len(report.warnings),
    "broken_total": len(brk),
    "broken_unique": len(agg),
    "targets": {t: {"kind": kind(t), "n": len(v), "src": sorted(set(v))}
                for t, v in sorted(agg.items(), key=lambda kv: (-len(kv[1]), kv[0]))},
}
op = os.path.join(VAULT, ".workbuddy", "scripts", "broken_links_v5.json")
with open(op, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print(f"\n已写出 {op}")

print("\n--- 引用次数 Top 30 断链 ---")
for t, v in sorted(agg.items(), key=lambda kv: -len(kv[1]))[:30]:
    print(f"  {len(v):4d}  [{kind(t)}]  {t}")
    print(f"        例: {v[0]}")
