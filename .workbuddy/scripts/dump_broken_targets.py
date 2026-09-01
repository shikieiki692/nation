"""用校验器自身口径导出当前正文断链：目标 → 引用位置列表。
口径与 validate_kb.py --full 完全一致（复用 collect_md_files + scan_file）。
"""
import os, sys, json, collections, re

VAULT = r"C:\Obsidion\妙妙屋"
sys.path.insert(0, os.path.join(VAULT, "11-模板", "scripts"))
import validate_kb as V

files = V.collect_md_files(V.VAULT_ROOT, V.INCLUDE_DIRS)
report = V.Report()
for f in files:
    V.scan_file(f, report, quick=False)

counts = collections.Counter(c for _, c, _ in report.warnings)
brk = [(f, d) for f, c, d in report.warnings if c == "断链"]
print(f"文件 {len(files)} / Error {len(report.errors)} / Warning {len(report.warnings)}")
print(f"断链 {len(brk)}")
for c, n in counts.most_common(8):
    print(f"   {c}: {n}")

TGT = re.compile(r"\[\[(.+?)\]\] → 文件不存在")
agg = collections.defaultdict(list)
for f, d in brk:
    m = TGT.match(d)
    if m:
        p = f if isinstance(f, str) else f.relative_to(V.VAULT_ROOT).as_posix()
        agg[m.group(1)].append(p.replace("\\", "/"))

out = {"files": len(files), "errors": len(report.errors), "warnings": len(report.warnings),
       "broken": len(brk), "checks": dict(counts),
       "targets": {t: sorted(set(v)) for t, v in
                   sorted(agg.items(), key=lambda kv: (-len(set(kv[1])), kv[0]))}}
json.dump(out, open(os.path.join(VAULT, ".workbuddy", "scripts",
                                 "broken_targets_now.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nunique 目标:", len(agg))
print("已写出 broken_targets_now.json")
