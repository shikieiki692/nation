from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from handout_audit_utils import (
    Finding,
    HANDOUT_MEDIA_ROOT,
    VAULT_ROOT,
    find_markdown_image_refs,
    load_frontmatter,
    read_text,
    resolve_handout_image_ref,
    strip_markdown,
)


REQUIRED_FRONTMATTER_FIELDS = {
    "title",
    "type",
    "chapter",
    "difficulty_level",
    "created",
    "updated",
    "image_count",
    "template_version",
}
ALLOWED_SIMPLE_UNICODE = {"mₛ", "mₗ", "dₓᵧ"}
DISCOURAGED_COMPLEX_UNICODE = {"dₓ₂", "dᵧ₂", "d₂²", "dₓ²₋ᵧ²"}
ALLOWED_META_LABELS = {
    "对应专题",
    "对应备课大纲",
    "建议使用方式",
    "前置要求",
    "深度边界",
    "课时",
    "版本说明",
    "记号约定",
}


@dataclass(slots=True)
class CaptionInfo:
    number: int
    line: int
    text: str


def find_line_numbers(text: str, pattern: str) -> list[tuple[int, str]]:
    regex = re.compile(pattern)
    results: list[tuple[int, str]] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if regex.search(line):
            results.append((idx, line))
    return results


def parse_captions(text: str) -> list[CaptionInfo]:
    captions: list[CaptionInfo] = []
    pattern = re.compile(r"^\*图\s*(\d+)\s+(.+)\*$")
    for idx, line in enumerate(text.splitlines(), start=1):
        match = pattern.match(line.strip())
        if match:
            captions.append(
                CaptionInfo(
                    number=int(match.group(1)),
                    line=idx,
                    text=strip_markdown(match.group(2)),
                )
            )
    return captions


def extract_label_from_blockquote(line: str) -> str | None:
    match = re.match(r"^>\s+\*\*([^*]+)\*\*[：:]", line.strip())
    return match.group(1).strip() if match else None


def run_preflight(markdown_path: Path) -> list[Finding]:
    text = read_text(markdown_path)
    findings: list[Finding] = []
    frontmatter = load_frontmatter(text)

    if not frontmatter:
        findings.append(Finding("error", "MISSING_FRONTMATTER", "缺少 YAML frontmatter"))
    else:
        for field in sorted(REQUIRED_FRONTMATTER_FIELDS):
            if field not in frontmatter:
                findings.append(Finding("error", "FRONTMATTER_FIELD_MISSING", f"缺少 frontmatter 字段：{field}"))

        difficulty_level = frontmatter.get("difficulty_level", "")
        if "⭐" in difficulty_level or "★" in difficulty_level:
            findings.append(Finding("error", "DIFFICULTY_STARS", "difficulty_level 仍使用星级标记"))

    for line_no, line in find_line_numbers(text, r"[⭐★]"):
        findings.append(Finding("error", "STAR_MARKER", "发现星级难度标记残留", line=line_no, context=line.strip()))

    for line_no, line in find_line_numbers(text, r"<center>|</center>"):
        findings.append(Finding("error", "HTML_CENTER_CAPTION", "仍存在 <center> 图注 legacy 写法", line=line_no, context=line.strip()))

    image_refs = find_markdown_image_refs(text)
    # Count unique image targets (not total occurrences) to match semantic meaning of image_count
    unique_image_targets = len({ref.target for ref in image_refs})
    declared_count = frontmatter.get("image_count") if frontmatter else None
    if declared_count is not None:
        try:
            expected_count = int(declared_count)
            if expected_count != unique_image_targets:
                findings.append(
                    Finding(
                        "error",
                        "IMAGE_COUNT_MISMATCH",
                        f"frontmatter image_count={expected_count}，实际唯一图片数={unique_image_targets}（总引用={len(image_refs)}）",
                    )
                )
        except ValueError:
            findings.append(Finding("error", "IMAGE_COUNT_INVALID", f"image_count 不是整数：{declared_count}"))

    for ref in image_refs:
        norm_target = ref.target.replace("\\", "/")
        if "/" not in norm_target:
            findings.append(
                Finding(
                    "error",
                    "BARE_IMAGE_REF",
                    f"图片必须显式写成 ![[media/...]]，不再接受裸文件名：{ref.target}",
                    line=ref.line,
                )
            )
            continue

        resolved, label = resolve_handout_image_ref(markdown_path, ref.target)
        if resolved is None:
            findings.append(
                Finding(
                    "error",
                    "IMAGE_MISSING",
                    f"图片引用找不到文件：{ref.target}",
                    line=ref.line,
                )
            )
            continue

        if norm_target.startswith("mineru/"):
            findings.append(
                Finding(
                    "error",
                    "DIRECT_MINERU_IMAGE",
                    f"图片直接引用了 mineru 来源：{ref.target}",
                    line=ref.line,
                )
            )
        elif norm_target.startswith("06-外部资料导入/"):
            findings.append(
                Finding(
                    "warning",
                    "DIRECT_EXTERNAL_IMAGE",
                    f"图片直接引用了外部资料路径：{ref.target}",
                    line=ref.line,
                )
            )

        if "Pasted image" in Path(norm_target).name:
            findings.append(
                Finding(
                    "warning",
                    "PASTED_IMAGE_NAME",
                    f"图片仍使用 Pasted image 临时文件名：{ref.target}",
                    line=ref.line,
                )
            )

        if not norm_target.startswith("media/"):
            findings.append(
                Finding(
                    "warning",
                    "NON_MEDIA_IMAGE_REF",
                    f"图片未使用 media/ 路径：{ref.target}（解析方式：{label}）",
                    line=ref.line,
                )
            )

    captions = parse_captions(text)
    caption_numbers = [caption.number for caption in captions]
    if captions:
        expected_numbers = list(range(1, len(captions) + 1))
        if caption_numbers != expected_numbers:
            findings.append(
                Finding(
                    "warning",
                    "CAPTION_SEQUENCE",
                    f"图注编号不连续：{caption_numbers}",
                )
            )
        for caption in captions:
            visible_len = len(caption.text.replace(" ", ""))
            if visible_len > 30:
                findings.append(
                    Finding(
                        "warning",
                        "LONG_CAPTION",
                        f"图注偏长（{visible_len} 字符）：图 {caption.number}",
                        line=caption.line,
                        context=caption.text,
                    )
                )

    image_lines = {ref.line for ref in image_refs}
    caption_lines = {caption.line for caption in captions}
    lines = text.splitlines()
    for ref in image_refs:
        lookahead = [line.strip() for line in lines[ref.line : min(ref.line + 3, len(lines))] if line.strip()]
        if not any(line.startswith("*图 ") and line.endswith("*") for line in lookahead):
            findings.append(
                Finding(
                    "warning",
                    "CAPTION_MISSING_NEAR_IMAGE",
                    f"图片附近未发现标准图注：{ref.target}",
                    line=ref.line,
                )
            )

    # Only match emoji as the callout marker (after > and whitespace only),
    # not emoji appearing later in the content text (e.g. after **bold**：)
    emoji_callout_lines = find_line_numbers(text, r"^>\s+[🧠⚠️💡📌🗣️📝🧪✏️]")
    for line_no, line in emoji_callout_lines:
        findings.append(
            Finding(
                "warning",
                "EMOJI_CALLOUT",
                "发现旧式 emoji callout",
                line=line_no,
                context=line.strip(),
            )
        )

    for idx, line in enumerate(lines, start=1):
        label = extract_label_from_blockquote(line)
        if label and label in ALLOWED_META_LABELS:
            continue
        # Only flag blockquotes that look like they're TRYING to use the > **标签**： format
        # but have a formatting issue. Valid callouts like > **text content** are fine.
        stripped = line.strip()
        if stripped.startswith("> **") and label is None:
            # Check if it has a colon pattern that looks like a malformed label
            if re.match(r"^>\s+\*\*[^*]{1,10}[：:]\s*\*\*", stripped):
                findings.append(
                    Finding(
                        "warning",
                        "BLOCKQUOTE_LABEL_FORMAT",
                        "blockquote 标签格式异常，未匹配到 > **标签**：内容",
                        line=idx,
                        context=stripped,
                    )
                )

    for token in DISCOURAGED_COMPLEX_UNICODE:
        for line_no, line in find_line_numbers(text, re.escape(token)):
            findings.append(
                Finding(
                    "warning",
                    "COMPLEX_UNICODE_SUBSCRIPT",
                    f"发现建议改回数学模式的复杂 Unicode 记号：{token}",
                    line=line_no,
                    context=line.strip(),
                )
            )

    if not image_refs and captions:
        findings.append(Finding("warning", "CAPTION_WITHOUT_IMAGES", "发现图注但未检测到图片引用"))

    # ── 新增：化学符号与格式检查 ──
    # e_g / t_2g 裸下划线格式（应为 $e_g$ LaTeX 下标）
    for line_no, line in find_line_numbers(text, r'(?<!\$)(?<!\w)[et]_(?:2g|g)\b(?!\$)'):
        # 排除已在 $...$ 中的
        cleaned = re.sub(r'\$[^$]+\$', '', line)
        if re.search(r'(?<!\w)[et]_(?:2g|g)\b', cleaned):
            findings.append(Finding("error", "BARE_SUBSCRIPT_FORMAT",
                f"发现裸下划线格式（应为 $e_g$ LaTeX 下标）", line=line_no, context=line.strip()[:80]))

    # 中文下标：T_转 等（_ 后跟中文字符）——排除 frontmatter（: 开头的行）和 LaTeX 数学
    for line_no, line in find_line_numbers(text, r'[A-Za-z]_[一-鿿]'):
        if line.strip().startswith('---') or ':' in line.strip()[:3]:
            continue  # 跳过 frontmatter 和 YAML 字段
        cleaned = re.sub(r'\$[^$]+\$', '', line)  # 去除 math mode
        match = re.search(r'([A-Za-z])_([一-鿿])', cleaned)
        if match:
            findings.append(Finding("error", "CHINESE_SUBSCRIPT",
                f"发现中文下标 '{match.group(0)}'（应为 $..._{{...}}$ LaTeX）",
                line=line_no, context=line.strip()[:80]))

    # H1 标题包含"超级充实版"（会进页眉）
    for line_no, line in find_line_numbers(text, r'^# .+超级充实版'):
        findings.append(Finding("error", "H1_SUPER_EDITION",
            "H1 标题包含'超级充实版'（会出现在 PDF 页眉中）",
            line=line_no, context=line.strip()[:80]))

    return findings


def print_summary(markdown_path: Path, findings: list[Finding]) -> int:
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]
    infos = [item for item in findings if item.severity == "info"]

    print(f"[preflight] file={markdown_path}")
    print(f"[preflight] errors={len(errors)} warnings={len(warnings)} info={len(infos)}")

    for bucket_name, bucket in [("ERROR", errors), ("WARN", warnings), ("INFO", infos)]:
        for finding in bucket:
            prefix = f"{bucket_name} {finding.code}"
            if finding.line:
                prefix += f" line={finding.line}"
            print(f"{prefix}: {finding.message}")
            if finding.context:
                print(f"    {finding.context}")
    return 1 if errors else 0


def main() -> int:
    # Fix GBK encoding crash on Windows when output contains Unicode (e.g. ⁺)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="学生讲义 PDF 预检器")
    parser.add_argument("markdown", nargs="+", help="待检查的 Markdown 文件（相对 vault 根目录或绝对路径）")
    args = parser.parse_args()

    exit_code = 0
    for raw_path in args.markdown:
        markdown_path = Path(raw_path)
        if not markdown_path.is_absolute():
            markdown_path = VAULT_ROOT / raw_path
        findings = run_preflight(markdown_path)
        exit_code = max(exit_code, print_summary(markdown_path, findings))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
