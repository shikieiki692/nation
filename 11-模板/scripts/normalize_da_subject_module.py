"""把同一大题的多个小问 frontmatter 归一化，避免被拆进不同模块池。

默认只输出建议报告（dry-run）；加 `--apply-pilot` 只对 27 届第 3 题试点应用。

用法:
    python -X utf8 11-模板/scripts/normalize_da_subject_module.py [--apply-pilot]
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, OrderedDict
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "04-题库"
PILOT = "题-027-3"


def collect() -> OrderedDict[str, list[dict]]:
    groups: OrderedDict[str, list[dict]] = OrderedDict()
    for path in sorted(SRC.rglob("*.md")):
        name = path.name
        m = re.match(r"^题-(\d+[A-Za-z]*?)-(\d+)-", name)
        if not m:
            continue
        key = f"题-{m.group(1)}-{m.group(2)}"
        text = path.read_text(encoding="utf-8")
        sm = (re.search(r"(?m)^subject_module:\s*(\S+)", text) or [None, ""])[1]
        mo = (re.search(r'(?m)^module:\s*"?([^"\n]+)"?', text) or [None, ""])[1].strip()
        groups.setdefault(key, []).append(
            {"path": path, "sm": sm.strip('"'), "mo": mo.strip('"')}
        )
    return groups


def majority(recs: list[dict], field: str) -> str:
    c = Counter(r[field] for r in recs)
    return c.most_common(1)[0][0]


def rewrite(path: Path, sm: str, mo: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'(?m)^subject_module:\s*.*$', f"subject_module: {sm}", text)
    text = re.sub(r'(?m)^module:\s*.*$', f'module: "{mo}"', text)
    path.write_text(text, encoding="utf-8", newline="")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply-pilot", action="store_true")
    ap.add_argument("--apply-all", action="store_true")
    args = ap.parse_args()
    groups = collect()
    rows = []
    for key, recs in groups.items():
        if len(recs) < 2:
            continue
        sms = {r["sm"] for r in recs}
        mos = {r["mo"] for r in recs}
        if len(sms) == 1 and len(mos) == 1:
            continue
        prop_sm, prop_mo = majority(recs, "sm"), majority(recs, "mo")
        rows.append((key, len(recs), "/".join(sorted(sms)), "/".join(sorted(mos)), prop_sm, prop_mo))

    out = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-大题subject_module规范化建议.md"
    L = [
        "---",
        "title: 2026-08-30-习题书V2-大题subject_module规范化建议",
        "type: 审计报告",
        "task_type: 习题册大题合并",
        "status: dry-run",
        "created: 2026-08-30",
        "updated: 2026-08-30",
        "---",
        "",
        "# 大题 subject_module 规范化建议",
        "",
        f"> 共 {len(rows)} 个大题组存在跨小问的 `subject_module`/`module` 不一致，会导致合并时被拆进不同模块池。",
        "",
        "| 大题 | 小问数 | 现状 subject_module | 现状 module | 建议 subject_module | 建议 module |",
        "|---|---:|---|---|---|---|",
    ]
    for key, n, sms, mos, ps, pm in sorted(rows, key=lambda x: -x[1]):
        L.append(f"| {key} | {n} | {sms} | {mos} | {ps} | {pm} |")
    L.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"mixed_groups={len(rows)} report={out.name}")

    if args.apply_pilot:
        picked = [r for r in rows if r[0] == PILOT]
        if picked:
            key, _, _, _, ps, pm = picked[0]
            for rec in groups[key]:
                rewrite(rec["path"], ps, pm)
            print(f"applied pilot {key}: subject_module={ps} module={pm} ({len(groups[key])} files)")
    if args.apply_all:
        n_files = 0
        for key, _, _, _, ps, pm in rows:
            for rec in groups[key]:
                rewrite(rec["path"], ps, pm)
                n_files += 1
        print(f"applied all {len(rows)} groups, {n_files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
