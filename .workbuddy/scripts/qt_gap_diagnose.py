#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
question_type 缺口诊断（B6 Task #12）。

背景：infer_question_type.py 跑完 dry-run 后，剩余 2,970 条里
T1/T2 命中数为 **0** —— 现有规则一条都补不了。三档构成：

  推断-无信号      1727   正则完全没命中
  推断-多小问跳过   701   一题多问且各问不同质
  推断-T3          542    只有弱兜底信号（规则规定不写）

本脚本回答一个问题：**这三档分别是"真的判不出来"还是"规则太窄"？**

诊断手段（只读，不写任何文件）：
  A. 对「无信号」档扫一遍宽泛动词表，统计哪些高频指令动词**未**被现有规则覆盖
  B. 对「无信号」档抽出"疑问尾部"（最后 ~70 字），按目录分组抽样，人眼看得出题型
  C. 对「多小问」档逐段推断，统计各段落空/落在 T3 的比例，判断是"真综合"还是"切段失败"
  D. 三档的目录分布，用于判断是否适合按目录批量补

用法：
  python qt_gap_diagnose.py                      # 全量诊断
  python qt_gap_diagnose.py --verbs 40           # 动词表 Top N
  python qt_gap_diagnose.py --samples 8          # 每目录抽样条数
  python qt_gap_diagnose.py --dump gap.txt       # 落盘细看
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
sys.path.insert(0, str(VAULT / ".workbuddy" / "scripts"))
sys.path.insert(0, str(VAULT / "11-模板" / "scripts"))
import validate_kb as V          # noqa: E402
import infer_question_type as IQ  # noqa: E402

TARGET_DIRS = ["04-题库", "05-真题库"]

# ── A. 宽泛动词表（仅用于诊断，不是推断规则）─────────────────────
# 覆盖化学题里所有常见指令动词。目的是找出「高频出现但现有规则未覆盖」的那些。
DIAG_VERBS = [
    # 计算类
    "计算", "试求", "求算", "推算", "估算", "估计", "求", "算出", "算得",
    "多少", "几个", "几克", "几摩尔",
    # 推断/判断类
    "推断", "推测", "判断", "确定", "识别", "鉴别", "检验", "猜想", "指认",
    # 书写/回答类
    "写出", "画出", "作出", "绘制", "配平", "完成", "补全", "举例", "列举",
    "命名", "排序", "排列", "预测", "指出", "标明", "标注",
    # 解释类
    "说明", "解释", "简述", "叙述", "描述", "比较", "对比", "讨论", "分析",
    "评价", "论证", "证明", "推导", "为什么", "为何", "怎样", "如何",
    # 综合类
    "设计", "合成", "制备", "分离", "提纯", "鉴定",
]
VERB_RE = re.compile("|".join(sorted((re.escape(v) for v in DIAG_VERBS), key=len, reverse=True)))

# 现有规则已覆盖的动词（来自 infer_question_type.RULES + CALC_VERB）
COVERED_VERBS = {
    "计算", "试求", "求算", "推算", "估算", "求", "算出", "算得",
    "推断", "判断", "写出", "画出", "作出", "绘制", "配平", "完成",
    "说明", "解释", "简述", "比较", "讨论", "鉴别", "为什么", "为何", "怎样", "如何",
}


def dir_group(rel: str) -> str:
    """取到二级目录，用于分组。04-题库/化学原理/Ch02-气体/02-01.md -> 化学原理/Ch02-气体"""
    parts = rel.split("/")
    return "/".join(parts[1:3]) if len(parts) > 3 else "/".join(parts[1:])


def tail_of(stem: str, n: int = 90) -> str:
    """疑问尾部：题目真正的提问通常在最后。去空白后取末 n 字。"""
    s = re.sub(r"\s+", " ", stem).strip()
    return s[-n:] if len(s) > n else s


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbs", type=int, default=30, help="动词表输出 Top N")
    ap.add_argument("--samples", type=int, default=6, help="每目录抽样条数")
    ap.add_argument("--dump", default="", help="落盘路径")
    args = ap.parse_args()

    files: list[Path] = []
    for d in TARGET_DIRS:
        files.extend(sorted((VAULT / d).rglob("*.md")))
    files = [p for p in files if p.name not in V.EXCLUDE_FILE_NAMES]

    buckets: dict[str, list] = {"无信号": [], "T3": [], "多问": []}
    verb_all: Counter = Counter()
    verb_by_bucket: dict[str, Counter] = defaultdict(Counter)
    noun_miss: Counter = Counter()

    print(f"扫描 {len(files)} 个文件…")
    for p in files:
        try:
            text = IQ.read_raw(p)
            fs, fe, lines = IQ.split_fm(text)
            if fs is None:
                continue
            import yaml
            try:
                fm = yaml.safe_load("\n".join(lines[fs + 1:fe])) or {}
            except Exception:
                continue
            if not isinstance(fm, dict):
                continue
            if str(fm.get("type", "")).strip() not in ("题目", "真题"):
                continue
            if fm.get("question_type") is not None:
                continue

            rel = p.relative_to(VAULT).as_posix()
            stem = IQ.stem_of(text)
            tier, types, evs = IQ.infer(stem)

            if tier is None:
                key = "无信号"
            elif tier != "T1" and IQ.is_multi(stem):
                _, m_types, _ = IQ.infer_multi(stem)
                key = "多问" if not m_types else "?"     # 能定多问同质的不会到这里
            else:
                key = "T3"

            for m in VERB_RE.finditer(stem):
                v = m.group(0)
                verb_all[v] += 1
                verb_by_bucket[key][v] += 1

            buckets[key].append((rel, dir_group(rel), stem, types, evs))
        except Exception as e:
            print(f"  !! {p.name}: {type(e).__name__}: {e}")

    out: list[str] = []
    total = sum(len(v) for v in buckets.values())

    print(f"\n缺 question_type 共 {total} 条，分档：")
    for k in ("无信号", "多问", "T3"):
        print(f"  {k:8s} {len(buckets[k]):5d}  ({len(buckets[k])/total*100:.1f}%)")

    # ── A. 动词频率 ──
    print(f"\n═══ A. 指令动词频率 Top {args.verbs}（★ = 现有规则未覆盖）═══")
    hdr = f"  {'动词':<8s} {'总计':>6s} {'无信号':>7s} {'多问':>6s} {'T3':>5s}"
    print(hdr)
    out.append(hdr)
    for v, n in verb_all.most_common(args.verbs):
        mark = "★" if v not in COVERED_VERBS else " "
        row = (f" {mark}{v:<7s} {n:>6d} {verb_by_bucket['无信号'][v]:>7d} "
               f"{verb_by_bucket['多问'][v]:>6d} {verb_by_bucket['T3'][v]:>5d}")
        print(row)
        out.append(row)

    # ── B. 按目录分布 ──
    print("\n═══ B. 目录分布（Top 20，按缺口总数）═══")
    by_dir: Counter = Counter()
    dir_tier: dict[str, Counter] = defaultdict(Counter)
    for k, items in buckets.items():
        for _, g, _, _, _ in items:
            by_dir[g] += 1
            dir_tier[g][k] += 1
    hdr2 = f"  {'目录':<44s} {'缺口':>5s} {'无信号':>7s} {'多问':>5s} {'T3':>4s}"
    print(hdr2)
    out.append(hdr2)
    for g, n in by_dir.most_common(20):
        d = dir_tier[g]
        row = f"  {g:<44s} {n:>5d} {d['无信号']:>7d} {d['多问']:>5d} {d['T3']:>4d}"
        print(row)
        out.append(row)

    # ── C. 多问档：逐段诊断 ──
    print("\n═══ C. 多问档：切段与段落命中情况 ═══")
    seg_stat: Counter = Counter()
    for rel, g, stem, _, _ in buckets["多问"]:
        segs = IQ.split_subq(stem)
        if len(segs) < 3:
            seg_stat["切不出≥3段"] += 1
            continue
        blanks, t3s, oks = 0, 0, 0
        for s in segs:
            t, _, _ = IQ.infer(s)
            if t is None:
                blanks += 1
            elif t == "T3":
                t3s += 1
            else:
                oks += 1
        if blanks == 0 and t3s == 0:
            seg_stat["全段命中（被并集>2拦下）"] += 1
        elif oks == 0:
            seg_stat["全段落空"] += 1
        else:
            seg_stat[f"部分命中(空{blanks}/兜底{t3s}/中{oks})"] += 1
    for k, n in seg_stat.most_common(12):
        print(f"  {k:<32s} {n}")
        out.append(f"  {k:<32s} {n}")

    # ── D. 每目录抽样（疑问尾部）──
    print("\n═══ D. 按目录抽样：疑问尾部（人眼判断题型）═══")
    by_dir_items: dict[str, list] = defaultdict(list)
    for k, items in buckets.items():
        for rel, g, stem, types, evs in items:
            by_dir_items[g].append((k, rel, stem))
    for g, _ in by_dir.most_common(10):
        items = by_dir_items[g]
        hdr3 = f"\n--- {g}（缺口 {len(items)} 条，抽样 {min(args.samples, len(items))}）---"
        print(hdr3)
        out.append(hdr3)
        step = max(1, len(items) // args.samples)
        for k, rel, stem in items[::step][: args.samples]:
            line = f"  [{k}] {Path(rel).stem[:28]}\n       …{tail_of(stem)}"
            print(line)
            out.append(line)

    if args.dump:
        Path(args.dump).write_text("\n".join(out), encoding="utf-8", newline="")
        print(f"\n诊断明细已写入：{args.dump}")


if __name__ == "__main__":
    main()
