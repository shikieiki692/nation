from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from handout_audit_utils import (
    Finding,
    VAULT_ROOT,
    detect_image_kind,
    file_kind_matches_extension,
    find_heading_before,
    find_inline_code_image_paths,
    normalize_relpath,
    read_text,
    resolve_vault_path,
)


INDEX_PATH = VAULT_ROOT / "00-首页" / "图片索引.md"
REPORT_DIR = VAULT_ROOT / "09-审计报告"


@dataclass(slots=True)
class IndexedImage:
    line: int
    path: str
    section: str | None
    source: str


@dataclass(slots=True)
class PreciseRow:
    theme: str
    path: str
    kp: str
    context: str
    image_type: str
    confidence: str
    note: str
    line: int


def is_placeholder_path(path: str) -> bool:
    markers = ("<", ">", "...", "XXX", "{hash}")
    return any(marker in path for marker in markers)


def build_basename_index() -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = defaultdict(list)
    for path in VAULT_ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}:
            index[path.name].append(path)
    return index


def extract_indexed_images(index_path: Path) -> tuple[list[IndexedImage], list[PreciseRow]]:
    text = read_text(index_path)
    lines = text.splitlines()

    indexed_images: list[IndexedImage] = []
    for line_no, rel_path in find_inline_code_image_paths(text):
        indexed_images.append(
            IndexedImage(
                line=line_no,
                path=rel_path,
                section=find_heading_before(lines, line_no),
                source="inline-code-path",
            )
        )

    precise_rows: list[PreciseRow] = []
    in_precise_table = False
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("| 主题 | 路径 |"):
            in_precise_table = True
            continue
        if in_precise_table:
            if not stripped.startswith("|"):
                in_precise_table = False
                continue
            if set(stripped) <= {"|", ":", "-", " "}:
                continue
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if len(cells) < 7:
                continue
            path = cells[1].strip("`")
            precise_rows.append(
                PreciseRow(
                    theme=cells[0],
                    path=normalize_relpath(path),
                    kp=cells[2],
                    context=cells[3],
                    image_type=cells[4],
                    confidence=cells[5],
                    note=cells[6],
                    line=idx,
                )
            )
    return indexed_images, precise_rows


def audit_index(index_path: Path) -> tuple[list[Finding], list[PreciseRow], Counter[str]]:
    indexed_images, precise_rows = extract_indexed_images(index_path)
    findings: list[Finding] = []
    type_counter: Counter[str] = Counter()
    basename_index = build_basename_index()

    seen_paths: dict[str, IndexedImage] = {}
    for entry in indexed_images:
        if is_placeholder_path(entry.path):
            continue
        type_counter["all-indexed-image-paths"] += 1
        path = resolve_vault_path(entry.path)
        if not path.exists():
            basename = Path(entry.path).name
            candidates = basename_index.get(basename, [])
            hint = ""
            if len(candidates) == 1:
                hint = f"；候选真实位置：{candidates[0].relative_to(VAULT_ROOT).as_posix()}"
            elif len(candidates) > 1:
                hint = f"；候选同名文件数：{len(candidates)}"
            findings.append(
                Finding(
                    severity="error",
                    code="INDEX_PATH_MISSING",
                    message=f"图片索引路径不存在：{entry.path}{hint}",
                    line=entry.line,
                    context=entry.section,
                )
            )
            continue

        actual = detect_image_kind(path)
        if not file_kind_matches_extension(path):
            findings.append(
                Finding(
                    severity="warning",
                    code="INDEX_KIND_MISMATCH",
                    message=f"扩展名与文件头不一致：{entry.path}（检测到 {actual}）",
                    line=entry.line,
                    context=entry.section,
                )
            )

        if entry.path in seen_paths:
            first = seen_paths[entry.path]
            findings.append(
                Finding(
                    severity="info",
                    code="INDEX_DUPLICATE_PATH",
                    message=f"重复记录同一路径：{entry.path}（首次出现于第 {first.line} 行）",
                    line=entry.line,
                    context=entry.section,
                )
            )
        else:
            seen_paths[entry.path] = entry

    for row in precise_rows:
        type_counter[row.image_type] += 1
        if not row.confidence.startswith(("🟢", "🟡", "🔴")):
            findings.append(
                Finding(
                    severity="warning",
                    code="INDEX_CONFIDENCE_FORMAT",
                    message=f"置信度格式不规范：{row.theme} / {row.confidence}",
                    line=row.line,
                    context=row.image_type,
                )
            )

    return findings, precise_rows, type_counter


def build_secondary_category_summary(rows: list[PreciseRow]) -> dict[str, list[str]]:
    buckets: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        image_type = row.image_type
        if any(key in image_type for key in ["轨道", "能级", "径向", "趋势", "因果链"]):
            buckets["原子结构与周期律"].add(image_type)
        elif any(key in image_type for key in ["晶胞", "堆积", "空隙", "投影", "对称", "配位", "层状", "簇"]):
            buckets["结构化学与晶体"].add(image_type)
        elif any(key in image_type for key in ["机理", "构型", "势能", "真题原图"]):
            buckets["有机与反应机理"].add(image_type)
        elif any(key in image_type for key in ["相图", "热化学", "公式", "示意", "元素实例"]):
            buckets["物化图表与方法图"].add(image_type)
        else:
            buckets["其他"].add(image_type)
    return {key: sorted(values) for key, values in buckets.items()}


def write_report(
    report_path: Path,
    index_path: Path,
    findings: list[Finding],
    rows: list[PreciseRow],
    type_counter: Counter[str],
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    secondary = build_secondary_category_summary(rows)
    missing = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]

    lines: list[str] = [
        "---",
        "title: 图片索引核验报告",
        "type: 审计报告",
        "status: 完成",
        f"created: {date.today().isoformat()}",
        f"updated: {date.today().isoformat()}",
        "tags: [审计报告, 图片索引, 讲义图片, 预检]",
        f"source_note: \"[[{index_path.relative_to(VAULT_ROOT).as_posix()}]]\"",
        "---",
        "",
        "# 图片索引核验报告",
        "",
        "## 结论",
        "",
        f"- 精标表条目数：{len(rows)}",
        f"- 实际核验到的图片路径数：{type_counter['all-indexed-image-paths']}",
        f"- 缺失路径：{len(missing)}",
        f"- 扩展名/文件头异常：{len(warnings)}",
        "",
        "## 二级分类建议",
        "",
    ]

    for bucket, types in secondary.items():
        lines.append(f"- **{bucket}**：{' / '.join(types) if types else '—'}")

    lines.extend(["", "## 类型分布", ""])
    lines.append("| 类型 | 数量 |")
    lines.append("|:---|---:|")
    for image_type, count in sorted(
        ((k, v) for k, v in type_counter.items() if k != "all-indexed-image-paths"),
        key=lambda item: (-item[1], item[0]),
    ):
        lines.append(f"| {image_type} | {count} |")

    lines.extend(["", "## 发现项", ""])
    if not findings:
        lines.append("- 无异常，所有已登记图片路径均能定位。")
    else:
        for finding in findings:
            where = f"（第 {finding.line} 行）" if finding.line else ""
            context = f"；上下文：{finding.context}" if finding.context else ""
            lines.append(
                f"- [{finding.severity.upper()}] `{finding.code}` {finding.message}{where}{context}"
            )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="核验图片索引中的实际图片路径。")
    parser.add_argument(
        "--index",
        default=str(INDEX_PATH.relative_to(VAULT_ROOT)),
        help="图片索引路径（相对 vault 根目录）",
    )
    parser.add_argument(
        "--report",
        default=str((REPORT_DIR / f"{date.today().isoformat()}-图片索引核验.md").relative_to(VAULT_ROOT)),
        help="输出报告路径（相对 vault 根目录）",
    )
    args = parser.parse_args()

    index_path = VAULT_ROOT / args.index
    report_path = VAULT_ROOT / args.report

    findings, rows, type_counter = audit_index(index_path)
    write_report(report_path, index_path, findings, rows, type_counter)

    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]

    print(f"[index-audit] rows={len(rows)} indexed_paths={type_counter['all-indexed-image-paths']}")
    print(f"[index-audit] errors={len(errors)} warnings={len(warnings)} report={report_path}")

    for finding in errors[:20]:
        prefix = f"line {finding.line}" if finding.line else "line ?"
        print(f"  ERROR {prefix}: {finding.message}")
    for finding in warnings[:20]:
        prefix = f"line {finding.line}" if finding.line else "line ?"
        print(f"  WARN  {prefix}: {finding.message}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
