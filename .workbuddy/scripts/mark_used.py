#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
出卷后回填 `used_in`，把「选题 → 出卷 → 标记已用」的闭环补上。

不回填的话，组卷工作台里的 EXCLUDE_USED 就是摆设（目前全库只有 8.2% 的题目带 used_in）。

用法：
    python mark_used.py --paper "06-讲义输出/2026秋期中卷.md"          # dry-run
    python mark_used.py --paper "06-讲义输出/2026秋期中卷.md" --write   # 落盘
    python mark_used.py --list selected.txt --tag "2026秋-期中卷"       # 从路径清单读

行为：
  · 解析试卷文件里的 wikilink，只取指向 04-题库 / 05-真题库 的题目文件
  · 给每题的 used_in 追加该卷（已存在则跳过，自动去重）
  · **写成 wikilink**（used_in: "[[卷名]]"）—— 沿用本库既有约定，
    好处是试卷文件里能看到反向链接；也因此 dataview 里它是 Link 对象，没有 .length
  · 单值写标量、多值写数组，与现有 344 条保持一致
  · 行级原地改值，不重新序列化 YAML —— diff 最小
  · 严格保留原行尾（本库是混合行尾，插入新行会按邻居风格补 \\r）

安全：默认 dry-run 不写盘；确认无误再加 --write。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")
Q_DIRS = ("04-题库", "05-真题库")

WIKILINK = re.compile(r"\[\[([^\]\|#]+)(?:[#\|][^\]]*)?\]\]")


def read_raw(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_raw(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def fm_range(lines: list[str]):
    """返回 frontmatter 结束行的下标（第二个 ---）；没有则返回 None。"""
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i
    return None


def find_key_line(lines: list[str], fm_end: int, field: str):
    """用 ^field: 锚定。注意 ^used_in: 不会误匹配别的字段。"""
    pat = re.compile(rf"^{re.escape(field)}\s*:")
    for idx in range(1, fm_end):
        if pat.match(lines[idx]):
            return idx
    return None


def fm_type(lines: list[str], fm_end: int) -> str:
    """取 frontmatter 的 type 值。题库目录下混着索引/系统/答案等非题目文件，
    只按路径前缀过滤会把 README.md 一类也写进去 —— 必须再过一道 type 白名单。"""
    idx = find_key_line(lines, fm_end, "type")
    if idx is None:
        return ""
    return lines[idx].split(":", 1)[1].strip().strip('"').strip("'")


def line_term(line: str) -> str:
    return "\r" if line.endswith("\r") else ""


def term_at(lines: list[str], idx: int) -> str:
    if idx < len(lines):
        return line_term(lines[idx])
    return line_term(lines[-1]) if lines else ""


def yq(s: str) -> str:
    """YAML 行内标量引号处理：只在必要时加引号。"""
    if s == "":
        return '""'
    if re.search(r'[\[\]:#{}&*!|>%@`",\n]', s) or s != s.strip():
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def render_inline(field: str, items: list[str]) -> str:
    return f"{field}: [{', '.join(yq(i) for i in items)}]"


def norm_tag(t: str) -> str:
    """把 tag 归一成裸名：去引号、去 [[ ]]、去别名/锚点。用于去重比较。"""
    t = str(t).strip().strip('"').strip("'").strip()
    if t.startswith("[["):
        t = t[2:]
    if t.endswith("]]"):
        t = t[:-2]
    return t.split("|")[0].split("#")[0].strip()


def render_used_in(names: list[str]) -> str:
    """单值写标量（沿用现有约定），多值写数组。值一律是 wikilink。"""
    links = [f"[[{n}]]" for n in names]
    if len(links) == 1:
        return f'used_in: "{links[0]}"'
    return render_inline("used_in", links)


def parse_used_in(value: str) -> list[str]:
    """把 `used_in: [a, b]` 或 `used_in: "a"` 的值解析成列表。"""
    v = value.strip()
    if not v:
        return []
    if v.startswith("["):
        inner = v[1:].rstrip()
        if inner.endswith("]"):
            inner = inner[:-1]
        out, buf, in_q, q = [], "", False, ""
        for ch in inner:
            if in_q:
                if ch == q:
                    in_q = False
                else:
                    buf += ch
            elif ch in "\"'":
                in_q, q = True, ch
            elif ch == ",":
                if t := buf.strip():
                    out.append(t)
                buf = ""
            else:
                buf += ch
        if t := buf.strip():
            out.append(t)
        return out
    # 标量：去掉可能的引号
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return [v] if v else []


def resolve_target(raw: str) -> Path | None:
    """把 wikilink 目标解析成题目文件路径。"""
    t = raw.strip().replace("\\", "/")
    if t.endswith(".md"):
        t = t[:-3]
    cand = VAULT / f"{t}.md"
    if cand.exists():
        return cand
    # 只写了文件名（Obsidian 最短路径写法）→ 在两个题库里找
    base = Path(t).name
    hits = []
    for d in Q_DIRS:
        hits.extend((VAULT / d).rglob(f"{base}.md"))
    return hits[0] if len(hits) == 1 else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", help="试卷文件路径（解析其中的 wikilink）")
    ap.add_argument("--list", help="题目路径清单文件（每行一个，相对 vault 根）")
    ap.add_argument("--tag", help="写入 used_in 的卷名；省略则取试卷文件名（去掉 .md）")
    ap.add_argument("--write", action="store_true", help="实写（默认 dry-run）")
    args = ap.parse_args()

    if not args.paper and not args.list:
        ap.error("需要 --paper 或 --list")

    # ── 收集目标文件 ──
    targets: list[Path] = []
    unresolved: list[str] = []

    if args.paper:
        paper = VAULT / args.paper.replace("\\", "/")
        if not paper.exists():
            sys.exit(f"试卷文件不存在：{paper}")
        for raw in WIKILINK.findall(read_raw(paper)):
            if not any(raw.strip().startswith(d) for d in Q_DIRS) and "/" in raw:
                continue  # 明确写了路径但不在这两个目录 → 不是题目
            p = resolve_target(raw)
            if p is None:
                unresolved.append(raw)
            elif p not in targets:
                targets.append(p)

    if args.list:
        lp = VAULT / args.list.replace("\\", "/")
        for line in read_raw(lp).split("\n"):
            line = line.strip().lstrip("-0123456789. ").strip()
            if not line or line.startswith("#"):
                continue
            m = WIKILINK.search(line)
            raw = m.group(1) if m else line
            p = resolve_target(raw)
            if p is None:
                unresolved.append(raw)
            elif p not in targets:
                targets.append(p)

    if unresolved:
        print(f"⚠️ 无法解析 {len(unresolved)} 个链接（前 5 条）：")
        for u in unresolved[:5]:
            print(f"     {u}")

    if not targets:
        sys.exit("没有找到任何题目文件，退出。")

    # ── 卷名：省略 --tag 时取试卷文件名，保证 used_in 与试卷文件严格对得上 ──
    tag_is_uniq_short = False   # tag 为短链且 vault 内 basename 唯一 → 允许按末段等价判定已有
    if args.tag:
        tag = norm_tag(args.tag)
        tag_is_uniq_short = "/" not in tag and len(list(VAULT.rglob(tag + ".md"))) == 1
    elif args.paper:
        tag = Path(args.paper.replace("\\", "/")).stem
        # 撞名消歧（2026-09-05）：vault 中同 basename 存在多份文件（如题库侧智能卷与
        # 课件侧正式卷同名）时，短链 [[卷名]] 解析有歧义 → 自动升级为相对 vault 全路径。
        if len(list(VAULT.rglob(tag + ".md"))) > 1:
            tag = args.paper.replace("\\", "/").strip("/")
            if tag.endswith(".md"):
                tag = tag[:-3]
            print(f"ℹ️ basename「{Path(tag).stem}」在库中不唯一，used_in 写全路径：[[{tag}]]")
        else:
            tag_is_uniq_short = True
    else:
        sys.exit("用 --list 时必须显式给 --tag（清单文件没有可供推断的卷名）")
    if not tag:
        sys.exit("卷名为空，退出。")

    print(f"解析到 {len(targets)} 个链接目标（非题目文件会在下面逐条跳过），卷名 = [[{tag}]]")
    print("─" * 60)

    n_new = n_skip = n_err = n_notq = 0
    for p in targets:
        try:
            text = read_raw(p)
            lines = text.split("\n")
            fm_end = fm_range(lines)
            if fm_end is None:
                print(f"  !! 无 frontmatter，跳过：{p.relative_to(VAULT).as_posix()}")
                n_err += 1
                continue

            ftype = fm_type(lines, fm_end)
            if ftype not in ("题目", "真题"):
                print(f"  -- 非题目文件（type={ftype or '空'}），跳过："
                      f"{p.relative_to(VAULT).as_posix()}")
                n_notq += 1
                continue

            idx = find_key_line(lines, fm_end, "used_in")
            if idx is None:
                cur: list[str] = []
            else:
                raw_v = lines[idx].split(":", 1)[1].rstrip("\r")
                cur = [norm_tag(x) for x in parse_used_in(raw_v)]
                cur = [x for x in cur if x]

            # 已有判定：字面相等，或（tag 为唯一短链时）已有值末段与之相同——
            # basename 唯一保证末段相同必为同一文件，全路径旧值可安全识别（2026-09-05）
            if tag in cur or (
                tag_is_uniq_short
                and any(x.split("/")[-1] == tag for x in cur)
            ):
                n_skip += 1
                continue

            new = cur + [tag]
            rel = p.relative_to(VAULT).as_posix()
            if idx is None:
                # 没有该字段：插到 difficulty 之后，没有则插到 frontmatter 末尾
                anchor = find_key_line(lines, fm_end, "difficulty")
                ins = (anchor + 1) if anchor is not None else fm_end
                lines.insert(ins, render_used_in(new) + term_at(lines, ins))
                action = f'新增 {render_used_in(new)}'
            else:
                lines[idx] = render_used_in(new) + line_term(lines[idx])
                action = f"追加 → {render_used_in(new)}"

            if args.write:
                write_raw(p, "\n".join(lines))
            n_new += 1
            print(f"  ✓ {rel}\n      {action}")
        except Exception as e:
            n_err += 1
            print(f"  !! {p.name}: {type(e).__name__}: {e}")

    print("─" * 60)
    print(f"将写入 {n_new} ｜ 已有该 tag 跳过 {n_skip} ｜ 非题目跳过 {n_notq} ｜ 异常 {n_err}")
    print("已实写。" if args.write else "这是 DRY-RUN，加 --write 才落盘。")


if __name__ == "__main__":
    main()
