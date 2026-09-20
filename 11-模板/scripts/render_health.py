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
    # ── 重型域：**默认不跑**（太贵），需要时用 `--only 04-题库` 或 `--include-heavy` ──
    ("04-题库", "题库主池（6000+ 份 ≈ 1 小时）—— 默认跳过，需要时点名跑"),
]

# 默认排除的重型域（`--include-heavy` 或 `--only <它>` 才会跑）
HEAVY = {"04-题库"}

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
    # ⚠️ 清单文件**每轮只用一个、反复覆盖**（不是每域写一个再删）。
    #    2026-09-21 实测事故：原先每域写一个再 `unlink` → 第 **50** 次删除触发环境的
    #    **safe-delete 批量确认拦截** → 异常直接中断整轮扫描（18 域只跑完 11 域）。
    #    故改为「按 pid 命名、全程复用、结束时清一次」（单次删除不会触阈值）。
    mf = VAULT / (".workbuddy/tmp/_health_%d.txt" % os.getpid())
    mf.parent.mkdir(parents=True, exist_ok=True)
    mf.write_text("\n".join(files) + "\n", encoding="utf-8", newline="\n")

    t0 = time.monotonic()
    r = subprocess.run([PY, "-X", "utf8", str(GATE), "--manifest", str(mf)],
                       capture_output=True, cwd=VAULT)
    secs = time.monotonic() - t0
    out = (r.stdout or b"").decode("utf-8", "replace") + \
          (r.stderr or b"").decode("utf-8", "replace")

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

# 域 → 处置建议（决定工单人先看谁）。
# 分级依据是**实测的产出路径**（不是猜），2026-09-21 实地核过：
#   · **交付路径**（产出学生/教师手上的文件）：
#     `06-学生侧材料/` 有 **319 docx**；`13-教案/` **52 docx**；
#     `04-课件/习题集/` 的 docx 在 `00-首页/题组Word/`（**640 份**）；
#     `04-课件/学生讲义/` 的 docx 在 `06-学生侧材料/讲义/`。
#   · **阅读路径**（不进 Word，但 Agent 反复读取）：KP / 提炼 / 专题题型。
#   · **源层**：原始 OCR 存档 —— **建议不修**（修存档不如重新导入）。
def advice_for(domain: str) -> str:
    if domain in ("06-外部资料导入", "mineru", "mineru02"):
        return "⛔ 建议不修"
    if domain in ("06-学生侧材料", "04-课件/习题集", "04-课件/学生讲义", "13-教案"):
        return "🔴 P0 交付路径"
    if domain == "03-知识点":
        return "🟠 P1 KP 页"
    if domain in ("07-资料提炼", "04-专题与题型", "高考化学", "02-考纲条目"):
        return "🟡 P2 阅读/提炼"
    return "🟢 P3 其他课件（实测未见交付产物，需按需定级）"


def classify(blob: str):
    """按**闸门给出的证据**分组。返回 (组名, 形状提示)。

    ⚠️ 2026-09-21 自我更正：组名**曾经断言成因**（如「文本命令嵌套」），但那是从
    **报错片段**（截断 90 字符）推的 —— 实测 12 份「文本命令嵌套」的源文件里
    `\\text{…\\cmd{…}}` 形态**一处都没有**。故：
      · **B 栏**四条 = `render_gate` 的 B 栏签名**直接命中**（可靠）；
      · **A 栏**分组 = 描述「**报错片段里出现了什么**」，**不宣称成因**。
    成因以工单明细里的「原因原文」为准。
    """
    if "行首 <div>" in blob:
        return "B栏｜行首 `<div>`（B 栏签名直接命中）", False
    if "TAB 残名" in blob:
        return "B栏｜TAB 残名（B 栏签名直接命中）", True
    if BS + "AA" in blob:
        return "B栏｜`" + BS + "AA`（B 栏签名直接命中）", True
    if BS + "text{" + BS + "text{" in blob:
        return "B栏｜`" + BS + "text{" + BS + "text{}}` 嵌套（B 栏签名直接命中）", True
    if "docx 转换失败" in blob:
        if any(k in blob for k in ("&lt;", "&gt;", "&amp;")):
            return "A栏｜报错片段含 HTML 实体（`&lt;` 等）", True
        if "unexpected control sequence" in blob:
            return "A栏｜报错为 `unexpected control sequence`（双反斜杠类）", False
        if blob.count(BS + "text") >= 2:
            return "A栏｜报错片段含多个 `" + BS + "text` 标记", False
        if "}}" in blob or "}]" in blob or ("{" in blob and "}" not in blob):
            return "A栏｜报错片段含 `}}` / `}]`（疑似花括号多余）", False
        return "A栏｜其他 texmath 报错", False
    if "产物字面 $" in blob:
        return "A栏｜仅字面 `$`（无 texmath 报错；多为算式不配平）", False
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


def _load_sanitizer():
    """载入同目录的 `md_sanitize`（用于**实测**「该文件能否被机械净化」）。"""
    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    try:
        import md_sanitize
        return md_sanitize
    except Exception:
        return None


def _sanitize_would_change(san, rel: str) -> bool:
    """**实测**该文件能否被机械净化 = 跑一遍 `sanitize()` 看前后是否变化。

    ⚠️ 2026-09-21 自我更正：本列**曾经是按「形状」猜的**（「这个分组名看起来
    有对应规则 ⇒ 标机械可修」）—— 结果 15 份里**一份都改不动**：
    `import_gate --no-run`（预检）报「可修 **0** / 无需改动 15」。
    根因是分组名来自**闸门报出的报错片段**（截断 90 字符），并不是对源文件的解析；
    片段里出现两次 `\\text` 就被我判成「文本命令嵌套」，而源文件里根本没有那个形态。
    → **判据必须按结果**：跑一遍 `sanitize()`，变化才算可修。
    """
    if san is None:
        return False
    try:
        t = (VAULT / rel).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    try:
        return san.sanitize(t) != t
    except Exception:
        return False


def build_work_order(rawdir: str, out_path: Path, parsed=None):
    """从 rawdir 里的逐域原始输出，生成可委派工单。返回 (总失败数, 覆盖域数)。

    `parsed` 可传入已解析结果（`read_raw_dir()` 的返回值）以免重复解析。
    """
    per_dom = read_raw_dir(rawdir) if parsed is None else parsed
    san = _load_sanitizer()
    all_items, tot_ck, tot_f, tot_allow, mismatches = [], 0, 0, 0, []
    for domain, note, d in per_dom:
        tot_ck += d["checked"]; tot_f += d["failed"]; tot_allow += d["allow"]
        if d["mismatch"]:
            mismatches.append((domain, d["mismatch"]))
        for rel, reasons in d["items"]:
            grp, _shape = classify(" ".join(reasons))
            # ⭐ 可修与否**实测**（跑一遍 sanitize 看是否变化），不按分组名猜
            all_items.append(dict(rel=rel, reasons=reasons, grp=grp,
                                  mech=_sanitize_would_change(san, rel), dom=domain))

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
    L.append("> 其中**实测可净化 %d 份**，其余 **%d 份必须回原书/原式校正**。"
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
    L.append("## 二、按**报错片段**分组（启发式，只用于排优先级）")
    L.append("")
    L.append("| 组 | 份数 | 其中实测可净化 | 备注 |")
    L.append("|:--|--:|--:|:--|")
    REMARK = {
        "B栏｜TAB 残名（B 栏签名直接命中）": "对应 `md_sanitize.fix_tab_pollution`",
        "B栏｜行首 `<div>`（B 栏签名直接命中）": "对应 `import_gate --fix`",
        "A栏｜报错片段含 HTML 实体（`&lt;` 等）": "对应 `md_sanitize.fix_html_entities_in_math`（只覆盖 `$…$` 内）",
        "A栏｜报错为 `unexpected control sequence`（双反斜杠类）": "**须看上下文**：在 `\\begin{cases}` / `array` 内合法",
    }
    for g, n in gc.most_common():
        mg = sum(1 for i in all_items if i["grp"] == g and i["mech"])
        L.append("| %s | %d | %d | %s |" % (g, n, mg, REMARK.get(g, "")))
    L.append("")
    L.append("> **「实测可净化」的算法**：对每份文件真跑一遍 `md_sanitize.sanitize()`，")
    L.append("> **前后有变化**才算 —— 不是「看起来像某个已知形态」。")
    L.append("> 而**分组名**依据的是 `render_gate` 报出的**报错片段**（截断 90 字符），属**启发式**：")
    L.append("> 同组内可能混有不同成因，**一律以明细里的「原因原文」为准**，不要按组名下结论。")
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
        L.append("3. **实测可净化的 %d 份**：直接跑 `import_gate.py --domain <域> --fix`（带备份）；"
                 "其余必须**回原书/原式**校正。" % n_mech)
    else:
        L.append("3. ⚠️ **本批没有任何一份能被机械净化**（实测：`sanitize()` 改动量为 0）")
        L.append("   —— **全部得回原书/原式校正**。这不是「工具不够好」：")
        L.append("   这些缺陷的形态是「**公式本身被 OCR 打乱**」（多括号 `[\\mathrm{L}}]`、")
        L.append("   缺下划线 `nH2O`、无效宏、串行 `\\cdot L^{-1}H_3BO_3`），写不出可靠规则 ——")
        L.append("   强写规则就会重演「按形状猜」的错误（本工单的「可净化」列**已被这个错误坑过一次**）。")
    L.append("4. ⛔ **不许**为了「清零」把 `$` 删掉或把公式改成纯文本：那会把「渲染失败」")
    L.append("   变成「静默的内容丢失」，后者更坏。改不动就标存疑，不要假装修好。")
    L.append("")
    L.append("## 五、本工单的边界（如实说明）")
    L.append("")
    L.append("- 分组是**启发式**：依据是 texmath 报错片段（截断 90 字符），**不是**对源文件的二次解析；")
    L.append("  原因原文列保留在明细里，人工可复核/改判。")
    L.append("- **重型域默认不跑**：`04-题库/`（6020 份 ≈ 1 小时）未纳入本次体检；")
    L.append("  抽样 99 份（两轮随机）**0 失败**，且它经生成器进成书层、成书层实测全绿 ⇒")
    L.append("  需要时用 `--only 04-题库` 单独跑。")
    L.append("- 「实测可净化」= **真跑 `md_sanitize.sanitize()`、前后有变化**（实测而非形状推断）。")
    L.append("  即便可净化，也只保证「不再报错」，**不保证语义一定对** —— 落盘后仍须复跑闸门确认。")
    L.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(L), encoding="utf-8", newline="")
    return tot_f, len(per_dom)


def read_raw_dir(rawdir: str):
    """读 rawdir 里逐域原始输出 → [(domain, note, res)]（保持 DOMAINS 顺序）。

    ⭐ 用途：**不重扫也能重建报告** —— 改完一批缺陷后，只刷新汇总表/快照/工单，
    省掉一次几十分钟的全量扫描。
    """
    out = []
    for domain, note in DOMAINS:
        raw = Path(rawdir) / (re.sub(r"[^\w]+", "_", domain) + ".txt")
        if not raw.is_file():
            continue
        d = parse_raw(raw)
        out.append((domain, note, dict(files=None, checked=d["checked"], failed=d["failed"],
                                       secs=0.0, line="", raw=str(raw), allow=d["allow"],
                                       items=d["items"], mismatch=d["mismatch"])))
    return out


def render_table(rows):
    """rows = [(domain, note, res)] → (markdown 表, 受检合计, 失败合计)。"""
    tot_ck = sum(r[2]["checked"] for r in rows)
    tot_f = sum(r[2]["failed"] for r in rows)
    o = ["| 域 | 受检 | 失败 | 占比 | 说明 |", "|:--|--:|--:|--:|:--|"]
    for d, note, r in rows:
        pct = ("%.1f%%" % (100.0 * r["failed"] / r["checked"])) if r["checked"] else "—"
        o.append("| `%s/` | %d | %s | %s | %s |"
                 % (d, r["checked"], ("**%d**" % r["failed"]) if r["failed"] else "0 ✅",
                    pct, note))
    o.append("| **合计** | **%d** | **%d** | **%.1f%%** | |"
             % (tot_ck, tot_f, (100.0 * tot_f / tot_ck) if tot_ck else 0.0))
    return "\n".join(o), tot_ck, tot_f


def write_snapshot(table: str):
    """把汇总表存档到 `09-审计报告/<日期>-公式健康度快照.md`，返回路径。"""
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
    return p


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
    ap.add_argument("--include-heavy", action="store_true",
                    help="也跑重型域（`04-题库/` 6000+ 份 ≈ 1 小时）。默认跳过 —— "
                         "它经生成器进成书层，而成书层实测全绿；需要时再单独跑。")
    ap.add_argument("--work-order", default=None, metavar="路径",
                    help="扫描后另生成「公式渲染缺陷工单」（分组 + 原因原文 + 处置建议）。"
                         "需与 --raw-dir 同用 —— 工单只从原始输出解析，不另立判据。")
    ap.add_argument("--parse-only", action="store_true",
                    help="**不扫描**，只从 --raw-dir 里已有的原始输出重建工单"
                         "（改完一批后刷新工单，不必重扫）。需与 --raw-dir / --work-order 同用。")
    args = ap.parse_args()

    if args.parse_only:
        if not args.raw_dir:
            raise SystemExit("!! --parse-only 需要 --raw-dir")
        rows = read_raw_dir(args.raw_dir)
        if not rows:
            raise SystemExit("!! --raw-dir 里没有可解析的原始输出：%s" % args.raw_dir)
        table, tot_ck, tot_f = render_table(rows)
        print("\n（解析模式，**未扫描** —— 数据来自已存原始输出）")
        print(table)
        print("\n受检 %d / 失败 %d（覆盖 %d 个域）" % (tot_ck, tot_f, len(rows)))
        print("请核对覆盖域是否齐全（应对照 --list 的域数；缺域＝那域还没扫过）。")
        if args.save:
            print("已存档：%s" % write_snapshot(table).relative_to(VAULT))
        if args.work_order:
            n, doms = build_work_order(args.raw_dir, Path(args.work_order), rows)
            print("已生成工单：%s（失败 %d / 覆盖 %d 个域）" % (args.work_order, n, doms))
        return 1 if tot_f else 0

    todo = [(d, note) for d, note in DOMAINS
            if (not args.only or d in args.only)
            and d not in args.skip
            # 重型域：只在「被点名（--only）」或「显式 --include-heavy」时跑
            and (d not in HEAVY or args.include_heavy
                 or (args.only is not None and d in args.only))]

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

    table, tot_ck, tot_f = render_table(rows)

    print("\n" + table)
    print("\n总耗时 %.0fs（受检 %d / 失败 %d）" % (time.monotonic() - t_all, tot_ck, tot_f))
    print("口径：排除 `_归档/`；文档类域不检查（见 `render_gate.should_check`）。")

    if args.save:
        print("\n已存档：%s" % write_snapshot(table).relative_to(VAULT))

    if args.work_order:
        if not args.raw_dir:
            raise SystemExit("!! --work-order 需要 --raw-dir（工单只从原始输出解析）")
        n, doms = build_work_order(args.raw_dir, Path(args.work_order))
        print("已生成工单：%s（失败 %d / 覆盖 %d 个域）" % (args.work_order, n, doms))

    # 清单文件：全程复用同一个，这里**只删一次**（单次删除不会触发 safe-delete 批量阈值）
    try:
        (VAULT / (".workbuddy/tmp/_health_%d.txt" % os.getpid())).unlink()
    except OSError:
        pass

    return 1 if tot_f else 0


if __name__ == "__main__":
    raise SystemExit(main())
