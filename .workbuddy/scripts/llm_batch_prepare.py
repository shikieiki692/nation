#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 语义补全 · 放量准备器（只读题目文件）
1) 全量无信号档 → 排除题组关联（stem 含「完整题干」等）与题面缺失（stem < 60 字符）
2) 剥图片链接为［图］占位、截 500 字 → 生成 4 批输入文件（蛇形分配，大小源混批）
输出：
  _llm_batch_meta.json      id → rel/group/batch（含排除清单）
  _llm_batch{1..4}_input.txt   子代理判定输入
  _llm_all_files.txt        全量待写文件清单（qt_write_guard snapshot 用）
  _llm_dataquality.txt      排除清单（数据质量问题，另行修源）
"""
import sys
import json
import re
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
import infer_question_type as IQ  # noqa: E402
import yaml  # noqa: E402

N_BATCH = 4
IMG_RE = re.compile(r"!\[\[[^\]]*\]\]")
ZK_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
SC = Path(__file__).parent


def main() -> None:
    files = []
    for d in ("04-题库", "05-真题库"):
        files.extend((IQ.VAULT / d).rglob("*.md"))
    files.sort()

    pool, excluded_dq = [], []
    for p in files:
        text = IQ.read_raw(p)
        fs, fe, lines = IQ.split_fm(text)
        if fs is None:
            continue
        try:
            fm = yaml.safe_load("\n".join(lines[fs + 1:fe])) or {}
        except Exception:
            continue
        if not isinstance(fm, dict) or str(fm.get("type", "")).strip() not in ("题目", "真题"):
            continue
        if fm.get("question_type") is not None:
            continue
        stem = IQ.stem_of(text)
        tier, types, evs = IQ.infer(stem)
        if tier is not None:
            continue
        rel = p.relative_to(IQ.VAULT).as_posix()
        # 题组关联与短/空题面不再机械排除（60 字阈值曾误杀合法短题），
        # 全部交给 LLM 按试点口径留空并注明原因，事后从 verdicts 筛数据质量清单。
        clean = ZK_RE.sub("［图］", IMG_RE.sub("［图］", stem)).strip()
        if not clean:
            excluded_dq.append((rel, "stem 为空"))
            continue
        parts = rel.split("/")
        group = "/".join(parts[:3]) if len(parts) >= 3 else rel
        pool.append({"rel": rel, "group": group, "stem": clean[:500]})

    print(f"无信号档可判: {len(pool)}；排除数据质量: {len(excluded_dq)}")

    # 蛇形分配：组按大小降序，轮流放入 4 批（批内再按 id 稳定排序）
    by_group = defaultdict(list)
    for it in pool:
        by_group[it["group"]].append(it)
    groups_sorted = sorted(by_group, key=lambda g: (-len(by_group[g]), g))
    batches = [[] for _ in range(N_BATCH)]
    order = list(range(N_BATCH))
    for gi, g in enumerate(groups_sorted):
        items = sorted(by_group[g], key=lambda x: x["rel"])
        seq = order if gi % 2 == 0 else order[::-1]
        for j, it in enumerate(items):
            batches[seq[j % N_BATCH]].append(it)

    meta = {"n_pool": len(pool), "n_excluded": len(excluded_dq), "batches": N_BATCH, "items": []}
    all_rels = []
    for b, items in enumerate(batches, 1):
        items.sort(key=lambda x: x["rel"])
        with (SC / f"_llm_batch{b}_input.txt").open("w", encoding="utf-8", newline="\n") as f:
            for it in items:
                f.write(f"===== [#{it['rel']}] =====\n")
                f.write(it["stem"] + "\n\n")
        (SC / f"_llm_all_files.txt").open("a" if b > 1 else "w", encoding="utf-8", newline="\n") \
            .write("\n".join(it["rel"] for it in items) + "\n")
        for it in items:
            meta["items"].append({"batch": b, "rel": it["rel"], "group": it["group"]})
        all_rels.extend(it["rel"] for it in items)
        print(f"批 {b}: {len(items)} 条")
    meta["items"].sort(key=lambda x: (x["batch"], x["rel"]))
    (SC / "_llm_batch_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    (SC / "_llm_dataquality.txt").write_text(
        "\n".join(f"{r}\t{w}" for r, w in sorted(excluded_dq)), encoding="utf-8")
    print(f"共 {len(all_rels)} 条待判 / 排除 {len(excluded_dq)} 条 → _llm_batch_meta.json")


if __name__ == "__main__":
    main()
