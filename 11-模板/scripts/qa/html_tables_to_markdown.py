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

## 支持形态

| 形态 | 处理 |
|:---|:---|
| 普通表 | 直转 |
| **colspan** | 左对齐展开（内容放首列、后 N-1 列留空） |
| **rowspan** | 下拉填充（内容在接下来 n 行逐行重复）—— 730 张中 727 张可保真 |
| **HTML 实体** `&gt;`/`&lt;` 等 | `html.unescape` 后转（`--allow-entities`） |
| 纯文字表（无公式） | 照转（`--all-tables`）—— Word 侧有收益 |

## 保守拒收判据（宁可不转，不可转坏）

含 `<img` / 列数 0 或 >8 / **列数 = 1（单列 = 段落伪装）** /
**窄表（≤2 列）单元格平均文本 >40 字** / **单格 >800 字** /
单元格 `$` 数为奇数（OCR 半包）/（entity 开启时）解码后仍含 `<img` 或真标签。

> 2026-09-20 规则修正：原「列数 ≤2 拒收」误杀真 2 列数据表（如「温度/K | δ/ppm」）；
> 原「平均 >40 字拒收」误杀宽表内的长文本单元格。现改为①只拒单列 ②长度阈值只对
> 窄表生效，另设单格 800 字硬上限。修正后 04-课件/习题集 多转 15 表、04-题库 多转 17 表。

## 用法（受管解释器 + 安全前缀）

    PY="C:/Users/蕾赛/.workbuddy/binaries/python/versions/3.13.12/python.exe"

    # 默认 dry-run（只报告，不写盘）
    $PY -X utf8 11-模板/scripts/qa/html_tables_to_markdown.py --dir "06-外部资料导入"

    # 实际写入（自动备份 + 渲染自证 + 四口径验证）
    $PY -X utf8 11-模板/scripts/qa/html_tables_to_markdown.py --dir X --apply

    # 全量口径（含纯文字表 + entity 解码）
    $PY -X utf8 11-模板/scripts/qa/html_tables_to_markdown.py --dir X --all-tables --allow-entities --apply

    # 全库扫描（排红线/活跃线）
    $PY -X utf8 11-模板/scripts/qa/html_tables_to_markdown.py --whole-vault

## 验收防线（--apply 自动执行）

① 渲染自证（markdown-it + KaTeX，残留 `$`==0）② 四口径（本次表残留 0 /
行数守恒 / 宽度一致 / 行尾保持 / 行结构自洽）③ 备份（已存在则不覆盖）。

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


def convert_table(block: str, allow_entities: bool = False):
    """单表转换。返回 (markdown, reason)；reason 为 None 时成功。"""
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
    if width == 0 or width > 8:
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


def plan_one(p: Path, math_only=True, allow_entities=False):
    raw = p.read_bytes()
    text = raw.decode("utf-8")
    items = []
    for m in TABLE_BLOCK.finditer(text):
        block = m.group(0)
        if math_only and not MATH_SPAN.search(block):
            continue
        md, reason = convert_table(block, allow_entities=allow_entities)
        items.append({"start": m.start(), "end": m.end(),
                      "original": block, "converted": md, "reason": reason})
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
          f"{'写入' if args.apply else 'dry-run'}")
    if args.allow_in_excluded:
        print(f"  放行排除域: {', '.join(args.allow_in_excluded)}")

    candidates = []
    for p, rel in files:
        try:
            text, items, raw = plan_one(p, math_only=math_only,
                                        allow_entities=args.allow_entities)
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
        widths_ok = True
        for it in good:
            ml = it["converted"].split("\n")
            data = [ln for i, ln in enumerate(ml) if i != 1 and ln.strip()]
            ws = {ln.replace("\\|", "").count("|") - 1 for ln in data}
            if len(ws) != 1:
                widths_ok = False
                break
        v["宽度一致"] = widths_ok
        nb = new_text.encode("utf-8")
        v["行尾保持"] = (nb.count(b"\r\n") == nb.count(b"\n")) if eol == "\r\n" \
            else (b"\r\n" not in nb)
        v["行结构自洽"] = all(
            len([ln for i, ln in enumerate(it["converted"].split("\n"))
                 if i != 1 and ln.strip()]) > 0 for it in good)
        ok_v = (v["本次表残留"] == 0 and v["行数"][0] == v["行数"][1]
                and v["宽度一致"] and v["行尾保持"] and v["行结构自洽"])

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
