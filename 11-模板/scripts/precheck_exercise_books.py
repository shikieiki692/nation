"""聚合 Word 预检：对习题书全部章节跑 build-all-handout-docx 的 precheck。

用法:
    python 11-模板/scripts/precheck_exercise_books.py [--root 04-课件/习题集/习题书-教师版]

输出每章 ERROR/WARN 计数与总体汇总，适合批处理 stdout 编码不稳定的场景。
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=r"04-课件\习题集\习题书-教师版",
        help="习题书章节目录根（默认 04-课件/习题集/习题书-教师版）",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: root not found: {root}", file=sys.stderr)
        return 2

    chapter_files = sorted(
        p for p in root.rglob("*.md")
        if p.parent != root and p.stem != "目录"
    )
    if not chapter_files:
        print(f"ERROR: no chapter files under {root}", file=sys.stderr)
        return 2

    total_errors = 0
    total_warnings = 0
    rows: list[tuple[str, int, int, bool]] = []
    for md_path in chapter_files:
        try:
            report = precheck_file(md_path)
        except Exception as exc:
            print(f"[EXC] {md_path.name}: {exc}", file=sys.stderr)
            rows.append((md_path.name, -1, -1, True))
            total_errors += 1
            continue
        rows.append(
            (
                md_path.name,
                report.error_count,
                report.warning_count,
                report.has_errors,
            )
        )
        total_errors += report.error_count
        total_warnings += report.warning_count

    print(f"{'file':<42}{'ERR':>5}{'WARN':>6}{'status':>8}")
    for name, err, warn, has_err in rows:
        print(f"{name:<42}{err:>5}{warn:>6}{'FAIL' if has_err else 'ok':>8}")
    print(f"\nTOTAL_ERRORS={total_errors}  TOTAL_WARNINGS={total_warnings}  FILES={len(rows)}")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
