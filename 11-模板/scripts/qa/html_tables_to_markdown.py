# -*- coding: utf-8 -*-
"""HTML 表格 → Markdown pipe table 转换工具（qa/ 常驻版，2026-09-20）

## 为什么转

块级 HTML 表格（`<table>` 独占一行）在 Obsidian 里被判为 `html_block`，
**块内内容完全不经过 inline 解析** → 单元格里的 `$...$` 显示为原始文本（不渲染）。
转成 pipe table 后有两处收益（2026-09-20 端到端实证）：

1. **Obsidian 公式恢复渲染**：`math_inline` 恢复调用。
2. **Word 导出保留表格结构**：HTML 表 `w:tbl`=0（内容拍平成段落），
   pipe 表 `w:tbl`=1。实测 6 样本 `w:tbl` 前→后 = 1→80 / 0→79 / 11→44 /
   33→43 / 5→8 / 15→21，公式（OMML）数**完全不变**（零回归）。

## 与既有脚本的区别

- `11-模板/scripts/convert_html_tables_to_markdown.py`（2026-08-30）：旧一次性脚本，
  绑定 `习题书V2-表格分类台账.jsonl`，仅 `04-题库` 习题书源，不支持 span。
  **本工具是它的通用化继任者**，该旧脚本保留不动。
- `build-all-handout-docx.py::_convert_html_tables()`：Word 管线**运行时**内嵌转换
  （不写回 md，无 span/entity 支持）。本工具是**离线批量治理**版。
- ~~`.workbuddy/tmp/_dcv.py`~~（D 项一次性转换器）：**2026-09-20 已并入本工具**
  （`--qa-cards`）→ 见下节「D 通道」。

## D 通道（`--qa-cards`）：评分卡 → 题干段 + 引用块

2026-09-20 由 `tmp/_dcv.py` 并入（commit `a7f0cb458`）。**并入等价性已实证**：
D 项 16 文件从「转换前」备份用本工具重转，产物与仓库现状**逐字节一致（16/16）**；
34 张样本表逐表比对旧转换器输出 **34/34 完全一致**。

**三通道调度**（`plan_one`）：主通道（数据表 → pipe）先试；拒收后若开 `--qa-cards`，
再试 D 通道（评分卡 → 题干段+引用块）。两通道判据独立，不会对同一表都成功。

**三条关键规则**（均有实证，详见 `convert_qa_card()` docstring）：
1. `is_answer` **只用「N分」得分标记**（用「题号 + `$`」会误判含公式的题干行）
2. 表内子表（表头 + ≥2 数据行）→ 转 pipe，**不得降级为裸文本**
3. **span 展开守恒**（文本只在起始格出现一次）；sandwich 复合卡**整表拒收**

**四口径适配**：D 通道产物**不是表格**，故
① 「宽度一致」口径**只对 pipe 通道生效**；
② D 通道改用「**内容守恒**」（原表每个非空单元格文本须在产物中出现）。
⚠️ 未适配时 D 形态会因 `widths_ok=False` **假失败被跳过**（2026-09-20 反向验证实证）。

## 支持形态

| 形态 | 处理 |
|:---|:---|
| 普通表 | 直转 |
| **colspan** | 左对齐展开（内容放首列、后 N-1 列留空） |
| **rowspan** | 下拉填充（内容在接下来 n 行逐行重复）—— 730 张中 727 张可保真 |
| **HTML 实体** `&gt;`/`&lt;` 等 | `html.unescape` 后转（`--allow-entities`） |
| 纯文字表（无公式） | 照转（`--all-tables`）—— Word 侧有收益 |
| **评分卡/问答卡**（`--qa-cards`） | **D 通道**：拆表格包裹 → 题干段 + 答案引用块（`> `） |

## 保守拒收判据（宁可不转，不可转坏）

含 `<img` / 列数 0 或 >12 / **列数 = 1（单列 = 段落伪装）** /
**窄表（≤2 列）单元格平均文本 >40 字** / **单格 >800 字** /
单元格 `$` 数为奇数（OCR 半包）/（entity 开启时）解码后仍含 `<img` 或真标签。

> 2026-09-20 规则修正：原「列数 ≤2 拒收」误杀真 2 列数据表（如「温度/K | δ/ppm」）；
> 原「平均 >40 字拒收」误杀宽表内的长文本单元格。现改为①只拒单列 ②长度阈值只对
> 窄表生效，另设单格 800 字硬上限。修正后 04-课件/习题集 多转 15 表、04-题库 多转 17 表。
>
> 2026-09-20 规则修正二：原「列数 >8 拒收」**误杀真数据表** —— 实证 `n l m ms` 量子数表
> （10 列）、水化焓/晶格能热力学表（9 列）、分子几何构型对照（9 列）、Hammett σ 取代基表
> （9 列）全为规整数据表，公式却因拒收而仍不渲染。宽表窄屏显示差 << 公式变乱码，故上限放宽至 12。

## 用法（受管解释器 + 安全前缀）

    PY="C:/Users/蕾赛/.workbuddy/binaries/python/versions/3.13.12/python.exe"

    # 默认 dry-run（只报告，不写盘）
    $PY -X utf8 11-模板/scripts/qa/html_tables_to_markdown.py --dir "06-外部资料导入"

    # 实际写入（自动备份 + 渲染自证 + 四口径验证）
    $PY -X utf8 11-模板/scripts/qa/html_tables_to_markdown.py --dir X --apply

    # 全量口径（含纯文字表 + entity 解码）
    $PY -X utf8 11-模板/scripts/qa/html_tables_to_markdown.py --dir X --all-tables --allow-entities --apply

    # 启用 D 通道（评分卡 → 题干段 + 引用块；含公式的评分卡必备）
    $PY -X utf8 11-模板/scripts/qa/html_tables_to_markdown.py --dir X --qa-cards --apply

    # 全库扫描（排红线/活跃线）
    $PY -X utf8 11-模板/scripts/qa/html_tables_to_markdown.py --whole-vault

## 验收防线（--apply 自动执行）

① 渲染自证（markdown-it + KaTeX，残留 `$`==0）② 四口径（本次表残留 0 /
行数守恒 / 宽度一致[pipe 通道] / 内容守恒[D 通道] / 行尾保持 / 行结构自洽）
③ 备份（已存在则不覆盖）。

## 相关

- Word 端到端验证：`word_verify.py`
- 全库基线：`table_baseline.py`
- 方法论与踩坑：WorkBuddy skill `html-block-table-to-md`、`09-审计报告/` 各 Wave 报告
"""

from __future__ import annotations

import argparse
import hashlib
import html as html_mod
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ── 统一 chdir 到 vault 根（与 qa/ 其他脚本一致，从任意目录调用均可）──
try:
    os.chdir(r"C:\Obsidion\妙妙屋")
except Exception:
    pass

VAULT = Path(r"C:\Obsidion\妙妙屋")
TMP = VAULT / ".workbuddy" / "tmp"
DEFAULT_BACKUP = TMP / "html_table_backup"

EXCLUDE_PREFIX = ("04-题库", "05-真题库", "04-课件", "07-资料提炼",
                  "_归档", ".git", ".obsidian",
                  ".workbuddy", "node_modules", "媒体仓库")

TABLE_BLOCK = re.compile(r"<table\b[^>]*>.*?</table>", re.I | re.S)
ROW_PAT = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.I | re.S)
CELL_ATTR_PAT = re.compile(r"<t[dh]\b([^>]*)>(.*?)</t[dh]>", re.I | re.S)
SPAN_COL = re.compile(r"colspan\s*=\s*[\"']?(\d+)", re.I)
SPAN_ROW = re.compile(r"rowspan\s*=\s*[\"']?(\d+)", re.I)
ENTITY_PAT = re.compile(r"&(?:#\d+|#x[0-9a-f]+|[a-z]+);", re.I)
MATH_SPAN = re.compile(r"\$[^$\n]{1,400}\$")
HARD_CELL_LEN = 800  # 单格字数上限：超过则拒收（Word 单元格会撑爆）

NODE = r"C:\Users\蕾赛\.workbuddy\binaries\node\versions\22.22.2-2\node.exe"
NODE_PATH = r"C:\Users\蕾赛\.workbuddy\binaries\node\workspace\node_modules"
SELFCHECK = Path(__file__).parent / "render_selfcheck.js"


def norm_cell(c: str) -> str:
    """单元格规整：剥标签、<br> 转空格、实体解码、空白归一。"""
    c = re.sub(r"<br\s*/?>", " ", c, flags=re.I)
    c = re.sub(r"<[^>]+>", "", c)
    c = html_mod.unescape(c)
    c = c.replace("\n", " ")
    c = re.sub(r"[ \t\u00a0\u200b]+", " ", c).strip()
    return c


def _esc_link_bracket(seg: str) -> str:
    return re.sub(r"\[([^\]\[\n]{1,80})\]\(", r"\\[\1](", seg)


def fix_bracket_link(text: str) -> str:
    """把 `$...$` 之外、会构成 markdown 链接的 `[` 转义为 `\\[`。

    单元格 `[GTP]($\\mu...$)` 转 pipe 表后，markdown 会把 `[GTP](` 识别为
    **链接**、`$` 被吞 → 公式不渲染。公式内部的 `[` 不受影响。
    """
    out = []
    pos = 0
    for m in MATH_SPAN.finditer(text):
        out.append(_esc_link_bracket(text[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(_esc_link_bracket(text[pos:]))
    return "".join(out)


def _build_grid(rows):
    """(text, rowspan, colspan) 三元组 → 网格。

    · colspan=n：内容放首列、后 n-1 列留空（左对齐展开）。
    · rowspan=n：内容在接下来 n 行逐行重复（下拉填充，99.6% 可保真）。
    """
    grid = []
    for ri, r in enumerate(rows):
        while len(grid) <= ri:
            grid.append([])
        for (txt, rs, cs) in r:
            ci = 0
            while ci < len(grid[ri]) and grid[ri][ci] is not None:
                ci += 1
            for k in range(cs):
                while ci + k >= len(grid[ri]):
                    grid[ri].append(None)
                grid[ri][ci + k] = txt if k == 0 else ""
            if rs > 1:
                for rr in range(ri + 1, ri + rs):
                    while len(grid) <= rr:
                        grid.append([])
                    for k in range(cs):
                        while ci + k >= len(grid[rr]):
                            grid[rr].append(None)
                        grid[rr][ci + k] = txt if k == 0 else ""
    width = max((len(g) for g in grid), default=0)
    for g in grid:
        while len(g) < width:
            g.append("")
    grid = [["" if c is None else c for c in g] for g in grid]
    grid = [g for g in grid if any(c.strip() for c in g)]
    return grid, width


# ══════════════════════════════════════════════════════════════════════
# D 通道：评分卡/问答卡 → 题干段 + 答案引用块（2026-09-20 并入，源自 tmp/_dcv.py）
#
# 适用形态：含「N分」得分标记的 HTML 表（评分卡 / 问答卡）。
# 这类表**不适合**转 pipe table —— 单元格是成段中文，「表格」只是视觉画框。
# 正解＝拆掉表格包裹，改为「题干普通段 + 答案引用块（`> `）」，公式随段落恢复 inline 渲染。
# 实证 16 文件 / 16 表（commit 1c4bb456f）。
#
# 三条关键规则（务必遵守，均有实证）：
#   1. `is_answer` **只用「N分」得分标记** —— 用「题号 + `$`」会把含公式的
#      **题干行**误判为答案行（如 `1-4 $IF_3$ 水解歧化,产物为三种常见无机物。`）。
#   2. 表内子表（表头 + ≥2 数据行）→ 转 **pipe table**，**不得降级为裸文本**
#      （首轮 120 行数据裸行缺陷的根因）。
#   3. **span 展开守恒**：`colspan`/`rowspan` 的文本**只在起始格出现一次**，
#      其余空占位；误当「复制」→ 内容膨胀 N 倍（首轮实证）。
#      `rowspan` 复合评分卡（答案-数据-答案 sandwich）→ **整表拒收**（不可拆）。
# ══════════════════════════════════════════════════════════════════════

# 得分标记：`20分` / `（20分）` / `(2.5分)`
SCORE_RE = re.compile(r"[（(]?\s*\d+(?:\.\d+)?\s*分\s*[)）]?")

# D 通道内部同款判据（与主通道共用 ENTITY_PAT / MATH_SPAN）
_D_ROW = re.compile(r"<tr\b[^>]*>.*?</tr>", re.I | re.S)
_D_CELL = re.compile(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", re.I | re.S)
_D_TAG = re.compile(r"<t[dh]\b[^>]*>", re.I)
_D_BLOCK_HTML = re.compile(
    r"<(details|summary|div|p|ul|ol|li|blockquote|figure|section)\b", re.I)


def _d_cell_text(c: str) -> str:
    """D 通道单元格取文本：剥行内标签 + 解码常见实体（不剥块级标签，由防线拦）。"""
    c = re.sub(r"</?(?:p|div|span|b|i|u|em|strong)\b[^>]*>", "", c, flags=re.I)
    for a, b in (("&gt;", ">"), ("&lt;", "<"), ("&amp;", "&"), ("&nbsp;", " ")):
        c = c.replace(a, b)
    return c.strip()


def _d_rows_of_rich(block):
    """按 <tr> 返回 [(text, ncells, cells)]，保留单元格数（子表边界识别用）。

    ⚠️ span 语义：colspan/rowspan 是「一格跨多列/多行」，其文本**只在起始
    位置出现一次**，其余位置为空占位。绝不能把文本复制到每个跨越格。
    展开后「有效（非空）单元格」才参与判定。
    """
    rows = _D_ROW.findall(block)
    grid = []
    carry = {}                       # (r,c) -> True（被上方 rowspan 占位）
    for r, tr in enumerate(rows):
        tags = _D_TAG.findall(tr)
        vals = [_d_cell_text(c) for c in _D_CELL.findall(tr)]
        cspans, rspans = [], []
        for tag in tags:
            cs = SPAN_COL.search(tag)
            rs = SPAN_ROW.search(tag)
            cspans.append(int(cs.group(1)) if cs else 1)
            rspans.append(int(rs.group(1)) if rs else 1)
        row = []
        ci = 0
        col = 0
        while ci < len(vals):
            while (r, col) in carry:          # 上方 rowspan 占位 → 跳过
                row.append("")
                col += 1
            v = vals[ci]
            cs = cspans[ci] if ci < len(cspans) else 1
            rs = rspans[ci] if ci < len(rspans) else 1
            row.append(v)                     # 文本只在起始格
            for k in range(1, cs):            # colspan 其余格：空
                row.append("")
            for rr in range(1, rs):           # rowspan 下方行：占位
                for k in range(cs):
                    carry[(r + rr, col + k)] = True
            col += cs
            ci += 1
        while (r, col) in carry:
            row.append("")
            col += 1
        grid.append(row)
    out = []
    for row in grid:
        cells = [c for c in row if c]
        txt = (" ".join(cells) if len(cells) > 1 else cells[0]) if cells else ""
        out.append((txt, len(cells), cells))
    return out


def _d_is_answer(text: str) -> bool:
    """答案行判据：**仅**含得分标记（N分 / （N分））。

    ⚠️ 2026-09-20 修正：原判据「题号 + `$`」会误判含公式的**题干行**
    （如 `1-4 $IF_3$ 水解歧化,产物为三种常见无机物。`）→ 已去掉该分支。
    """
    return bool(SCORE_RE.search(text))


def _d_is_data_row(text: str) -> bool:
    """纯数据行：字段数 ≥2、无中文、至多 2 个字段不含数字。

    （允许 `p $K_a$ 3.80 4.00 4.60 4.90` 这类「符号列名 + 数值」组合。）
    """
    t = text.strip()
    if not t or len(t) > 90:
        return False
    if re.search(r"[\u4e00-\u9fff]", t):
        return False
    parts = t.split()
    if len(parts) < 2:
        return False
    nonnum = sum(1 for p in parts if not re.search(r"\d", p))
    return nonnum <= 2 and len(parts) - nonnum >= 2


def _d_is_subtable_head(text: str) -> bool:
    """子表表头行：短、无中文句读、字段数 ≥2（仅当后随 is_data_row 才采用）。"""
    t = text.strip()
    if not t or len(t) > 90:
        return False
    if re.search(r"[，。；：？！,;:]", t):
        return False
    return len(t.split()) >= 2


def _d_emit_subtable(rows):
    """把连续的数据行渲染成 pipe table（首行为表头）。"""
    lines = []
    head = rows[0]
    lines.append("| " + " | ".join(head) + " |")
    lines.append("|" + "---|" * len(head))
    for r in rows[1:]:
        r = (r + [""] * len(head))[:len(head)]
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def convert_qa_card(block: str):
    """D 通道：评分卡/问答卡 → 题干段 + 答案引用块。返回 (md, reason)。

    适用形态：
      · 任意宽度 ≤ 12；至少 1 行含「N分」得分标记（否则交回主通道）
      · 每行要么是「题干」（无得分标记），要么是「答案」（含得分标记）
      · 排除含 <img> / 块级 HTML / 未解码 entity
    """
    low = block.lower()
    if "<img" in low:
        return None, "d:img"
    if _D_BLOCK_HTML.search(low):
        return None, "d:blockhtml"
    if ENTITY_PAT.search(block):
        return None, "d:entity"
    w = max((len(_D_TAG.findall(tr)) for tr in _D_ROW.findall(block)), default=0)
    if w == 0 or w > 12:
        return None, f"d:width{w}"
    rich = [r for r in _d_rows_of_rich(block) if r[0]]
    if not rich:
        return None, "d:norows"
    # 形态校验：至少 1 行含得分标记（否则这不是答案卡）
    if not any(_d_is_answer(r[0]) for r in rich):
        return None, "noscore"

    blocks = []          # 逐段产出：("p", text) / ("q", text) / ("t", [cells...])
    i = 0
    n = len(rich)
    while i < n:
        text, nc, cells = rich[i]
        if _d_is_answer(text):
            blocks.append(("q", text))
            i += 1
            continue
        # 子表识别：本行可作表头，且后续 ≥2 行是纯数据行
        if nc >= 2 and _d_is_subtable_head(text):
            j = i + 1
            run = []
            while j < n and rich[j][1] >= 2 and _d_is_data_row(rich[j][0]):
                run.append(rich[j][2])
                j += 1
            if len(run) >= 2:
                blocks.append(("t", [cells] + run))
                i = j
                continue
        # 无表头的纯数据行（≥3 行连着）
        if nc >= 2 and _d_is_data_row(text):
            j = i
            run = []
            while j < n and rich[j][1] >= 2 and _d_is_data_row(rich[j][0]):
                run.append(rich[j][2])
                j += 1
            if len(run) >= 3:
                blocks.append(("t", run))
                i = j
                continue
        blocks.append(("p", text))
        i += 1

    # 后处理：孤立「数据行」若前后都是答案行 → 并入前一条引用块
    # （实证：3-2-2 的 `p $K_a$ 3.80 4.00 4.60 4.90` 独立成段形似乱码）
    merged = []
    for idx, (kind, payload) in enumerate(blocks):
        if kind == "p" and _d_is_data_row(payload):
            prev = merged[-1] if merged else None
            nxt = blocks[idx + 1] if idx + 1 < len(blocks) else None
            if prev and prev[0] == "q" and nxt and nxt[0] == "q":
                merged[-1] = ("q", prev[1] + " " + payload)
                continue
        merged.append((kind, payload))
    blocks = merged

    # ⚠️ sandwich 防线：数据表之后又出现答案行 → 属「评分卡 + 内嵌数据表 + 评分续行」
    # 复合形态，拆分会破坏语义（实证 3-2-2 的 rowspan 复合评分卡）→ 整表拒收。
    # 「数据表都在答案行之后」（尾部参考数据表）为正常形态，接受。
    seen_t = False
    for k, _ in blocks:
        if k == "t":
            seen_t = True
        elif k == "q" and seen_t:
            return None, "sandwich"

    parts = []
    for kind, payload in blocks:
        if kind == "q":
            parts.append("> " + payload)
        elif kind == "p":
            parts.append(payload)
        else:
            parts.append(_d_emit_subtable(payload))
    return "\n\n".join(parts), None


def convert_table(block: str, allow_entities: bool = False):
    """单表转换。返回 (markdown, reason)；reason 为 None 时成功。

    ⚠️ 本函数走「数据表 → pipe table」主通道。当表**不含得分标记**时
    （`noscore`），改由 `--qa-cards` 的 D 通道（`convert_qa_card()`）处理；
    未开 `--qa-cards` 时按原样返回 `noscore`（保持向后兼容）。
    """
    low = block.lower()
    if "<img" in low:
        return None, "img"
    # 表内含块级 HTML（<details>/<summary>/<div>/<p> 等）→ 单元格无法承载块级结构，
    # 强行转 pipe table 会把块级内容压进单元格并吞掉标签本身（2026-09-20 实证：
    # 3-晶体结构.md 表内嵌 <details> 折叠块，转换后 details/summary 各 -1）。
    if re.search(r"<(details|summary|div|p|ul|ol|li|blockquote|figure|section)\b", low):
        return None, "blockhtml"
    if ENTITY_PAT.search(block):
        if not allow_entities:
            return None, "entity"
        dec = html_mod.unescape(block)
        body = re.sub(r"</?(?:table|tr|td|th|thead|tbody)\b[^>]*>", "", dec, flags=re.I)
        if "<img" in body.lower():
            return None, "entity-img"
        if re.search(r"<(?!\/?(?:br|hr|sub|sup|b|i|u|em|strong)\b)[a-zA-Z]", body):
            return None, "entity-tag"

    rows = []
    for tr in ROW_PAT.findall(block):
        r = []
        for m in CELL_ATTR_PAT.finditer(tr):
            attrs, content = m.group(1), m.group(2)
            sm = SPAN_COL.search(attrs)
            cs = int(sm.group(1)) if sm else 1
            rm = SPAN_ROW.search(attrs)
            rs = int(rm.group(1)) if rm else 1
            r.append((norm_cell(content), rs, cs))
        if r:
            rows.append(r)
    if not rows:
        return None, "norows"

    grid, width = _build_grid(rows)
    if not grid:
        return None, "norows"
    # 宽度上限 8 → 12（2026-09-20 修正）：原上限**误杀真数据表**。
    # 实证：`n l m ms` 量子数表（10 列）、水化焓/晶格能热力学表（9 列）、
    # 分子几何构型对照（9 列）、Hammett σ 取代基表（9 列）——
    # 全是规整数据表，公式却因被拒收而**仍不渲染**。
    # 宽表在窄屏显示差 << 公式变 LaTeX 源码乱码，故放宽到 12。
    if width == 0 or width > 12:
        return None, f"width{width}"
    if width <= 1:
        # 单列表 = 段落伪装成表格，转 pipe table 无意义（2026-09-20 放宽）
        return None, f"narrow{width}"

    flat = [c for g in grid for c in g if c.strip()]
    if not flat:
        return None, "empty"
    # 单格超长（>800 字）→ 单元格会撑爆 Word，拒收
    if max(len(c) for c in flat) > HARD_CELL_LEN:
        return None, "hardprose"
    avg_len = sum(len(c) for c in flat) / len(flat)
    # prose 阈值只对窄表（<=2 列）生效；宽表不论长短都是真表格（2026-09-20 修正）
    if width <= 2 and avg_len > 40:
        return None, f"prose{int(avg_len)}"
    for c in flat:
        if c.replace("\\$", "").count("$") % 2 == 1:
            return None, "halfwrap"

    out = []
    for k, g in enumerate(grid):
        cells = [fix_bracket_link(c.replace("|", "\\|")) for c in g]
        out.append("| " + " | ".join(cells) + " |")
        if k == 0:
            out.append("| " + " | ".join(["---"] * width) + " |")
    return "\n".join(out), None


def iter_files(dirs=None, whole_vault=False, allow=()):
    """遍历 md。whole_vault 时全库（仍排 EXCLUDE_PREFIX）。

    allow: 显式放行前缀元组（如 ("04-课件",)）。命中的路径即使落在
    EXCLUDE_PREFIX 内也放行——用于用户授权的作用域（如成品区/红线区）。
    """
    def _excluded(s: str) -> bool:
        if any(s.startswith(a) for a in allow):
            return False
        return any(s.startswith(x) for x in EXCLUDE_PREFIX)

    if whole_vault:
        for p in sorted(VAULT.rglob("*.md")):
            s = str(p.relative_to(VAULT)).replace("\\", "/")
            if _excluded(s):
                continue
            yield p, s
    else:
        for d in (dirs or []):
            root = VAULT / d
            if not root.exists():
                print(f"⚠️ 目录不存在，跳过: {d}", file=sys.stderr)
                continue
            for p in sorted(root.rglob("*.md")):
                s = str(p.relative_to(VAULT)).replace("\\", "/")
                if _excluded(s):
                    continue
                yield p, s


def plan_one(p: Path, math_only=True, allow_entities=False, qa_cards=False):
    """扫描单文件的候选表。

    `qa_cards=True` 时启用 **D 通道兜底**：主通道（数据表 → pipe）拒收后，
    再试 D 通道（评分卡 → 题干段 + 引用块）。两通道判据相互独立：
    主通道专收「规整数据表」，D 通道专收「含 N分 得分标记的评分卡」，
    不会对同一张表都成功（D 通道要求 `SCORE_RE` 命中，主通道数据表通常无）。
    """
    raw = p.read_bytes()
    text = raw.decode("utf-8")
    items = []
    for m in TABLE_BLOCK.finditer(text):
        block = m.group(0)
        if math_only and not MATH_SPAN.search(block):
            continue
        md, reason = convert_table(block, allow_entities=allow_entities)
        channel = "pipe"
        if md is None and qa_cards:
            md2, reason2 = convert_qa_card(block)
            if md2 is not None:
                md, reason, channel = md2, None, "qa"
            else:
                reason = f"{reason}|{reason2}"
        items.append({"start": m.start(), "end": m.end(),
                      "original": block, "converted": md, "reason": reason,
                      "channel": channel if md is not None else None})
    return text, items, raw


def selfcheck(items):
    payload = json.dumps([{"id": i, "md": m} for i, m in items], ensure_ascii=False)
    env = dict(os.environ)
    env["NODE_PATH"] = NODE_PATH
    r = subprocess.run([NODE, str(SELFCHECK)], input=payload.encode("utf-8"),
                       capture_output=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"selfcheck failed: {r.stderr.decode('utf-8', 'replace')[:400]}")
    out = json.loads(r.stdout.decode("utf-8"))
    if isinstance(out, dict) and "error" in out:
        raise RuntimeError(out["error"])
    return {o["id"]: o for o in out}


def main():
    ap = argparse.ArgumentParser(
        description="HTML 表格 → Markdown pipe table（含自证 + 四口径 + 备份）")
    ap.add_argument("--dir", action="append", default=[],
                    help="作用域目录（可多次指定，相对 vault 根）")
    ap.add_argument("--whole-vault", action="store_true", help="全库扫描（排排除项）")
    ap.add_argument("--apply", action="store_true", help="实际写入（默认 dry-run）")
    ap.add_argument("--all-tables", action="store_true", help="含纯文字表（默认只转含公式）")
    ap.add_argument("--allow-entities", action="store_true", help="entity 解码后转")
    ap.add_argument("--qa-cards", action="store_true",
                    help="启用 D 通道：含「N分」得分标记的评分卡/问答卡 → "
                         "题干段 + 答案引用块（`> `），公式随段落恢复 inline 渲染。"
                         "主通道拒收后兜底尝试。")
    ap.add_argument("--allow-in-excluded", action="append", default=[],
                    metavar="PREFIX",
                    help="显式放行落在 EXCLUDE_PREFIX 内的路径前缀（可多次，"
                         "如 --allow-in-excluded 04-课件）。用户授权作用域专用。")
    ap.add_argument("--backup-dir", default=str(DEFAULT_BACKUP),
                    help="备份目录（默认 .workbuddy/tmp/html_table_backup）")
    args = ap.parse_args()

    if not args.dir and not args.whole_vault:
        ap.error("需指定 --dir 或 --whole-vault")
    if not SELFCHECK.exists():
        ap.error(f"自证器缺失: {SELFCHECK}")

    backup_dir = Path(args.backup_dir)
    math_only = not args.all_tables
    scope = "全库" if args.whole_vault else " ".join(args.dir)
    files = list(iter_files(args.dir, args.whole_vault,
                            allow=tuple(args.allow_in_excluded)))
    print(f"作用域: {scope}  文件 {len(files)}  "
          f"含纯文字表: {args.all_tables}  entity解码: {args.allow_entities}  "
          f"D通道(qa-cards): {args.qa_cards}  "
          f"{'写入' if args.apply else 'dry-run'}")
    if args.allow_in_excluded:
        print(f"  放行排除域: {', '.join(args.allow_in_excluded)}")

    candidates = []
    for p, rel in files:
        try:
            text, items, raw = plan_one(p, math_only=math_only,
                                        allow_entities=args.allow_entities,
                                        qa_cards=args.qa_cards)
        except Exception as e:
            print(f"  ⚠️ 读取失败 {rel}: {e}", file=sys.stderr)
            continue
        ok = [it for it in items if it["reason"] is None]
        if ok:
            candidates.append((p, rel, text, ok, raw))
    print(f"候选文件: {len(candidates)}")

    sc_items = []
    for fi, (_, _, _, ok, _) in enumerate(candidates):
        for ti, it in enumerate(ok):
            sc_items.append((f"{fi}:{ti}", it["converted"]))
    sc = selfcheck(sc_items) if sc_items else {}
    ok_ids = {k for k, v in sc.items() if v["ok"]}
    print(f"渲染自证: {len(ok_ids)}/{len(sc_items)} 通过")
    fails = [(k, v) for k, v in sc.items() if not v["ok"]]
    if fails:
        print(f"  未通过（前 5）: {fails[:5]}")

    backup_dir.mkdir(parents=True, exist_ok=True)
    applied_files = applied_tables = skipped = 0
    report = []

    for fi, (p, rel, text, ok_items, raw) in enumerate(candidates):
        good = [it for ti, it in enumerate(ok_items) if f"{fi}:{ti}" in ok_ids]
        skipped += len(ok_items) - len(good)
        if not good:
            continue

        eol = "\r\n" if b"\r\n" in raw else "\n"
        new_text = text
        for it in sorted(good, key=lambda x: -x["start"]):
            conv = it["converted"]
            if eol == "\r\n":
                conv = conv.replace("\n", "\r\n")
            new_text = new_text[:it["start"]] + conv + new_text[it["end"]:]

        v = {}
        v["本次表残留"] = sum(1 for it in good if it["original"] in new_text)
        orig_lines = text.count("\n")
        gen_lines = sum(it["converted"].count("\n") + 1 for it in good)
        old_lines = sum(it["original"].count("\n") + 1 for it in good)
        v["行数"] = (new_text.count("\n"), orig_lines - old_lines + gen_lines)
        # 「宽度一致」口径**只对 pipe 通道生效** —— 该口径假设产物是表格
        # （逐行 `|` 数一致）。D 通道产物是「题干段 + 引用块」混合文本，
        # `|` 数天然不等 → 原口径会**假失败**（2026-09-20 并入实证：
        # 反向验证时 2 表全部因 widths_ok=False 被跳过，处理文件 0）。
        # D 通道改用**内容守恒**：原表每个非空单元格文本须在产物中出现。
        widths_ok = True
        content_ok = True
        for it in good:
            if it.get("channel") == "qa":
                prod = it["converted"]
                flat = [c for g in _d_rows_of_rich(it["original"]) for c in g[2]]
                for c in flat:
                    c = c.strip()
                    if not c:
                        continue
                    if c.replace("|", "\\|") not in prod and c not in prod:
                        content_ok = False
                        break
                if not content_ok:
                    break
                continue
            ml = it["converted"].split("\n")
            data = [ln for i, ln in enumerate(ml) if i != 1 and ln.strip()]
            ws = {ln.replace("\\|", "").count("|") - 1 for ln in data}
            if len(ws) != 1:
                widths_ok = False
                break
        v["宽度一致"] = widths_ok
        v["内容守恒"] = content_ok
        nb = new_text.encode("utf-8")
        v["行尾保持"] = (nb.count(b"\r\n") == nb.count(b"\n")) if eol == "\r\n" \
            else (b"\r\n" not in nb)
        def _struct_ok(it):
            lines = it["converted"].split("\n")
            if it.get("channel") == "qa":
                return any(ln.strip() for ln in lines)
            # pipe：须有「表头 + 分隔行」之外的至少 1 条数据行
            return len([ln for i, ln in enumerate(lines)
                        if i != 1 and ln.strip()]) > 0

        v["行结构自洽"] = all(_struct_ok(it) for it in good)
        ok_v = (v["本次表残留"] == 0 and v["行数"][0] == v["行数"][1]
                and v["宽度一致"] and v["内容守恒"]
                and v["行尾保持"] and v["行结构自洽"])

        report.append({"path": rel, "tables": len(good), "verify": v, "ok": ok_v})
        if not args.apply:
            continue
        if not ok_v:
            print(f"  ⚠️ 验证未过，跳过: {rel}  {v}", file=sys.stderr)
            continue

        key = hashlib.md5(rel.encode("utf-8")).hexdigest()[:12]
        # ⚠️ 已存在则不覆盖：保护更早的「转换前」快照（多批次共用目录时关键）
        if not (backup_dir / f"{key}.md").exists():
            (backup_dir / f"{key}.md").write_bytes(raw)
            (backup_dir / f"{key}.path").write_text(rel, encoding="utf-8")
        p.write_bytes(new_text.encode("utf-8"))
        applied_files += 1
        applied_tables += len(good)

    print()
    print("=" * 72)
    print("RESULT" + ("（已写入）" if args.apply else "（dry-run，未写入）"))
    print("=" * 72)
    print(f"  处理文件: {applied_files if args.apply else len(report)}")
    print(f"  转换表数: {applied_tables if args.apply else sum(r['tables'] for r in report)}")
    print(f"  自证未过跳过: {skipped}")
    badv = [r for r in report if not r["ok"]]
    print(f"  {'⚠️ 四口径未过: ' + str(len(badv)) if badv else '✅ 四口径全部通过'}")
    for r in badv[:5]:
        print(f"     {r['path']}  {r['verify']}")
    print("\n前 5 个样例:")
    for r in report[:5]:
        print(f"  {r['tables']:3d} 表  {r['path']}")

    TMP.mkdir(parents=True, exist_ok=True)
    out = TMP / "html_tables_to_markdown_report.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(f"\n报告: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
