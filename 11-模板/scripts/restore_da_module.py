"""只把 `module:` 行恢复到 git HEAD 原值，保留归一化的 `subject_module`。

用途：撤销“把 module 改成众数”导致的章节路由偏离。

用法:
    python -X utf8 11-模板/scripts/restore_da_module.py
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


def module_line(text: str) -> str | None:
    m = re.search(r"(?m)^module:\s*.*$", text)
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
        if len(line) < 4:
            continue
        rel = line[3:].strip().strip("\r")
        if not rel.endswith(".md"):
            continue
        path = VAULT_ROOT / rel
        if not path.exists():
            continue
        cur = path.read_text(encoding="utf-8")
        orig = git_show(rel)
        cur_mod = module_line(cur)
        orig_mod = module_line(orig)
        if cur_mod is None or orig_mod is None or cur_mod == orig_mod:
            continue
        new = re.sub(r"(?m)^module:\s*.*$", orig_mod, cur, count=1)
        path.write_text(new, encoding="utf-8")
        changed += 1
    print(f"restored_module_files={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
