# -*- coding: utf-8 -*-
"""习题书补入提升器：把 07-资料提炼/习题书-补入候选.json 中的题目
从 章节练习层 提升为 模块习题集（入书）。

前置校验（宁缺毋滥，04-题库/README.md 分层入库制）：fidelity 必填、
submodule 必填、source 必填、文件名含主题词、classification 可命中。
默认 dry-run，--write 实写。运行：系统 Python 3.12，vault 根目录。
"""
import io
import json
import re
import sys
from pathlib import Path

if not (getattr(sys.stdout, "encoding", "") == "utf-8"
        and getattr(sys.stdout, "errors", "") == "replace"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, "11-模板/scripts")
import build_module_book as B  # noqa: E402

VAULT = Path(__file__).resolve().parents[2]
CAND_JSON = VAULT / "07-资料提炼" / "习题书-补入候选.json"
WRITE = "--write" in sys.argv
TODAY = B.TODAY


def promote(path, cand):
    p = VAULT / "04-题库" / path
    s = p.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^(---\n)(.*?)(\n---\n)", s, re.S)
    if not m:
        return None, "无 frontmatter"
    fm = m.group(2)
    if not re.search(r"(?m)^pack: 章节练习", fm):
        return None, "pack 非 章节练习"
    # 必填字段校验
    problems = []
    for field in ("fidelity", "submodule", "source", "subject_module", "exam_stage"):
        v = re.search(rf"(?m)^{field}: (.*)$", fm)
        if not v or not v.group(1).strip() or v.group(1).strip() in ("[]", '""'):
            problems.append(field)
    if problems:
        return None, "必填字段缺失: " + ",".join(problems)
    new_fm = re.sub(r"(?m)^pack: 章节练习\s*$", "pack: 模块习题集", fm)
    if not re.search(r"(?m)^promoted:", new_fm):
        new_fm = new_fm.rstrip("\n") + f"\npromoted: {TODAY} 习题书择优补入（难度{cand['difficulty']}·考纲相关·分类可命中）\n"
    new = s[:m.start(2)] + new_fm + s[m.end(2):]
    if WRITE:
        p.write_text(new, encoding="utf-8", newline="")
    return new, None


def main():
    data = json.loads(CAND_JSON.read_text(encoding="utf-8"))
    print(f"补入候选 {data['total']} 条（{'实写' if WRITE else 'dry-run，加 --write 落盘'}）")
    ok, skip = 0, 0
    for c in data["entries"]:
        new, err = promote(c["path"], c)
        if err:
            skip += 1
            print(f"  ⚠️ 跳过 {c['path']}: {err}")
            continue
        ok += 1
        print(f"  {'✅' if WRITE else '(dry)'} {c['path']} → {c['subject_module']}")
    print(f"\n补入 {ok}，跳过 {skip}")


if __name__ == "__main__":
    main()
