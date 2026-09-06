"""按归属清单删除 27 届初赛“同页 7 图”簇的误挂图片行。

只删除独立成行的 `![[哈希.jpg]]`；媒体文件保留。每文件保留清单见
`09-审计报告/2026-08-30-习题书V2-重复图归属建议-27届初赛簇.md`。

用法:
    python -X utf8 11-模板/scripts/remove_misattached_images.py
"""

from __future__ import annotations

from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "04-题库/真题/第27届初赛"

HASH = {
    "A": "0a1498d59a7843bd0ce5525c07283d7dfb9bf468e44673deaaa3369b41e6b891",
    "B": "94ba0ccf835497bcafefbedb1b7edfea4eb7bada4240519a544afab21ffbe04c",
    "C": "724f92736ebd1304052ca58bcdf78fc6c9cd46b44ba86978ed8b297f1d07a5f2",
    "D": "87c23673ef9590263d5a2e6cc8d6bdb9cc39afda631bae3cde804b5224f40d21",
    "E": "fd4e14d9deb96227f15759c88d573c59ae3b5c407076d839b612698e459acab6",
    "F": "d50206ff9c5b8a939b460825692de308e9ee7e76e66b17d5f837d8f73292ae83",
    "G": "81a8d5b638511406e9e810a993f3a2d775264832df8b007f3a79e19fd694bf2a",
}

REMOVE = {
    "无机和结构化学/题-027-2-1-Bi2Cl8结构与杂化.md": "CDEFG",
    "无机和结构化学/题-027-2-2-液氨中Mg置换Na.md": "ABCDEFG",
    "无机和结构化学/题-027-2-3-Pb液氨电解.md": "ABCDEFG",
    "无机和结构化学/题-027-2-4-1-金属氧化物配位数.md": "ABCDE",
    "无机和结构化学/题-027-2-4-2-晶胞原子数.md": "ABCDE",
    "无机和结构化学/题-027-2-4-3-金属氧化物化学式.md": "ABCDE",
    "无机和结构化学/题-027-2-5-多核钴配合物手性结构.md": "ABCFG",
    "无机和结构化学/题-027-2-6-铬酰氯推断与结构.md": "ABDEFG",
    "无机和结构化学/题-027-2-7-钯配合物组成计算.md": "ABCDEFG",
    "化学原理/题-027-2-8-甲烷燃烧体积比.md": "ABCDEFG",
}


def main() -> int:
    removed = 0
    for rel, keys in REMOVE.items():
        path = SRC / rel
        if not path.exists():
            print(f"missing: {rel}")
            continue
        targets = {f"![[{HASH[k]}.jpg]]" for k in keys}
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        keep = [ln for ln in lines if ln.strip() not in targets]
        n = len(lines) - len(keep)
        if n:
            path.write_text("".join(keep), encoding="utf-8", newline="")
            removed += n
            print(f"  {rel}: removed {n}")
    print(f"total_removed={removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
