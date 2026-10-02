# -*- coding: utf-8 -*-
"""把「最近 N 分钟内改过的讲义 md」写成清单文件（LF 行尾），供闸门脚本 --list 使用。

清单必须 LF：validate_kb / jsyaml_verify 对 \\r 敏感（清单里混 \\r 会导致 exists 全 False）。

用法:
    python -X utf8 11-模板/scripts/emit_changed_handout_list.py [分钟数] [输出文件]
默认 120 分钟，输出 .workbuddy/tmp/changed_handout.txt
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "04-课件" / "学生讲义"


def main() -> None:
    minutes = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else (
        VAULT_ROOT / ".workbuddy" / "tmp" / "changed_handout.txt")
    cutoff = time.time() - minutes * 60
    files = sorted(str(p.relative_to(VAULT_ROOT)).replace("\\", "/")
                   for p in SRC.rglob("*.md")
                   if p.stat().st_mtime >= cutoff
                   and "_归档" not in p.relative_to(SRC).parts)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(files) + "\n")
    print("清单 %s：%d 个文件（%.0f 分钟内）" % (out, len(files), minutes))


if __name__ == "__main__":
    main()
