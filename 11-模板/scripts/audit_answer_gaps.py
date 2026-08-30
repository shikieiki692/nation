#!/usr/bin/env python3
"""只读审计：按生成器真实抽取逻辑，把无解答源文件分成可修复的桶。

用法:
  python 11-模板/scripts/audit_answer_gaps.py
  python 11-模板/scripts/audit_answer_gaps.py --write-report
"""

import io
import os
import re
import sys
from collections import Counter
from datetime import date
from importlib import import_module

_here = os.path.dirname(os.path.abspath(__file__))
_root = _here
while not os.path.isdir(os.path.join(_root, "04-题库")):
    _next = os.path.dirname(_root)
    if _next == _root:
        raise SystemExit("未找到 vault 根目录（04-题库）")
    _root = _next
os.chdir(_root)
if _here not in sys.path:
    sys.path.insert(0, _here)

bm = import_module("build_module_book")

MODULE_SPECS = [
    ("结构化学", bm.STRUCTURE_MAP, (99, "综合"), None),
    ("元素与分析", bm.YSFX_MAP, (99, "综合"), None),
    ("化学原理", bm.CHEM_MAP, (6, "综合"), None),
    ("有机化学", bm.ORGANIC_MAP, (6, "综合"), bm.ORGANIC_EXCLUDE),
]

ANSWER_HEADING_RE = re.compile(
    r"(?m)^#{1,4}\s*(?:参考答案|答案|解答|解析|解题思路|易错分析)\b"
)
ANSWER_INLINE_RE = re.compile(r">\s*\*\*(?:答案|参考答案|解析)\*\*|【答案】|答案[:：]")


def bucket_of(item):
    q_text, a_text = bm.split_question_answer(item["body"])
    if a_text.strip():
        return None
    body = item["body"]
    details_blocks = [m.group(1) for m in re.finditer(r"(?is)<details[^>]*>(.*?)</details>", body)]
    if details_blocks and any(bm.answer_markers(block) for block in details_blocks):
        return "有答案但内嵌details未抽取"
    if ANSWER_HEADING_RE.search(body) or ANSWER_INLINE_RE.search(body):
        return "有答案但标题格式未识别"
    if any(k in body for k in ("原书未提供本题解答", "原书未提供解答", "未提供本题解答", "暂无答案", "无答案")):
        return "真无答案-源书明确未提供"
    if not q_text.strip():
        return "空文件-仅元信息"
    return "真无答案-无答案节"


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    write_report = "--write-report" in sys.argv
    rows = []
    for module, chapter_map, fallback, exclude_subs in MODULE_SPECS:
        exclude_subs = set(exclude_subs or [])
        pool = [q for q in bm.gather_questions(module) if q["submodule"] not in exclude_subs]
        for item in pool:
            bucket = bucket_of(item)
            if bucket:
                rows.append({"module": module, "path": item["path"], "bucket": bucket})
    rows.sort(key=lambda x: (x["module"], x["path"]))

    print(f"无解答源文件总数: {len(rows)}")
    print("\n按模块：")
    by_mod = Counter(r["module"] for r in rows)
    for mod, cnt in by_mod.most_common():
        print(f"  {mod}: {cnt}")
    print("\n按桶：")
    for bucket, cnt in Counter(r["bucket"] for r in rows).most_common():
        print(f"  {bucket}: {cnt}")

    if not write_report:
        print("\n（仅统计；加 --write-report 写审计报告）")
        return

    out = os.path.join("09-审计报告", f"{date.today().isoformat()}-习题书QA答案缺口分桶.md")
    lines = []
    lines.append("---")
    lines.append("title: 习题书 Q-A 答案缺口分桶")
    lines.append("type: 审计报告")
    lines.append(f"updated: {date.today().isoformat()}")
    lines.append("---")
    lines.append("")
    lines.append("# 习题书 Q-A 答案缺口分桶")
    lines.append("")
    lines.append("> 按生成器 `build_module_book.split_question_answer` 的真实抽取逻辑统计：")
    lines.append("> split 后答案正文为空，即成书会写“（原书未提供解答）”的源文件。")
    lines.append("")
    lines.append("## 汇总")
    lines.append("")
    lines.append("| 模块 | 数 |")
    lines.append("|---|--:|")
    for mod in ("结构化学", "元素与分析", "化学原理", "有机化学"):
        lines.append(f"| {mod} | {by_mod.get(mod, 0)} |")
    lines.append(f"| 合计 | {len(rows)} |")
    lines.append("")
    lines.append("| 桶 | 数 | 处理方式 |")
    lines.append("|---|--:|---|")
    buckets = [
        ("有答案但内嵌details未抽取", "检查源文件并优先修生成器/源格式"),
        ("有答案但标题格式未识别", "按源书答案区补标题后重生成"),
        ("真无答案-源书明确未提供", "保持占位，只在教师版标注来源"),
        ("真无答案-无答案节", "回源书逐题核验是否真有答案"),
        ("空文件-仅元信息", "先恢复题干，再补答案或归档"),
    ]
    for bucket, note in buckets:
        lines.append(f"| {bucket} | {Counter(r['bucket'] for r in rows).get(bucket, 0)} | {note} |")
    lines.append("")
    lines.append("## 文件清单")
    lines.append("")
    for bucket, note in buckets:
        items = [r for r in rows if r["bucket"] == bucket]
        lines.append(f"### {bucket}（{len(items)}）")
        lines.append("")
        for r in items:
            lines.append(f"- `{r['path']}`")
        lines.append("")
    text = "\n".join(lines).rstrip() + "\n"
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"\n已写报告: {out}")


if __name__ == "__main__":
    main()
