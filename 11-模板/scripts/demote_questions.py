# -*- coding: utf-8 -*-
"""习题书低质量题降级器。

输入：07-资料提炼/习题书-低质量候选.json（audit_book_quality.py 产出）。
默认只处置 action=降级 的条目（难度过低/篇幅过短）；--all 连同"补元数据"组一起降级（不建议）。
动作：源文件 frontmatter  `pack: 模块习题集` → `章节练习`，并追加 demoted 标记行；
      全部处置登记到 07-资料提炼/习题书剔除清单.json（可恢复依据）。
默认 dry-run，--write 实写。运行：系统 Python 3.12，vault 根目录。
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

VAULT = Path(__file__).resolve().parents[2]
CAND_JSON = VAULT / "07-资料提炼" / "习题书-低质量候选.json"
LOG_JSON = VAULT / "07-资料提炼" / "习题书剔除清单.json"

WRITE = "--write" in sys.argv
ALL_ACTIONS = "--all" in sys.argv
TODAY = __import__("build_module_book", fromlist=["TODAY"]).TODAY \
    if False else __import__("datetime").date.today().isoformat()


def edit_file(path, reason):
    p = VAULT / "04-题库" / path
    s = p.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^(---\n)(.*?)(\n---\n)", s, re.S)
    if not m:
        return None, "未找到 frontmatter"
    fm = m.group(2)
    if re.search(r"(?m)^pack: 章节练习", fm):
        return None, "已是章节练习"
    if not re.search(r"(?m)^pack: 模块习题集", fm):
        return None, "pack 非 模块习题集"
    new_fm = re.sub(r"(?m)^pack: 模块习题集\s*$", "pack: 章节练习", fm)
    if not re.search(r"(?m)^demoted:", new_fm):
        new_fm = new_fm.rstrip("\n") + f"\ndemoted: {TODAY} 习题书质量降级（{reason}）\n"
    new = s[:m.start(2)] + new_fm + s[m.end(2):]
    if WRITE:
        p.write_text(new, encoding="utf-8", newline="")
    return new, None


def main():
    data = json.loads(CAND_JSON.read_text(encoding="utf-8"))
    entries = [e for e in data["entries"]
               if ALL_ACTIONS or e.get("action") == "降级"]
    print(f"候选 {len(data['entries'])} 条，本次处置 {len(entries)} 条"
          f"（{'--all 全部' if ALL_ACTIONS else '仅 action=降级'}，"
          f"{'实写' if WRITE else 'dry-run，加 --write 落盘'}）")

    log_entries, skipped = [], []
    n_files = 0
    for e in entries:
        reason = "+".join(e["reasons"])
        for path in e["paths"]:
            new, err = edit_file(path, reason)
            if err:
                skipped.append({"path": path, "err": err})
                print(f"  ⚠️ 跳过 {path}: {err}")
                continue
            n_files += 1
            if WRITE:
                print(f"  ✅ {path}")
            else:
                print(f"  (dry) {path}")
        log_entries.append({
            "paths": e["paths"], "module": e["module"],
            "title": e.get("title", ""), "reasons": e["reasons"],
            "action": e.get("action", "降级"), "date": TODAY,
        })

    print(f"\n共 {n_files} 个源文件{'已' if WRITE else '将'}降级；跳过 {len(skipped)}")
    if WRITE:
        old = []
        if LOG_JSON.exists():
            try:
                old = json.loads(LOG_JSON.read_text(encoding="utf-8")).get("entries", [])
            except Exception:
                old = []
        LOG_JSON.write_text(json.dumps({
            "note": "习题书剔除/降级登记簿（可恢复依据；源文件 pack 已改回章节练习，"
                    "恢复=改回 pack: 模块习题集 并删除 demoted 行）。",
            "entries": old + log_entries,
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"登记簿已更新: {LOG_JSON}")


if __name__ == "__main__":
    main()
