#!/usr/bin/env python3
"""fix_tags_yaml.py — 修复 KP frontmatter 中 `tags: [X]` + 缩进块列表 的 YAML 损坏。

问题模式（YAML 语法错误，导致 aliases 等字段无法被解析）：
  tags: [化竞]      ← flow 列表
    - 知识点          ← 遗留的块列表项
    - 化学原理
修复为：
  tags: [化竞, 知识点, 化学原理]

同时也修复 pass1 曾产生的粘连（tags: [..]key: / tags: [..]---）：
  tags: [化竞, 知识点]related: [...]
→
  tags: [化竞, 知识点]
  related: [...]

用法：
  python fix_tags_yaml.py            # 实际修复（排除 .obsidian/.claude/kb-vault-mcp 等）
  python fix_tags_yaml.py --dry-run  # 只预览不改动
"""
import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent.parent

# 排除目录（不应触碰系统/工具目录）
EXCLUDE_PREFIXES = (
    ".obsidian", ".claude", ".git", "node_modules", "kb-vault-mcp",
    "09-审计报告", "06-外部资料导入", "00-首页", "11-模板", "02-数据库",
)

# pass1：`tags: [X]` 后紧跟的缩进块列表
TAGS_BLOCK_PAT = re.compile(
    r"(?m)^(\s*tags:\s*\[[^\]]*\])\n"
    r"((?:\s+-\s+[^\n]+(?:\n|$))+)"
)
# pass2：`tags: [...]` 后紧贴非换行内容（粘连的 key: 或 ---）
GLUED_PAT = re.compile(r"(?m)^(\s*tags:\s*\[[^\]]*\])(?!\n)")


def parse_flow_items(text: str) -> list[str]:
    """解析 tags: [a, b, c] → ['a','b','c']（去引号、去空白）。"""
    inner = text[text.index("[") + 1:text.rindex("]")]
    items = []
    for raw in inner.split(","):
        item = raw.strip().strip('"').strip("'")
        if item:
            items.append(item)
    return items


def fix_content(content: str) -> tuple[str, int, bool]:
    """修复一个文件的 tags 块，返回 (新内容, 修复块数, 是否变更)。"""
    changed = False
    fixed = 0

    def repl(m: "re.Match[str]") -> str:
        nonlocal changed, fixed
        flow_line = m.group(1)
        block = m.group(2)
        items = parse_flow_items(flow_line)
        block_items = []
        for line in block.split("\n"):
            line = line.strip()
            if line.startswith("-") and len(line) > 1:
                item = line[1:].strip().strip('"').strip("'")
                if item:
                    block_items.append(item)
        if not block_items:
            return m.group(0)
        merged = list(items)
        for item in block_items:
            if item not in merged:
                merged.append(item)
        changed = True
        fixed += 1
        # 必须保留尾部换行，否则会粘连下一行（related:/--- 等）
        return "tags: [" + ", ".join(merged) + "]\n"

    content = TAGS_BLOCK_PAT.sub(repl, content)

    # pass2：修复粘连（tags: [..]key: 或 tags: [..]---）
    if GLUED_PAT.search(content):
        content = GLUED_PAT.sub(r"\1\n", content)
        changed = True
        fixed += 1

    return content, fixed, changed


def main() -> None:
    dry = "--dry-run" in sys.argv
    total_files = 0
    total_fixed = 0
    samples = []
    for f in sorted(VAULT_ROOT.rglob("*.md")):
        rel = f.relative_to(VAULT_ROOT).as_posix()
        if any(rel.startswith(p) for p in EXCLUDE_PREFIXES):
            continue
        try:
            content = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if not (TAGS_BLOCK_PAT.search(content) or GLUED_PAT.search(content)):
            continue
        new_content, fixed, changed = fix_content(content)
        if not changed:
            continue
        total_files += 1
        total_fixed += fixed
        if len(samples) < 12:
            samples.append(rel)
        if not dry:
            if "\r\n" in content:
                out = new_content.replace("\n", "\r\n")
            else:
                out = new_content
            try:
                f.write_text(out, encoding="utf-8", newline="")
            except OSError as e:
                print(f"  !! 写入失败: {rel}: {e}", file=sys.stderr)
    print(f"{'[DRY-RUN] ' if dry else ''}修复文件数: {total_files}, 修复块数: {total_fixed}")
    for s in samples:
        print(f"  {s}")


if __name__ == "__main__":
    main()
