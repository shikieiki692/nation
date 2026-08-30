"""把习题书教师版全部 Word 预检 WARN 导出为 JSONL，供 Phase 4 逐条清理。

用法:
    python -X utf8 11-模板/scripts/dump_precheck_warnings.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parents[1]
OUT = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-预检WARN清单.jsonl"

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
    rows = []
    for md_path in chapter_files:
        report = precheck_file(md_path)
        for issue in report.issues:
            if issue.severity != "WARN":
                continue
            rows.append(
                {
                    "chapter": md_path.relative_to(root).as_posix(),
                    "line": issue.line_no,
                    "rule": issue.rule,
                    "excerpt": issue.excerpt,
                }
            )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"warn={len(rows)} -> {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
