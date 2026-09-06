#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
question_type 批量写入的快照与校验（B6）。

按 heuristic-field-backfill 技能的第 4、5 步：
  打快照 → 写入 → 与快照逐行 diff 校验。

两步用法：
  python qt_write_guard.py snapshot --pending <清单> --zip <快照zip>
  python infer_question_type.py --write
  python qt_write_guard.py verify   --zip <快照zip>

verify 的四项断言（任一失败即列出明细，不通过）：
  1. 文件仍存在且可读
  2. diff 只含 equal / insert，且 insert 恰好 1 行（原地改值的场景会走 replace 1:1）
  3. **行尾风格不变**：改前纯 CRLF → 改后仍是纯 CRLF；改前纯 LF → 改后仍是纯 LF
  4. 被插入的那一行确实是 question_type

第 3 项是本项目的高频事故点：`.gitattributes` 有 `*.md text eol=lf`，
git 会做归一化 —— 所以**不能用 git diff 检测行尾污染**，只能逐字节比快照。
而 `git show HEAD:` 存的就是归一化后的 LF，也不能当基线（详见技能文档）。
"""
from __future__ import annotations

import argparse
import difflib
import sys
import time
import zipfile
from pathlib import Path

VAULT = Path(r"C:\Obsidion\妙妙屋")


def read_bytes(p: Path) -> bytes:
    return p.read_bytes()


def eol_style(b: bytes) -> str:
    crlf, lf = b.count(b"\r\n"), b.count(b"\n")
    if crlf == lf and lf > 0:
        return "CRLF"
    if crlf == 0:
        return "LF"
    return f"混合(CRLF {crlf}/LF {lf})"


def cmd_snapshot(pending: Path, zip_path: Path) -> int:
    rels = [ln.strip() for ln in
            open(pending, encoding="utf-8", newline="").read().split("\n") if ln.strip()]
    missing = [r for r in rels if not (VAULT / r).is_file()]
    if missing:
        print(f"!! 清单里 {len(missing)} 个文件不存在，先修清单")
        for r in missing[:10]:
            print(f"   {r}")
        return 1
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for r in rels:
            z.write(VAULT / r, r)
    print(f"快照完成：{len(rels)} 个文件 → {zip_path}"
          f"（{zip_path.stat().st_size/1024:.0f} KB）")
    return 0


def cmd_verify(zip_path: Path) -> int:
    problems: list[str] = []
    n_ok = n_insert = n_replace = 0

    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        print(f"校验 {len(names)} 个文件…\n")
        for name in names:
            before = z.read(name)
            fp = VAULT / name
            if not fp.is_file():
                problems.append(f"[文件消失] {name}")
                continue
            after = read_bytes(fp)

            if before == after:
                problems.append(f"[未改动] {name}")
                continue

            # 行尾判定分三种情况。混合行尾文件里插入一行，CRLF 与 LF 计数必然
            # 各 +1（若按邻居风格插的是 CRLF）或只 LF +1（插的是 LF），
            # 这都是**正确**行为 —— 不能拿"计数变了"当错误。
            b_crlf, a_crlf = before.count(b"\r\n"), after.count(b"\r\n")
            b_lf, a_lf = before.count(b"\n"), after.count(b"\n")
            d_crlf, d_lf = a_crlf - b_crlf, a_lf - b_lf
            b_style, a_style = eol_style(before), eol_style(after)
            eol_bad = False
            if b_style == "CRLF":
                eol_bad = (a_style != "CRLF")
            elif b_style == "LF":
                eol_bad = (a_style != "LF")
            else:                                    # 混合：允许 +1 行，风格随邻居
                eol_bad = not (d_lf == 1 and d_crlf in (0, 1))
            if eol_bad:
                problems.append(f"[行尾变了 {b_style} → {a_style}] {name}")

            b_lines = before.decode("utf-8").split("\n")
            a_lines = after.decode("utf-8").split("\n")
            sm = difflib.SequenceMatcher(None, b_lines, a_lines, autojunk=False)
            ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
            bad = eol_bad
            for tag, i1, i2, j1, j2 in ops:
                if tag == "insert" and (j2 - j1) == 1:
                    if not a_lines[j1].startswith("question_type:"):
                        problems.append(f"[插入的不是 question_type] {name}: {a_lines[j1][:60]}")
                        bad = True
                    else:
                        # 插入行的行尾必须与该位置原有邻居一致
                        ref = a_lines[j1 - 1] if j1 > 0 else (
                            a_lines[j1 + 1] if j1 + 1 < len(a_lines) else "")
                        want = "\r" if ref.endswith("\r") else ""
                        got = "\r" if a_lines[j1].endswith("\r") else ""
                        if want != got:
                            problems.append(
                                f"[插入行行尾与邻居不符 邻居{'' if want else '无'}CR] {name}")
                            bad = True
                        n_insert += 1
                elif tag == "replace" and (i2 - i1) == 1 and (j2 - j1) == 1:
                    if not a_lines[j1].startswith("question_type:"):
                        problems.append(f"[改写的不是 question_type] {name}: {a_lines[j1][:60]}")
                        bad = True
                    else:
                        n_replace += 1
                else:
                    problems.append(f"[异常 diff {tag} {i1}:{i2}→{j1}:{j2}] {name}")
                    bad = True
            if not bad:
                n_ok += 1

    print(f"  通过 {n_ok}   插入 {n_insert}   原地改写 {n_replace}")
    if problems:
        print(f"\n!! {len(problems)} 处异常：")
        for p in problems[:30]:
            print(f"   {p}")
        if len(problems) > 30:
            print(f"   …共 {len(problems)} 处")
        return 1
    print("\n✓ 全部通过：改动只含 question_type 的单行插入/改写，行尾风格零变化。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("snapshot")
    s.add_argument("--pending", required=True)
    s.add_argument("--zip", default="")

    v = sub.add_parser("verify")
    v.add_argument("--zip", required=True)

    args = ap.parse_args()
    if args.cmd == "snapshot":
        zp = Path(args.zip) if args.zip else (
            VAULT / ".workbuddy" / "backups" /
            f"qt_before_{time.strftime('%Y%m%d_%H%M%S')}.zip")
        zp.parent.mkdir(parents=True, exist_ok=True)
        return cmd_snapshot(Path(args.pending), zp)

    return cmd_verify(Path(args.zip))


if __name__ == "__main__":
    sys.exit(main())
