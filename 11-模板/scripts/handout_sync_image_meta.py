# -*- coding: utf-8 -*-
"""按正文实际图片数重算讲义 frontmatter 的 image_count / has_images。

要点：
1. 统计时排除 HTML 注释区与代码围栏——注释里的图不导出，不应计数。
2. 写前必须查 frontmatter 重复键（重复键会让整条文件在 Obsidian 消失，P0）。
3. 字面替换，不做 YAML 回写，保留原有格式与注释。
4. 拼回用「首行 --- + fm 行 + 闭合 --- 行 + body」，不用字节偏移。

用法:
    python -X utf8 11-模板/scripts/handout_sync_image_meta.py [--apply]
默认 dry-run。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "04-课件" / "学生讲义"

def iter_sources():
    """递归采集讲义源（按模块分子目录后），排除 _归档 与 _ 开头的辅助目录。"""
    for p in sorted(SRC.rglob("*.md")):
        rel = p.relative_to(SRC)
        if "_归档" in rel.parts or rel.parts[0].startswith("_"):
            continue
        yield p



IMG = re.compile(r"!\[\[([^\]\|\n]+)")
KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:")


def mask(lines: list[str]) -> list[str]:
    """置空代码围栏与 HTML 注释区内的行。"""
    out: list[str] = []
    in_fence = False
    in_comment = False
    for L in lines:
        if L.strip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        s = L
        if in_comment:
            out.append("")
            if "-->" in s:
                in_comment = False
            continue
        if "<!--" in s:
            if "-->" not in s or s.index("-->") < s.index("<!--"):
                in_comment = True
            out.append("")
            continue
        out.append("" if in_fence else L)
    return out


def split_fm(lines: list[str]) -> int | None:
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i
    return None


def eol_of(lines: list[str]) -> str:
    for l in lines:
        if l.endswith("\r\n"):
            return "\r\n"
        if l.endswith("\n"):
            return "\n"
    return "\n"


def process(path: Path, apply: bool) -> tuple[int, str]:
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    lines = text.splitlines(keepends=True)
    e = split_fm(lines)
    if e is None:
        return 0, "无 frontmatter"

    fm, body = lines[1:e], lines[e + 1:]
    n = len(IMG.findall("".join(mask(body))))

    keys = [m.group(1) for m in (KEY.match(l) for l in fm) if m]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        return 0, "重复键 %s（跳过）" % ",".join(dup)

    eol = eol_of(lines)
    new_fm: list[str] = []
    changed = 0
    seen_img = False
    seen_has = False
    for L in fm:
        stripped = L.rstrip("\r\n")
        if re.match(r"^image_count\s*:", stripped):
            val = "image_count: %d" % n
            seen_img = True
            if val != stripped:
                changed += 1
                new_fm.append(val + eol)
            else:
                new_fm.append(L)
            continue
        if re.match(r"^has_images\s*:", stripped):
            val = "has_images: %s" % ("true" if n > 0 else "false")
            seen_has = True
            if val != stripped:
                changed += 1
                new_fm.append(val + eol)
            else:
                new_fm.append(L)
            continue
        new_fm.append(L)
    if not seen_img:
        new_fm.append("image_count: %d%s" % (n, eol))
        changed += 1
    if not seen_has:
        new_fm.append("has_images: %s%s" % ("true" if n > 0 else "false", eol))
        changed += 1

    if changed and apply:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("".join(lines[:1] + new_fm + lines[e:e + 1] + body))
    return changed, "图片 %d 张" % n


def main() -> None:
    apply = "--apply" in sys.argv
    total = 0
    files = 0
    for p in sorted(iter_sources()):
        if p.name == "README.md":
            continue
        c, note = process(p, apply)
        if c:
            files += 1
            total += c
            print("%-52s %s（改 %d 处）" % (p.name, note, c))
        elif "重复键" in note or "无 frontmatter" in note:
            print("%-52s %s" % (p.name, note))
    print("\n合计改 %d 处 / %d 份；模式：%s"
          % (total, files, "APPLY 已写盘" if apply else "DRY-RUN 未写盘"))


if __name__ == "__main__":
    main()
