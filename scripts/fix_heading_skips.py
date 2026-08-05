# -*- coding: utf-8 -*-
"""标题跳跃修复脚本 (2026-08-04)

修复 validate_kb 报告的"标题跳跃"告警：当前标题级 > 上一标题级 + 1 时，
将该标题降级为 上一标题级 + 1（纯机械，不改标题文本 → wikilink 引用不受影响）。

与 validate_kb.check_headings 的差异：
- 本脚本**识别代码围栏**（``` 与 ~~~），围栏内的 `#` 行不视为标题、不修改，
  避免误改代码注释/示例。

用法:
  python scripts/fix_heading_skips.py            # DRY-RUN：列出将修改的文件与跳级类型
  python scripts/fix_heading_skips.py --apply    # 实际修改（保留原 CRLF/LF）

说明:
  跳级降级会级联处理（前一行被降级后，后续标题按新基准继续判定），
  保证修复后 validate 不再报任何标题跳跃。
"""
import os
import re
import sys

VAULT = r'C:\Obsidion\妙妙屋'
INCLUDE_DIRS = [
    "01-考纲导航", "02-考纲条目", "03-知识点",
    "04-课件", "04-专题与题型", "04-题库",
    "06-学生侧材料", "07-资料提炼", "11-模板", "12-教学洞察",
]
EXCLUDE_PATTERNS = [
    ".obsidian", ".claude", ".git", "__pycache__", "node_modules",
    "09-审计报告", "06-外部资料导入", "00-首页", ".chem_media",
]
EXCLUDE_PATH_PREFIXES = [
    "06-学生侧材料/讲义/media/",
    "07-资料提炼/网课资料/无机化学-新课-周坤-2020-难度适中/笔记/",
    "07-资料提炼/网课资料/无机化学-新课-周坤-2020-难度适中/学生讲义/",
]

HEADING_RE = re.compile(r'^(#{1,6})(\s.*)$')
FENCE_RE = re.compile(r'^(`{3,}|~{3,})')


def is_excluded(rel: str) -> bool:
    for p in EXCLUDE_PATTERNS:
        if rel == p or rel.startswith(p + "/") or "/" + p + "/" in rel:
            return True
    for p in EXCLUDE_PATH_PREFIXES:
        if rel.startswith(p):
            return True
    return False


def collect_md_files():
    out = []
    for d in INCLUDE_DIRS:
        base = os.path.join(VAULT, d)
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [x for x in dirs if not any(
                x == p or x.startswith(p) for p in EXCLUDE_PATTERNS)]
            for fn in files:
                if not fn.endswith('.md'):
                    continue
                fp = os.path.join(root, fn)
                rel = os.path.relpath(fp, VAULT).replace('\\', '/')
                if not is_excluded(rel):
                    out.append((fp, rel))
    return out


def process_file(fp: str, apply: bool):
    """返回 (changes, newline)。changes = [(lineno, old_level, new_level), ...]"""
    with open(fp, 'rb') as f:
        raw = f.read()
    newline = '\r\n' if b'\r\n' in raw else '\n'
    text = raw.decode('utf-8')
    lines = text.split('\n')
    content = [l.rstrip('\r') for l in lines]

    changes = []
    in_code = False
    prev_level = 0
    for i, cl in enumerate(content):
        if FENCE_RE.match(cl.strip()):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEADING_RE.match(cl)
        if not m:
            continue
        level = len(m.group(1))
        if prev_level > 0 and level > prev_level + 1:
            new_level = prev_level + 1
            changes.append((i + 1, level, new_level))
            prev_level = new_level
        else:
            prev_level = level

    if not changes:
        return [], newline
    if apply:
        for i, _, new in changes:
            idx = i - 1  # changes 存 1-indexed 行号，转为 0-indexed
            cl = content[idx]
            m = HEADING_RE.match(cl)
            if m:
                content[idx] = '#' * new + m.group(2)
        out = '\n'.join(content)
        if newline == '\r\n':
            out = out.replace('\n', '\r\n')
        with open(fp, 'w', encoding='utf-8', newline='') as f:
            f.write(out)
    return changes, newline


def main():
    apply = '--apply' in sys.argv
    per_file = {}
    total = 0
    for fp, rel in collect_md_files():
        changes, _ = process_file(fp, apply)
        if changes:
            per_file[rel] = changes
            total += len(changes)

    print(f"{'已修复' if apply else '待修复'}文件: {len(per_file)} 个 · 跳级 {total} 处")
    if not apply:
        from collections import Counter
        c = Counter((a, b) for _, a, b in [f for fs in per_file.values() for f in fs])
        print("跳级类型: " + "；".join(f"{a}#→{b}#×{n}" for (a, b), n in c.most_common()))
        print("\n⚠️ DRY-RUN（未写文件）。加 --apply 执行。")
        for rel in sorted(per_file):
            print(f"  {len(per_file[rel]):3}  {rel}")
        return
    print(f"\n✅ 完成。注意：validate_kb.check_headings 若不识别代码围栏，围栏内 # 行可能仍被误报，需同步修复验证器。")


if __name__ == '__main__':
    main()
