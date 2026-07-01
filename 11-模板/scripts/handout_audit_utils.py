from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


VAULT_ROOT = Path(__file__).resolve().parents[2]
HANDOUT_ROOT = VAULT_ROOT / "04-课件" / "学生讲义"
HANDOUT_MEDIA_ROOT = HANDOUT_ROOT / "media"
IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".bmp",
}


@dataclass(slots=True)
class Finding:
    severity: str
    code: str
    message: str
    line: int | None = None
    context: str | None = None


@dataclass(slots=True)
class ImageRef:
    raw: str
    target: str
    width: str | None
    line: int


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_lines(text: str) -> Iterable[tuple[int, str]]:
    for idx, line in enumerate(text.splitlines(), start=1):
        yield idx, line


def normalize_relpath(raw_path: str) -> str:
    return raw_path.strip().replace("\\", "/").strip("/")


def is_image_path(raw_path: str) -> bool:
    return Path(raw_path).suffix.lower() in IMAGE_EXTENSIONS


def strip_markdown(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text.strip()


def find_markdown_image_refs(text: str) -> list[ImageRef]:
    refs: list[ImageRef] = []
    pattern = re.compile(r"!\[\[([^\]]+)\]\]")
    for line_no, line in iter_lines(text):
        for match in pattern.finditer(line):
            raw = match.group(1).strip()
            target, width = split_obsidian_target(raw)
            if is_image_path(target):
                refs.append(ImageRef(raw=raw, target=target, width=width, line=line_no))
    return refs


def split_obsidian_target(raw: str) -> tuple[str, str | None]:
    if "|" not in raw:
        return raw.strip(), None
    target, width = raw.split("|", 1)
    return target.strip(), width.strip() or None


def find_inline_code_image_paths(text: str) -> list[tuple[int, str]]:
    results: list[tuple[int, str]] = []
    pattern = re.compile(r"`([^`\n]+\.(?:png|jpg|jpeg|gif|webp|svg|bmp))`", re.IGNORECASE)
    for line_no, line in iter_lines(text):
        for match in pattern.finditer(line):
            results.append((line_no, normalize_relpath(match.group(1))))
    return results


def resolve_vault_path(raw_path: str) -> Path:
    rel = normalize_relpath(raw_path)
    return VAULT_ROOT / rel


def resolve_handout_image_ref(markdown_path: Path, target: str) -> tuple[Path | None, str]:
    rel = normalize_relpath(target)
    note_dir = markdown_path.parent

    candidates: list[tuple[Path, str]] = []
    if "/" in rel:
        candidates.append((note_dir / rel, "note-relative"))
        candidates.append((VAULT_ROOT / rel, "vault-relative"))
        if rel.startswith("media/"):
            candidates.append((HANDOUT_ROOT / rel, "handout-media"))

    seen: set[Path] = set()
    for candidate, label in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            return candidate, label
    return None, "missing"


def detect_image_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".svg":
        return "svg"

    try:
        header = path.read_bytes()[:32]
    except OSError:
        return "unreadable"

    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if header.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if header.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if header.startswith(b"BM"):
        return "bmp"
    if len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "webp"
    if header.lstrip().startswith(b"<svg") or b"<svg" in header.lower():
        return "svg"
    return suffix.lstrip(".") or "unknown"


def file_kind_matches_extension(path: Path) -> bool:
    suffix = path.suffix.lower().lstrip(".")
    actual = detect_image_kind(path)
    if suffix == "jpg":
        suffix = "jpeg"
    return suffix == actual


def load_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def find_heading_before(lines: list[str], line_no: int) -> str | None:
    for idx in range(line_no - 1, -1, -1):
        line = lines[idx].strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return None
