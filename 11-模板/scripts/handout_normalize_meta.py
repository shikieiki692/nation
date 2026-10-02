# -*- coding: utf-8 -*-
"""讲义元数据归一：补 module（按所在目录）、stage（按有无 docx 产物）、aliases（文件名简写补全称）。

铁律：
1. 写前强制查 frontmatter 重复键（重复键会让整条文件在 Obsidian 消失）
2. 字面替换/追加，不做 YAML 回写
3. 读写 newline=""，保持行尾不变

用法:
    python -X utf8 11-模板/scripts/handout_normalize_meta.py [--apply]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SRC = VAULT / "04-课件" / "学生讲义"
DOC = VAULT / "06-学生侧材料" / "讲义"

MODULES = {"化学原理", "结构化学", "有机化学", "元素与分析"}

# 文件名简写 → title 里的全称（加 alias 让两种写法都能解析，避免改名断链）
ALIAS = {
    "烷烃烯烃炔烃": "烷烃·烯烃·炔烃",
    "醇醚胺酚": "醇·醚·胺·酚",
    "醛酮羧酸": "醛·酮·羧酸及其衍生物",
    "杂环糖氨基酸": "杂环·糖·氨基酸与波谱初步",
}

KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:")


def core(name: str) -> str:
    n = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)
    n = re.sub(r"（(自学完整|课堂填空|Word清稿|完整版)）$", "", n)
    return n.strip()


def fm_range(lines: list[str]) -> tuple[int, int] | None:
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return 0, i
    return None


def eol_of(lines: list[str]) -> str:
    for l in lines:
        if l.endswith("\r\n"):
            return "\r\n"
        if l.endswith("\n"):
            return "\n"
    return "\n"


def process(path: Path, group: str, apply: bool) -> list[str]:
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.read().splitlines(keepends=True)
    rng = fm_range(lines)
    if not rng:
        return []
    s, e = rng
    fm = lines[s + 1:e]
    body = lines[e:]

    keys = [m.group(1) for m in (KEY.match(l) for l in fm) if m]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        print("  [SKIP 重复键] %s: %s" % (path.name, ",".join(dup)))
        return []

    # docx 与 md 同名（含「（自学完整）」等后缀），不能直接套 core() 剥离后缀
    has_docx = any((DOC / cand).exists() for cand in
                   (path.stem + ".docx", core(path.stem) + ".docx"))
    want = {}
    if group in MODULES:
        want["module"] = group
    want["stage"] = "published" if has_docx else "draft"
    if path.stem in ALIAS:
        want["aliases"] = '["%s"]' % ALIAS[path.stem]

    out_fm: list[str] = []
    seen: set[str] = set()
    changed: list[str] = []
    for L in fm:
        m = KEY.match(L)
        if m and m.group(1) in want:
            k = m.group(1)
            seen.add(k)
            old = L.rstrip("\r\n")
            newval = "%s: %s" % (k, want[k])
            if old.strip() != newval:
                changed.append("%s: %s → %s" % (k, old.split(":", 1)[1].strip()[:24], want[k][:30]))
                out_fm.append(newval + eol_of([L]))
            else:
                out_fm.append(L)
            continue
        out_fm.append(L)
    eol = eol_of(lines)
    for k, v in want.items():
        if k not in seen:
            out_fm.append("%s: %s%s" % (k, v, eol))
            changed.append("新增 %s: %s" % (k, v[:30]))

    if changed and apply:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("".join(lines[:s + 1] + out_fm + body))
    return changed


def main() -> None:
    apply = "--apply" in sys.argv
    total = 0
    files = 0
    for p in sorted(SRC.rglob("*.md")):
        rel = p.relative_to(SRC)
        if "_归档" in rel.parts or p.name == "README.md":
            continue
        group = rel.parts[0] if len(rel.parts) > 1 else ""
        ch = process(p, group, apply)
        if ch:
            files += 1
            total += len(ch)
            print("%-52s %s" % (p.name, " | ".join(ch)))
    print("\n合计 %d 处 / %d 份；模式：%s"
          % (total, files, "APPLY" if apply else "DRY-RUN"))


if __name__ == "__main__":
    main()
