"""习题书图片资产审计与落库工具。

扫描生成结果里的全部 Obsidian 图片嵌入，按 basename 检查是否已存在于
媒体仓库/ 根目录；缺失时在全库定位同名源文件，--write 时复制落库。
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
from collections import defaultdict
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MEDIA_ROOT = VAULT_ROOT / "媒体仓库"

EMBED_RE = re.compile(r"!\[\[([^\]\n]+)\]\]")
HASH_NAME_RE = re.compile(r"[0-9a-fA-F]{64}\.[A-Za-z0-9]+")
IMAGE_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp",
    ".emf", ".wmf", ".tif", ".tiff", ".pdf",
}
SKIP_DIRS = {
    ".git", ".agents", ".codex", "node_modules", ".miktex-local",
    "__pycache__", "$outDir", ".preview_build", ".preview_build2",
}


def sha256(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def iter_markdown(root: Path):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(files):
            if fn.lower().endswith(".md"):
                yield Path(dirpath) / fn


def collect_embeds(root: Path) -> list[dict]:
    records = []
    for path in iter_markdown(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in EMBED_RE.finditer(text):
            raw = m.group(1).strip()
            target = raw.split("|", 1)[0].strip()
            basename = os.path.basename(target.replace("\\", "/")).strip()
            records.append({
                "file": rel,
                "raw": raw,
                "target": target,
                "basename": basename,
                "is_hash": bool(HASH_NAME_RE.fullmatch(basename)),
            })
    return records


def build_file_index(vault_root: Path) -> dict[str, list[Path]]:
    index = defaultdict(list)
    for dirpath, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(files):
            if Path(fn).suffix.lower() in IMAGE_SUFFIXES:
                index[fn.lower()].append(Path(dirpath) / fn)
    return index


def exact_candidate(target: str) -> Path | None:
    normalized = target.replace("\\", "/")
    if not normalized or normalized.startswith("/"):
        return None
    if re.match(r"^[A-Za-z]:/", normalized):
        return None
    parts = [p for p in normalized.split("/") if p not in ("", ".")]
    if ".." in parts:
        return None
    path = VAULT_ROOT.joinpath(*parts)
    return path if path.is_file() else None


def score_path(path: Path):
    parts = [p.lower() for p in path.parts]
    score = 0
    if any("_images" in p for p in parts):
        score += 3
    if any(p in {"mineru", "media"} for p in parts):
        score += 2
    if "媒体仓库" in path.parts:
        score += 2
    if ".chem_media" in parts:
        score += 1
    if HASH_NAME_RE.fullmatch(path.name):
        score += 1
    for marker in ("06-外部资料导入", "03-教材书籍", "07-资料提炼", "04-题库"):
        if marker in path.parts:
            score += 1
    return (-score, len(path.parts), str(path))


def best_path(paths: list[Path]) -> Path:
    return min(paths, key=score_path)


def content_groups(paths: list[Path]) -> dict[str, list[Path]]:
    groups = defaultdict(list)
    for p in paths:
        h = sha256(p)
        if h:
            groups[h].append(p)
    return groups


def analyze(records, file_index, media_root: Path):
    missing: dict[str, dict] = {}
    mismatches: dict[str, list[dict]] = defaultdict(list)
    existing_basenames = set()
    for rec in records:
        base = rec["basename"]
        if not base:
            continue
        dst = media_root / base
        if dst.is_file():
            existing_basenames.add(base)
            exact = exact_candidate(rec["target"])
            if exact is not None and sha256(dst) != sha256(exact):
                mismatches[base].append({"ref": rec, "exact": exact})
            continue
        missing.setdefault(base, {"basename": base, "refs": []})["refs"].append(rec)

    for info in missing.values():
        base = info["basename"]
        exact_sources = []
        for rec in info["refs"]:
            exact = exact_candidate(rec["target"])
            if exact is not None:
                exact_sources.append(exact)
        info["exact_sources"] = sorted(set(exact_sources), key=str)
        info["candidates"] = file_index.get(base.lower(), [])
        if info["exact_sources"]:
            info["source"] = best_path(info["exact_sources"])
            info["status"] = "exact"
        elif info["candidates"]:
            groups = content_groups(info["candidates"])
            group_bests = {
                h: best_path(paths)
                for h, paths in groups.items()
            }
            chosen_h = min(group_bests, key=lambda h: score_path(group_bests[h]))
            info["source"] = group_bests[chosen_h]
            info["status"] = "resolved" if len(groups) == 1 else "ambiguous"
        else:
            info["status"] = "unresolved"
    return missing, dict(mismatches), existing_basenames


def write_report(report_path: Path, args, media_root: Path, records, missing, mismatches, existing_basenames):
    total = len(records)
    unique_raw = len({r["raw"] for r in records})
    unique_base = len({r["basename"] for r in records})
    hash_refs = sum(1 for r in records if r["is_hash"])
    hash_unique = len({r["basename"] for r in records if r["is_hash"]})
    non_hash_refs = total - hash_refs
    non_hash_unique = len({r["basename"] for r in records if not r["is_hash"]})
    path_refs = sum(1 for r in records if r["target"] != r["basename"])
    missing_refs = sum(len(info["refs"]) for info in missing.values())
    resolved = [info for info in missing.values() if info["status"] in {"exact", "resolved"}]
    ambiguous = [info for info in missing.values() if info["status"] == "ambiguous"]
    unresolved = [info for info in missing.values() if info["status"] == "unresolved"]

    lines = [
        "# 习题书媒体收口审计",
        f"- root: {args.root}",
        f"- media_root: {media_root}",
        "",
        "## 汇总",
        f"- 嵌入引用: {total}",
        f"- 唯一 raw 目标: {unique_raw}",
        f"- 唯一 basename: {unique_base}",
        f"- 纯哈希引用: {hash_refs} / 唯一 {hash_unique}",
        f"- 非哈希引用: {non_hash_refs} / 唯一 {non_hash_unique}",
        f"- 路径式引用（target 含目录）: {path_refs}",
        f"- 已在媒体仓库根目录: {len(existing_basenames)}",
        f"- 媒体仓库根目录缺失: {len(missing)} / 引用 {missing_refs}",
        f"- 已定位来源: {len(resolved)}",
        f"- 内容歧义: {len(ambiguous)}",
        f"- 未解析: {len(unresolved)}",
        "",
        "## 缺失计划",
        "basename\tstatus\tsource\trefs",
    ]
    for info in sorted(missing.values(), key=lambda x: x["basename"].lower()):
        source = info.get("source")
        source_rel = source.relative_to(VAULT_ROOT).as_posix() if source else "-"
        lines.append(f"{info['basename']}\t{info['status']}\t{source_rel}\t{len(info['refs'])}")
    if mismatches:
        lines.append("")
        lines.append("## 根目录同名但内容不一致（exact 路径可解析时）")
        lines.append("basename\troot_sha256\texact_source\texact_sha256")
        for base in sorted(mismatches):
            for item in mismatches[base]:
                dst = media_root / base
                exact = item["exact"]
                lines.append(
                    f"{base}\t{sha256(dst)[:12]}\t{exact.relative_to(VAULT_ROOT).as_posix()}\t{sha256(exact)[:12]}"
                )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
    return {
        "total": total,
        "unique_raw": unique_raw,
        "unique_base": unique_base,
        "hash_refs": hash_refs,
        "hash_unique": hash_unique,
        "non_hash_refs": non_hash_refs,
        "non_hash_unique": non_hash_unique,
        "path_refs": path_refs,
        "existing": len(existing_basenames),
        "missing": len(missing),
        "missing_refs": missing_refs,
        "resolved": len(resolved),
        "ambiguous": len(ambiguous),
        "unresolved": len(unresolved),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".preview_build2", help="习题书生成输出根目录")
    ap.add_argument("--media-root", default=str(DEFAULT_MEDIA_ROOT))
    ap.add_argument("--report", default=".preview_build2/_qc_media_plan.txt")
    ap.add_argument("--write", action="store_true", help="把缺失图片复制到媒体仓库根目录")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    media_root = Path(args.media_root).resolve()
    if not root.is_dir():
        raise SystemExit(f"输出目录不存在: {root}")
    if not media_root.is_dir():
        raise SystemExit(f"媒体仓库不存在: {media_root}")

    records = collect_embeds(root)
    file_index = build_file_index(VAULT_ROOT)
    missing, mismatches, existing_basenames = analyze(records, file_index, media_root)
    summary = write_report(Path(args.report), args, media_root, records, missing, mismatches, existing_basenames)

    if args.write:
        copied = 0
        skipped_conflict = 0
        for info in sorted(missing.values(), key=lambda x: x["basename"].lower()):
            source = info.get("source")
            if source is None:
                continue
            dst = media_root / info["basename"]
            if dst.is_file():
                if sha256(dst) != sha256(source):
                    info["action"] = "conflict"
                    skipped_conflict += 1
                else:
                    info["action"] = "exists"
                continue
            shutil.copy2(source, dst)
            info["action"] = "copied"
            copied += 1
        write_report(Path(args.report), args, media_root, records, missing, mismatches, existing_basenames)
        print(f"复制 {copied} 个文件；跳过冲突 {skipped_conflict} 个。")

    print(f"嵌入 {summary['total']}（唯一 basename {summary['unique_base']}）")
    print(f"哈希引用 {summary['hash_refs']}，非哈希引用 {summary['non_hash_refs']}，路径式引用 {summary['path_refs']}")
    print(f"已在根目录 {summary['existing']}，缺失 {summary['missing']}（引用 {summary['missing_refs']}）")
    print(f"可解析 {summary['resolved']}，歧义 {summary['ambiguous']}，未解析 {summary['unresolved']}")
    print(f"报告: {Path(args.report).resolve()}")
    if summary["unresolved"]:
        print("存在未解析图片，需要人工处理后再推进。")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
