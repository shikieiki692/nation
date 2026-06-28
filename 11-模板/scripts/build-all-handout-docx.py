#!/usr/bin/env python3
"""
Batch converter: Markdown student handouts → uniformly formatted .docx (v2)

三段式管线：
  1. Preprocess  — 剥 YAML frontmatter、解 [[wiki-link]]、预处理 \\ce{} 为 \\text{}
  2. Pandoc      — pypandoc 转换 markdown → docx（自动 LaTeX → OMML 公式）
  3. Postprocess — python-docx 修正字体（正文 SimSun / 标题 SimHei / 英文 TNR）

用法:
    python build-all-handout-docx.py                          # 全量转换
    python build-all-handout-docx.py --dry-run                # 预览文件列表
    python build-all-handout-docx.py --file 化学平衡          # 单文件测试
    python build-all-handout-docx.py --file 原子结构 -v       # 单文件详细日志

依赖: python-docx, PyYAML, pypandoc (pandoc 3.9+)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

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
from docx_utils import postprocess_pandoc_docx

# ── Paths ────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent
HANDOUT_SRC = VAULT_ROOT / "04-课件" / "学生讲义"
HANDOUT_OUT = VAULT_ROOT / "06-学生侧材料" / "讲义"

SRC_GLOB = "*.md"

# Pandoc 转换扩展
PANDOC_EXTENSIONS = "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_tex"

# 参考模板（字体/页边距已预设好）
REFERENCE_DOC = SCRIPT_DIR / "templates" / "custom-reference.docx"


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


def _transform_callout_blocks(text: str) -> str:
    """Transform emoji-prefixed callout blockquotes to bold-led paragraphs.

    Obsidian callouts (> 🧠/🗣️/⚠️/etc...) render as plain indented text in Word.
    This converts them to normal paragraphs with bold headers that stand out.

    Before:   > 🧠 **教学洞察**：内容
    After:    **🧠 教学洞察**：内容

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
            # Boldify the emoji + bold header on the first line
            if block:
                first = block[0]
                first = re.sub(
                    r'^([' + CALLOUT_EMOJIS + r'])\s*\*\*(.*?)\*\*',
                    r'**\1 \2**',
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
    """Convert \\ce{...} → \\text{...} inside math ($...$ / $$...$$) for OMML compat.

    Pandoc passes \\ce{} through to OMML, but OMML doesn't understand the
    mhchem package macros.  Wrapping in \\text{} preserves the content as
    readable upright text in the Word equation editor.
    """
    return re.sub(r'\\ce\{([^}]*)\}', r'\\text{\1}', text)


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

    # Scan for blockquote region followed by ---
    in_bq = False
    first_div = -1
    for i in range(first_h + 1, len(lines)):
        ln = lines[i]
        if ln.startswith("> "):
            in_bq = True
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

    if first_div < 0:
        return text

    # Keep: heading + blank line + divider + everything after
    kept = lines[: first_h + 1] + ["", lines[first_div]] + lines[first_div + 1 :]
    return "\n".join(kept)


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

    # 1) Image embeds: ![[image.png]] or ![[image.png|alt text]] → ![alt](image.png)
    text = re.sub(
        r'!\[\[([^\]]+?)\.(png|jpg|jpeg|gif|webp|svg)(?:\|([^\]]*))?\]\]',
        lambda m: f'![{m.group(3) or ""}]({m.group(1)}.{m.group(2)})',
        text, flags=re.IGNORECASE)

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

    # 1d) Remove ⚠️ and 💡 emoji symbols (formatting artifacts)


    # 2) Convert \ce{...} → \text{...} inside math blocks
    #    First handle display math $$...$$
    text = re.sub(r'(\$\$[^$]*?)\\ce\{([^}]*)\}([^$]*?\$\$)',
                  lambda m: m.group(1) + '\\text{' + m.group(2) + '}' + m.group(3),
                  text)
    #    Then handle inline math $...$
    text = re.sub(r'(\$[^$]*?)\\ce\{([^}]*)\}([^$]*?\$)',
                  lambda m: m.group(1) + '\\text{' + m.group(2) + '}' + m.group(3),
                  text)

    # 3) Wiki-links to plain text
    text = _resolve_wikilink(text)

    # 4a) \overset{+6}{Cr} / \overset{+6}{\mathrm{Cr_2}} → Cr^{(+6)} / \mathrm{Cr_2}^{(+6)}
    #     (oxidation number notation; no extra \mathrm wrapping to avoid nesting issues)
    _arg = r'(\{(?:[^{}]|\{[^{}]*\})*\})'
    text = re.sub(r'\\overset' + _arg + _arg,
                  lambda m: m.group(2)[1:-1] + '^{(' + m.group(1)[1:-1] + ')}',
                  text)

    # 4b) \underset{text}{formula} → formula (text)
    #     (label underneath; handles one level of nested braces)
    text = re.sub(r'\\underset' + _arg + _arg,
                  lambda m: m.group(2)[1:-1] + ' \\;(' + m.group(1)[1:-1] + ')',
                  text)

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


# ══════════════════════════════════════════════════════════════════
#  Stage 2: Pandoc Conversion
# ══════════════════════════════════════════════════════════════════

def pandoc_convert(md_path: Path, docx_path: Path, resource_path: Path, verbose: bool = False) -> None:
    """Convert preprocessed Markdown to .docx with OMML math.

    Pandoc automatically handles:
      - $...$ inline math   → OMML formula
      - $$...$$ display math → OMML formula
      - Markdown tables      → Word tables
      - ![](image.png)       → embedded image
    """
    extra_args = [
        f"--from={PANDOC_EXTENSIONS}",
        "--to=docx",
        f"--resource-path={resource_path}",
        f"--reference-doc={REFERENCE_DOC}",
    ]

    if verbose:
        print(f"  [pandoc] Converting to docx...", file=sys.stderr)

    pypandoc.convert_file(
        str(md_path),
        "docx",
        outputfile=str(docx_path),
        extra_args=extra_args,
    )


# ══════════════════════════════════════════════════════════════════
#  Stage 3: Post-process Fonts (via docx_utils)
# ══════════════════════════════════════════════════════════════════

def _add_page_numbers(docx_path: Path) -> None:
    """Add centered page number footer to the document."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn as oxml_qn
    from docx import Document as DxDoc

    doc = DxDoc(str(docx_path))
    for section in doc.sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        p = footer.paragraphs[0]
        p.alignment = 1  # WD_ALIGN_PARAGRAPH.CENTER

        # Build run with PAGE field
        run = p.add_run()
        fldChar1 = OxmlElement("w:fldChar")
        fldChar1.set(oxml_qn("w:fldCharType"), "begin")
        run._element.append(fldChar1)

        run2 = p.add_run()
        instrText = OxmlElement("w:instrText")
        instrText.set(oxml_qn("xml:space"), "preserve")
        instrText.text = " PAGE "
        run2._element.append(instrText)

        run3 = p.add_run()
        fldChar2 = OxmlElement("w:fldChar")
        fldChar2.set(oxml_qn("w:fldCharType"), "end")
        run3._element.append(fldChar2)

    doc.save(str(docx_path))


def _center_first_heading(docx_path: Path) -> None:
    """Center the first Heading 1 paragraph (the document title)."""
    from docx import Document as DxDoc
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn as oxml_qn

    doc = DxDoc(str(docx_path))
    for para in doc.paragraphs:
        pPr = para._element.find(oxml_qn("w:pPr"))
        if pPr is None:
            continue
        pStyle = pPr.find(oxml_qn("w:pStyle"))
        if pStyle is None:
            continue
        if pStyle.get(oxml_qn("w:val")) == "Heading1":
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            break
    doc.save(str(docx_path))


def postprocess(docx_path: Path, verbose: bool = False) -> None:
    """Fix fonts on pandoc-generated docx, add page numbers, center title."""
    if verbose:
        print(f"  [fonts] Post-processing...", file=sys.stderr)
    postprocess_pandoc_docx(docx_path)
    _center_first_heading(docx_path)
    _add_page_numbers(docx_path)


# ══════════════════════════════════════════════════════════════════
#  Main: Batch Processing
# ══════════════════════════════════════════════════════════════════

def convert_file(
    md_path: Path,
    verbose: bool = False,
    dry_run: bool = False,
    output_dir: Path | None = None,
) -> Path | None:
    """Convert a single .md handout to .docx via the three-stage pipeline.

    Returns output Path on success, None if skipped.
    """
    if not md_path.exists():
        print(f"  [SKIP] File not found: {md_path}", file=sys.stderr)
        return None

    stem = md_path.stem
    out_dir = Path(output_dir) if output_dir else HANDOUT_OUT
    out_path = out_dir / f"{stem}.docx"

    if dry_run:
        print(f"  [DRY] {md_path.name}  →  {out_path.name}")
        return None

    # ── Read & parse ──
    content = md_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    if verbose:
        yaml_title = fm.get("title", "")
        print(f"  YAML title: {yaml_title!r}", file=sys.stderr)

    # ── Stage 1: Preprocess ──
    processed_body = body

    # 1a) Strip metadata blockquote between title and first ---
    processed_body = _strip_metadata_blockquote(processed_body)
    # 1b) Strip attribution footer (*本讲义依据…*)
    processed_body = _strip_footer(processed_body)
    # 1b2) Auto-render Excalidraw .md files to PNG if no sibling PNG exists
    #      Uses the excalidraw-to-png.mjs script (Puppeteer headless browser)
    for excal_match in re.finditer(r'!?\[\[([^\]]+\.(?:md|excalidraw))(?:\|[^\]]*)?\]\]', processed_body):
        excal_path_str = excal_match.group(1)
        excal_full = md_path.parent / excal_path_str
        if not excal_full.exists():
            continue
        # Check if it's an Excalidraw file (has excalidraw-plugin frontmatter)
        try:
            first_lines = excal_full.read_text('utf-8', errors='replace')[:200]
            if 'excalidraw-plugin:' not in first_lines:
                continue
        except Exception:
            continue
        # Check if PNG sibling exists
        png_candidate = excal_full.with_suffix('.png')
        if png_candidate.exists():
            continue
        # Render Excalidraw → PNG
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

    # 1b3) Replace .md image embeds with rendered PNG (if available)
    #      The "Excalidraw" files are actually Mermaid diagrams; we render them to PNG.
    #      Fallback: if no PNG exists, the .md ref will be removed by step 1b in _preprocess_markdown.
    def _mermaid_png_fallback(m: re.Match) -> str:
        """If [[media/xxx.md]] or [[xxx.md]] has a media/xxx.png sibling, use PNG."""
        path = m.group(1)   # e.g. "media/excalidraw-xxx.md" or "excalidraw-xxx.md"
        alias = m.group(2) or ""
        # Normalize: strip the .md extension and find the png
        base = re.sub(r'\.md$', '', path, flags=re.IGNORECASE)
        # Also try with media/ prefix
        candidates = [
            md_path.parent / f"{base}.png",                              # relative to handout
            md_path.parent / "media" / f"{Path(base).name}.png",         # media/ dir
        ]
        for cand in candidates:
            if cand.exists():
                if verbose:
                    print(f"  [MERMAID] {path} → {cand.name}", file=sys.stderr)
                return f'![[{cand.relative_to(md_path.parent)}|{alias}]]' if alias else f'![[{cand.relative_to(md_path.parent)}]]'
        # No PNG found — let the pipeline's step 1b warn & remove it
        return m.group(0)
    processed_body = re.sub(
        r'!?\[\[([^\]]+\.md)(?:\|([^\]]*))?\]\]',
        _mermaid_png_fallback,
        processed_body,
    )
    # 1c) Standard markdown pre-processing
    processed_body = _preprocess_markdown(processed_body)

    # Use the body as-is — its first line is already # 第N讲：标题
    full_md = processed_body

    # Write to temp file
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_md = out_dir / f"_{stem}.tmp.md"
    tmp_md.write_text(full_md, encoding="utf-8")

    # ── Sync media directory for image embeds ──
    src_media = HANDOUT_SRC / "media"
    dst_media = out_dir / "media"
    if src_media.exists():
        dst_media.mkdir(parents=True, exist_ok=True)
        for f in src_media.iterdir():
            if f.is_file():
                (dst_media / f.name).write_bytes(f.read_bytes())

    try:
        # ── Stage 2: Pandoc ──
        tmp_docx = out_dir / f"_{stem}.tmp.docx"
        pandoc_convert(tmp_md, tmp_docx, resource_path=out_dir, verbose=verbose)

        # ── Stage 3: Post-process fonts ──
        postprocess(tmp_docx, verbose=verbose)

        # ── Stage 3.5: Post-generation validation ──
        _validate_docx(tmp_docx, md_path, tmp_md, verbose=verbose)

        # ── Rename temp → final ──
        tmp_docx.replace(out_path)

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
) -> None:
    """Validate generated docx for common issues.

    Checks:
    1) docx file size is reasonable (> 10 KB)
    2) Image count in docx matches ![[media/...]] references in source
    3) No raw [[wikilink]] syntax leaked through
    """
    issues: list[str] = []

    # Check 1: file size
    size = docx_path.stat().st_size
    if size < 10_240:
        issues.append(f"docx too small: {size} bytes (< 10 KB)")

    # Check 2: image count match
    source_text = md_source.read_text(encoding="utf-8")
    src_images = set(re.findall(r'!\[\[media/([^\]]+)', source_text))
    # Also match preprocessed markdown image embeds
    prep_text = md_preprocessed.read_text(encoding="utf-8") if md_preprocessed.exists() else ""
    prep_images = set(re.findall(r'!\[.*?\]\(media/([^)]+)\)', prep_text))

    # Count images in docx
    import zipfile
    try:
        with zipfile.ZipFile(docx_path) as z:
            docx_images = [n for n in z.namelist() if n.startswith("word/media/")]
    except Exception:
        docx_images = []

    if src_images and not docx_images:
        issues.append(
            f"Source has {len(src_images)} image(s) but docx has 0 — "
            f"images may not have rendered"
        )
    elif len(docx_images) < len(src_images):
        issues.append(
            f"Image count mismatch: source {len(src_images)}, "
            f"docx {len(docx_images)}"
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

    if issues:
        print(f"  [WARN] Validation: {'; '.join(issues)}", file=sys.stderr)
    elif verbose:
        print(f"  [OK] Validation passed (size={size}B, images={len(docx_images)})")


def main():
    parser = argparse.ArgumentParser(
        description="Batch-convert all student handouts from .md to .docx (v2)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List files that would be processed without converting",
    )
    parser.add_argument(
        "--file", type=str, default=None,
        help="Convert a single file (substring match on filename, e.g. '滴定分析')",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Detailed per-file processing log",
    )
    parser.add_argument(
        "--output-dir", type=str, default=None,
        help="Output directory (default: 06-学生侧材料/讲义)",
    )
    parser.add_argument(
        "--parallel", type=int, nargs="?", const=4, default=None,
        help="Enable parallel processing with N workers (default: 4). "
             "Only effective for batch (non --file) mode.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve() if args.output_dir else HANDOUT_OUT

    # ── Gather input files ──
    all_md = sorted(HANDOUT_SRC.glob(SRC_GLOB))
    if not all_md:
        print(f"ERROR: No files matching '{SRC_GLOB}' found in {HANDOUT_SRC}", file=sys.stderr)
        sys.exit(1)

    # Skip non-handout files
    EXCLUDED_STEMS = {"README"}
    EXCLUDED_PREFIXES = {"讲义升级模式-"}
    all_md = [
        f for f in all_md
        if f.stem not in EXCLUDED_STEMS
        and not any(f.stem.startswith(p) for p in EXCLUDED_PREFIXES)
    ]

    if args.file:
        files = [f for f in all_md if args.file in f.stem]
        if not files:
            print(f"ERROR: No files match --file '{args.file}'", file=sys.stderr)
            print(f"  Available: {[f.stem for f in all_md]}", file=sys.stderr)
            sys.exit(1)
    else:
        files = all_md

    print(f"Found {len(all_md)} handouts in {HANDOUT_SRC}")
    print(f"Selected {len(files)} for processing")
    if args.dry_run:
        print("Dry-run mode — no files will be written:\n")
    else:
        print(f"Output: {output_dir}\n")

    # ── Process ──
    success = 0
    errors = 0

    if args.parallel and not args.file and not args.dry_run:
        # ── Parallel mode ──
        import concurrent.futures
        n_workers = args.parallel if isinstance(args.parallel, int) else 4
        print(f"Parallel mode: {n_workers} workers\n")

        def _convert_one(md_path: Path) -> tuple[str, bool | str]:
            """Wrapper for parallel execution; returns (filename, True|error_msg)."""
            try:
                out = convert_file(md_path, verbose=args.verbose, output_dir=output_dir)
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

            try:
                out = convert_file(md_path, verbose=args.verbose, output_dir=output_dir)
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
    if args.dry_run:
        print(f"Dry-run complete. {len(files)} files listed.")
    else:
        print(f"Done. {success} converted, {errors} errors.")
        if errors:
            sys.exit(1)


if __name__ == "__main__":
    main()
