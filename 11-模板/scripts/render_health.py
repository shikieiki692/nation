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
import os
import re
import subprocess
import sys
import time
from collections import Counter
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
        os.getpid(), re.sub(r"[^\w]+", "_", domain)))
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


# ── 工单生成：把「哪些文件坏了、坏在哪」变成可委派、可复跑的一张表 ───────────
# 全部事实都来自 render_gate 的原始输出，**本模块不另立判据**。
ROW_RE = re.compile(r"^(?P<name>.*?)\s+(?P<om>\d+|—)\s+(?P<tag>✅|❌|ALLOW)\s*$")
BS = chr(92)

# 域 → 处置建议（决定工单人先看谁）
def advice_for(domain: str) -> str:
    if domain in ("06-外部资料导入", "mineru", "mineru02"):
        return "⛔ 建议不修"
    if domain.startswith("06-学生侧材料"):
        return "🔴 P0 立即"
    if domain.startswith("03-知识点"):
        return "🟠 P1"
    return "🟡 P2"


def classify(blob: str):
    """按闸门给的原因原文分组。返回 (组名, 是否**机械可修**)。

    顺序 = 优先级，命中即止。⚠️ 分组依据是 render_gate 打印的**原因片段**
    （texmath 报错被截到 90 字符），故属**启发式**——工单里同时保留原因原文，
    人工可复核；分组只用于排优先级，不用于下结论。
    """
    if "行首 <div>" in blob:
        return "B栏｜行首 `<div>`（Obsidian 下吞块内 markdown）", False
    if "TAB 残名" in blob:
        return "B栏｜TAB 残名（真制表符吃掉命令首字母）", True
    if BS + "AA" in blob:
        return "B栏｜`" + BS + "AA` 未转义", True
    if BS + "text{" + BS + "text{" in blob:
        return "B栏｜`" + BS + "text{" + BS + "text{}}` 嵌套", True
    if "docx 转换失败" in blob:
        if any(k in blob for k in ("&lt;", "&gt;", "&amp;")):
            return "A栏｜HTML 实体混入数学域", True
        if "unexpected control sequence" in blob:
            return "A栏｜双反斜杠 `" + BS + BS + "`（仅 array 类环境内合法）", False
        if blob.count(BS + "text") >= 2:
            return "A栏｜`" + BS + "text{…" + BS + "cmd{…}}` 文本命令嵌套", True
        if "}}" in blob or "}]" in blob or ("{" in blob and "}" not in blob):
            return "A栏｜花括号不配平", False
        return "A栏｜其他 texmath 语法错（多为 OCR 乱码）", False
    if "产物字面 $" in blob:
        return "A栏｜`$` 不配平（公式整段未渲染）", False
    return "其他（需人工看原因原文）", False


def parse_raw(path: Path):
    """解析一个域的 render_gate 原始输出。

    ⚠️ 行里的文件名被 `%-58s` **截断**、不可反解，故失败项的**全路径取自文末
    「失败清单」并按出现顺序与 `❌` 行一一对应**；两者条数不等时**不猜**，
    返回 mismatch 让人知道解析失败（宁可报错也不产出错工单）。
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    checked = failed = 0
    m = SUMMARY_RE.search(text)
    if m:
        checked, failed = int(m.group(3)), int(m.group(4))

    full = []
    if "失败清单：" in lines:
        i = lines.index("失败清单：")
        # ⚠️ 只取**连续的 4 空格缩进块**。实测踩过：管线自己会往 stderr 打
        #    `  [WARN] 3 Excalidraw embed(s) removed …`，而本函数读的是
        #    stdout+stderr 合并流（必须合，pandoc 的 `Could not convert TeX math`
        #    走 stderr）⇒ 该行会落在这个位置、被当成第 3 条失败路径，
        #    使「❌ 行数 ≠ 失败清单条数」而误报解析告警。
        for ln in lines[i + 1:]:
            s = ln.strip()
            if not s or not ln.startswith("    ") or s.startswith("["):
                break
            full.append(s)

    rows, cur = [], None
    for ln in lines:
        mm = ROW_RE.match(ln)
        if mm and mm.group("tag") in ("❌", "ALLOW"):
            cur = dict(tag=mm.group("tag"), reasons=[])
            rows.append(cur)
            continue
        if cur is not None and ln.startswith("        · "):
            cur["reasons"].append(ln.strip()[2:].strip())

    bad = [r for r in rows if r["tag"] == "❌"]
    n_allow = len(rows) - len(bad)
    if len(bad) != len(full):
        return dict(checked=checked, failed=failed, items=[], allow=n_allow,
                    mismatch=(len(bad), len(full)))
    items = [(rel, r["reasons"]) for r, rel in zip(bad, full)]
    return dict(checked=checked, failed=failed, items=items, allow=n_allow, mismatch=None)


def build_work_order(rawdir: str, out_path: Path):
    """从 rawdir 里的逐域原始输出，生成可委派工单。返回 (总失败数, 出场域数)。"""
    per_dom, all_items, tot_ck, tot_f, tot_allow, mismatches = [], [], 0, 0, 0, []
    for domain, note in DOMAINS:
        raw = Path(rawdir) / (re.sub(r"[^\w]+", "_", domain) + ".txt")
        if not raw.is_file():
            continue
        d = parse_raw(raw)
        tot_ck += d["checked"]; tot_f += d["failed"]; tot_allow += d["allow"]
        if d["mismatch"]:
            mismatches.append((domain, d["mismatch"]))
        per_dom.append((domain, note, d))
        for rel, reasons in d["items"]:
            grp, mech = classify(" ".join(reasons))
            all_items.append(dict(rel=rel, reasons=reasons, grp=grp, mech=mech, dom=domain))

    gc = Counter(i["grp"] for i in all_items)
    dc = Counter(i["dom"] for i in all_items)
    ac = Counter(advice_for(i["dom"]) for i in all_items)
    n_mech = sum(1 for i in all_items if i["mech"])

    L = []
    L.append("---")
    L.append("title: 公式渲染缺陷工单 %s" % datetime.date.today().isoformat())
    L.append("type: 审计")
    L.append("created: %s" % datetime.date.today().isoformat())
    L.append("updated: %s" % datetime.date.today().isoformat())
    L.append("tags: [公式渲染, 工单, 内容线]")
    L.append("---")
    L.append("")
    L.append("# 公式渲染缺陷工单 · %s" % datetime.date.today().isoformat())
    L.append("")
    L.append("> **这份工单解决什么**：「有 %d 份文件公式渲染不出来」是个没法动手的数字；" % tot_f)
    L.append("> 本文把它拆成「**哪些域、多少份、坏在哪、谁先做、哪些不该做**」，")
    L.append("> 且每份都附**闸门给的原因原文** —— 拿起来就能改，不用先自己扫一遍。")
    L.append(">")
    L.append("> **一句话**：共 **%d** 份 —— %s；"
             % (tot_f, "、".join("%s **%d** 份" % (k, v) for k, v in ac.most_common())))
    L.append("> 其中**机械可修 %d 份**，其余 **%d 份必须回原书/原式校正**。"
             % (n_mech, tot_f - n_mech))
    L.append(">")
    L.append("> **复跑**（改完一批后刷新本表，同一条命令）：")
    L.append("> `python -X utf8 11-模板/scripts/render_health.py --raw-dir %s --work-order <本文件路径>`" % rawdir)
    L.append(">")
    L.append("> **口径**：排除 `_归档/`（死文件）；文档类域（审计报告 / 数据库表 / 索引 / README）不检查")
    L.append("> —— 那里 `$` 常是价格、散文描述、DataviewJS 语法。判据 = `render_gate.py`（产物字面 `$` == 0 且无 texmath 转换失败）。")
    L.append("")
    L.append("## 一、汇总（与闸门对账）")
    L.append("")
    L.append("| 域 | 受检 | 失败 | 允许 | 处置建议 |")
    L.append("|:--|--:|--:|--:|:--|")
    for domain, note, d in per_dom:
        L.append("| `%s/` | %d | %s | %d | %s |"
                 % (domain, d["checked"],
                    ("**%d**" % d["failed"]) if d["failed"] else "0 ✅",
                    d["allow"], advice_for(domain)))
    L.append("| **合计** | **%d** | **%d** | **%d** | |" % (tot_ck, tot_f, tot_allow))
    L.append("")
    L.append("> **对账**：分组明细合计 **%d** == 各域失败数合计 **%d** %s"
             % (sum(gc.values()), tot_f, "✅" if sum(gc.values()) == tot_f else "❌ 不符，需查"))
    L.append("> （不一致只可能来自原始输出解析失败，见文末「解析告警」。）")
    L.append("")
    if mismatches:
        L.append("### ⚠️ 解析告警（这些域的数字**不可信**）")
        L.append("")
        for dom, (a, b) in mismatches:
            L.append("- `%s`：`❌` 行 %d 条 ≠ 失败清单 %d 条 —— 解析器不猜，该域未纳入明细。" % (dom, a, b))
        L.append("")
    L.append("## 二、按根因分组")
    L.append("")
    L.append("| 组 | 份数 | 机械可修 | 备注 |")
    L.append("|:--|--:|:--|:--|")
    REMARK = {
        "B栏｜TAB 残名（真制表符吃掉命令首字母）": "`md_sanitize.fix_tab_pollution` 可修",
        "B栏｜行首 `<div>`（Obsidian 下吞块内 markdown）": "`import_gate --fix` 可修",
        "A栏｜HTML 实体混入数学域": "`md_sanitize.fix_html_entities_in_math` 可修",
        "A栏｜`" + BS + "text{…" + BS + "cmd{…}}` 文本命令嵌套": "`md_sanitize.fix_text_inner_cmd` 可修",
        "A栏｜双反斜杠 `" + BS + BS + "`（仅 array 类环境内合法）": "**须看上下文**：在 `\\begin{cases}`/`array` 内合法",
    }
    for g, n in gc.most_common():
        mech = next((i["mech"] for i in all_items if i["grp"] == g), False)
        L.append("| %s | %d | %s | %s |"
                 % (g, n, "✅" if mech else "❌", REMARK.get(g, "")))
    L.append("")
    L.append("## 三、明细（按「域处置建议 → 份数」排序）")
    L.append("")
    order = sorted(dc.items(), key=lambda kv: (advice_for(kv[0]), -kv[1]))
    for dom, _ in order:
        items = [i for i in all_items if i["dom"] == dom]
        if not items:
            continue
        L.append("### `%s/` —— %d 份（%s）" % (dom, len(items), advice_for(dom)))
        L.append("")
        L.append("| # | 文件 | 闸门原因（原文） |")
        L.append("|--:|:--|:--|")
        for k, i in enumerate(sorted(items, key=lambda x: x["rel"]), 1):
            rsn = "；".join(i["reasons"]) or "—"
            rsn = rsn.replace("|", BS + "|")
            L.append("| %d | `%s` | %s |" % (k, i["rel"], rsn))
        L.append("")
    L.append("## 四、怎么用这张工单")
    L.append("")
    L.append("1. **先看「建议不修」的域** —— 那是原始 OCR 存档，修存档不如重新导入；")
    L.append("   把它们当作「导入质量」的观测值，**不要排进工作队列**。")
    L.append("2. **再从 P0/P1 往下做**，每改完一批就**复跑**（见文开头命令）刷新本表；")
    L.append("   份数下降即进度，新出现的项即回归。")
    if n_mech:
        L.append("3. **机械可修的 %d 份**（见分组表「机械可修」列）：可直接跑 "
                 "`import_gate.py --domain <域> --fix`（带备份）；其余必须**回原书/原式**校正。" % n_mech)
    else:
        L.append("3. ⚠️ **本批没有任何一份是机械可修的** —— **全部得回原书/原式校正**。")
        L.append("   这不是「工具不够好」：这些缺陷的形态就是「**公式本身被 OCR 打乱**」")
        L.append("   （多括号 `[\\mathrm{L}}]`、缺下划线 `nH2O`、无效宏、串行 `\\cdot L^{-1}H_3BO_3`），")
        L.append("   写不出可靠规则 —— 强写规则就会重演本会话已证伪的「按形状猜」错误。")
    L.append("4. ⛔ **不许**为了「清零」把 `$` 删掉或把公式改成纯文本：那会把「渲染失败」")
    L.append("   变成「静默的内容丢失」，后者更坏。改不动就标存疑，不要假装修好。")
    L.append("")
    L.append("## 五、本工单的边界（如实说明）")
    L.append("")
    L.append("- 分组是**启发式**：依据是 texmath 报错片段（截断 90 字符），**不是**对源文件的二次解析；")
    L.append("  原因原文列保留在明细里，人工可复核/改判。")
    L.append("- 只覆盖 `render_health.DOMAINS` 里登记的域；未登记的域（如 `04-题库/`）**未受检**。")
    L.append("- 「机械可修」= **本会话已验证过的净化规则**恰好覆盖该形态，不代表修完语义一定对；")
    L.append("  落盘后仍需复跑闸门确认。")
    L.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(L), encoding="utf-8", newline="")
    return tot_f, len(per_dom)


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
    ap.add_argument("--work-order", default=None, metavar="路径",
                    help="扫描后另生成「公式渲染缺陷工单」（分组 + 原因原文 + 处置建议）。"
                         "需与 --raw-dir 同用 —— 工单只从原始输出解析，不另立判据。")
    ap.add_argument("--parse-only", action="store_true",
                    help="**不扫描**，只从 --raw-dir 里已有的原始输出重建工单"
                         "（改完一批后刷新工单，不必重扫）。需与 --raw-dir / --work-order 同用。")
    args = ap.parse_args()

    if args.parse_only:
        if not (args.raw_dir and args.work_order):
            raise SystemExit("!! --parse-only 需同时给 --raw-dir 与 --work-order")
        n, doms = build_work_order(args.raw_dir, Path(args.work_order))
        print("（解析模式，未扫描）已生成工单：%s（失败 %d / 覆盖 %d 个域）"
              % (args.work_order, n, doms))
        return 1 if n else 0

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

    if args.work_order:
        if not args.raw_dir:
            raise SystemExit("!! --work-order 需要 --raw-dir（工单只从原始输出解析）")
        n, doms = build_work_order(args.raw_dir, Path(args.work_order))
        print("已生成工单：%s（失败 %d / 覆盖 %d 个域）" % (args.work_order, n, doms))

    return 1 if tot_f else 0


if __name__ == "__main__":
    raise SystemExit(main())
