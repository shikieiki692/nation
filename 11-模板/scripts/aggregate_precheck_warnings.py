"""汇总习题书教师版 Word 预检 WARN，按规则分类输出，供 Phase 4 清理使用。

用法:
    python -X utf8 11-模板/scripts/aggregate_precheck_warnings.py
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parents[1]
REPORT = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-预检WARN分布.md"

_spec = importlib.util.spec_from_file_location(
    "build_all_handout_docx",
    SCRIPT_DIR / "build-all-handout-docx.py",
)
_module = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _module
assert _spec.loader is not None
_spec.loader.exec_module(_module)
precheck_file = _module.precheck_file


def main() -> int:
    root = VAULT_ROOT / "04-课件/习题集/习题书-教师版"
    chapter_files = sorted(p for p in root.rglob("*.md") if p.parent != root)
    rule_counts: Counter = Counter()
    rule_files: Counter = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    total = 0
    for md_path in chapter_files:
        report = precheck_file(md_path)
        for issue in report.issues:
            if issue.severity != "WARN":
                continue
            total += 1
            rule_counts[issue.rule] += 1
            rule_files[issue.rule] += 1
            if len(examples[issue.rule]) < 3:
                excerpt = (issue.excerpt or "").replace("|", "\\|")
                loc = f"{md_path.name}:L{issue.line_no}" if issue.line_no else md_path.name
                examples[issue.rule].append(f"{loc} · {excerpt[:80]}")

    L = [
        "---",
        "title: 2026-08-30-习题书V2-预检WARN分布",
        "type: 预检汇总",
        "task_type: 习题册公式清理",
        "status: 待清理",
        "created: 2026-08-30",
        "updated: 2026-08-30",
        "---",
        "",
        "# 习题书 V2 Word 预检 WARN 分布（Phase 4）",
        "",
        f"> 教师版 31 章，WARN 合计 {total}。",
        "",
        "## 一、按规则汇总",
        "",
        "| 规则 | 条数 | 涉及章节 | 示例 |",
        "|---|---:|---:|---|",
    ]
    for rule, count in rule_counts.most_common():
        ex = examples[rule][0] if examples[rule] else ""
        L.append(f"| {rule} | {count} | {rule_files[rule]} | {ex} |")
    L.append("")
    L.append("## 二、规则说明")
    L.append("")
    L.append("见 `build-all-handout-docx.py` 的 `_run_word_formula_precheck` 规则定义。")
    L.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"total_warn={total} rules={len(rule_counts)} -> {REPORT.name}")
    for rule, count in rule_counts.most_common():
        print(f"  {rule}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
