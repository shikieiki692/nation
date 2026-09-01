#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_kb_phase3_math.py — 应用「美元符号未闭合」逐文件修复清单。

清单来源：09-审计报告/缓存-美元修复.json（三个子代理诊断 + 人工复核/覆盖后定稿）
安全机制：old 必须逐字存在于文件中才替换；写入前备份；结束后逐文件验证 $ 奇偶性。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")

V = Path(__file__).resolve().parents[2]
FIXES = json.load(open(V / "09-审计报告" / "缓存-美元修复.json", encoding="utf-8"))
BACKUP = V / "09-审计报告" / "备份" / "题库修复-2026-08-31"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    n_applied = 0
    fails = []
    odd_after = []
    for rel, edits in FIXES.items():
        f = V / rel
        if not f.exists():
            fails.append((rel, "文件不存在"))
            continue
        raw = f.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        changed = False
        for old, new, reason in edits:
            cnt = text.count(old)
            if cnt == 0:
                fails.append((rel, f"old 未匹配: {old[:50]}"))
                continue
            text = text.replace(old, new, cnt)
            changed = True
        if not changed:
            continue
        if args.dry:
            n_applied += 1
            print(f"  [dry] {rel}")
            continue
        dst = BACKUP / rel
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(raw)
        f.write_bytes(text.encode("utf-8"))
        n_applied += 1
        # 奇偶性
        e = text.find("\n---", 3)
        b = text[e + 4:] if e > 0 else text
        b2 = re.sub(r"\$\$.+?\$\$", "", b, flags=re.S)
        if b2.count("$") % 2:
            odd_after.append(rel)
        print(f"  ✓ {rel}")

    print(f"\n📊 {'预览' if args.dry else '已应用'} {n_applied} 文件")
    if fails:
        print("❌ 未匹配项：")
        for rel, msg in fails:
            print(f"   {msg}  ← {rel}")
    if odd_after:
        print("⚠ 修复后仍为奇数 $：")
        for r in odd_after:
            print("   ", r)


if __name__ == "__main__":
    main()
