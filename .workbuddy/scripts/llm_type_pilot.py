#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 语义补全试点 · 抽样器（只读，不落盘任何题目文件）
从「无信号档」（question_type 缺失且 infer() 完全无命中）按来源目录分层抽样 ~100 条，
导出题面供 LLM 逐条语义判定。
口径与 infer_question_type.py main() 完全一致（直接复用其 split_fm / stem_of / infer）。

输出：
  _pilot_sample.txt   编号 + 路径 + 题面（截 800 字）——供 LLM 阅读
  _pilot_meta.json    编号 → rel / group 映射——供回填判定与合成报告
"""
import sys
import random
import json
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
import infer_question_type as IQ  # noqa: E402
import yaml  # noqa: E402

SEED = 42
TARGET = 100
OUT_TXT = Path(__file__).parent / "_pilot_sample.txt"
OUT_META = Path(__file__).parent / "_pilot_meta.json"


def main() -> None:
    files = []
    for d in ("04-题库", "05-真题库"):
        files.extend((IQ.VAULT / d).rglob("*.md"))
    files.sort()

    pool = []          # (rel, stem, group)
    n_have = 0
    for p in files:
        text = IQ.read_raw(p)
        fs, fe, lines = IQ.split_fm(text)
        if fs is None:
            continue
        try:
            fm = yaml.safe_load("\n".join(lines[fs + 1:fe])) or {}
        except Exception:
            continue
        if not isinstance(fm, dict):
            continue
        if str(fm.get("type", "")).strip() not in ("题目", "真题"):
            continue
        if fm.get("question_type") is not None:
            n_have += 1
            continue
        stem = IQ.stem_of(text)
        tier, types, evs = IQ.infer(stem)
        if tier is None:
            rel = p.relative_to(IQ.VAULT).as_posix()
            parts = rel.split("/")
            group = "/".join(parts[:3]) if len(parts) >= 3 else rel
            pool.append((rel, stem, group))

    print(f"question_type 已有值: {n_have}")
    print(f"缺失且无信号: {len(pool)}")

    # ── 分层比例配额，每层保底 2 ──
    by_group = defaultdict(list)
    for item in pool:
        by_group[item[2]].append(item)
    rnd = random.Random(SEED)
    quota = {}
    for g, items in by_group.items():
        quota[g] = max(2, round(TARGET * len(items) / len(pool)))
    # 超出 TARGET 时从最大组削减（不低于 2）
    while sum(quota.values()) > TARGET:
        g = max(quota, key=lambda k: quota[k] - (2 if quota[k] > 2 else TARGET))
        if quota[g] <= 2:
            break
        quota[g] -= 1

    sample = []
    for g in sorted(by_group, key=lambda k: -len(by_group[k])):
        items = sorted(by_group[g])
        q = quota[g]
        take = items if len(items) <= q else rnd.sample(items, q)
        sample.extend((rel, stem, g) for rel, stem in ((a, b) for a, b, _ in take))

    print(f"抽样: {len(sample)} 条 / {len(by_group)} 组")
    for g in sorted(by_group, key=lambda k: -len(by_group[k])):
        n = sum(1 for _, _, gg in sample if gg == g)
        print(f"  {g}: {n}/{len(by_group[g])}")

    # ── 导出题面 ──
    meta = []
    with OUT_TXT.open("w", encoding="utf-8", newline="\n") as f:
        for i, (rel, stem, g) in enumerate(sample, 1):
            f.write(f"===== [#{i:03d}] {rel} =====\n")
            f.write(stem[:800].rstrip() + "\n\n")
            meta.append({"id": i, "rel": rel, "group": g})
    OUT_META.write_text(
        json.dumps({"seed": SEED, "pool": len(pool), "sample": meta},
                   ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    print(f"已写出 {OUT_TXT.name} / {OUT_META.name}")


if __name__ == "__main__":
    main()
