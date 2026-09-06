#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_kb_phase2_map.py — 幽灵知识点映射表生成（先审核，后执行）

输入：04-题库/05-真题库 题目类 frontmatter 中无法解析的 [[KP]]
输出：09-审计报告/2026-08-31-知识点缺口映射表.md（供人工审核）

分类：
  A. 高频(≥3次)——人工逐条判定
  B. 一次性(1-2次)——词面相似度匹配（阈值 0.5，且须显著高于次优）
  C. 无可靠目标——建议删除该标签（前提：删除后仍有其他 KP）
  D. 删除后无 KP 可用——保持原样并标记人工处理

本脚本只生成报告，不修改任何题库文件。执行用 fix_kb_phase2_apply.py。
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_kb as VKB

V = VKB.VAULT_ROOT
OUT = V / "09-审计报告" / "2026-08-31-知识点缺口映射表.md"
QT = {"题目", "真题", "例题", "题组", "题目集"}
SKIP = {".obsidian", "node_modules", "09-AI工作区"}
FIELDS = ("knowledge_points", "depends_on", "cross_references", "related")

# ── A. 高频名人工映射（≥3 次，58 名）──────────────────────────
# 语义必须成立；无对应 KP 的技能型/泛化标签进 DELETE_SET
CURATED: dict[str, str] = {
    # s区/碱金属（Ch12 批量标签簇的逐名归宿）
    "BeCl2导电性": "铍化学",
    "BeCl2成键": "铍化学",
    "锂镁相似性": "对角线规则",
    "铍铝相似性": "对角线规则",
    "钾的制备": "单质制备方法",
    "炼镁冷却剂": "单质制备方法",
    "卤化物生成热": "晶格能",
    "镁溶解性": "镁",
    "黑火药": "碱金属",
    "过氧化钠": "碱金属",
    # 水溶液平衡
    "盐类水解": "酸碱平衡",
    "水解反应": "酸碱平衡",
    "沉淀平衡": "沉淀溶解平衡",
    "溶解度比较": "溶解度",
    # 化学平衡 / 电化学
    "平衡转化率": "化学平衡计算",
    "标准电动势": "标准电极电势",
    "半反应": "电极",
    # 分析化学
    "分配定律": "萃取",
    "配位效应": "副反应系数",
    # 结构与配位
    "十八电子规则": "18电子规则",
    "σ-π配键": "反馈π键",
    "杂化方式": "杂化轨道理论",
    "内轨型": "配合物杂化轨道理论",
    "外轨型": "配合物杂化轨道理论",
    "平面四边形": "配合物几何构型",
    "空间利用率": "等径球堆积",
    "价层电子": "VSEPR理论",
    # 原子结构 / 量子
    "电子跃迁": "原子光谱与光谱项",
    "电子能量": "Bohr模型计算",
    "光子能量": "Bohr模型计算",
    "德布罗意波": "原子轨道与波函数",
    "本征函数": "原子轨道与波函数",
    "态叠加原理": "箱中粒子模型",
    "EPR": "顺磁性",
    "未成对电子": "顺磁性",
    # 元素与表征
    "化学式推导": "化学式推断",
    "矿物化学式": "化学式推断",
    "化合物颜色": "过渡元素颜色与配位行为",
    "离子颜色": "过渡元素颜色与配位行为",
    "颜色变化": "过渡元素颜色与配位行为",
    "X射线光电子能谱": "异构与结构表征",
    "工业制备流程": "单质制备方法",
    "α衰变": "核反应",
    "β衰变": "核反应",
}

# 技能型/泛化标签：不是知识点，删除
DELETE_SET = {
    "综合分析", "逻辑推理", "数学方法", "化学反应原理",
    "实验现象解释", "实验现象", "物质合成", "稳定性",
    "分离", "鉴别", "物质鉴别", "离子分离",
}

# Ch12 复制粘贴簇：按题名重派（文件名 → 应保留的 KP，映射后落点）
CH12_REASSIGN = {
    "12.35-12.45-简答题": ["BeCl2导电性", "BeCl2成键", "锂镁相似性", "铍铝相似性",
                        "钾的制备", "炼镁冷却剂", "黑火药", "卤化物生成热", "镁溶解性"],
    "12.35-BeCl2熔盐导电": ["BeCl2导电性"],
    "12.36-钾的制备": ["钾的制备"],
    "12.37-锂的特殊性": ["锂镁相似性"],
    "12.38-锂镁相似性": ["锂镁相似性"],
    "12.39-铍铝相似性": ["铍铝相似性"],
    "12.40-黑火药用KNO3": ["黑火药"],
    "12.41-卤化物生成热": ["卤化物生成热"],
    "12.42-镁溶于氯化铵": ["镁溶解性"],
    "12.43-BeCl2成键与构型": ["BeCl2成键"],
    "12.44-炼镁冷却剂": ["炼镁冷却剂"],
    "12.45-混合物成分判断": ["焰色反应"],
}

# 陈旧 cross_references
STALE_XREF = {
    "题-汇智-分子结构-36": None,  # 文件不存在（34/35/37 在，36 缺号）→ 删除该引用
    "题-011-初赛讲义-分子结构-习题3.44": "题-001-初赛讲义-分子结构-习题3.44",
}


def strip_fm(t: str):
    t = t.lstrip("\ufeff")
    if t.startswith("---"):
        e = t.find("\n---", 3)
        if e > 0:
            try:
                m = yaml.safe_load(t[3:e])
                return (m if isinstance(m, dict) else {}), t[e + 4:]
            except Exception:
                return {}, t[e + 4:]
    return {}, t


def bigrams(s: str) -> set[str]:
    s = re.sub(r"[\s\-·]", "", s)
    return {s[i:i + 2] for i in range(len(s) - 1)} or {s}


def sim(a: str, b: str) -> float:
    A, B = bigrams(a), bigrams(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def main() -> None:
    # KP 宇宙
    kp_stems: set[str] = set()
    kp_labels: dict[str, set[str]] = defaultdict(set)   # label → stems
    for f in (V / "03-知识点").rglob("*.md"):
        fm, _ = strip_fm(f.read_text(encoding="utf-8", errors="replace"))
        if str(fm.get("status", "")).strip() in ("deprecated", "已废弃", "重定向", "已合并"):
            continue
        kp_stems.add(f.stem)
        kp_labels[f.stem].add(f.stem)
        for fld in ("title", "aliases"):
            v = fm.get(fld)
            vals = [v] if isinstance(v, str) else (v if isinstance(v, list) else [])
            for x in vals:
                if str(x).strip():
                    kp_labels[f.stem].add(str(x).strip())

    # 收集真断链
    phantom = Counter()          # name → 次数
    holders = defaultdict(list)  # name → [文件]
    for d in ["04-题库", "05-真题库"]:
        for f in (V / d).rglob("*.md"):
            if set(f.relative_to(V).parts) & SKIP:
                continue
            fm, _ = strip_fm(f.read_text(encoding="utf-8", errors="replace"))
            if str(fm.get("type", "")).strip() not in QT:
                continue
            for fld in FIELDS:
                v = fm.get(fld)
                if isinstance(v, str):
                    v = [v]
                if not isinstance(v, list):
                    continue
                for item in v:
                    if not isinstance(item, str):
                        continue
                    for t in re.findall(r"\[\[([^\]|#]+)", item):
                        t = t.strip()
                        if not t:
                            continue
                        n = VKB.normalize_wikilink_target(t)
                        if not n or VKB.is_placeholder_target(n):
                            continue
                        if VKB.find_wikilink_target(n, V) is None:
                            phantom[t] += 1
                            holders[t].append(f)

    mapped: dict[str, str] = {}
    deleted: set[str] = set()
    unmatched: dict[str, int] = {}

    for name, cnt in phantom.items():
        if name in CURATED:
            mapped[name] = CURATED[name]
        elif name in DELETE_SET:
            deleted.add(name)
        elif cnt >= 3:
            unmatched[name] = cnt   # 高频但未判定 → 人工区
        else:
            # B：词面匹配（须显著优于次优）
            scored = []
            for stem, labels in kp_labels.items():
                s = max(sim(name, x) for x in labels)
                if s > 0:
                    scored.append((s, stem))
            scored.sort(reverse=True)
            if scored and scored[0][0] >= 0.5 and (len(scored) == 1 or scored[0][0] - scored[1][0] >= 0.12):
                mapped[name] = scored[0][1]
            else:
                unmatched[name] = cnt

    # ── 写报告 ──
    lines = ["# 知识点缺口映射表（待审核）", ""]
    lines.append("> 生成：fix_kb_phase2_map.py · 审核通过后由 fix_kb_phase2_apply.py 执行")
    lines.append(f"> 断链总数：{sum(phantom.values())} 处 / {len(phantom)} 个唯一名")
    lines.append("")
    lines.append("| 类别 | 名称数 | 涉及链接数 | 处置 |")
    lines.append("|:--|--:|--:|:--|")
    lines.append(f"| A 人工映射（高频/白名单） | {len(mapped)} | {sum(phantom[n] for n in mapped)} | 改写到指定 KP |")
    lines.append(f"| B 词面自动匹配（一次性） | {len([n for n in mapped if n not in CURATED])} | {sum(phantom[n] for n in mapped if n not in CURATED)} | 改写到词面最近 KP |")
    lines.append(f"| C 技能型标签删除 | {len(deleted)} | {sum(phantom[n] for n in deleted)} | 删除该 KP 条目 |")
    lines.append(f"| D 无可靠目标 | {len(unmatched)} | {sum(unmatched.values()) | 0} | 删除（若仍有其他 KP）/ 保留待人工 |")
    lines.append("")

    lines.append("## A+B 映射明细")
    lines.append("")
    lines.append("| 幽灵名 | 次数 | 落点 KP | 依据 |")
    lines.append("|:--|--:|:--|:--|")
    for name in sorted(mapped, key=lambda n: -phantom[n]):
        basis = "人工判定" if name in CURATED else "词面匹配"
        lines.append(f"| {name} | {phantom[name]} | [[{mapped[name]}]] | {basis} |")
    lines.append("")

    lines.append("## C 删除清单（技能型标签，非知识点）")
    lines.append("")
    lines.append("、".join(sorted(deleted)))
    lines.append("")

    lines.append("## D 未处理清单")
    lines.append("")
    for name, cnt in sorted(unmatched.items(), key=lambda x: -x[1]):
        lines.append(f"- {name}（{cnt} 次）")
    lines.append("")

    lines.append("## E 陈旧 cross_references")
    lines.append("")
    lines.append("| 引用目标 | 处置 |")
    lines.append("|:--|:--|")
    for k, v in STALE_XREF.items():
        lines.append(f"| [[{k}]] | {'改指 ' + v if v else '删除（目标文件不存在，34/35/37 在、36 缺号）'} |")
    lines.append("")

    lines.append("## F Ch12 复制粘贴簇重派（12 文件）")
    lines.append("")
    lines.append("Ch12 的 12 道题被批量复制了同一组 9 个 KP，按题名重派：")
    lines.append("")
    lines.append("| 文件 | 保留 KP（映射后） |")
    lines.append("|:--|:--|")
    for stem, kps in CH12_REASSIGN.items():
        dest = [CURATED.get(k, k) for k in kps]
        lines.append(f"| {stem} | {'、'.join(dest)} |")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")

    # 缓存供执行脚本用
    cache = {
        "mapped": mapped, "deleted": sorted(deleted), "unmatched": unmatched,
        "ch12": CH12_REASSIGN, "stale_xref": STALE_XREF,
        "phantom": dict(phantom),
    }
    (V / "09-审计报告" / "缓存-知识点映射.json").write_text(
        json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"断链 {sum(phantom.values())} 处 / {len(phantom)} 名")
    print(f"A+B 映射 {len(mapped)} 名（覆盖 {sum(phantom[n] for n in mapped)} 处）")
    print(f"C 删除 {len(deleted)} 名（{sum(phantom[n] for n in deleted)} 处）")
    print(f"D 未处理 {len(unmatched)} 名（{sum(unmatched.values())} 处）")
    print(f"📄 {OUT}")


if __name__ == "__main__":
    main()
