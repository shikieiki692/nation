"""习题书一键门禁：审计 / 预检 / 表格 / Word 结构渲染检查。

默认只跑校验门禁；加 `--rebuild` 会先重生成教师版/学生版 Markdown 与 docx。

用法:
    python -X utf8 11-模板/scripts/gate_exercise_books.py [--rebuild]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parents[1]


def run(script: str, *args: str) -> tuple[int, str]:
    cmd = [sys.executable, "-X", "utf8", str(SCRIPT_DIR / script), *args]
    proc = subprocess.run(
        cmd,
        cwd=VAULT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=1800,
    )
    tail = (proc.stdout or "") + (proc.stderr or "")
    tail = "\n".join(tail.strip().splitlines()[-6:])
    return proc.returncode, tail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()

    results: list[tuple[str, bool, str]] = []
    if args.rebuild:
        for edition in ("teacher", "student"):
            code, tail = run(
                "build_module_book.py",
                "--strict",
                "--write",
                "--clean",
                *(("--edition", edition) if edition == "student" else ()),
            )
            results.append((f"build-{edition}", code == 0, tail))
        for root, out in (
            ("04-课件/习题集/习题书-教师版", "00-首页/题组Word/习题书/教师版"),
            ("04-课件/习题集/习题书-学生版", "00-首页/题组Word/习题书/学生版"),
        ):
            code, tail = run(
                "build-all-handout-docx.py",
                "--batch-root",
                root,
                "--output-dir",
                out,
                "--strict-images",
                "--cover",
                "--parallel",
                "4",
            )
            results.append((f"docx-{Path(root).name}", code == 0, tail))

    checks = [
        (
            "audit",
            "audit_exercise_book.py",
            [
                "--root",
                "04-课件/习题集/习题书-教师版",
                "--report",
                "09-审计报告/2026-08-30-习题书V2正式版审计.md",
                "--mapping",
                "09-审计报告/2026-08-30-习题书V2正式版-source-map.jsonl",
                "--image-context",
                "09-审计报告/2026-08-30-习题书V2正式版-图片归属清单.jsonl",
            ],
        ),
        ("precheck", "precheck_exercise_books.py", ["--root", "04-课件/习题集/习题书-教师版"]),
        ("tables", "classify_book_tables.py", []),
        ("docx-structure", "validate_docx_structure.py", []),
    ]
    for name, script, args_list in checks:
        code, tail = run(script, *args_list)
        results.append((name, code == 0, tail))

    print("\n=== 门禁结果 ===")
    failed = 0
    for name, ok, tail in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if tail:
            print("    " + tail.replace("\n", "\n    "))
        if not ok:
            failed += 1
    print(f"\nGATE_RESULT={'PASS' if failed == 0 else 'FAIL'}  failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
