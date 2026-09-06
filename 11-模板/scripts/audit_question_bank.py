#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_question_bank.py — 题库专项深度审计

背景：validate_kb.py 的 REQUIRED_FIELDS 未收录 type=题目，
      因此题库的「六字段必填」等规范长期处于零校验状态。本脚本补齐。

检查维度：
  A. frontmatter：YAML 可解析 / BOM / 六字段 / 枚举值 / status
  B. 链接：knowledge_points / depends_on / cross_references 断链
  C. 图片：![[...]] 是否存在
  D. 内容：题干缺失 / 答案缺失或占位 / 答案过短
  E. 成书兼容格式：单行紧凑 / HTML 标签 / 高危宏 / 半截 math / 裸下标 / 重复反斜杠
  F. 重复：title 重复 / 正文重复
  G. 命名规范：按来源库正则抽查

用法:
    python audit_question_bank.py                 # 全量
    python audit_question_bank.py --dir 04-题库/化学原理
输出:
    09-审计报告/YYYY-MM-DD-题库全面审计.md
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() in ("gbk", "gb2312"):
    sys.stderr.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required.", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT = SCRIPT_DIR.parent.parent

# 复用 validate_kb 的 Obsidian 三级链接解析器（路径 → basename → title/aliases），
# 与知识库主校验器保持同一口径；导入失败时降级为脚本内置解析器。
sys.path.insert(0, str(SCRIPT_DIR))
try:
    import validate_kb as _VKB
except Exception:
    _VKB = None
REPORT_DIR = VAULT / "09-审计报告"

# ── 扫描范围 ────────────────────────────────────────────────
TARGET_DIRS = ["04-题库", "05-真题库"]
SKIP_DIR_PARTS = {".obsidian", ".git", "node_modules", "__pycache__", "09-AI工作区", ".chem_media"}

# ── 规范常量（来源：04-题库/新题入库SOP.md v1.1）────────────
SIX_FIELDS = ["fidelity", "difficulty", "exam_stage", "subject_module", "pack", "knowledge_points"]
ENUM = {
    "fidelity": ["原书逐字", "原书改写", "自编"],
    "exam_stage": ["初赛", "决赛", "省预赛"],
    "subject_module": ["化学原理", "结构化学", "有机化学", "元素与分析"],
    "pack": ["章节练习", "模块习题集", "综合模拟卷", "预赛专项"],
}
ALLOWED_STATUS = ["draft", "review", "published", "已入库", "已填充", "已补全答案",
                  "deprecated", "待审核", "待填充"]

# ── 只有这些 type 视为「题」，其余（系统/索引/答案/横向对比）不计入题库缺陷 ──
QUESTION_TYPES = {"题目", "真题", "例题", "题组", "题目集"}

# ── 命名规范（来源：SOP 1.1）────────────────────────────────
NAME_RULES = {
    "教材习题/化学竞赛初赛讲义": r"^题-\d{3}-初赛讲义-.+-习题\d+(\.\d+)?$",
    "教材习题/ABOC": r"^题-\d{3}-ABOC-(?:Ch\d+|FT[01])-.+",
    "教材习题/Clayden": r"^题-\d{3}-Clayden-Ch\d+-P\d+-.+",
    "教材习题/上海中学竞赛课程": r"^题-\d{3}-上海中学-.+-习题\d+",
    "教材习题/赵鑫光": r"^题-赵鑫光-.+",
    "教材习题/汇智竞赛题目": r"^题-汇智-.+",
    "教材习题/结构化学基础": r"^题-\d{3}-结构化学基础-.+",
    "化学原理/": r"^\d{2}-\d{2}$",
}

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".tif", ".tiff"}
IMG_REF_RE = re.compile(r"!\[\[([^\]]+)\]\]")
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_TAG_RE = re.compile(r"<(img|table|tr|td|th|div|span|br|p)\b", re.I)
BAD_MACRO_RE = re.compile(r"\\xlongequal|\\AA\b|\\Biggl|\\xrightleftharpoons")
DBL_BS_RE = re.compile(r"\\\\\\\\")          # 文本里真实出现 4 个反斜杠
STD_DEG_RE = re.compile(r"(?<![0-9])°(?!C|F|M)")  # 非温度/非角度的标准态误用
INLINE_MATH_RE = re.compile(r"\$([^$\n]+)\$")


# ══════════════════════════════════════════════════════════════
#  索引
# ══════════════════════════════════════════════════════════════
def build_md_index() -> dict[str, list[Path]]:
    idx: dict[str, list[Path]] = defaultdict(list)
    for f in VAULT.rglob("*.md"):
        parts = set(f.parts)
        if parts & SKIP_DIR_PARTS:
            continue
        idx[f.stem.lower()].append(f)
    return idx


def build_label_index() -> dict[str, list[Path]]:
    """title / aliases → 文件（Obsidian 三级解析的第 3 级）。
    只解析 03-知识点 与 08-术语与卡片，避免全库 7k 文件的解析开销。"""
    idx: dict[str, list[Path]] = defaultdict(list)
    for base in ("03-知识点", "08-术语与卡片", "04-专题与题型"):
        root = VAULT / base
        if not root.exists():
            continue
        for f in root.rglob("*.md"):
            try:
                fm, _ = strip_fm(f.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                continue
            for field in ("title", "aliases", "syllabus_code"):
                v = fm.get(field)
                if isinstance(v, str):
                    vals = [x.strip().strip('"').strip("'")
                            for x in v.strip()[1:-1].split(",")] if v.strip().startswith("[") else [v]
                elif isinstance(v, list):
                    vals = [str(x) for x in v]
                else:
                    continue
                for s in vals:
                    s = s.strip()
                    if s:
                        idx[s.lower()].append(f)
    return idx


def build_image_index() -> dict[str, list[Path]]:
    idx: dict[str, list[Path]] = defaultdict(list)
    for f in VAULT.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in IMAGE_EXT:
            continue
        if set(f.parts) & SKIP_DIR_PARTS:
            continue
        idx[f.name.lower()].append(f)
    return idx


def resolve_link(target, src, md_idx, label_idx=None):
    """按 Obsidian 规则解析 wikilink：
    1) 路径（库根 / 相对当前目录）  2) 末段 basename  3) title/aliases 标签"""
    t = target.replace("\\", "/").strip().strip("/")
    if not t:
        return True
    # 优先用主校验器的三级解析器（口径一致）
    if _VKB is not None:
        n = _VKB.normalize_wikilink_target(t)
        if not n or _VKB.is_placeholder_target(n):
            return True
        return _VKB.find_wikilink_target(n, VAULT) is not None
    # 降级：脚本内置解析
    for cand in (VAULT / t, VAULT / (t + ".md"), src.parent / t, src.parent / (t + ".md")):
        if cand.is_file():
            return True
    if Path(t).stem.lower() in md_idx:
        return True
    if label_idx is not None and Path(t).stem.lower() in label_idx:
        return True
    return False


def resolve_image(target: str, src: Path, img_idx: dict[str, list[Path]]) -> bool:
    """按 Obsidian 规则解析 ![[...]]：basename 优先（全局附件库）→ 路径 → 相对目录。"""
    t = target.replace("\\", "/").strip()
    if not t:
        return True
    base = Path(t).name.lower()
    if base in img_idx:
        return True
    for cand in (VAULT / t, VAULT / "媒体仓库" / t, VAULT / "media" / t, src.parent / t):
        if cand.is_file():
            return True
    return False


def strip_fm(text: str):
    t = text.lstrip("\ufeff")
    if not t.startswith("---"):
        return {}, t
    end = t.find("\n---", 3)
    if end == -1:
        return {}, t
    block = t[3:end].strip("\n")
    body = t[end + 4:]
    try:
        fm = yaml.safe_load(block)
        if not isinstance(fm, dict):
            return {}, body
        return fm, body
    except yaml.YAMLError as e:
        return {"__yaml_error__": str(e).split("\n")[0]}, body


# ══════════════════════════════════════════════════════════════
#  审计
# ══════════════════════════════════════════════════════════════
class R:
    def __init__(self):
        self.rows = []          # (level, dir, file, dim, detail)
        self.n = 0
        self.skipped = 0
        self.skipped_types = defaultdict(int)
        self.by_type = defaultdict(int)
        self.by_dir = defaultdict(lambda: defaultdict(int))
        self.titles = defaultdict(list)
        self.hashes = defaultdict(list)
        self.dir_total = defaultdict(int)
        self.dir_six_ok = defaultdict(int)
        self.has_answer = 0
        self.no_answer = 0
        self.placeholder_answer = 0
        self.ext_answer = 0
        self.short_answer = 0
        self.sub = Counter()   # E 维度子类型计数

    def add(self, level, d, f, dim, detail):
        self.rows.append((level, d, f, dim, detail))


def norm_dir(rel: str) -> str:
    """归一到「来源库」粒度：04-题库/教材习题/Clayden/xxx.md → 教材习题/Clayden"""
    p = rel.split("/")
    if len(p) >= 3 and p[1] in ("教材习题", "真题"):
        return "/".join(p[:3])
    if len(p) >= 2:
        return "/".join(p[:2])
    return rel


# 宽口径答案标记（2026-08-31 修正：原规则漏掉 `> **答案**：` 引用块与【答案】格式，虚报约 500 处）
ANSWER_OPEN_RE = re.compile(
    r"<details"
    r"|#{1,6}\s*(参考答案|答案|解答|解析|答案解析|答案与解析|答案及解析|参考答案与解析)\s*[:：]?"
    r"|>\s*\*{0,2}(参考答案|答案|解答|解析)\*{0,2}\s*[:：]"
    r"|\*{1,2}(参考答案|答案|解答|解析)\*{0,2}\s*[:：]"
    r"|【(参考答案|答案)】|^答案\s*[:：]",
    re.M | re.I)
EXT_ANSWER_RE = re.compile(r"答案见|见答案|答案详见|解答见|答案位于|答案在|参考答案见|解答(请|均)?见|请见")
placeholder_re = re.compile(r"原书未提供|未提供解答|未提供答案|答案略|无答案|见原书|（略|略，见")
# 合法短答案：选择题（**答案：A**）、纯选项、数值结果、点群记号、加粗选项 **(A)**
short_answer_ok_re = re.compile(r"答案\s*[:：]|应选择|选\s*[A-E]|^[A-Ea-e、，,\s\d\.\-]+$|\*{1,2}\s*\([A-Ea-e]\)\s*\*{0,2}")
# 内嵌解答：题目与答案合写（“题目与答案”小节 / 加粗“解” / “解析：” / 知识卡自含结论）
EMBEDDED_ANSWER_RE = re.compile(r"题目与答案|^解\s*[:：]|\*\*解\*\*|#{1,6}\s*解\s*[:：]?|解答|解析\s*[:：]|结论\s*[:：]|解得|两类原因|原因如下|核心原则|速查表")


def audit_file(path: Path, r: R, md_idx, img_idx, label_idx) -> None:
    rel = path.relative_to(VAULT).as_posix()
    d = norm_dir(rel)

    raw = path.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8", errors="replace")
    fm, body = strip_fm(text)

    # ── A. frontmatter ────────────────────────────────────
    if "__yaml_error__" in fm:
        r.add("P0", d, rel, "A-frontmatter", f"YAML 解析失败：{fm['__yaml_error__']}")
        fm = {}
    if has_bom:
        r.add("P1", d, rel, "A-frontmatter", "文件含 BOM")
    if not fm:
        r.add("P0", d, rel, "A-frontmatter", "无 frontmatter")
        return

    ftype = str(fm.get("type", "")).strip()
    r.by_type[ftype or "(空)"] += 1
    if ftype == "题组":
        # 题组是题目组 schema（含 question_count 等），不套用单题六字段
        r.skipped += 1
        return
    if ftype not in QUESTION_TYPES:
        # 索引/系统/答案/横向对比类文件不是题目，不按题库规范审计
        r.skipped += 1
        r.skipped_types[ftype or "(空)"] += 1
        return
    r.dir_total[d] += 1

    missing = [k for k in SIX_FIELDS if fm.get(k) in (None, "", [])]
    if missing:
        lvl = "P0" if len(missing) >= 4 else ("P1" if len(missing) >= 2 else "P2")
        r.add(lvl, d, rel, "A-六字段", f"缺 {len(missing)}/6：{','.join(missing)}")
    else:
        r.dir_six_ok[d] += 1

    for k, allowed in ENUM.items():
        v = fm.get(k)
        if v in (None, "", []):
            continue
        # 多值合法写法：exam_stage="初赛/决赛"（按 / 拆分，每项须在允许列表）
        parts = [p.strip() for p in str(v).split("/") if p.strip()]
        if parts and all(p in allowed for p in parts):
            continue
        r.add("P1", d, rel, "A-枚举", f"{k}='{v}' 不在 {allowed}")

    diff = fm.get("difficulty")
    if diff is not None:
        s = str(diff).strip()
        ok = False
        try:
            if re.fullmatch(r"\d+", s) and 1 <= int(s) <= 5:
                ok = True
            elif re.fullmatch(r"\d+-\d+", s):  # 区间写法（题组/合集难度范围）
                a, b = (int(x) for x in s.split("-"))
                ok = 1 <= a <= b <= 5
        except (TypeError, ValueError):
            ok = False
        if not ok:
            r.add("P1", d, rel, "A-枚举", f"difficulty='{diff}' 非 1-5 整数或合法区间")

    st = fm.get("status")
    if st is not None and st not in ALLOWED_STATUS:
        r.add("P2", d, rel, "A-枚举", f"status='{st}' 不在允许列表")

    # ── B. 链接 ───────────────────────────────────────────
    for field in ("knowledge_points", "depends_on", "cross_references", "related"):
        vals = fm.get(field)
        if isinstance(vals, str):
            vals = [vals]
        if not isinstance(vals, list):
            continue
        for v in vals:
            if not isinstance(v, str):
                continue
            for tgt in re.findall(r"\[\[([^\]|#]+)", v):
                tgt = tgt.strip()
                if not tgt:
                    continue
                if not resolve_link(tgt, path, md_idx, label_idx):
                    r.add("P1", d, rel, "B-断链", f"{field} → [[{tgt}]] 不存在")
    kp = fm.get("knowledge_points")
    if isinstance(kp, list) and len(kp) == 0:
        r.add("P1", d, rel, "B-链接", "knowledge_points 为空列表")

    # ── C. 图片 ───────────────────────────────────────────
    seen_bad_img = set()
    for m in IMG_REF_RE.finditer(body):
        tgt = m.group(1).split("|")[0].strip()
        if "#" in tgt or "*" in tgt or "{" in tgt:
            continue
        if tgt in seen_bad_img:
            continue
        if not resolve_image(tgt, path, img_idx):
            seen_bad_img.add(tgt)
            r.sub['wiki 图缺失'] += 1
            r.add("P1", d, rel, "C-图片", f"![[{tgt}]] 全库不存在")
    for m in MD_IMG_RE.finditer(body):
        r.add("P2", d, rel, "C-图片", f"Markdown 图片语法 ![]({m.group(1)[:60]})，应改 ![[...]]")

    # ── D. 内容 ───────────────────────────────────────────
    plain = re.sub(r"!\[\[[^\]]+\]\]", "", body)
    plain = re.sub(r"\s+", "", plain)
    if len(plain) < 50:
        r.add("P0", d, rel, "D-题干", f"正文过短（{len(plain)} 字符），疑似题干缺失")
    # 宽口径答案标记：<details> / 各级标题 / > **答案**： 引用块 / **答案**：粗体 / 【答案】
    if ftype == "题目集":
        pass  # 题目集是存档/集合，不强制单题答案块
    else:
        m = ANSWER_OPEN_RE.search(body)
        ext_m = EXT_ANSWER_RE.search(body)
        if ext_m and m is None:
            # 答案外置到独立答案文件（答案见 [[...]]）
            r.ext_answer += 1
        elif m:
            ans = body[m.end():]
            ans = re.sub(r"<summary>.*?</summary>", "", ans, flags=re.S)
            ans = re.sub(r"</?details>", "", ans)
            ans = re.sub(r"\s+", "", ans)
            if placeholder_re.search(ans[:60]) or len(ans) < 5:
                # 已明确标注「原书未提供解答」「（略，见源文件解析）」等
                r.placeholder_answer += 1
                r.add("P1", d, rel, "D-答案", f"答案缺失（已标注）：{ans[:24]}")
            elif len(ans) < 30:
                if short_answer_ok_re.search(ans) or "```" in ans:
                    # 选择题答案（**答案：A**）／数值答案／代码块——合法短答案
                    r.short_answer += 1
                else:
                    r.no_answer += 1
                    r.add("P2", d, rel, "D-答案", f"答案过短待确认（{len(ans)} 字符）：{ans[:24]}")
            else:
                r.has_answer += 1
        elif re.search(r"答案见|答案详见|见答案|答案位于|解答见", body):
            # 答案外置到独立答案文件（初赛讲义等来源的合法模式）
            m2 = re.search(r"\[\[([^\]|#]+)", body[body.find("答案见") if "答案见" in body else 0:])
            if m2 and resolve_link(m2.group(1), path, md_idx, label_idx):
                r.ext_answer += 1
            else:
                r.no_answer += 1
                r.add("P1", d, rel, "D-答案", "外链答案目标不可解析")
        else:
            # 内嵌解答（题目与答案合写、解引导、知识卡自含）且正文充分 → 视为合法
            if EMBEDDED_ANSWER_RE.search(body) and len(plain) > 200:
                r.has_answer += 1
            else:
                r.no_answer += 1
                r.add("P1", d, rel, "D-答案", "无答案块（无 <details>/## 参考答案/答案见）")

    # ── E. 成书兼容格式 ───────────────────────────────────
    for line in body.split("\n"):
        if len(re.findall(r"(?m)(^|\s)#{2,6}\s", line)) >= 2 or re.search(r"##[^#\n]*##", line):
            r.sub['单行紧凑格式'] += 1
            r.add("P1", d, rel, "E-格式", "单行紧凑格式（多个 ## 标题挤在一行）")
            break
    tags = sorted(set(HTML_TAG_RE.findall(body)))
    if tags:
        r.add("P2", d, rel, "E-格式",
              f"含 HTML 标签 {'/'.join('<' + t + '>' for t in tags)}（SOP 8.3 禁用）")
        r.sub['HTML 标签 ' + '/'.join(tags)] += 1
    if BAD_MACRO_RE.search(body):
        r.sub['不友好宏 xlongequal/AA/Biggl'] += 1
        r.add("P2", d, rel, "E-公式", "含 texmath 不友好宏（xlongequal/AA/Biggl 等）")
    if DBL_BS_RE.search(body):
        r.sub['翻倍反斜杠 \\\\\\\\（OCR 残留）'] += 1
        r.add("P2", d, rel, "E-公式", "含翻倍反斜杠 \\\\\\\\（OCR 残留）")
    n_deg = len(re.findall(r"(?<=[HGSEK])°", body))
    if n_deg:
        r.sub['标准态误用 °'] += 1
        r.add("P2", d, rel, "E-公式", f"标准态误用 ° （{n_deg} 处），应为 θ")
    # 半截 math：仅提示不含字母的纯上标/下标（同位素/谱项等含字母者为合法记号）
    bad_math = [s for s in INLINE_MATH_RE.findall(body)
                if s.strip().startswith(("^", "_")) and len(s.strip()) <= 6
                and not re.match(r"[\\^_][^\\^_]*[A-Za-z]", s.strip())]
    if bad_math:
        r.sub['分裂记号（需抽查）'] += 1
        r.add("P2", d, rel, "E-公式", f"疑似分裂记号（Word管线需抽查）：{' / '.join('$' + b + '$' for b in bad_math[:3])}")
    if body.count("$") % 2:
        r.sub['$ 奇数（公式未闭合）'] += 1
        r.add("P2", d, rel, "E-公式", "$ 数量为奇数，行内公式可能未闭合")
    for line in body.split("\n"):
        if line.strip().startswith("|") and "![[" in line:
            r.sub['表格内嵌图片'] += 1
            r.add("P2", d, rel, "E-格式", "图片写进表格单元格（SOP 8.2 禁用）")
            break

    # ── F. 重复 ───────────────────────────────────────────
    title = str(fm.get("title", "")).strip()
    if title:
        r.titles[title].append(rel)
    h = hashlib.md5(plain.encode("utf-8")).hexdigest()
    if len(plain) > 80:
        r.hashes[h].append(rel)

    # ── G. 命名 ───────────────────────────────────────────
    for prefix, pat in NAME_RULES.items():
        if rel.startswith("04-题库/" + prefix):
            stem = path.stem
            if not re.match(pat, stem):
                r.add("P2", d, rel, "G-命名", f"文件名 '{stem}' 不符合 {prefix} 规范")
            break


# ══════════════════════════════════════════════════════════════
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", nargs="*", default=None)
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    dirs = args.dir or TARGET_DIRS
    files: list[Path] = []
    for d in dirs:
        root = VAULT / d
        if not root.exists():
            print(f"  ⚠ 目录不存在: {d}", file=sys.stderr)
            continue
        for f in sorted(root.rglob("*.md")):
            if set(f.relative_to(VAULT).parts) & SKIP_DIR_PARTS:
                continue
            files.append(f)

    print(f"🔍 题库专项审计 · 受检 {len(files)} 文件", file=sys.stderr)
    md_idx = build_md_index()
    label_idx = build_label_index()
    img_idx = build_image_index()
    print(f"   索引：{len(md_idx)} 个 md / {len(img_idx)} 张图片", file=sys.stderr)

    r = R()
    for f in files:
        try:
            audit_file(f, r, md_idx, img_idx, label_idx)
        except Exception as e:
            r.add("P0", norm_dir(f.relative_to(VAULT).as_posix()),
                  f.relative_to(VAULT).as_posix(), "扫描异常", str(e)[:100])

    # ── 汇总 ──────────────────────────────────────────────
    lv = defaultdict(int)
    dim = defaultdict(int)
    for level, d, f, dm, det in r.rows:
        lv[level] += 1
        dim[dm] += 1

    dup_titles = {k: v for k, v in r.titles.items() if len(v) > 1}
    dup_body = {k: v for k, v in r.hashes.items() if len(v) > 1}

    lines = []
    today = datetime.date.today().isoformat()
    lines.append(f"# 题库专项审计报告 · {today}")
    lines.append("")
    lines.append(f"> **范围**：{' / '.join(dirs)}　**受检文件**：{len(files)}")
    lines.append(f"> **依据**：[[04-题库/新题入库SOP]] v1.1 · [[04-题库/习题集体系总纲]] v1.1")
    lines.append(f"> **工具**：`11-模板/scripts/audit_question_bank.py`")
    lines.append(f"> **实际审计题数**：{sum(r.dir_total.values())}（另有 {r.skipped} 个非题目文件："
                 + "、".join(f"{k}×{v}" for k, v in sorted(r.skipped_types.items(), key=lambda x: -x[1]))
                 + "，不计入缺陷）")
    lines.append("")
    lines.append("## 一、总览")
    lines.append("")
    lines.append("| 级别 | 数量 |")
    lines.append("|:--|--:|")
    for k in ("P0", "P1", "P2"):
        lines.append(f"| {k} | {lv.get(k, 0)} |")
    lines.append(f"| **合计** | **{sum(lv.values())}** |")
    lines.append("")
    lines.append("### 按维度")
    lines.append("")
    lines.append("| 维度 | 数量 |")
    lines.append("|:--|--:|")
    for k, v in sorted(dim.items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |")
    lines.append("")

    lines.append("### type 分布")
    lines.append("")
    lines.append("| type | 数量 |")
    lines.append("|:--|--:|")
    for k, v in sorted(r.by_type.items(), key=lambda x: -x[1])[:12]:
        lines.append(f"| `{k}` | {v} |")
    lines.append("")

    lines.append("### 答案覆盖")
    lines.append("")
    lines.append(f"- 有效答案：**{r.has_answer}**")
    lines.append(f"- 缺失/过短：**{r.no_answer}**")
    lines.append(f"- 占位答案：**{r.placeholder_answer}**")
    lines.append(f"- 外链答案（合法）：**{r.ext_answer}**")
    lines.append(f"- 合法短答案（选择题/数值）：**{r.short_answer}**")
    lines.append("")

    lines.append("## 二、各来源库六字段合规率")
    lines.append("")
    lines.append("| 来源库 | 题数 | 六字段齐全 | 合规率 |")
    lines.append("|:--|--:|--:|--:|")
    for d in sorted(r.dir_total, key=lambda x: -r.dir_total[x]):
        tot = r.dir_total[d]
        ok = r.dir_six_ok.get(d, 0)
        pct = f"{ok / tot * 100:.0f}%" if tot else "—"
        flag = "" if tot == ok else (" 🔴" if ok == 0 else " 🟡")
        lines.append(f"| {d} | {tot} | {ok} | {pct}{flag} |")
    lines.append("")

    # 明细（按维度分组，截断）
    by_dim = defaultdict(list)
    for level, d, f, dm, det in r.rows:
        by_dim[dm].append((level, d, f, det))

    lines.append("### 问题子类型（按出现文件数）")
    lines.append("")
    lines.append("| 子类型 | 文件数 |")
    lines.append("|:--|--:|")
    for k, v in r.sub.most_common(20):
        lines.append(f"| {k} | {v} |")
    lines.append("")

    lines.append("### 维度 × 来源库 分布（问题最集中的库）")
    lines.append("")
    lines.append("| 维度 | 来源库 | 数量 |")
    lines.append("|:--|:--|--:|")
    dim_dir = defaultdict(lambda: defaultdict(int))
    for level, d, f, dm, det in r.rows:
        dim_dir[dm][d] += 1
    for dm in sorted(dim_dir, key=lambda x: -sum(dim_dir[x].values())):
        tops = sorted(dim_dir[dm].items(), key=lambda x: -x[1])[:6]
        for i, (d, n) in enumerate(tops):
            lines.append(f"| {dm if i == 0 else ''} | {d} | {n} |")
    lines.append("")

    lines.append("## 三、问题明细")
    lines.append("")
    order = sorted(by_dim, key=lambda x: -len(by_dim[x]))
    for dm in order:
        items = by_dim[dm]
        lines.append(f"### {dm}（{len(items)} 处）")
        lines.append("")
        lines.append("| 级别 | 来源库 | 文件 | 详情 |")
        lines.append("|:--|:--|:--|:--|")
        for level, d, f, det in items[:args.top]:
            short = f.split("/")[-1]
            lines.append(f"| {level} | {d} | `{short}` | {det} |")
        if len(items) > args.top:
            lines.append(f"| … | | | 还有 {len(items) - args.top} 处 |")
        lines.append("")

    p0rows = [x for x in r.rows if x[0] == "P0"]
    lines.append("## 四、P0 全量清单（阻塞性）")
    lines.append("")
    if p0rows:
        lines.append("| 来源库 | 文件 | 维度 | 详情 |")
        lines.append("|:--|:--|:--|:--|")
        for level, d, f, dm, det in p0rows[:200]:
            lines.append(f"| {d} | `{f.split('/')[-1]}` | {dm} | {det} |")
        if len(p0rows) > 200:
            lines.append(f"| … | | | 还有 {len(p0rows) - 200} 条 |")
    else:
        lines.append("无。")
    lines.append("")

    lines.append("## 五、重复检测")
    lines.append("")
    lines.append(f"- **title 重复**：{len(dup_titles)} 组")
    lines.append(f"- **正文完全重复**：{len(dup_body)} 组")
    lines.append("")
    if dup_titles:
        lines.append("| title | 文件数 | 样例 |")
        lines.append("|:--|--:|:--|")
        for t, v in sorted(dup_titles.items(), key=lambda x: -len(x[1]))[:args.top]:
            lines.append(f"| {t[:60]} | {len(v)} | `{v[0].split('/')[-1]}` |")
        lines.append("")
    if dup_body:
        lines.append("| 重复组 | 文件 |")
        lines.append("|:--|:--|")
        for i, (h, v) in enumerate(sorted(dup_body.items(), key=lambda x: -len(x[1]))[:args.top], 1):
            names = " ｜ ".join(f"`{x.split('/')[-1]}`" for x in v[:4])
            lines.append(f"| #{i}（{len(v)} 份） | {names} |")
        lines.append("")

    lines.append("---")
    lines.append(f"*自动生成于 {today} · audit_question_bank.py*")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / f"{today}-题库全面审计.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    print(f"\n📊 P0={lv.get('P0',0)}  P1={lv.get('P1',0)}  P2={lv.get('P2',0)}", file=sys.stderr)
    print(f"📄 {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
