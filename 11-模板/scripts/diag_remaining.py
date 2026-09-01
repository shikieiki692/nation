# -*- coding: utf-8 -*-
"""诊断剩余问题（2026-08-31 收尾）：答案缺口清单 + 命名不合规 + 题目实测计数。
只读，不写盘。复用 audit_question_bank 的检测逻辑。"""
import sys, re, json
from pathlib import Path
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).parent))
import audit_question_bank as A

VAULT = A.VAULT
OUT = VAULT / "09-审计报告" / "缓存-剩余问题诊断.json"

files = []
for d in A.TARGET_DIRS:
    root = VAULT / d
    for f in sorted(root.rglob("*.md")):
        if set(f.relative_to(VAULT).parts) & A.SKIP_DIR_PARTS:
            continue
        files.append(f)

md_idx = A.build_md_index()
label_idx = A.build_label_index()
img_idx = A.build_image_index()

gaps = {"no_answer": [], "placeholder": [], "short": [], "no_body": [], "ext_bad": []}
name_bad = []
type_count = defaultdict(int)
dir_total = defaultdict(int)   # 04-题库/05-真题库 × type=题目

for f in files:
    rel = f.relative_to(VAULT).as_posix()
    d = A.norm_dir(rel)
    text = f.read_text(encoding="utf-8", errors="replace")
    fm, body = A.strip_fm(text)
    ftype = str(fm.get("type", "")).strip()
    if ftype in A.QUESTION_TYPES:
        type_count[ftype] += 1
        if ftype != "题组":
            dir_total[rel.split("/")[0]] += 1

    # G. 命名（所有文件，不论 type）
    for prefix, pat in A.NAME_RULES.items():
        if rel.startswith("04-题库/" + prefix):
            if not re.match(pat, f.stem):
                name_bad.append({"rel": rel, "prefix": prefix, "stem": f.stem})
            break

    # D. 答案缺口（只对单题类；题目集为存档/集合，不强制单题答案块）
    if ftype not in A.QUESTION_TYPES or ftype in ("题组", "题目集"):
        continue
    plain = re.sub(r"!\[\[[^\]]+\]\]", "", body)
    plain = re.sub(r"\s+", "", plain)
    if len(plain) < 50:
        gaps["no_body"].append({"rel": rel, "len": len(plain)})
    m = A.ANSWER_OPEN_RE.search(body)
    ext_m = A.EXT_ANSWER_RE.search(body)
    if ext_m and m is None:
        pass  # 外链答案，合法
    elif m:
        ans = body[m.end():]
        ans = re.sub(r"<summary>.*?</summary>", "", ans, flags=re.S)
        ans = re.sub(r"</?details>", "", ans)
        ans = re.sub(r"\s+", "", ans)
        if A.placeholder_re.search(ans[:60]) or len(ans) < 5:
            gaps["placeholder"].append({"rel": rel, "flag": ans[:30]})
        elif len(ans) < 30:
            if not (A.short_answer_ok_re.search(ans) or "```" in ans):
                gaps["short"].append({"rel": rel, "ans": ans[:30]})
    elif re.search(r"答案见|答案详见|见答案|答案位于|解答见", body):
        m2 = re.search(r"\[\[([^\]|#]+)", body[body.find("答案见") if "答案见" in body else 0:])
        if not (m2 and A.resolve_link(m2.group(1), f, md_idx, label_idx)):
            gaps["ext_bad"].append({"rel": rel, "tgt": m2.group(1) if m2 else ""})
    else:
        if A.EMBEDDED_ANSWER_RE.search(body) and len(plain) > 200:
            pass  # 内嵌解答合法
        else:
            gaps["no_answer"].append({"rel": rel})

# 命名按目录统计
name_by_dir = defaultdict(list)
for x in name_bad:
    name_by_dir[x["prefix"]].append(x)

result = {
    "题目计数": dict(type_count),
    "dir_total": dict(dir_total),
    "答案缺口": {k: len(v) for k, v in gaps.items()},
    "答案缺口清单": gaps,
    "命名不合规": {k: len(v) for k, v in name_by_dir.items()},
    "命名清单": {k: v for k, v in name_by_dir.items()},
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
print("题目计数:", dict(type_count))
print("dir_total:", dict(dir_total))
print("答案缺口:", {k: len(v) for k, v in gaps.items()})
print("命名不合规:", {k: len(v) for k, v in name_by_dir.items()})
print("→", OUT)
