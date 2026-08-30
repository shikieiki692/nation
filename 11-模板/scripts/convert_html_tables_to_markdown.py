"""把 Phase 3 分类为 pipe_candidate 的源文件 HTML 表转成 Markdown pipe table。

用法:
    python -X utf8 11-模板/scripts/convert_html_tables_to_markdown.py

只处理 `09-审计报告/2026-08-30-习题书V2-表格分类台账.jsonl` 中
classification == pipe_candidate 且能定位到源文件的表，避免误改 span/超宽表。
转换前会再次校验：无 colspan/rowspan、无 <br>、无图片、无未转义 |、列数 <= 8。
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
LEDGER = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-表格分类台账.jsonl"
LOG = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-表格转Markdown.log.jsonl"


def parse_table(block: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for tr in re.findall(r"<tr\b[^>]*>(.*?)</tr>", block, flags=re.I | re.S):
        cells = re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", tr, flags=re.I | re.S)
        rows.append([html.unescape(c).strip() for c in cells])
    return rows


def to_pipe_table(rows: list[list[str]], prefix: str = "") -> str:
    width = max((len(r) for r in rows), default=0)
    padded = [r + [""] * (width - len(r)) for r in rows]
    lines = []
    for row in padded:
        cells = [c.replace("|", "\\|") if "|" in c else c for c in row]
        lines.append(prefix + "| " + " | ".join(cells) + " |")
    if width:
        lines.insert(1, prefix + "| " + " | ".join(["---"] * width) + " |")
    return "\n".join(lines)


def main() -> int:
    records = [
        json.loads(line)
        for line in LEDGER.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    targets: dict[Path, list[int]] = {}
    for rec in records:
        if rec.get("classification") != "pipe_candidate":
            continue
        for cand in rec.get("source_candidates", []):
            p = VAULT_ROOT / "04-题库" / cand["file"]
            targets.setdefault(p, []).append(cand["line"])

    converted = 0
    skipped: list[dict] = []
    changed_files: list[dict] = []
    for path in sorted(targets):
        lines_to_fix = sorted(set(targets[path]))
        text = path.read_text(encoding="utf-8")
        raw_lines = text.splitlines(keepends=True)
        file_changed = False
        file_converted = 0
        for line_no in lines_to_fix:
            idx = line_no - 1
            if idx >= len(raw_lines):
                skipped.append({"file": str(path), "line": line_no, "reason": "line_missing"})
                continue
            raw = raw_lines[idx]
            line = raw.rstrip("\r\n")
            m = re.search(r"<table\b[^>]*>.*?</table>", line, flags=re.I | re.S)
            if not m:
                skipped.append({"file": str(path), "line": line_no, "reason": "table_not_found"})
                continue
            block = m.group(0)
            low = block.lower()
            if "colspan" in low or "rowspan" in low:
                skipped.append({"file": str(path), "line": line_no, "reason": "span"})
                continue
            if "<br" in low or "![[" in block or "<img" in low:
                skipped.append({"file": str(path), "line": line_no, "reason": "complex_cell"})
                continue
            rows = parse_table(block)
            width = max((len(r) for r in rows), default=0)
            if not rows or width == 0 or width > 8:
                skipped.append(
                    {"file": str(path), "line": line_no, "reason": f"width={width} rows={len(rows)}"}
                )
                continue
            if any("|" in c for r in rows for c in r):
                skipped.append({"file": str(path), "line": line_no, "reason": "pipe_in_cell"})
                continue
            prefix = line[: len(line) - len(line.lstrip())]
            raw_lines[idx] = to_pipe_table(rows, prefix=prefix) + raw[len(line) :]
            file_changed = True
            file_converted += 1
            converted += 1
        if file_changed:
            path.write_text("".join(raw_lines), encoding="utf-8", newline="")
            changed_files.append(
                {"file": str(path.relative_to(VAULT_ROOT)), "converted": file_converted}
            )

    log_rows = changed_files + skipped
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("w", encoding="utf-8") as f:
        for row in log_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"converted={converted} files={len(changed_files)} skipped={len(skipped)}")
    if skipped:
        reasons = Counter(s["reason"] for s in skipped)
        print("skip_reasons=" + ", ".join(f"{k}:{v}" for k, v in reasons.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
