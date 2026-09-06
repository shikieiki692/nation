import re
import pathlib

import sys

sys.path.insert(0, str(pathlib.Path(r"11-模板/scripts").resolve()))
import reconcile_module_books as rc

recon = pathlib.Path(r"09-审计报告/2026-08-30-习题书新旧对账.md")
text = recon.read_text(encoding="utf-8")

# Parse the old-only source list.
section = text.split("## 旧书有、新预览无（候选差异）")[1].split("## 新预览有、旧书无（新增方向）")[0]
old_only = []
for line in section.splitlines():
    if line.startswith("- `"):
        parts = line.split("`")
        rel = parts[1]
        pack = re.search(r"pack=([^\] ]+)", line)
        status = re.search(r"status=([^\] ]+)", line)
        old = re.search(r"· 旧书 (##\s+\S+)\s+in (.+)", line)
        old_only.append(
            {
                "rel": rel,
                "pack": pack.group(1) if pack else "",
                "status": status.group(1) if status else "",
                "header": old.group(1) if old else "",
                "old": old.group(2) if old else "",
            }
        )
print("old_only parsed", len(old_only))
print("deprecated", sum(1 for x in old_only if x["status"] == "deprecated"))
print("non-deprecated", sum(1 for x in old_only if x["status"] != "deprecated"))

preview_root = pathlib.Path(r".preview_build2/04-课件/习题集/习题书")
preview_files = list(preview_root.rglob("*.md"))
preview_blocks = rc.build_preview_blocks(preview_root)

for x in old_only:
    src_path = pathlib.Path(x["rel"])
    text = src_path.read_text(encoding="utf-8")
    qfp = rc.question_fingerprint(rc.split_source_question(text))
    fullfp = rc.body_fingerprint_loose(re.sub(r"^---[ \t]*\n.*?\n---[ \t]*\n?", "", text, flags=re.S, count=1))
    block_fp = {pb["fp"] for pb in preview_blocks}
    matching = []
    for pb in preview_blocks:
        if len(qfp) >= 20 and qfp in pb["fp"]:
            matching.append(("fp", pb["rel"]))
        elif len(qfp) >= 20 and qfp in pb["noimg"]:
            matching.append(("q-in-noimg", pb["rel"]))
        elif len(fullfp) >= 20 and fullfp in pb["noimg"]:
            matching.append(("full-in-noimg", pb["rel"]))
        elif len(qfp) >= 20:
            # Longest answer-bearing line from source present in this block.
            lines = [
                rc.norm(ln)
                for ln in re.split(r"\r?\n", re.sub(r"^---[ \t]*\n.*?\n---[ \t]*\n?", "", text, flags=re.S, count=1))
                if 40 <= len(rc.norm(ln)) <= 1000
            ]
            hit = sum(1 for ln in lines if ln in pb["noimg"])
            if hit >= 2:
                matching.append((f"lines={hit}", pb["rel"]))
    print(f"[{x['status']:12}] {pathlib.Path(x['rel']).name}")
    if matching:
        print("   covered by:", "; ".join(f"{k}@{v}" for k, v in matching[:4]))
    else:
        print("   NO CONTENT MATCH IN PREVIEW")
