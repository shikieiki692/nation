#!/usr/bin/env python3
"""Q-D 对账辅助：导出旧书未匹配题块，并在新预览/源库中做宽松定位。

用法:
  python 11-模板/scripts/review_unmatched_blocks.py
  python 11-模板/scripts/review_unmatched_blocks.py --old-root 04-课件/习题集/习题书 \
      --source-root 04-题库 --preview-root .preview_build2

输出: 09-审计报告/<today>-习题书Q-D对账明细.md
"""

import io
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import reconcile_module_books as rc


def parse_args(argv):
    args = {
        "old_root": "04-课件/习题集/习题书",
        "source_root": "04-题库",
        "preview_root": ".preview_build2",
        "max_rows": 400,
    }
    keys = list(args)
    for i, a in enumerate(argv):
        if a.startswith("--") and a[2:] in keys and i + 1 < len(argv):
            v = argv[i + 1]
            if isinstance(args[a[2:]], int):
                v = int(v)
            args[a[2:]] = v
    return args


def clean_old_body(text):
    """去掉旧块中不会参与定位的元信息/占位行。"""
    t = text.replace("题干见源文件", "")
    t = re.sub(r"(?m)^##\s+相关题目\s*\n.*?(?=^##\s+|\Z)", "", t, flags=re.S)
    return t


def long_line_loose(text):
    """取旧块中最有辨识度的正文行（跳过标题/元信息/代码块）。"""
    lines = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith(("#", ">", "---", "```", "<details", "</details")):
            continue
        if s.startswith(("**答案", "**解析", "**解题思路", "**知识点映射")):
            continue
        norm = rc.norm(s)
        if 40 <= len(norm) <= 800:
            lines.append(norm)
    return lines


def block_header(text):
    m = re.search(r"^(##\s+\d+\.\d+.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def find_preview_hits(body_text, preview_blocks):
    """在预览题块中搜旧块正文；返回命中块及命中行数。"""
    search = rc.body_fingerprint_loose(clean_old_body(body_text))
    if len(search) < 30:
        search = ""
    lines = long_line_loose(clean_old_body(body_text))
    hits = []
    for pb in preview_blocks:
        score = 0
        if search and search in pb["noimg"]:
            score += 3
        for ln in lines:
            if ln in pb["noimg"]:
                score += 1
        if score >= 2:
            hits.append(
                {
                    "rel": pb["rel"],
                    "header": block_header(pb.get("_text", "")),
                    "score": score,
                }
            )
    return hits


def find_source_hits(body_text, source_loose):
    """在源库文件全文里搜旧块正文；返回源路径及命中行数。"""
    search = rc.body_fingerprint_loose(clean_old_body(body_text))
    if len(search) < 30:
        search = ""
    lines = long_line_loose(clean_old_body(body_text))
    hits = []
    for rel, loose in source_loose:
        score = 0
        if search and search in loose:
            score += 3
        for ln in lines:
            if ln in loose:
                score += 1
        if score >= 2:
            hits.append({"rel": rel, "score": score})
    return hits


def old_block_flags(body_text):
    flags = []
    if "题干见源文件" in body_text:
        flags.append("题干见源文件")
    if "原书未提供解答" in body_text:
        flags.append("无解答占位")
    if re.search(r"^##\s+(参考答案|答案|解析|解题思路|知识点映射|易错分析)", body_text, re.M):
        flags.append("内嵌答案节")
    if re.search(r"^#+\s*第[一二三四五六七八九十]+部分", body_text, re.M):
        flags.append("疑似整章混入")
    if re.search(r"^##\s*[一二三四五六七八九十]+、", body_text, re.M):
        flags.append("疑似源书题号")
    return flags


def main():
    args = parse_args(sys.argv[1:])
    old_root = Path(args["old_root"])
    src_root = Path(args["source_root"])
    prev_root = Path(args["preview_root"])
    preview_blocks = rc.build_preview_blocks(prev_root) if prev_root.is_dir() else []
    for pb in preview_blocks:
        pb["_text"] = pb.get("_text", "")
    # 重建预览块文本，供定位结果回显题号
    if prev_root.is_dir():
        preview_blocks = []
        for p in rc.walk_md(prev_root):
            rel = p.relative_to(prev_root).as_posix()
            for block in rc.split_question_blocks(rc.read_text(p)):
                pb = {
                    "rel": rel,
                    "fp": rc.question_fingerprint(block),
                    "loose": rc.body_fingerprint_loose(block),
                    "noimg": rc.body_fingerprint_loose(rc.strip_embedded_images(block)),
                    "_text": block,
                }
                preview_blocks.append(pb)
    source_loose = []
    src_meta = {}
    for p in rc.walk_md(src_root):
        text = rc.read_text(p)
        y = rc.frontmatter_yaml(text)
        if "type: 题目" not in y:
            continue
        rel = p.as_posix()
        full = re.sub(r"^---[ \t]*\n.*?\n---[ \t]*\n?", "", text, flags=re.S, count=1)
        loose = rc.body_fingerprint_loose(full)
        if len(loose) >= 20:
            source_loose.append((rel, loose))
        src_meta[rel] = {
            "status": (re.search(r"(?m)^status:\s*(.*)\s*$", y) or [None, ""])[1].strip(),
            "source": (re.search(r"(?m)^source:\s*(.*)\s*$", y) or [None, ""])[1].strip(),
        }

    by_fp, by_stem, by_source_key, _ = rc.build_source_index(src_root)
    prev_by_fp = {}
    for pb in preview_blocks:
        if len(pb["fp"]) >= 20:
            prev_by_fp.setdefault(pb["fp"], []).append(pb["rel"])
    rows = []
    bucket_counts = Counter()
    per_module = Counter()
    flags_counts = Counter()
    for p in sorted(rc.walk_md(old_root)):
        rel_key = p.relative_to(old_root).as_posix()
        for b in rc.extract_old_blocks(p):
            body_text = "\n".join(b["text"])
            fp = rc.question_fingerprint(body_text)
            note = b["source_note"]
            body_clean = clean_old_body(body_text)
            src_hits = by_fp.get(fp, [])
            if src_hits or fp in prev_by_fp:
                continue
            kind = rc.preview_match_kind(body_text, fp, rel_key, preview_blocks)
            if kind:
                continue
            segs = re.findall(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)+", note)
            stem_hit = any(by_stem.get(rc.norm(seg), []) for seg in segs)
            if stem_hit:
                continue
            key = rc.source_key(note)
            key_hits = by_source_key.get(key, []) if key else []
            if key and len(set(key_hits)) == 1:
                continue
            if note and any(marker in note for marker in ("经典例题", "教学改编", "无源")):
                continue
            source_link_body = "题干见源文件" in body_text
            if key and len(set(key_hits)) != 1:
                bucket = "来源键多候选"
            elif source_link_body:
                bucket = "题干见源文件-未定位"
            elif "忠实重录" in body_text or "忠实重录" in note:
                bucket = "忠实重录-未定位"
            elif not note:
                bucket = "无来源标注"
            else:
                bucket = "其他未匹配"
            bucket_counts[bucket] += 1
            per_module[rel_key.split("/", 1)[0]] += 1
            flags = old_block_flags(body_text)
            for f in flags:
                flags_counts[f] += 1
            phits = find_preview_hits(body_text, preview_blocks)
            shits = find_source_hits(body_text, source_loose)
            snippet = re.sub(r"\s+", " ", body_clean).strip()[:150]
            snippet = snippet.replace("|", "｜")
            rows.append(
                {
                    "path": p.as_posix(),
                    "header": b["header"],
                    "bucket": bucket,
                    "note": note,
                    "flags": flags,
                    "snippet": snippet,
                    "preview": sorted(phits, key=lambda x: -x["score"])[:2],
                    "source": sorted(shits, key=lambda x: -x["score"])[:3],
                }
            )

    out = []
    out.append("---")
    out.append("title: 习题书 Q-D 对账明细")
    out.append("type: 审计报告")
    out.append(f"updated: {date.today().isoformat()}")
    out.append(f"unmatched: {len(rows)}")
    out.append("---")
    out.append("")
    out.append("# 习题书 Q-D 对账明细")
    out.append("")
    out.append(f"旧书未匹配题块共 **{len(rows)}** 个。")
    out.append("")
    out.append("## 分桶")
    out.append("")
    for k, v in bucket_counts.most_common():
        out.append(f"- {k}: **{v}**")
    out.append("")
    out.append("## 按篇分布")
    out.append("")
    for k, v in per_module.most_common():
        out.append(f"- {k}: {v}")
    out.append("")
    out.append("## 旧块特征")
    out.append("")
    for k, v in flags_counts.most_common():
        out.append(f"- {k}: {v}")
    out.append("")
    out.append("## 明细")
    out.append("")
    for r in rows[: args["max_rows"]]:
        out.append(f"- `{r['path']}` · `{r['header']}` · 〔{r['bucket']}〕")
        if r["note"]:
            out.append(f"  - 来源标注：{r['note'][:120]}")
        if r["flags"]:
            out.append(f"  - 特征：{' / '.join(r['flags'])}")
        if r["preview"]:
            ph = r["preview"][0]
            out.append(f"  - 新预览疑似命中：`{ph['rel']}` `{ph['header']}`（score={ph['score']}）")
        if r["source"]:
            sh = r["source"][0]
            out.append(f"  - 源库疑似命中：`{sh['rel']}`（score={sh['score']}）")
        if r["snippet"]:
            out.append(f"  - 题干片段：{r['snippet']}")
        out.append("")
    out.append(f"未匹配共 {len(rows)} 个；本明细供 Q-D 逐桶复核。")
    out.append("")
    report_dir = Path("09-审计报告")
    report_dir.mkdir(exist_ok=True)
    out_path = report_dir / f"{date.today().isoformat()}-习题书Q-D对账明细.md"
    out_path.write_text("\n".join(out), encoding="utf-8")
    print(f"未匹配 {len(rows)} 个；分桶 " + "；".join(f"{k}={v}" for k, v in bucket_counts.most_common()))
    print(f"明细已写入 {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
