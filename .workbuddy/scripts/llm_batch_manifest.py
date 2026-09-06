#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 语义补全放量 · 分批清单生成器（只读，不写任何题目文件）
口径与 llm_type_pilot.py 完全一致（复用 infer_question_type 的 split_fm/stem_of/infer）：
pool = type ∈ {题目,真题} 且 question_type 缺失 且 infer() 零命中（无信号档）。

排除规则（2026-09-02 用户决策 + 当日 clean_stem 盲区发现）：
  1) 题组关联：stem 有行同时含「完整题干」+「请见」→ 排除（题干在父文件，
     实测 3 条全部为「完整题干与解答请见：[[父题]]」，05-真题库）
  2) stem < 20 字符时先复查 clean_stem 切短原因，分三类（盲区发现见当日日志）：
     - 正文有 ## 题目/问题/原题/题干 小节 → 短题干是真实题干，**留在池里**
     - ANS_CUT 出现在正文前 300 字符内 → 答案前置布局（题干在答案区之后），
       clean_stem 被切瞎 → 排除，标记 answer_first（候选 B6.5 修复 + 可能转规则可写）
     - 其余 → 真缺失/仅标题 → 排除；再按有无图片嵌入拆「图片题/真缺失」
"""
import sys
import json
from pathlib import Path
from collections import OrderedDict
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
import infer_question_type as IQ  # noqa: E402
import yaml  # noqa: E402

BATCH_MAX = 300
STEM_MIN = 20
ANS_FIRST_POS = 300
OUT = Path(__file__).parent.parent / "backups" / "llm_batch_manifest.json"


def is_group_link(stem: str) -> bool:
    return any(("完整题干" in ln and "请见" in ln) for ln in stem.splitlines())


def main() -> None:
    files = []
    for d in ("04-题库", "05-真题库"):
        files.extend((IQ.VAULT / d).rglob("*.md"))
    files.sort()

    pool = []              # (rel, group)
    short_real = []        # stem 短但是真实题干（## 问题 小节布局）
    excl_link = []         # 题组关联
    excl_ans_first = []    # 答案前置被切瞎（B6.5 候选）
    excl_image = []        # 真短 + 正文有图片（图片题）
    excl_missing = []      # 真短 + 无图片（修源工单）
    n_have = 0
    n_skip_tier = 0
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
        tier, _types, _evs = IQ.infer(stem)
        if tier is not None:
            n_skip_tier += 1
            continue
        rel = p.relative_to(IQ.VAULT).as_posix()
        parts = rel.split("/")
        group = "/".join(parts[:3]) if len(parts) >= 3 else rel

        if is_group_link(stem):
            excl_link.append(rel)
            continue
        if len(stem.strip()) < STEM_MIN:
            body = "\n".join(lines[fe + 1:]) if fs is not None else text
            if IQ.SECTION_Q.search(body):
                short_real.append(rel)          # 短而真，可判
                pool.append((rel, group))
                continue
            m_ans = IQ.ANS_CUT.search(body)
            if m_ans is not None and m_ans.start() < ANS_FIRST_POS:
                excl_ans_first.append(rel)      # 答案前置切瞎
                continue
            if "![[" in text or "!http" in text or "<img" in text:
                excl_image.append(rel)
            else:
                excl_missing.append(rel)
            continue
        pool.append((rel, group))

    by_group = OrderedDict()
    for rel, g in pool:
        by_group.setdefault(g, []).append(rel)

    batches = []
    cur, cur_groups = [], []
    for g in sorted(by_group, key=lambda k: -len(by_group[k])):
        for rel in sorted(by_group[g]):
            if len(cur) >= BATCH_MAX:
                batches.append({"groups": cur_groups, "files": cur})
                cur, cur_groups = [], []
            cur.append(rel)
            if g not in cur_groups:
                cur_groups.append(g)
    if cur:
        batches.append({"groups": cur_groups, "files": cur})

    manifest = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "note": ("LLM question_type 放量分批清单；口径=llm_type_pilot.py（无信号档）；"
                 "排除=题组关联+题面真缺失/图片题；answer_first=clean_stem 盲区单列（B6.5 候选）"),
        "pool_total": len(pool),
        "n_question_type_present": n_have,
        "n_skip_tier_multimixed_t3": n_skip_tier,
        "n_short_real_stem_kept": len(short_real),
        "short_real_stem": short_real,
        "excluded_group_link": excl_link,
        "excluded_answer_first_blinded": excl_ans_first,
        "excluded_stem_image_only": excl_image,
        "excluded_stem_missing": excl_missing,
        "batch_max": BATCH_MAX,
        "batches": [
            {"id": i + 1, "groups": b["groups"], "count": len(b["files"]), "files": b["files"]}
            for i, b in enumerate(batches)
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"question_type 已有值: {n_have}")
    print(f"多问/T3 跳过档（tier≠None，按设计不入 LLM 池）: {n_skip_tier}")
    print(f"无信号档对账: pool {len(pool)} + 题组关联 {len(excl_link)} + 答案前置 {len(excl_ans_first)}"
          f" + 图片题 {len(excl_image)} + 真缺失 {len(excl_missing)}"
          f" = {len(pool) + len(excl_link) + len(excl_ans_first) + len(excl_image) + len(excl_missing)}"
          f"  (试点基线 1,325)")
    print(f"其中短而真的题干留池: {len(short_real)}")
    for r in short_real:
        print(f"  + {r}")
    print(f"排除-题组关联: {len(excl_link)}")
    for r in excl_link:
        print(f"  - {r}")
    print(f"排除-答案前置被切瞎（B6.5 候选，不进本批）: {len(excl_ans_first)}")
    for r in excl_ans_first:
        print(f"  - {r}")
    print(f"排除-题面过短且为图片题: {len(excl_image)}")
    for r in excl_image:
        print(f"  - {r}")
    print(f"排除-题面过短且真缺失(→修源工单): {len(excl_missing)}")
    for r in excl_missing:
        print(f"  - {r}")
    print(f"分批: {len(batches)} 批 (批上限 {BATCH_MAX})")
    for b in manifest["batches"]:
        gs = "、".join(b["groups"][:3]) + ("…" if len(b["groups"]) > 3 else "")
        print(f"  批{b['id']:>2}: {b['count']:>4} 条 | {gs} | {len(b['groups'])} 组")
    print(f"已写出 {OUT}")


if __name__ == "__main__":
    main()
