#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""render_health.py —— 公式健康度汇总（跨域，一条命令）。

为什么需要它
------------
`render_gate.py` 是**单域 / 单文件**粒度。此前想知道"全库现在什么水平"，
只能手敲一连串 `--domain`（中文路径 + shell 引号，本库已因此踩过多次坑）。
本脚本把**域清单固化在代码里**，逐域调用 render_gate 并汇总它的输出 ——
**不复制任何判据**（判据只有 render_gate 一处，避免第二套口径）。

口径（与"单域扫描"的三处差异，读数字前必看）
--------------------------------------------
1. **排除 `_归档/`**：那是死文件（`build-all-handout-docx.py` 默认构建也排除），
   计入会污染趋势 —— 你永远不会去修它们。归档内的问题请用 `audit_deprecated.py` 管。
2. **只统计 `should_check` 范围内的域**：文档类域（`09-审计报告/`、`02-数据库/`、
   `12-教学洞察/`、`08-可视化资源/`、`10-索引与统计/`、`01-考纲导航/`、`11-模板/`、
   `00-首页/`）默认不检查 —— 那里的 `$` 常被用作价格 / 散文描述 / DataviewJS 语法。
3. **`受检` 是排除后的实际份数**，不等于目录里的 .md 总数。

成本：约 1.4s/份（每份跑 1 次 pandoc）。全量约 40 分钟，建议后台跑。

用法
----
    python -X utf8 11-模板/scripts/render_health.py                      # 全量汇总
    python -X utf8 11-模板/scripts/render_health.py --only 03-知识点 07-资料提炼
    python -X utf8 11-模板/scripts/render_health.py --save               # 存档到 09-审计报告/
    python -X utf8 11-模板/scripts/render_health.py --raw-dir <目录>     # 保留每域原始输出
    python -X utf8 11-模板/scripts/render_health.py --list               # 只列域清单
"""
import argparse
import datetime
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[1]
GATE = HERE / "render_gate.py"
PY = sys.executable

# ── 域清单（有序：**交付相关在前**，读表的人先看到最要紧的）────────────────
# (域路径, 说明)
DOMAINS = [
    ("06-学生侧材料", "学生侧交付物（练习卷 / 讲义 / 习题册）"),
    ("04-课件/习题集", "成书层 + 随堂层 + 竞赛导向层"),
    ("04-课件/学生讲义", "学生讲义（md 源，出 docx）"),
    ("13-教案", "课时教案"),
    ("04-课件/新授课", "新授课课件"),
    ("04-课件/备课大纲", "备课大纲"),
    ("04-课件/专题课", "专题课合集"),
    ("04-课件/复习课", "复习课"),
    ("04-课件/工具卡", "工具卡"),
    ("04-专题与题型", "专题 / 题型页"),
    ("03-知识点", "KP 页（✱ 出 Word 的域之外，既有预检照不到）"),
    ("07-资料提炼", "资料提炼页（同上）"),
    ("05-真题库", "真题库"),
    ("高考化学", "高考线资料"),
    ("02-考纲条目", "考纲条目"),
    ("06-外部资料导入", "源层：外部导入原始材料"),
    ("mineru", "源层：MinerU 原始输出"),
    ("mineru02", "源层：MinerU 原始输出（第二批）"),
]

# `_归档/` 在**路径任意一级**出现都算归档（库里有 `04-课件/学生讲义/_归档/` 这种层级）
ARCHIVE_SEGS = ("_归档", "归档")

SUMMARY_RE = re.compile(
    r"RENDER_GATE=(PASS|FAIL) \[(\w+)\]\s+受检 (\d+) / 失败 (\d+)")


def list_md(domain: str):
    """该域下**现役** .md（排除 `_归档/` 与 `.workbuddy/`）。"""
    root = VAULT / domain
    if not root.is_dir():
        return None
    out = []
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(VAULT).as_posix()
        parts = rel.split("/")
        if any(seg in ARCHIVE_SEGS for seg in parts[:-1]):
            continue
        out.append(rel)
    return out


def run_domain(domain: str, rawdir):
    """跑一域，返回 (受检, 失败, 耗时秒, 摘要行, 原始输出路径或 None)。"""
    files = list_md(domain)
    if files is None:
        return None
    if not files:
        return dict(files=0, checked=0, failed=0, secs=0.0, line="（目录下无现役 .md）", raw=None)

    # 走 --manifest（而非 --domain）是为了**自己控制文件集合**（排除归档）。
    # 用固定名会与并发进程打架，故按 pid 命名。
    mf = Path(".workbuddy/tmp/_health_%d_%s.txt" % (
        __import__("os").getpid(), re.sub(r"[^\w]+", "_", domain)))
    (VAULT / mf).parent.mkdir(parents=True, exist_ok=True)
    (VAULT / mf).write_text("\n".join(files) + "\n", encoding="utf-8", newline="\n")

    t0 = time.monotonic()
    r = subprocess.run([PY, "-X", "utf8", str(GATE), "--manifest", str(mf)],
                       capture_output=True, cwd=VAULT)
    secs = time.monotonic() - t0
    out = (r.stdout or b"").decode("utf-8", "replace") + \
          (r.stderr or b"").decode("utf-8", "replace")
    try:
        (VAULT / mf).unlink()
    except OSError:
        pass

    m = SUMMARY_RE.search(out)
    if m:
        verdict, mode, checked, failed = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
        line = "RENDER_GATE=%s [%s] 受检 %d / 失败 %d" % (verdict, mode, checked, failed)
    else:
        checked = failed = 0
        line = out.strip().splitlines()[-1] if out.strip() else "（无输出）"

    raw = None
    if rawdir:
        Path(rawdir).mkdir(parents=True, exist_ok=True)
        raw = Path(rawdir) / (re.sub(r"[^\w]+", "_", domain) + ".txt")
        raw.write_text(out, encoding="utf-8", newline="\n")

    return dict(files=len(files), checked=checked, failed=failed,
                secs=secs, line=line, raw=str(raw) if raw else None)


def main() -> int:
    ap = argparse.ArgumentParser(description="公式健康度汇总（跨域）")
    ap.add_argument("--only", nargs="*", default=None, metavar="域",
                    help="只跑这些域（默认全部）")
    ap.add_argument("--skip", nargs="*", default=[], metavar="域")
    ap.add_argument("--save", action="store_true",
                    help="把汇总表存档到 09-审计报告/<日期>-公式健康度快照.md")
    ap.add_argument("--raw-dir", default=None, metavar="目录",
                    help="逐域保留 render_gate 的原始输出（出工单/定位时用）")
    ap.add_argument("--list", action="store_true", help="只列出域清单与其文件数")
    args = ap.parse_args()

    todo = [(d, note) for d, note in DOMAINS
            if (not args.only or d in args.only) and d not in args.skip]

    if args.list:
        for d, note in todo:
            fs = list_md(d)
            print("  %-20s %5s  %s" % (d, len(fs) if fs is not None else "—", note))
        return 0

    rows = []
    t_all = time.monotonic()
    for i, (d, note) in enumerate(todo, 1):
        res = run_domain(d, args.raw_dir)
        if res is None:
            print("[%d/%d] %-20s （目录不存在，跳过）" % (i, len(todo), d), flush=True)
            continue
        print("[%d/%d] %-20s 受检 %4d / 失败 %3d  (%.0fs)"
              % (i, len(todo), d, res["checked"], res["failed"], res["secs"]), flush=True)
        rows.append((d, note, res))

    tot_ck = sum(r[2]["checked"] for r in rows)
    tot_f = sum(r[2]["failed"] for r in rows)

    out = []
    out.append("| 域 | 受检 | 失败 | 占比 | 说明 |")
    out.append("|:--|--:|--:|--:|:--|")
    for d, note, r in rows:
        pct = ("%.1f%%" % (100.0 * r["failed"] / r["checked"])) if r["checked"] else "—"
        out.append("| `%s/` | %d | %s | %s | %s |"
                   % (d, r["checked"],
                      ("**%d**" % r["failed"]) if r["failed"] else "0 ✅",
                      pct, note))
    out.append("| **合计** | **%d** | **%d** | **%.1f%%** | |"
               % (tot_ck, tot_f, (100.0 * tot_f / tot_ck) if tot_ck else 0.0))
    table = "\n".join(out)

    print("\n" + table)
    print("\n总耗时 %.0fs（受检 %d / 失败 %d）" % (time.monotonic() - t_all, tot_ck, tot_f))
    print("口径：排除 `_归档/`；文档类域不检查（见 `render_gate.should_check`）。")

    if args.save:
        stamp = datetime.date.today().isoformat()
        p = VAULT / "09-审计报告" / ("%s-公式健康度快照.md" % stamp)
        head = [
            "---",
            "title: 公式健康度快照 %s" % stamp,
            "type: 审计",
            "created: %s" % stamp,
            "updated: %s" % stamp,
            "tags: [公式渲染, 健康度, 快照]",
            "---",
            "",
            "# 公式健康度快照 · %s" % stamp,
            "",
            "> **怎么复跑**：`python -X utf8 11-模板/scripts/render_health.py`",
            "> （工具：`11-模板/scripts/render_health.py`；判据源：`render_gate.py`）",
            ">",
            "> **口径**：排除 `_归档/`（死文件，默认构建也不含）；文档类域不检查。",
            "> **判据**：产物字面 `$` == 0 且无 texmath 转换失败 —— 即「公式到底渲没渲染出来」。",
            "",
            "## 域级汇总",
            "",
            table,
            "",
            "## 怎么看这张表",
            "",
            "- **失败 ≠ 待办**：多数是 **OCR 导入阶段**带进来的公式语法错（需按原书校正），",
            "  不是创作问题。分类与逐条清单见 `2026-09-20-公式渲染缺陷清单-知识点与资料提炼.md`。",
            "- **源层失败率高是预期**：`06-外部资料导入/`、`mineru*` 是原始 OCR 存档，",
            "  修存档不如重新导入 —— 这部分建议**不修**，只作为「导入质量」的观测值。",
            "- **趋势比绝对值重要**：复跑同一条命令，比较失败数是否上升。",
            "",
        ]
        p.write_text("\n".join(head), encoding="utf-8", newline="")
        print("\n已存档：%s" % p.relative_to(VAULT))

    return 1 if tot_f else 0


if __name__ == "__main__":
    raise SystemExit(main())
