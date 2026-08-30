#!/usr/bin/env python3
"""Scan exercise-book markdown through the Word precheck and write a report."""

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


ROOTS = [
    Path(r"C:\Obsidion\妙妙屋\04-课件\习题集\习题书-教师版"),
    Path(r"C:\Obsidion\妙妙屋\04-课件\习题集\习题书-学生版"),
]
REPORT = Path(r"C:\Obsidion\妙妙屋\.preview_build2\precheck-report-2026-08-30.txt")


def main() -> int:
    lines: list[str] = []
    total_errors = 0
    any_errors = False
    for root in ROOTS:
        lines.append(f"==== {root.name} ====")
        for md_path in sorted(root.glob("*/**/*.md")):
            if md_path.name == "目录.md":
                continue
            try:
                report = wc.precheck_file(md_path, verbose=False)
            except Exception as exc:  # pragma: no cover - defensive
                lines.append(f"EXC {md_path.relative_to(root)}: {exc}")
                any_errors = True
                continue
            flag = "OK " if report.error_count == 0 else "ERR"
            lines.append(
                f"{flag} {md_path.relative_to(root)}: "
                f"E={report.error_count} W={report.warning_count} I={report.info_count}"
            )
            total_errors += report.error_count
            for issue in report.issues:
                if issue.severity != "ERROR":
                    continue
                excerpt = (issue.excerpt or "").replace("\n", " ").strip()
                if len(excerpt) > 180:
                    excerpt = excerpt[:180] + "..."
                lines.append(
                    f"    ERROR {issue.rule} L{issue.line_no}: {excerpt}"
                )
                any_errors = True

    lines.append(f"\nTOTAL_ERRORS={total_errors}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if not any_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
