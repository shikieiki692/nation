#!/usr/bin/env python3
"""Q-D residual rebuild: parse the official detail report, locate old book blocks,
and reverse-attribute "double-none" rows to 汇智 chapter-practice source files.

Temporary read-only analysis script. Output: _tmp_qd_residual_candidates.md
"""

import io
import re
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import reconcile_module_books as rc

ROOT = SCRIPT_DIR.parents[1]
REPORT = ROOT / "09-审计报告" / "2026-08-30-习题书Q-D对账明细.md"
OLD_ROOT = ROOT / "04-课件" / "习题集" / "习题书"
HUIZHI_ROOT = ROOT / "04-题库" / "教材习题" / "汇智竞赛题目"
OUT = ROOT / "_tmp_qd_residual_candidates.md"


def parse_report(text):
    rows = []
    cur = None
    for ln in text.splitlines():
        m = re.match(r"^- `([^`]+)` · `([^`]+)` · 〔(.+)〕$", ln)
        if m:
            if cur is not None:
                rows.append(cur)
            cur = {
                "path": m.group(1),
                "header": m.group(2),
                "bucket": m.group(3),
                "note": "",
                "flags": [],
                "preview": [],
                "source": [],
                "snippet": "",
            }
        elif cur is not None and ln.startswith("  - "):
            body = ln[4:]
            if body.startswith("来源标注："):
                cur["note"] = body[len("来源标注：") :]
            elif body.startswith("特征："):
                cur["flags"] = [x.strip() for x in body[len("特征：") :].split("/")]
            elif body.startswith("新预览疑似命中："):
                cur["preview"].append(body[len("新预览疑似命中：") :])
            elif body.startswith("源库疑似命中："):
                cur["source"].append(body[len("源库疑似命中：") :])
            elif body.startswith("题干片段：") and not cur["snippet"]:
                cur["snippet"] = body[len("题干片段：") :]
    if cur is not None:
        rows.append(cur)
    return rows


def index_old_blocks():
    idx = {}
    for p in rc.walk_md(OLD_ROOT):
        rel = p.relative_to(OLD_ROOT).as_posix()
        full = "04-课件/习题集/习题书/" + rel
        for b in rc.extract_old_blocks(p):
            idx.setdefault(full, {})[b["header"].strip()] = b
    return idx


def is_sub_label(tok):
    parts = tok.split("-")
    if not 2 <= len(parts) <= 3:
        return False
    nums = []
    for part in parts:
        if not part.isdigit():
            return False
        nums.append(int(part))
    if nums[0] == 20:
        return False
    return all(0 <= n <= 99 for n in nums)


def sub_labels(text):
    found = []
    seen = set()
    for m in re.finditer(r"(?<![0-9A-Za-z])([0-9]{1,2}-[0-9]{1,2}(?:-[0-9]{1,2})?)", text):
        tok = m.group(1)
        if tok in seen or not is_sub_label(tok):
            continue
        seen.add(tok)
        # 忽略紧跟说明文字的“来源：第x届第x题”这类无连线上下文，靠行首/独立空位判定
        before = text[max(0, m.start() - 2) : m.start()]
        after = text[m.end() : m.end() + 1]
        if before.strip() and before.strip() not in ("（", "("):
            continue
        if after and after not in (" ", ".", "。", "，", ",", "：", ":", "）", ")", "\n"):
            continue
        found.append(tok)
    return found


def answer_text(block):
    body = "\n".join(block["text"])
    m = re.search(r"<details>(.*?)</details>", body, flags=re.S)
    return m.group(1) if m else body


def long_lines(text, min_len=25):
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith(("#", ">", "---", "```", "<details", "</details", "|")):
            continue
        if s.startswith(("**答案", "**解析", "**解题思路", "**知识点映射", "**易错分析", "**题目图示")):
            continue
        n = rc.norm(s)
        if min_len <= len(n) <= 900:
            out.append(n)
    return out


def huizhi_index():
    files = {}
    for p in rc.walk_md(HUIZHI_ROOT):
        text = rc.read_text(p)
        y = rc.frontmatter_yaml(text)
        if "type: 题目" not in y:
            continue
        body = re.sub(r"^---[ \t]*\n.*?\n---[ \t]*\n?", "", text, flags=re.S, count=1)
        qpart, _, apart = body.partition("## 参考答案")
        if not apart:
            qpart, _, apart = body.partition("## 答案")
        files[p.as_posix()] = {
            "stem": p.stem,
            "body_norm": rc.body_fingerprint_loose(body),
            "q_norm": rc.question_fingerprint(qpart),
            "a_norm": rc.body_fingerprint_loose(apart),
            "a_lines": set(long_lines(apart)),
            "labels": set(sub_labels(apart)),
        }
    return files


def attr_score(block, hz):
    body = "\n".join(block["text"])
    ans = answer_text(block)
    q_side = body.split("<details>", 1)[0]
    ans_lines = long_lines(ans)
    old_labels = set(sub_labels(ans))
    if not ans_lines and not old_labels:
        return 0
    score = 0
    label_hits = old_labels & hz["labels"]
    score += len(label_hits) * 2
    for ln in ans_lines:
        if ln in hz["a_lines"]:
            score += 2
        elif ln in hz["body_norm"]:
            score += 1
    q_lines = long_lines(q_side)
    for ln in q_lines:
        if ln in hz["q_norm"] or ln in hz["body_norm"]:
            score += 1
    return score


def main():
    text = rc.read_text(REPORT)
    rows = parse_report(text)
    old_idx = index_old_blocks()
    hz = huizhi_index()
    hz_list = sorted(hz.values(), key=lambda x: len(x["a_lines"]), reverse=True)

    print(f"明细共 {len(rows)} 条")
    print("分桶 " + "；".join(f"{k}={v}" for k, v in Counter(r['bucket'] for r in rows).most_common()))

    double_none = [r for r in rows if not r["preview"] and not r["source"]]
    print(f"双无（无预览命中且无源库命中）{len(double_none)} 条")
    print("双无分桶 " + "；".join(f"{k}={v}" for k, v in Counter(r['bucket'] for r in double_none).most_common()))

    lines = []
    lines.append("# Q-D 残差重建候选表（临时）")
    lines.append("")
    lines.append(f"- 正式明细：{len(rows)} 条")
    lines.append(f"- 双无条目：{len(double_none)} 条")
    lines.append("")
    lines.append("| # | 旧书题块 | 桶 | 特征 | 小问标签 | 汇智候补 | 分 |")
    lines.append("|---:|---|---|---|---|---:|---:|")

    attributed = []
    multi = []
    none = []
    for i, r in enumerate(double_none, 1):
        block = old_idx.get(r["path"], {}).get(r["header"])
        if block is None:
            none.append((r, [], 0))
            lines.append(f"| {i} | {r['path']} `{r['header']}` | {r['bucket']} | 未找到旧块 | - | - | - |")
            continue
        scored = []
        ans = answer_text(block)
        old_labels = set(sub_labels(ans))
        for h in hz_list:
            s = attr_score(block, h)
            if s > 0:
                scored.append((s, h["stem"]))
        scored.sort(reverse=True)
        top = scored[:3] if scored else []
        top_score = top[0][0] if top else 0
        second_score = top[1][0] if len(top) > 1 else 0
        label_txt = "、".join(sorted(old_labels)[:8]) if old_labels else "-"
        cand_txt = "；".join(f"{s}({name})" for s, name in top) if top else "-"
        if top_score >= 8 and top_score - second_score >= 2:
            verdict = "汇智唯一归因"
            attributed.append((r, top[0][1], top_score))
        elif top_score >= 8:
            verdict = "汇智多候选"
            multi.append((r, top, top_score))
        else:
            verdict = "未归因"
            none.append((r, top, top_score))
        lines.append(
            f"| {i} | {r['path']} `{r['header']}` | {r['bucket']} | {'/'.join(r['flags']) or '-'} "
            f"| {label_txt} | {cand_txt} | {verdict} |"
        )

    lines.append("")
    lines.append(f"汇智唯一归因：{len(attributed)}；多候选：{len(multi)}；未归因：{len(none)}")
    lines.append("")
    lines.append("## 未归因清单")
    lines.append("")
    lines.append("| # | 题块 | 桶 | 片段 |")
    lines.append("|---:|---|---|---|")
    for j, (r, top, top_score) in enumerate(none, 1):
        cand = f"（{top_score}）" if top else "-"
        lines.append(f"| {j} | {r['path']} `{r['header']}` | {r['bucket']} | {r['snippet'][:90]} |")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"输出：{OUT}")
    print(f"汇智唯一归因 {len(attributed)}；多候选 {len(multi)}；未归因 {len(none)}")


if __name__ == "__main__":
    raise SystemExit(main())
