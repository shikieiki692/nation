# -*- coding: utf-8 -*-
"""生成 04-课件/学生讲义/README.md（模块视图 + 轮次视图双索引）。

用法:
    python -X utf8 11-模板/scripts/generate_handout_readme.py [--apply]
默认 dry-run（打印到 stdout）。
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SRC = VAULT / "04-课件" / "学生讲义"
DOC = VAULT / "06-学生侧材料" / "讲义"

# 2026-09-18：目录结构对齐《未央化学竞赛课程计划》§二「各模块内容规划」的 6 大模块。
# `_数学工具/` 为工具层（考纲无对应条目），`_综合/` 为跨模块。
MODULES = ["1-化学基础知识", "2-结构化学", "3-物理化学", "4-分析化学", "5-无机化学", "6-有机化学", "_数学工具"]


def fm_get(text: str, key: str) -> str:
    if not text.startswith("---"):
        return ""
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^" + key + r"\s*:\s*(.*)$", line)
        if m:
            return m.group(1).strip()
    return ""


def docx_ok(stem: str) -> bool:
    # 2026-09-10：产物目录已按模块分子目录（如 06-学生侧材料/讲义/结构化学/晶体学/），
    # 只查 DOC 根会漏判全部 docx，改为递归查找。
    return any(p.name == stem + ".docx" for p in DOC.rglob("*.docx"))


def collect():
    items = []
    for p in sorted(SRC.rglob("*.md")):
        rel = p.relative_to(SRC)
        if "_归档" in rel.parts or p.name.startswith("README"):
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        group = rel.parts[0] if len(rel.parts) > 1 else "(根)"
        rounds = fm_get(t, "serve_rounds") or "(未标)"
        rounds = rounds.strip("[]")
        items.append({
            "group": group,
            "stem": p.stem,
            "title": fm_get(t, "title") or p.stem,
            "rounds": rounds,
            "stage": fm_get(t, "stage") or "(未标)",
            "lines": len(t.splitlines()),
            "docx": docx_ok(p.stem),
            "path": str(rel).replace("\\", "/"),
        })
    return items


def build(items) -> str:
    by_group = defaultdict(list)
    for it in items:
        by_group[it["group"]].append(it)

    out = [
        "---",
        "title: 学生讲义总索引",
        "type: 索引",
        "tags: [学生讲义, 索引]",
        "updated: 2026-09-18",
        "---",
        "",
        "# 学生讲义总索引",
        "",
        "> 本文件由 `11-模板/scripts/generate_handout_readme.py` 生成，改动手写内容会被覆盖；",
        "> 要改请改脚本或改讲义自身的 frontmatter。",
        "",
        "## 一、组织逻辑",
        "",
        "`04-课件/学生讲义/` 下的顶层目录**与《未央化学竞赛课程计划（初二至高二）》§二「各模块内容规划」的 6 大模块一一对应**；",
        "`_数学工具/` 为**工具层**（非化学学科模块，考纲无对应条目），`_综合/` 收跨模块内容：",
        "",
        "| 目录 | 收什么 |",
        "|:--|:--|",
        "| `1-化学基础知识/` | 氧化还原、溶液、常见酸碱盐、离子反应、物质的量、化学计算规范 |",
        "| `2-结构化学/` | 原子结构、周期律、分子结构、晶体、配位化合物、结构桥章、超分子、结构专题与复习 |",
        "| `3-物理化学/` | 气体和溶液、热力学、动力学与平衡、相平衡与胶体、表面界面、量子化学初步、电化学 |",
        "| `4-分析化学/` | 数据处理与误差、容量分析、重量分析、分光光度法 |",
        "| `5-无机化学/` | 各族元素（卤素/氧族/氮族/碳族/硼族/碱金属/过渡金属）、元素推断与情境化训练 |",
        "| `6-有机化学/` | 基础与波谱、立体化学、各族化合物、各类反应机理、金属有机与催化、分离纯化 |",
        "| `_数学工具/` | 支撑层：函数与线性化、对数与指数、微分与积分直觉、偏导与全微分、量纲估算、组合与概率 |",
        "| `_综合/` | 跨模块：真题模拟拆解、真题小问总集 |",
        "| `_归档/` | 历史旧版（不维护、不导出） |",
        "",
        "判据是**内容主题**（对齐课程计划的「章」），不是文件名形态。同一主题的不同版本（如「超级充实版」「第一轮基础版」「教师增强版」）",
        "归在同一模块目录内，靠文件名后缀区分形态。",
        "",
        "**为什么按模块而不是按轮次分**：一份讲义常服务多轮（如 `[第一轮, 第二轮, 第三轮, 第四轮]`），",
        "按轮次分会导致同一文件无处安放；轮次走 frontmatter 的 `serve_rounds`，用下面的轮次视图检索；",
        "多轮共用的讲义按**主讲轮次**归入对应模块。",
        "",
        "## 二、模块视图",
        "",
    ]

    for g in MODULES + ["_综合"]:
        lst = sorted(by_group.get(g, []), key=lambda x: x["stem"])
        if not lst:
            continue
        out.append("### %s（%d 份）" % (g, len(lst)))
        out.append("")
        out.append("| 讲义 | 服务轮次 | 状态 | 篇幅 | docx |")
        out.append("|:--|:--|:--|--:|:--:|")
        for it in lst:
            out.append("| [[%s]] | %s | %s | %d 行 | %s |" % (
                it["stem"], it["rounds"], it["stage"], it["lines"],
                "✅" if it["docx"] else "—"))
        out.append("")

    # 轮次视图
    by_round = defaultdict(list)
    for it in items:
        for r in [x.strip() for x in it["rounds"].split(",") if x.strip()]:
            by_round[r].append(it)
    out += ["## 三、轮次视图", ""]
    order = ["第一轮", "第二轮", "第三轮", "第四轮", "决赛", "(未标)"]
    for r in order:
        lst = sorted(by_round.get(r, []), key=lambda x: (x["group"], x["stem"]))
        if not lst:
            continue
        out.append("### %s（%d 份）" % (r, len(lst)))
        out.append("")
        for it in lst:
            out.append("- `%s` %s — [[%s]]" % (it["group"], "✅" if it["docx"] else "—", it["stem"]))
        out.append("")

    out += [
        "## 四、命名与元数据约定",
        "",
        "| 项 | 约定 |",
        "|:--|:--|",
        "| 文件名 | `<主题>[-<形态>].md`，无日期前缀；形态后缀如 `-超级充实版（自学完整）`、`-第一轮基础版（普化原理）`、`-新课`、`-教师增强版` |",
        "| 简写 vs 全称 | 文件名用简写（如 `烷烃烯烃炔烃`），全称放 `title`，并在 `aliases` 里登记（如 `烷烃·烯烃·炔烃`），两种写法都能解析 |",
        "| `module` | 四模块之一，与所在目录一致 |",
        "| `serve_rounds` | 内联数组，如 `[第一轮, 第二轮]` |",
        "| `stage` | `draft`（无 docx 产物）→ `published`（已导出成品） |",
        "| 图片 | `![[<64位哈希>.jpg]]`，不写 alt，禁 `media/` 等子目录前缀 |",
        "| 公式 | 简单用 Unicode（H₂O），复杂用整段 math（$$…$$），**严禁半截 math**（如 `H$_2$O`） |",
        "",
        "## 五、常用命令",
        "",
        "```bash",
        "PY=\"C:/Users/蕾赛/AppData/Local/Programs/Python/Python312/python.exe -X utf8\"",
        "# 看哪些讲义的 docx 落后于 md",
        "$PY 11-模板/scripts/handout_stale_docx_report.py",
        "# 重导出（默认批量集；注意必须清这两个环境变量）",
        "CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID= $PY 11-模板/scripts/build-all-handout-docx.py --parallel 4 --strict-images",
        "# 单独导出一份（不要用 --file，它是子串匹配会误命中）",
        "CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID= $PY 11-模板/scripts/build-all-handout-docx.py --path \"<绝对路径>.md\"",
        "# 体检：注释配平 / 半截math / 裸LaTeX / 图片元数据",
        "$PY 11-模板/scripts/check_comment_balance.py",
        "$PY 11-模板/scripts/handout_fix_half_math.py",
        "$PY 11-模板/scripts/handout_latex_outside_math.py --all",
        "$PY 11-模板/scripts/handout_sync_image_meta.py",
        "```",
        "",
        "> 产物统一落在 `06-学生侧材料/讲义/`（按同名 6 模块分子目录），历史产物分层归档在 `_archive/`。详见那里的 README。",
        "",
    ]
    return "\n".join(out) + "\n"


def main() -> None:
    items = collect()
    text = build(items)
    if "--apply" in sys.argv:
        (SRC / "README.md").write_text(text, encoding="utf-8", newline="")
        print("已写入 %s（%d 份讲义）" % (SRC / "README.md", len(items)))
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
