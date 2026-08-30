#!/usr/bin/env python3
"""Q-D residual v2: label-overlap first attribution for double-none old blocks."""

import io
import re
import sys
from collections import Counter, defaultdict
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
OUT = ROOT / "_tmp_qd_residual_v2.md"


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


LABEL_RE = re.compile(r"(?<![0-9A-Za-z])([0-9]{1,2}-[0-9]{1,2}(?:-[0-9]{1,2})?)")
DIRECT_MARKER_RE = re.compile(r"题-汇智-(原子|分子|晶体)结构·题(\d+)")
LABEL_PREFIX_OK = (
    "",
    "（",
    "(",
    "题目",
    "题",
    "第",
    "、",
    "，",
    ",",
    "。",
    "：",
    ":",
    "答案",
    "小问",
    "—",
    "-",
)
CHAPTER_FAMILIES = {
    "1-原子结构.md": "原子",
    "2-分子结构与化学键.md": "分子",
    "3-晶体结构.md": "晶体",
}


def is_sub_label(tok):
    parts = tok.split("-")
    if not 2 <= len(parts) <= 3:
        return False
    nums = []
    for part in parts:
        if not part.isdigit():
            return False
        nums.append(int(part))
    return all(0 <= n <= 99 for n in nums)


def sub_labels(text):
    clean = text.replace("{", "").replace("}", "")
    clean = clean.replace(" - ", "-").replace(" -", "-").replace("- ", "-")
    found = []
    seen = set()
    for m in LABEL_RE.finditer(clean):
        tok = m.group(1)
        if tok in seen or not is_sub_label(tok):
            continue
        before = clean[max(0, m.start() - 2) : m.start()]
        after = clean[m.end() : m.end() + 1]
        if before.strip() and before.strip() not in LABEL_PREFIX_OK:
            continue
        if after and after not in (" ", ".", "。", "，", ",", "：", ":", "）", ")", "\n"):
            continue
        found.append(tok)
        seen.add(tok)
    return found


def direct_markers(text):
    """旧块答案中嵌入的汇智源文件 frontmatter 垃圾是最强直接归因信号。"""
    found = []
    seen = set()
    for kind, num in DIRECT_MARKER_RE.findall(text):
        stem = f"题-汇智-{kind}结构-{num}"
        if stem not in seen:
            seen.add(stem)
            found.append(stem)
    return found


def chapter_family(path):
    for fn, fam in CHAPTER_FAMILIES.items():
        if fn in path:
            return fam
    return None


def answer_text(block):
    body = "\n".join(block["text"])
    m = re.search(r"<details>(.*?)</details>", body, flags=re.S)
    return m.group(1) if m else body


def block_text(block):
    return "\n".join(block["text"])


def long_lines(text, min_len=20):
    out = []
    skip_prefixes = (
        "**答案",
        "**解析",
        "**解题思路",
        "**知识点映射",
        "**易错分析",
        "**题目图示",
    )
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith(("#", ">", "---", "```", "<details", "</details", "|")):
            continue
        if s.startswith(skip_prefixes):
            continue
        n = rc.norm(s)
        if min_len <= len(n) <= 1200:
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
        files[p.stem] = {
            "path": p.as_posix(),
            "stem": p.stem,
            "q_norm": rc.question_fingerprint(qpart),
            "body_norm": rc.body_fingerprint_loose(body),
            "a_norm": rc.body_fingerprint_loose(apart),
            "a_lines": set(long_lines(apart)),
            "a_labels": set(sub_labels(apart)),
            "q_labels": set(sub_labels(qpart)),
        }
    return files


def attr(block, hz, preferred=""):
    body = block_text(block)
    ans = answer_text(block)
    q_side = body.split("<details>", 1)[0]
    old_labels = set(sub_labels(ans))
    if not old_labels:
        old_labels = set(sub_labels(body))
    ans_lines = set(long_lines(ans))
    q_lines = set(long_lines(q_side))
    label_hits = old_labels & hz["a_labels"]
    total_q_hits = old_labels & (hz["a_labels"] | hz["q_labels"])
    coverage = len(label_hits) / len(old_labels) if old_labels else 0.0
    text_hits = len(ans_lines & hz["a_lines"])
    # 题干整段包含匹配：旧题干若在源题库题干指纹中出现即强信号
    q_contain = 0
    for ln in q_lines:
        if ln and (ln in hz["q_norm"] or ln in hz["body_norm"]):
            q_contain += 1
    score = int(coverage * 100) + len(label_hits) * 3 + text_hits * 2 + q_contain * 1
    if preferred and preferred in hz["stem"]:
        score += 2
    return {
        "label_hits": len(label_hits),
        "total_q_hits": len(total_q_hits),
        "coverage": coverage,
        "text_hits": text_hits,
        "q_contain": q_contain,
        "score": score,
        "labels": sorted(label_hits)[:10],
    }


def verdict(top):
    if not top:
        return "未归因", "-"
    t, t_stem = top[0]
    second = top[1] if len(top) > 1 else None
    second_rec = second[0] if second is not None else None
    if t["coverage"] >= 0.5 and (second_rec is None or second_rec["coverage"] < 0.5):
        return "唯一归因-标签", t_stem
    if t["score"] >= 8 and (second_rec is None or t["score"] - second_rec["score"] >= 2):
        return "唯一归因-内容", t_stem
    if t["score"] >= 8:
        return "汇智多候选", "、".join(x[1] for x in top[:3])
    return "未归因", "-"


def main():
    text = rc.read_text(REPORT)
    rows = parse_report(text)
    old_idx = index_old_blocks()
    hz = huizhi_index()
    hz_list = sorted(hz.values(), key=lambda x: (len(x["a_labels"]), len(x["a_lines"])), reverse=True)
    hz_by_stem = {h["stem"]: h for h in hz_list}

    double_none = [r for r in rows if not r["preview"] and not r["source"]]
    print(f"明细 {len(rows)}；双无 {len(double_none)}")

    lines = []
    lines.append("# Q-D 残差 v2 归因表（临时）")
    lines.append("")
    lines.append(f"- 双无条目：{len(double_none)}")
    lines.append("")
    lines.append("| # | 旧书题块 | 桶 | 旧标签 | 唯一归因 | 候选 | 分 | 判定 |")
    lines.append("|---:|---|---|---|---|---:|---|---|")

    counted = Counter()
    missing_candidates = []
    for i, r in enumerate(double_none, 1):
        block = old_idx.get(r["path"], {}).get(r["header"])
        if block is None:
            counted["未找到旧块"] += 1
            lines.append(f"| {i} | {r['path']} `{r['header']}` | {r['bucket']} | - | - | - | - | 未找到旧块 |")
            continue
        body = block_text(block)
        ans = answer_text(block)
        pref = chapter_family(r["path"])
        old_labels = set(sub_labels(ans)) or set(sub_labels(body))
        scored = []
        for h in hz_list:
            a = attr(block, h, pref or "")
            if a["score"] > 0 or a["label_hits"] > 0 or a["coverage"] > 0:
                scored.append((a, h["stem"]))
        scored.sort(key=lambda x: (-x[0]["score"], -x[0]["coverage"]))
        top = scored[:4] if scored else []
        top_rec = top[0][0] if top else None
        direct = direct_markers(body)
        direct_hit = next((s for s in direct if s in hz_by_stem), None)
        direct_missing = [s for s in direct if s not in hz_by_stem]
        if direct_hit:
            verdict_text = "唯一归因-直接标记"
            target = direct_hit
            counted["唯一归因-直接标记"] += 1
        elif direct_missing:
            verdict_text = "直接标记-缺源文件"
            target = "、".join(direct_missing)
            counted["直接标记-缺源文件"] += 1
            missing_candidates.append(
                (r, old_labels, target, top_rec, "直接标记源文件不存在")
            )
        else:
            verdict_text, target = verdict(top)
            if verdict_text.startswith("唯一归因"):
                counted["唯一归因"] += 1
            elif verdict_text == "汇智多候选":
                counted["汇智多候选"] += 1
            else:
                counted["未归因"] += 1
                stems_txt = "、".join(x[1] for x in top[:4]) or "-"
                missing_candidates.append((r, old_labels, stems_txt, top_rec, ""))
        label_txt = "、".join(sorted(old_labels)[:10]) if old_labels else "-"
        cand_txt = "；".join(f"{sco}({name})" for sco, name in top[:4]) if top else "-"
        sc_txt = str(top_rec["score"]) if top_rec else "-"
        lines.append(
            f"| {i} | {r['path']} `{r['header']}` | {r['bucket']} | {label_txt} "
            f"| {target} | {cand_txt} | {sc_txt} | {verdict_text} |"
        )

    lines.append("")
    lines.append("汇总：" + "；".join(f"{k}={v}" for k, v in counted.most_common()))
    lines.append("")
    lines.append("## 未归因与缺号待核")
    lines.append("")
    lines.append("| # | 题块 | 桶 | 旧标签 | 汇智候补 | 片段 | 备注 |")
    lines.append("|---:|---|---|---|---|---|---|")
    for j, (r, labels, cand, rec, extra) in enumerate(missing_candidates, 1):
        lines.append(
            f"| {j} | {r['path']} `{r['header']}` | {r['bucket']} | "
            f"{'、'.join(sorted(labels)[:10])} | {cand} | {r['snippet'][:80]} | {extra} |"
        )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"输出 {OUT}")
    print("汇总：" + "；".join(f"{k}={v}" for k, v in counted.most_common()))
    print("未归因/缺号 " + str(len(missing_candidates)))


if __name__ == "__main__":
    raise SystemExit(main())
