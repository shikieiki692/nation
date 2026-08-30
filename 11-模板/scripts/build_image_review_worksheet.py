"""把 547 条待人工图片核验导出为 CSV 工作表，并生成视觉抽看清单。

用法:
    python -X utf8 11-模板/scripts/build_image_review_worksheet.py
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2严格版-图片归属清单.jsonl"
CSV_OUT = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-图片人工核验工作表.csv"
CHECKLIST = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-人工视觉抽看清单.md"


def main() -> int:
    rows = [
        json.loads(line)
        for line in SRC.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    pending = [r for r in rows if r.get("disposition") == "待人工"]

    header = [
        "源文件",
        "行号",
        "图片哈希",
        "语义块",
        "块标题",
        "答案区",
        "跨题重复",
        "出现文件数",
        "上下文摘要",
        "核验结论",
        "备注",
    ]
    with CSV_OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in pending:
            writer.writerow(
                [
                    r.get("source_path", ""),
                    r.get("line", ""),
                    r.get("base", ""),
                    r.get("bucket", ""),
                    r.get("block_heading", ""),
                    "是" if r.get("in_answer") else "否",
                    "是" if r.get("cross_question_repeat") else "否",
                    r.get("repeat_files", ""),
                    (r.get("line_snippet", "") or "").replace("\n", " ")[:160],
                    "",
                    "",
                ]
            )

    buckets = Counter(r.get("bucket", "") for r in pending)
    repeat = sum(1 for r in pending if r.get("cross_question_repeat"))
    unique_repeat = len(
        {r.get("base") for r in pending if r.get("cross_question_repeat")}
    )
    L = [
        "---",
        "title: 2026-08-30-习题书V2-人工视觉抽看清单",
        "type: 交接清单",
        "task_type: 习题册人工验收",
        "status: 待人工",
        "created: 2026-08-30",
        "updated: 2026-08-30",
        "---",
        "",
        "# 习题书 V2 人工视觉抽看清单",
        "",
        "## 一、图片人工核验工作表",
        "",
        f"- 待人工记录：{len(pending)} 条；跨题重复 {repeat} 条（唯一图 {unique_repeat} 组）。",
        f"- 工作表：`09-审计报告/2026-08-30-习题书V2-图片人工核验工作表.csv`（UTF-8，可直接用 Excel 打开）。",
        "- 结论列填写：`保留-题干 / 保留-答案 / 删除-装饰 / 重找`，必要时在备注写清原因。",
        "",
        "### 区块分布",
        "",
        "| 语义块 | 条数 |",
        "|---|---:|",
    ]
    for name, count in buckets.most_common():
        L.append(f"| {name} | {count} |")
    L.append("")
    L.append("## 二、Word 代表章视觉抽看")
    L.append("")
    L.append("渲染目录：`.tmp-word-render/`，每章建议抽看 5 类页面：")
    L.append("")
    L.append("1. 封面页：章节标题、题数、日期是否正常。")
    L.append("2. 首个题目页：题干、来源引用、公式是否正常。")
    L.append("3. 表格页：pipe table 是否完整、不串列。")
    L.append("4. 图片页：图片是否在位、方向正确、不遮挡文字。")
    L.append("5. 答案页：`查看答案`、解析、公式是否完整。")
    L.append("")
    L.append("| 章节 | 页数 | 建议重点 |")
    L.append("|---|---:|---|")
    L.append("| 1-热力学 | 45 | 封面、答案页、公式 |")
    L.append("| 3-晶体结构 | 228 | 表格页、图片页、超宽表 |")
    L.append("| 4-配位化学 | 125 | 图片页、表格页、公式 |")
    L.append("| 2-立体化学 | 92 | 图片页、立体结构图 |")
    L.append("| 1-结构基础与波谱分析 | 149 | 图片页、谱图、答案页 |")
    L.append("| 6-化学分析 | 57 | 表格页、答案页 |")
    L.append("")
    CHECKLIST.parent.mkdir(parents=True, exist_ok=True)
    CHECKLIST.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"pending={len(pending)} repeat={repeat} unique_repeat={unique_repeat}")
    print(f"csv={CSV_OUT.name} checklist={CHECKLIST.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
