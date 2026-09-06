#!/usr/bin/env python3
"""normalize_line_endings.py — 妙妙屋全库 md 行尾/BOM 一次性统一。

口径：UTF-8 无 BOM + LF。
默认 dry-run 只摸底；加 --apply 才写盘。

排除目录（历史内容不动 / 非内容区）：
  .git, .obsidian, .trash, node_modules, kb-vault-mcp,
  09-审计报告, 00-首页/工作日志

用法：
  python normalize_line_endings.py <vault_root>            # dry-run 摸底
  python normalize_line_endings.py <vault_root> --apply    # 实际转换
"""
import sys
from pathlib import Path

EXCLUDE_DIRS = {".git", ".obsidian", ".trash", "node_modules", "kb-vault-mcp"}
EXCLUDE_TOP = {("09-审计报告",), ("00-首页", "工作日志")}

BOM = b"\xef\xbb\xbf"


def excluded(rel: Path) -> bool:
    parts = rel.parts
    if any(p in EXCLUDE_DIRS for p in parts):
        return True
    for pre in EXCLUDE_TOP:
        if parts[: len(pre)] == pre:
            return True
    return False


def scan_file(p: Path):
    raw = p.read_bytes()
    has_bom = raw.startswith(BOM)
    body = raw[len(BOM):] if has_bom else raw
    crlf = body.count(b"\r\n")
    lone_cr = body.replace(b"\r\n", b"").count(b"\r")
    return has_bom, crlf, lone_cr, raw


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    apply = "--apply" in sys.argv
    stats = {"total": 0, "clean": 0, "bom": 0, "crlf": 0, "lone_cr": 0, "changed": 0}
    by_top: dict[str, int] = {}

    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if excluded(rel):
            continue
        stats["total"] += 1
        has_bom, crlf, lone_cr, raw = scan_file(p)
        if not (has_bom or crlf or lone_cr):
            stats["clean"] += 1
            continue
        if has_bom:
            stats["bom"] += 1
        if crlf:
            stats["crlf"] += 1
        if lone_cr:
            stats["lone_cr"] += 1
        by_top[rel.parts[0]] = by_top.get(rel.parts[0], 0) + 1
        if apply:
            body = raw[len(BOM):] if has_bom else raw
            body = body.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            p.write_bytes(body)
            stats["changed"] += 1

    mode = "APPLY" if apply else "DRY-RUN"
    print(f"[{mode}] 扫描 md: {stats['total']}")
    print(f"  已干净: {stats['clean']}")
    print(f"  需处理: BOM={stats['bom']}  CRLF={stats['crlf']}  孤立CR={stats['lone_cr']}")
    if apply:
        print(f"  已转换: {stats['changed']}")
    if by_top:
        print("  按顶层目录分布:")
        for k in sorted(by_top):
            print(f"    {k}: {by_top[k]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
