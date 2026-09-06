# -*- coding: utf-8 -*-
"""习题书覆盖率核查（只读）。

对 04-题库 + 05-真题库 全部题目逐题标注：入书 / 未入书原因。
  入书 = pack=模块习题集 且分类命中（习题书实际收录口径）
  未入书原因 = 章节练习层 / 综合模拟卷 / 预赛专项 / pack缺失 / deprecated /
               待分类 / 缺口题 / 真题库层(05) / 非四模块
并筛"补入候选"：章节练习层中 difficulty≥4、考纲相关、分类可命中的题
（宁缺毋滥，走 04-题库/README.md 新题分层入库制提升）。

输出：09-审计报告/<日期>-覆盖率核查清单.md
      07-资料提炼/习题书-补入候选.json（promote_questions.py 输入）
运行：系统 Python 3.12（需 PyYAML），vault 根目录。
"""
import io
import json
import re
import sys
import collections
from pathlib import Path

if not (getattr(sys.stdout, "encoding", "") == "utf-8"
        and getattr(sys.stdout, "errors", "") == "replace"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, "11-模板/scripts")
import build_module_book as B  # noqa: E402
import audit_book_quality as Q  # noqa: E402  （复用考纲词表与 syllabus_related）

VAULT = Path(__file__).resolve().parents[2]
REPORT = VAULT / "09-审计报告" / f"{B.TODAY}-覆盖率核查清单.md"
CAND_JSON = VAULT / "07-资料提炼" / "习题书-补入候选.json"

MODULES = [
    ("化学原理", B.CHEM_MAP, None),
    ("有机化学", B.ORGANIC_MAP, B.ORGANIC_EXCLUDE),
    ("元素与分析", B.YSFX_MAP, None),
    ("结构化学", B.STRUCTURE_MAP, None),
]
MAP_BY_MODULE = {m: (cmap, exc) for m, cmap, exc in MODULES}


def parse_fm(s):
    m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
    if not m:
        return None, None
    return m.group(1), m.end()


def main():
    vocab = Q.load_vocab()
    counts = collections.Counter()          # (pack层, subject_module) -> n
    unclassified, candidates = [], []
    inbook_by_mod = collections.Counter()
    src_counter = collections.defaultdict(collections.Counter)

    import os
    for base in ("04-题库", "05-真题库"):
        for root, dirs, fs in os.walk(VAULT / base):
            if "高考" in str(root):
                continue
            for fn in fs:
                if not fn.endswith(".md"):
                    continue
                p = Path(root) / fn
                rel = p.relative_to(VAULT / "04-题库").as_posix() if base == "04-题库" else f"05-真题库/{fn}"
                s = p.read_text(encoding="utf-8", errors="replace")
                y, fm_end = parse_fm(s)
                if y is None:
                    counts[("无frontmatter", "-")] += 1
                    continue
                typ = (re.search(r"(?m)^type: (.*)", y) or [None, ""])[1].strip()
                if typ not in ("题目", "真题", "例题", "题组", "题目集"):
                    counts[("非题目类文件", "-")] += 1
                    continue
                pack = (re.search(r"(?m)^pack: (.*)", y) or [None, ""])[1].strip()
                subj = (re.search(r"(?m)^subject_module: (.*)", y) or [None, ""])[1].strip()
                status = (re.search(r"(?m)^status: (.*)", y) or [None, ""])[1].strip()
                diff = (re.search(r"(?m)^difficulty: (.*)", y) or [None, "3"])[1].strip()
                diff = int(diff) if diff.isdigit() else 3
                fid = (re.search(r"(?m)^fidelity: (.*)", y) or [None, ""])[1].strip()
                src = (re.search(r"(?m)^source: (.*)", y) or [None, ""])[1].strip()
                sub = (re.search(r"(?m)^submodule: (.*)", y) or [None, ""])[1].strip().strip('"')

                if base == "05-真题库" or typ == "真题":
                    counts[("真题库层(05-真题库)", subj or "-")] += 1
                    continue
                if status == "deprecated":
                    counts[("deprecated", subj or "-")] += 1
                    continue

                if pack == "模块习题集" and subj in MAP_BY_MODULE:
                    body = s[fm_end:]
                    item = {"file": fn, "path": rel, "difficulty": diff,
                            "submodule": sub, "module": "", "fidelity": fid,
                            "source": src, "title": "", "kps": B._fm_kps(y), "body": body}
                    exc = MAP_BY_MODULE[subj][1]
                    if sub in set(exc or []):
                        counts[("在书·排除子模块", subj)] += 1
                        continue
                    if B.is_gap_item(item):
                        counts[("在书·缺口题剔除", subj)] += 1
                        continue
                    cmap = MAP_BY_MODULE[subj][0]
                    mod_override = B.PATH_SUBJECT_MODULE_OVERRIDES.get(rel, subj)
                    res = B.classify_by_keywords(item, cmap, mod_override)
                    if res is None:
                        unclassified.append((subj, rel, sub))
                        counts[("在书·待分类(实际不入书)", subj)] += 1
                    else:
                        counts[("在书", subj)] += 1
                        inbook_by_mod[subj] += 1
                        src_counter[subj][src or "（来源未填）"] += 1
                    continue

                # 未入书层
                layer = pack or "pack缺失"
                counts[(f"未入书·{layer}", subj or "-")] += 1
                src_counter[subj or "-"]["未入书·" + layer] += 0  # 不计数仅归位

                # 补入候选：章节练习层 + difficulty≥4 + 非四模块外 + 考纲相关 + 分类可命中
                if pack == "章节练习" and diff >= 4 and subj in MAP_BY_MODULE and status != "deprecated":
                    fm_full = Q.load_full_fm(rel) if base == "04-题库" else {}
                    rel_flag, why = Q.syllabus_related(fm_full, vocab)
                    if not rel_flag:
                        continue
                    body = s[fm_end:]
                    item = {"file": fn, "path": rel, "difficulty": diff,
                            "submodule": sub, "module": "", "fidelity": fid,
                            "source": src, "title": "", "kps": B._fm_kps(y), "body": body}
                    cmap = MAP_BY_MODULE[subj][0]
                    if B.classify_by_keywords(item, cmap, subj) is None:
                        continue
                    candidates.append({
                        "subject_module": subj, "path": rel, "difficulty": diff,
                        "fidelity": fid, "source": src, "submodule": sub,
                        "syllabus": why[:80],
                    })

    # ---- 汇总打印 ----
    total_cls = sum(n for (layer, _), n in counts.items() if layer in
                    ("在书", "在书·缺口题剔除", "在书·待分类(实际不入书)", "在书·排除子模块"))
    print(f"04-题库 题目类文件合计: {sum(n for (l, _), n in counts.items() if l not in ('真题库层(05-真题库)', '非题目类文件', '无frontmatter'))}")
    for (layer, subj), n in sorted(counts.items()):
        print(f"  {layer} | {subj}: {n}")
    print(f"补入候选: {len(candidates)}")

    # ---- 报告 ----
    L = ["---", 'title: "习题书覆盖率核查清单"', "type: 审计报告",
         f"updated: {B.TODAY}", "---", "",
         f"# 习题书覆盖率核查清单（{B.TODAY}）", "",
         f"> 全库题目逐题标注入书/未入书原因。**在书 {inbook_by_mod and sum(inbook_by_mod.values())}** "
         f"题（分类命中）；待分类 {len(unclassified)}；补入候选 {len(candidates)}。", ""]

    L.append("## 一、分层矩阵（层 × 篇）")
    L.append("")
    layers = sorted({l for l, _ in counts})
    mods = ["化学原理", "结构化学", "有机化学", "元素与分析", "-"]
    L.append("| 层 | " + " | ".join(mods) + " | 合计 |")
    L.append("|:--|" + ":--:|" * (len(mods) + 1))
    for layer in layers:
        row = [counts.get((layer, m), 0) for m in mods]
        L.append(f"| {layer} | " + " | ".join(str(x) for x in row) + f" | {sum(row)} |")
    L.append("")

    if unclassified:
        L.append(f"## 二、在书但待分类（{len(unclassified)} 条，实际未入书）")
        L.append("")
        for subj, rel, sub in unclassified:
            L.append(f"- [{subj}] {rel}（submodule={sub or '空'}）")
        L.append("")

    L.append(f"## 三、补入候选（章节练习层 · difficulty≥4 · 考纲相关 · 分类可命中，共 {len(candidates)} 条）")
    L.append("")
    if candidates:
        cand_mod = collections.Counter(c["subject_module"] for c in candidates)
        L.append("分布：" + "、".join(f"{m} {n}" for m, n in cand_mod.most_common()))
        L.append("")
        L.append("| 篇 | 难度 | 保真 | 来源 | 源文件 |")
        L.append("|:--|:--|:--|:--|:--|")
        for c in sorted(candidates, key=lambda c: (c["subject_module"], -c["difficulty"])):
            L.append(f"| {c['subject_module']} | {c['difficulty']} | {c['fidelity'] or '—'} "
                     f"| {c['source'] or '—'} | {c['path']} |")
    else:
        L.append("无（章节练习层的高难度题均不满足考纲相关或分类可命中条件）")
    L.append("")

    L.append("## 四、在书题目来源 TOP（各篇）")
    L.append("")
    for m in ["化学原理", "结构化学", "有机化学", "元素与分析"]:
        top = src_counter[m].most_common(12)
        L.append(f"### {m}")
        L.append("")
        L.append("```")
        for v, n in top:
            L.append(f"{n:>5}  {v}")
        L.append("```")
        L.append("")

    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"报告已写入: {REPORT}")

    CAND_JSON.parent.mkdir(exist_ok=True)
    CAND_JSON.write_text(json.dumps({
        "generated": B.TODAY,
        "note": "习题书补入候选（章节练习层择优）；promote_questions.py 按此批量提升 pack。",
        "total": len(candidates),
        "entries": candidates,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"候选清单已写入: {CAND_JSON}（{len(candidates)} 条）")


if __name__ == "__main__":
    main()
