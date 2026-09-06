#!/usr/bin/env python3
"""只读对账：旧习题书每题 vs 当前 04-题库 源文件 vs 新版预览。

用法:
  python 11-模板/scripts/reconcile_module_books.py
  python 11-模板/scripts/reconcile_module_books.py --old-root 04-课件/习题集/习题书 \
      --source-root 04-题库 --preview-root .preview_build2 --max-unmatched 200

输出: 09-审计报告/<today>-习题书新旧对账.md
"""

import io
import os
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def parse_args(argv):
    args = {
        "old_root": "04-课件/习题集/习题书",
        "source_root": "04-题库",
        "preview_root": ".preview_build2",
        "max_unmatched": 200,
        "max_new_questions": 60,
    }
    keys = list(args)
    for i, a in enumerate(argv):
        if a.startswith("--") and a[2:] in keys and i + 1 < len(argv):
            v = argv[i + 1]
            if isinstance(args[a[2:]], int):
                v = int(v)
            args[a[2:]] = v
    return args


def norm(text):
    """题干指纹：小写、去空白与 Markdown 标点。"""
    t = text.lower()
    t = re.sub(r"\s+", "", t)
    t = re.sub(r"[#*_`>|\[\]()（）【】《》,，。；;：:!！?？\"'“”‘’\-—]", "", t)
    return t


def read_text(path):
    """统一读取 Markdown：去 BOM、把 CRLF 归一为 LF，保证正则与行处理稳定。"""
    return (
        Path(path)
        .read_text(encoding="utf-8", errors="replace")
        .lstrip("\ufeff")
        .replace("\r\n", "\n")
    )


def walk_md(root, skip_dirs=("高考",)):
    root = Path(root)
    if not root.is_dir():
        return
    for dirpath, dirnames, filenames in os.walk(root):
        if any(s in dirpath for s in skip_dirs):
            continue
        for fn in filenames:
            if fn.endswith(".md"):
                yield Path(dirpath) / fn


def frontmatter_yaml(text):
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n?", text, re.S)
    return m.group(1) if m else ""


QUESTION_START_RE = re.compile(r"(?m)^##[ \t]+题目\s*$")
ANSWER_START_RE = re.compile(
    r"(?m)^##[ \t]+(?:参考答案|答案|解析|解题思路|知识点映射|易错分析)\s*$"
)


def split_source_question(body):
    """取源文件题干正文：优先按 ## 题目 切，缺失标题时取答案节之前。"""
    body = re.sub(r"^---[ \t]*\n.*?\n---[ \t]*\n?", "", body, flags=re.S, count=1)
    work = re.sub(r"(?m)^#(?!#)[^\n]*$", "", body).strip()
    qloc = QUESTION_START_RE.search(work)
    aloc = ANSWER_START_RE.search(work)
    if qloc and (not aloc or qloc.start() < aloc.start()):
        q_end = aloc.start() if aloc else len(work)
        return work[qloc.end():q_end].strip()
    if aloc:
        return work[:aloc.start()].strip()
    return work


def question_fingerprint(text):
    """只保留题干正文指纹：去掉引用元信息、标题与答案块。"""
    t = strip_related_sections(text)
    t = re.sub(r"(?m)^>\s*\[!(?:info|note)\][^\n]*\n", "", t)
    t = re.sub(r"(?m)^>[^\n]*\n", "", t)
    t = re.sub(r"(?m)^#{1,6}\s+[^\n]*\n", "", t)
    t = re.sub(r"(?m)^-{3,}[ \t]*$", "", t)
    t = re.split(r"<details", t, maxsplit=1)[0]
    return norm(t)


def body_fingerprint_loose(text):
    """保留答案在内的宽松指纹；用于“题干见源文件”类旧块在新预览中定位。"""
    t = strip_related_sections(text)
    t = re.sub(r"(?m)^\s*>\s*\[!(?:info|note)\][^\n]*\n", "", t)
    t = re.sub(r"(?m)^\s*>[^\n]*\n", "", t)
    t = re.sub(r"(?m)^#{1,6}\s+[^\n]*\n", "", t)
    t = re.sub(r"(?m)^-{3,}[ \t]*$", "", t)
    return norm(t)


def strip_embedded_images(text):
    """去掉图片引用差异（Markdown 图链、Obsidian 嵌入、旧裸图链/裸哈希图名）。"""
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    t = re.sub(r"!\[\[[^\]]+\]\]", "", t)
    t = re.sub(r"![0-9a-fA-F]{32,64}\.[A-Za-z0-9]+", "", t)
    # 旧书裸路径图链可能含空格，使用非贪婪匹配并按首个扩展名截断
    t = re.sub(r"![^!\[\]()\r\n]+?\.(?:jpe?g|png|gif|svg|webp)", "", t)
    return t


def strip_related_sections(text):
    """去掉旧产物“相关题目”及其后的元信息块，避免干扰成书对账。"""
    return re.sub(r"(?ms)^##\s+相关题目\s*\n.*?(?=^##\s+|\Z)", "", text)


def exam_stage(text):
    """从来源描述提取初赛/决赛/复赛阶段。"""
    if not text:
        return ""
    for s in ("复赛", "初赛", "决赛"):
        if s in text:
            return s
    return ""


def source_key(text, fallback_stage=""):
    """从来源描述提取 (届, 阶段, 大题, 小问) 作为弱匹配键。

    示例：第28届初赛第1题第(1-2)小问、第32届决赛第6题。
    """
    s = re.sub(r"[（(][^）)]*原始文件[^）)]*[）)]", "", text)
    m = re.search(r"第\s*(\d+)\s*届[^\d]{0,30}第\s*(\d+)\s*题", s)
    if not m:
        return None
    sub = re.search(r"第\s*\(?([\d\-]+)\)?\s*小问", s)
    stage = exam_stage(s) or fallback_stage
    return (int(m.group(1)), stage, int(m.group(2)), sub.group(1) if sub else "")


def build_source_index(source_root):
    """返回题库索引：题干指纹、文件名片段、来源键，以及源文件元信息。"""
    by_fp = {}
    by_stem = {}
    by_source_key = {}
    meta = {}
    for p in walk_md(source_root):
        text = read_text(p)
        y = frontmatter_yaml(text)
        if "type: 题目" not in y:
            continue
        rel = p.as_posix()
        qfp = question_fingerprint(split_source_question(text))
        if len(qfp) >= 20:
            by_fp.setdefault(qfp, []).append(rel)
        stem_fp = norm(p.stem)
        if len(stem_fp) >= 8:
            by_stem.setdefault(stem_fp, []).append(rel)
            bare_fp = norm(re.sub(r"^题[_-]", "", p.stem))
            if len(bare_fp) >= 8:
                by_stem.setdefault(bare_fp, []).append(rel)
        src = (re.search(r"(?m)^source:\s*(.*)\s*$", y) or [None, ""])[1].strip()
        y_stage = (re.search(r"(?m)^exam_stage:\s*(.*)\s*$", y) or [None, ""])[1].strip()
        key = source_key(src, fallback_stage=y_stage)
        if key:
            by_source_key.setdefault(key, []).append(rel)
        meta[rel] = {
            "file": p.name,
            "stem": p.stem,
            "title": p.stem,
            "source": src,
            "module": (re.search(r"(?m)^subject_module:\s*(.*)\s*$", y) or [None, ""])[1].strip(),
            "pack": (re.search(r"(?m)^pack:\s*(.*)\s*$", y) or [None, ""])[1].strip(),
            "status": (re.search(r"(?m)^status:\s*(.*)\s*$", y) or [None, ""])[1].strip(),
            "stage": exam_stage(src) or y_stage,
        }
    return by_fp, by_stem, by_source_key, meta


def extract_old_blocks(path):
    text = read_text(path)
    lines = text.splitlines()
    blocks = []
    cur = None
    qh = re.compile(r"^##\s+(\d+\.\d+)(\s+〔.*?〕)?\s*$")
    for ln in lines:
        m = qh.match(ln)
        if m:
            if cur:
                blocks.append(cur)
            cur = {"header": ln, "text": [], "source_note": ""}
        elif cur is not None:
            cur["text"].append(ln)
            if not cur["source_note"]:
                m = re.search(r"来源[:：]\s*(.+)$", ln)
                if m:
                    cur["source_note"] = m.group(1).strip()
    if cur:
        blocks.append(cur)
    return blocks


def split_question_blocks(text):
    """新版章节文件里以 ## n.m 开头的题块。"""
    blocks = []
    cur = None
    qh = re.compile(r"^##\s+\d+\.\d+(\s+〔.*?〕)?\s*$")
    for ln in text.splitlines():
        if qh.match(ln):
            if cur is not None:
                blocks.append("\n".join(cur))
            cur = [ln]
        elif cur is not None:
            cur.append(ln)
    if cur is not None:
        blocks.append("\n".join(cur))
    return blocks


def build_preview_index(preview_root):
    """新版预览题块指纹 → 所在文件；用于判断旧书题目是否继续留在成书。"""
    by_fp = {}
    for p in walk_md(preview_root):
        for block in split_question_blocks(read_text(p)):
            fp = question_fingerprint(block)
            if len(fp) >= 20:
                by_fp.setdefault(fp, []).append(p.as_posix())
    return by_fp


def build_preview_blocks(preview_root):
    """新版预览题块及宽松指纹；旧块可按同章节文件做答案包含匹配。"""
    blocks = []
    for p in walk_md(preview_root):
        rel = p.relative_to(preview_root).as_posix()
        for block in split_question_blocks(read_text(p)):
            blocks.append(
                {
                    "rel": rel,
                    "fp": question_fingerprint(block),
                    "loose": body_fingerprint_loose(block),
                    "noimg": body_fingerprint_loose(strip_embedded_images(block)),
                }
            )
    return blocks


def preview_match_kind(body_text, fp, rel_key, preview_blocks):
    """在同篇跨章预览题块中定位旧块，返回 fp/loose 匹配类型或 None。"""
    old_mod = rel_key.split("/", 1)[0]
    source_link_body = "题干见源文件" in body_text
    if len(fp) >= 20:
        for pb in preview_blocks:
            if pb["rel"].rsplit("习题书/", 1)[-1].split("/", 1)[0] == old_mod and fp in pb["fp"]:
                return "fp"
    old_body = body_text.replace("题干见源文件", "")
    loose = body_fingerprint_loose(old_body)
    if len(loose) >= 20:
        for pb in preview_blocks:
            if pb["rel"].rsplit("习题书/", 1)[-1].split("/", 1)[0] == old_mod and loose in pb["loose"]:
                return "loose"
    # 旧块若保留裸哈希图名，预览已统一为 ![[哈希.jpg]]；去掉图片后仍有相同正文才算命中
    loose_ni = body_fingerprint_loose(strip_embedded_images(old_body))
    if len(loose_ni) >= 20 and loose_ni != loose:
        for pb in preview_blocks:
            if pb["rel"].rsplit("习题书/", 1)[-1].split("/", 1)[0] == old_mod and loose_ni in pb["noimg"]:
                return "loose"
    # 旧块可能是新预览连续多个题块的拼接，只在长块上启用以免短题干误命中
    if len(loose) >= 1000:
        by_chapter = {}
        for pb in preview_blocks:
            key = pb["rel"].rsplit("习题书/", 1)[-1]
            if key.rsplit("/", 1)[0] == old_mod:
                by_chapter.setdefault(key, []).append(pb["noimg"])
        for parts in by_chapter.values():
            if loose in "".join(parts):
                return "loose"
    return None


def fingerprint_block(text):
    """取题块前 200 个字符的指纹，去掉 metadata 小节。"""
    body = re.sub(r"(?m)^##\s+[^\n]*\n", "", text)
    return norm(body[:200])


def main():
    args = parse_args(sys.argv[1:])
    old_root = Path(args["old_root"])
    src_root = Path(args["source_root"])
    prev_root = Path(args["preview_root"])
    if not old_root.is_dir():
        print(f"旧书目录不存在: {old_root}")
        return 1
    if not src_root.is_dir():
        print(f"源库目录不存在: {src_root}")
        return 1

    by_fp, by_stem, by_source_key, src_meta = build_source_index(src_root)
    preview_blocks = build_preview_blocks(prev_root) if prev_root.is_dir() else []
    prev_by_fp = {}
    for pb in preview_blocks:
        if len(pb["fp"]) >= 20:
            prev_by_fp.setdefault(pb["fp"], []).append(pb["rel"])
    old_total = 0
    confirmed = 0
    fuzzy = 0
    old_in_preview = 0
    answer_in_preview = 0
    classic_manual = 0
    old_only_sources = []
    unmatched = []
    fuzzy_records = []
    source_key_unmatched = Counter()
    bucket_counts = Counter()

    for p in sorted(walk_md(old_root)):
        blocks = extract_old_blocks(p)
        old_total += len(blocks)
        rel_key = p.relative_to(old_root).as_posix()
        for b in blocks:
            body_text = "\n".join(b["text"])
            source_link_body = "题干见源文件" in body_text
            fp = question_fingerprint(body_text)
            src_hits = by_fp.get(fp, [])
            in_prev = fp in prev_by_fp
            if in_prev:
                old_in_preview += 1
            if src_hits:
                confirmed += 1
                if not in_prev:
                    if preview_match_kind(body_text, fp, rel_key, preview_blocks):
                        old_in_preview += 1
                    else:
                        for rel in src_hits[:1]:
                            old_only_sources.append((rel, src_meta.get(rel, {}), p.as_posix(), b["header"]))
                continue
            if in_prev:
                # 新预览里存在，但当前题库指纹未命中：通常只是措辞微调
                confirmed += 1
                continue
            kind = preview_match_kind(body_text, fp, rel_key, preview_blocks)
            if kind == "fp":
                confirmed += 1
                old_in_preview += 1
                continue
            if kind == "loose":
                answer_in_preview += 1
                old_in_preview += 1
                continue
            # 弱匹配：来源标注里的文件名片段，例如 Ch13-例13.6、题-053-1
            segs = re.findall(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)+", b["source_note"])
            stem_hits = []
            for seg in segs:
                stem_hits += by_stem.get(norm(seg), [])
            if stem_hits:
                fuzzy += 1
                fuzzy_records.append((p.as_posix(), b["header"], b["source_note"][:80], stem_hits[:1]))
                continue
            key = source_key(b["source_note"])
            key_hits = by_source_key.get(key, []) if key else []
            if len(set(key_hits)) == 1:
                fuzzy += 1
                fuzzy_records.append((p.as_posix(), b["header"], b["source_note"][:80], key_hits[:1]))
                continue
            note = b["source_note"] or ""
            if note and any(marker in note for marker in ("经典例题", "教学改编", "无源")):
                classic_manual += 1
                continue
            if key:
                bucket = "来源键多候选"
                source_key_unmatched[key] += 1
            elif source_link_body:
                bucket = "题干见源文件-未定位"
            elif "忠实重录" in body_text or "忠实重录" in note:
                bucket = "忠实重录-未定位"
            elif not note:
                bucket = "无来源标注"
            else:
                bucket = "其他未匹配"
            bucket_counts[bucket] += 1
            rec = {
                "path": p.as_posix(),
                "header": b["header"],
                "note": b["source_note"],
                "bucket": bucket,
            }
            unmatched.append(rec)

    # 新预览题块数、新增题、旧书有但新预览无的来源
    new_total = 0
    preview_new_by_fp = {}
    old_fp_seen = set()
    for p in sorted(walk_md(old_root)):
        for b in extract_old_blocks(p):
            old_fp_seen.add(question_fingerprint("\n".join(b["text"])))
    if prev_root.is_dir():
        for p in walk_md(prev_root):
            for block in split_question_blocks(read_text(p)):
                new_total += 1
                fp = question_fingerprint(block)
                if fp not in old_fp_seen:
                    preview_new_by_fp.setdefault(fp, []).append(p.as_posix())

    old_only_unique = {}
    for rel, meta, book_path, header in old_only_sources:
        old_only_unique.setdefault(rel, {"meta": meta, "old_places": []})["old_places"].append(
            (book_path, header)
        )

    preview_new_sources = {}
    for fp, paths in preview_new_by_fp.items():
        srcs = by_fp.get(fp, [])
        for rel in srcs:
            preview_new_sources.setdefault(rel, []).extend(paths[:1])

    out = []
    out.append("---")
    out.append("title: 习题书新旧对账")
    out.append("type: 审计报告")
    out.append(f"updated: {date.today().isoformat()}")
    out.append(f"old_total: {old_total}")
    out.append(f"new_preview_total: {new_total}")
    out.append("---")
    out.append("")
    out.append("# 习题书新旧对账")
    out.append("")
    out.append(f"> 旧书 `{args['old_root']}` 共 {old_total} 题；新预览 `{args['preview_root']}` 共 {new_total} 题。")
    out.append("")
    out.append("## 汇总")
    out.append("")
    out.append(f"- 旧书题块总数: **{old_total}**")
    out.append(f"- 题干指纹确认匹配: **{confirmed}**")
    out.append(f"- 文件名/来源键弱匹配: **{fuzzy}**")
    out.append(f"- 旧题答案在新预览定位: **{answer_in_preview}**")
    out.append(f"- 无源手工题（经典例题/教学改编）: **{classic_manual}**")
    out.append(f"- 未匹配: **{len(unmatched)}**")
    out.append(f"- 旧书题块同时存在于新预览: **{old_in_preview}**")
    out.append(f"- 旧书有、新预览无的源文件（唯一路径）: **{len(old_only_unique)}**")
    out.append(f"- 新预览有、旧书无的源文件（唯一路径）: **{len(preview_new_sources)}**")
    out.append(f"- 新预览题块总数: **{new_total}**")
    out.append("")
    out.append("> 说明：指纹匹配为只读自动判定；”旧书有、新预览无“与”新预览有、旧书无“已按唯一源路径去重，仍需人工复核章节归属与合并题差异。")
    out.append("")
    out.append("## 差异解释")
    out.append("")
    out.append("- 对账口径以旧书顶层 `## n.m` 题块为准；新预览按同格式题块计数，详见上方汇总。")
    out.append("- 旧书合并大块可能对应新预览同章单个大块或连续多个拆分块；例如 `第一篇-化学原理/6-综合.md` 的旧 `6.10`、`6.29`、`6.31` 分别落入新预览 `4.36`（10.25–10.37）、`4.35`（光合作用/锰氧簇）、`4.25`（10.20 电极电势-pH 图）。")
    out.append("- 旧产物“相关题目”及其后的元信息块不进入指纹，避免把旧产物导航/关联信息误当成题目差异。")
    out.append("- “旧书有、新预览无”按唯一源路径去重；若源文件 `status=deprecated`，说明旧合并文件已被拆分文件取代，不计为漏题。")
    out.append("")
    out.append("## 未匹配分桶")
    out.append("")
    for bucket, cnt in bucket_counts.most_common():
        out.append(f"- {bucket}: **{cnt}**")
    out.append("")

    out.append("## 旧书有、新预览无（候选差异）")
    out.append("")
    out.append(f"共 {len(old_only_unique)} 个源文件；这组应优先核对是否为旧产物多收、弃用或新管道漏题。")
    out.append("")
    for rel, info in sorted(old_only_unique.items()):
        m = info["meta"]
        old_place = info["old_places"][0]
        pack = m.get("pack") or "(无pack)"
        status = m.get("status") or "-"
        out.append(
            f"- `{rel}` [pack={pack} status={status}] · 旧书 {old_place[1]} in {old_place[0]}"
        )
    if old_only_unique:
        non_deprecated = [
            rel
            for rel, info in old_only_unique.items()
            if (info["meta"].get("status") or "") != "deprecated"
        ]
        if not non_deprecated:
            out.append("")
            out.append(
                f"> 上述 {len(old_only_unique)} 个源文件均 `status=deprecated`，属于旧合并文件；拆分后的新文件已进入新预览，整组视为正常排除，不阻塞替换。"
            )
        else:
            out.append("")
            out.append(
                f"> 存在 {len(non_deprecated)} 个非 deprecated 源文件，需先人工复核：`{'；'.join(non_deprecated[:5])}`。"
            )
    out.append("")

    out.append("## 新预览有、旧书无（新增方向）")
    out.append("")
    out.append(f"共 {len(preview_new_sources)} 个源文件；通常为源库新增或旧书漏收。")
    out.append("")
    for rel in sorted(preview_new_sources)[: args["max_new_questions"]]:
        out.append(f"- `{rel}`")
    if len(preview_new_sources) > args["max_new_questions"]:
        out.append(f"- … 其余 {len(preview_new_sources) - args['max_new_questions']} 个")
    out.append("")

    out.append("## 弱匹配记录")
    out.append("")
    out.append(f"共 {len(fuzzy_records)} 项；来自来源标注文件名或考试届数，未做逐字指纹确认。")
    out.append("")
    for book_path, header, note, hit in fuzzy_records[:40]:
        out.append(f"- `{book_path}` · `{header}` · {note} → `{hit[0]}`")
    if len(fuzzy_records) > 40:
        out.append(f"- … 其余 {len(fuzzy_records) - 40} 项")
    out.append("")

    out.append("## 未匹配明细")
    out.append("")
    out.append(f"共 {len(unmatched)} 项；需继续人工复核。")
    out.append("")
    if unmatched:
        out.append("")
        for rec in unmatched[: args["max_unmatched"]]:
            out.append(f"- `{rec['path']}` · `{rec['header']}` · {rec['note'][:90]} 〔{rec['bucket']}〕")
        if len(unmatched) > args["max_unmatched"]:
            out.append(f"- … 其余 {len(unmatched) - args['max_unmatched']} 项")
    out.append("")
    out.append(f"新预览 {new_total} 题 vs 旧书 {old_total} 题：净差 {new_total - old_total:+d}（成书口径，非唯一源路径差）。")
    out.append("")

    report_dir = Path("09-审计报告")
    report_dir.mkdir(exist_ok=True)
    out_path = report_dir / f"{date.today().isoformat()}-习题书新旧对账.md"
    out_path.write_text("\n".join(out), encoding="utf-8")
    print(f"旧书 {old_total} 题：指纹确认 {confirmed}，弱匹配 {fuzzy}，答案定位 {answer_in_preview}，无源手工 {classic_manual}，未匹配 {len(unmatched)}")
    print(f"未匹配分桶: " + "；".join(f"{k}={v}" for k, v in bucket_counts.most_common()))
    print(f"旧书在新预览中 {old_in_preview} 题；旧有源文件 {len(old_only_unique)} 个，新预览新增源文件 {len(preview_new_sources)} 个")
    print(f"新预览 {new_total} 题；报告已写入 {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
