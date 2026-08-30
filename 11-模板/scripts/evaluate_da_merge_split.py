"""按“大题内部小问相似度”评估 合并/拆分/待定，给出建议与计划。

用法:
    python -X utf8 11-模板/scripts/evaluate_da_merge_split.py
"""

from __future__ import annotations

import re
from collections import Counter, OrderedDict
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC = VAULT_ROOT / "04-题库"
OUT = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-大题合分评估.md"
KEYS = VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-大题合并候选.txt"


def collect() -> OrderedDict[str, list[dict]]:
    groups: OrderedDict[str, list[dict]] = OrderedDict()
    for path in sorted(SRC.rglob("*.md")):
        m = re.match(r"^题-(\d+[A-Za-z]*?)-(\d+)-", path.name)
        if not m:
            continue
        key = f"题-{m.group(1)}-{m.group(2)}"
        text = path.read_text(encoding="utf-8")
        sm = (re.search(r"(?m)^subject_module:\s*(\S+)", text) or [None, ""])[1].strip('"')
        sub = (re.search(r"(?m)^submodule:\s*(\S+)", text) or [None, ""])[1].strip('"')
        mo = (re.search(r'(?m)^module:\s*"?([^"\n]+)"?', text) or [None, ""])[1].strip('"')
        imgs = set(re.findall(r"!\[\[([^\]|]+)", text))
        groups.setdefault(key, []).append(
            {"path": path, "sm": sm, "sub": sub, "mo": mo, "imgs": imgs}
        )
    return groups


def recommend(recs: list[dict]) -> tuple[str, str]:
    n = len(recs)
    u_sm = len({r["sm"] for r in recs})
    u_sub = len({r["sub"] for r in recs})
    u_mo = len({r["mo"] for r in recs})
    shared = len(set.intersection(*(r["imgs"] for r in recs)))
    sm_note = "；subject_module 不一致，需先统一标签" if u_sm > 1 else ""
    if u_sub == 1:
        return "合并", "小问主题一致（submodule 单一）" + sm_note
    if u_sub <= 2 and shared >= 1:
        return "合并", "主题相近且共享同一图" + sm_note
    if u_sub <= 2:
        return "合并", "主题相近" + sm_note
    return "拆分", f"主题差异较大（{u_sub} 个 submodule），宜拆分组卷" + sm_note


def main() -> int:
    groups = collect()
    rows = []
    for key, recs in groups.items():
        if len(recs) < 2:
            continue
        n = len(recs)
        u_sm = len({r["sm"] for r in recs})
        u_sub = len({r["sub"] for r in recs})
        u_mo = len({r["mo"] for r in recs})
        shared = len(set.intersection(*(r["imgs"] for r in recs)))
        rec, note = recommend(recs)
        rows.append(
            {
                "key": key,
                "n": n,
                "u_sub": u_sub,
                "u_mo": u_mo,
                "u_sm": u_sm,
                "shared": shared,
                "rec": rec,
                "note": note,
            }
        )

    c = Counter(r["rec"] for r in rows)
    merge_keys = [r["key"] for r in rows if r["rec"] == "合并"]
    merged_count = len(merge_keys) + sum(1 for r in rows if r["rec"] != "合并" for _ in range(r["n"] - 0))
    # 预计合并后题数 = 合并组数(每组1题) + 非合并组的小问数 + 非大题题
    total_before = sum(r["n"] for r in rows)
    merged_after = c["合并"] + sum(r["n"] for r in rows if r["rec"] != "合并")

    L = [
        "---",
        "title: 2026-08-30-习题书V2-大题合分评估",
        "type: 审计报告",
        "task_type: 习题册大题合分",
        "status: 建议",
        "created: 2026-08-30",
        "updated: 2026-08-30",
        "---",
        "",
        "# 习题书 V2 大题合分评估",
        "",
        f"> 共 {len(rows)} 个大题组（≥2 小题）。按“小问主题相似度 / 是否共享图 / 是否跨模块”给出 合并/拆分/待复核 建议。",
        "",
        "## 一、汇总",
        "",
        "| 建议 | 组数 | 涉及小问 |",
        "|---|---:|---:|",
    ]
    for rec in ["合并", "拆分", "待人工复核"]:
        L.append(f"| {rec} | {c.get(rec, 0)} | {sum(r['n'] for r in rows if r['rec']==rec)} |")
    L.append("")
    L.append(f"> 仅合并“合并”组，题数约 **{total_before} → {merged_after}**；其余保持拆分。")
    L.append("")
    L.append("## 二、逐组建议")
    L.append("")
    L.append("| 大题 | 小问 | submodule 数 | module 数 | 跨模块 | 共享图 | 建议 | 说明 |")
    L.append("|---|---:|---:|---:|---|---|---|---|")
    for r in sorted(rows, key=lambda x: (c[x["rec"]], -x["n"], x["key"])):
        L.append(
            f"| {r['key']} | {r['n']} | {r['u_sub']} | {r['u_mo']} | "
            f"{'是' if r['u_sm']>1 else '否'} | {r['shared']} | {r['rec']} | {r['note']} |"
        )
    L.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    KEYS.write_text(
        "\n".join(r["key"] for r in rows if r["rec"] == "合并") + "\n",
        encoding="utf-8",
    )
    print(f"groups={len(rows)} merge={c.get('合并',0)} split={c.get('拆分',0)} review={c.get('待人工复核',0)}")
    print(f"before={total_before} after={merged_after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
