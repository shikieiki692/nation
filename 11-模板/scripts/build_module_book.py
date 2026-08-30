import os, re, sys, io, collections
from datetime import date
from collections import Counter

# 通用模块习题书生成器
BASE = "04-题库"
TODAY = date.today().isoformat()

# 个别源文件 subject_module 写错但路径/module 字段可靠；生成阶段先路由，不擅改源库
PATH_SUBJECT_MODULE_OVERRIDES = {
    "分析化学/络合滴定与重量分析/返滴定法测铝.md": "元素与分析",
    # 29届初赛第6题同一大题被误拆：6-3 的 subject_module 误标为元素与分析，
    # 但 module/路径均为化学原理；路由到化学原理使其与 6-1/6-2/6-4 合并为 4.5。
    "真题/第29届初赛/化学原理/题-029-6-3-除镍反应方程式.md": "化学原理",
}
WRITE = "--write" in sys.argv
if "--dry-run" in sys.argv:
    WRITE = False
CLEAN = "--clean" in sys.argv
# 严格模式（过滤教学注释块）默认开启；--no-strict 关闭（旧开关 --strict 保留兼容）
STRICT = "--no-strict" not in sys.argv
# 大题合并默认开启：同一道大题的全部小问并入一个题目小节；--no-merge 关闭
MERGE_DA = "--no-merge" not in sys.argv
# ---------------- 全书来源索引聚合器 ----------------
ALL_NON_EXAM = []  # 每项: {module, num, title, source, fid}
# --merge-keys-file 已废弃（历史上用于白名单部分合并），保留解析但不生效
MERGE_KEYS = set()
if "--merge-keys-file" in sys.argv:
    _ki = sys.argv.index("--merge-keys-file")
    if _ki + 1 < len(sys.argv):
        with open(sys.argv[_ki + 1], encoding="utf-8") as _kf:
            MERGE_KEYS = {line.strip() for line in _kf if line.strip()}
# --fix-math：修复 04-题库 源文件中的半截 math（X$_2$ / X$^{2+}$ / $^{18}$O 型），
# 默认 dry-run 仅打印 diff 清单，加 --write 才实写源文件。
FIX_MATH = "--fix-math" in sys.argv
INCLUDE_DEPRECATED = "--include-deprecated" in sys.argv
OUT_ROOT = ""
if "--out-root" in sys.argv:
    idx = sys.argv.index("--out-root")
    if idx + 1 < len(sys.argv):
        OUT_ROOT = os.path.abspath(sys.argv[idx + 1])

EDITION = "teacher"
if "--edition" in sys.argv:
    idx = sys.argv.index("--edition")
    if idx + 1 < len(sys.argv):
        EDITION = sys.argv[idx + 1].strip().lower()
if EDITION not in {"student", "teacher"}:
    raise SystemExit("--edition 仅支持 student|teacher")
EDITION_LABEL = "学生版" if EDITION == "student" else "教师版"


def write_output(path, text):
    """统一写盘；未加 --write 时仅打印将要写入的目标。"""
    if WRITE:
        if OUT_ROOT:
            path = os.path.join(OUT_ROOT, path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    else:
        print(f"  [dry-run] {os.path.relpath(path)} · {len(text.splitlines())} 行")


def clean_output_dir(path):
    """重建前清理本生成器写出的章节/目录文件，避免旧章节残留污染校验口径。"""
    target = os.path.join(OUT_ROOT, path) if OUT_ROOT else path
    if not os.path.isdir(target):
        return
    kept = []
    removed = []
    for fn in os.listdir(target):
        if fn in {"目录.md", "_未分类submodule统计.md"} or re.fullmatch(r"\d+-[^\n/]+\.md", fn):
            removed.append(fn)
        else:
            kept.append(fn)
    for fn in removed:
        os.remove(os.path.join(target, fn))
    if removed:
        print(f"  [clean] {os.path.relpath(target)}: 删除 {len(removed)} 个旧生成文件；保留 {len(kept)} 个非生成文件")


def strip_wikilinks(s):
    """清理普通 wikilink，保留 ![[图片]] 嵌入。"""
    s = re.sub(r"(?<!!)\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"(?<!!)\[\[([^\]]+)\]\]", r"\1", s)
    return s


def drop_noise_sections(s):
    """移除源文件里不适合进习题书的 dataview 与相关题目尾巴。"""
    s = re.sub(r"```dataviewjs\b.*?```", "", s, flags=re.S)
    s = re.sub(
        r"(?ms)^##[ \t]+(?:相关题目|相关真题|真题链接|参考阅读|题目来源|题目信息)[ \t]*\n.*?(?=^##[ \t]+|\Z)",
        "",
        s,
    )
    return s.strip("\n")


def flatten_embedded_details(s):
    """把源文件中题内嵌的 <details> 展开为普通文本，避免与生成器答案块冲突。"""
    def unwrap(m):
        inner = m.group(1)
        inner = re.sub(r"(?m)^\s*<summary>[^\n]*</summary>\s*", "", inner)
        return inner.strip()
    while re.search(r"<details[^>]*>.*?</details>", s, flags=re.S):
        s = re.sub(r"<details[^>]*>(.*?)</details>", unwrap, s, flags=re.S)
    return s


def normalize_markdown_images(s):
    """把源文件里的 ![](...) 图链统一为 Obsidian ![[哈希文件名]] 嵌入。"""
    def repl(m):
        raw = m.group(1).strip()
        # Markdown 允许 "路径 \"标题\"" 后缀；路径本身可含空格，只剥离带引号的 title。
        raw = re.sub(r'\s+"[^"]*"\s*$', "", raw).strip()
        name = os.path.basename(raw.replace("\\", "/"))
        if re.fullmatch(r"[0-9a-fA-F]{64}\.[A-Za-z0-9]+", name):
            return f"![[{name}]]"
        return m.group(0)
    return re.sub(r"!\[[^\]]*\]\(([^)]+)\)", repl, s)


def normalize_obsidian_embeds(s):
    """把路径式 Obsidian 图片嵌入收敛为根目录 basename，哈希图统一为 ![[哈希.扩展名]]。"""
    def repl(m):
        raw = m.group(1).strip()
        target = re.split(r"\s*\|\s*", raw, maxsplit=1)[0].strip()
        name = os.path.basename(target.replace("\\", "/"))
        has_path = "/" in target or "\\" in target
        if re.fullmatch(r"[0-9a-fA-F]{64}\.[A-Za-z0-9]+", name) or has_path:
            return f"![[{name}]]"
        return m.group(0)
    return re.sub(r"!\[\[([^\]\n]+)\]\]", repl, s)


# 题首元信息引用行（来源/难度/教学层级/关联小问等）一律不进习题书正文；
# 真题来源由生成器在小节头统一标注，其余来源不显示。
META_QUOTE_LINE_RE = re.compile(
    r"(?m)^>[ \t]*(?:\*\*)?[ \t]*(?:来源|难度|教学层级|关联小问|相关小问|承上|接续)"
    r"[ \t]*(?:\*\*)?[ \t]*[：:][^\n]*\n?"
    r"|^>[ \t]*\*\*原书解答（[^）]*）\*\*[ \t]*\n?"
)


def clean_section_text(s):
    """统一清理正文：保留图片嵌入，把源文件残留 H2 降级为 H3。"""
    s = strip_wikilinks(s)
    s = re.sub(r"(?m)^> \[!info\][^\n]*\n", "", s)
    s = re.sub(r"(?m)^> \[!note\][^\n]*\n", "", s)
    s = META_QUOTE_LINE_RE.sub("", s)
    s = flatten_embedded_details(s)
    s = normalize_markdown_images(s)
    s = normalize_obsidian_embeds(s)
    s = re.sub(r"(?m)^##\s+", "### ", s)
    return s.strip()


GLUED_HEADING_RE = re.compile(
    r"^##[ \t]+(?!题目与答案\b)(题目|参考答案|参考解答|答案|解答|解析|解题思路|知识点映射|易错分析)(.*)$"
)
IMAGE_EMBED_RE = re.compile(r"!\[\[[^\]\n]+\]\]")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")


def normalize_glued_headings(s, source=""):
    """把 `## 题目> 来源：…` 等标题与正文同行写法拆成独立标题+正文。"""
    out = []
    for line in s.splitlines():
        if re.match(r"^##[ \t]+题目与答案[ \t]*$", line):
            # 保留给 split_question_answer 的“题目与答案”引用块版式专用分支处理。
            out.append(line)
            continue
        m = GLUED_HEADING_RE.match(line)
        if not m:
            out.append(line)
            continue
        head, rest = m.group(1), m.group(2).strip()
        if not rest:
            out.append(f"## {head}")
            continue
        if rest.startswith(">"):
            if source:
                src_pat = re.compile(rf"^(\s*>\s*来源：{re.escape(source)}\s*)(.*)$", re.S)
                sm = src_pat.match(rest)
                if sm:
                    out.append(f"## {head}")
                    out.append(sm.group(1).strip())
                    body = sm.group(2).strip()
                    if body:
                        out.append("")
                        out.append(body)
                    continue
            bq = re.match(r"(>.*?\]\]）)(.*)$", rest)
            if bq:
                out.append(f"## {head}")
                out.append(bq.group(1).strip())
                body = bq.group(2).strip()
                if body:
                    out.append("")
                    out.append(body)
                continue
        out.append(f"## {head}")
        out.append(rest)
    return "\n".join(out)


def normalize_image_paragraphs(s):
    """把贴分隔线、图文同行、同行多图拆成独立图片段落；表格行保持原样。"""
    s = re.sub(r"---\s*(?=!\[\[)", "", s)
    lines = s.splitlines()
    out = []
    for line in lines:
        if TABLE_ROW_RE.match(line) or "<td" in line.lower() or "<tr" in line.lower():
            out.append(line)
            continue
        embeds = list(IMAGE_EMBED_RE.finditer(line))
        if not embeds:
            out.append(line)
            continue
        parts = []
        pos = 0
        for m in embeds:
            prefix = line[pos:m.start()].strip()
            if prefix:
                parts.append(prefix)
            parts.append(m.group(0).strip())
            pos = m.end()
        suffix = line[pos:].strip()
        if suffix:
            parts.append(suffix)
        if len(parts) <= 1:
            out.append(line)
            continue
        for i, part in enumerate(parts):
            if i > 0 and out and out[-1].strip():
                out.append("")
            out.append(part)
    return "\n".join(out).strip()


TEACHING_BLOCK_HEADING_RE = re.compile(
    r"^#{1,6}[ \t]*[^\n]*(?:解题思路|易错分析|相关图片|小问关联|得分点|读题定位|关键转换|计算要点"
    r"|错误表|课堂提问表|方法点拨|思路点拨|关联知识点|关联小问|易错点|常见错误)"
    r"[ \t]*[^\n]*$",
    re.M,
)
TEACHING_HEADING_ONLY_RE = re.compile(
    r"^#{1,6}[ \t]*(?:题目图示与结构参考|知识点映射|知识扩展|知识拓展)"
    r"(?:[ \t]*[^\n]*)?$",
    re.M,
)
TEACHING_CONT_HEADING_RE = re.compile(
    r"^#{1,6}[ \t]*[^\n]*(?:解题思路|知识点映射|易错分析|相关图片|知识扩展|知识拓展"
    r"|方法点拨|思路点拨|关联知识点|关联小问|易错点|常见错误|小问关联|得分点|读题定位|关键转换|计算要点)"
    r"[^\n]*$",
    re.M,
)
TEACHING_NUMBERED_SUBHEADING_RE = re.compile(
    r"^#{1,6}[ \t]*第[0-9一二三四五六七八九十百]+题[ \t]*(?:解题思路|易错分析|相关图片"
    r"|小问关联|关联小问|得分点|读题定位|关键转换|计算要点|方法点拨|思路点拨|关联知识点|易错点|常见错误)"
    r"[ \t]*[^\n]*$",
    re.M,
)
TEACHING_IMG_HEADING_RE = re.compile(r"^#{1,6}[ \t]*[^\n]*!\[\[[^\]]+\]\]", re.M)
TEACHING_PREFIX_RE = re.compile(
    r"^\s*(?:>\s*)?(?:[-*+]\s+|\d+[.、)]\s+)?\*\*[ \t]*"
    r"(?:[^\n*]{0,8}[ \t]*)?(?:小问关联|关联小问|得分点|读题定位|关键转换|计算要点"
    r"|易错分析|解题思路|思路提示|方法提示|答题技巧)[^\n]*?\*\*[ \t]*(?:[:：]|$)",
    re.M,
)
TEACHING_INLINE_RE = re.compile(
    r"^\s*(?:>\s*)?(?:[-*+]\s+|\d+[.、)]\s+)?(?:解题思路|易错分析|读题定位|关键转换)[ \t]*[:：]",
    re.M,
)
TEACHING_TABLE_RE = re.compile(
    r"^\s*\|[ \t]*(?:关联 KP|关联小问|错误|易错点|易错|课堂提问|小问关联|得分点"
    r"|常见错误|失分点)[ \t]*\|",
    re.M,
)
SIBLING_HEADING_RE = re.compile(r"^#{1,6}[ \t]*🔗[ \t]*同大题小问[ \t]*$", re.M)
CALLOUT_EMOJI_RE = re.compile(
    r"(?m)^(>\s*)(?:📎|🌱|🏆|🌟|🔥|💡|📝|🧠|🗣|⚡|🔗|🏅|⭐|💎|🎯|⚠️|✅|❌|📌)\s*"
)


def _is_teaching_continuation_heading(line):
    """教学块内的关键词子标题或图片标题视为同一教学块，继续删除。"""
    if TEACHING_CONT_HEADING_RE.match(line):
        return True
    if TEACHING_IMG_HEADING_RE.match(line):
        title = re.sub(r"^#{1,6}[ \t]*", "", line).strip()
        if re.match(r"^(?:参考答案|参考解答|答案|解答|解析|题目)", title):
            return False
        return True
    return False


def _consume_contiguous_block(lines, i):
    """删除前缀/表格型教学行：无空行分隔时整段删除，空行后的正文保留。"""
    j = i + 1
    while j < len(lines):
        nxt = lines[j]
        if not nxt.strip():
            k = j
            while k < len(lines) and not lines[k].strip():
                k += 1
            return k
        j += 1
    return j


def _consume_teaching_block(lines, i):
    """删除教学块标题及其续接内容；遇到真实标题/正文边界时停止。"""
    numbered_sub = bool(TEACHING_NUMBERED_SUBHEADING_RE.match(lines[i]))
    j = i + 1
    while j < len(lines):
        nxt = lines[j]
        if not nxt.strip():
            k = j
            while k < len(lines) and not lines[k].strip():
                k += 1
            if k < len(lines) and _is_teaching_continuation_heading(lines[k]):
                j = k
                continue
            if k < len(lines) and re.match(r"^#{1,6}[ \t]", lines[k]):
                return k
            prev = j - 1
            while prev >= 0 and not lines[prev].strip():
                prev -= 1
            if numbered_sub or (prev >= 0 and TEACHING_NUMBERED_SUBHEADING_RE.match(lines[prev])):
                j = k
                continue
            return k
        if re.match(r"^#{1,6}[ \t]", nxt):
            if _is_teaching_continuation_heading(nxt):
                j += 1
                continue
            return j
        j += 1
    return j


def _consume_teaching_block(lines, i):
    """删除教学块标题及其全部内容，直到下一个标题或 --- 分节线为止。"""
    j = i + 1
    while j < len(lines):
        nxt = lines[j]
        if not nxt.strip():
            j += 1
            continue
        if re.match(r"^#{1,6}[ \t]", nxt):
            return j
        if re.match(r"^\s*(?:---|\*\*\*|___)+\s*$", nxt):
            return j
        j += 1
    return j


def _skip_kp_residue(lines, i):
    """知识点映射标题被移除后，继续删除其后的要点列表残块（兼容多种列表格式）。"""
    j = i
    while j < len(lines) and not lines[j].strip():
        j += 1
    while j < len(lines) and re.match(r"^\s*(?:[-*+]|\d+[.、)])\s+", lines[j]):
        j += 1
        while j < len(lines) and not lines[j].strip():
            j += 1
    return j


def strip_teaching_blocks(s):
    """严格模式：删除教学注释块，保留题目、解析正文与图片。"""
    if not STRICT or not s:
        return s
    # 答案表内指向已删除教学块的悬空引用，改为指向下方保留的详细解答。
    s = re.sub(r"(?m)^(\s*\|.*?)见解题思路[^|\n]*(\|)", r"\1见下方详细解答\2", s)
    s = s.replace("见易错分析", "见下方易错说明")
    s = CALLOUT_EMOJI_RE.sub(r"\1", s)
    lines = s.splitlines()
    keep = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if SIBLING_HEADING_RE.match(line):
            i += 1
            continue
        if TEACHING_BLOCK_HEADING_RE.match(line):
            i = _consume_teaching_block(lines, i)
            continue
        if TEACHING_HEADING_ONLY_RE.match(line):
            if "题目图示与结构参考" in line:
                i += 1  # 只去标题，保留题目配图
                continue
            if "知识点映射" in line:
                i = _skip_kp_residue(lines, i + 1)
                continue
            i = _consume_teaching_block(lines, i)  # 知识扩展/拓展：整块删除
            continue
        if (TEACHING_PREFIX_RE.match(line) or TEACHING_INLINE_RE.match(line)
                or TEACHING_TABLE_RE.match(line)):
            i = _consume_contiguous_block(lines, i)
            continue
        keep.append(line)
        i += 1
    return "\n".join(keep).strip()


def _answer_heading_pattern():
    # 严格模式下只认真实答案标题；教学块（解题思路/知识点映射/易错分析等）
    # 不再充当答案切分入口，避免把教学注释混入解析正文。
    if STRICT:
        return re.compile(
            r"^#{1,4}[ \t]+(?:参考答案|参考解答|答案|解答|解析)(?:（[^）]*）)?[ \t]*(?=\n|\r|$)",
            re.M,
        )
    return re.compile(
        r"^#{1,4}[ \t]+(?:参考答案|参考解答|答案|解答|解析|解题思路|知识点映射|易错分析)[ \t]*$",
        re.M,
    )


ANSWER_HEADING_RE = _answer_heading_pattern()
ANSWER_INLINE_RE = re.compile(r"\*\*\s*答案\s*[:：]\s*\*\*|【答案】\s*[:：]?")
ANSWER_BLOCKQUOTE_RE = re.compile(r"^>\s*\*\*(?:答案|参考答案)\*\*\s*[:：]?\s*", re.M)
SOLVE_LINE_RE = re.compile(r"^[ \t]*解\s*[:：]\s*", re.M)
DISPLAY_MATH_RE = re.compile(
    r"\$\$\r?\n.*?\r?\n\$\$|\$\$.+?\$\$|\\\[.*?\\\]",
    re.S,
)
SOLVE_IN_BLOCK_RE = re.compile(r"解[^\n]{0,12}[:：]")
QUESTION_START_RE = re.compile(r"^##[ \t]+题目\s*$", re.M)
QA_SECTION_RE = re.compile(r"^##[ \t]+题目与答案\s*$", re.M)
QUESTION_LABEL_RE = re.compile(
    r"(?m)^#{2,6}[ \t]*(?:例)?\d+(?:\.\d+)*[^\n]*$"
    r"|^\*\*\s*(?:例)?\d+(?:\.\d+)*[^\n]*\*\*"
)


def answer_markers(s):
    """返回源文件里所有可辨识的答案入口（含解答标题、行首解：、公式块内解：）。"""
    marks = []
    for m in ANSWER_HEADING_RE.finditer(s):
        marks.append((m.start(), m.end(), "heading"))
    for m in ANSWER_INLINE_RE.finditer(s):
        marks.append((m.start(), m.end(), "inline"))
    for m in ANSWER_BLOCKQUOTE_RE.finditer(s):
        marks.append((m.start(), m.end(), "blockquote"))
    for m in SOLVE_LINE_RE.finditer(s):
        marks.append((m.start(), m.end(), "line"))
    for m in DISPLAY_MATH_RE.finditer(s):
        if SOLVE_IN_BLOCK_RE.search(m.group(0)):
            marks.append((m.start(), m.end(), "math"))
    marks.sort(key=lambda x: (x[0], x[1]))
    # 已由更早的答案标题/行首解：覆盖时，公式块内的解：不再单独成段，
    # 避免同一公式块在答案里重复出现两次。
    early = [ms for ms, _, kind in marks if kind != "math"]
    filtered = []
    for ms, me, kind in marks:
        if kind == "math" and any(ms0 < ms for ms0 in early):
            continue
        filtered.append((ms, me, kind))
    return filtered


def strip_stray_choice_tail(s):
    """去掉补答案阶段残留的 `> **答案**：**(X)** 占位尾巴，但保留仅有该行的真答案。"""
    lines = s.splitlines()
    while lines:
        last = lines[-1].strip()
        if re.fullmatch(r">\s*\*\*(?:答案|参考答案)\*\*\s*[:：]?\s*\*\*\([A-Ha-h]\)\*\*", last) \
                or re.fullmatch(r"\*\*\([A-Ha-h]\)\*\*", last):
            if any(l.strip() for l in lines[:-1]):
                lines.pop()
                continue
        break
    return "\n".join(lines).strip()


def split_question_answer(body, source=""):
    """按源文件常见分节切题干/答案，缺失任一标题时也不丢正文。"""
    # 只移除真正的 H1 标题（单个 #），避免误删正文中的 ## 分节标题。
    work = re.sub(r"(?m)^#[ \t]+[^\n]*\n?", "", body, count=1).strip()
    work = drop_noise_sections(work)
    work = normalize_glued_headings(work, source)
    markers = answer_markers(work)
    if markers and QA_SECTION_RE.search(work):
        # “题目与答案”一体文件在有答案标记时，把包装头归一为 ## 题目，
        # 避免 `### 题目与答案` 残留在题干；无标记的引用块版式仍走专用分支。
        work = QA_SECTION_RE.sub("## 题目", work)
        markers = answer_markers(work)
    if markers:
        first = markers[0][0]
        # 例题文件常混入整章 OCR 尾巴，从第一个答案入口后的“第X部分”章节头开始裁掉。
        tail = re.search(r"(?m)^#{1,4}[ \t]*第[一二三四五六七八九十]+部分[ \t]*[^\n]*$", work[first:])
        if tail:
            work = work[:first + tail.start()]
            markers = answer_markers(work)
    qloc = QUESTION_START_RE.search(work)
    if not markers:
        if qloc:
            q_text = work[qloc.end():]
        else:
            q_text = work
        a_text = ""
        # 源书“题目与答案”版式：答案以纯引用块跟在每个小题后，无 **答案：** 标签；
        # 仅在此版式下按引用块拆分，避免把题头的“> 来源”引用误判为答案。
        qa = QA_SECTION_RE.search(q_text)
        if qa:
            tail = q_text[qa.end():]
            q_lines, a_lines = [], []
            for line in tail.splitlines():
                stripped = line.lstrip()
                if stripped.startswith(">"):
                    a_lines.append(re.sub(r"^>\s?", "", stripped))
                else:
                    q_lines.append(line)
            q_text = "\n".join(q_lines).strip()
            a_text = "\n".join(a_lines).strip()
        return q_text.strip(), a_text

    q_start = qloc.end() if (qloc and qloc.start() < markers[0][0]) else 0
    label_positions = [m.start() for m in QUESTION_LABEL_RE.finditer(work)]
    q_parts = []
    a_parts = []
    for i, (ms, me, kind) in enumerate(markers):
        next_marker = markers[i + 1][0] if i + 1 < len(markers) else len(work)
        boundary = next_marker
        # 只有题内逐小题的 **答案：** 需要把下一小题标题还回题干；
        # 标题式答案节里的 **20.40** 等是答案子题号，不能当题干边界。
        if kind == "inline":
            for lp in label_positions:
                if me < lp < boundary:
                    boundary = lp
                    break
        piece_start = ms if kind == "math" else me
        a_parts.append(work[piece_start:boundary])
        if boundary < next_marker:
            q_parts.append(work[boundary:next_marker])

    q_text = work[q_start:markers[0][0]] + "".join(q_parts)
    a_text = strip_stray_choice_tail("\n\n".join(a_parts).strip())
    if a_text:
        a_text = strip_stray_choice_tail(a_text)
    return q_text.strip(), a_text


def gather_questions(module):
    """收集指定模块、pack=模块习题集的所有题目"""
    pool = []
    for root, dirs, fs in os.walk(BASE):
        if "高考" in root: continue
        for fn in fs:
            if not fn.endswith(".md"): continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, BASE).replace(os.sep, "/")
            s = open(path, encoding="utf-8", errors="replace").read()
            fm = re.match(r"^---\n(.*?)\n---\n", s, re.S)
            if not fm: continue
            y = fm.group(1)
            if not re.search(r"(?m)^type: 题目", y): continue
            if not re.search(r"(?m)^pack: 模块习题集", y): continue
            override_target = PATH_SUBJECT_MODULE_OVERRIDES.get(rel)
            if override_target:
                if module != override_target:
                    continue
                if not re.search(r"(?m)^subject_module:", y):
                    continue
            elif not re.search(rf"(?m)^subject_module: {re.escape(module)}$", y):
                continue
            status = (re.search(r"(?m)^status: (.*)", y) or [None, ""])[1].strip()
            if status == "deprecated" and not INCLUDE_DEPRECATED:
                continue
            diff = (re.search(r"(?m)^difficulty: (.*)", y) or [None, "3"])[1].strip()
            sub = (re.search(r"(?m)^submodule: (.*)", y) or [None, ""])[1].strip().strip('"')
            mod = (re.search(r"(?m)^module: (.*)", y) or [None, ""])[1].strip().strip('"')
            fid = (re.search(r"(?m)^fidelity: (.*)", y) or [None, ""])[1].strip()
            src = (re.search(r"(?m)^source: (.*)", y) or [None, ""])[1].strip()
            ttl = (re.search(r"(?m)^title: (.*)", y) or [None, ""])[1].strip().strip('"').strip("'")
            body = s[fm.end():].strip()
            d = int(diff) if diff.isdigit() else 3
            pool.append({
                "file": fn,
                "path": rel,
                "difficulty": d,
                "submodule": sub,
                "module": mod,
                "fidelity": fid,
                "source": src,
                "title": ttl,
                "body": body,
            })
    return pool


def classify_by_keywords(item, chapter_map, module=None):
    """根据关键词映射返回章节名；同时识别有机/元素题中的一些模式"""
    sub = item["submodule"]
    text = (sub + " " + item["file"] + " " + item.get("path", "")).lower()

    # 路径与 module 是比 submodule 更可靠的来源线索；优先处理已知不可靠字段
    if module == "结构化学":
        p = item["path"]
        if "Weller/Ch20" in p or "Weller/Ch21" in p:
            return (4, "配位化学")

    if module == "元素与分析":
        mod = item.get("module", "").lower()
        p = item["path"]
        pl = p.lower()
        if "分析化学" in mod or "分析化学/" in pl:
            return (6, "化学分析")
        if mod.startswith("过渡-") or "元素化学/过渡-" in pl or "无机化学例题与习题/ch19" in pl \
                or "无机化学例题与习题/ch20" in pl or "无机化学例题与习题/ch21" in pl \
                or "无机化学例题与习题/ch22" in pl or "weller/ch19" in pl:
            return (4, "过渡元素化学")
        if "无机化学例题与习题/ch14" in pl or "无机化学例题与习题/ch15" in pl \
                or "无机化学例题与习题/ch16" in pl or "无机化学例题与习题/ch17" in pl \
                or "无机化学例题与习题/ch18" in pl or "weller/ch18" in pl:
            return (3, "主族元素化学")
        if "稀有气体" in sub or "溶液与化学分析" in sub:
            return (3, "主族元素化学") if "稀有气体" in sub else (6, "化学分析")

    # 直接 submodule → 章节映射（由清洗脚本推断的章节名）
    DIRECT_SUB_MAP = {
        "化学分析": (6, "化学分析"),
        "化学基础与计量": (1, "化学基础与计量"),
        "离子反应与方程式": (2, "离子反应与方程式"),
        "主族元素化学": (3, "主族元素化学"),
        "过渡元素化学": (4, "过渡元素化学"),
        "元素推断": (5, "元素推断"),
        "结构基础与波谱分析": (1, "结构基础与波谱分析"),
        "立体化学": (2, "立体化学"),
        "烷烯炔与加成反应": (3, "烷烯炔与加成反应"),
        "芳香化合物与亲电取代": (4, "芳香化合物与亲电取代"),
        "亲核取代、消除与羧酸衍生物": (5, "亲核取代、消除与羧酸衍生物"),
        "羰基化学与缩合反应": (6, "羰基化学与缩合反应"),
        "金属有机与偶联反应": (7, "金属有机与偶联反应"),
        "周环反应与自由基": (8, "周环反应与自由基"),
        "杂环化合物与含杂原子有机物": (9, "杂环化合物与含杂原子有机物"),
        "有机合成设计": (10, "有机合成设计"),
        "反应机理与推断": (11, "反应机理与推断"),
        "高分子化学": (12, "高分子化学"),
    }
    if module in ("有机化学", "元素与分析") and sub in DIRECT_SUB_MAP:
        return DIRECT_SUB_MAP[sub]

    # 化学原理：优先按学科主题归类，避免"电化学与热力学"等复合子模块误入热力学
    if module == "化学原理":
        if sub == "化学基础与计量" or any(k in text for k in ["化学计量", "有效数字", "气体定律", "同位素", "核化学", "放射性衰变", "核反应"]):
            return (6, "化学基础与计量")
        if sub in {"酸碱平衡", "沉淀溶解平衡", "溶度积与沉淀溶解平衡", "酸碱平衡·分布系数"}:
            return (5, "溶液与酸碱平衡")
        if any(k in text for k in ["电化学", "电极", "电势", "原电池", "电池", "电解", "氧化还原", "歧化", "latimer", "nernst", "e-ph", "kolbe", "电镀"]):
            return (4, "氧化还原与电化学")
        if any(k in text for k in ["动力学", "速率", "半衰期", "活化能", "arrhenius", "反应机理", "稳态近似"]):
            return (3, "化学动力学")
        if any(k in text for k in ["热力学", "焓", "熵", "gibbs", "hess", "盖斯", "燃烧", "生成焓", "能量变化", "热化学"]):
            return (1, "热力学")
        if any(k in text for k in ["酸碱", "滴定", "缓冲", "解离", "溶度积", "ksp", "分布系数"]):
            return (5, "溶液与酸碱平衡")
        if any(k in text for k in ["平衡", "转化率", "勒夏特列", "化学势", "相图"]):
            return (2, "化学平衡")
        # 未命中 → None（由 build_book 记入待分类告警，不再收容进"综合"章）
        return None

    # 有机题的模式化 submodule 处理（仅对有机模块生效）
    if module == "有机化学":
        if sub.startswith("有机反应·"):
            rx = sub.split("·", 1)[1].lower()
            if rx in ["臭氧化", "羟汞化", "烯烃的亲电加成", "加成"]:
                return (3, "烷烯炔与加成反应")
            if rx in ["knoevenagel", "aldol", "claisen", "缩合"]:
                return (6, "羰基化学与缩合反应")
            if rx in ["diels-alder", "电环化", "nazarov", "achmatowicz"]:
                return (8, "周环反应与自由基")
            if rx in ["亲核取代", "消除"]:
                return (5, "亲核取代、消除与羧酸衍生物")
            if rx in ["自由基"]:
                return (8, "周环反应与自由基")
            if rx in ["芳香", "亲电取代"]:
                return (4, "芳香化合物与亲电取代")
            if rx in ["羰基", "羧酸", "醛", "酮"]:
                return (6, "羰基化学与缩合反应")
            if rx in ["金属有机", "偶联"]:
                return (7, "金属有机与偶联反应")
            return (11, "反应机理与推断")
        if sub.startswith("有机结构·") or sub.startswith("有机基础·"):
            return (1, "结构基础与波谱分析")
        if sub.startswith("有机合成·"):
            return (10, "有机合成设计")
        if sub in ["有机推断", "有机催化·碱催化"]:
            return (11, "反应机理与推断")
        if sub in ["有机物理化学", "有机热力学·稳定性"]:
            return (1, "结构基础与波谱分析")
        if sub == "硫化学":
            return (9, "杂环化合物与含杂原子有机物")
        if sub in ["高分子化学", "高分子物理", "开环聚合与热力学"]:
            return (12, "高分子化学")
        if sub.startswith("人名反应与"):
            return (8, "周环反应与自由基")
        if sub.startswith("有机机理·"):
            return (11, "反应机理与推断")
        if sub in ["反应中间体与机理", "活性中间体与反应机理", "反应中间体", "有机反应类型", "化学计算"]:
            return (11, "反应机理与推断")
        if sub in ["氢键、HFIP溶剂", "有机化合物性质", "分子异构体、三角双锥构型", "有机结构·共振式", "有机结构·同分异构", "有机基础·不饱和度", "同分异构与分子推断", "碳正离子与取代基效应"]:
            return (1, "结构基础与波谱分析")
        if sub in ["无氧实验操作", "有机化合物鉴别", "有机合成·天然产物"]:
            return (10, "有机合成设计")
        if sub in ["有机化学进阶", "有机热力学·稳定性", "开环聚合与热力学", "高分子物理"]:
            return (12, "高分子化学")

    # 非有机内容：返回 None 以便交给 cross-module 脚本处理（仅对有机模块生效）
    if module == "有机化学" and sub in ["蒸气压", "分子间作用力", "化学平衡与转化率", "萃取与分配定律", "离子交换", "吸光光度法", "酸碱反应", "酸碱·电离", "无机合成", "氧化亚铜、羟胺还原", "化学生物学"]:
        return None

    # 元素与分析题的模式化 submodule 处理
    if module == "元素与分析":
        if sub in ["萃取与分配定律", "吸光光度法"]:
            return (6, "化学分析")
        if sub == "无机合成":
            return (4, "过渡元素化学")
        if sub == "氧化亚铜、羟胺还原":
            return (2, "离子反应与方程式")
        if sub == "化学生物学":
            return (5, "元素推断")

    for num, name, keywords in chapter_map:
        for kw in keywords:
            if kw.lower() in text:
                return (num, name)

    # 结构化学习题的模式化 submodule 处理（keyword 未命中的情况）
    if module == "结构化学":
        if "群论" in sub or "点群" in sub or "对称性" in sub:
            return (5, "对称性与群论")
        if "超分子" in sub or sub in ["三维骨架结构", "二维层状结构", "表面化学", "胶束化学", "MOF", "沸石", "分子筛", "锂离子电池电解质、分子构型推断"]:
            return (6, "超分子与材料化学")
        if sub in ["结构化学基础", "化学计量与计算", "物理化学", "无氧实验操作"]:
            return (7, "结构化学基础")
        if "推断" in sub or "推导" in sub or "综合" in sub or sub in ["化合物分子式推断", "结构推导", "结构化学·聚合阴离子", "计算化学·密度"]:
            return (8, "结构推断与综合")
        if "中级无机化学" in sub:
            fn_low = item["file"].lower()
            if any(k in fn_low for k in ["群论", "对称性", "点群"]):
                return (5, "对称性与群论")
            if any(k in fn_low for k in ["原子簇", "固体化学", "超分子"]):
                return (6, "超分子与材料化学")
            if any(k in fn_low for k in ["配合物", "配位", "晶体场", "反应机理"]):
                return (4, "配位化学")
            if any(k in fn_low for k in ["晶体", "晶胞", "晶格"]):
                return (3, "晶体结构")
            return (7, "结构化学基础")

    return None


def da_key(filename):
    """从源文件名提取大题 key：`题-036决理-2-...` → `题-036决理-2`。"""
    m = re.match(r"^题-(\d+[A-Za-z]*?)-(\d+)-", filename)
    return f"题-{m.group(1)}-{m.group(2)}" if m else None


def _natkey(fn):
    """文件名自然排序键：数字段按数值比较，保证 1-2 排在 1-10 前。"""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", fn)]


def _common_prefix_len(a, b):
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


def merge_da_items(items):
    """把同一大题下的小问归一为一道题（仅生成阶段，不改源文件）。

    组内按文件名自然排序；以首小问题干为基准，后续小问若整段重复了共享题干
    （公共前缀 ≥40 字）则剥掉重复前缀，只保留该小问的新增内容。
    """
    groups = collections.OrderedDict()
    out = []
    for item in items:
        k = da_key(item["file"])
        if k is None:
            out.append(item)
            continue
        groups.setdefault(k, []).append(item)
    for k, g in groups.items():
        if len(g) == 1:
            out.append(g[0])
            continue
        g = sorted(g, key=lambda x: _natkey(x["file"]))
        q_parts, a_parts = [], []
        base_q = ""
        for idx, it in enumerate(g):
            q, a = split_question_answer(it["body"], it.get("source", ""))
            q = clean_section_text(q)
            a = clean_section_text(a)
            if STRICT:
                q = strip_teaching_blocks(q)
                a = strip_teaching_blocks(a)
            q = normalize_image_paragraphs(q)
            a = normalize_image_paragraphs(a)
            q = collapse_hrs(q.strip())
            a = collapse_hrs(a.strip())
            if idx == 0:
                base_q = q
            elif base_q and q:
                pl = _common_prefix_len(base_q, q)
                if pl >= 40:
                    # 截断点尽量落在换行边界，避免切断半句
                    cut = q.rfind("\n", 0, pl)
                    q = q[cut:].strip() if cut >= 40 else q[pl:].strip()
            q_parts.append(f"### （{idx + 1}）\n{q}")
            a_parts.append(f"**（{idx + 1}）**\n{a.strip()}")
        merged = {
            "file": g[0]["file"],
            "path": g[0]["path"],
            "difficulty": max(x["difficulty"] for x in g),
            "submodule": g[0]["submodule"],
            "module": g[0]["module"],
            # fidelity 取组内最低档（自编 < 原书改写 < 原书逐字）
            "fidelity": min((x["fidelity"] for x in g),
                            key=lambda f: {"自编": 0, "原书改写": 1}.get(f, 2)),
            "source": g[0]["source"],
            "title": g[0].get("title", ""),
            "_q": "\n\n".join(q_parts),
            "_a": "\n\n".join(a_parts),
            "_merged_n": len(g),
        }
        out.append(merged)
    out.sort(key=lambda x: x["difficulty"])
    return out


def is_gap_item(item):
    """含外部资料缺口的题（答案待补充 / 前驱待定位 / 图片待补）：不入习题书。"""
    body = item.get("body", "")
    return bool(re.search(r"答案待补充|前驱文件待定位|图片待补", body))


def collapse_hrs(s):
    """折叠连续多个 --- 分隔线（允许空行间隔），并去掉文本尾部的孤分隔线。"""
    out = []
    for line in s.splitlines():
        if re.fullmatch(r"\s*---\s*", line):
            k = len(out) - 1
            while k >= 0 and not out[k].strip():
                k -= 1
            if k >= 0 and re.fullmatch(r"\s*---\s*", out[k]):
                continue  # 与上一条分隔线重复，丢弃
        out.append(line)
    s = "\n".join(out)
    s = re.sub(r"(\s*\n)?\s*---\s*$", "", s)
    return s.rstrip()


WARNINGS = collections.defaultdict(list)  # kind -> [定位信息]


def _warn(kind, msg):
    WARNINGS[kind].append(msg)


def short_title(item):
    """小节标题：真题取文件名描述尾段；教材题剥掉模块名前缀；其余回退 frontmatter title。"""
    fn = item["file"][:-3] if item["file"].endswith(".md") else item["file"]
    m = re.match(r"^题-[\dA-Za-z]+(?:-\d+)+-(.+)$", fn)
    if m:
        return m.group(1).strip()
    t = re.sub(r"^题-\d+-", "", fn)
    parts = t.split("-")
    drop = {item.get("submodule", ""), item.get("module", ""),
            "初赛讲义", "上海中学", "结构化学基础", "无机化学例题与习题", "例题与习题",
            "赵鑫光", "汇智", "Clayden", "ABOC", "中级无机化学", "普通化学原理"}
    while len(parts) > 1 and parts[0] in drop:
        parts.pop(0)
    t = "-".join(parts).strip()
    if t and not re.fullmatch(r"[\d\-.]+", t):
        return t
    ttl = item.get("title", "")
    ttl = re.sub(r"^题-[^\s：:]+[：:]\s*", "", ttl).strip()
    return ttl


def exam_label(item):
    """真题来源标签：仅真题返回如「第38届初赛」，其余一律返回空串。"""
    m = re.search(r"(?:^|/)真题/(第\d+届[^/]+|省预赛)/", item["path"])
    if m:
        return m.group(1)
    s = item.get("source", "")
    m = re.search(r"第\s*(\d+)\s*届.{0,12}?(初赛|决赛)", s)
    if m:
        return f"第{m.group(1)}届{m.group(2)}"
    if "预赛" in s:
        return "省预赛"
    return ""


def build_book(module, out_dir, chapter_map, exclude_subs=None):
    if WRITE and CLEAN:
        clean_output_dir(out_dir)
    exclude_subs = set(exclude_subs or [])
    pool = [q for q in gather_questions(module) if q["submodule"] not in exclude_subs]
    _gap = [q for q in pool if is_gap_item(q)]
    if _gap:
        print(f"  [gap-excluded] {module}: 剔除 {len(_gap)} 道需外部资料的缺口题"
              f"（{', '.join(q['path'] for q in _gap)}）")
        pool = [q for q in pool if not is_gap_item(q)]
    if MERGE_DA:
        # 先在模块池内按大题归并，再整体分类，避免同一大题被拆分到不同章节。
        pool = merge_da_items(pool)
        n_merged = sum(1 for x in pool if "_merged_n" in x)
        n_sub = sum(x.get("_merged_n", 1) for x in pool)
        if n_merged:
            print(f"  [merge] {module}: {n_sub} 个小问文件 → {len(pool)} 题（{n_merged} 个大题合并组）")

    # 分类；未命中章节映射的题不再收容进"综合"章，记入待分类告警
    groups = collections.OrderedDict()
    for item in pool:
        res = classify_by_keywords(item, chapter_map, module)
        if res is None:
            _warn("待分类", f"[{module}] {item['path']}（submodule={item['submodule'] or '空'}）")
            continue
        groups.setdefault(res, []).append(item)

    # 按章节号排序
    groups = collections.OrderedDict(sorted(groups.items(), key=lambda x: x[0][0]))

    # 每章按难度排序
    for key in groups:
        groups[key].sort(key=lambda x: x["difficulty"])

    # 生成章节文件
    index_rows = []
    for (num, name), items in groups.items():
        fname = f"{num}-{name}.md"
        lines = []
        lines.append("---")
        lines.append(f'title: "{module} 第{num}章 {name}（{EDITION_LABEL}）"')
        lines.append("type: 习题集章节")
        lines.append(f"edition: {EDITION}")
        lines.append(f"updated: {TODAY}")
        lines.append(f"question_count: {len(items)}")
        lines.append(f"subject_module: {module}")
        lines.append("---")
        lines.append("")
        lines.append(f"# 第 {num} 章 {name}")
        lines.append("")
        dc = collections.Counter(x["difficulty"] for x in items)
        dstr = " ".join(f"d{i}={dc.get(i, 0)}" for i in range(1, 6))
        lines.append(f"> **题量**：{len(items)} ｜ **难度**：{dstr}")
        lines.append("")
        lines.append("---")
        lines.append("")

        qn = 0
        for item in items:
            qn += 1
            fid = item["fidelity"]
            tag = "🟢" if "逐字" in fid else ("🔵" if "自编" in fid else "🟡")
            d = item["difficulty"]
            if "_q" in item:
                q_text, a_text = item["_q"], item["_a"]
            else:
                q_text, a_text = split_question_answer(item["body"], item.get("source", ""))
                q_text = clean_section_text(q_text)
                a_text = clean_section_text(a_text)
                if STRICT:
                    q_text = strip_teaching_blocks(q_text)
                    a_text = strip_teaching_blocks(a_text)
                q_text = normalize_image_paragraphs(q_text)
                a_text = normalize_image_paragraphs(a_text)
                q_text = collapse_hrs(q_text)
                a_text = collapse_hrs(a_text)

            # ---- 质量告警（不打断生成，dry-run/正式均汇总打印）----
            loc = f"[{module}] {fname} #{num}.{qn} ← {item['path']}"
            if not q_text.strip():
                _warn("空题干", loc)
            if re.search(r"【(?:例题|习题)?参考答案】|【习题精练】|【例题精讲】", q_text):
                _warn("题干混入答案块", loc)
            if not a_text.strip():
                _warn("答案为空", loc)
            elif re.search(r"原书未提供|略，见源文件|答案待补充|需要完整题目信息|图片待补", a_text):
                _warn("答案占位", loc)
            for seg_label, seg in (("题干", q_text), ("答案", a_text)):
                if seg.count("$") % 2:
                    _warn("未闭合math", f"{loc} [{seg_label}]")
            # 题/答边界错位探测（仅限 2026-08-25 逐字回填批次的文件）：
            # 题干结尾无终止标点，且答案首个实质行（跳过"原书解答"头）以续接符/
            # 数学/小写字母/数字开头 → 题干残尾很可能漏进了答案块。
            if re.search(r"原书解答|逐字转录", a_text):
                tail_q = q_text.rstrip()[-1:] if q_text.strip() else ""
                ans_lines = [l.strip().lstrip("> ").strip() for l in a_text.splitlines() if l.strip()]
                ans_lines = [l for l in ans_lines if not re.match(r"^\*\*原书解答", l)]
                first_a = ans_lines[0] if ans_lines else ""
                stem_open_ended = bool(tail_q) and tail_q not in "。！？；：.!?】)）」』$|`'"
                ans_continues = bool(first_a) and (
                    re.match(r"^[，。、；：）)]", first_a)
                    or first_a.startswith("$")
                    or first_a[0].islower()
                    or first_a[0].isdigit()
                )
                if stem_open_ended and ans_continues:
                    _warn("疑似题答边界错位", loc)

            head = f"## {num}.{qn}"
            title = short_title(item)
            if title:
                head += f" {title}"
            head += f" 〔{tag} d{d}〕"
            label = exam_label(item)
            if label:
                head += f"（{label}）"
            index_rows.append({
                "num": f"{num}.{qn}",
                "title": title,
                "source": item.get("source", ""),
                "fid": fid,
                "path": item["path"],
                "exam": label,
            })
            lines.append(head)
            lines.append("")
            lines.append(q_text if q_text else "（题干见源文件）")
            lines.append("")
            if EDITION == "teacher":
                lines.append("<details>")
                lines.append("<summary>📖 查看答案</summary>")
                lines.append("")
                lines.append(a_text if a_text else "（原书未提供解答）")
                lines.append("")
                lines.append("</details>")
            lines.append("")
            lines.append("---")
            lines.append("")

        write_output(os.path.join(out_dir, fname), "\n".join(lines))
        print(f"  {fname}: {len(items)} 题")

    # 生成目录（题数以实际入书为准；待分类题只进告警，不进目录）
    total_q = sum(len(v) for v in groups.values())

    toc = []
    toc.append("---")
    toc.append(f'title: "习题书 · {module}（目录 · {EDITION_LABEL}）"')
    toc.append("type: 目录")
    toc.append(f"edition: {EDITION}")
    toc.append(f"updated: {TODAY}")
    toc.append(f"question_count: {total_q}")
    toc.append("---")
    toc.append("")
    toc.append(f"# {module} · 目录（{EDITION_LABEL}）")
    toc.append("")
    toc.append(f"> **总题数**：{total_q} ｜ **章数**：{len(groups)}")
    toc.append("")
    for (num, name), items in groups.items():
        dc = collections.Counter(x["difficulty"] for x in items)
        dstr = " ".join(f"d{i}={dc.get(i, 0)}" for i in range(1, 6))
        toc.append(f"{num}. [[{num}-{name}|第 {num} 章 {name}]] — {len(items)} 题（{dstr}）")
    toc.append("")

    write_output(os.path.join(out_dir, "目录.md"), "\n".join(toc))

    # ---- 来源索引（全书聚合）：非真题题目的来源统一登记到书末总索引 ----
    # 真题题目在正文小节头已带「第X届初赛」标注，此处不再重复；只收真题之外的来源。
    non_exam = [r for r in index_rows if not r["exam"]]
    for r in non_exam:
        ALL_NON_EXAM.append({
            "module": module,
            "num": r["num"],
            "title": r["title"],
            "source": r["source"],
            "fid": r["fid"],
        })
    if non_exam:
        print(f"  {module} 来源索引汇总: {len(non_exam)} 条非真题来源")

    print(f"\n{module} 习题书生成完成: {len(groups)} 章, {total_q} 题")


# 化学原理习题书（酸碱置于化学平衡之前，避免 submodule「酸碱平衡」误入第 2 章）
CHEM_MAP = [
    (1, "热力学", ["热力学", "焓", "熵", "gibbs", "hess", "盖斯", "燃烧", "生成焓", "能量变化", "热化学"]),
    (3, "化学动力学", ["动力学", "速率", "半衰期", "活化能", "arrhenius", "反应机理", "稳态近似"]),
    (4, "氧化还原与电化学", ["电化学", "电极", "电势", "原电池", "电池", "电解", "氧化还原", "歧化", "latimer", "nernst", "e-ph", "kolbe", "电镀"]),
    (5, "溶液与酸碱平衡", ["酸碱", "滴定", "缓冲", "解离", "溶度积", "ksp", "分布系数"]),
    (2, "化学平衡", ["平衡", "转化率", "勒夏特列", "化学势", "相图"]),
]

# 有机化学习题书
ORGANIC_MAP = [
    (1, "结构基础与波谱分析", ["结构基础", "波谱", "nmr", "电子效应", "共轭效应", "酸碱质子", "基础概念", "同分异构", "共振", "不饱和度", "取代基效应", "吸光光度"]),
    (2, "立体化学", ["立体化学", "立体电子效应", "立体选择性", "非对映选择性", "构象", "区域选择性", "不对称合成", "对映异构", "手性分子"]),
    (3, "烷烯炔与加成反应", ["烷", "烯烃", "炔", "加成反应", "共轭加成", "烯烃的亲电加成", "硼氢化", "羟汞化", "臭氧化", "环氧化", "亲电加成"]),
    (4, "芳香化合物与亲电取代", ["芳香", "芳香反应", "亲电取代", "定位效应", "傅-克", "硝化", "磺化", "vilsmeier"]),
    (5, "亲核取代、消除与羧酸衍生物", ["亲核取代", "消除反应", "羧酸衍生物", "消除与重排", "sn1", "sn2", "e1", "e2", "卤代烃", "醇", "醚"]),
    (6, "羰基化学与缩合反应", ["羰基", "缩合反应", "aldol", "claisen", "烯醇", "缩醛", "亚胺", "wittig", "michael", "硫硅磷", "羧酸", "羧酸衍生物", "醛", "酮", "swern", "achmatowicz", "knoevenagel", "羟醛", "缩合"]),
    (7, "金属有机与偶联反应", ["金属有机", "有机金属", "金属催化", "grignard", "格氏", "偶联", "suzuki", "heck", "negishi", "钯催化"]),
    (8, "周环反应与自由基", ["周环", "环加成", "自由基", "重排", "光化学", "diels-alder", "电环化", "人名反应", "pinacol", "beckmann"]),
    (9, "杂环化合物与含杂原子有机物", ["杂环", "含杂原子", "硫化学", "硫硅磷", "含氮", "含硫", "含磷", "含硅"]),
    (10, "有机合成设计", ["有机合成", "全合成", "逆合成", "保护基", "化学选择性", "合成设计", "合成策略", "路线设计"]),
    (11, "反应机理与推断", ["反应机理", "活性中间体", "方法学分析", "反应动力学", "机理与推断", "中间体", "推断"]),
    (12, "高分子化学", ["高分子", "聚合", "开环聚合", "加聚", "缩聚"]),
]
ORGANIC_EXCLUDE = {"结构化学基础", "元素化学", "中级无机化学", "机械力化学", "无机化学", "配位化学", "配合物", "吸光光度法", "化学平衡与转化率", "离子交换"}

# 元素与分析习题书
YSFX_MAP = [
    (1, "化学基础与计量", ["化学基础", "有效数字", "气体", "气体定律", "溶液", "溶液和胶体", "溶液依数性", "热力学", "化学计量", "物理化学", "化学史", "同位素", "核化学", "放射性衰变"]),
    (2, "离子反应与方程式", ["反应方程式", "离子反应", "化学方程式", "氧化还原方程式", "配平", "方程式书写"]),
    (3, "主族元素化学", ["碱金属", "碱土金属", "硼族", "碳族", "氮族", "氧族", "卤素", "氢和稀有气体", "主族元素", "硼化学", "铍化学", "铝", "硅", "磷", "硫", "氯", "氟", "溴", "碘", "氢", "碲", "锗", "卤化物", "多硼酸根", "分布图"]),
    (4, "过渡元素化学", ["钛副族", "钒副族", "铬副族", "锰副族", "铁系", "铂系", "铜副族", "锌副族", "过渡元素", "钛", "钒", "铬", "锰", "铁", "钴", "镍", "铜", "锌", "铂", "钯", "锇", "钪", "镍化学"]),
    (5, "元素推断", ["推断技术", "元素推断", "元素化学推断", "元素化学与离子推断", "元素化学与定量计算"]),
    (6, "化学分析", ["溶液与化学分析", "滴定分析", "沉淀溶解平衡", "氧化还原滴定", "碘量法", "分析", "水中平衡", "萃取", "分配定律", "溶解度", "络合滴定", "分光光度", "光度", "容量", "误差", "重量分析", "返滴定", "选择性滴定", "EDTA"]),
]

# 结构化学习题书
STRUCTURE_MAP = [
    (1, "原子结构", ["原子", "量子", "核外", "波函数", "电离", "光谱", "电子排布", "屏蔽效应", "电子亲和能", "放射性衰变", "核化学", "核反应", "超重元素", "外星周期系", "二维周期系"]),
    (2, "分子结构与化学键", ["分子结构", "化学键", "共价键", "价键", "杂化", "vsepr", "lewis", "等电子体", "离域π键", "分子轨道", "氢键", "价键理论", "离子键", "化学键与分子结构", "分子结构与VSEPR"]),
    (3, "晶体结构", ["晶体", "晶胞", "晶格", "点阵", "堆积", "布拉维", "晶面", "晶胞计算", "晶胞计数", "密堆积", "金刚石", "NaCl", "ZnS", "钙钛矿", "沸石", "分子筛", "富勒烯", "六方氮化硼", "合金", "冰晶石", "NiAs", "高温超导", "缺陷晶体", "表面化学", "超四面体", "聚八面体", "最密堆积", "固体电解质", "金属晶体", "离子晶体", "储氢", "二维层状", "三维骨架", "冰"]),
    (4, "配位化学", ["配位", "配合物", "晶体场", "分裂能", "配位数", "配体", "配合物结构", "配合物组成", "配合物化学", "配位立体异构", "配位场理论", "配位催化", "金属有机", "配合物磁性", "配合物杂化"]),
    (5, "对称性与群论", ["对称性", "群论", "点群", "分子对称性"]),
    (6, "超分子与材料化学", ["超分子", "氢键网络", "三维骨架", "分子筛", "沸石", "MOF", "胶束", "表面化学", "纳米", "材料", "二维层状", "固体电解质", "锂离子电池"]),
    (7, "结构化学基础", ["结构化学基础", "化学计量", "物理化学", "无氧实验操作"]),
    (8, "结构推断与综合", ["推断", "推导", "综合", "化合物分子式", "结构推导", "聚合阴离子", "计算化学", "密度"]),
]


# ---------------- 半截 math 源文件修复器（--fix-math） ----------------

_SUB_TRANS = str.maketrans("0123456789+-", "₀₁₂₃₄₅₆₇₈₉₊₋")
_SUP_TRANS = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")

# X$_2$ / X$_{2}$ / Ni(CO) $_{4}$ → X₂（$ 前为字母/右括号/中文，允许一个空格）
MATH_HALF_SUB_RE = re.compile(r"(?<=[A-Za-z\)\]一-鿿])[ ]?\$_\{?([0-9+-]+)\}?\$")
# X$^{2+}$ / X$^+$ / d$^1$ / L$^{-1}$ → X²⁺ / d¹ / L⁻¹
MATH_HALF_SUP_RE = re.compile(r"(?<=[A-Za-z\)\]一-鿿])[ ]?\$\^\{?([+-]?[0-9]+[+-]?|[+-])\}?\$")
# $^{18}$O → ¹⁸O（同位素前置写法）
MATH_ISO_RE = re.compile(r"\$\^\{?([0-9]+)\}?\$([A-Z][a-z]?)")


def fix_math_text(s):
    """半截 math → Unicode 上下标；跳过围栏代码块。返回 (新文本, 替换次数)。"""
    n = 0

    def _counted(pattern, func, text):
        nonlocal n
        new, cnt = pattern.subn(func, text)
        n += cnt
        return new

    parts = re.split(r"(```.*?```)", s, flags=re.S)
    for i in range(0, len(parts), 2):
        p = parts[i]
        p = _counted(MATH_ISO_RE, lambda m: m.group(1).translate(_SUP_TRANS) + m.group(2), p)
        p = _counted(MATH_HALF_SUB_RE, lambda m: m.group(1).translate(_SUB_TRANS), p)
        p = _counted(MATH_HALF_SUP_RE, lambda m: m.group(1).translate(_SUP_TRANS), p)
        parts[i] = p
    return "".join(parts), n


def fix_math_mode():
    """扫描 04-题库全部源文件修复半截 math；dry-run 只列清单，--write 才落盘。"""
    changed = 0
    total_subs = 0
    for root, dirs, fs in os.walk(BASE):
        for fn in sorted(fs):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            s = open(path, encoding="utf-8", errors="replace").read()
            new, n = fix_math_text(s)
            if new != s:
                changed += 1
                total_subs += n
                rel = os.path.relpath(path, BASE).replace(os.sep, "/")
                print(f"  [fix-math] {rel}: {n} 处")
                if WRITE:
                    with open(path, "w", encoding="utf-8", newline="") as f:
                        f.write(new)
    mode = "实写" if WRITE else "dry-run（加 --write 才落盘）"
    print(f"\n[fix-math] {mode}：{changed} 个文件，共 {total_subs} 处替换")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    if FIX_MATH:
        fix_math_mode()
        raise SystemExit(0)

    if not WRITE:
        print("当前为 dry-run（不落盘）；确认无误后请加 --write 重新执行。")

    book_root = f"04-课件/习题集/习题书-{EDITION_LABEL}"

    build_book("化学原理", f"{book_root}/第一篇-化学原理", CHEM_MAP)

    build_book("有机化学", f"{book_root}/第三篇-有机化学", ORGANIC_MAP, exclude_subs=ORGANIC_EXCLUDE)

    build_book("元素与分析", f"{book_root}/第四篇-元素与分析", YSFX_MAP)

    build_book("结构化学", f"{book_root}/第二篇-结构化学", STRUCTURE_MAP)

    # ---- 全书来源索引（附于成书最后）：聚合四篇的全部非真题来源 ----
    if ALL_NON_EXAM:
        idx = []
        idx.append("---")
        idx.append(f'title: "习题书（来源索引 · {EDITION_LABEL}）"')
        idx.append("type: 索引")
        idx.append(f"edition: {EDITION}")
        idx.append(f"updated: {TODAY}")
        idx.append(f"question_count: {len(ALL_NON_EXAM)}")
        idx.append("---")
        idx.append("")
        idx.append(f"# 习题书 · 来源索引（{EDITION_LABEL}）")
        idx.append("")
        idx.append(f"> 收录非真题题目 **{len(ALL_NON_EXAM)}** 条（真题已在正文标注届次来源）。")
        idx.append("> 排序：先按来源，再按篇·题号。")
        idx.append("")
        by_src = collections.OrderedDict()
        for r in sorted(ALL_NON_EXAM, key=lambda r: (r["source"], r["module"], r["num"])):
            by_src.setdefault(r["source"] or "（来源未填）", []).append(r)
        for src, rows in by_src.items():
            idx.append(f"## {src}")
            idx.append("")
            idx.append("| 篇·题号 | 标题 | 保真 |")
            idx.append("|:--|:--|:--|")
            for r in rows:
                tag = "🟢" if "逐字" in r["fid"] else ("🔵" if "自编" in r["fid"] else "🟡")
                idx.append(f"| {r['module']}·{r['num']} | {r['title'] or '(无标题)'} | {tag} |")
            idx.append("")
        write_output(os.path.join(book_root, "来源索引.md"), "\n".join(idx))
        print(f"  全书来源索引: {len(ALL_NON_EXAM)} 条非真题来源 → {book_root}/来源索引.md")

    # ---- 质量告警汇总（两篇版本共用，按类型聚合）----
    if WARNINGS:
        print("\n================ 质量告警汇总 ================")
        for kind, items in sorted(WARNINGS.items(), key=lambda kv: -len(kv[1])):
            print(f"\n[{kind}] 共 {len(items)} 处")
            for msg in items[:9999]:
                print(f"  - {msg}")
