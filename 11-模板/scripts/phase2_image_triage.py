"""Phase 2 图片分批待办：从图片归属清单生成可执行工作清单。

用法:
    python 11-模板/scripts/phase2_image_triage.py

输出 Markdown 分批待办报告，供人工按“跨题重复图 → HTML <img> → 缺失媒体 →
待人工文件”顺序核验。加 `--copy-missing` 时会把批 C 的缺失图片复制进媒体仓库
（保留哈希原名），不修改源题库、不修改成书。
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import shutil
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]


def image_dims(path: Path) -> str:
    try:
        data = path.read_bytes()
    except OSError:
        return ""
    if data[:3] == b"\xff\xd8\xff":
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h = int.from_bytes(data[i + 5 : i + 7], "big")
                w = int.from_bytes(data[i + 7 : i + 9], "big")
                return f"{w}x{h}"
            i += 2 + int.from_bytes(data[i + 2 : i + 4], "big")
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w = int.from_bytes(data[16:20], "big")
        h = int.from_bytes(data[20:24], "big")
        return f"{w}x{h}"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        w = int.from_bytes(data[6:8], "little")
        h = int.from_bytes(data[8:10], "little")
        return f"{w}x{h}"
    return ""


def locate_missing(records: list[dict], vault_root: Path) -> dict[str, Path]:
    """在 vault 里按文件名定位媒体仓库缺失的图片。"""
    missing = sorted({r["base"] for r in records if not r["media_present"] and r["base"]})
    if not missing:
        return {}
    targets = set(missing)
    found: dict[str, Path] = {}
    for dirpath, dirnames, filenames in os.walk(vault_root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            if name in targets:
                found.setdefault(name, Path(dirpath) / name)
                targets.discard(name)
        if not targets:
            break
    return found


def fmt_md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--image-context",
        default=str(VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-图片归属清单.jsonl"),
    )
    ap.add_argument("--media-root", default=str(VAULT_ROOT / "媒体仓库"))
    ap.add_argument("--vault-root", default=str(VAULT_ROOT))
    ap.add_argument(
        "--output",
        default=str(VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-Phase2待办清单.md"),
    )
    ap.add_argument(
        "--copy-missing",
        action="store_true",
        help="把媒体仓库缺失的图片从 vault 原位置复制进媒体仓库（保留哈希原名）",
    )
    args = ap.parse_args()

    image_context = Path(args.image_context).resolve()
    media_root = Path(args.media_root).resolve()
    vault_root = Path(args.vault_root).resolve()
    output = Path(args.output).resolve()

    records = [
        json.loads(line)
        for line in image_context.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    pending = [r for r in records if r["disposition"] == "待人工"]
    html_imgs = [r for r in records if r["kind"] == "html_img"]
    missing = [r for r in records if not r["media_present"] and r["base"]]
    missing_by_hash = collections.defaultdict(list)
    for r in missing:
        missing_by_hash[r["base"]].append(r)
    located = locate_missing(records, vault_root)

    if args.copy_missing:
        copied = 0
        for base in sorted(missing_by_hash):
            src = located.get(base)
            if not src:
                print(f"SKIP not located: {base}")
                continue
            shutil.copy2(src, media_root / base)
            copied += 1
        print(f"copied_missing_media={copied}")

    by_base = collections.defaultdict(list)
    for r in records:
        if r["base"]:
            by_base[r["base"]].append(r)
    repeated = []
    for base, recs in by_base.items():
        files = sorted({r["source_path"] for r in recs})
        if len(files) > 1:
            repeated.append((base, recs, files))
    repeated.sort(key=lambda x: (-len(x[2]), x[0]))

    pending_by_file = collections.defaultdict(list)
    for r in pending:
        pending_by_file[r["source_path"]].append(r)
    pending_files = sorted(
        pending_by_file.items(), key=lambda kv: (-len(kv[1]), kv[0])
    )

    L: list[str] = []
    L.append("# 习题书 V2 Phase 2 图片分批待办")
    L.append("")
    L.append(f"> 生成命令：`python 11-模板/scripts/phase2_image_triage.py`")
    L.append(f"> 输入：`{image_context.name}`，共 {len(records)} 条图片记录")
    L.append("")

    L.append("## 一、总览")
    L.append("")
    L.append(
        fmt_md_table(
            ["指标", "数值"],
            [
                ["图片记录", len(records)],
                ["待人工", len(pending)],
                ["跨题重复唯一图", len(repeated)],
                [
                    "跨题重复图片记录",
                    sum(len(x[1]) for x in repeated),
                ],
                ["HTML <img> 残留", len(html_imgs)],
                ["媒体仓库缺失", len(missing)],
                ["已定位缺失文件", sum(1 for r in missing if r["base"] in located)],
                ["表格单元格内图", sum(1 for r in records if r["in_td"])],
                ["同行多图", sum(1 for r in records if r["multi_image_line"])],
                ["贴分隔线（---![[）", sum(1 for r in records if r["glued_to_separator"])],
            ],
        )
    )
    L.append("")

    L.append("## 二、批 A：跨题重复图（优先目检装饰/页眉）")
    L.append("")
    L.append(
        "> 同一哈希出现在多个源题文件时，通常是 OCR 页眉/装饰图或同卷插图。"
        "只能作为核验线索，不能仅凭重复次数删除；目检确认后再移出成书。"
    )
    L.append("")
    L.append(
        fmt_md_table(
            ["哈希文件名（前 24 字符）", "文件数", "图片记录", "尺寸", "主要区块", "首个位置"],
            [
                [
                    base[:24],
                    str(len(files)),
                    str(len(recs)),
                    image_dims(
                        located.get(base, media_root / base)
                        if not recs[0]["media_present"]
                        else media_root / base
                    ),
                    ", ".join(
                        f"{b}×{c}"
                        for b, c in collections.Counter(
                            r["bucket"] for r in recs
                        ).most_common()
                    ),
                    f"{recs[0]['source_path']}:{recs[0]['line']}",
                ]
                for base, recs, files in repeated
            ],
        )
    )
    L.append("")

    L.append("## 三、批 B：HTML <img> 残留")
    L.append("")
    L.append(
        "> 处理方式：先定位物理文件，复制/确认到 `媒体仓库/`，再改为 `![[哈希.jpg]]`，"
        "并拆出表格单元格或独立成段。"
    )
    L.append("")
    L.append(
        fmt_md_table(
            ["源文件", "行号", "哈希", "媒体仓库", "区块", "表格内"],
            [
                [
                    r["source_path"],
                    str(r["line"]),
                    r["base"][:24],
                    "有" if r["media_present"] else "缺",
                    r["bucket"],
                    "是" if r["in_td"] else "",
                ]
                for r in sorted(html_imgs, key=lambda r: (r["source_path"], r["line"]))
            ],
        )
    )
    L.append("")

    L.append("## 四、批 C：媒体仓库缺失文件")
    L.append("")
    L.append(
        "> 2026-08-30 已把 23 个缺失哈希从原 OCR 目录复制进 `媒体仓库/`，"
        "当前缺失为 0。若以后再次出现缺失，按下方表定位后复制即可，不要改哈希名。"
    )
    L.append("")
    L.append(
        fmt_md_table(
            ["哈希", "源文件", "行号", "已定位路径"],
            [
                [
                    r["base"],
                    r["source_path"],
                    str(r["line"]),
                    str(located.get(r["base"], "未找到")),
                ]
                for r in sorted(
                    missing,
                    key=lambda r: (r["base"], r["source_path"], r["line"]),
                )
            ],
        )
    )
    L.append("")

    L.append("## 五、批 D：待人工图片按源文件排序")
    L.append("")
    L.append(
        "> 教学块（解题思路/易错分析/相关图片/题干图示/扩展块）中的图片逐个确认："
        "原题图移入题干，解析图移入答案，纯教学图移出成书。"
    )
    L.append("")
    L.append(
        fmt_md_table(
            ["源文件", "待人工", "该文件图片总数", "区块分布"],
            [
                [
                    path,
                    str(len(recs)),
                    str(
                        sum(
                            1
                            for r in records
                            if r["source_path"] == path
                        )
                    ),
                    ", ".join(
                        f"{b}×{c}"
                        for b, c in collections.Counter(
                            r["bucket"] for r in recs
                        ).most_common()
                    ),
                ]
                for path, recs in pending_files
            ],
        )
    )
    L.append("")

    L.append("## 六、建议执行顺序")
    L.append("")
    L.append("1. 批 A：先目检跨题重复图（从重复 10 次向下看），标记装饰/页眉图。")
    L.append("2. 批 C：当前缺失已归零；后续新增引用如再缺失，复制哈希原名进 `媒体仓库/`。")
    L.append("3. 批 B：27 个 `<img>` 全部归一化为 `![[哈希.jpg]]` 并独立成段。")
    L.append("4. 按批 D（本报告第五节）逐文件核对 547 条待人工图片的最终归属。")
    L.append("5. 每完成一批就重跑 `audit_exercise_book.py`，确认 2,016 张成书图不丢。")
    L.append("")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    print(f"pending={len(pending)} repeated={len(repeated)} html_img={len(html_imgs)} missing={len(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
