#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""audit_deprecated.py —— 废弃机制（`deprecated` + `sunsetDate`）过期项核查。

## 为什么有这个工具
仓库的废弃约定写在 **frontmatter** 里，不是靠人记：
    deprecated: true
    deprecatedDate: 2026-08-08
    sunsetDate: 2026-08-15          # 到期日：此后该文件应已消失
    supersededBy: <替代文件的仓库相对路径>

但「到期了没有 / 到期了能不能删」需要**逐条核四件事**，人工做易漏。
本工具把这件事**变成可重复执行的核对**（2026-09-21 从一次性脚本沉淀而来）。

## 逐条核什么（每项都可证伪）
1. **是否已在归档目录内**（`_归档/`、`归档/`、`归档首页/`、`历史任务卡/`）
   → 已在归档 = 此前用「移入归档」处理过，**无需再动**。
2. **`supersededBy` 目标是否真实存在**
   → 不存在 ⇒ 删了会真的丢内容（**必须先人工确认**）。
3. **有多少「真 wikilink」**（`[[<名字>` 的字面形式）
   → ⚠️ **「短链名出现」≠「是链接」**：实测某份在 24 个活文档里「出现」，
     带 `[[ ]]` 的只有 6 个。统计必须用**带方括号**的形式。
   → 用 `git grep -z` 取原始字节，**避免中文路径被八进制转义**（否则过滤失效、数字虚高）。
4. **替代文件是否已有可承接旧名的 `aliases`**
   → 有则删后链接仍可解析；无则**必须先补 alias 再删**。

## 用法
    python -X utf8 11-模板/scripts/audit_deprecated.py
    python -X utf8 11-模板/scripts/audit_deprecated.py --today 2026-09-01   # 复现历史口径
    python -X utf8 11-模板/scripts/audit_deprecated.py --quiet              # 只出汇总

**只报告，不删任何文件。** 删除是破坏性动作，须人工授权后逐条执行
（用 `os.remove` 逐文件删，**不要** `git rm -r` / `Remove-Item -Recurse`）。
"""
import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]

ARCH_HINT = ("_归档/", "归档/", "归档首页/", "历史任务卡/")
NOISE = ("00-首页/工作日志/", "09-审计报告/", ".workbuddy/",
         "00-首页/归档/", "09-审计报告/归档首页/", "09-审计报告/历史任务卡/")

RE_SUNSET = re.compile(r"^sunsetDate\s*:\s*(\d{4}-\d{2}-\d{2})", re.M)
RE_DEPRECATED = re.compile(r"^deprecated\s*:\s*true\s*$", re.M)
RE_SUPERSEDED = re.compile(r"^supersededBy\s*:\s*(.+)$", re.M)
RE_ALIASES = re.compile(r"^aliases\s*:\s*(.+)$", re.M)


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else ""


def tracked_md():
    out = subprocess.run(["git", "ls-files", "-z", "*.md"],
                         capture_output=True, cwd=VAULT).stdout
    return [p.decode("utf-8") for p in out.split(b"\x00") if p]


def count_real_links(name: str):
    """返回引用了 `[[<name>`（带方括号）的活文档（原始字节解析 + 去噪）。"""
    r = subprocess.run(["git", "grep", "-l", "-z", "-F", "[[" + name, "--", "*.md"],
                       capture_output=True, cwd=VAULT)
    hits = [p.decode("utf-8") for p in r.stdout.split(b"\x00") if p]
    return [h for h in hits if not any(n in h for n in NOISE)]


def resolve_target(src_rel: str, value: str):
    """把 supersededBy 的值解析成实际路径（支持含/不含目录两种写法）。"""
    v = value.strip().strip('"').strip("'")
    if not v:
        return None
    if v.endswith("/"):
        return VAULT / v
    cand = VAULT / v if "/" in v else (VAULT / src_rel).parent / v
    if cand.exists():
        return cand
    if not cand.suffix:
        for ext in (".md", ".docx"):
            if cand.with_suffix(ext).exists():
                return cand.with_suffix(ext)
    return None


def has_alias(target: Path, name: str) -> bool:
    if target is None or not target.is_file():
        return False
    m = RE_ALIASES.search(frontmatter(target.read_text(encoding="utf-8", errors="replace")))
    return bool(m) and name in m.group(1)


def main() -> int:
    ap = argparse.ArgumentParser(description="废弃机制过期项核查（只报告）")
    ap.add_argument("--today", default=None, help="以指定日期为「今天」（YYYY-MM-DD）")
    ap.add_argument("-q", "--quiet", action="store_true", help="只出汇总")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()

    rows = []
    for rel in tracked_md():
        p = VAULT / rel
        try:
            fm = frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        if not fm or not RE_DEPRECATED.search(fm):
            continue
        m = RE_SUNSET.search(fm)
        if not m:
            continue
        try:
            sunset = dt.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if sunset >= today:
            continue
        sup = RE_SUPERSEDED.search(fm)
        rows.append({"rel": rel, "sunset": sunset.isoformat(),
                     "sup": sup.group(1).strip() if sup else "",
                     "archived": any(h in rel for h in ARCH_HINT),
                     "size": p.stat().st_size})

    todo = []
    for r in rows:
        if r["archived"]:
            r["verdict"] = "已归档（已处理）"
        else:
            tgt = resolve_target(r["rel"], r["sup"]) if r["sup"] else None
            name = Path(r["rel"]).stem
            links = count_real_links(name)
            if r["sup"] and tgt is None:
                r["verdict"] = "❓替代文件不存在 —— 须人工确认"
            elif links and not has_alias(tgt, name):
                r["verdict"] = "⚠️ 有 %d 个真链接且替代页无 alias —— 先补 alias 再删" % len(links)
            else:
                r["verdict"] = "✅ 可删（真链接 %d）" % len(links)
        if not r["archived"]:
            todo.append(r)

    print("=== 已过 sunsetDate（今天 %s）：%d 份 ===" % (today, len(rows)))
    print("   其中 已在归档目录内 %d 份（无需再动）；**待处置 %d 份**"
          % (len(rows) - len(todo), len(todo)))
    if not args.quiet:
        for r in sorted(todo, key=lambda x: x["sunset"]):
            print("\n  [%s] %s   (%.1f KB)" % (r["sunset"], r["rel"], r["size"] / 1024))
            print("      supersededBy: %s" % (r["sup"] or "—（无该字段）"))
            print("      %s" % r["verdict"])
        done = [r for r in rows if r["archived"]]
        if done:
            print("\n  --- 已在归档目录内（%d 份，仅列名）---" % len(done))
            for r in sorted(done, key=lambda x: x["sunset"]):
                print("    [%s] %s" % (r["sunset"], r["rel"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
