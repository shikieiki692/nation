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

__all__ = ["strip_mineru_div", "fix_aa", "fix_text_nesting",
           "fix_html_entities_in_math", "fix_tab_pollution", "sanitize"]

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

# ── ③b `\text{\text{X}}` 嵌套（由宏替换顺序错造成，也见于存量）────────────
# 真实案例：源侧裸替换 `\AA` → `\text{Å}` 时，原稿 `\text{\AA}` 变成
# `\text{\text{Å}}` → texmath 报 "Could not convert TeX math"。
# 这里作**安全网**：即使上游顺序错了，sanitize 也能把它压平。
# ⚠️ 2026-09-20 补：**中间可带空白**。首版用 `re.escape(BS+"text{"+BS+"text{")` 紧邻匹配，
#    漏掉了存量里的 `\text{ \text{Å}}` 形态（实测 `03-知识点/无机和结构化学/等径球堆积.md`）。
_TEXT_NEST = re.compile(
    re.escape(BS + "text{") + r"\s*" + re.escape(BS + "text{")
    + r"\s*([^{}]*?)\s*" + re.escape("}") + r"\s*" + re.escape("}")
)

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

# ── ③ TAB 污染：`\t` 被写成真制表符 U+0009，LaTeX 命令断头 ────────────────
# 例如 `$\text{Pa}$` 实际存成 `$<TAB>ext{Pa}$`。
# 窄规则：只认 TAB 后跟可识别的 LaTeX 残名，**不碰表格对齐 TAB**。
_TAB_RESID = re.compile(TAB + r"(ext(?:bf|it|rm|tt|sc|sl)?)\{")


def fix_text_nesting(text: str) -> str:
    """压平 `\\text{\\text{X}}` → `\\text{X}`（含中间带空白的形态）。"""
    return _TEXT_NEST.sub(lambda m: BS + "text{" + (m.group(1) or "") + "}", text)


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
    div 先（改结构）→ 宏后（改内容）→ 嵌套压平（安全网）→ TAB 复位。
    """
    text = strip_mineru_div(text)
    text = fix_aa(text)
    text = fix_text_nesting(text)
    text = fix_html_entities_in_math(text)
    text = fix_tab_pollution(text)
    return text
