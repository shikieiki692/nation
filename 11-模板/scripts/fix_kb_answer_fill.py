# -*- coding: utf-8 -*-
"""补答案执行：备份 → 追加答案/占位标注 → 更新 frontmatter。
来源：缓存-补答案-{ZOC,XES,赵鑫光}.json + Weller 真缺清单。"""
import json, re, sys
from pathlib import Path

VAULT = Path(r"C:/Obsidion/妙妙屋")
BACKUP = VAULT / "09-审计报告" / "备份" / "答案补充-2026-08-31"

def split_fm(text: str):
    if text.startswith("\ufeff"):
        text = text[1:]
    if text.startswith("---\n"):
        m = re.search(r"^---\n(.*?)\n---\n", text, re.S)
        if m:
            return m.group(1), text[m.end():]
    return "", text

def update_fm(text: str, status: str | None, updated: str = "2026-08-31"):
    fm, body = split_fm(text)
    if not fm:
        return text
    if status:
        fm = re.sub(r"(?m)^status:.*$", f"status: {status}", fm)
        if "status:" not in fm:
            fm += f"\nstatus: {status}"
    fm = re.sub(r"(?m)^updated:.*$", f"updated: {updated}", fm)
    if "updated:" not in fm:
        fm += f"\nupdated: {updated}"
    return f"---\n{fm}\n---\n{body}"

# ── 收集计划 ─────────────────────────────────────────────
plan: dict[str, tuple[str, str]] = {}   # rel -> (kind, content)

for tag in ["ZOC", "XES", "赵鑫光"]:
    src = json.load(open(VAULT / "09-审计报告" / f"缓存-补答案-{tag}.json", encoding="utf-8"))
    for x in src:
        rel = x["rel"]
        if x.get("found"):
            plan[rel] = ("answer", x["answer_md"])
        else:
            note = (x.get("note") or "").strip().replace("\n", " ")[:70]
            plan[rel] = ("mark", f"> **答案**：未找到对应解答（源文件无答案区/无对应解答；{note}）。\n\n")

# Weller 56：OCR 无答案区 → 占位标注
d = json.load(open(VAULT / "09-审计报告" / "缓存-剩余问题诊断.json", encoding="utf-8"))
no_answer = [x["rel"] for x in d["答案缺口清单"]["no_answer"]]
for rel in no_answer:
    if rel.startswith("04-题库/教材习题/无机化学第6版Weller"):
        plan[rel] = ("mark",
            "> **答案**：原书未提供解答（《无机化学》第6版练习题，OCR 源 `06-外部资料导入/无机化学Weller/无机化学第6版Welle19-21章.md` 不含答案区，2026-08-31 核查）。\n\n")

# ── 执行 ─────────────────────────────────────────────────
manifest = []
for rel, (kind, content) in sorted(plan.items()):
    p = VAULT / rel
    if not p.exists():
        print(f"  ⚠ 缺失: {rel}")
        continue
    raw = p.read_bytes()
    bak = BACKUP / rel
    bak.parent.mkdir(parents=True, exist_ok=True)
    bak.write_bytes(raw)

    text = raw.decode("utf-8")
    new_text = text.rstrip("\n") + "\n\n" + content.lstrip("\n") + "\n"
    if kind == "answer":
        new_text = update_fm(new_text, "已补全答案")
    else:
        new_text = update_fm(new_text, None)
    p.write_text(new_text, encoding="utf-8")
    manifest.append({"rel": rel, "kind": kind, "bak": str(bak)})

json.dump(manifest, open(VAULT / "09-审计报告" / "缓存-答案补充-manifest.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
from collections import Counter
print("完成。", dict(Counter(m["kind"] for m in manifest)), "共", len(manifest))
print("备份目录:", BACKUP)
