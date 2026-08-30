"""从严格版图片归属清单导出跨题重复图的去重分析 CSV。

用法:
    python -X utf8 11-模板/scripts/build_dup_image_analysis.py
"""

from __future__ import annotations

import csv
import json
from collections import Counter, OrderedDict
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2严格版-图片归属清单.jsonl"
MEDIA = VAULT_ROOT / "媒体仓库"
OUT = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-重复图去重分析.csv"


def main() -> int:
    rows = [
        json.loads(line)
        for line in SRC.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    groups: OrderedDict[str, list[dict]] = OrderedDict()
    for r in rows:
        if r.get("disposition") != "待人工":
            continue
        if not r.get("cross_question_repeat"):
            continue
        groups.setdefault(r["base"], []).append(r)

    header = [
        "图片哈希",
        "出现文件数",
        "语义块",
        "首现文件",
        "全部源文件",
        "媒体存在",
    ]
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for base, recs in sorted(
            groups.items(), key=lambda kv: (-len(kv[1]), kv[0])
        ):
            files = OrderedDict()
            bucket = Counter(r.get("bucket", "") for r in recs).most_common(1)[0][0]
            for r in recs:
                files[r["source_path"]] = r.get("line", "")
            writer.writerow(
                [
                    base,
                    len(files),
                    bucket,
                    next(iter(files)),
                    " | ".join(f"{p}:{ln}" for p, ln in files.items()),
                    "是" if (MEDIA / base).exists() else "否",
                ]
            )

    print(f"repeat_groups={len(groups)} -> {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
