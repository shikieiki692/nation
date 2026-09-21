#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""记忆系统体检（可复用）。两件事，均为**只读**：

  --pointers  核查 `MEMORY.md` 里的路径指针是否有效
              （区分「路径式」须精确存在 / 「文件名式」全库同名即算有效）
  --logs      报告日志老化：>30 天的日志（规则要求「并入速查后删」）、体积、小节标题
  --all       两者都跑（默认）

用法（相对 vault 根）：
  CODEBUDDY_SESSION_ID= CLAUDE_SESSION_ID= python -X utf8 .workbuddy/scripts/audit_memory.py --all

⚠️ 判据说明：
- 「文件名式」引用（如 `render_gate.py`）**不判失效** —— 它对人是可检索的；
  首版把它们算失效 ⇒ 34 个假阴性，是本工具存在的原因之一。
- 占位符（`YYYY-MM-DD.md`、`<日期>-validation.md`）、git 语法（`origin/master..HEAD`）、
  字段名（`deprecated / deprecatedDate`）、LaTeX（`\\theta/\\nu`）一律**跳过**。
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]          # .workbuddy/scripts/x.py → vault
MEM = VAULT / ".workbuddy/memory"
MEMORY_MD = MEM / "MEMORY.md"
# ⚠️ 千万别把整个 `.workbuddy` 跳过：MEMORY 里大量合法引用就在 `.workbuddy/scripts/`
#    （首版这么跳过 ⇒ 把 `test_postprocess_preserves_content.py` 误报为失效）。
#    只跳 `.workbuddy/tmp`（体积大且会被清理，指向它的引用本就不稳）。
SKIP_DIRS = {".git", "node_modules", ".obsidian", "_归档", ".workbuddy/tmp"}
PLACEHOLDER = re.compile(r"YYYY|MM-DD|<[^>]*>|\.\.\.|…|^\.py$|^http|^C:|^~$|^deprecated")
# 已在文中明确标注「已过期/不存在」的路径，不计为缺陷（人工确认过，见工单/速查）
KNOWN_OBSOLETE = {"04-题库/教材习题/物理化学Atkins/", "教材习题/物理化学Atkins/"}
# 指向 `.workbuddy/tmp` 的工具脚本属「临时区」，单独归类提示（不混入真失效）
TMP_HINT = re.compile(r"^(qb_full_measure|final_verify|math_probe|show_failures|apply_sanitize)\.py$")


def _basename_index():
    idx = {}
    for p in VAULT.rglob("*"):
        if p.is_dir() or any(s in p.parts for s in SKIP_DIRS):
            continue
        idx.setdefault(p.name, []).append(p)
    return idx


def check_pointers():
    if not MEMORY_MD.is_file():
        print("!! 找不到 %s" % MEMORY_MD)
        return 2
    t = MEMORY_MD.read_text(encoding="utf-8")
    idx = _basename_index()
    bypath_ok, byname_ok, bad = [], [], []
    for s in dict.fromkeys(x.strip() for x in re.findall(r"`([^`\n]+)`", t)):
        if not ("/" in s or s.endswith((".md", ".py", ".json", ".txt", ".jsonl", ".docx", ".csv"))):
            continue
        if any(c in s for c in ("--", "git ", "$", "CODEBUDDY", "NODE_PATH")) or "*" in s:
            continue
        if PLACEHOLDER.search(s) or s.startswith(("…", "~")):
            continue
        # 跳过「非路径」写法：LaTeX（含反斜杠）、散文并列（` / ` 或 空格+CJK）、git ref/range
        if ("\\" in s or " / " in s or ".." in s or s.startswith("refs/") or s.startswith("origin/")
                or ((" " in s) and re.search(r"[\u4e00-\u9fff]", s))):
            continue
        if "/" in s:
            cands = [VAULT / s, MEM / s, VAULT / "11-模板/scripts" / s, VAULT / ".workbuddy/scripts" / s]
            (bypath_ok if any(c.exists() for c in cands) else bad).append(s)
        else:
            (byname_ok if (s.rstrip("/") in idx or (MEM / s).exists()) else bad).append(s)
    print("=== 指针核查 ===")
    print("路径式有效 %d ｜ 文件名式（不判失效）%d ｜ **失效 %d**" % (len(bypath_ok), len(byname_ok), len(bad)))
    for b in bad:
        # 近失提示：同 basename 是否在别处存在（帮人一眼定位真路径）
        base = b.rstrip("/").split("/")[-1]
        alt = [str(p.relative_to(VAULT)).replace("\\", "/") for p in idx.get(base, [])][:3]
        hint = ("  → 实际在 " + "、".join(alt)) if alt else ""
        print("   ❌ %s%s" % (b, hint))
    stale_tmp = [b for b in bad if TMP_HINT.search(b.rstrip("/").split("/")[-1])]
    if stale_tmp:
        print("   ℹ️ 其中 %d 个指向 `.workbuddy/tmp/`（临时区，随时会被清理）→ 建议改为固定落点或删引用：%s"
              % (len(stale_tmp), "、".join(stale_tmp)))
    # 版本号
    m = re.match(r"# .*?（(\d{4}-\d{2}-\d{2}) (v\d+)）", t.splitlines()[0] if t.splitlines() else "")
    if m:
        print("   版本：%s %s ｜ %d B" % (m.group(1), m.group(2), MEMORY_MD.stat().st_size))
    real = [b for b in bad if b.rstrip("/") not in KNOWN_OBSOLETE and not TMP_HINT.search(b.rstrip("/").split("/")[-1])]
    return 1 if real else 0


def check_logs(days=30, today=None):
    today = today or datetime.date.today()
    print("\n=== 日志老化（阈值 %d 天）===" % days)
    print("%-16s %8s %6s %s" % ("日志", "体积", "龄期", "状态"))
    due, total = [], 0
    for p in sorted(MEM.glob("2026-*.md")):
        try:
            d = datetime.date.fromisoformat(p.stem)
        except ValueError:
            continue
        age = (today - d).days
        total += p.stat().st_size
        flag = "⏰ 待并入速查后删" if age > days else ("⚠️ 临近（≤7 天）" if age > days - 7 else "")
        if age > days:
            due.append(p)
        print("%-16s %7.0fK %5d天 %s" % (p.name, p.stat().st_size / 1024, age, flag))
    print("合计 %.1f MB ｜ 待处理 %d 份" % (total / 1048576, len(due)))
    for p in due:
        secs = [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.startswith("## ")]
        print("\n── %s（%d 个小节，前 12）：" % (p.name, len(secs)))
        for s in secs[:12]:
            print("     %s" % s[:88])
    # 速查文件规模
    for f in ("工程细则速查.md", "工程细则速查-历史存档.md", "题库选题口径速查.md"):
        q = MEM / f
        if q.is_file():
            print("\n  %-34s %7.0f KB / %d 行" % (f, q.stat().st_size / 1024, len(q.read_text(encoding="utf-8").splitlines())))
    return 1 if due else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pointers", action="store_true")
    ap.add_argument("--logs", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    do_all = a.all or not (a.pointers or a.logs)
    rc = 0
    if a.pointers or do_all:
        rc |= check_pointers()
    if a.logs or do_all:
        rc |= check_logs()
    sys.exit(0)          # 只报告，不因发现而失败（供自动化使用）
