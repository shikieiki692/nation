#!/usr/bin/env python3
"""Scan source question bank markdown through the Word precheck (compact)."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(r"C:\Obsidion\妙妙屋\11-模板\scripts")
sys.path.insert(0, str(SCRIPT_DIR))

import importlib.util

_SPEC = importlib.util.spec_from_file_location(
    "build_all_handout_docx",
    SCRIPT_DIR / "build-all-handout-docx.py",
)
wc = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
sys.modules[_SPEC.name] = wc
_SPEC.loader.exec_module(wc)


ROOT = Path(r"C:\Obsidion\妙妙屋\04-题库")
REPORT = Path(r"C:\Obsidion\妙妙屋\.preview_build2\precheck-report-sources-2026-08-30.txt")


def main() -> int:
    lines: list[str] = []
    total_errors = 0
    error_files = 0
    scanned = 0
    by_rule: dict[str, int] = {}
    for md_path in sorted(ROOT.rglob("*.md")):
        scanned += 1
        try:
            report = wc.precheck_file(md_path, verbose=False)
        except Exception as exc:  # pragma: no cover - defensive
            lines.append(f"EXC {md_path.relative_to(ROOT)}: {exc}")
            continue
        if report.error_count == 0:
            continue
        error_files += 1
        rel = md_path.relative_to(ROOT)
        lines.append(f"ERR {report.error_count} {rel}")
        for issue in report.issues:
            if issue.severity != "ERROR":
                continue
            by_rule[issue.rule] = by_rule.get(issue.rule, 0) + 1
            excerpt = (issue.excerpt or "").replace("\n", " ").strip()
            if len(excerpt) > 220:
                excerpt = excerpt[:220] + "..."
            lines.append(f"    {issue.rule} L{issue.line_no}: {excerpt}")
        total_errors += report.error_count

    lines.append(f"\nSCANNED={scanned} ERROR_FILES={error_files} TOTAL_ERRORS={total_errors}")
    lines.append("BY_RULE " + " ".join(f"{k}={v}" for k, v in sorted(by_rule.items())))
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"SCANNED={scanned} ERROR_FILES={error_files} TOTAL_ERRORS={total_errors}")
    print("BY_RULE " + " ".join(f"{k}={v}" for k, v in sorted(by_rule.items())))
    print(f"report: {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
