"""把源文件中 `ΔH° / E° / K°` 等标准态 `°` 统一为 `θ`，避开度数单位（25°C、θ/°）。

规则：仅替换前一个有效字符为 H/G/S/E/K 的 `°`；该集合覆盖 ΔH°、ΔG°、ΔS°、
E°、K°、ΔfH°、ΔE°、TΔS° 等常见标准态写法。`键角/(°)`、`θ/°`、`25°C` 不触发。

用法:
    python -X utf8 11-模板/scripts/clean_standard_state_degree.py
"""

from __future__ import annotations

import re
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = VAULT_ROOT / "04-题库"
PATTERN = re.compile(r"(?<=[HGSEK])°")
# 文档示例文件保留 `E°` 原样，避免把规则示例本身改掉。
SKIP = {
    VAULT_ROOT / "04-题库/教学改编题/无机和结构化学/错误模式知识库.md",
}


def main() -> int:
    changed = 0
    files = 0
    for path in sorted(SRC_ROOT.rglob("*.md")):
        if path in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = PATTERN.subn("θ", text)
        if n:
            path.write_text(new_text, encoding="utf-8", newline="")
            files += 1
            changed += n
    print(f"replaced={changed} files={files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
