# -*- coding: utf-8 -*-
"""归档落点引用分诊（只读；不写任何库内文件）

用途：扫全库 md 中引用 `_归档/` 的行，按「文件区域 × 行级规则」分类为 A/B/C/待判。
分类规则：
  C 类 —— 行内含取代标注词（已被本页取代 / superseded_by / 不再维护 / 旧版）
  B 类 —— 行位于 frontmatter 区；或行位于 {#related-lessons} 关系表块
  A 类 —— 含导引词（使用建议 / 前置要求 / 📄 / 落点 …）；或正文表格行
  待判 —— 以上均不命中
自证判据：备课思路/新课大章节-第一轮化学原理.md 应命中 6 处 A 类。
"""
import os
import re
import sys
from collections import defaultdict, OrderedDict

ROOT = r"C:\Obsidion\妙妙屋"
NEEDLE = "_归档/"
OUT = os.path.join(ROOT, ".workbuddy", "tmp", "archived_link_triage_0916.md")

GUIDE_WORDS = [
    "使用建议", "前置要求", "前置讲义", "前置知识", "配套", "📄",
    "落点", "课堂主线", "参考讲义", "教材来源", "使用说明",
]
C_WORDS = ["已被本页取代", "superseded_by", "supersededBy", "不再维护", "旧版"]

REGION_ORDER = ["现役", "红区", "归档自身", "审计", "临时"]
CAT_ORDER = ["A", "B", "C", "D", "待判"]


def region_of(rel):
    p = rel.replace("\\", "/")
    if p.startswith("04-题库/") or p.startswith("05-真题库/"):
        return "红区"
    if p.startswith(".workbuddy/"):
        return "临时"
    if p.startswith("09-审计报告/") or "/历史任务卡/" in p:
        return "审计"
    if ("/_归档/" in p or "/_archive/" in p or "/归档/" in p
            or "/审计归档/" in p or p.startswith("_归档/")):
        return "归档自身"
    return "现役"


def strip_cr(s):
    return s[:-1] if s.endswith("\r") else s


def table_blocks(lines):
    """连续 `|` 行块 -> [(start_idx, end_idx, header_line)]（0-based，闭区间）"""
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        if lines[i].lstrip().startswith("|"):
            j = i
            while j + 1 < n and lines[j + 1].lstrip().startswith("|"):
                j += 1
            blocks.append((i, j, lines[i]))
            i = j + 1
        else:
            i += 1
    return blocks


def classify_line(idx, line, fm_end, blocks, lines):
    if re.search(r"`[^`]*_归档/[^`]*`", line):
        return "D", "反引号内文字提及"
    if "[[" not in line and "![[" not in line:
        return "D", "纯文字提及（无 wikilink）"
    if any(w in line for w in C_WORDS):
        return "C", "含取代标注词"
    if fm_end >= 0 and idx <= fm_end:
        return "B", "位于 frontmatter"
    for (s, e, hdr) in blocks:
        if s <= idx <= e:
            ctx = "\n".join(lines[max(0, s - 3):s + 1])
            if "班型" in ctx and "日期" in ctx:
                return "B", "关系表块(班型/日期)"
            if "落点" in ctx or "教材来源" in ctx or "映射" in ctx:
                return "A", "落点/映射表行"
            if "📄" in ctx:
                return "A", "讲义清单表行"
            return "待判", "正文表格行"
    for w in GUIDE_WORDS:
        if w in line:
            return "A", "含导引词「%s」" % w
    return "待判", "无匹配规则"


def main():
    rows = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", "node_modules", "__pycache__")]
        for fn in filenames:
            if not fn.lower().endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            try:
                with open(full, "r", encoding="utf-8", newline="") as f:
                    content = f.read()
            except Exception as exc:
                print("SKIP %s: %s" % (rel, exc))
                continue
            if NEEDLE not in content:
                continue
            lines = [strip_cr(x) for x in content.split("\n")]
            m = re.match(r"^---\r?\n.*?\r?\n---\r?\n", content, re.S)
            fm_end = (content[:m.end()].count("\n") - 1) if m else -1
            blocks = table_blocks(lines)
            reg = region_of(rel)
            for idx, line in enumerate(lines):
                if NEEDLE not in line:
                    continue
                cat, why = classify_line(idx, line, fm_end, blocks, lines)
                rows.append({
                    "rel": rel, "ln": idx + 1, "cat": cat, "why": why,
                    "reg": reg, "text": line.strip()[:220],
                })

    # ---- 统计 ----
    files_by_reg_cat = defaultdict(set)
    cnt = defaultdict(int)
    for r in rows:
        files_by_reg_cat[(r["reg"], r["cat"])].add(r["rel"])
        cnt[(r["reg"], r["cat"])] += 1

    out = []
    out.append("# 归档落点引用分诊报告（只读）")
    out.append("")
    out.append("> 由 `.workbuddy/tmp/triage_archived_links_0916.py` 生成（脚本须先自证）。")
    out.append("> 判据：C=取代标注 / B=frontmatter或关系表 / A=导引词或正文表格行 / 待判=无匹配。")
    out.append("")
    out.append("## 一、总览（行数 / 文件数）")
    out.append("")
    out.append("| 区域 | " + " | ".join(CAT_ORDER) + " | 合计 |")
    out.append("|:---|" + "---:|" * (len(CAT_ORDER) + 1))
    for reg in REGION_ORDER:
        cells, tot = [], 0
        for cat in CAT_ORDER:
            n = cnt.get((reg, cat), 0)
            f = len(files_by_reg_cat.get((reg, cat), ()))
            cells.append("%d / %d" % (n, f))
            tot += n
        if tot == 0:
            continue
        out.append("| %s | %s | %d |" % (reg, " | ".join(cells), tot))
    out.append("")

    # ---- 现役区明细 ----
    for cat in ["A", "B", "C", "D", "待判"]:
        sel = [r for r in rows if r["reg"] == "现役" and r["cat"] == cat]
        if not sel:
            continue
        byfile = OrderedDict()
        for r in sorted(sel, key=lambda x: (x["rel"], x["ln"])):
            byfile.setdefault(r["rel"], []).append(r)
        title = {"A": "A 类（真缺陷候选）", "B": "B 类（疑似正当）",
                 "C": "C 类（已标注取代）", "D": "D 类（文字提及，非引用）",
                 "待判": "待判"}[cat]
        out.append("## 二·%s %s —— %d 行 / %d 文件" % (cat, title, len(sel), len(byfile)))
        out.append("")
        for rel, items in byfile.items():
            out.append("### `%s` （%d 处）" % (rel, len(items)))
            out.append("")
            out.append("| 行 | 归因 | 原文 |")
            out.append("|---:|:---|:---|")
            for it in items:
                txt = it["text"].replace("|", "\\|")
                out.append("| %d | %s | %s |" % (it["ln"], it["why"], txt))
            out.append("")

    # ---- 红区（仅记录，不动） ----
    sel = [r for r in rows if r["reg"] == "红区"]
    if sel:
        byfile = OrderedDict()
        for r in sorted(sel, key=lambda x: (x["rel"], x["ln"])):
            byfile.setdefault(r["rel"], []).append(r)
        out.append("## 三、红区引用（仅记录，不修）—— %d 行 / %d 文件" % (len(sel), len(byfile)))
        out.append("")
        for rel, items in byfile.items():
            out.append("- `%s`：%d 处（行 %s）"
                       % (rel, len(items), ", ".join(str(i["ln"]) for i in items)))
        out.append("")

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")

    # ---- 控制台摘要 ----
    print("=== 总览（行数 / 文件数） ===")
    for reg in REGION_ORDER:
        cells = []
        for cat in CAT_ORDER:
            n = cnt.get((reg, cat), 0)
            f = len(files_by_reg_cat.get((reg, cat), ()))
            if n:
                cells.append("%s=%d/%d文件" % (cat, n, f))
        if cells:
            print("  %-6s %s" % (reg, "  ".join(cells)))
    print("")
    print("=== 现役区 A 类文件清单 ===")
    a_files = defaultdict(int)
    for r in rows:
        if r["reg"] == "现役" and r["cat"] == "A":
            a_files[r["rel"]] += 1
    for rel, n in sorted(a_files.items(), key=lambda x: -x[1]):
        print("  %2d  %s" % (n, rel))
    print("")
    print("=== 自证检查 ===")
    target = "备课思路/新课大章节-第一轮化学原理.md"
    got = a_files.get(target, 0)
    print("  %s  A 类 = %d （预期 6）→ %s"
          % (target, got, "PASS" if got == 6 else "FAIL"))
    print("")
    print("报告已写：%s" % OUT)
    return 0 if got == 6 else 1


if __name__ == "__main__":
    sys.exit(main())
