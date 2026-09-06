"""习题书 V2 审计：非白名单教学块 / 图片位置 / HTML 表格 / 源文件映射。

用法:
    python 11-模板/scripts/audit_exercise_book.py [--root 04-课件/习题集/习题书-教师版]
        [--media-root 媒体仓库] [--source-root 04-题库]
        [--report 09-审计报告/2026-08-30-习题书V2基线.md]
        [--mapping 09-审计报告/2026-08-30-习题书V2-source-map.jsonl]
        [--image-context 09-审计报告/2026-08-30-习题书V2-图片归属清单.jsonl]
        [--no-image-context]
        [--no-precheck] [--limit-samples 5]

只读审计：不修改成书、不修改源题库。输出 Markdown 基线报告与 JSONL
源文件→成书映射清单，以及源文件图片归属清单（题干/参考答案/教学块/参考图示等），
供 Phase 1-5 持续对账。
"""

from __future__ import annotations

import argparse
import collections
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent

EMBED_RE = re.compile(r"!\[\[([^\]\n]+)\]\]")
HASH_NAME_RE = re.compile(r"[0-9a-fA-F]{64}\.[A-Za-z0-9]+")
QHEAD_RE = re.compile(r"^##\s+(\d+\.\d+)\b", re.M)
DETAILS_RE = re.compile(r"^<details>$", re.M)
PLACEHOLDER_RE = re.compile(r"（原书未提供解答）")

# 非白名单教学块标记：成书只允许 题目/解析/适当拓展/来源/知识点 进入正文。
BLOCK_RULES = [
    ("小问关联", re.compile(r"小问关联")),
    ("得分点", re.compile(r"得分点")),
    ("关联KP表", re.compile(r"关联\s*KP")),
    ("读题定位", re.compile(r"读题定位")),
    ("关键转换", re.compile(r"关键转换")),
    ("计算要点", re.compile(r"计算要点")),
    ("错误/课堂提问表", re.compile(r"^\s*\|?\s*错误\s*\|")),
    ("易错分析", re.compile(r"易错分析")),
    ("解题思路", re.compile(r"解题思路")),
    ("相关图片", re.compile(r"相关图片")),
    ("知识点映射", re.compile(r"知识点映射")),
]

# 源文件里“标题与正文同行”的典型写法，生成后会留下粘连残块。
HEADING_GLUE_RE = re.compile(
    r"^#{1,6}[ \t]+(?:题目|参考答案|参考解答|答案|解答|解析|解题思路|知识点映射|易错分析)[^\n]*[^\s#]"
)

# 知识点映射标题被 split_question_answer 吞掉后留下的无标题残块：
# “- 知识点名 — 说明”，出现在答案 <details> 内。
KP_RESIDUAL_RE = re.compile(r"^\s*-\s*[^:：$\n]{1,40}\s+[—-]\s+")

HTML_IMG_RE = re.compile(r"<img\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
SECTION_HEADING_RE = re.compile(r"^#{1,6}[ \t]+([^\n#]{1,200})$")
BOLD_HEADING_RE = re.compile(r"^\*\*\s*([^\n*]{1,60})\s*\*\*\s*$")

# 源文件图片归属的区块顺序（报告展示用）。
BUCKET_ORDER = [
    "题干",
    "题干图示",
    "参考答案",
    "知识点映射",
    "解题思路",
    "易错分析",
    "相关图片",
    "参考图示",
    "其他/扩展",
    "其他",
]

# 教师版/学生版目录 → 生成器模块名
MODULE_DIRS = [
    ("第一篇-化学原理", "化学原理"),
    ("第二篇-结构化学", "结构化学"),
    ("第三篇-有机化学", "有机化学"),
    ("第四篇-元素与分析", "元素与分析"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def fm_value(yaml_text: str, key: str) -> str:
    m = re.search(rf"(?m)^{re.escape(key)}:\s*(.*)", yaml_text)
    return m.group(1).strip().strip('"') if m else ""


def trim_line(line: str, width: int = 90) -> str:
    line = line.strip()
    if len(line) <= width:
        return line
    return line[:width] + "…"


def classify_image_risks(line: str) -> list[str]:
    """按行返回图片位置风险类别；独立成段的单图不算风险。"""
    risks = []
    lower = line.lower()
    if re.search(r"---\s*!\[\[", line):
        risks.append("图贴分隔线")
    embeds = EMBED_RE.findall(line)
    if len(embeds) > 1:
        risks.append("同行多图")
    if "<td" in lower and "![[" in line:
        risks.append("表格单元格内图")
    if "<img" in lower:
        risks.append("HTML-img残留")
    if embeds:
        rest = EMBED_RE.sub("", line).strip()
        if re.search(r"[\u4e00-\u9fffA-Za-z0-9]", rest):
            risks.append("图文同行")
    return risks


def image_disposition(bucket: str) -> str:
    """成书白名单下的图片最终处置。

    题干/参考答案原图保留；参考图示是跨题复用的装饰/背景图候选，应删除；
    其余教学块里的图片可能藏着原题必需图，先标“待人工”，不能一刀切删除。
    """
    if bucket in ("题干", "参考答案"):
        return "保留"
    if bucket == "参考图示":
        return "应删除"
    return "待人工"


def classify_section_bucket(text: str, in_answer: bool = False) -> str | None:
    """把源文件小标题归入图片归属区块；顺序很重要，避免误判。"""
    t = re.sub(r"\s+", "", text).strip("*").lstrip("#").strip()
    if not t:
        return None
    if "知识点映射" in t:
        return "知识点映射"
    if "题目图示与结构参考" in t or t.startswith("题目图示"):
        # 决赛源文件常见小节，通常放的是题干必需原图，不能直接删。
        return "题干图示"
    if "知识扩展" in t or "相关拓展" in t or t.endswith("扩展") or t.endswith("拓展"):
        return "其他/扩展"
    if t.startswith("参考图示"):
        return "参考图示"
    if t.startswith("结构参考"):
        # 答案之后的“结构参考”多为解析图示；题干区域的同名标题保守归“题干图示”。
        return "参考答案" if in_answer else "题干图示"
    if "解题思路" in t:
        return "解题思路"
    if "易错分析" in t:
        return "易错分析"
    if "相关图片" in t:
        return "相关图片"
    if re.match(r"^(参考答案|参考解答|答案|解答|解析)", t):
        return "参考答案"
    if t.startswith("题目"):
        return "题干"
    return None


def normalize_image_base(target: str) -> str:
    target = target.split("|", 1)[0].strip().replace("\\", "/")
    base = os.path.basename(target).strip()
    return base if base else ""


def image_refs_in_line(line: str) -> list[dict]:
    refs = []
    for m in EMBED_RE.finditer(line):
        raw = m.group(1).strip()
        refs.append(
            {
                "kind": "obsidian",
                "raw": raw,
                "base": normalize_image_base(raw),
                "start": m.start(),
            }
        )
    for m in HTML_IMG_RE.finditer(line):
        raw = m.group(1).strip()
        refs.append(
            {
                "kind": "html_img",
                "raw": raw,
                "base": normalize_image_base(raw),
                "start": m.start(),
            }
        )
    refs.sort(key=lambda r: r["start"])
    return refs


def scan_source_images(source_root: Path, media_root: Path, mapping: list[dict]) -> list[dict]:
    """遍历源题文件，逐行记录每张图片的区块归属与成书映射。"""
    by_path = {}
    for rec in mapping:
        by_path.setdefault(rec["source_path"], []).append(rec)

    records = []
    for source_path, mrecs in sorted(by_path.items()):
        path = source_root / source_path
        if not path.is_file():
            records.append(
                {
                    "source_path": source_path,
                    "source_title": mrecs[0]["source_title"],
                    "generated_entries": [
                        {
                            "generated_chapter": r["generated_chapter"],
                            "generated_qno": r["generated_qno"],
                            "difficulty": r["difficulty"],
                            "fidelity": r["fidelity"],
                            "has_answer": r["has_answer"],
                        }
                        for r in mrecs
                    ],
                    "line": 0,
                    "kind": "missing_source",
                    "base": "",
                    "raw": "",
                    "bucket": "其他",
                    "block_heading": "",
                    "question_index": 0,
                    "in_answer": False,
                    "in_td": False,
                    "multi_image_line": False,
                    "glued_to_separator": False,
                    "media_present": False,
                    "disposition": "待人工",
                    "line_snippet": "源文件缺失",
                }
            )
            continue

        text = read_text(path)
        fm = parse_frontmatter(text)
        body_start = 0
        if fm:
            m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            if m:
                body_start = m.end()
        body = text[body_start:]
        base_line = text.count("\n", 0, body_start)

        current_bucket = "题干"
        current_heading = "（题首）"
        in_answer = False
        qindex = 1
        qhead_seen = False

        for li, line in enumerate(body.splitlines(), 1):
            line_no = base_line + li
            # 源文件常见 `## 解题思路1. ...#` 尾部残留井号，先归一化再识别标题。
            stripped_heading = line.rstrip().rstrip("#").rstrip()
            hm = SECTION_HEADING_RE.match(stripped_heading) or BOLD_HEADING_RE.match(stripped_heading)
            heading_text = hm.group(1) if hm else ""
            if not hm and line.lstrip().startswith("#") and "![" in line:
                # 长标题与图片同行（如 `## 解题思路1. ...![[hash.jpg]]`），
                # SECTION_HEADING_RE 匹配不到，但图片语义应归属该标题区块。
                heading_text = line.split("![", 1)[0].strip()
                hm = object()
            if hm:
                bucket = classify_section_bucket(heading_text, in_answer=in_answer)
                if bucket:
                    current_bucket = bucket
                    current_heading = trim_line(heading_text.strip(), 40)
                    if bucket == "题干":
                        in_answer = False
                        qindex = 1 if not qhead_seen else qindex + 1
                        qhead_seen = True
                    elif bucket in ("参考答案", "解题思路", "易错分析", "知识点映射"):
                        in_answer = True

            refs = image_refs_in_line(line)
            if not refs:
                continue
            multi = len(refs) > 1
            in_td = "<td" in line.lower()
            glued = bool(re.search(r"---\s*!\[\[", line))
            for ref in refs:
                if not ref["base"]:
                    continue
                records.append(
                    {
                        "source_path": source_path,
                        "source_title": mrecs[0]["source_title"],
                        "generated_entries": [
                            {
                                "generated_chapter": r["generated_chapter"],
                                "generated_qno": r["generated_qno"],
                                "difficulty": r["difficulty"],
                                "fidelity": r["fidelity"],
                                "has_answer": r["has_answer"],
                            }
                            for r in mrecs
                        ],
                        "line": line_no,
                        "kind": ref["kind"],
                        "base": ref["base"],
                        "raw": ref["raw"],
                        "bucket": current_bucket,
                        "block_heading": current_heading,
                        "question_index": qindex,
                        "in_answer": in_answer,
                        "in_td": in_td,
                        "multi_image_line": multi,
                        "glued_to_separator": glued,
                        "media_present": (media_root / ref["base"]).is_file(),
                        "disposition": image_disposition(current_bucket),
                        "line_snippet": trim_line(line, 120),
                    }
                )
    # 同一张图出现在多个源题文件里，通常是 OCR 页眉/装饰图或跨题复用；
    # 记录 repeat_files 供 Phase 2 优先核验，避免把原题必需图误判为删除。
    base_file_sets: dict[str, set[str]] = collections.defaultdict(set)
    for r in records:
        if r["base"]:
            base_file_sets[r["base"]].add(r["source_path"])
    for r in records:
        r["repeat_files"] = len(base_file_sets.get(r["base"], ()))
        r["cross_question_repeat"] = r["repeat_files"] > 1
    return records


def load_builder():
    """加载生成器模块，复用 gather/classify/split 逻辑做映射重建。"""
    spec = importlib.util.spec_from_file_location(
        "build_module_book", SCRIPT_DIR / "build_module_book.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def scan_chapter(path: Path, root: Path, media_root: Path):
    text = read_text(path)
    rel = path.relative_to(root).as_posix()
    fm = parse_frontmatter(text)
    declared = int(fm_value(fm, "question_count") or 0)
    edition = fm_value(fm, "edition") or ""
    subject = fm_value(fm, "subject_module") or ""

    qheads = [m.group(1) for m in QHEAD_RE.finditer(text)]
    details = len(DETAILS_RE.findall(text))
    placeholders = len(PLACEHOLDER_RE.findall(text))

    embeds = []
    missing = set()
    for m in EMBED_RE.finditer(text):
        raw = m.group(1).strip().split("|", 1)[0].strip()
        base = os.path.basename(raw.replace("\\", "/")).strip()
        if not base:
            continue
        line_no = text.count("\n", 0, m.start()) + 1
        embeds.append({"base": base, "raw": raw, "line": line_no})
        if not (media_root / base).is_file():
            missing.add(base)
    path_embeds = sum(1 for e in embeds if "/" in e["raw"] or "\\" in e["raw"])

    block_hits = collections.Counter()
    block_samples = collections.defaultdict(list)
    image_risks = collections.Counter()
    image_risk_samples = collections.defaultdict(list)
    heading_glue = []

    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        for label, rule in BLOCK_RULES:
            if rule.search(line):
                block_hits[label] += 1
                if len(block_samples[label]) < 5:
                    block_samples[label].append((rel, i, trim_line(line)))
        if HEADING_GLUE_RE.search(line):
            heading_glue.append((rel, i, trim_line(line)))
        for risk in classify_image_risks(line):
            count = len(re.findall(r"<img\b", line, re.I)) if risk == "HTML-img残留" else 1
            image_risks[risk] += count
            if len(image_risk_samples[risk]) < 5:
                image_risk_samples[risk].append((rel, i, trim_line(line)))

    tables = len(re.findall(r"<table\b", text, re.I))
    colspans = len(re.findall(r"colspan\s*=", text, re.I))
    rowspans = len(re.findall(r"rowspan\s*=", text, re.I))
    td_images = sum(
        1
        for line in lines
        if "<td" in line.lower() and ("![[" in line or "<img" in line.lower())
    )
    br_in_tables = len(re.findall(r"<br\b", text, re.I))

    # 按题块统计答案块、图片归属
    qblocks = []
    positions = list(QHEAD_RE.finditer(text))
    kp_residual_lines = 0
    kp_residual_samples = []
    for idx, m in enumerate(positions):
        qno = m.group(1)
        end = positions[idx + 1].start() if idx + 1 < len(positions) else len(text)
        block = text[m.start():end]
        q_images = a_images = t_images = other_images = 0
        in_details = False
        for li, line in enumerate(block.splitlines(), 1):
            if in_details and KP_RESIDUAL_RE.match(line) and "$" not in line and "=" not in line and "**" not in line:
                kp_residual_lines += 1
                if len(kp_residual_samples) < 5:
                    line_no = text.count("\n", 0, m.start()) + li
                    kp_residual_samples.append((rel, line_no, trim_line(line)))
            if DETAILS_RE.search(line):
                in_details = True
                continue
            line_embeds = len(EMBED_RE.findall(line))
            if line_embeds == 0:
                continue
            if in_details:
                a_images += line_embeds
            elif any(rule.search(line) for _, rule in BLOCK_RULES):
                t_images += line_embeds
            else:
                q_images += line_embeds
        other_images = max(0, len(EMBED_RE.findall(block)) - q_images - a_images - t_images)
        qblocks.append(
            {
                "qno": qno,
                "has_answer": bool(DETAILS_RE.search(block)),
                "image_count": len(EMBED_RE.findall(block)),
                "images_question": q_images,
                "images_answer": a_images,
                "images_teaching": t_images,
                "images_other": other_images,
            }
        )

    return {
        "path": rel,
        "title": fm_value(fm, "title") or path.stem,
        "edition": edition,
        "subject_module": subject,
        "declared": declared,
        "qheads": qheads,
        "details": details,
        "placeholders": placeholders,
        "embeds": embeds,
        "path_embeds": path_embeds,
        "missing": sorted(missing),
        "block_hits": block_hits,
        "block_samples": dict(block_samples),
        "image_risks": image_risks,
        "image_risk_samples": dict(image_risk_samples),
        "heading_glue": heading_glue,
        "kp_residual_lines": kp_residual_lines,
        "kp_residual_samples": kp_residual_samples,
        "tables": tables,
        "colspans": colspans,
        "rowspans": rowspans,
        "td_images": td_images,
        "br_in_tables": br_in_tables,
        "qblocks": qblocks,
        "qblock_by_qno": {b["qno"]: b for b in qblocks},
    }


def collect_chapters(root: Path):
    files = []
    for path in sorted(root.rglob("*.md")):
        if path.name in {"目录.md", "_未分类submodule统计.md", "来源索引.md"}:
            continue
        files.append(path)
    return files


def build_mapping(builder, source_root: Path, chapters_by_file: dict[str, dict]):
    """用生成器同一套 gather/classify/sort 逻辑重建源文件→成书映射。"""
    records = []
    by_chapter = {}
    for rel, info in chapters_by_file.items():
        by_chapter.setdefault(rel, []).append(info)

    for book_dir, module in MODULE_DIRS:
        chapter_map = {
            "化学原理": builder.CHEM_MAP,
            "结构化学": builder.STRUCTURE_MAP,
            "有机化学": builder.ORGANIC_MAP,
            "元素与分析": builder.YSFX_MAP,
        }[module]
        fallback = (6, "综合") if module == "化学原理" else (99, "综合")
        exclude = builder.ORGANIC_EXCLUDE if module == "有机化学" else set()

        pool = [
            q for q in builder.gather_questions(module)
            if q["submodule"] not in exclude
        ]
        groups = collections.OrderedDict()
        for item in pool:
            res = builder.classify_by_keywords(item, chapter_map, module)
            if res is None:
                res = fallback
            groups.setdefault(res, []).append(item)
        groups = collections.OrderedDict(
            sorted(groups.items(), key=lambda x: x[0][0])
        )

        for (num, name), items in groups.items():
            items.sort(key=lambda x: x["difficulty"])
            fname = f"{num}-{name}.md"
            chapter_rel = f"{book_dir}/{fname}"
            chapter_info = by_chapter.get(chapter_rel)
            declared = chapter_info[0]["declared"] if chapter_info else None
            status = "ok"
            if not chapter_info:
                status = "chapter_missing"
            elif declared != len(items):
                status = "count_mismatch"
            qblock_map = (
                chapter_info[0]["qblock_by_qno"] if chapter_info else {}
            )
            for qn, item in enumerate(items, 1):
                qno = f"{num}.{qn}"
                src_path = source_root / item["path"]
                src_text = read_text(src_path)
                src_fm = parse_frontmatter(src_text)
                body = src_text[len(src_fm) + 6:] if src_fm else src_text
                src_title = fm_value(src_fm, "title") or src_path.stem
                source_has_answer = bool(
                    builder.split_question_answer(body)[1].strip()
                )
                block = qblock_map.get(qno)
                if block:
                    has_answer = block["has_answer"]
                    image_count = block["image_count"]
                    images_question = block["images_question"]
                    images_answer = block["images_answer"]
                    images_teaching = block["images_teaching"]
                    images_other = block["images_other"]
                else:
                    has_answer = False
                    image_count = images_question = images_answer = 0
                    images_teaching = images_other = 0
                    status = "qno_missing"
                records.append(
                    {
                        "source_path": item["path"],
                        "source_title": src_title,
                        "generated_chapter": chapter_rel,
                        "generated_qno": qno,
                        "subject_module": module,
                        "difficulty": item["difficulty"],
                        "fidelity": item["fidelity"],
                        "has_answer": has_answer,
                        "source_has_answer": source_has_answer,
                        "image_count": image_count,
                        "images_question": images_question,
                        "images_answer": images_answer,
                        "images_teaching": images_teaching,
                        "images_other": images_other,
                        "mapping_status": status,
                    }
                )
    return records


def run_precheck(root: Path) -> tuple[int | None, int | None, str]:
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "precheck_exercise_books.py"),
        "--root",
        str(root),
    ]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
    except Exception as exc:
        return None, None, f"precheck 运行失败: {exc}"
    out = (proc.stdout or "") + (proc.stderr or "")
    m = re.search(r"TOTAL_ERRORS=(\d+)\s+TOTAL_WARNINGS=(\d+)\s+FILES=(\d+)", out)
    if not m:
        return None, None, "precheck 输出缺少 TOTAL_* 汇总行"
    return int(m.group(1)), int(m.group(2)), out.strip()


def fmt_md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |"]
    out.append("|" + "---|" * len(headers))
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


def render_report(args, teacher, student, mapping, precheck, image_records=None) -> str:
    today = date.today().isoformat()
    stem = Path(args.report).stem
    L = []
    L.append("---")
    L.append(f"title: {stem}")
    L.append("type: 审计报告")
    L.append(f"audit_date: {today}")
    L.append("edition: 教师版/学生版")
    L.append("generator: 11-模板/scripts/audit_exercise_book.py")
    L.append("---")
    L.append("")
    L.append(f"# {stem}")
    L.append("")
    L.append(
        "> 生成命令："
        f"`python 11-模板/scripts/audit_exercise_book.py --root {args.root}"
        f" --media-root {args.media_root} --source-root {args.source_root}"
        f" --report {args.report} --mapping {args.mapping}"
        f" --image-context {args.image_context}`"
    )
    L.append("")

    def sums(chapters):
        return {
            "questions": sum(c["declared"] for c in chapters.values()),
            "qheads": sum(len(c["qheads"]) for c in chapters.values()),
            "details": sum(c["details"] for c in chapters.values()),
            "placeholders": sum(c["placeholders"] for c in chapters.values()),
            "embeds": sum(len(c["embeds"]) for c in chapters.values()),
            "missing": sum(len(c["missing"]) for c in chapters.values()),
            "block": sum(sum(c["block_hits"].values()) for c in chapters.values()),
            "image_risks": sum(
                sum(c["image_risks"].values()) for c in chapters.values()
            ),
            "tables": sum(c["tables"] for c in chapters.values()),
            "colspans": sum(c["colspans"] for c in chapters.values()),
            "rowspans": sum(c["rowspans"] for c in chapters.values()),
            "heading_glue": sum(len(c["heading_glue"]) for c in chapters.values()),
            "kp_residual": sum(c["kp_residual_lines"] for c in chapters.values()),
        }

    t, s = sums(teacher), sums(student)
    L.append("## 一、总体基线")
    L.append("")
    L.append(
        fmt_md_table(
            ["指标", "教师版", "学生版"],
            [
                ["章节数", len(teacher), len(student)],
                ["题目数（frontmatter）", t["questions"], s["questions"]],
                ["题头数（## n.m）", t["qheads"], s["qheads"]],
                ["答案块（<details>）", t["details"], s["details"]],
                ["无解答占位", t["placeholders"], s["placeholders"]],
                ["Obsidian 图片", t["embeds"], s["embeds"]],
                ["媒体缺失图片", t["missing"], s["missing"]],
                ["非白名单行命中", t["block"], s["block"]],
                ["图片风险行", t["image_risks"], s["image_risks"]],
                ["标题粘连行", t["heading_glue"], s["heading_glue"]],
                ["知识点残块(疑似)行", t["kp_residual"], s["kp_residual"]],
                ["HTML <table>", t["tables"], s["tables"]],
                ["colspan/rowspan", f"{t['colspans']}/{t['rowspans']}", f"{s['colspans']}/{s['rowspans']}"],
            ],
        )
    )
    L.append("")

    L.append("## 二、非白名单教学块")
    L.append("")
    L.append("> 成书白名单：完整题目 / 完整解析 / 适当拓展 / 来源 / 知识点。")
    L.append("")
    labels = [label for label, _ in BLOCK_RULES]
    rows = []
    for label in labels:
        t_hits = sum(c["block_hits"][label] for c in teacher.values())
        s_hits = sum(c["block_hits"][label] for c in student.values())
        sample = ""
        for c in teacher.values():
            samples = c["block_samples"].get(label, [])
            if samples:
                rel, line_no, snippet = samples[0]
                sample = f"{rel}:{line_no}"
                break
        rows.append([label, t_hits, s_hits, sample])
    L.append(fmt_md_table(["块标记", "教师版行命中", "学生版行命中", "首个样例位置"], rows))
    L.append("")

    L.append("## 三、图片位置风险")
    L.append("")
    risk_labels = ["图贴分隔线", "同行多图", "表格单元格内图", "HTML-img残留", "图文同行"]
    rows = []
    for label in risk_labels:
        t_hits = sum(c["image_risks"][label] for c in teacher.values())
        s_hits = sum(c["image_risks"][label] for c in student.values())
        sample = ""
        for c in teacher.values():
            samples = c["image_risk_samples"].get(label, [])
            if samples:
                rel, line_no, snippet = samples[0]
                sample = f"{rel}:{line_no}"
                break
        rows.append([label, t_hits, s_hits, sample])
    L.append(fmt_md_table(["风险类别", "教师版", "学生版", "首个样例位置"], rows))
    L.append("")

    L.append("## 四、HTML 表格")
    L.append("")
    table_chapters = [
        c
        for c in teacher.values()
        if c["tables"] or c["colspans"] or c["rowspans"]
    ]
    table_chapters.sort(key=lambda c: -c["tables"])
    if table_chapters:
        rows = [
            [
                c["path"],
                c["tables"],
                c["colspans"],
                c["rowspans"],
                c["td_images"],
                c["br_in_tables"],
            ]
            for c in table_chapters
        ]
        L.append(
            fmt_md_table(
                ["章节", "HTML表", "colspan", "rowspan", "表格内图", "<br>"],
                rows,
            )
        )
    else:
        L.append("教师版无 HTML 表格残留。")
    L.append("")

    L.append("## 五、源文件→成书映射")
    L.append("")
    by_status = collections.Counter(r["mapping_status"] for r in mapping)
    by_fidelity = collections.Counter(
        (r["fidelity"] or "空").strip() for r in mapping
    )
    by_difficulty = collections.Counter(r["difficulty"] for r in mapping)
    no_answer = [r for r in mapping if not r["source_has_answer"]]
    no_img = sum(1 for r in mapping if r["image_count"] == 0)
    multi_img = sum(1 for r in mapping if r["image_count"] > 1)
    L.append(
        fmt_md_table(
            ["指标", "数值"],
            [
                ["映射记录数", len(mapping)],
                ["mapping_status=ok", by_status["ok"]],
                ["chapter_missing", by_status["chapter_missing"]],
                ["count_mismatch", by_status["count_mismatch"]],
                ["qno_missing", by_status["qno_missing"]],
                ["源文件无答案标记", len(no_answer)],
                ["成书题块 0 图", no_img],
                ["成书题块 >1 图", multi_img],
                [
                    "难度分布",
                    " ".join(
                        f"d{d}={by_difficulty[d]}" for d in sorted(by_difficulty)
                    ),
                ],
                [
                    "fidelity 分布",
                    " ".join(f"{k}={v}" for k, v in sorted(by_fidelity.items())),
                ],
            ],
        )
    )
    L.append("")
    L.append(f"> 映射清单（JSONL）：`{Path(args.mapping).name}`")
    L.append("")

    L.append("## 六、源文件图片归属清单")
    L.append("")
    if image_records is None:
        L.append("已按 `--no-image-context` 跳过。")
    else:
        by_bucket = collections.Counter(r["bucket"] for r in image_records)
        by_disposition = collections.Counter(r["disposition"] for r in image_records)
        by_kind = collections.Counter(r["kind"] for r in image_records)
        in_td = sum(1 for r in image_records if r["in_td"])
        multi = sum(1 for r in image_records if r["multi_image_line"])
        glued = sum(1 for r in image_records if r["glued_to_separator"])
        media_missing = sum(1 for r in image_records if not r["media_present"])
        repeat_total = sum(1 for r in image_records if r.get("cross_question_repeat"))
        repeat_by_bucket = collections.Counter(
            r["bucket"] for r in image_records if r.get("cross_question_repeat")
        )
        repeat_desc = " ".join(
            f"{b}={repeat_by_bucket.get(b, 0)}" for b in BUCKET_ORDER if repeat_by_bucket.get(b, 0)
        )
        L.append(
            fmt_md_table(
                ["指标", "数值"],
                [
                    ["源文件图片记录", len(image_records)],
                    [
                        "区块分布",
                        " ".join(
                            f"{b}={by_bucket.get(b, 0)}"
                            for b in BUCKET_ORDER
                            if by_bucket.get(b, 0)
                        ),
                    ],
                    [
                        "最终处置",
                        " ".join(
                            f"{k}={by_disposition.get(k, 0)}"
                            for k in ["保留", "应删除", "待人工"]
                        ),
                    ],
                    ["Obsidian 嵌入 / HTML <img>", f"{by_kind.get('obsidian', 0)} / {by_kind.get('html_img', 0)}"],
                    ["表格单元格内图", in_td],
                    ["同行多图", multi],
                    ["贴分隔线（---![[）", glued],
                    ["媒体仓库缺失", media_missing],
                    ["跨题重复图（疑装饰/页眉）", f"{repeat_total}（{repeat_desc}）"],
                ],
            )
        )
        L.append("")
        L.append(f"> 图片归属清单（JSONL）：`{Path(args.image_context).name}`")
        L.append("")
        rows = []
        for bucket in BUCKET_ORDER:
            hits = [r for r in image_records if r["bucket"] == bucket]
            if not hits:
                continue
            rows.append([bucket, len(hits), f"{hits[0]['source_path']}:{hits[0]['line']}"])
        L.append(fmt_md_table(["区块", "图片数", "首个样例位置"], rows))
        L.append("")
        del_rows = [r for r in image_records if r["disposition"] == "应删除"]
        del_rows.sort(key=lambda r: (r["source_path"], r["line"]))
        if del_rows:
            L.append(f"### 应删除图片样例（前 10 条）")
            L.append("")
            rows = [
                [
                    r["source_path"],
                    r["line"],
                    r["bucket"],
                    r["kind"],
                    f"`{r['line_snippet']}`",
                ]
                for r in del_rows[:10]
            ]
            L.append(fmt_md_table(["源文件", "行号", "区块", "类型", "片段"], rows))
            L.append("")
        review_rows = [r for r in image_records if r["disposition"] == "待人工"]
        review_rows.sort(key=lambda r: (r["source_path"], r["line"]))
        if review_rows:
            L.append("### 待人工图片样例（前 10 条）")
            L.append("")
            L.append(
                "> 教学块（解题思路/易错分析/相关图片/题干图示/扩展块）中可能藏着原题必需图，"
                "Phase 2 逐个确认后再决定移入题干/解析或删除；跨题重复图优先按装饰图核验。"
            )
            L.append("")
            rows = [
                [
                    r["source_path"],
                    r["line"],
                    r["bucket"],
                    r["kind"],
                    str(r.get("repeat_files", 1)),
                    f"`{r['line_snippet']}`",
                ]
                for r in review_rows[:10]
            ]
            L.append(
                fmt_md_table(
                    ["源文件", "行号", "区块", "类型", "跨题文件数", "片段"],
                    rows,
                )
            )
            L.append("")

    L.append("## 七、Word 预检")
    L.append("")
    if precheck:
        err, warn, note = precheck
        if err is not None:
            L.append(f"- 教师版：ERROR={err} WARN={warn}")
        else:
            L.append(f"- 教师版：{note}")
    else:
        L.append("- 已按 `--no-precheck` 跳过。")
    L.append("")

    L.append("## 八、逐章明细（教师版）")
    L.append("")
    rows = []
    for rel in sorted(teacher):
        c = teacher[rel]
        rows.append(
            [
                c["path"],
                c["declared"],
                len(c["qheads"]),
                c["details"],
                len(c["embeds"]),
                len(c["missing"]),
                sum(c["block_hits"].values()),
                sum(c["image_risks"].values()),
                c["kp_residual_lines"],
                len(c["heading_glue"]),
                c["tables"],
                f"{c['colspans']}/{c['rowspans']}",
            ]
        )
    L.append(
        fmt_md_table(
            ["章节", "题数", "题头", "答案块", "图片", "缺失", "非白名单行", "图片风险行", "知识点残块(疑似)", "标题粘连", "HTML表", "span"],
            rows,
        )
    )
    L.append("")

    def sample_section(title, samples):
        L.append(f"## {title}")
        L.append("")
        if not samples:
            L.append("无。")
            L.append("")
            return
        rows = []
        for rel, line_no, snippet in samples:
            rows.append([rel, line_no, f"`{snippet}`"])
        L.append(fmt_md_table(["文件", "行号", "片段"], rows))
        L.append("")

    L.append("## 九、抽样明细")
    L.append("")
    all_block_samples = {}
    all_image_samples = {}
    for c in teacher.values():
        for label, samples in c["block_samples"].items():
            all_block_samples.setdefault(label, []).extend(samples)
        for label, samples in c["image_risk_samples"].items():
            all_image_samples.setdefault(label, []).extend(samples)
    for label in labels:
        sample_section(f"教学块样例 · {label}", all_block_samples.get(label, [])[:5])
    for label in risk_labels:
        sample_section(f"图片风险样例 · {label}", all_image_samples.get(label, [])[:5])
    glue = []
    for c in teacher.values():
        glue.extend(c["heading_glue"])
    sample_section("标题粘连样例", glue[:5])
    kp_residual = []
    for c in teacher.values():
        kp_residual.extend(c["kp_residual_samples"])
    sample_section("知识点残块(疑似)样例", kp_residual[:5])

    return "\n".join(L).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(VAULT_ROOT / "04-课件/习题集/习题书-教师版"))
    ap.add_argument("--media-root", default=str(VAULT_ROOT / "媒体仓库"))
    ap.add_argument("--source-root", default=str(VAULT_ROOT / "04-题库"))
    ap.add_argument(
        "--report",
        default=str(VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2基线.md"),
    )
    ap.add_argument(
        "--mapping",
        default=str(VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-source-map.jsonl"),
    )
    ap.add_argument(
        "--image-context",
        default=str(VAULT_ROOT / "09-审计报告/2026-08-30-习题书V2-图片归属清单.jsonl"),
    )
    ap.add_argument("--no-image-context", action="store_true")
    ap.add_argument("--limit-samples", type=int, default=5)
    ap.add_argument("--no-precheck", action="store_true")
    args = ap.parse_args()

    # 生成器使用相对路径（BASE=04-题库），审计脚本统一从 vault 根运行。
    os.chdir(VAULT_ROOT)
    root = Path(args.root).resolve()
    media_root = Path(args.media_root).resolve()
    source_root = Path(args.source_root).resolve()
    if not root.is_dir():
        raise SystemExit(f"成书目录不存在: {root}")
    if not media_root.is_dir():
        raise SystemExit(f"媒体仓库不存在: {media_root}")
    if not source_root.is_dir():
        raise SystemExit(f"源题库目录不存在: {source_root}")

    if "学生版" in root.name:
        teacher_root = root.with_name(root.name.replace("学生版", "教师版"))
        student_root = root
    else:
        teacher_root = root
        student_root = root.with_name(root.name.replace("教师版", "学生版"))
    if not teacher_root.is_dir():
        raise SystemExit(f"教师版目录不存在: {teacher_root}")
    if not student_root.is_dir():
        raise SystemExit(f"学生版目录不存在: {student_root}")

    builder = load_builder()
    chapters = {}
    for path in collect_chapters(teacher_root):
        info = scan_chapter(path, teacher_root, media_root)
        chapters[info["path"]] = info

    student = {}
    for path in collect_chapters(student_root):
        info = scan_chapter(path, student_root, media_root)
        student[info["path"]] = info

    mapping = build_mapping(builder, source_root, chapters)

    precheck = None
    if not args.no_precheck:
        precheck = run_precheck(teacher_root)

    image_records = None
    if not args.no_image_context:
        image_records = scan_source_images(source_root, media_root, mapping)

    report = render_report(args, chapters, student, mapping, precheck, image_records)
    report_path = Path(args.report).resolve()
    mapping_path = Path(args.mapping).resolve()
    image_context_path = Path(args.image_context).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8", newline="")
    with mapping_path.open("w", encoding="utf-8", newline="") as f:
        for rec in mapping:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    if image_records is not None:
        image_context_path.parent.mkdir(parents=True, exist_ok=True)
        with image_context_path.open("w", encoding="utf-8", newline="") as f:
            for rec in image_records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"report: {report_path}")
    print(f"mapping: {mapping_path}")
    if image_records is not None:
        print(f"image_context: {image_context_path}")
    print(
        f"questions={sum(c['declared'] for c in chapters.values())} "
        f"qheads={sum(len(c['qheads']) for c in chapters.values())} "
        f"details={sum(c['details'] for c in chapters.values())} "
        f"images={sum(len(c['embeds']) for c in chapters.values())} "
        f"missing={sum(len(c['missing']) for c in chapters.values())} "
        f"block_hits={sum(sum(c['block_hits'].values()) for c in chapters.values())} "
        f"image_risks={sum(sum(c['image_risks'].values()) for c in chapters.values())} "
        f"tables={sum(c['tables'] for c in chapters.values())} "
        f"mapping={len(mapping)}"
    )
    if image_records is not None:
        print(f"image_context={len(image_records)}")
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    raise SystemExit(main())
