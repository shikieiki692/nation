"""对习题书 docx 做结构校验，并检查代表章渲染 PNG 是否非空。

用法:
    python -X utf8 11-模板/scripts/validate_docx_structure.py
"""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from PIL import Image

VAULT_ROOT = Path(__file__).resolve().parents[2]
DOCX_ROOTS = [
    VAULT_ROOT / "00-首页/题组Word/习题书/教师版",
    VAULT_ROOT / "00-首页/题组Word/习题书/学生版",
]
MD_ROOTS = {
    "教师版": VAULT_ROOT / "04-课件/习题集/习题书-教师版",
    "学生版": VAULT_ROOT / "04-课件/习题集/习题书-学生版",
}
RENDER_DIRS = [
    "1-热力学",
    "3-晶体结构",
    "4-配位化学",
    "2-立体化学",
    "1-结构基础与波谱分析",
    "6-化学分析",
]
RENDER_ROOT = VAULT_ROOT / ".tmp-word-render"
REPORT = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-Word结构与渲染检查.md"
JSONL = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-Word结构与渲染检查.jsonl"


def docx_stats(path: Path) -> dict:
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        media = [n for n in names if n.startswith("word/media/")]
        xml = zf.read("word/document.xml").decode("utf-8", errors="replace")
    return {
        "media": len(media),
        "tables": len(re.findall(r"<w:tbl\b", xml)),
        "drawings": len(re.findall(r"<w:drawing\b", xml)),
        "blips": len(re.findall(r"<a:blip\b", xml)),
        "text_runs": len(re.findall(r"<w:t\b", xml)),
    }


def md_image_count(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    embeds = re.findall(r"!\[\[([^\]|]+)", text)
    return len(set(embeds)), len(embeds)


def png_nonblank(path: Path) -> float:
    with Image.open(path) as im:
        im = im.convert("L").resize((200, 260))
        px = im.tobytes()
    dark = sum(1 for v in px if v < 245)
    return dark / len(px)


def main() -> int:
    rows: list[dict] = []
    for root in DOCX_ROOTS:
        edition = root.name
        for docx in sorted(root.glob("*.docx")):
            stats = docx_stats(docx)
            md = MD_ROOTS[edition] / docx.stem.replace("-", "-", 1)
            md_candidates = list(MD_ROOTS[edition].rglob(f"{docx.stem}.md"))
            md_unique, md_total = (
                md_image_count(md_candidates[0]) if md_candidates else (-1, -1)
            )
            rows.append(
                {
                    "edition": edition,
                    "chapter": docx.stem,
                    "media": stats["media"],
                    "tables": stats["tables"],
                    "drawings": stats["drawings"],
                    "blips": stats["blips"],
                    "text_runs": stats["text_runs"],
                    "md_images_unique": md_unique,
                    "md_images_total": md_total,
                    "media_match": md_unique < 0 or stats["media"] == md_unique,
                }
            )

    render_rows: list[dict] = []
    for name in RENDER_DIRS:
        d = RENDER_ROOT / name
        pages = sorted(d.glob("page-*.png")) if d.exists() else []
        ratios = [png_nonblank(p) for p in pages]
        blank = [i + 1 for i, r in enumerate(ratios) if r < 0.0005]
        render_rows.append(
            {
                "chapter": name,
                "pages": len(pages),
                "blank_pages": blank[:20],
                "blank_count": len(blank),
                "min_ink": round(min(ratios), 5) if ratios else None,
                "max_ink": round(max(ratios), 5) if ratios else None,
            }
        )

    with JSONL.open("w", encoding="utf-8") as f:
        for r in rows + render_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    L = [
        "---",
        "title: 2026-08-30-习题书V2-Word结构与渲染检查",
        "type: 审计报告",
        "task_type: 习题册Word验收",
        "status: 已生成",
        "created: 2026-08-30",
        "updated: 2026-08-30",
        "---",
        "",
        "# 习题书 V2 Word 结构与渲染检查",
        "",
        "## 一、docx 结构",
        "",
        "| 版本 | 章节 | 图片(media) | 表格 | 图片(drawing) | 文本run | 源图数 | 一致 |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        L.append(
            "| {edition} | {chapter} | {media} | {tables} | {drawings} | {text_runs} | "
            "{md_unique}（出现 {md_total} 次） | {ok} |".format(
                edition=r["edition"],
                chapter=r["chapter"],
                media=r["media"],
                tables=r["tables"],
                drawings=r["drawings"],
                text_runs=r["text_runs"],
                md_unique=r["md_images_unique"],
                md_total=r["md_images_total"],
                ok="是" if r["media_match"] else "否",
            )
        )
    L.append("")
    L.append("## 二、代表章渲染（PNG 非空检查）")
    L.append("")
    L.append("| 章节 | 页数 | 空白页 | 最低墨量 | 最高墨量 |")
    L.append("|---|---:|---:|---:|---:|")
    for r in render_rows:
        L.append(
            "| {chapter} | {pages} | {blank_count} | {min_ink} | {max_ink} |".format(
                chapter=r["chapter"],
                pages=r["pages"],
                blank_count=r["blank_count"],
                min_ink=r["min_ink"],
                max_ink=r["max_ink"],
            )
        )
    L.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")

    bad = [r for r in rows if not r["media_match"]]
    blank_total = sum(r["blank_count"] for r in render_rows)
    print(
        f"docx={len(rows)} media_mismatch={len(bad)} "
        f"rendered_pages={sum(r['pages'] for r in render_rows)} blank_pages={blank_total}"
    )
    return 1 if bad or blank_total else 0


if __name__ == "__main__":
    raise SystemExit(main())
