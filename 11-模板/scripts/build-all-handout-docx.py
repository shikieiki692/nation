#!/usr/bin/env python3
"""
Batch converter: Markdown student handouts → uniformly formatted .docx (v2)

三段式管线：
  1. Preprocess  — 剥 YAML frontmatter、解 [[wiki-link]]、预处理 \\ce{} 为 \\text{}
  2. Pandoc      — pypandoc 转换 markdown → docx（自动 LaTeX → OMML 公式）
  3. Postprocess — python-docx 修正字体（正文 仿宋 FangSong / 标题 SimHei / 英文 TNR）

用法:
    python build-all-handout-docx.py                          # 全量转换
    python build-all-handout-docx.py --dry-run                # 预览文件列表
    python build-all-handout-docx.py --precheck-only          # 仅跑 Word 源稿预检（公式 + Mermaid）
    python build-all-handout-docx.py --file 化学平衡          # 单文件测试
    python build-all-handout-docx.py --file 原子结构 -v       # 单文件详细日志

依赖: python-docx, PyYAML, pypandoc (pandoc 3.9+)
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date as date_cls
import hashlib
import os
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any, Literal, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    from docx import Document
except ImportError:
    print("ERROR: python-docx is required. Install with: pip install python-docx", file=sys.stderr)
    sys.exit(1)

try:
    import pypandoc
except ImportError:
    print("ERROR: pypandoc is required. Install with: pip install pypandoc_binary", file=sys.stderr)
    sys.exit(1)

# Add parent dir so docx_utils can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docx_utils import _atomic_replace, postprocess_pandoc_docx
from docx_utils import add_exercise_cover

# ── Paths ────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent
HANDOUT_SRC = VAULT_ROOT / "04-课件" / "学生讲义"
HANDOUT_OUT = VAULT_ROOT / "00-首页" / "学生讲义Word"

SRC_GLOB = "*.md"

# Vault root media directory (images are here, not in handout subdir)
VAULT_MEDIA = VAULT_ROOT / "媒体仓库"

# Pandoc 转换扩展
PANDOC_EXTENSIONS = "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_tex"

# 参考模板（字体/页边距已预设好）
REFERENCE_DOC = SCRIPT_DIR / "templates" / "custom-reference.docx"
RENDER_SCRIPT = SCRIPT_DIR / "render_docx_windows.py"
CODEX_BUNDLED_PYTHON = (
    Path.home()
    / ".cache"
    / "codex-runtimes"
    / "codex-primary-runtime"
    / "dependencies"
    / "python"
    / "python.exe"
)

PRECHECK_SEVERITY_ORDER = {"ERROR": 0, "WARN": 1, "INFO": 2}


@dataclass(frozen=True)
class WordFormulaPrecheckIssue:
    severity: Literal["ERROR", "WARN", "INFO"]
    rule: str
    message: str
    line_no: int | None = None
    excerpt: str | None = None


@dataclass
class WordFormulaPrecheckReport:
    md_path: Path
    issues: list[WordFormulaPrecheckIssue]

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "ERROR")

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "WARN")

    @property
    def info_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "INFO")

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0

    def render(
        self,
        limit: int = 10,
        severities: set[str] | None = None,
    ) -> str:
        selected = [
            issue for issue in self.issues
            if severities is None or issue.severity in severities
        ]
        selected.sort(
            key=lambda issue: (
                PRECHECK_SEVERITY_ORDER.get(issue.severity, 99),
                issue.line_no or 10**9,
                issue.rule,
                issue.message,
            )
        )
        lines = [
            (
                f"[precheck] {self.md_path.name}: "
                f"{self.error_count} error(s), "
                f"{self.warning_count} warning(s), "
                f"{self.info_count} info"
            )
        ]
        shown = selected[:limit]
        for issue in shown:
            loc = f"L{issue.line_no}" if issue.line_no else "L?"
            line = f"  {issue.severity} {loc} {issue.rule}: {issue.message}"
            if issue.excerpt:
                line += f" | {issue.excerpt}"
            lines.append(line)
        remaining = len(selected) - len(shown)
        if remaining > 0:
            lines.append(f"  ... {remaining} more issue(s)")
        return "\n".join(lines)


def _dedupe_existing_paths(paths: list[Path]) -> list[Path]:
    """Return existing paths with order preserved and duplicates removed."""
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        key = str(resolved).lower()
        if key in seen or not resolved.exists():
            continue
        seen.add(key)
        result.append(resolved)
    return result


def _build_resource_path(md_path: Path, out_dir: Path) -> str:
    """Build Pandoc resource search path without copying the whole media vault."""
    paths = _dedupe_existing_paths([
        md_path.parent,
        md_path.parent / "media",
        VAULT_ROOT,
        VAULT_MEDIA,
        out_dir,
    ])
    return os.pathsep.join(str(path) for path in paths)


def _candidate_render_pythons() -> list[str]:
    """Return Python candidates for the DOCX render helper, in priority order."""
    candidates: list[str] = []
    candidates.append(sys.executable)
    env_python = os.environ.get("CODEX_PYTHON") or os.environ.get("CODEX_BUNDLED_PYTHON")
    if env_python:
        candidates.append(env_python)
    candidates.append(str(CODEX_BUNDLED_PYTHON))
    path_python = shutil.which("python")
    if path_python:
        candidates.append(path_python)

    seen: set[str] = set()
    resolved: list[str] = []
    for candidate in candidates:
        if not candidate:
            continue
        key = candidate.lower()
        if key in seen:
            continue
        seen.add(key)
        if Path(candidate).exists():
            resolved.append(candidate)
    return resolved


def _resolve_render_output_dir(docx_path: Path, render_output_dir: Path | None) -> Path | None:
    """Return the preview folder to use for a rendered DOCX."""
    if render_output_dir is None:
        return None
    return render_output_dir / f"{docx_path.stem}_render"


def _render_docx_preview(
    docx_path: Path,
    render_output_dir: Path | None = None,
    emit_pdf: bool = False,
    verbose: bool = False,
) -> Path:
    """Render a DOCX to page PNGs for visual QA."""
    if not RENDER_SCRIPT.exists():
        raise RuntimeError(f"Render script not found: {RENDER_SCRIPT}")

    output_dir = _resolve_render_output_dir(docx_path, render_output_dir)
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    for python_exe in _candidate_render_pythons():
        cmd = [
            python_exe,
            str(RENDER_SCRIPT),
            str(docx_path),
        ]
        if output_dir is not None:
            cmd.extend(["--output_dir", str(output_dir)])
        if emit_pdf:
            cmd.append("--emit_pdf")
        if verbose:
            cmd.append("--verbose")

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode == 0:
            if verbose and proc.stdout.strip():
                print(proc.stdout.rstrip(), file=sys.stderr)
            if verbose and proc.stderr.strip():
                print(proc.stderr.rstrip(), file=sys.stderr)
            return output_dir or docx_path.with_suffix("")

        failures.append(
            f"Command: {' '.join(cmd)}\n"
            f"Exit: {proc.returncode}\n"
            f"STDOUT:\n{proc.stdout}\n"
            f"STDERR:\n{proc.stderr}"
        )

    raise RuntimeError(
        "DOCX render preview failed with all Python runtimes.\n\n"
        + "\n\n".join(failures)
    )


def _blank_preserving_newlines(text: str) -> str:
    """Replace content with spaces while preserving line structure."""
    return "".join("\n" if ch == "\n" else " " for ch in text)


def _mask_pattern(text: str, pattern: str, flags: int = 0) -> str:
    """Mask regex matches with spaces while preserving newlines."""
    return re.sub(
        pattern,
        lambda m: _blank_preserving_newlines(m.group(0)),
        text,
        flags=flags,
    )


def _mask_non_formula_segments(text: str) -> str:
    """Mask code/math/embed spans so plain-text formula checks avoid false positives."""
    masked = text
    patterns = [
        (r"```.*?```", re.DOTALL),
        (r"~~~.*?~~~", re.DOTALL),
        (r"`[^`\n]+`", 0),
        (r"\$\$.*?\$\$", re.DOTALL),
        (r"\\\[.*?\\\]", re.DOTALL),
        (r"(?<!\\)\$(?!\$)(?:\\.|[^$\n])*(?<!\\)\$", 0),
        (r"\\\((?:\\.|[^\\\n])*(?<!\\)\\\)", 0),
        (r"!\[[^\]]*]\([^)]+\)", 0),
        (r"\[[^\]]*]\([^)]+\)", 0),
        (r"!?\[\[[^\]]+\]\]", 0),
        (r"<https?://[^>\s]+>", 0),
        (r"https?://\S+", 0),
    ]
    for pattern, flags in patterns:
        masked = _mask_pattern(masked, pattern, flags)
    return masked


def _count_markdown_math_expressions(text: str) -> int:
    """Approximate number of markdown/LaTeX math expressions in the text."""
    masked = text
    total = 0
    patterns = [
        (r"\$\$.*?\$\$", re.DOTALL),
        (r"\\\[.*?\\\]", re.DOTALL),
        (r"(?<!\\)\$(?!\$)(?:\\.|[^$\n])*(?<!\\)\$", 0),
        (r"\\\((?:\\.|[^\\\n])*(?<!\\)\\\)", 0),
    ]
    for pattern, flags in patterns:
        matches = list(re.finditer(pattern, masked, flags))
        total += len(matches)
        masked = _mask_pattern(masked, pattern, flags)
    return total


def _prev_significant_char(text: str, idx: int) -> str | None:
    """Return the nearest non-space char before idx, skipping closing braces."""
    i = idx - 1
    while i >= 0 and text[i].isspace():
        i -= 1
    while i >= 0 and text[i] in "}])":
        i -= 1
        while i >= 0 and text[i].isspace():
            i -= 1
    return text[i] if i >= 0 else None


def _next_significant_char(text: str, idx: int) -> str | None:
    """Return the nearest non-space char after idx, skipping opening braces."""
    i = idx
    while i < len(text) and text[i].isspace():
        i += 1
    while i < len(text) and text[i] in "{[(":
        i += 1
        while i < len(text) and text[i].isspace():
            i += 1
    return text[i] if i < len(text) else None


def _is_caption_line(line: str) -> bool:
    """Heuristic for figure/table caption lines in markdown sources."""
    stripped = line.strip()
    stripped = re.sub(r"</?center>", "", stripped, flags=re.IGNORECASE).strip()
    stripped = stripped.strip("*").strip()
    return bool(re.match(r"^(图|表)\s*(?:\d+(?:\.\d+)*|[A-Za-z])", stripped))


def _append_precheck_issue(
    issues: list[WordFormulaPrecheckIssue],
    seen: set[tuple[str, str, str, int | None, str]],
    *,
    severity: Literal["ERROR", "WARN", "INFO"],
    rule: str,
    message: str,
    line_no: int | None = None,
    excerpt: str | None = None,
) -> None:
    normalized_excerpt = " ".join((excerpt or "").strip().split())
    key = (severity, rule, message, line_no, normalized_excerpt)
    if key in seen:
        return
    seen.add(key)
    issues.append(
        WordFormulaPrecheckIssue(
            severity=severity,
            rule=rule,
            message=message,
            line_no=line_no,
            excerpt=normalized_excerpt or None,
        )
    )


def _run_word_formula_precheck(
    md_path: Path,
    source_text: str,
    processed_text: str,
) -> WordFormulaPrecheckReport:
    """Run Word handout source precheck v1 on source and preprocessed markdown."""
    issues: list[WordFormulaPrecheckIssue] = []
    seen: set[tuple[str, str, str, int | None, str]] = set()

    source_lines = source_text.splitlines()
    masked_source_lines = _mask_non_formula_segments(source_text).splitlines()
    processed_lines = processed_text.splitlines()

    critical_bare_subscript = re.compile(r"\b(?:K|Q|E|pK|v|V)_[A-Za-z][A-Za-z0-9+\-]*\b")
    generic_bare_subscript = re.compile(r"\b[A-Za-zΔ∆][A-Za-z0-9]*_[A-Za-z][A-Za-z0-9+\-]*\b")
    risky_latex_outside_math = re.compile(
        r"\\(?:frac|dfrac|sqrt|sum|int|boxed|left|right|mathrm|mathbf|overline|underline|"
        r"Delta|theta|alpha|beta|gamma|rightarrow|leftarrow|rightleftharpoons)\b"
    )
    circ_superscript = re.compile(r"\^\s*\{?\s*\\circ\s*\}?")
    caption_any_math = re.compile(r"(?<!\\)\$(?!\$)|\\\(|\\\[")
    caption_complex_math = re.compile(
        r"(?<!\\)\$(?!\$)|\\\(|\\\[|\\(?:frac|sqrt|ce|mathrm|Delta|theta|boxed|overset|underset)|[_^]"
    )
    mermaid_fence_start = re.compile(
        r"^[ \t]*(?P<fence>`{3,}|~{3,})[ \t]*mermaid(?:\s+.*)?$",
        re.IGNORECASE,
    )
    md_embed = re.compile(r"!\[\[([^\]]+\.md)(?:\|([^\]]*))?\]\]", re.IGNORECASE)

    in_mermaid_block = False
    mermaid_fence_char = ""
    mermaid_fence_len = 0
    mermaid_start_line: int | None = None
    mermaid_excerpt_lines: list[str] = []
    in_html_comment = 0  # 多行 HTML 注释（<!-- ... -->）深度计数

    for idx, raw_line in enumerate(source_lines, start=1):
        if not in_mermaid_block:
            mermaid_start = mermaid_fence_start.match(raw_line)
            if mermaid_start:
                fence_token = mermaid_start.group("fence")
                in_mermaid_block = True
                mermaid_fence_char = fence_token[0]
                mermaid_fence_len = len(fence_token)
                mermaid_start_line = idx
                mermaid_excerpt_lines = [raw_line.strip()]
                continue
        else:
            stripped = raw_line.strip()
            if stripped and len(mermaid_excerpt_lines) < 2:
                mermaid_excerpt_lines.append(stripped)
            if re.match(rf"^[ \t]*{re.escape(mermaid_fence_char)}{{{mermaid_fence_len},}}[ \t]*$", raw_line):
                excerpt = " | ".join(mermaid_excerpt_lines[:2])
                _append_precheck_issue(
                    issues,
                    seen,
                    severity="ERROR",
                    rule="mermaid_block_word_incompatible",
                    message="检测到 Mermaid 代码块；学生讲义源稿不要直接保留 Mermaid，请改成 `![[media/...png]]` 或改写为表格/列表",
                    line_no=mermaid_start_line,
                    excerpt=excerpt,
                )
                in_mermaid_block = False
                mermaid_fence_char = ""
                mermaid_fence_len = 0
                mermaid_start_line = None
                mermaid_excerpt_lines = []
            continue

        masked_line = masked_source_lines[idx - 1] if idx - 1 < len(masked_source_lines) else ""

        for match in md_embed.finditer(raw_line):
            embed_target = match.group(1)
            _append_precheck_issue(
                issues,
                seen,
                severity="WARN",
                rule="legacy_md_embed",
                message=f"检测到 `![[{embed_target}]]` 历史 `.md` 嵌入；正式讲义源稿请直接改成最终图片 `![[media/...png]]`，不要依赖兼容层",
                line_no=idx,
                excerpt=raw_line,
            )

        for match in critical_bare_subscript.finditer(masked_line):
            token = match.group(0)
            _append_precheck_issue(
                issues,
                seen,
                severity="ERROR",
                rule="bare_subscript_critical",
                message=f"数学模式外出现裸下标 `{token}`；请改成 `$...$` 中的正式下标写法",
                line_no=idx,
                excerpt=raw_line,
            )

        for match in generic_bare_subscript.finditer(masked_line):
            token = match.group(0)
            if critical_bare_subscript.fullmatch(token):
                continue
            _append_precheck_issue(
                issues,
                seen,
                severity="WARN",
                rule="bare_subscript_generic",
                message=f"检测到可能的裸下标 `{token}`；建议改成数学模式，避免 Word 排版不稳定",
                line_no=idx,
                excerpt=raw_line,
            )

        macro_hits = sorted({m.group(0) for m in risky_latex_outside_math.finditer(masked_line)})
        if macro_hits:
            shown = ", ".join(macro_hits[:4])
            _append_precheck_issue(
                issues,
                seen,
                severity="ERROR",
                rule="latex_outside_math",
                message=f"检测到数学模式外的 LaTeX 公式宏：{shown}",
                line_no=idx,
                excerpt=raw_line,
            )

        for match in circ_superscript.finditer(raw_line):
            prev = _prev_significant_char(raw_line, match.start())
            nxt = _next_significant_char(raw_line, match.end())
            if prev and not prev.isdigit() and nxt not in {"C", "F"}:
                _append_precheck_issue(
                    issues,
                    seen,
                    severity="WARN",
                    rule="standard_state_circ",
                    message="检测到 `^\\circ` 标准态写法；管线会自动转成 `\\theta`，但建议源稿直接写 `\\theta`",
                    line_no=idx,
                    excerpt=raw_line,
                )

        for match in re.finditer("°", raw_line):
            prev = _prev_significant_char(raw_line, match.start())
            nxt = _next_significant_char(raw_line, match.start() + 1)
            if prev and not prev.isdigit() and nxt not in {"C", "F"}:
                _append_precheck_issue(
                    issues,
                    seen,
                    severity="WARN",
                    rule="standard_state_degree_symbol",
                    message="检测到公式语境中的 `°`；管线会自动转成 `θ`，但建议源稿直接写 `θ`",
                    line_no=idx,
                    excerpt=raw_line,
                )

        if _is_caption_line(raw_line):
            if caption_complex_math.search(raw_line):
                _append_precheck_issue(
                    issues,
                    seen,
                    severity="ERROR",
                    rule="caption_complex_formula",
                    message="图注/表注中含复杂公式；请改成纯中文描述或把公式移到正文",
                    line_no=idx,
                    excerpt=raw_line,
                )
            elif caption_any_math.search(raw_line):
                _append_precheck_issue(
                    issues,
                    seen,
                    severity="WARN",
                    rule="caption_math",
                    message="图注/表注中含公式；Word 成品更稳妥的做法是图注只保留纯文本",
                    line_no=idx,
                    excerpt=raw_line,
                )

        # ── 学生讲义纪律检查：教师向/规划类内容残留（WARN） ──
        # 只检查「可见行」；HTML 注释（<!-- ... -->）内的教师信息不报警。
        # 多行 HTML 注释（<!-- ... -->）内的内容不视为「可见行」：
        # 逐行正则无法跨行，用深度计数判断当前行是否处于注释区内。
        if in_html_comment > 0 or "<!--" in raw_line:
            visible_line = ""
        else:
            visible_line = re.sub(r"<!--.*?-->", "", raw_line)
        in_html_comment = max(0, in_html_comment + raw_line.count("<!--") - raw_line.count("-->"))
        heading_match = re.match(r"^\s*#{1,6}\s+(.*)$", visible_line)
        if heading_match:
            heading_text = heading_match.group(1)
            for term in (
                "四层结构总览", "主线导航", "轮次划分", "本讲定位", "本轮定位",
                "深度边界", "深度分层", "使用说明", "易错清单",
            ):
                if term in heading_text:
                    _append_precheck_issue(
                        issues,
                        seen,
                        severity="WARN",
                        rule="teacher_facing_section",
                        message=(
                            f"学生讲义出现教师向/规划类小节标题「{term}」；"
                            "请移入 HTML 教师向注释区或删除（易错点并入「核心公式速查」）"
                        ),
                        line_no=idx,
                        excerpt=raw_line,
                    )
                    break
        bq_label_match = re.match(
            r"^\s*>\s*\*{1,2}\s*([^：:]+?)\s*\*{0,2}\s*[：:]", visible_line
        )
        if bq_label_match:
            label = bq_label_match.group(1).strip("* ")
            if any(
                t in label
                for t in ("本讲定位", "本轮定位", "深度边界", "上节衔接",
                          "下节衔接", "对应备课大纲", "对应专题", "主线导航", "轮次划分")
            ):
                _append_precheck_issue(
                    issues,
                    seen,
                    severity="WARN",
                    rule="teacher_facing_blockquote",
                    message=(
                        f"学生讲义正文出现教师向信息 `> **{label}**`；"
                        "请移入 HTML 教师向注释区或删除"
                    ),
                    line_no=idx,
                    excerpt=raw_line,
                )

        # ── emoji 残留（WARN，学生讲义建议零 emoji） ──
        for emoji in ("📎", "🌱", "🏆", "🌟", "🔥", "💡", "📝",
                      "🧠", "🗣", "⚡", "🔗", "🏅", "⭐", "💎", "🎯"):
            if emoji in visible_line:
                _append_precheck_issue(
                    issues,
                    seen,
                    severity="WARN",
                    rule="decorative_emoji",
                    message=(
                        f"检测到装饰性 emoji `{emoji}`；学生讲义建议移除"
                        "（Word 渲染不稳定），难度分级请用文字标签「基础/进阶/挑战」"
                    ),
                    line_no=idx,
                    excerpt=raw_line,
                )
                break

        # ── MO 反键星号未转义（WARN）──
        # σ* / π* 在 Obsidian/Word 中成对出现会被当成斜体吞掉（2026-08-05 发现）。
        # 只有同一行出现 ≥2 个才会成对触发，单星提及不报警。
        mo_star_count = len(re.findall(r"σ\*(?!\*)|π\*(?!\*)", visible_line))
        if mo_star_count >= 2:
            _append_precheck_issue(
                issues,
                seen,
                severity="WARN",
                rule="mo_antibonding_star_unescaped",
                message=(
                    "检测到同一直行有 ≥2 个未转义的 MO 反键星号（σ*/π*）；在 Obsidian/Word 中会成对当成斜体吞掉，"
                    "请写成 `σ\\*/π\\*`"
                ),
                line_no=idx,
                excerpt=raw_line,
            )

        # ── MO 反键星号位置错误（WARN）──
        # 规范：星号在轨道标号之后作上标（σ2s* / π2p*），不是 σ*2s / π*2p。
        if re.search(r"σ\*[₀₁₂₃₄₅₆₇₈₉0-9ₛₚ]|π\*[₀₁₂₃₄₅₆₇₈₉0-9ₛₚ]", visible_line):
            _append_precheck_issue(
                issues,
                seen,
                severity="WARN",
                rule="mo_antibonding_star_position",
                message=(
                    "MO 反键星号位置错误：应为 `σ2s*`/`π2p*`（星号在轨道标号后作上标），"
                    "不是 `σ*2s`/`π*2p`"
                ),
                line_no=idx,
                excerpt=raw_line,
            )

        # ── MO 轨道标号未用下标（WARN）──
        # 规范：1s/2s/2p 是下标，应写作 σ₁ₛ/σ₂ₛ/π₂ₚ，不是 σ1s/σ2s/π2p。
        if re.search(r"(σ|π)[0-9]+[sp]", visible_line):
            _append_precheck_issue(
                issues,
                seen,
                severity="WARN",
                rule="mo_orbital_plain_subscript",
                message=(
                    "MO 轨道标号未用下标：应写作 `σ₁ₛ`/`σ₂ₛ`/`π₂ₚ`（1s/2s/2p 是下标），"
                    "不是 `σ1s`/`σ2s`/`π2p`"
                ),
                line_no=idx,
                excerpt=raw_line,
            )

    macro_descriptions = {
        r"\\ce\{": r"\ce{...}",
        r"\\overset\b": r"\overset",
        r"\\underset\b": r"\underset",
        r"\\displaylines\b": r"\displaylines",
    }
    for pattern, label in macro_descriptions.items():
        matches = list(re.finditer(pattern, source_text))
        if matches:
            line_no = source_text.count("\n", 0, matches[0].start()) + 1
            excerpt = source_lines[line_no - 1] if 0 <= line_no - 1 < len(source_lines) else ""
            _append_precheck_issue(
                issues,
                seen,
                severity="INFO",
                rule="compat_macro_source",
                message=f"源文档含兼容宏 `{label}` 共 {len(matches)} 处；当前依赖预处理兼容层",
                line_no=line_no,
                excerpt=excerpt,
            )

    for pattern, label in macro_descriptions.items():
        matches = list(re.finditer(pattern, processed_text))
        if matches:
            line_no = processed_text.count("\n", 0, matches[0].start()) + 1
            excerpt = processed_lines[line_no - 1] if 0 <= line_no - 1 < len(processed_lines) else ""
            _append_precheck_issue(
                issues,
                seen,
                severity="ERROR",
                rule="compat_macro_residual",
                message=f"预处理后仍残留 `{label}`；这会影响 Word 公式稳定渲染",
                line_no=line_no,
                excerpt=excerpt,
            )

    if in_mermaid_block:
        excerpt = " | ".join(mermaid_excerpt_lines[:2])
        _append_precheck_issue(
            issues,
            seen,
            severity="ERROR",
            rule="mermaid_block_unclosed",
            message="检测到未闭合的 Mermaid 代码块；学生讲义源稿不要直接保留 Mermaid",
            line_no=mermaid_start_line,
            excerpt=excerpt,
        )

    return WordFormulaPrecheckReport(md_path=md_path, issues=issues)


def _emit_word_formula_precheck(
    report: WordFormulaPrecheckReport,
    *,
    verbose: bool = False,
    include_info: bool = False,
) -> None:
    """Print precheck summary to stderr."""
    if not report.issues:
        if verbose:
            print(f"  [precheck] OK — no source issues found", file=sys.stderr)
        return
    severities = {"ERROR", "WARN"}
    if include_info or verbose:
        severities.add("INFO")
    limit = 12 if verbose else 6
    print(report.render(limit=limit, severities=severities), file=sys.stderr)


# ══════════════════════════════════════════════════════════════════
#  Stage 1: Preprocess
# ══════════════════════════════════════════════════════════════════

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter and return (metadata_dict, body_text)."""
    if not text.startswith("---"):
        return {}, text.strip()

    end_idx = text.find("---", 3)
    if end_idx == -1 or end_idx > 5000:
        return {}, text.strip()

    fm_text = text[3:end_idx].strip()
    body = text[end_idx + 3:].strip()

    try:
        fm: dict[str, Any] = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm = {}
    return (fm, body) if isinstance(fm, dict) else ({}, body)


def _clean_title(raw: str) -> str:
    """Remove '学生讲义-' prefix from YAML title."""
    t = raw.strip()
    for prefix in ["学生讲义-", "学生讲义"]:
        if t.startswith(prefix):
            return t[len(prefix):].strip()
    return t


def _clean_word_title(raw: str) -> str:
    """Build a cleaner student-facing Word title."""
    title = raw.strip()
    for prefix in ["学生讲义：", "学生讲义-", "学生讲义"]:
        if title.startswith(prefix):
            title = title[len(prefix):].strip()
    title = re.sub(
        r"（(?:超级充实版(?:·自学完整)?|自学完整|超级充实版)）$",
        "",
        title,
    ).strip()
    title = title.rstrip("：:- ").strip()
    return title or "学生讲义"


def build_title(fm: dict[str, Any]) -> str:
    """Build display title from frontmatter."""
    yaml_title = fm.get("title", "")
    if yaml_title and isinstance(yaml_title, str):
        cleaned = _clean_title(yaml_title)
        if cleaned:
            return cleaned
    # Fallback
    return "学生讲义"


def _resolve_wikilink(text: str) -> str:
    """Convert [[page]] → page, [[page|alias]] → alias."""
    # [[link|alias]] → alias
    text = re.sub(r'\[\[([^\|\]]+)\|([^\]]+)\]\]', r'\2', text)
    # [[link]] → link
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
    return text


_SIMPLE_SUPERSCRIPT_MAP = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "+": "⁺",
    "-": "⁻",
    "=": "⁼",
    "(": "⁽",
    ")": "⁾",
}

_SIMPLE_SUBSCRIPT_MAP = {
    "0": "₀",
    "1": "₁",
    "2": "₂",
    "3": "₃",
    "4": "₄",
    "5": "₅",
    "6": "₆",
    "7": "₇",
    "8": "₈",
    "9": "₉",
    "+": "₊",
    "-": "₋",
    "=": "₌",
    "(": "₍",
    ")": "₎",
}

_SIMPLE_INLINE_SCRIPT_TOKEN_RE = re.compile(
    r'(?<!\$)\$(?!\$)([A-Za-z0-9]+(?:(?:\^|_)(?:\{[^{}$\n]+\}|[^{}$\n]))+)\$(?!\$)'
)
_SCRIPT_PART_RE = re.compile(r'(\^|_)(\{[^{}$\n]+\}|[^{}$\n])')
_SPLIT_INLINE_SCRIPT_RE = re.compile(
    r'([A-Za-z0-9]+)\$(\^|_)(\{[^{}$\n]+\}|[^{}$\n])\$'
)
_ATTACHED_SIMPLE_SCRIPT_RE = re.compile(
    r'([^\s$]+)\$((?:(?:\^|_)(?:\{[^{}$\n]+\}|[^{}$\n]))+)\$'
)


def _map_simple_script_arg(op: str, arg: str) -> str | None:
    """Convert a simple script payload to unicode super/subscript glyphs."""
    mapping = _SIMPLE_SUPERSCRIPT_MAP if op == "^" else _SIMPLE_SUBSCRIPT_MAP
    converted: list[str] = []
    for ch in arg:
        mapped = mapping.get(ch)
        if mapped is None:
            return None
        converted.append(mapped)
    return "".join(converted)


def _convert_simple_script_token(token: str) -> str | None:
    """Convert simple inline math script tokens like `I_1` or `Na^+` to unicode."""
    m = re.fullmatch(
        r'([A-Za-z0-9]+)((?:(?:\^|_)(?:\{[^{}$\n]+\}|[^{}$\n]))+)',
        token,
    )
    if not m:
        return None

    base = m.group(1)
    suffix = m.group(2)
    out = [base]
    for op, raw_arg in _SCRIPT_PART_RE.findall(suffix):
        arg = raw_arg[1:-1] if raw_arg.startswith("{") and raw_arg.endswith("}") else raw_arg
        mapped = _map_simple_script_arg(op, arg)
        if mapped is None:
            return None
        out.append(mapped)
    return "".join(out)


def _extract_markdown_h1(text: str) -> str | None:
    """Return the first level-1 markdown heading text."""
    m = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip()


def _normalize_markdown_heading_title(title: str) -> str:
    """Normalize section titles for structural filtering."""
    normalized = title.strip()
    normalized = re.sub(r"^[一二三四五六七八九十]+[、.．]\s*", "", normalized)
    normalized = re.sub(r"^\d+(?:\.\d+)*\s*", "", normalized)
    return normalized.strip()


_WORD_CLEAN_SECTION_TITLES = {
    "与竞赛真题的对接",
    "跨专题联系",
    "深化方向",
    "延伸阅读",
}

_WORD_CLEAN_LEADING_SECTION_TITLES = {
    "学习目标",
}


def _strip_markdown_sections_by_title(text: str, titles: set[str]) -> str:
    """Remove markdown heading sections whose normalized titles match `titles`."""
    lines = text.splitlines()
    result: list[str] = []
    skipping = False
    skip_level = 99

    for line in lines:
        heading = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            normalized = _normalize_markdown_heading_title(heading.group(2))
            if skipping and level <= skip_level:
                skipping = False
            if normalized in titles:
                skipping = True
                skip_level = level
                continue
        if skipping:
            continue
        result.append(line)
    return "\n".join(result)


def _strip_non_image_wikilink_lines(text: str) -> str:
    """Remove non-image knowledge-base link lines from a Word clean copy."""
    kept_lines: list[str] = []
    for line in text.splitlines():
        if "[[" in line and "![[" not in line:
            continue
        kept_lines.append(line)
    return "\n".join(kept_lines)


def _collect_markdown_sections_by_title(text: str, titles: set[str]) -> str:
    """Collect heading sections whose normalized titles match `titles`."""
    lines = text.splitlines()
    collected: list[str] = []
    buffer: list[str] = []
    collecting = False
    collect_level = 99

    for line in lines:
        heading = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            normalized = _normalize_markdown_heading_title(heading.group(2))
            if collecting and level <= collect_level:
                collected.extend(buffer)
                buffer = []
                collecting = False
            if normalized in titles:
                collecting = True
                collect_level = level
                buffer = [line]
                continue
        if collecting:
            buffer.append(line)

    if collecting and buffer:
        collected.extend(buffer)

    return "\n".join(collected).strip()


def _collapse_extra_blank_lines(text: str) -> str:
    """Collapse repeated blank lines and duplicate horizontal rules."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?:\n\s*___\s*){2,}", "\n\n___\n\n", text)
    text = re.sub(r"(?:\n\s*---\s*){2,}", "\n\n---\n\n", text)
    return text.strip()


def _build_word_clean_body(fm: dict[str, Any], body: str) -> str:
    """Build a student-facing Word clean copy from the markdown source."""
    heading_title = _extract_markdown_h1(body)
    clean_title = _clean_word_title(heading_title or build_title(fm))

    main_match = re.search(r"^##\s+[一二三四五六七八九十]+、", body, flags=re.MULTILINE)
    prefix_text = body[:main_match.start()] if main_match else body
    leading_sections = _collect_markdown_sections_by_title(
        prefix_text,
        _WORD_CLEAN_LEADING_SECTION_TITLES,
    )
    if main_match:
        core = body[main_match.start():].strip()
    else:
        core = re.sub(r"^#\s+.+?\n+", "", body, count=1, flags=re.MULTILINE).strip()

    leading_sections = _strip_non_image_wikilink_lines(leading_sections)
    leading_sections = _collapse_extra_blank_lines(leading_sections) if leading_sections.strip() else ""
    core = _strip_markdown_sections_by_title(core, _WORD_CLEAN_SECTION_TITLES)
    core = _strip_non_image_wikilink_lines(core)
    core = re.sub(r"^\s*>\s*相关知识点：.*$", "", core, flags=re.MULTILINE)
    core = re.sub(r"^\s*>\s*\*\*相关知识点\*\*：.*$", "", core, flags=re.MULTILINE)
    core = _collapse_extra_blank_lines(core)
    parts = [f"# {clean_title}"]
    if leading_sections:
        parts.append(leading_sections)
    parts.append(core)
    return "\n\n".join(parts).strip() + "\n"


def _normalize_split_inline_scripts(text: str) -> str:
    """Normalize `Na$^+$` / `2s$^2$` / `4f$_{+3}$` style split-script markup.

    Strategy:
      - simple superscript/subscript payloads → unicode form
      - complex payloads (e.g. `$_{x(x^2-3y^2)}$`) → merged full math token
    """

    def _replace(match: re.Match[str]) -> str:
        base = match.group(1)
        op = match.group(2)
        raw_arg = match.group(3)
        token = f"{base}{op}{raw_arg}"
        converted = _convert_simple_script_token(token)
        if converted is not None:
            return converted
        return f"${base}{op}{raw_arg}$"

    return _SPLIT_INLINE_SCRIPT_RE.sub(_replace, text)


def _normalize_simple_inline_math_tokens(text: str) -> str:
    """Convert simple inline math tokens to plain unicode-friendly text where safe."""

    def _replace(match: re.Match[str]) -> str:
        token = match.group(1)
        converted = _convert_simple_script_token(token)
        if converted is not None:
            return converted
        if token in {"Z^*", "Z^{*}"}:
            return "Z*"
        return match.group(0)

    return _SIMPLE_INLINE_SCRIPT_TOKEN_RE.sub(_replace, text)


def _normalize_attached_simple_math_scripts(text: str) -> str:
    """Convert `NO$_2^-$` / `[O=N-O]$^-$` style attached scripts to unicode."""

    def _replace(match: re.Match[str]) -> str:
        base = match.group(1)
        suffix = match.group(2)
        out = [base]
        for op, raw_arg in _SCRIPT_PART_RE.findall(suffix):
            arg = raw_arg[1:-1] if raw_arg.startswith("{") and raw_arg.endswith("}") else raw_arg
            mapped = _map_simple_script_arg(op, arg)
            if mapped is None:
                return match.group(0)
            out.append(mapped)
        return "".join(out)

    return _ATTACHED_SIMPLE_SCRIPT_RE.sub(_replace, text)


def _normalize_strong_markup(text: str) -> str:
    """Trim stray inner spaces in plain `**...**` strong markup.

    Keeps normal strong emphasis unchanged, while normalizing malformed forms
    such as `** 标题**`, `**标题 **`, and `**  标题  **`.
    Empty strong markers like `**  **` are removed.
    """

    def _trim_inner_spaces(match: re.Match[str]) -> str:
        inner = match.group(1)
        stripped = inner.strip()
        if not stripped:
            return ""
        return f"**{stripped}**"

    return re.sub(
        r'(?<!\*)\*\*([^\n*]*?)\*\*(?!\*)',
        _trim_inner_spaces,
        text,
        flags=re.MULTILINE,
    )


def _transform_callout_blocks(text: str) -> str:
    """Transform emoji-prefixed callout blockquotes to bold-led paragraphs.

    Obsidian callouts (> 🧠/🗣️/⚠️/etc...) render as plain indented text in Word.
    This converts them to normal paragraphs with bold headers that stand out.
    Emoji symbols are stripped — only the label text (教学洞察, 易错点, etc.) remains.

    Before:   > 🧠 **教学洞察**：内容
    After:    **教学洞察**：内容

    Continuation lines (additional > lines) have their > prefix stripped.
    """
    CALLOUT_EMOJIS = '🧠🗣️⚠️💡⚡🔥📝🌟✅🔗'
    # Match both:  > ⚠️ **header**   and   > **⚠️ header**
    callemoji_re = re.compile(r'^>\s*(?:\*\*)?\s*([' + CALLOUT_EMOJIS + r'])')

    lines = text.split('\n')
    result: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        m = callemoji_re.match(line.strip())
        if m:
            # Collect all consecutive > lines belonging to this callout
            block: list[str] = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                block.append(re.sub(r'^>\s*', '', lines[i]))
                i += 1
            # Boldify the label on the first line, strip emoji
            if block:
                first = block[0]
                # Remove emoji, keep only the **bold label**
                first = re.sub(
                    r'^([' + CALLOUT_EMOJIS + r'])\s*\*\*(.*?)\*\*',
                    r'**\2**',
                    first,
                )
                block[0] = first
                # Insert a blank line before the callout for visual separation
                if result and result[-1].strip() != '':
                    result.append('')
                result.extend(block)
                result.append('')
        else:
            result.append(line)
            i += 1

    # Remove trailing blank lines
    while result and result[-1].strip() == '':
        result.pop()
    return '\n'.join(result)


def _preprocess_ce_in_math(text: str) -> str:
    r"""Convert \ce{...} → proper LaTeX inside math ($...$ / $$...$$) for OMML compat.

    Complete mhchem-to-LaTeX converter handling:
      - Arrows: ->, <-, <=>, ->[text], <-[text]
      - Charges: H+, ClO4-, Fe3+ (detected by trailing +/-)
      - Subscripts: H2O → H_2O, Fe2O3 → Fe_2O_3
      - Isotopes: ^{238}_{92}U → ^{238}_{92}U
      - Comparison: >> → \\gg, << → \\ll
      - Chinese text in formulas (preserved as-is inside \\text{})

    Uses balanced-brace matching to handle nested {} inside \\ce{...}.
    """
    def _find_ce_end(text, start):
        r"""Find matching } for \ce{ starting at 'start'. Returns end index (exclusive)."""
        if not text[start:].startswith('\\ce{'):
            return -1
        i = start + 4  # skip \ce{
        depth = 1
        while i < len(text) and depth > 0:
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
            i += 1
        return i if depth == 0 else -1

    def _has_explicit_subscript(species):
        """Check if species contains explicit _ (subscript) notation."""
        i = 0
        while i < len(species):
            if species[i] == '\\' and i + 1 < len(species):
                i += 2  # skip escaped char
            elif species[i] == '{':
                depth = 1
                i += 1
                while i < len(species) and depth > 0:
                    if species[i] == '{': depth += 1
                    elif species[i] == '}': depth -= 1
                    i += 1
            elif species[i] == '_':
                return True
            else:
                i += 1
        return False

    def _parse_species(species):
        """Convert a single mhchem species to LaTeX.

        Rules:
          1. ^{...} and _{...} preserved as-is
          2. Bare ^x → ^{x}, bare _x → _{x}
          3. Trailing charge (+, -, 2+, 3-, etc) → ^{...}
          4. Bare digits after letters → _{digit}
          5. Leading digits → _{digit}
          6. Special chars (*, δ, Δ) preserved
        """
        import re as _re

        # Already fully specified with ^ or _ — just normalize bare markers
        if '^' in species or _has_explicit_subscript(species):
            s = _re.sub(r'\^([^{])', r'^{\1}', species)
            s = _re.sub(r'_([^{])', r'_{\1}', s)
            return s

        # Detect trailing charge: ClO4- → charge -, H3O+ → charge +
        # Simple: match only the trailing +/- as the charge
        # Note: Fe3+ → Fe_3^{+} (3 treated as subscript, not charge digit)
        # This is acceptable — explicit ^{3+} notation is preferred for charge digits
        charge_match = _re.search(r'([+\-])$', species)
        if charge_match:
            base = species[:charge_match.start()]
            charge = charge_match.group(1)
            # Convert subscripts in the base part (digit after letter → _{digit})
            base = _re.sub(r'([A-Za-z\)}])(\d)', r'\1_{\2}', base)
            return base + '^{' + charge + '}'

        # No charge, no explicit subscripts — add subscripts for bare digits
        result = _re.sub(r'([A-Za-z\)}])(\d)', r'\1_{\2}', species)
        return result

    def _convert_ce_content(inner):
        """Convert full mhchem content to proper LaTeX.

        1. Replace arrows (longest first)
        2. Split by + and spaces (preserving arrow parts)
        3. Parse each species
        4. Recombine
        """
        import re as _re

        s = inner

        # Replace arrows (longest first to avoid partial matches)
        # <-[text] and ->[text] with conditions
        s = _re.sub(r'<-\[([^\]]*)\]', r'\\xleftarrow{\\text{\1}}', s)
        s = _re.sub(r'->\[([^\]]*)\]', r'\\xrightarrow{\\text{\1}}', s)
        # Equilibrium arrows
        s = s.replace('<=>', r' \rightleftharpoons ')
        s = s.replace('<=>', r' \rightleftharpoons ')  # double if needed
        # Simple arrows
        s = s.replace('->', r' \rightarrow ')
        s = s.replace('<-', r' \leftarrow ')
        # Comparison operators
        s = s.replace('>>', r' \\gg ')
        s = s.replace('<<', r' \\ll ')

        # If result already has LaTeX commands (from arrow replacement), split and parse
        has_latex = any(cmd in s for cmd in [
            '\\rightarrow', '\\leftarrow', '\\rightleftharpoons',
            '\\xrightarrow', '\\xleftarrow', '\\gg', '\\ll',
        ])

        if has_latex:
            # Split by " + " (species separator, NOT charge +), parse each token
            # In mhchem: "H+ + A-" → split by " + " → ["H+", "A-"]
            tokens = _re.split(r'(\s\+\s|\\rightarrow|\\leftarrow|'
                               r'\\rightleftharpoons|\\xrightarrow\{[^}]*\}|'
                               r'\\xleftarrow\{[^}]*\}|\\gg|\\ll)', s)
            parsed = []
            for tok in tokens:
                tok_stripped = tok.strip()
                if tok_stripped in ('+', '-', '\\rightarrow', '\\leftarrow',
                                    '\\rightleftharpoons', '\\gg', '\\ll'):
                    parsed.append(' ' + tok_stripped + ' ')
                elif tok_stripped.startswith('\\xrightarrow') or tok_stripped.startswith('\\xleftarrow'):
                    parsed.append(' ' + tok_stripped + ' ')
                elif tok_stripped:
                    parsed.append(_parse_species(tok_stripped))
                else:
                    parsed.append(tok)
            return ''.join(parsed)
        else:
            # No arrows — parse as space-separated species
            parts = s.split()
            parsed = [_parse_species(p) for p in parts if p]
            return ' '.join(parsed)

    # Find and replace all \ce{...} blocks with balanced brace matching
    result = []
    i = 0
    while i < len(text):
        ce_start = text.find('\\ce{', i)
        if ce_start < 0:
            result.append(text[i:])
            break
        # Copy text before this \ce
        result.append(text[i:ce_start])
        # Find balanced closing brace
        end = _find_ce_end(text, ce_start)
        if end < 0:
            result.append(text[ce_start:])
            break
        inner = text[ce_start + 4:end - 1]  # content between \ce{ and }
        result.append(_convert_ce_content(inner))
        i = end
    return ''.join(result)


def _strip_metadata_blockquote(text: str) -> str:
    """Remove blockquote metadata section between title and first `---` divider.

    Before:
        # 第四讲：化学平衡

        > **适用**：第一轮（初学）→ 第二轮（深化）
        > **对应备课大纲**：[[...]]
        > **前置要求**：热力学基础

        ---

        ## 学习目标

    After:
        # 第四讲：化学平衡

        ---

        ## 学习目标

    Works with:
      - Standard metadata (short blockquote + ---)
      - 超级充实版 (long blockquote with multiline > **深度边界** + > **版本说明**)
    """
    # ── Quick self-test on import ──
    _SELF_CHECK = "> **对应专题**：[[xxx]]\n> **深度边界**：多行内容\n>\n---"
    _test = text if "SELF_CHECK" in globals() else None  # skip in production
    lines = text.split("\n")
    # Locate first # heading
    first_h = -1
    for i, ln in enumerate(lines):
        if ln.startswith("# "):
            first_h = i
            break
    if first_h < 0:
        return text

    # Scan for blockquote region followed by --- or ## heading
    in_bq = False
    first_div = -1
    bq_end = -1  # line after last blockquote line
    for i in range(first_h + 1, len(lines)):
        ln = lines[i]
        if ln.startswith("> "):
            in_bq = True
            bq_end = i + 1
            continue
        if in_bq:
            if ln.strip() == "":
                continue
            if ln.strip() == "---":
                first_div = i
                break
            # Non-blank, non-bq, non-div → not metadata
            in_bq = False
            break
        # Not in blockquote: metadata region ends at the first non-blank line
        if ln.strip():
            break

    # Case A: blockquote + --- divider (original behavior)
    if first_div >= 0:
        kept = lines[: first_h + 1] + ["", lines[first_div]] + lines[first_div + 1 :]
        return "\n".join(kept)

    # Case B: blockquote followed by ## heading (no --- divider)
    # Strip the entire blockquote region
    if bq_end > first_h:
        kept = lines[: first_h + 1] + [""] + lines[bq_end:]
        return "\n".join(kept)

    return text


def _strip_footer(text: str) -> str:
    """Remove '*本讲义依据 …*' / '*主要内容来源 …*' / '*对应 …*' footer lines.

    These are markdown-italic attribution lines at the very end of some handouts.
    """
    lines = text.rstrip().split("\n")
    # Patterns for footer lines (before wiki-link resolution)
    pat = re.compile(
        r"^\*\s*(本讲义依据|主要内容来源|对应).*\*$"
    )
    while lines and pat.match(lines[-1].strip()):
        lines.pop()
    # Also drop trailing blank lines left after removal
    while lines and lines[-1].strip() == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def _preprocess_markdown(text: str) -> str:
    """Full markdown preprocessing for pandoc compatibility.

    1. Convert Obsidian-style image embeds ![[...]] to ![](...)
       (Currently no handouts use this, but pipeline is ready.)
    2. Convert \\ce{...} → \\text{...} inside math blocks
    3. Convert [[wiki-links]] to plain text
    4. Convert OMML-incompatible LaTeX macros:
       - \\overset{...}{...}  →  \\mathrm{...^{(...)}}  (oxidation numbers)
       - \\underset{...}{...}  →  side annotation
       - \\displaylines{...}   →  separate equations
    """
    # 0) Transform callout blockquotes (> 🧠/🗣️/⚠️) to bold-led paragraphs
    text = _transform_callout_blocks(text)
    # 0b) Normalize malformed strong emphasis with stray inner spaces
    text = _normalize_strong_markup(text)
    # 0c) Normalize split-script inline math like `Na$^+$` / `2s$^2$`
    text = _normalize_split_inline_scripts(text)
    # 0d) Simplify safe inline tokens like `$I_1$` → `I₁`, `$Z^*$` → `Z*`
    text = _normalize_simple_inline_math_tokens(text)
    # 0e) Normalize attached simple scripts like `NO$_2^-$` / `[O=N-O]$^-$`
    text = _normalize_attached_simple_math_scripts(text)
    # 0f) Normalize MO orbital notation so Word/Obsidian render correctly.
    #   a) subshell → Unicode subscript (σ2s/σ₂s → σ₂ₛ, π2p → π₂ₚ)
    #   b) antibonding star AFTER the label + escaped (σ₂ₛ* → σ₂ₛ\*), so paired
    #      `*` are never parsed as markdown emphasis. Legacy σ*2s is reordered.
    _mo_sub_map = {'0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
                   '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
                   's': 'ₛ', 'p': 'ₚ'}
    _mo_sub_t = str.maketrans(_mo_sub_map)

    def _mo_subshell(m: re.Match) -> str:
        return m.group(1) + (m.group(2) + m.group(3)).translate(_mo_sub_t)

    # 1) legacy star-before → move after: σ*2s → σ2s\*
    text = re.sub(
        r"(σ|π)\*([0-9₀₁₂₃₄₅₆₇₈₉]+)([sp])",
        lambda m: m.group(1) + m.group(2) + m.group(3) + r"\*",
        text,
    )
    # 2) plain/mixed subshell → Unicode subscripts: σ2s/σ₂s → σ₂ₛ, π2p → π₂ₚ
    text = re.sub(
        r"(σ|π)([0-9₀₁₂₃₄₅₆₇₈₉]+)([sp])",
        _mo_subshell,
        text,
    )
    # 3) star-after → escape: σ₂ₛ* → σ₂ₛ\*
    text = re.sub(
        r"(σ|π)([₀₁₂₃₄₅₆₇₈₉0-9ₛₚ]+)\*(?!\*)",
        lambda m: m.group(1) + m.group(2) + r"\*",
        text,
    )
    # 4) generic σ*/π* (no subshell) → escape
    text = re.sub(
        r"(σ|π)\*(?!\*)",
        lambda m: m.group(1) + r"\*",
        text,
    )
    # 0g) Standard-state notation: `^\circ` / `°` in standard-state contexts
    #     → `\theta`/`θ` (ΔG° → ΔGθ). Degree contexts (90°, 37°C) kept.
    def _std_state_circ(m: re.Match) -> str:
        prev = _prev_significant_char(m.string, m.start())
        nxt = _next_significant_char(m.string, m.end())
        if prev and not prev.isdigit() and nxt not in {"C", "F"}:
            return m.group(0).replace("\\circ", "\\theta").replace("°", "θ")
        return m.group(0)
    text = re.sub(r"\^\s*\{?\s*\\circ\s*\}?|°", _std_state_circ, text)

    # 1) Image embeds: ![[image.png]] or ![[image.png|alt text]] → ![alt](image.png)
    text = re.sub(
        r'!\[\[([^\]]+?)\.(png|jpg|jpeg|gif|webp|svg)(?:\|([^\]]*))?\]\]',
        lambda m: f'![{m.group(3) or ""}]({m.group(1)}.{m.group(2)})',
        text, flags=re.IGNORECASE)
    # Adjacent embeds in one table cell (e.g. `![[a.jpg]]![[b.jpg]]`) must be
    # separated, otherwise pandoc merges the pair and drops one image.
    text = re.sub(
        r'(!\[[^\]]*?\]\([^)]+\))(?=\s*!\[[^\]]*?\]\()',
        r'\1 ',
        text,
    )

    # 1b) Excalidraw .md embeds → warn + remove (cannot embed in docx)
    # Note: [[link|alias]] format is handled by the (?:|\|[^\]]*)? optional group
    excalibur_matches = list(re.finditer(r'!?\[\[([^\]]+\.(md|excalidraw))(?:\|[^\]]*)?\]\]', text, flags=re.IGNORECASE))
    if excalibur_matches:
        fnames = [m.group(1) for m in excalibur_matches]
        print(f"  [WARN] {len(excalibur_matches)} Excalidraw embed(s) removed (not renderable in docx): {fnames}", file=sys.stderr)
    text = re.sub(r'!?\[\[([^\]]+\.(md|excalidraw))(?:\|[^\]]*)?\]\]',
                  '', text, flags=re.IGNORECASE)

    # 1c) Replace standalone --- with ___ to prevent Pandoc YAML parsing
    #     Pandoc interprets --- as YAML metadata blocks, which breaks when
    #     body content (e.g. **bold**) appears between paired ---.
    #     ___ renders identically as a horizontal rule in Word.
    text = re.sub(r'^---\s*$', '___', text, flags=re.MULTILINE)

    # 1d) Remove residual emoji symbols from callout labels (safety net)
    text = re.sub(r'[🧠🗣️⚠️💡⚡🔥📝🌟✅🔗]\s*', '', text)

    # 1e) #### headings → bold text (#### is too deep for Word, convert to bold)
    text = re.sub(r'^####\s+(.+)$', r'**\1**', text, flags=re.MULTILINE)

    # 2) \\ce{...} → standard LaTeX math inside $...$
    #    Pandoc docx output does NOT support mhchem \\ce{}.
    #    Convert to standard LaTeX with proper superscript/subscript notation.
    text = _preprocess_ce_in_math(text)

    # 3) Wiki-links to plain text
    text = _resolve_wikilink(text)

    # 4a) \overset{+6}{Cr} / \overset{+6}{\mathrm{Cr_2}} → Cr^{(+6)} / \mathrm{Cr_2}^{(+6)}
    #     (oxidation number notation; no extra \mathrm wrapping to avoid nesting issues)
    # 2026-09-05: _arg 放宽到三层嵌套（\underset{k_{\mathrm{CO,des}}}{\stackrel{k_{\mathrm{CO,ads}}}{...}}
    # 类参数曾超出单层限制导致 compat 转换失败、宏残留进 Word 产物，precheck compat_macro_residual ERROR）
    _arg = r'(\{(?:[^{}]|\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})*\})'
    text = re.sub(r'\\overset' + _arg + _arg,
                  lambda m: m.group(2)[1:-1] + '^{(' + m.group(1)[1:-1] + ')}',
                  text)

    # 4b) \underset{text}{formula} → formula (text)
    #     (label underneath; handles one level of nested braces)
    text = re.sub(r'\\underset' + _arg + _arg,
                  lambda m: m.group(2)[1:-1] + ' \\;(' + m.group(1)[1:-1] + ')',
                  text)

    # 4b2) \xlongequal → \xrightarrow / \rightarrow
    #      texmath 不支持 \xlongequal；无花括号参数是 OCR 残留，退化为 \rightarrow。
    text = re.sub(r'\\xlongequal(?=[ \t]*[A-Za-z\\])', r'\\rightarrow', text)
    text = re.sub(r'\\xlongequal', r'\\xrightarrow', text)

    # 4b3) \AA → \text{Å}（texmath 不支持 \AA）
    text = re.sub(r'\\text\{\\AA\}', r'\\text{Å}', text)
    text = re.sub(r'\\mathrm\{\\AA\}', r'\\text{Å}', text)
    text = re.sub(r'\\AA', r'\\text{Å}', text)

    # 4b4) 去掉 \Biggl/\Bigl/\biggl/\bigl 等尺寸前缀，保留后续定界符
    text = re.sub(
        r'\\(?:Biggl|Bigl|biggl|bigl|Biggr|Bigr|biggr|bigr)\s*',
        '',
        text,
    )

    # 4b5) 去掉 \tag{...}（texmath 不支持；兼容 `\tag {H}` 的空格写法）
    text = re.sub(r'\s*\\tag\s*\{[^{}]*\}', '', text)

    # 4b6) \xrightarrow{...\\...} 的条件内换行改为分号（texmath 不支持 \\）
    def _fix_arrow_breaks(m: re.Match) -> str:
        return m.group(1) + m.group(2).replace('\\\\', '; ') + m.group(3)
    text = re.sub(
        r'(\\xrightarrow(?:\[[^\]]*\])?\{)([^{}]*)(\})',
        _fix_arrow_breaks,
        text,
    )

    # 4c) \displaylines{...} → split into separate display equations
    #     (handles one level of nested \text{} etc. inside)
    text = re.sub(r'\\displaylines' + _arg,
                  lambda m: '\n'.join(
                      '$$' + line.strip() + '$$'
                      for line in m.group(1)[1:-1].split(r'\\')
                      if line.strip()
                  ),
                  text)

    return text


def build_subtitle(fm: dict[str, Any]) -> str | None:
    """Build a subtitle line from frontmatter."""
    parts: list[str] = []
    source = fm.get("source_book", "") or fm.get("source", "") or ""
    if source and isinstance(source, str):
        parts.append(source)
    chapter = fm.get("chapter", "")
    if chapter and isinstance(chapter, str):
        parts.append(chapter)
    rounds = fm.get("serve_rounds", [])
    if rounds:
        rs = "/".join(str(r) for r in (rounds if isinstance(rounds, list) else [rounds]))
        parts.append(rs)
    return " · ".join(parts) if parts else None


def _prepare_handout_markdown(
    md_path: Path,
    verbose: bool = False,
    word_clean: bool = False,
) -> tuple[dict[str, Any], str, str]:
    """Read one markdown handout and return (frontmatter, source_body, processed_body)."""
    content = md_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    source_body = _build_word_clean_body(fm, body) if word_clean else body
    processed_body = source_body

    # 1a) Strip metadata blockquote between title and first ---.
    # Word 清稿模式下，正文会直接从第一章开始，后文中的正常 blockquote
    # 不应再被误判成顶层 metadata。
    if not word_clean:
        processed_body = _strip_metadata_blockquote(processed_body)
    # 1b) Strip attribution footer (*本讲义依据…*).
    processed_body = _strip_footer(processed_body)
    # 1b2) Auto-render Excalidraw .md files to PNG if no sibling PNG exists.
    for excal_match in re.finditer(r'!?\[\[([^\]]+\.(?:md|excalidraw))(?:\|[^\]]*)?\]\]', processed_body):
        excal_path_str = excal_match.group(1)
        excal_full = md_path.parent / excal_path_str
        if not excal_full.exists():
            excal_full = VAULT_MEDIA / Path(excal_path_str).name
        if not excal_full.exists():
            continue
        try:
            first_lines = excal_full.read_text('utf-8', errors='replace')[:200]
            if 'excalidraw-plugin:' not in first_lines:
                continue
        except Exception:
            continue
        png_candidate = excal_full.with_suffix('.png')
        if png_candidate.exists():
            continue
        script_dir = Path(__file__).parent
        excal_script = script_dir / 'excalidraw-to-png.mjs'
        if excal_script.exists():
            if verbose:
                print(f"  [EXCALIDRAW] Rendering {excal_path_str} → {png_candidate.name}...", file=sys.stderr)
            subprocess.run(
                ['node', str(excal_script), str(excal_full), str(png_candidate)],
                capture_output=True, timeout=120000,
            )
        if png_candidate.exists():
            print(f"  [EXCALIDRAW] {excal_path_str} → {png_candidate.name} (OK)", file=sys.stderr)
        else:
            print(f"  [WARN] Excalidraw render failed for {excal_path_str}", file=sys.stderr)

    # 1b2b) Auto-render SVG files to PNG if no sibling PNG exists.
    for svg_match in re.finditer(r'!\[\[([^\]]+\.svg)(?:\|[^\]]*)?\]\]', processed_body):
        svg_path_str = svg_match.group(1)
        svg_full = VAULT_MEDIA / Path(svg_path_str).name
        if not svg_full.exists():
            svg_full = md_path.parent / svg_path_str
        if not svg_full.exists():
            continue
        png_candidate = svg_full.with_suffix('.png')
        if png_candidate.exists():
            continue
        script_dir = Path(__file__).parent
        svg_script = script_dir / 'svg-to-png.mjs'
        if svg_script.exists():
            if verbose:
                print(f"  [SVG] Rendering {svg_path_str} → {png_candidate.name}...", file=sys.stderr)
            subprocess.run(
                ['node', str(svg_script), str(svg_full), str(png_candidate)],
                capture_output=True, timeout=60000,
            )
        if png_candidate.exists():
            print(f"  [SVG] {svg_path_str} → {png_candidate.name} (OK)", file=sys.stderr)
        else:
            print(f"  [WARN] SVG render failed for {svg_path_str}", file=sys.stderr)

    # 1b2c) Replace SVG references with PNG after rendering.
    def _svg_to_png_ref(m: re.Match) -> str:
        svg_path = m.group(1)
        alias = m.group(2) or ""
        png_name = Path(svg_path).stem + '.png'
        for d in [VAULT_MEDIA, md_path.parent / 'media', md_path.parent]:
            if (d / png_name).exists():
                return f'![[{png_name}|{alias}]]' if alias else f'![[{png_name}]]'
        return m.group(0)

    processed_body = re.sub(
        r'!\[\[([^\]]+\.svg)(?:\|([^\]]*))?\]\]',
        _svg_to_png_ref,
        processed_body,
    )

    # 1b3) Replace .md image embeds with rendered PNG (if available).
    def _mermaid_png_fallback(m: re.Match) -> str:
        path = m.group(1)
        alias = m.group(2) or ""
        base = re.sub(r'\.md$', '', path, flags=re.IGNORECASE)
        candidates = [
            md_path.parent / f"{base}.png",
            md_path.parent / "media" / f"{Path(base).name}.png",
            VAULT_MEDIA / f"{Path(base).name}.png",
        ]
        for cand in candidates:
            if cand.exists():
                if verbose:
                    print(f"  [MERMAID] {path} → {cand.name}", file=sys.stderr)
                return f'![[{cand.name}|{alias}]]' if alias else f'![[{cand.name}]]'
        return m.group(0)

    processed_body = re.sub(
        r'!?\[\[([^\]]+\.md)(?:\|([^\]]*))?\]\]',
        _mermaid_png_fallback,
        processed_body,
    )
    processed_body = _preprocess_markdown(processed_body)
    return fm, source_body, processed_body


def precheck_file(
    md_path: Path,
    verbose: bool = False,
) -> WordFormulaPrecheckReport:
    """Run Word handout source precheck v1 for one markdown handout."""
    if not md_path.exists():
        raise FileNotFoundError(md_path)
    _, body, processed_body = _prepare_handout_markdown(md_path, verbose=verbose)
    report = _run_word_formula_precheck(md_path, body, processed_body)
    _emit_word_formula_precheck(report, verbose=verbose, include_info=True)
    return report


# ══════════════════════════════════════════════════════════════════
#  Stage 2: Pandoc Conversion
# ══════════════════════════════════════════════════════════════════

def pandoc_convert(
    md_path: Path,
    docx_path: Path,
    resource_path: str,
    verbose: bool = False,
) -> None:
    """Convert preprocessed Markdown to .docx with OMML math.

    Pandoc automatically handles:
      - $...$ inline math   → OMML formula
      - $$...$$ display math → OMML formula
      - Markdown tables      → Word tables
      - ![](image.png)       → embedded image
    """
    lua_filter_path = SCRIPT_DIR / "callout_to_style.lua"
    extra_args = [
        f"--from={PANDOC_EXTENSIONS}",
        "--to=docx",
        f"--resource-path={resource_path}",
        f"--reference-doc={REFERENCE_DOC}",
        f"--lua-filter={lua_filter_path}",
    ]

    if verbose:
        print(f"  [pandoc] Converting to docx...", file=sys.stderr)
        print(f"  [pandoc] Resource path: {resource_path}", file=sys.stderr)

    pypandoc.convert_file(
        str(md_path),
        "docx",
        outputfile=str(docx_path),
        extra_args=extra_args,
    )


def _build_cover_meta(
    md_path: Path,
    fm: dict[str, Any],
    body: str,
) -> dict[str, str]:
    """从章节文件 frontmatter/路径构建封面元信息。"""
    chapter_title = _extract_markdown_h1(body) or build_title(fm)
    part_label = ""
    parent = md_path.parent.name
    part_match = re.match(r"^(第[一二三四五六七八九十]+篇)[-—]?\s*(.+)$", parent)
    if part_match:
        part_label = f"{part_match.group(1)} {part_match.group(2)}"
    else:
        part_label = parent

    question_count = ""
    raw_count = fm.get("question_count")
    if raw_count is not None:
        question_count = str(raw_count)
    else:
        q_nums = re.findall(r"^###\s*第\d+题", body, flags=re.MULTILINE)
        if q_nums:
            question_count = str(len(q_nums))

    edition = str(fm.get("edition", "")).strip()
    if edition == "teacher":
        edition_label = "教师版（含答案）"
    elif edition == "student":
        edition_label = "学生版（无答案）"
    elif edition:
        edition_label = edition
    else:
        edition_label = ""

    return {
        "book_title": "化学竞赛习题册",
        "part_label": part_label,
        "chapter_title": chapter_title,
        "question_count": question_count,
        "edition_label": edition_label,
        "date": date_cls.today().isoformat(),
    }


def postprocess(
    docx_path: Path,
    verbose: bool = False,
    cover_meta: dict[str, str] | None = None,
) -> None:
    """Fix fonts on pandoc-generated docx, add page numbers, center title."""
    if verbose:
        print(f"  [fonts] Post-processing...", file=sys.stderr)
    if cover_meta:
        add_exercise_cover(docx_path, **cover_meta)
    postprocess_pandoc_docx(
        docx_path,
        center_title=True,
        add_page_numbers=True,
    )


# ══════════════════════════════════════════════════════════════════
#  Main: Batch Processing
# ══════════════════════════════════════════════════════════════════

def convert_file(
    md_path: Path,
    verbose: bool = False,
    dry_run: bool = False,
    output_dir: Path | None = None,
    render_preview: bool = False,
    render_output_dir: Path | None = None,
    emit_render_pdf: bool = False,
    word_clean: bool = False,
    strict_images: bool = False,
    cover: bool = False,
    output_stem: str | None = None,
) -> Path | None:
    """Convert a single .md handout to .docx via the three-stage pipeline.

    Returns output Path on success, None if skipped.
    """
    if not md_path.exists():
        print(f"  [SKIP] File not found: {md_path}", file=sys.stderr)
        return None

    # ── Read & parse ──
    fm, body, processed_body = _prepare_handout_markdown(
        md_path,
        verbose=verbose,
        word_clean=word_clean,
    )
    cover_meta = _build_cover_meta(md_path, fm, body) if cover else None
    if output_stem is not None:
        stem = output_stem
    elif word_clean:
        title_candidate = _extract_markdown_h1(body) or build_title(fm)
        stem = _clean_word_title(title_candidate) + "（Word清稿）"
    else:
        stem = md_path.stem
    stem = re.sub(r'[\\/:*?"<>|]+', "-", stem).strip()
    out_dir = Path(output_dir) if output_dir else HANDOUT_OUT
    out_path = out_dir / f"{stem}.docx"

    if dry_run:
        print(f"  [DRY] {md_path.name}  →  {out_path.name}")
        return None

    if verbose:
        yaml_title = fm.get("title", "")
        print(f"  YAML title: {yaml_title!r}", file=sys.stderr)

    report = _run_word_formula_precheck(md_path, body, processed_body)
    if report.has_errors:
        raise RuntimeError(report.render(limit=12, severities={"ERROR", "WARN"}))
    if report.issues:
        _emit_word_formula_precheck(report, verbose=verbose)

    # Use the body as-is — its first line is already # 第N讲：标题
    full_md = processed_body

    # Write to temp file
    out_dir.mkdir(parents=True, exist_ok=True)
    # Unique per-process/thread temp base so parallel workers never collide on the
    # same `_{stem}.tmp.*` path.
    tmp_id = f"{os.getpid()}-{threading.get_ident()}"
    tmp_md = out_dir / f"_{stem}.{tmp_id}.tmp.md"
    tmp_md.write_text(full_md, encoding="utf-8")
    resource_path = _build_resource_path(md_path, out_dir)

    try:
        # ── Stage 2: Pandoc ──
        tmp_docx = out_dir / f"_{stem}.{tmp_id}.tmp.docx"
        pandoc_convert(tmp_md, tmp_docx, resource_path=resource_path, verbose=verbose)

        # ── Stage 3: Post-process fonts ──
        postprocess(tmp_docx, verbose=verbose, cover_meta=cover_meta)

        # ── Stage 3.5: Post-generation validation ──
        _validate_docx(
            tmp_docx,
            md_path,
            tmp_md,
            verbose=verbose,
            strict_images=strict_images,
        )

        # ── Rename temp → final ──
        _atomic_replace(tmp_docx, out_path)

        if render_preview:
            preview_dir = _render_docx_preview(
                out_path,
                render_output_dir=render_output_dir,
                emit_pdf=emit_render_pdf,
                verbose=verbose,
            )
            if verbose:
                print(f"  [render] Preview written to {preview_dir}", file=sys.stderr)

    finally:
        # Cleanup temp markdown
        if tmp_md.exists():
            tmp_md.unlink()

    return out_path


def _validate_docx(
    docx_path: Path,
    md_source: Path,
    md_preprocessed: Path,
    verbose: bool = False,
    strict_images: bool = False,
) -> None:
    """Validate generated docx for common issues.

    Checks:
    1) docx file size is reasonable (> 10 KB)
    2) Core OOXML members are present
    3) Image count in docx roughly matches expected image refs
    4) No raw [[wikilink]] syntax leaked through
    5) OMML math count roughly matches markdown math count
    """
    issues: list[str] = []

    # Check 1: file size
    size = docx_path.stat().st_size
    if size < 10_240:
        issues.append(f"docx too small: {size} bytes (< 10 KB)")

    # Check 2: image count match
    source_text = md_source.read_text(encoding="utf-8")
    # Match ALL image embeds: ![[media/...]], ![[mineru/...]], ![[06-外部资料导入/...]], etc.
    src_images = set(re.findall(r'!\[\[([^\]]+)', source_text))
    # Also match preprocessed markdown image embeds (converted to ![](path) format)
    prep_text = md_preprocessed.read_text(encoding="utf-8") if md_preprocessed.exists() else ""
    prep_images = set(re.findall(r'!\[.*?\]\(([^)]+)\)', prep_text))
    expected_math = _count_markdown_math_expressions(prep_text)

    # Hard loss signals (raised in strict mode): a *real* media slot is missing, or a
    # source image ref cannot be resolved to any file on disk at all.
    image_issues: list[str] = []
    # Diagnostic-only signals (always WARN, never strict-raise): pandoc legitimately
    # re-encodes images (.png → .jpg), so a docx media sha256 won't always equal the
    # source file's. A content mismatch here is NOT proof of a dropped image.
    image_diagnostics: list[str] = []

    import zipfile
    try:
        with zipfile.ZipFile(docx_path) as z:
            namelist = set(z.namelist())
            # Count REAL media files. The `word/media/` directory entry is NOT an image.
            docx_images = [
                n for n in namelist
                if n.startswith("word/media/") and not n.endswith("/")
            ]
            document_xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    except Exception as exc:
        issues.append(f"docx zip validation failed: {exc}")
        namelist = set()
        docx_images = []
        document_xml = ""

    required_members = {
        "[Content_Types].xml",
        "word/document.xml",
        "word/styles.xml",
    }
    missing_members = required_members - namelist
    if missing_members:
        issues.append(f"missing OOXML members: {sorted(missing_members)}")

    expected_images = prep_images or src_images

    # ── Content-level image reconciliation ──
    # Count alone is unreliable (re-encoded images, a `word/media/` dir entry, or a
    # pandoc silent drop all shift media counts). Resolve each source image ref to its
    # on-disk file and compare sha256 against the actual docx media payload.
    expected_media_hashes: dict[str, str] = {}
    missing_refs: list[str] = []

    def _resolve_image_ref(ref: str) -> Path | None:
        """Resolve an Obsidian image ref against the same roots pandoc searches."""
        base = Path(ref)
        candidates = [
            md_source.parent / base,
            VAULT_ROOT / base,
            VAULT_MEDIA / base,
            md_preprocessed.parent / base,
        ]
        for cand in candidates:
            if cand.exists() and cand.is_file():
                return cand
        return None

    for ref in expected_images:
        found = _resolve_image_ref(ref)
        if found is None:
            missing_refs.append(ref)
            continue
        try:
            expected_media_hashes[ref] = hashlib.sha256(found.read_bytes()).hexdigest()
        except OSError:
            missing_refs.append(ref)

    # Actual docx media payload hashes.
    docx_media_hashes: set[str] = set()
    if docx_images:
        with zipfile.ZipFile(docx_path) as z:
            for name in docx_images:
                docx_media_hashes.add(hashlib.sha256(z.read(name)).hexdigest())

    missing_content_refs = [
        ref for ref, h in expected_media_hashes.items() if h not in docx_media_hashes
    ]

    if expected_images and not docx_images:
        image_issues.append(
            f"Expected {len(expected_images)} image(s) but docx has 0 — "
            f"images did not render"
        )
    elif len(docx_images) < len(expected_images):
        image_issues.append(
            f"{len(expected_images) - len(docx_images)} image(s) lost: expected "
            f"{len(expected_images)}, docx {len(docx_images)}"
        )
    if missing_refs:
        image_issues.append(
            f"{len(missing_refs)} image ref(s) unresolvable on disk: {missing_refs[:4]}"
        )
    if missing_content_refs:
        image_diagnostics.append(
            f"{len(missing_content_refs)} image(s) content differs from source "
            f"(likely pandoc re-encode, not a loss): {missing_content_refs[:4]}"
        )

    # Check 3: raw wikilink leakage (only in preprocessed, not source)
    # Source legitimately has wikilinks; check the preprocessed version
    if prep_text:
        leaked = re.findall(r'\[\[([^\]]+)\]\]', prep_text)
        if leaked:
            issues.append(
                f"{len(leaked)} raw [[wikilink]]s leaked through preprocessing: "
                f"{leaked[:3]}..."
            )

    if document_xml:
        if "**" in document_xml:
            issues.append(
                "Literal `**` leaked into generated docx XML — likely malformed strong markup"
            )
        docx_math = len(re.findall(r"<m:oMath(?:\s|>)", document_xml))
        if expected_math and docx_math == 0:
            issues.append(
                f"Expected {expected_math} math expression(s) but docx has 0 OMML objects"
            )
        elif expected_math <= 2 and docx_math < expected_math:
            issues.append(
                f"Math count mismatch: expected about {expected_math}, docx OMML {docx_math}"
            )
        elif expected_math >= 3 and docx_math * 10 < expected_math * 6:
            issues.append(
                f"Math count suspiciously low: expected about {expected_math}, docx OMML {docx_math}"
            )

    # Check 4: answer-question number alignment (for exercise sets)
    if source_text:
        # Extract question numbers from "### 第N题" headings
        q_nums = set(re.findall(r'###\s*第(\d+)题', source_text))
        # Extract answer numbers from "**第N题**:" or "**第N题**：" markers
        a_nums = set(re.findall(r'\*\*第(\d+)题\*\*\s*[：:]', source_text))
        if q_nums and a_nums:
            missing_answers = q_nums - a_nums
            extra_answers = a_nums - q_nums
            if missing_answers:
                sorted_missing = sorted(missing_answers, key=int)
                issues.append(
                    f"Questions without answers: {sorted_missing}"
                )
            if extra_answers:
                sorted_extra = sorted(extra_answers, key=int)
                issues.append(
                    f"Answers without matching question: {sorted_extra}"
                )

    # Merge image gate findings into the report. In strict mode, a *real* image loss is
    # a hard failure (raise) rather than a WARN, so a silently-dropped figure blocks the
    # conversion instead of being reported as "OK". Diagnostic-only findings (possible
    # pandoc re-encode) never raise, even in strict mode.
    if image_issues:
        issues.extend(image_issues)
    if image_diagnostics:
        print(
            f"  [WARN] Image diag: {'; '.join(image_diagnostics)}",
            file=sys.stderr,
        )

    if issues:
        if strict_images and image_issues:
            raise RuntimeError(
                "Strict image validation failed: " + "; ".join(image_issues)
            )
        print(f"  [WARN] Validation: {'; '.join(issues)}", file=sys.stderr)
    elif verbose:
        print(
            f"  [OK] Validation passed "
            f"(size={size}B, images={len(docx_images)}, math={expected_math})"
        )


def _run_self_tests() -> bool:
    """Internal regression self-tests for preprocess helpers.

    Guard against the 2026-08-05 regression where `_strip_metadata_blockquote`
    silently deleted document-head content (图1/图2) whenever a handout had no
    title-adjacent metadata blockquote.
    """
    ok = True

    # Case 1: 标题后直接跟正文/图片，无元信息 blockquote —— 头部必须原样保留
    case_head_no_meta = (
        "# 结构化学第一轮复习\n"
        "\n"
        "## 目录\n"
        "- §1 元素周期律与元素周期系（考纲§4）\n"
        "\n"
        "![[ad990d2119aabbf46ff0645d1a49344a959b58d7ba554502912e765280ac770f.jpg]]\n"
    )
    out = _strip_metadata_blockquote(case_head_no_meta)
    if "## 目录" not in out or "ad990d2119aabb" not in out:
        print("  [FAIL] _strip_metadata_blockquote: 无元信息 blockquote 时误删头部内容", file=sys.stderr)
        ok = False
    else:
        print("  [OK] _strip_metadata_blockquote keeps head when no metadata blockquote", file=sys.stderr)

    # Case 2: 标准元信息 blockquote + --- 分隔线 —— 应剥离 blockquote、保留 --- 与后续标题
    case_with_meta = (
        "# 第四讲：化学平衡\n"
        "\n"
        "> **适用**：第一轮（初学）→ 第二轮（深化）\n"
        "> **对应备课大纲**：[[...]]\n"
        "> **前置要求**：热力学基础\n"
        "\n"
        "---\n"
        "\n"
        "## 学习目标\n"
    )
    out = _strip_metadata_blockquote(case_with_meta)
    if "**适用**" in out or "**前置要求**" in out:
        print("  [FAIL] _strip_metadata_blockquote: 未剥离元信息 blockquote", file=sys.stderr)
        ok = False
    else:
        print("  [OK] _strip_metadata_blockquote strips standard metadata blockquote", file=sys.stderr)

    # Case 3: 纯标题 + 正文（无 blockquote、无分隔线）—— 原样返回
    case_title_only = "# 某讲义\n\n正文直接开始。\n"
    out = _strip_metadata_blockquote(case_title_only)
    if out.strip() != case_title_only.strip():
        print("  [FAIL] _strip_metadata_blockquote: 纯标题文档被改动", file=sys.stderr)
        ok = False
    else:
        print("  [OK] _strip_metadata_blockquote keeps title-only doc", file=sys.stderr)

    # Case 4: 长 blockquote（超级充实版多行元信息）后跟 --- —— 只保留标题 + --- + 之后内容
    case_long_meta = (
        "# 原子结构\n"
        "\n"
        "> **本讲定位**：第一轮初学 → 第二轮深化参照\n"
        "> **深度边界**：第一轮聚焦量子数、电子排布、Slater；\n"
        "> 不展开角动量耦合、完整 Rydberg 方程推导。\n"
        "> **版本说明**：v5.0\n"
        "\n"
        "---\n"
        "\n"
        "## 一、量子数与轨道\n"
    )
    out = _strip_metadata_blockquote(case_long_meta)
    if "**本讲定位**" in out or "**深度边界**" in out or "**版本说明**" in out:
        print("  [FAIL] _strip_metadata_blockquote: 未剥离长元信息 blockquote", file=sys.stderr)
        ok = False
    else:
        print("  [OK] _strip_metadata_blockquote strips long metadata blockquote", file=sys.stderr)

    return ok


def main():
    parser = argparse.ArgumentParser(
        description="Batch-convert all student handouts from .md to .docx (v2)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List files that would be processed without converting",
    )
    parser.add_argument(
        "--precheck-only", action="store_true",
        help="Run Word source precheck (formula + Mermaid) without converting to docx",
    )
    parser.add_argument(
        "--file", type=str, default=None,
        help="Convert a single file (substring match on filename, e.g. '滴定分析')",
    )
    parser.add_argument(
        "--path", type=str, default=None,
        help="Convert one explicit markdown file path",
    )
    parser.add_argument(
        "--batch-root", type=str, default=None,
        help="Batch-convert all chapter .md files under a root directory "
             "(excludes 目录.md)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Detailed per-file processing log",
    )
    parser.add_argument(
        "--output-dir", type=str, default=None,
        help="Output directory (default: 00-首页/学生讲义Word)",
    )
    parser.add_argument(
        "--parallel", type=int, nargs="?", const=4, default=None,
        help="Enable parallel processing with N workers (default: 4). "
             "Only effective for batch (non --file) mode.",
    )
    parser.add_argument(
        "--render-preview", action="store_true",
        help="Render generated DOCX files to page PNGs for visual QA",
    )
    parser.add_argument(
        "--word-clean", action="store_true",
        help="Generate a student-facing Word clean copy that removes intro scaffolding and vault-only links",
    )
    parser.add_argument(
        "--render-output-dir", type=str, default=None,
        help="Root directory for rendered preview folders",
    )
    parser.add_argument(
        "--emit-render-pdf", action="store_true",
        help="Keep the intermediate PDF when rendering preview pages",
    )
    parser.add_argument(
        "--self-test", action="store_true",
        help="Run internal regression self-tests (e.g. _strip_metadata_blockquote) and exit",
    )
    parser.add_argument(
        "--strict-images", action="store_true",
        help="Hard-fail conversion when any source image is missing from the generated "
             "docx (count or content-hash mismatch), instead of only warning",
    )
    parser.add_argument(
        "--cover", action="store_true",
        help="Insert a chapter cover page (book/part/chapter title, question count, date)",
    )
    args = parser.parse_args()

    if args.self_test:
        ok = _run_self_tests()
        sys.exit(0 if ok else 1)

    if args.dry_run and args.precheck_only:
        print("ERROR: --dry-run and --precheck-only cannot be used together", file=sys.stderr)
        sys.exit(2)

    output_dir = Path(args.output_dir).resolve() if args.output_dir else HANDOUT_OUT
    render_output_dir = (
        Path(args.render_output_dir).resolve()
        if args.render_output_dir else None
    )

    # ── Optional exercise-book batch root (chapter files under 篇 dirs) ──
    if args.batch_root:
        batch_root = Path(args.batch_root).expanduser().resolve()
        if not batch_root.is_dir():
            print(f"ERROR: batch root not found: {batch_root}", file=sys.stderr)
            sys.exit(2)
        all_md = sorted(
            p for p in batch_root.rglob("*.md")
            if p.stem != "目录"
            and p.stem != "README"
            and not p.stem.startswith("_未分类")
        )
        if not all_md:
            print(f"ERROR: no chapter .md files under {batch_root}", file=sys.stderr)
            sys.exit(2)
        print(f"Found {len(all_md)} chapter files in {batch_root}")
        files = all_md
        # Different 篇 (sections) may legitimately re-use the same chapter stem
        # (e.g. "1-化学基础与计量" exists in both 化学原理 and 元素与分析).
        # Output is named by stem only, so a duplicate stem would silently
        # overwrite another chapter's .docx. Detect collisions and disambiguate
        # by prefixing with the parent section folder name.
        stem_counts: dict[str, int] = {}
        for md_path in files:
            stem = re.sub(r'[\\/:*?"<>|]+', "-", md_path.stem).strip()
            stem_counts[stem] = stem_counts.get(stem, 0) + 1
        output_stem_by_path: dict[Path, str | None] = {p: None for p in files}
        for md_path in files:
            stem = re.sub(r'[\\/:*?"<>|]+', "-", md_path.stem).strip()
            if stem_counts[stem] > 1:
                section = md_path.parent.name
                output_stem_by_path[md_path] = f"{section}-{stem}"
        if any(s for s in output_stem_by_path.values()):
            print(
                "Note: disambiguating duplicate chapter stems via parent section "
                "folder: " + ", ".join(
                    f"{p.name} -> {s}" for p, s in output_stem_by_path.items() if s
                )
            )
        print(f"Selected {len(files)} for processing")
        if args.precheck_only:
            print("Mode: Word source precheck only (formula + Mermaid)\n")
        elif args.dry_run:
            print("Dry-run mode — no files will be written:\n")
        else:
            print(f"Output: {output_dir}\n")
        # ── Process ──
        success = 0
        errors = 0

        if args.precheck_only:
            for md_path in files:
                print(f"[CHK] {md_path.name}")
                try:
                    report = precheck_file(md_path, verbose=args.verbose)
                    if report.has_errors:
                        errors += 1
                    else:
                        success += 1
                except Exception as e:
                    print(f"  [ERROR] {e}", file=sys.stderr)
                    if args.verbose:
                        import traceback
                        traceback.print_exc(file=sys.stderr)
                    errors += 1
        elif args.parallel and not args.dry_run:
            import concurrent.futures
            n_workers = args.parallel if isinstance(args.parallel, int) else 4
            print(f"Parallel mode: {n_workers} workers\n")

            def _convert_one(md_path: Path) -> tuple[str, bool | str]:
                try:
                    dynamic_output_dir = output_dir / md_path.parent.relative_to(batch_root) if args.batch_root else output_dir
                    dynamic_output_dir.mkdir(parents=True, exist_ok=True)
                    out = convert_file(
                        md_path,
                        verbose=args.verbose,
                        output_dir=dynamic_output_dir,
                        render_preview=args.render_preview,
                        render_output_dir=render_output_dir,
                        emit_render_pdf=args.emit_render_pdf,
                        word_clean=args.word_clean,
                        strict_images=args.strict_images,
                        cover=args.cover,
                        output_stem=output_stem_by_path.get(md_path),
                    )
                    if out:
                        return (md_path.name, True)
                    return (md_path.name, "skipped")
                except Exception as e:
                    if args.verbose:
                        import traceback
                        traceback.print_exc(file=sys.stderr)
                    return (md_path.name, str(e))

            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers) as pool:
                futures = {pool.submit(_convert_one, p): p for p in files}
                for future in concurrent.futures.as_completed(futures):
                    fname, status = future.result()
                    if status is True:
                        results.append((fname, True))
                        print(f"[OK] {fname}  →  converted")
                    else:
                        results.append((fname, status))
                        print(f"[ERR] {fname}  →  {status}", file=sys.stderr)

            success = sum(1 for _, s in results if s is True)
            errors = sum(1 for _, s in results if s is not True)
        else:
            for md_path in files:
                label = "DRY" if args.dry_run else ".."
                print(f"[{label}] {md_path.name}", end="")
                if args.dry_run:
                    print()
                    continue
                try:
                    dynamic_output_dir = output_dir / md_path.parent.relative_to(batch_root) if args.batch_root else output_dir
                    dynamic_output_dir.mkdir(parents=True, exist_ok=True)
                    out = convert_file(
                        md_path,
                        verbose=args.verbose,
                        output_dir=dynamic_output_dir,
                        render_preview=args.render_preview,
                        render_output_dir=render_output_dir,
                        emit_render_pdf=args.emit_render_pdf,
                        word_clean=args.word_clean,
                        strict_images=args.strict_images,
                        cover=args.cover,
                        output_stem=output_stem_by_path.get(md_path),
                    )
                    if out:
                        print(f"  →  {out.name}")
                        success += 1
                    else:
                        print("  [skipped]")
                except Exception as e:
                    print(f"  [ERROR] {e}", file=sys.stderr)
                    if args.verbose:
                        import traceback
                        traceback.print_exc(file=sys.stderr)
                    errors += 1

        print()
        if args.precheck_only:
            print(f"Precheck complete. Passed: {success}, Files with errors: {errors}.")
            sys.exit(1 if errors else 0)
        if args.dry_run:
            print(f"Dry-run complete. {len(files)} files listed.")
            sys.exit(0)
        print(f"Done. {success} converted, {errors} errors.")
        sys.exit(1 if errors else 0)

    # ── Gather input files ──
    all_md = sorted(HANDOUT_SRC.glob(SRC_GLOB))
    if not all_md:
        print(f"ERROR: No files matching '{SRC_GLOB}' found in {HANDOUT_SRC}", file=sys.stderr)
        sys.exit(1)

    # Skip non-handout files
    EXCLUDED_STEMS = {"README"}
    EXCLUDED_PREFIXES = {"讲义升级模式-"}
    # 标准学生讲义（批量默认范围）：超级充实版 / 第一轮基础版 / 复习课 / 新课
    HANDOUT_MARKERS = ("超级充实", "基础版", "复习", "-新课")

    candidates = [
        f for f in all_md
        if f.stem not in EXCLUDED_STEMS
        and not any(f.stem.startswith(p) for p in EXCLUDED_PREFIXES)
    ]
    # 批量默认只处理标准讲义；--file/--path 可在 candidates 内任意指定
    all_md = [f for f in candidates if any(m in f.stem for m in HANDOUT_MARKERS)]

    if args.path:
        explicit = Path(args.path).expanduser().resolve()
        if not explicit.exists():
            print(f"ERROR: File not found: {explicit}", file=sys.stderr)
            sys.exit(1)
        if explicit.suffix.lower() != ".md":
            print(f"ERROR: Not a markdown file: {explicit}", file=sys.stderr)
            sys.exit(1)
        files = [explicit]
    elif args.file:
        # --file 按名字匹配任意学生讲义（含复习课/新课/专题合集等非批量默认文件）
        files = [f for f in candidates if args.file in f.stem]
        if not files:
            print(f"ERROR: No files match --file '{args.file}'", file=sys.stderr)
            print(f"  Available: {[f.stem for f in candidates]}", file=sys.stderr)
            sys.exit(1)
    else:
        files = all_md

    print(f"Found {len(all_md)} handouts in {HANDOUT_SRC}")
    print(f"Selected {len(files)} for processing")
    if args.precheck_only:
        print("Mode: Word source precheck only (formula + Mermaid)\n")
    elif args.dry_run:
        print("Dry-run mode — no files will be written:\n")
    else:
        print(f"Output: {output_dir}\n")

    # ── Process ──
    success = 0
    errors = 0

    if args.precheck_only:
        for md_path in files:
            print(f"[CHK] {md_path.name}")
            try:
                report = precheck_file(md_path, verbose=args.verbose)
                if report.has_errors:
                    errors += 1
                else:
                    success += 1
            except Exception as e:
                print(f"  [ERROR] {e}", file=sys.stderr)
                if args.verbose:
                    import traceback
                    traceback.print_exc(file=sys.stderr)
                errors += 1

    elif args.parallel and not (args.file or args.path) and not args.dry_run:
        # ── Parallel mode ──
        import concurrent.futures
        n_workers = args.parallel if isinstance(args.parallel, int) else 4
        print(f"Parallel mode: {n_workers} workers\n")

        def _convert_one(md_path: Path) -> tuple[str, bool | str]:
            """Wrapper for parallel execution; returns (filename, True|error_msg)."""
            try:
                out = convert_file(
                    md_path,
                    verbose=args.verbose,
                    output_dir=output_dir,
                    render_preview=args.render_preview,
                    render_output_dir=render_output_dir,
                    emit_render_pdf=args.emit_render_pdf,
                    word_clean=args.word_clean,
                    strict_images=args.strict_images,
                    cover=args.cover,
                )
                if out:
                    return (md_path.name, True)
                return (md_path.name, "skipped")
            except Exception as e:
                if args.verbose:
                    import traceback
                    traceback.print_exc(file=sys.stderr)
                return (md_path.name, str(e))

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers) as pool:
            futures = {pool.submit(_convert_one, p): p for p in files}
            for future in concurrent.futures.as_completed(futures):
                fname, status = future.result()
                if status is True:
                    results.append((fname, True))
                    print(f"[OK] {fname}  →  converted")
                else:
                    results.append((fname, status))
                    print(f"[ERR] {fname}  →  {status}", file=sys.stderr)

        success = sum(1 for _, s in results if s is True)
        errors = sum(1 for _, s in results if s is not True)

    else:
        # ── Sequential mode (original) ──
        for md_path in files:
            label = "DRY" if args.dry_run else ".."
            print(f"[{label}] {md_path.name}", end="")

            if args.dry_run:
                print()
                continue

            dynamic_output_dir = output_dir / md_path.parent.relative_to(batch_root) if args.batch_root else output_dir
            dynamic_output_dir.mkdir(parents=True, exist_ok=True)
            try:
                out = convert_file(
                    md_path,
                    verbose=args.verbose,
                    output_dir=dynamic_output_dir,
                    render_preview=args.render_preview,
                    render_output_dir=render_output_dir,
                    emit_render_pdf=args.emit_render_pdf,
                    word_clean=args.word_clean,
                    strict_images=args.strict_images,
                    cover=args.cover,
                    output_stem=output_stem_by_path.get(md_path) if 'output_stem_by_path' in locals() else None,
                )
                if out:
                    print(f"  →  {out.name}")
                    success += 1
                else:
                    print("  [skipped]")
            except Exception as e:
                print(f"  [ERROR] {e}", file=sys.stderr)
                if args.verbose:
                    import traceback
                    traceback.print_exc(file=sys.stderr)
                errors += 1

    # ── Summary ──
    print()
    if args.precheck_only:
        print(f"Precheck complete. Passed: {success}, Files with errors: {errors}.")
        if errors:
            sys.exit(1)
    elif args.dry_run:
        print(f"Dry-run complete. {len(files)} files listed.")
    else:
        print(f"Done. {success} converted, {errors} errors.")
        if errors:
            sys.exit(1)


if __name__ == "__main__":
    main()
