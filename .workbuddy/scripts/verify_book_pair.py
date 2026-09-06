# -*- coding: utf-8 -*-
"""
习题书双版本题头对账闸门（md 层全量 + docx 层全量）

校验：
  1. md 层：教师版/学生版逐章题头数（## N.M 标题）一致；学生版 0 答案 details；
     教师版每章 details 数 == 题头数。
  2. docx 层：双版本每章 docx 中 Heading 2 且形如 N.M 的段落数一致，且与 md 层相等。

用法： python verify_book_pair.py
退出码：0 = 全部一致；1 = 存在不一致。
"""
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

VAULT = Path(r"C:\Obsidion\妙妙屋")
TEACHER_MD = VAULT / "04-课件" / "习题集" / "习题书-教师版"
STUDENT_MD = VAULT / "04-课件" / "习题集" / "习题书-学生版"
TEACHER_DOCX = VAULT / "00-首页" / "题组Word" / "习题书" / "教师版"
STUDENT_DOCX = VAULT / "00-首页" / "题组Word" / "习题书" / "学生版"

HEAD_RE = re.compile(r"^## (\d+\.\d+) ", re.M)
ANS_RE = re.compile(r"<details>")
DOCX_HEAD_RE = re.compile(r"^\d+\.\d+ ")

fails = []


def md_stats(root: Path):
    """返回 {(篇, 章): (题头数, details数)}，排除 目录.md 与 来源索引.md。"""
    out = {}
    for part_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        for f in sorted(part_dir.glob("*.md")):
            if f.name == "目录.md":
                continue
            text = f.read_text(encoding="utf-8")
            out[(part_dir.name, f.stem)] = (
                len(HEAD_RE.findall(text)),
                len(ANS_RE.findall(text)),
            )
    return out


def docx_heads(path: Path) -> int:
    """docx 中 Heading 2 且形如 N.M 的段落数（题头）。"""
    from docx import Document

    doc = Document(str(path))
    return sum(
        1
        for p in doc.paragraphs
        if p.style.name == "Heading 2" and DOCX_HEAD_RE.match(p.text.strip())
    )


def main():
    tm, sm = md_stats(TEACHER_MD), md_stats(STUDENT_MD)
    if set(tm) != set(sm):
        only_t = set(tm) - set(sm)
        only_s = set(sm) - set(tm)
        fails.append(f"章节集合不一致: 仅教师版={sorted(only_t)} 仅学生版={sorted(only_s)}")

    t_total = s_total = 0
    print(f"{'篇/章':<40} {'md师':>5} {'md生':>5} {'det师':>5} {'det生':>5} {'docx师':>6} {'docx生':>6}")
    for key in sorted(set(tm) & set(sm)):
        th, ta = tm[key]
        sh, sa = sm[key]
        t_total += th
        s_total += sh
        tdx = docx_heads(TEACHER_DOCX / key[0] / f"{key[1]}.docx")
        sdx = docx_heads(STUDENT_DOCX / key[0] / f"{key[1]}.docx")
        bad = th != sh or ta != th or sa != 0 or tdx != th or sdx != sh
        if bad:
            fails.append(f"{key}: md师={th} md生={sh} det师={ta} det生={sa} docx师={tdx} docx生={sdx}")
        flag = " ❌" if bad else ""
        print(f"{key[0]}/{key[1]:<24} {th:>5} {sh:>5} {ta:>5} {sa:>5} {tdx:>6} {sdx:>6}{flag}")

    print("-" * 80)
    print(f"md 题头合计: 教师版 {t_total} / 学生版 {s_total}")
    if t_total != s_total:
        fails.append(f"总题头数不一致: 教师版 {t_total} vs 学生版 {s_total}")
    if fails:
        print(f"\n❌ {len(fails)} 处不一致：")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("✅ 双版本题头逐文件一致；学生版 0 答案块；教师版答案块=题头数；docx 层一致。")


if __name__ == "__main__":
    main()
