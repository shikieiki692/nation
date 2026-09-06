# -*- coding: utf-8 -*-
"""validate_kb 新增层级漂移检查的功能自测（只读 + 内存模拟，不改任何文件）。

1. 复用 validate_kb 收集 04-题库/05-真题库 语料，走 record_tl_bucket 真实路径
2. 断言记录数与预期同量级（04-题库 二级目录下有 teaching_level 的题目/真题）
3. 断言真实数据告警 = 0（经典例题/基础 已豁免）
4. 人工注入假孤例（化学原理/竞赛）断言告警触发且文案正确
"""
import sys

sys.path.insert(0, r"C:\Obsidion\妙妙屋\11-模板\scripts")
import validate_kb as V  # noqa: E402

report = V.Report()
files = V.collect_md_files(V.VAULT_ROOT, ["04-题库", "05-真题库"])
for f in files:
    text = f.read_text(encoding="utf-8", errors="replace")
    fm, _body = V.parse_frontmatter(text)
    rel = f.relative_to(V.VAULT_ROOT).as_posix()
    V.record_tl_bucket(f, rel, fm)

print(f"语料 md: {len(files)}，层级记录: {len(V.TL_RECORDS)}")
buckets = {}
for _rel, b, lv in V.TL_RECORDS:
    buckets.setdefault(b, {}).setdefault(lv, 0)
    buckets[b][lv] += 1
for b in sorted(buckets):
    print(f"  {b}: {dict(sorted(buckets[b].items()))}")

r1 = V.Report()
V.check_teaching_level_drift(r1)
print(f"\n真实数据告警: {len(r1.warnings)}（应 0）")
for w in r1.warnings:
    print(f"  !! {w}")
assert len(r1.warnings) == 0, "真实数据不应有漂移告警"

V.TL_RECORDS.append(("04-题库/化学原理/Ch01-假-测试题.md", "化学原理", "竞赛"))
r2 = V.Report()
V.check_teaching_level_drift(r2)
print(f"注入假孤例后告警: {len(r2.warnings)}（应 1）")
for w in r2.warnings:
    print(f"  -> {w[0]} | {w[1]} | {w[2][:50]}...")
assert len(r2.warnings) == 1 and r2.warnings[0][1] == "层级-目录漂移"

print("\n全部断言通过：检查路径真实生效且基线 0 告警。")
