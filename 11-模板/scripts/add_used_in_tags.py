#!/usr/bin/env python3
"""
add_used_in_tags.py
===================
Parse source index tables from 5 exercise group files in
04-题库/教学改编题/无机和结构化学/, resolve source references to
actual vault files, and add `used_in` frontmatter tags.

Usage:
    python 11-模板/scripts/add_used_in_tags.py [--dry-run] [--verbose]

Source reference patterns handled:
  - 题库11-XX / 普化原理11-XX  → 04-题库/化学原理/Ch11-原子结构/11-XX.md
  - 题库12-XX                   → 04-题库/化学原理/Ch12-化学键与分子结构/12-XX.md
  - 题库13-XX                   → 04-题库/化学原理/Ch13-晶体与晶体结构/13-XX.md
  - 题库14-XX                   → 04-题库/化学原理/Ch14-配位化合物/14-XX.md
  - 教材习题Ch05-5.XX           → 04-题库/教材习题/无机化学例题与习题/Ch05-*/习题|例题/5.XX*.md
  - 第XX届初赛Q(N)/QN           → 04-题库/真题/第XX届初赛/**/题-0XX-Q-*.md
  - 第XX届决赛Q(N)/QN           → 04-题库/真题/第XX届决赛/**/题-XXX-*.md
  - 初赛讲义X.XX                 → 04-题库/教材习题/化学竞赛初赛讲义/题-*-习题X.XX.md
  - 自编 / 自编补充 / 改编题     → skip (no source file)
  - 讲义7.1 / 讲义例N / 讲义算一算 → skip (lecture-only, no separate file)
"""

import argparse
import glob
import os
import re
import sys
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")

# ── Exercise group files and their used_in tags ──────────────────────────────

EXERCISE_GROUPS = [
    {
        "path": "04-题库/教学改编题/无机和结构化学/题-改编-原子结构基础-第一轮练习题组.md",
        "used_in": "原子结构题组",
    },
    {
        "path": "04-题库/教学改编题/无机和结构化学/题-改编-元素周期表与周期律-第一轮练习题组.md",
        "used_in": "元素周期律题组",
    },
    {
        "path": "04-题库/教学改编题/无机和结构化学/题-改编-分子结构基础-第一轮练习题组.md",
        "used_in": "分子结构题组",
    },
    {
        "path": "04-题库/教学改编题/无机和结构化学/题-改编-配位化合物基础-第一轮练习题组.md",
        "used_in": "配位化合物题组",
    },
    {
        "path": "04-题库/教学改编题/无机和结构化学/题-改编-晶体学与晶体结构-第一轮练习题组.md",
        "used_in": "晶体结构题组",
    },
]


def read_file(path: str) -> str:
    """Read a file with UTF-8 encoding."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    """Write a file with UTF-8 encoding."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ── Source reference parsing ─────────────────────────────────────────────────

def parse_source_index(filepath: str) -> list[dict]:
    """
    Parse the source index table from an exercise group file.
    Returns list of dicts with keys: question_id, source_ref, content_summary
    """
    text = read_file(filepath)
    results = []

    # Strategy: find all "> **来源**：" lines in the question sections
    # These appear as blockquotes like: > **来源**：题库11-25
    # or table rows in the source index at the end

    # First try: parse the "题目来源索引" table at the bottom
    # Format: | 题号 | 来源 | 具体题目内容 |
    table_pattern = re.compile(
        r'\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|',
        re.MULTILINE
    )

    # Find the source index section
    source_section = text
    # Look for "来源索引" or "题目来源索引"
    idx_match = re.search(r'(?:题目)?来源索引', text)
    if idx_match:
        source_section = text[idx_match.start():]

    for m in table_pattern.finditer(source_section):
        qid = m.group(1).strip()
        source_raw = m.group(2).strip()
        content_summary = m.group(3).strip()

        # Skip header rows
        if qid in ('题号', ':---', '---') or '题号' in qid:
            continue

        # Parse the source reference
        ref = parse_source_ref(source_raw)
        if ref:
            results.append({
                "question_id": qid,
                "source_raw": source_raw,
                "source_ref": ref,
                "content_summary": content_summary,
            })

    return results


def parse_source_ref(raw: str) -> dict | None:
    """
    Parse a raw source reference string into a structured reference.
    Returns None if the reference should be skipped (自编, 讲义-only, 改编题, etc.)
    Returns dict with keys: type, pattern, raw

    Reference types:
      - tiku: 题库XX-YY
      - puhua: 普化原理XX-YY
      - chuyi: 教材习题ChXX-YY or 《无机化学例题与习题》
      - zhenti: 第XX届初赛/决赛 with sub-question info
      - jiangyi: 初赛讲义X.XX
      - zhaoxinguang: 赵鑫光 (no individual files)
      - huizhi: 汇智 (no individual files)
    """
    raw = raw.strip()

    # ── Skip self-authored / vague / lecture-only references ──
    skip_patterns = [
        r'^自编', r'^改编题$', r'讲义例\d', r'讲义算一算',
        r'讲义\d+\.\d+基础', r'^补充题$', r'^真题$',
        r'^初赛讲义习题$', r'^普化原理$', r'^教材习题Ch\d+$',
        r'教材习题-无机化学第\d版',
    ]
    for pat in skip_patterns:
        if re.search(pat, raw):
            return None

    # ── 题库XX-YY ──
    m = re.search(r'题库(\d+)-(\d+)', raw)
    if m:
        return {"type": "tiku", "ch": m.group(1), "num": m.group(2), "raw": raw}

    # ── 普化原理XX-YY ──
    m = re.search(r'普化原理(\d+)-(\d+)', raw)
    if m:
        return {"type": "puhua", "ch": m.group(1), "num": m.group(2), "raw": raw}

    # ── 教材习题ChXX-YY (with specific question number) ──
    m = re.search(r'教材习题\s*Ch(\d+)-([\d.]+)', raw)
    if m:
        return {"type": "chuyi", "ch": m.group(1), "num": m.group(2), "raw": raw}

    # ── 教材习题-对角线规则应用 ──
    if re.search(r'教材习题.*对角线规则', raw):
        return {"type": "chuyi_special", "pattern": "对角线规则", "raw": raw}

    # ── 教材习题-XX-YY ──
    m = re.search(r'教材习题-?(\d+)-(\d+)', raw)
    if m:
        return {"type": "chuyi", "ch": m.group(1), "num": m.group(2), "raw": raw}

    # ── 第XX届初赛/决赛 with sub-question: 第N题(M) or 第N题(M-P) ──
    m = re.search(r'第(\d+)届(初赛|决赛).*?第(\d+)题\((\d+(?:-\d+)*)\)', raw)
    if m:
        return {"type": "zhenti", "year": m.group(1), "comp": m.group(2),
                "qnum": m.group(3), "subq": m.group(4), "raw": raw}

    # ── 第XX届初赛/决赛 with sub-question: 第N场第M题 ──
    m = re.search(r'第(\d+)届(初赛|决赛).*?第(\d+)场.*?第(\d+)题', raw)
    if m:
        return {"type": "zhenti", "year": m.group(1), "comp": m.group(2),
                "qnum": m.group(4), "raw": raw}

    # ── 第XX届初赛/决赛 QN ──
    m = re.search(r'第(\d+)届(初赛|决赛).*?[Qq](\d+)', raw)
    if m:
        return {"type": "zhenti", "year": m.group(1), "comp": m.group(2),
                "qnum": m.group(3), "raw": raw}

    # ── 第XX届初赛/决赛 (year only, no Q number) ──
    m = re.search(r'第(\d+)届(初赛|决赛)', raw)
    if m:
        return {"type": "zhenti_noq", "year": m.group(1), "comp": m.group(2), "raw": raw}

    # ── XX届初赛/决赛 QN (without 第) ──
    m = re.search(r'(\d+)[届](初赛|决赛).*?[Qq](\d+)', raw)
    if m:
        return {"type": "zhenti", "year": m.group(1), "comp": m.group(2),
                "qnum": m.group(3), "raw": raw}

    # ── 初赛讲义X.XX ──
    m = re.search(r'初赛讲义\s*(\d+\.\d+)', raw)
    if m:
        return {"type": "jiangyi", "num": m.group(1), "raw": raw}

    # ── 赵鑫光 (any pattern) ──
    if re.search(r'赵鑫光', raw):
        return {"type": "zhaoxinguang", "raw": raw}

    # ── 汇智 (any pattern) ──
    if re.search(r'汇智', raw):
        return {"type": "huizhi", "raw": raw}

    # ── 《无机化学例题与习题》with specific question: 习题XX.YY or 教N ──
    m = re.search(r'无机化学例题与习题.*?习题(\d+)\.(\d+)', raw)
    if m:
        return {"type": "chuyi_puhua", "ch": m.group(1), "num": m.group(2), "raw": raw}
    m = re.search(r'无机化学例题与习题.*?教(\d+)', raw)
    if m:
        return {"type": "chuyi_generic", "num": m.group(1), "raw": raw}
    # Generic 《无机化学例题与习题》 without specific question
    if re.search(r'无机化学例题与习题', raw):
        return None  # too vague, skip

    # ── 《普通化学原理》with specific exercise: 习题XX.YY ──
    m = re.search(r'普通化学原理.*?习题(\d+)\.(\d+)', raw)
    if m:
        ch = m.group(1)
        num = m.group(2)
        # Map to 题库/化学原理/ChXX-*/XX-YY.md (zero-padded)
        num_padded = num.zfill(2)
        return {"type": "puhua_ex", "ch": ch, "num": num_padded, "raw": raw}
    # 《普通化学原理》with Ch.XX例题 or Ch.XX内容
    m = re.search(r'普通化学原理.*?Ch\.?(\d+)', raw)
    if m:
        return None  # chapter-level reference, too vague
    if re.search(r'普通化学原理', raw):
        return None  # too vague

    # ── Anything with 教N pattern (generic textbook) ──
    m = re.search(r'教(\d+)', raw)
    if m:
        return {"type": "chuyi_generic", "num": m.group(1), "raw": raw}

    # ── 讲义 with specific number ──
    m = re.search(r'讲义\s*(\d+\.\d+)', raw)
    if m:
        return {"type": "jiangyi", "num": m.group(1), "raw": raw}

    # Unrecognized reference - skip silently
    return None


# ── Source reference → file path resolution ──────────────────────────────────

def resolve_source_files(ref: dict) -> list[str]:
    """
    Resolve a source reference dict to actual vault file paths.
    Returns list of absolute paths (may be empty if not found).
    """
    if ref is None:
        return []

    rtype = ref["type"]

    if rtype == "tiku":
        ch, num = ref["ch"], ref["num"]
        pattern = str(VAULT / f"04-题库/化学原理/Ch{ch}-*/{ch}-{num}.md")
        return glob.glob(pattern)

    elif rtype == "puhua":
        ch, num = ref["ch"], ref["num"]
        pattern = str(VAULT / f"04-题库/化学原理/Ch{ch}-*/{ch}-{num}.md")
        return glob.glob(pattern)

    elif rtype == "puhua_ex":
        # 《普通化学原理》习题XX.YY → 04-题库/化学原理/ChXX-*/XX-YY.md
        ch, num = ref["ch"], ref["num"]
        pattern = str(VAULT / f"04-题库/化学原理/Ch{ch}-*/{ch}-{num}.md")
        return glob.glob(pattern)

    elif rtype == "chuyi":
        ch, num = ref["ch"], ref["num"]
        results = []
        # Try exact match in 习题/ with range patterns like 5.1-5.10
        pattern1 = str(VAULT / f"04-题库/教材习题/无机化学例题与习题/Ch{ch}-*/习题/{num}*.md")
        results.extend(glob.glob(pattern1))
        # Try exact match in 例题/
        pattern2 = str(VAULT / f"04-题库/教材习题/无机化学例题与习题/Ch{ch}-*/例题/例{num}*.md")
        results.extend(glob.glob(pattern2))
        # Try broader match
        pattern3 = str(VAULT / f"04-题库/教材习题/无机化学例题与习题/Ch{ch}-*/**/{num}*.md")
        results.extend(glob.glob(pattern3))
        return list(set(results))

    elif rtype == "chuyi_puhua":
        # 《无机化学例题与习题》习题XX.YY → find file containing this exercise
        ch, num = ref["ch"], ref["num"]
        results = []
        # Files are named like 5.1-5.10-选择题.md, need to find which range contains num
        base = VAULT / f"04-题库/教材习题/无机化学例题与习题/Ch{ch}-*"
        for d in glob.glob(str(base)):
            for sub in ["习题", "例题", ""]:
                pat = str(Path(d) / sub / "*.md") if sub else str(Path(d) / "*.md")
                for f in glob.glob(pat):
                    fname = Path(f).stem
                    # Check if this file's range contains the exercise number
                    # Pattern: N.M-N.K-description.md or 例N.M-description.md
                    range_m = re.search(r'(\d+)\.(\d+)-(\d+)\.(\d+)', fname)
                    if range_m:
                        start = int(range_m.group(2))
                        end = int(range_m.group(4))
                        if start <= int(num) <= end:
                            results.append(f)
        return results

    elif rtype == "chuyi_special":
        pattern = str(VAULT / "04-题库/教材习题/无机化学例题与习题/**/*对角线*.md")
        return glob.glob(pattern)

    elif rtype in ("zhenti",):
        year, comp, qnum = ref["year"], ref["comp"], ref["qnum"]
        year_padded = year.zfill(3)
        results = []
        base_dir = VAULT / f"04-题库/真题/第{year}届{comp}"
        if base_dir.exists():
            pattern1 = str(base_dir / "**" / f"题-{year_padded}-{qnum}-*.md")
            results.extend(glob.glob(pattern1, recursive=True))
            pattern2 = str(base_dir / "**" / f"题-{year_padded}-{qnum}.md")
            results.extend(glob.glob(pattern2, recursive=True))
        return list(set(results))

    elif rtype == "zhenti_noq":
        # Year-level reference without specific question number
        # Skip - too vague to resolve to specific files
        return []

    elif rtype == "jiangyi":
        num = ref["num"]
        pattern = str(VAULT / f"04-题库/教材习题/化学竞赛初赛讲义/*-习题{num}.md")
        return glob.glob(pattern)

    elif rtype in ("zhaoxinguang", "huizhi"):
        return []

    elif rtype == "chuyi_generic":
        num = ref["num"]
        pattern = str(VAULT / f"04-题库/教材习题/无机化学例题与习题/**/教{num}*.md")
        return glob.glob(pattern)

    elif rtype == "puhua_generic":
        num = ref["num"]
        pattern = str(VAULT / f"04-题库/化学原理/**/{num}.md")
        return glob.glob(pattern)

    return []


# ── Frontmatter manipulation ─────────────────────────────────────────────────

def get_frontmatter(content: str) -> tuple[str, str, str]:
    """
    Split content into (before_frontmatter, frontmatter_body, after_frontmatter).
    If no frontmatter, returns ('', '', content).
    """
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            frontmatter_body = content[3:end].strip()
            after = content[end + 3:]
            return ('---\n', frontmatter_body, after)
    return ('', '', content)


def has_used_in(frontmatter_body: str, tag: str) -> bool:
    """Check if the frontmatter already has a used_in entry with this tag."""
    # Match used_in: [...] and check if tag is already in the list
    m = re.search(r'used_in:\s*\[([^\]]*)\]', frontmatter_body)
    if m:
        existing_tags = [t.strip().strip('"').strip("'") for t in m.group(1).split(',')]
        return tag in existing_tags
    return False


def add_used_in_tag(content: str, tag: str) -> str:
    """
    Add a used_in tag to the frontmatter.
    If used_in already exists as a list, append the tag.
    If used_in doesn't exist, add it after the last existing field.
    Returns the modified content.
    """
    before, fm_body, after = get_frontmatter(content)

    if not fm_body:
        # No frontmatter - this shouldn't happen for our source files
        return content

    # Check if used_in already exists
    m = re.search(r'used_in:\s*\[([^\]]*)\]', fm_body)
    if m:
        # Append to existing list
        existing = m.group(1).strip()
        if existing:
            new_used_in = f'used_in: [{existing}, {tag}]'
        else:
            new_used_in = f'used_in: [{tag}]'
        fm_body = fm_body[:m.start()] + new_used_in + fm_body[m.end():]
    else:
        # Add new used_in field - insert before the closing or at end
        # Try to insert after 'tags:' line if it exists
        tags_match = re.search(r'(tags:.*?\n)', fm_body)
        if tags_match:
            insert_pos = tags_match.end()
            fm_body = fm_body[:insert_pos] + f'used_in: [{tag}]\n' + fm_body[insert_pos:]
        else:
            # Append at end of frontmatter
            fm_body = fm_body.rstrip() + f'\nused_in: [{tag}]\n'

    return before + fm_body + '\n---' + after


# ── Main logic ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Add used_in frontmatter tags to source files referenced by exercise groups."
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without modifying files.')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed resolution info for each reference.')
    args = parser.parse_args()

    # Collect all source → file mappings
    # Key: absolute path to source file
    # Value: set of used_in tags to add
    file_tags: dict[str, set[str]] = {}
    skipped_refs: list[dict] = []
    unresolved_refs: list[dict] = []

    for group in EXERCISE_GROUPS:
        group_path = str(VAULT / group["path"])
        used_in_tag = group["used_in"]

        print(f"\n{'='*60}")
        print(f"Processing: {group['path']}")
        print(f"  used_in tag: {used_in_tag}")
        print(f"{'='*60}")

        refs = parse_source_index(group_path)
        print(f"  Found {len(refs)} source references in index table")

        for entry in refs:
            ref = entry["source_ref"]
            qid = entry["question_id"]
            raw = entry["source_raw"]

            if ref is None:
                skipped_refs.append({
                    "group": used_in_tag,
                    "qid": qid,
                    "raw": raw,
                    "reason": "self-authored or lecture-only",
                })
                if args.verbose:
                    print(f"  [SKIP] Q{qid}: {raw} → self-authored/lecture-only")
                continue

            if ref["type"] in ("zhaoxinguang", "huizhi"):
                skipped_refs.append({
                    "group": used_in_tag,
                    "qid": qid,
                    "raw": raw,
                    "reason": f"no individual source file ({ref['type']})",
                })
                if args.verbose:
                    print(f"  [SKIP] Q{qid}: {raw} → no individual source file")
                continue

            resolved = resolve_source_files(ref)

            if not resolved:
                unresolved_refs.append({
                    "group": used_in_tag,
                    "qid": qid,
                    "raw": raw,
                    "ref": ref,
                })
                if args.verbose:
                    print(f"  [MISS] Q{qid}: {raw} → no matching file found")
                continue

            for fpath in resolved:
                if fpath not in file_tags:
                    file_tags[fpath] = set()
                file_tags[fpath].add(used_in_tag)

            if args.verbose:
                rel_paths = [os.path.relpath(p, str(VAULT)) for p in resolved]
                print(f"  [HIT]  Q{qid}: {raw} → {rel_paths}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"  Files to modify:     {len(file_tags)}")
    print(f"  Skipped references:  {len(skipped_refs)}")
    print(f"  Unresolved references: {len(unresolved_refs)}")

    if skipped_refs:
        print(f"\n  Skipped (self-authored/lecture-only/no source file):")
        for s in skipped_refs:
            print(f"    [{s['group']}] Q{s['qid']}: {s['raw']} → {s['reason']}")

    if unresolved_refs:
        print(f"\n  Unresolved (no matching file found):")
        for u in unresolved_refs:
            print(f"    [{u['group']}] Q{u['qid']}: {u['raw']}")
            if args.verbose:
                print(f"      ref: {u['ref']}")

    if not file_tags:
        print("\n  No files to modify. Exiting.")
        return

    # Show planned changes
    print(f"\n  Planned changes ({len(file_tags)} files):")
    for fpath in sorted(file_tags.keys()):
        rel = os.path.relpath(fpath, str(VAULT))
        tags = sorted(file_tags[fpath])
        content = read_file(fpath)
        _, fm_body, _ = get_frontmatter(content)

        # Check which tags are actually new
        new_tags = [t for t in tags if not has_used_in(fm_body, t)]
        existing_tags = [t for t in tags if has_used_in(fm_body, t)]

        status_parts = []
        if new_tags:
            status_parts.append(f"+ADD {new_tags}")
        if existing_tags:
            status_parts.append(f"SKIP {existing_tags} (already present)")
        status = ", ".join(status_parts)
        print(f"    {rel}: {status}")

    if args.dry_run:
        print("\n  [DRY RUN] No files were modified.")
        return

    # Apply changes
    modified_count = 0
    for fpath in sorted(file_tags.keys()):
        tags = sorted(file_tags[fpath])
        content = read_file(fpath)
        _, fm_body, _ = get_frontmatter(content)

        new_tags = [t for t in tags if not has_used_in(fm_body, t)]
        if not new_tags:
            continue

        for tag in new_tags:
            content = add_used_in_tag(content, tag)

        write_file(fpath, content)
        modified_count += 1

        rel = os.path.relpath(fpath, str(VAULT))
        print(f"  [DONE] {rel}: added {new_tags}")

    print(f"\n  Modified {modified_count} files.")


if __name__ == "__main__":
    main()
