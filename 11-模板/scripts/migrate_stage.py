#!/usr/bin/env python3
"""
migrate_stage.py — 存量文件 status → stage 批量迁移

读取现有文件的 status 字段，按映射规则填入 stage 字段。
不覆盖已存在 stage 字段的文件。
仅在文件有改动时回写磁盘。

用法:
    python migrate_stage.py                          # 默认范围：03-知识点 + 04-课件/学生讲义
    python migrate_stage.py --all                    # 扩展到 备课大纲/专题/题型
    python migrate_stage.py --dry-run                # 只预览不改写
    python migrate_stage.py --report                 # 生成迁移统计报告
"""

from __future__ import annotations

import argparse
import json
import sys
import re
from pathlib import Path
from typing import Any

# Windows GBK 终端兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() in ("gbk", "gb2312"):
    sys.stderr.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(1)

VAULT_ROOT = Path(__file__).resolve().parent.parent.parent

# ── 映射规则：status → stage ────────────────────────────────
STATUS_TO_STAGE: dict[str, str] = {
    # 知识点 & 通用
    "已填充": "published",
    "stub": "draft",
    "骨架": "draft",
    # 学生讲义
    "已审校": "published",
    "初稿": "review",
    # 备课大纲
    "草稿": "draft",
    "样板试跑": "review",
    "已生成（桥梁增强）": "published",
    # 专题
    "精品": "published",
    # 题型
    "框架": "draft",
    # 通用英文状态
    "draft": "draft",
    "review": "review",
    "published": "published",
    "deprecated": "deprecated",
    "archived": "archived",
}

# ── 目标目录优先级 ─────────────────────────────────────────
TARGET_DIRS_CORE = ["03-知识点", "04-课件/学生讲义"]
TARGET_DIRS_ALL = [
    "03-知识点",
    "04-课件/学生讲义",
    "04-课件/备课大纲",
    "04-专题与题型/专题",
    "04-专题与题型/题型",
]


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, str]:
    """返回 (fm_dict, body, raw_frontmatter_with_dashes)。"""
    if not text.startswith("---"):
        return {}, text.strip(), ""
    end = text.find("---", 3)
    if end == -1:
        return {}, text.strip(), ""
    raw = text[:end + 3]
    yaml_block = text[3:end].strip()
    body = text[end + 3:].strip()
    try:
        fm = yaml.safe_load(yaml_block)
        return (fm, body, raw) if isinstance(fm, dict) else ({}, body, raw)
    except yaml.YAMLError:
        return {}, body, raw


def add_stage_to_frontmatter(raw_fm: str, stage: str) -> str:
    """在 frontmatter 的 status 行之后插入 stage 行。"""
    lines = raw_fm.split("\n")
    # 找到 status 行，在其后插入
    new_lines: list[str] = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        # 在 status: <value> 行后插入（跳过 frontmatter 的 --- 边界）
        if not inserted and re.match(r'^\s*status\s*:\s*\S', line):
            # 缩进对齐
            indent = re.match(r'^(\s*)', line).group(1)
            new_lines.append(f"{indent}stage: {stage}")
            inserted = True
    if not inserted:
        # 没有 status 行，在第一个空行或 --- 前插入
        for i, line in enumerate(new_lines):
            if line.strip() == "---" and i > 0 and not inserted:
                indent = "  " if any(l.strip().startswith("-") for l in new_lines) else ""
                new_lines.insert(i, f"{indent}stage: {stage}")
                inserted = True
                break
    if not inserted:
        new_lines.append(f"stage: {stage}")
    return "\n".join(new_lines)


def guess_stage_from_body(body: str, fm: dict[str, Any]) -> str | None:
    """对无 status 的文件，通过内容猜测 stage。"""
    if len(body.strip()) > 500:
        return "published"
    if len(body.strip()) > 100:
        return "review"
    return "draft"


def main() -> None:
    parser = argparse.ArgumentParser(description="存量 status→stage 迁移")
    parser.add_argument("--all", action="store_true", help="扩展到备课大纲/专题/题型")
    parser.add_argument("--dry-run", action="store_true", help="只预览不改写")
    parser.add_argument("--report", action="store_true", help="生成迁移统计报告")
    args = parser.parse_args()

    target_dirs = TARGET_DIRS_ALL if args.all else TARGET_DIRS_CORE
    stats: dict[str, dict[str, int]] = {
        "scanned": 0,
        "already_has_stage": 0,
        "migrated": 0,
        "skipped_no_status": 0,
        "errors": 0,
    }
    migrated_files: list[tuple[str, str, str]] = []  # (path, status, stage)

    for d in target_dirs:
        target = VAULT_ROOT / d
        if not target.exists():
            print(f"⚠️  目录不存在: {d}")
            continue
        for f in sorted(target.rglob("*.md")):
            if ".excalidraw" in f.name:
                continue
            rel = f.relative_to(VAULT_ROOT).as_posix()
            stats["scanned"] += 1

            text = f.read_text(encoding="utf-8", errors="replace")
            fm, body, raw_fm = parse_frontmatter(text)
            if not fm:
                continue

            # 跳过已有 stage 的
            if fm.get("stage"):
                stats["already_has_stage"] += 1
                continue

            # 确定 status → stage
            status = fm.get("status")
            if status and status in STATUS_TO_STAGE:
                stage = STATUS_TO_STAGE[status]
            elif status:
                # 未知 status 值，用 draft 兜底
                stage = "draft"
            else:
                # 无 status 字段，通过内容猜测
                guess = guess_stage_from_body(body, fm)
                if guess:
                    stage = guess
                else:
                    stats["skipped_no_status"] += 1
                    continue

            # 执行迁移
            new_raw = add_stage_to_frontmatter(raw_fm, stage)
            new_text = new_raw + "\n\n" + body + "\n" if body else new_raw + "\n"

            if not args.dry_run:
                try:
                    f.write_text(new_text, encoding="utf-8")
                except Exception as e:
                    print(f"❌  写入失败: {rel} — {e}")
                    stats["errors"] += 1
                    continue

            stats["migrated"] += 1
            migrated_files.append((rel, str(status) if status else "(无)", stage))
            print(f"  {'[DRY]' if args.dry_run else '  ✓'} {rel}: status={status or '(无)'} → stage={stage}")

    # ── 报告 ─────────────────────────────────────────────────
    print(f"\n{'='*50}")
    print(f"迁移完成")
    print(f"  扫描: {stats['scanned']} 文件")
    print(f"  已有 stage: {stats['already_has_stage']}")
    print(f"  本次迁移: {stats['migrated']}")
    print(f"  跳过（无 status）: {stats['skipped_no_status']}")
    print(f"  错误: {stats['errors']}")
    print(f"{'='*50}")

    if args.report or args.dry_run:
        report_path = VAULT_ROOT / "02-数据库" / "stage-migration-report.json"
        report_data = {
            "date": __import__("datetime").date.today().isoformat(),
            "stats": stats,
            "migrated_files": migrated_files,
            "dry_run": args.dry_run,
        }
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        print(f"\n📄 报告: {report_path}")


if __name__ == "__main__":
    main()
