#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
按推断出的题型标签分组抽样，供人工核验精度。

复用 infer_question_type 的扫描/推断逻辑，只做「看」，不做「写」。
输出：每个标签抽 N 条，带触发证据 + 题干前 160 字。
"""
import sys
import random
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import infer_question_type as Q  # noqa: E402

PER_LABEL = int(sys.argv[1]) if len(sys.argv) > 1 else 25
SEED = 20260902


def main() -> None:
    files: list[Path] = []
    for d in Q.TARGET_DIRS:
        files.extend(sorted((Q.VAULT / d).rglob("*.md")))
    files = [p for p in files if p.name not in Q.V.EXCLUDE_FILE_NAMES]

    buckets: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    rng = random.Random(SEED)

    import yaml

    for p in files:
        text = Q.read_raw(p)
        fs, fe, lines = Q.split_fm(text)
        if fs is None:
            continue
        try:
            fm = yaml.safe_load("\n".join(lines[fs + 1:fe])) or {}
        except Exception:
            continue
        if not isinstance(fm, dict):
            continue
        if str(fm.get("type", "")).strip() != "题目":
            continue
        if fm.get("question_type") is not None:
            continue  # 已有标注的跳过，只看推断出来的
        stem = Q.stem_of(text)
        tier, types, evs = Q.infer(stem)
        if not types:
            continue
        if tier != "T1" and Q.is_multi(stem):
            # 与主脚本一致：先试同质多问，失败才跳过
            m_tier, m_types, m_evs = Q.infer_multi(stem)
            if not m_types:
                continue
            tier, types, evs = m_tier, m_types, m_evs
        label = "+".join(types)
        rel = p.relative_to(Q.VAULT).as_posix()
        item = (rel, " | ".join(evs), stem.replace("\n", " ")[:160])
        # 水库抽样
        b = buckets[label]
        if len(b) < PER_LABEL:
            b.append(item)
        else:
            j = rng.randrange(len(b) + 1)
            if j < PER_LABEL:
                b[j] = item

    out: list[str] = []
    order = sorted(buckets, key=lambda k: -len(buckets[k]))
    # 统计各标签总量（另跑一遍完整计数代价大，这里用抽样近似：略）
    for label in order:
        items = buckets[label]
        out.append(f"\n{'=' * 70}\n标签 [{label}]  抽 {len(items)} 条\n{'=' * 70}")
        for rel, ev, snip in items:
            out.append(f"\n· {rel}")
            out.append(f"  证据: {ev}")
            out.append(f"  题干: {snip}")

    txt = "\n".join(out)
    dst = HERE / "qt_by_label.txt"
    dst.write_text(txt, encoding="utf-8", newline="")
    print(f"已写入 {dst}（{len(txt)} 字符，{len(order)} 个标签）")


if __name__ == "__main__":
    main()
