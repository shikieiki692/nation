#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""md_sanitize.py —— Markdown 净化的**唯一事实源**。

## 为什么有这个模块
2026-09-20 发现同类净化逻辑散落在 **4 处**（`build-all-handout-docx.py` 1 处 +
`build_module_book.py` / `gen_r1.py` / `gen_r1_mixed.py` 各 1 处）——
同一类知识 4 个副本，必然漂移。本模块把它们收敛为单一实现，4 个消费方一律 import。

## 设计原则
1. **顺序即语义**：LaTeX 宏替换必须「最具体 → 最一般」。
   反例（真实踩过）：把 `\\AA` 裸替换成 `\\text{Å}`，则原稿 `\\text{\\AA}` 会变成
   `\\text{\\text{Å}}` **嵌套** → texmath 转不了，把本来正确的文件改坏。
   管线自身的处理器有顺序保护，源侧裸替换绕过了它 —— 本模块把顺序固化下来。
2. **只认已知签名**：只动 `class="mineru-algorithm"` 这一种 div；
   `<details>` / `<summary>`（答案折叠块）是**合法**的，一律不碰。
3. **CRLF 安全**：正则容 `\\r`；不改动行尾风格。
4. **幂等**：同一文本跑两次结果相同（有单测）。

## 用法
    import md_sanitize as san
    text = san.sanitize(text)          # 一次跑全部（推荐）
    text = san.strip_mineru_div(text)  # 只剥 div
    text = san.fix_aa(text)            # 只修 \\AA
    text = san.fix_tab_pollution(text) # 只复位 TAB 残名
"""
import re

__all__ = ["strip_mineru_div", "fix_r_break", "fix_aa", "fix_text_nesting",
           "fix_text_inner_cmd", "fix_html_entities_in_math", "fix_dollar_digit",
           "fix_double_backslash_cmd", "fix_tab_pollution", "sanitize"]

BS = chr(92)
TAB = chr(9)

# ── ① MinerU OCR 的行首 div 包裹块 ───────────────────────────────────────
# CommonMark 系解析器（Obsidian）把行首 <div> 当 raw HTML block，
# 块内 Markdown（含 $..$）不解析 → 公式显示为源码。
# ⚠️ pandoc 的 markdown 方言会「降级」处理 div（丢标签、照常解析内部），
#    故该缺陷**只在 Obsidian 侧显形**，用 commonmark 才测得出。
_DIV_OPEN = re.compile(r'^<div\s+class="mineru-algorithm"[^>]*>[ \t\r]*$')
_DIV_CLOSE = re.compile(r"^</div>[ \t\r]*$")

# ── ② `\AA` → `\text{Å}`（**顺序不可换**，镜像 build-all-handout-docx.py L1847-1850）──
_AA_RULES = [
    (re.compile(re.escape(BS + "text{" + BS + "AA}")), BS + "text{Å}"),
    (re.compile(re.escape(BS + "mathrm{" + BS + "AA}")), BS + "text{Å}"),
    (re.compile(re.escape(BS + "AA") + r"\b"), BS + "text{Å}"),
]

# ── ③b `\text{…\text{…}…}` 同命令嵌套（宏替换顺序错造成，也见于存量）──────
# 真实案例：源侧裸替换 `\AA` → `\text{Å}` 时，原稿 `\text{\AA}` 变成
# `\text{\text{Å}}` → texmath 报 "Could not convert TeX math"。
# 这里作**安全网**：即使上游顺序错了，sanitize 也能把它压平。
# ⚠️ 2026-09-20 两轮补漏（都是实测发现的，非推测）：
#   ① 中间可带空白 —— 首版紧邻匹配 `\text{\text{`，漏掉 `\text{ \text{Å}}`
#      （实测 `03-知识点/无机和结构化学/等径球堆积.md`）；
#   ② 内层**不必紧贴开头**，外层**不必紧贴结尾** —— 首版要求二者紧贴，
#      漏掉 `\text{a\text{Å}b}` 这类。故加 `pre/post` 两段。
_TEXT_NEST = re.compile(
    re.escape(BS + "text{") + r"([^{}]*?)" + r"\s*"
    + re.escape(BS + "text{") + r"\s*([^{}]*?)\s*" + re.escape("}")
    + r"\s*([^{}]*?)" + re.escape("}")
)

# ── ③b2 `\text{…\cmd{…}…}` —— `\text` 内套**任何**命令 ────────────────────
# ⚠️ 2026-09-20 实测（不是推测，逐例跑过 pandoc+texmath）：
#   ① `$\text{中文}$`              → ✅ 1 个 oMath
#   ② `$\text{中\textbf{X}}$`      → ❌ Could not convert，公式不渲染
#   ③ `$\text{中}\textbf{X}$`      → ✅ 好   ← **修法依据**
#   ④ `$\textbf{X}$`               → ✅ 好
#   ⑤ `$\text{中\mathrm{X}}$`      → ❌ 坏（所以不限 \textbf，任何命令都会坏）
#   ⑥ `$\mathrm{中\textbf{X}}$`    → ✅ 好   ← **所以规则必须锚定外层是 `\text`**，
#                                             不能泛化到所有命令（泛化会误伤 ⑥）
#   ⑦ `$\text{中 \textbf{X}}$`     → ❌ 坏（带空格同坏）
#   ⇒ 规律：**`\text{}` 内部只要再出现 `\<命令>{`，texmath 就拒绝整个公式**。
#   ⇒ 修法：把内层命令**提出到 `\text{}` 之外**（③ 已证可行）。
# 之前 ③b 只处理 `\text{\text{X}}`（同命令、且内层必须紧贴开头），漏了本形态。
_TEXT_INNER_CMD = re.compile(
    re.escape(BS + "text{")
    + r"([^{}]*?)"                        # 前置文本（惰性）
    + re.escape(BS) + r"([a-zA-Z]+)\{"    # 内层命令名
    + r"([^{}]*)"                         # 内层参数（无花括号）
    + re.escape("}")
    + r"([^{}]*?)"                        # 后置文本
    + re.escape("}")
)


def _hoist_inner_cmd(m):
    pre, cmd, arg, post = m.group(1), m.group(2), m.group(3), m.group(4)
    if cmd == "text":                     # 同命令：直接并回一段 \text
        return BS + "text{" + pre + arg + post + "}"
    parts = []
    if pre.strip():
        parts.append(BS + "text{" + pre + "}")
    parts.append(BS + cmd + "{" + arg + "}")
    if post.strip():
        parts.append(BS + "text{" + post + "}")
    return "".join(parts)


def fix_text_inner_cmd(text: str, limit: int = 8) -> str:
    """把 `\\text{…\\cmd{…}…}` 里的内层命令**提出**到 `\\text{}` 外。

    实测 `\\text{中\\textbf{X}}` 会让 texmath 拒绝整个公式，而 `\\text{中}\\textbf{X}` 正常。
    每轮先压平同命令嵌套、再提命令，迭代至稳定（上限 `limit` 轮）。
    """
    for _ in range(limit):
        new = _TEXT_NEST.sub(_flatten_same, text)
        new = _TEXT_INNER_CMD.sub(_hoist_inner_cmd, new)
        if new == text:
            break
        text = new
    return text


# ── ④ `\r` 家族断行（与「`\t` → 真 TAB」是孪生形态）──────────────────────
# 机制：导入时把 `\r`（**反斜杠 + r**）当转义序列解析 ⇒ 变成真换行，
# 于是 `\rm` / `\rho` / `\rightarrow` 等**以 r 开头**的命令被从中间劈开：
#   原： `… $\rm B(SH)_3$ |`
#   坏： `… $`  /换行/  `m B(SH)_3$ |`
# 后果：上一行以**未闭合的 `$`** 收尾 → 数学域断裂；表格行也被劈成两行。
#
# ⭐ 还原**统一是插入 `\r` 两字符** —— 因为污染永远只吃掉命令开头的 `\` 和 `r`。
#    残尾只用于**识别**（判断这确实是本条签名），不决定插入内容。
# 三重护栏（任一不满足就不动），防误合两行普通文本：
#   ① 本行以已知残尾开头，且残尾后紧跟边界字符（空白/`{`/`$`/`\`/标点）
#   ② 上一行以 `$` 收尾且该行 `$` 计数为**奇数**（= 数学域未闭合）
#   ③ 本行含 `$`，且合并后整行 `$` 计数变为**偶数**
_R_CMD_TAILS = [
    "ightleftharpoons", "ightleftarrows", "ightrightarrows", "ightarrowtail",
    "ightsquigarrow", "ightharpoonup", "ightharpoondown", "ightthreetimes",
    "ightarrow", "ightgroup", "Rightarrow", "isingdotseq",
    "ho", "angle", "floor", "ceil", "brace", "vert", "Vert", "lap", "times", "m",
]
_R_BOUND = set(" {" + "$" + "\\" + ",.;:)]}")


def _r_tail_of(body: str):
    """若 body 以某已知残尾开头（且后接边界），返回该残尾，否则 None。"""
    for t in _R_CMD_TAILS:
        if body.startswith(t):
            rest = body[len(t):]
            if not rest or rest[0] in _R_BOUND:
                return t
    return None


def fix_r_break(text: str):
    """把 `\\r` 家族被劈开的行**合回**（支持级联：一行含多个被劈命令）。

    ⚠️ 为什么护栏必须严（实测踩过）：
    `m` 这个残尾**本身极弱** —— `$$` 显示块里的 `m v r = nh/2π`（Bohr 公式）、
    `m_{S} = 1, S = 1`（量子数）都以 `m ` 开头且**完全合法**。
    真正的判据不是「本行以 `m` 开头」，而是「**上一行有未闭合的 `$`**」——
    即污染把**行内**数学域劈断了。故：
      ① 上一行以 `$` 收尾且该行 `$` 计数为**奇数**（数学域开着）；
      ② 本行含 `$`，且以已知残尾 + 边界字符开头；
      ③ 级联吞并后续残尾行，**最终整行 `$` 计数必须为偶数**才落盘
         （现实中一行可出现 2 个 `\\rm` → 被劈成 3 行）。
    """
    lines = text.split("\n")
    out = []
    n = 0
    i = 0
    while i < len(lines):
        ln = lines[i]
        body = ln.rstrip("\r")
        tail = _r_tail_of(body)
        if tail and out and "$" in body:
            prev_body = out[-1].rstrip("\r")
            if prev_body.endswith("$") and prev_body.count("$") % 2 == 1:
                cur = prev_body
                j = i
                while j < len(lines):
                    b = lines[j].rstrip("\r")
                    if j > i and (_r_tail_of(b) is None or "$" not in b):
                        break
                    cur = cur + BS + "r" + b
                    if cur.count("$") % 2 == 0:
                        break
                    j += 1
                if cur.count("$") % 2 == 0:          # ③ 只有配平才落盘
                    had_cr = out[-1].endswith("\r")
                    out[-1] = cur + ("\r" if had_cr else "")   # 行尾风格守恒
                    n += 1
                    i = j + 1
                    continue
        out.append(ln)
        i += 1
    return "\n".join(out), n


# ── ③c 数学域内的 HTML 实体：`&lt;` / `&gt;` / `&amp;` ──────────────────────
# texmath 见到 `&` 直接报 `unexpected '&'`，整个公式不渲染。
# ⚠️ **只在数学域内替换**：散文里的 `&lt;` 是**正确**的 HTML 转义，
#    pandoc 会把它还原成 `<`；动了反而破坏。故必须按域处理。
_ENTITIES = ((r"&lt;", "<"), (r"&gt;", ">"), (r"&amp;", "&"), (r"&nbsp;", " "))
_RE_MATH_SPAN = re.compile(
    r"\$\$.*?\$\$"                       # 显示公式
    r"|(?<!\\)\$(?!\$)(?:\\.|[^$\n])*(?<!\\)\$"   # 行内公式
    , re.DOTALL
)

# ── ③d 闭合 `$` 紧跟 ASCII 数字（pandoc `tex_math_dollars` 的**邻接规则**）──
# pandoc 手册：行内 `$…$` 的**闭合 `$` 右边不能紧跟数字**，否则整个 `$…$`
#   不被认作公式 → `$…$` 原样落进正文。**不报转换失败**（所以闸门 A 栏只数到字面 `$`）。
#   实测（`:markdown+tex_math_dollars` + 预处理）：
#     `$\times$2`      → 产物 `$$2`，字面 `$`×2、oMath 0   ❌
#     `$\times$ 2`     → 产物 `×2`，字面 `$` 0、oMath 1    ✅  ← 修法依据
#   另两条边界也一并实测过（用来划范围）：
#     `2$a$`（开 `$` 前是数字）→ ✅ 正常；`$a$ 2`（闭 `$` 后是空格）→ ✅ 正常；
#     `$c$²`（闭 `$` 后是**上标 2** U+00B2）→ ✅ 正常
#     （pandoc 用 Haskell `Data.Char.isDigit`，**只认 ASCII 0-9**）。
# 修法：把紧跟的数字串**移进数学域**（`$\times$2` → `$\times 2$`），产物仍为 `×2`。
# ⚠️ **必须窄**（这是本会话第三次「代理指标要划边界」的教训）：
#   只认「数学域内容**以 LaTeX 命令结尾**」的形态 —— 即 `\<字母…>$<数字>`。
#   若放宽成任意 `$…$`+数字（如价格 `$300 … $500`、`$x$2`），
#   会**把散文/价格误当公式改造**（实测：`$300 与 $500` 会被配成一对）。
_DD = re.compile(r"\$([^$\n]*?\\[a-zA-Z]+)\$([0-9]+(?:\.[0-9]+)?)")


def _dd_repl(m):
    return "$" + m.group(1) + " " + m.group(2) + "$"


def fix_dollar_digit(text: str) -> str:
    """`$…\\cmd$<数字>` → `$…\\cmd <数字>$`（把数字移进数学域，救回被吞的公式）。

    只动「域内容以 LaTeX 命令结尾」的形态；行内代码（`` `…` ``）不碰。
    """
    parts = re.split(r"(`[^`]*`)", text)
    for i in range(0, len(parts), 2):          # 偶数下标 = 非代码段
        parts[i] = _DD.sub(_dd_repl, parts[i])
    return "".join(parts)


# ── ③e `\\<字母命令>` 出现在 **array 类环境之外**（多了一个反斜杠）──────────
# 机制：`\\`（换行）**只在 array/cases/aligned 等环境内合法**（本会话实测：
#   `$a \\ b$` ❌ 而 `\begin{cases}…\\…\end{cases}` ✅）。
#   导入/OCR 常把 `\mathrm` 误写成 `\\mathrm` —— 在环境外就是一个非法的 `\\`，
#   texmath 直接报错、整个公式不渲染。
#   实测实例：`$K_{\\mathrm{sp}}$`、`$s = \\sqrt{…}$`、`\\text{…} = \\frac{1}{2}\\times\\text{…}`
#   （`03-知识点/化学原理/溶度积.md` 一处文件就有 103 处）。
# ⚠️ **必须环境感知**：环境**内**的 `\\` 是合法换行，绝不能碰。
# 同时必须跳过**代码围栏 / 行内代码**（那些 `\\` 是 Windows 路径、代码示例，合法）。
_DB_CMD = re.compile(re.escape(BS + BS) + r"([a-zA-Z])")
_RE_BEGIN = re.compile(re.escape(BS) + r"begin\{")
_RE_END = re.compile(re.escape(BS) + r"end\{")


def fix_double_backslash_cmd(text: str) -> str:
    """把环境之外的 `\\\\<字母>` 减成一个 `\\`（还原被写坏的 `\\mathrm` 等）。

    环境深度按 `\\begin{` / `\\end{` 位置扫描；代码围栏与行内代码先掩码。
    """
    lines = text.split("\n")
    mask = []                       # 要掩码的区间
    idx = 0
    # ① frontmatter：值里可能有 Windows 路径（`C:\\Users\\…`），绝不能动
    if lines and lines[0].strip() == "---":
        for k in range(1, len(lines)):
            if lines[k].strip() == "---":
                mask.append((0, sum(len(x) + 1 for x in lines[:k + 1])))
                break
    fence = False
    for ln in lines:
        st = ln.strip()
        if st.startswith("```") or st.startswith("~~~"):
            fence = not fence
            mask.append((idx, idx + len(ln)))
        elif fence:
            mask.append((idx, idx + len(ln)))
        idx += len(ln) + 1
    for m in re.finditer(r"`[^`]*`", text):
        mask.append((m.start(), m.end()))
    chars = list(text)
    for a, b in mask:
        for i in range(a, min(b, len(chars))):
            chars[i] = " "
    masked = "".join(chars)

    for _ in range(3):              # 迭代，兼顾 `\\\\mathrm` 这类
        dels = []
        depth = 0
        i = 0
        while i < len(masked):
            mb = _RE_BEGIN.match(masked, i)
            me = _RE_END.match(masked, i)
            mm = _DB_CMD.match(masked, i)
            if mb:
                depth += 1
                i = mb.end()
                continue
            if me:
                depth = max(0, depth - 1)
                i = me.end()
                continue
            if mm:
                if depth == 0:
                    dels.append(i)
                i = mm.end()
                continue
            i += 1
        if not dels:
            break
        ds = set(dels)
        text = "".join(c for k, c in enumerate(text) if k not in ds)
        masked = "".join(c for k, c in enumerate(masked) if k not in ds)
    return text


# ── ③ TAB 污染：`\t` 被写成真制表符 U+0009，LaTeX 命令断头 ────────────────
# 例如 `$\text{Pa}$` 实际存成 `$<TAB>ext{Pa}$`。
# 窄规则：只认 TAB 后跟可识别的 LaTeX 残名，**不碰表格对齐 TAB**。
_TAB_RESID = re.compile(TAB + r"(ext(?:bf|it|rm|tt|sc|sl)?)\{")


def _flatten_same(m):
    """`\\text{pre\\text{arg}post}` → `\\text{pre+arg+post}`（两侧空白剥除）。"""
    pre = (m.group(1) or "").strip()
    arg = m.group(2) or ""
    post = (m.group(3) or "").strip()
    return BS + "text{" + pre + arg + post + "}"


def fix_text_nesting(text: str, limit: int = 8) -> str:
    """压平 `\\text{…\\text{…}…}` → `\\text{…}`（含前后文与空白，迭代至稳定）。

    迭代是必要的：`\\text{ \\text{a\\text{b}}}` 需两轮才能降到 `\\text{ab}`。
    """
    for _ in range(limit):
        new = _TEXT_NEST.sub(_flatten_same, text)
        if new == text:
            break
        text = new
    return text


def fix_html_entities_in_math(text: str) -> str:
    """把**数学域内**的 HTML 实体还原成裸字符（散文里的保持不动）。

    `$x &lt; 10^{-8}$` → `$x < 10^{-8}$`（否则 texmath 报 unexpected '&'）。
    """
    def _repl(m):
        seg = m.group(0)
        for pat, rep in _ENTITIES:
            seg = re.sub(pat, rep, seg)
        return seg
    return _RE_MATH_SPAN.sub(_repl, text)


def strip_mineru_div(text: str) -> str:
    """成对删除 `<div class="mineru-algorithm" …>` 与其 `</div>`，保留块内内容。

    开标签后若上一行与本行都非空，补一个空行以保证块级分隔
    （否则内容仍可能被前一个 HTML 块吞掉）。
    """
    lines = text.split("\n")
    out = []
    depth = 0
    pending_sep = False
    for ln in lines:
        if _DIV_OPEN.match(ln.rstrip("\r")):
            depth += 1
            pending_sep = True
            continue
        if depth and _DIV_CLOSE.match(ln.rstrip("\r")):
            depth -= 1
            continue
        if pending_sep:
            pending_sep = False
            if out and out[-1].strip() and ln.strip():
                out.append("")
        out.append(ln)
    return "\n".join(out)


def fix_aa(text: str) -> str:
    """`\\AA` → `\\text{Å}`，**按「最具体 → 最一般」顺序**执行。

    顺序若反，`\\text{\\AA}` 会变成 `\\text{\\text{Å}}` 嵌套（真实踩过）。
    """
    for pat, rep in _AA_RULES:
        text = pat.sub(rep.replace(BS, "\\\\"), text)
    return text


def fix_tab_pollution(text: str) -> str:
    """把 TAB 残名 `<TAB>ext{…}` 复位为 `\\text{…}`（含 \\textbf 等家族）。

    只认「TAB + LaTeX 残名 + `{`」，**不碰表格对齐 TAB**。
    """
    return _TAB_RESID.sub(lambda m: BS + "text" + (m.group(1) or "") + "{", text)


def sanitize(text: str) -> str:
    """一次跑全部净化。**顺序有意固定**：
    结构类先（div 剥壳 → `\\r` 断行合回）→ 宏替换（改内容）→ 文本命令嵌套（安全网）
    → 数学域内实体 → TAB 复位。

    ⚠️ 顺序约束：
    - `fix_aa` 会**产生** `\\text{…}`（`\\AA` → `\\text{Å}`），故必须在文本嵌套修复**之前**；
    - `fix_r_break` 会**改行结构**（合行），须在任何按行扫描的规则之前。
    """
    text = strip_mineru_div(text)
    text, _ = fix_r_break(text)
    text = fix_aa(text)
    text = fix_double_backslash_cmd(text)   # 须在文本嵌套修复**之前**（可能产生 `\text{\text{…}}`）
    text = fix_text_inner_cmd(text)      # 内含 fix_text_nesting，可处理前后文/空白
    text = fix_html_entities_in_math(text)
    text = fix_dollar_digit(text)
    text = fix_tab_pollution(text)
    return text
