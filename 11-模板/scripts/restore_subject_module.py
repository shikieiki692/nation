"""把 `subject_module:` 行恢复到 git HEAD 原值，撤销批量归一化。

用法:
    python -X utf8 11-模板/scripts/restore_subject_module.py
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]


def git_show(rel: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(VAULT_ROOT), "show", f"HEAD:{rel}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.stdout


def field_line(text: str, field: str) -> str | None:
    m = re.search(rf"(?m)^{field}:\s*.*$", text)
    return m.group(0) if m else None


def main() -> int:
    proc = subprocess.run(
        ["git", "-C", str(VAULT_ROOT), "status", "--porcelain", "-z", "--", "04-题库"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    changed = 0
    for line in proc.stdout.split("\x00"):
        if not line:
            continue
        rel = line[3:].strip().strip("\r")
        if not rel.endswith(".md"):
            continue
        path = VAULT_ROOT / rel
        if not path.exists():
            continue
        cur = path.read_text(encoding="utf-8")
        orig = git_show(rel)
        cur_f = field_line(cur, "subject_module")
        orig_f = field_line(orig, "subject_module")
        if cur_f is None or orig_f is None or cur_f == orig_f:
            continue
        new = re.sub(r"(?m)^subject_module:\s*.*$", orig_f, cur, count=1)
        path.write_text(new, encoding="utf-8")
        changed += 1
    print(f"restored_subject_module_files={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
