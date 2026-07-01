#!/usr/bin/env python3
"""
validate_kb.py — 知识库自动化健康检查 (v1)

五支柱框架的支柱一。
在 Agent 开工前/收工后运行，自动捕获 frontmatter 缺失、断链、格式异常，
把人工验证的负担从 Agent 身上剥离。

用法:
    python validate_kb.py --full                    # 全量检查（完整报告）
    python validate_kb.py --quick                   # 快速检查（仅断链+frontmatter）
    python validate_kb.py --changed file1.md file2.md  # 增量检查（仅改动的文件）
    python validate_kb.py --dir 03-知识点/化学原理    # 按目录检查

依赖: PyYAML (pip install pyyaml)
输出: 09-审计报告/auto-validation/YYYY-MM-DD-validation.md
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

# Windows GBK 终端兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() in ("gbk", "gb2312"):
    sys.stderr.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ── Paths ────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent
REPORT_DIR = VAULT_ROOT / "09-审计报告" / "auto-validation"
DEP_MAP_PATH = VAULT_ROOT / "02-数据库" / "dependency-map.json"
METRICS_PATH = VAULT_ROOT / "02-数据库" / "quality-metrics.jsonl"

# ── 受检目录（不检查系统文件/外部资料/归档）───────────────
INCLUDE_DIRS = [
    "01-考纲导航", "02-考纲条目",
    "03-知识点",
    "04-课件", "04-专题与题型", "04-题库",
    "06-学生侧材料",
    "07-资料提炼",
    "11-模板",
    "12-教学洞察",
]
EXCLUDE_PATTERNS = [
    ".obsidian", ".claude", ".git", "__pycache__", "node_modules",
    "09-审计报告", "06-外部资料导入",
    "00-首页",  # 系统入口页不由本脚本检查
    ".chem_media",
]
EXCLUDE_FILE_PREFIXES = ["_pre_"]
EXCLUDE_FILE_NAMES = {"_preprocessed.md", "_test_sup.md", "_test_sup2.md"}
EXCLUDE_PATH_PREFIXES = [
    "06-学生侧材料/讲义/media/",
    "07-资料提炼/网课资料/无机化学-新课-周坤-2020-难度适中/笔记/",
    "07-资料提炼/网课资料/无机化学-新课-周坤-2020-难度适中/学生讲义/",
]
LINK_RESOLUTION_EXTRA_PREFIXES = [
    "06-外部资料导入/",
]

# ── 各 type 的必填 frontmatter 字段 ──────────────────────────
REQUIRED_FIELDS: dict[str, list[str]] = {
    "知识点": ["title", "type", "subject", "status", "updated"],
    "学生讲义": ["title", "type", "serve_rounds", "difficulty_level", "created", "updated"],
    "活跃任务卡": ["title", "type", "task_type", "status", "priority", "area",
                   "source_notes", "related_notes", "evidence", "created", "updated"],
    "模板": ["title", "type", "role", "version", "updated"],
    "考纲条目": ["title", "type", "status", "updated"],
    "专题": ["title", "type", "subject", "status", "updated"],
    "题型": ["title", "type", "subject", "status", "updated"],
    "教学洞察": ["title", "type", "subject", "updated"],
    "备课大纲": ["title", "type", "lesson_round", "created", "updated"],
    "资料提炼": ["title", "type", "source_book", "updated"],
    "新授课": ["title", "type", "round", "created", "updated"],
    "习题课": ["title", "type", "round", "created", "updated"],
    "复习课": ["title", "type", "round", "created", "updated"],
    "学生闪卡": ["title", "type", "subject", "updated"],
    "工具卡": ["title", "type", "subject", "updated"],
}

FIELD_ALIASES_BY_PATH: dict[str, dict[str, list[str]]] = {
    "02-考纲条目/": {
        "status": ["coverage_status"],
    },
    "04-课件/备课大纲/": {
        "lesson_round": ["round"],
    },
    "04-课件/学生讲义/": {
        "serve_rounds": ["round"],
    },
    "07-资料提炼/": {
        "source_book": ["source"],
        "updated": ["extracted_date", "date"],
    },
}

	# ── 允许的 status 枚举值（按 type）─────────────────────────────
ALLOWED_STATUS: dict[str, list[str]] = {
    "知识点": ["骨架", "初稿", "已填充", "stub"],
    "活跃任务卡": ["active", "blocked", "completed", "paused"],
    "考纲条目": ["active", "已完成", "未开始", "未覆盖", "部分填充", "已填充", "已覆盖"],
    "专题": ["骨架", "初稿", "已填充", "草稿", "已审校", "精品"],
    "题型": ["骨架", "初稿", "已填充", "框架"],
    "题目": ["draft", "review", "published", "已入库"],
    "资料提炼": ["草稿", "待审核", "待填充", "已提炼", "已填充"],
    "教学逻辑提炼": ["草稿", "待审核", "已提炼"],
    "备课大纲": ["骨架", "初稿", "已填充", "draft", "review", "published", "草稿", "已审校", "待确认"],
}

# ── 生命周期 stage 枚举 ────────────────────────────────────────
ALLOWED_STAGES = ["draft", "review", "published", "deprecated", "archived"]

# ── stage 门禁：前置条件检查项 ──────────────────────────────────
STAGE_GATES: dict[str, list[str]] = {
    "review": ["前置条件：所有必填 frontmatter 字段必须完整"],
    "published": ["前置条件：无断链 + 必填字段完整 + 有 ≥1 条 evidence"],
    "deprecated": ["前置条件：必须有 replacement 字段指向替代文件"],
    "archived": ["前置条件：已在 deprecated 状态 ≥7 天"],
}


# ══════════════════════════════════════════════════════════════════
#  Frontmatter 解析
# ══════════════════════════════════════════════════════════════════

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter and return (metadata_dict, body_text)."""
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text.strip()
    end = text.find("---", 3)
    if end == -1:
        return {}, text.strip()
    yaml_block = text[3:end].strip()
    body = text[end + 3:].strip()
    try:
        fm = yaml.safe_load(yaml_block)
        return (fm, body) if isinstance(fm, dict) else ({}, body)
    except yaml.YAMLError:
        return {}, body


def parse_frontmatter_from_file(path: Path) -> tuple[dict[str, Any], str]:
    """Read file and parse frontmatter."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}, ""
    return parse_frontmatter(text)


def frontmatter_value_present(value: Any) -> bool:
    """Return True when a frontmatter value should count as populated."""
    return value is not None and value != ""


def frontmatter_field_value(file: Path, fm: dict[str, Any], field: str) -> Any:
    """Read a frontmatter field with path-scoped fallback aliases."""
    value = fm.get(field)
    if frontmatter_value_present(value):
        return value

    rel = file.relative_to(VAULT_ROOT).as_posix()
    for prefix, aliases_by_field in FIELD_ALIASES_BY_PATH.items():
        if not rel.startswith(prefix):
            continue
        for alias in aliases_by_field.get(field, []):
            alias_value = fm.get(alias)
            if frontmatter_value_present(alias_value):
                return alias_value
    return value


def is_excluded_path(rel: str) -> bool:
    """Return True when a relative path should be skipped by validation."""
    normalized = rel.replace("\\", "/")
    if any(normalized.startswith(prefix) for prefix in EXCLUDE_PATH_PREFIXES):
        return True
    parts = [part for part in normalized.split("/") if part]
    if any(part in EXCLUDE_PATTERNS for part in parts):
        return True

    filename = parts[-1] if parts else ""
    if filename.endswith(".excalidraw.md"):
        return True
    if any(filename.startswith(prefix) for prefix in EXCLUDE_FILE_PREFIXES):
        return True
    if filename in EXCLUDE_FILE_NAMES:
        return True
    return False


# ══════════════════════════════════════════════════════════════════
#  检查项
# ══════════════════════════════════════════════════════════════════

class Report:
    """累加检查结果，最终输出 Markdown 报告。"""

    def __init__(self) -> None:
        self.errors: list[tuple[str, str, str]] = []   # (file_path, check_name, detail)
        self.warnings: list[tuple[str, str, str]] = []
        self.infos: list[tuple[str, str, str]] = []
        self.stats: dict[str, int] = {
            "files_checked": 0,
            "files_with_frontmatter": 0,
            "broken_wikilinks": 0,
            "broken_images": 0,
            "orphan_images": 0,
            "orphan_files": 0,
            "stale_files": 0,
            "heading_skips": 0,
        }
        self.all_files: set[Path] = set()
        self.wikilink_map: dict[str, set[str]] = defaultdict(set)  # target → sources

    def error(self, file: str, check: str, detail: str) -> None:
        self.errors.append((file, check, detail))

    def warning(self, file: str, check: str, detail: str) -> None:
        self.warnings.append((file, check, detail))

    def info(self, file: str, check: str, detail: str) -> None:
        self.infos.append((file, check, detail))


def check_frontmatter(file: Path, fm: dict[str, Any], report: Report) -> None:
    """检查 frontmatter 必填字段 + status 枚举值。"""
    rel = file.relative_to(VAULT_ROOT).as_posix()
    doc_type = fm.get("type", "")

    # 必填字段检查
    required = REQUIRED_FIELDS.get(doc_type, ["title", "type", "updated"])
    missing = [f for f in required if not frontmatter_value_present(frontmatter_field_value(file, fm, f))]
    if missing:
        report.error(rel, "frontmatter-缺失", f"缺字段: {', '.join(missing)}")

    # status 枚举值检查
    status = frontmatter_field_value(file, fm, "status")
    if status is not None:
        allowed = ALLOWED_STATUS.get(doc_type)
        if allowed is not None and status not in allowed:
            report.warning(rel, "status-枚举", f"status='{status}' 不在允许列表 {allowed} 中")

    # 日期格式检查
    for date_field in ["created", "updated", "completed"]:
        val = fm.get(date_field)
        if val and isinstance(val, str) and not re.match(r"^\d{4}-\d{2}-\d{2}$", val):
            report.warning(rel, f"日期格式-{date_field}", f"'{val}' 不是 YYYY-MM-DD 格式")


def check_wikilinks(file: Path, body: str, report: Report) -> None:
    """提取 wikilink，标注断链。"""
    rel = file.relative_to(VAULT_ROOT).as_posix()
    links = re.findall(r'\[\[([^\]]+)\]\]', body)
    for link in links:
        target = normalize_wikilink_target(link)
        if not target:
            continue
        # 处理图片嵌入 ![[image.png]] — 在 check_images 中处理
        if target.startswith("media/") or target.startswith("./media/"):
            continue

        # Wikilink 可能不带 .md，也可能带
        target_path = find_wikilink_target(target, VAULT_ROOT)
        if target_path is None:
            report.warning(rel, "断链", f"[[{target}]] → 文件不存在")

        # 记录反向引用（用于孤儿文件检测）
        if target_path:
            normalized = str(target_path.relative_to(VAULT_ROOT).with_suffix("").as_posix())
            report.wikilink_map[normalized].add(rel)
        else:
            # 断链也记录下引用来源，便于追溯
            report.wikilink_map[f"__broken__:{target}"].add(rel)


# ── Wikilink 解析缓存 ──────────────────────────────────────────
_FILENAME_INDEX: dict[str, list[Path]] | None = None
"""惰性构建：basename（无扩展名）→ 匹配的文件列表"""
_LABEL_INDEX: dict[str, list[Path]] | None = None
"""惰性构建：title/aliases（小写）→ 匹配的文件列表"""


def is_link_resolution_extra_path(rel: str) -> bool:
    """Return True when a path should participate in link resolution only."""
    normalized = rel.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in LINK_RESOLUTION_EXTRA_PREFIXES)


def iter_link_resolution_files(vault_root: Path):
    """Yield files that can serve as wikilink targets, including extra source dirs."""
    seen: set[Path] = set()
    for f in vault_root.rglob("*.md"):
        rel = f.relative_to(vault_root).as_posix()
        if is_excluded_path(rel) and not is_link_resolution_extra_path(rel):
            continue
        if f in seen:
            continue
        seen.add(f)
        yield f


def build_filename_index(vault_root: Path) -> dict[str, list[Path]]:
    """遍历 vault 下所有 .md 文件，建立 basename → [Path, ...] 索引。"""
    index: dict[str, list[Path]] = {}
    for f in iter_link_resolution_files(vault_root):
        names = {f.stem.lower()}
        normalized = re.sub(r"^[（(]\s*已压缩\s*[）)]", "", f.stem, count=1).strip().lower()
        if normalized:
            names.add(normalized)
        for name in names:
            index.setdefault(name, []).append(f)
    return index


def build_label_index(vault_root: Path) -> dict[str, list[Path]]:
    """遍历可解析目标文件，建立 title/aliases → [Path, ...] 索引。"""
    index: dict[str, list[Path]] = {}
    for f in iter_link_resolution_files(vault_root):
        fm, _ = parse_frontmatter_from_file(f)
        labels: set[str] = set()

        for field in ("title", "aliases", "syllabus_code"):
            value = fm.get(field)
            if isinstance(value, str) and value.strip():
                labels.add(value.strip().lower())
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and item.strip():
                        labels.add(item.strip().lower())

        for label in labels:
            index.setdefault(label, []).append(f)
    return index


def normalize_wikilink_target(target: str) -> str:
    """Normalize Obsidian wikilinks by stripping aliases and heading/block anchors."""
    target = target.split("|", 1)[0].strip()
    if not target or target.startswith("#"):
        return ""
    if "#" in target:
        target = target.split("#", 1)[0].strip()
    target = target.rstrip("/\\").strip()
    return target


def find_wikilink_target(target: str, vault_root: Path) -> Path | None:
    """
    尝试解析 wikilink 目标文件。多级 fallback：

    1. 精确路径匹配（当前行为）
    2. basename 匹配（处理 [[05-酸碱理论]] → 自动找对应文件）
    3. title/aliases 匹配（通过 frontmatter title/aliases 字段）
    """
    global _FILENAME_INDEX, _LABEL_INDEX

    # ── Level 1: 精确路径匹配 ──────────────────────────────
    candidates = [
        vault_root / target,
        vault_root / f"{target}.md" if not target.endswith(".md") else None,
    ]

    for c in candidates:
        if c and c.exists() and c.is_file():
            return c

    # ── Level 2: basename 模糊匹配 ────────────────────────
    # 惰性构建文件名索引（仅一次）
    if _FILENAME_INDEX is None:
        _FILENAME_INDEX = build_filename_index(vault_root)

    target_basename = target.split("/")[-1].lower()
    matches = _FILENAME_INDEX.get(target_basename, [])

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        # 多文件匹配：优先选 INCLUDE_DIRS 中的，否则选第一个
        for m in matches:
            rel = m.relative_to(vault_root).as_posix()
            if any(rel.startswith(d) or f"/{d}/" in rel for d in INCLUDE_DIRS):
                return m
        return matches[0]

    # ── Level 3: title / aliases 匹配 ───────────────────────
    if _LABEL_INDEX is None:
        _LABEL_INDEX = build_label_index(vault_root)

    label_keys = []
    target_key = target.strip().lower()
    if target_key:
        label_keys.append(target_key)
    if target_basename != target_key:
        label_keys.append(target_basename)

    label_matches: list[Path] = []
    seen: set[Path] = set()
    for key in label_keys:
        for match in _LABEL_INDEX.get(key, []):
            if match not in seen:
                seen.add(match)
                label_matches.append(match)

    if len(label_matches) == 1:
        return label_matches[0]
    elif len(label_matches) > 1:
        for m in label_matches:
            rel = m.relative_to(vault_root).as_posix()
            if any(rel.startswith(d) or f"/{d}/" in rel for d in INCLUDE_DIRS):
                return m
        return label_matches[0]

    return None


def check_images(file: Path, body: str, report: Report) -> None:
    """检查 ![[media/...]] 引用是否存在。"""
    rel = file.relative_to(VAULT_ROOT).as_posix()
    images = re.findall(r'!\[\[([^\]]+)\]\]', body)
    for img in images:
        # 提取实际路径（可能有 | 替代文本）
        img_path = img.split("|")[0].strip()
        candidates = [
            VAULT_ROOT / img_path,
            VAULT_ROOT / "04-课件" / "学生讲义" / img_path,
        ]
        exists = any(c.is_file() for c in candidates)
        if not exists:
            report.warning(rel, "图片缺失", f"![[{img_path}]] → 文件不存在")


def check_headings(file: Path, body: str, report: Report) -> None:
    """检查标题层级是否跳跃（如 # → ### 跳过了 ##）。"""
    rel = file.relative_to(VAULT_ROOT).as_posix()
    lines = body.split("\n")
    prev_level = 0
    for i, line in enumerate(lines):
        m = re.match(r'^(#{1,6})\s', line)
        if m:
            level = len(m.group(1))
            if prev_level > 0 and level > prev_level + 1:
                report.warning(rel, "标题跳跃",
                               f"第 {i+1} 行: {'#' * level} 跳过了 {'#' * (prev_level + 1)} 级")
            prev_level = level


def check_stale(file: Path, fm: dict[str, Any], report: Report, threshold_days: int = 30) -> None:
    """检查 updated 日期是否过于陈旧。"""
    rel = file.relative_to(VAULT_ROOT).as_posix()
    updated = fm.get("updated")
    if updated and isinstance(updated, str):
        try:
            d = datetime.date.fromisoformat(updated)
            delta = datetime.date.today() - d
            if delta.days > threshold_days:
                report.info(rel, "过期内容", f"updated={updated}（{delta.days} 天前）")
                report.stats["stale_files"] += 1
        except ValueError:
            pass


def check_orphans(report: Report) -> None:
    """标记没有入链的受检文件。"""
    # 建立所有受检文件的集合
    all_normalized: set[str] = set()
    for f in report.all_files:
        try:
            normalized = str(f.relative_to(VAULT_ROOT).with_suffix("").as_posix())
            all_normalized.add(normalized)
        except ValueError:
            pass

    # 排除系统入口文件
    excluded_prefixes = ("00-首页", "09-审计报告", ".obsidian", ".claude", "11-模板/scripts")
    for f in all_normalized:
        if any(f.startswith(p) for p in excluded_prefixes):
            continue
        has_incoming = False
        for targets in report.wikilink_map.values():
            if f in targets:
                has_incoming = True
                break
        if not has_incoming:
            report.info(f, "孤儿文件", "无任何入链引用")
            report.stats["orphan_files"] += 1


def check_orphan_images(report: Report) -> None:
    """标记 media/ 目录中未被任何讲义引用的图片。"""
    media_dir = VAULT_ROOT / "04-课件" / "学生讲义" / "media"
    if not media_dir.exists():
        return

    # 搜集所有图片文件名
    all_images: set[str] = set()
    for f in media_dir.iterdir():
        if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
            all_images.add(f.name)

    if not all_images:
        return

    # 从所有受检文件中提取 ![[media/...]] 引用
    referenced: set[str] = set()
    img_ref_pat = re.compile(r'!?\[\[media/([^\]]+)\]\]')
    for f in report.all_files:
        try:
            text = f.read_text(encoding="utf-8")
            for match in img_ref_pat.finditer(text):
                # Handle possible |alt text suffix
                ref = match.group(1).split("|")[0].strip()
                referenced.add(ref)
        except Exception:
            pass

    orphaned = all_images - referenced
    if orphaned:
        # 取前 10 个报告，其余计数
        sample = sorted(orphaned)[:10]
        remainder = len(orphaned) - 10
        msg = f"media/ 中存在 {len(orphaned)} 张未被引用的图片: {', '.join(sample)}"
        if remainder > 0:
            msg += f" ...及其他 {remainder} 张"
        report.warning("media/", "孤儿图片", msg)
        report.stats["orphan_images"] = len(orphaned)


def check_lifecycle(file: Path, fm: dict[str, Any], body: str, report: Report) -> None:
    """检查生命周期 stage 字段有效性与门禁条件。"""
    rel = file.relative_to(VAULT_ROOT).as_posix()
    stage = fm.get("stage")
    if stage is None:
        return  # 未设置 stage 的不检查

    # 1. 枚举值有效性
    if stage not in ALLOWED_STAGES:
        report.warning(rel, "stage-枚举",
                       f"stage='{stage}' 不在允许列表 {ALLOWED_STAGES} 中")
        return

    doc_type = fm.get("type", "")
    required = REQUIRED_FIELDS.get(doc_type, ["title", "type", "updated"])

    # 2. 门禁检查
    if stage == "review":
        # draft→review：所有必填 frontmatter 字段必须存在
        missing = [f for f in required if not frontmatter_value_present(frontmatter_field_value(file, fm, f))]
        if missing:
            report.warning(rel, "stage-门禁",
                           f"stage=review 但缺必填字段: {', '.join(missing)}")
        # 还需要检查是否有证据（body 非空）
        if len(body.strip()) < 50:
            report.warning(rel, "stage-门禁",
                           "stage=review 但正文内容过短（<50 字符），可能未完成")

    elif stage == "published":
        # review→published：无断链 + 内容完整
        missing = [f for f in required if not frontmatter_value_present(frontmatter_field_value(file, fm, f))]
        missing_critical = [f for f in missing if f in ("title", "type")]
        if missing_critical:
            report.warning(rel, "stage-门禁",
                           f"stage=published 但缺关键字段: {', '.join(missing_critical)}")
        elif missing:
            report.info(rel, "stage-建议",
                        f"stage=published 但缺可选字段: {', '.join(missing)}")
        # 检查 evidence 字段（信息性，非阻塞）
        evidence = fm.get("evidence")
        if not evidence:
            report.info(rel, "stage-建议",
                        "stage=published 但未设置 evidence 字段")
        # 检查断链（published 不应有断链）
        links = re.findall(r'\[\[([^\]]+)\]\]', body)
        if links:
            broken = 0
            for link in links:
                target = normalize_wikilink_target(link)
                if not target:
                    continue
                if target.startswith("media/") or target.startswith("./media/"):
                    continue
                if find_wikilink_target(target, VAULT_ROOT) is None:
                    broken += 1
            if broken > 0:
                report.warning(rel, "stage-门禁",
                               f"stage=published 但存在 {broken} 处断链")

    elif stage == "deprecated":
        # published→deprecated：必须有 replacement 字段
        replacement = fm.get("replacement")
        if not replacement:
            report.warning(rel, "stage-门禁",
                           "stage=deprecated 但缺少 replacement 字段（指向替代文件）")

    elif stage == "archived":
        # deprecated→archived：检查文件是否在归档目录
        if "09-审计报告" not in rel and "archived" not in rel:
            report.info(rel, "stage-建议",
                        "stage=archived 但文件未在 09-审计报告/ 归档目录中")


# ══════════════════════════════════════════════════════════════════
#  主扫描
# ══════════════════════════════════════════════════════════════════

def collect_md_files(root: Path, dirs: list[str]) -> list[Path]:
    """收集所有需要检查的 .md 文件。"""
    files: list[Path] = []
    for d in dirs:
        target = root / d
        if not target.exists():
            continue
        for f in sorted(target.rglob("*.md")):
            # 排除 exclude 目录
            rel = f.relative_to(root).as_posix()
            if is_excluded_path(rel):
                continue
            files.append(f)
    return files


def scan_file(file: Path, report: Report, quick: bool = False) -> None:
    """对单个文件执行所有检查。"""
    rel = file.relative_to(VAULT_ROOT).as_posix()
    if is_excluded_path(rel):
        return

    report.stats["files_checked"] += 1
    report.all_files.add(file)

    text = file.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_frontmatter(text)

    if fm:
        report.stats["files_with_frontmatter"] += 1

    # Frontmatter 检查（quick 模式下也做）
    check_frontmatter(file, fm, report)
    # 生命周期 stage 检查
    check_lifecycle(file, fm, body, report)

    if not quick:
        # 断链检查
        check_wikilinks(file, body, report)
        # 图片引用检查
        check_images(file, body, report)
        # 标题层级检查
        check_headings(file, body, report)
        # 过期检查
        check_stale(file, fm, report)
        # 反向索引构建（wikilink_map 已填充）


def build_report_markdown(report: Report, scan_mode: str, target_dirs: list[str] | None) -> str:
    """生成 Markdown 格式报告。"""
    today = datetime.date.today().isoformat()
    lines: list[str] = []
    lines.append(f"# 自动验证报告 · {today}")
    lines.append("")
    lines.append(f"> **扫描模式**: {scan_mode}")
    if target_dirs:
        lines.append(f"> **目标范围**: {', '.join(target_dirs)}")
    lines.append(f"> **受检文件**: {report.stats['files_checked']}")
    lines.append(f"> **检出异常**: {len(report.errors)} error / {len(report.warnings)} warning / {len(report.infos)} info")
    lines.append("")

    # 摘要表
    lines.append("## 摘要")
    lines.append("")
    lines.append("| 指标 | 值 |")
    lines.append("|:---|---:|")
    lines.append(f"| 受检文件 | {report.stats['files_checked']} |")
    lines.append(f"| 有 frontmatter | {report.stats['files_with_frontmatter']} |")
    lines.append(f"| 断链 | {report.stats['broken_wikilinks']} |")
    lines.append(f"| 图片缺失 | {report.stats['broken_images']} |")
    lines.append(f"| 孤儿图片 | {report.stats['orphan_images']} |")
    lines.append(f"| 孤儿文件 | {report.stats['orphan_files']} |")
    lines.append(f"| 过期内容 | {report.stats['stale_files']} |")
    lines.append(f"| 标题跳跃 | {report.stats['heading_skips']} |")
    lines.append("")
    lines.append(f"| Error | {len(report.errors)} |")
    lines.append(f"| Warning | {len(report.warnings)} |")
    lines.append(f"| Info | {len(report.infos)} |")
    lines.append("")

    # Error 明细
    if report.errors:
        lines.append("## 🔴 Errors")
        lines.append("")
        lines.append("| 文件 | 检查项 | 详情 |")
        lines.append("|:---|:---|:---|")
        for f, c, d in report.errors:
            lines.append(f"| {f} | {c} | {d} |")
        lines.append("")

    # Warning 明细
    if report.warnings:
        lines.append("## 🟡 Warnings")
        lines.append("")
        lines.append("| 文件 | 检查项 | 详情 |")
        lines.append("|:---|:---|:---|")
        # 按检查项分组
        by_check: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for f, c, d in report.warnings:
            by_check[c].append((f, d))
        for check_name in ["断链", "图片缺失", "标题跳跃", "status-枚举", "日期格式"]:
            items = by_check.pop(check_name, [])
            if not items:
                continue
            lines.append(f"**{check_name}**（{len(items)} 处）：")
            for f, d in items:
                lines.append(f"  - `{f}` → {d}")
            lines.append("")
        for check_name, items in by_check.items():
            lines.append(f"**{check_name}**（{len(items)} 处）：")
            for f, d in items[:10]:
                lines.append(f"  - `{f}` → {d}")
            if len(items) > 10:
                lines.append(f"  - …还有 {len(items)-10} 处")
            lines.append("")

    # Info 明细（仅显示数量，不列出全部）
    if report.infos:
        lines.append("## ℹ️ Info")
        lines.append("")
        by_info: dict[str, int] = defaultdict(int)
        for _, c, _ in report.infos:
            by_info[c] += 1
        for c, n in sorted(by_info.items()):
            lines.append(f"- **{c}**: {n} 处")
        lines.append("")

    lines.append("---")
    lines.append(f"*自动生成于 {today} · validate_kb.py v1*")
    lines.append("")
    return "\n".join(lines)


def save_metrics(report: Report) -> None:
    """将关键指标追加到质量时序文件。"""
    today = datetime.date.today().isoformat()
    metrics = {
        "date": today,
        "files_checked": report.stats["files_checked"],
        "errors": len(report.errors),
        "warnings": len(report.warnings),
        "infos": len(report.infos),
        "broken_wikilinks": report.stats["broken_wikilinks"],
        "orphan_files": report.stats["orphan_files"],
        "orphan_images": report.stats["orphan_images"],
        "stale_files": report.stats["stale_files"],
    }
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(metrics, ensure_ascii=False) + "\n")


# ══════════════════════════════════════════════════════════════════
#  反向索引构建（Pillar 2 集成）
# ══════════════════════════════════════════════════════════════════

def build_dependency_map(report: Report) -> dict[str, dict[str, list[str]]]:
    """从 wikilink_map 构建完整的依赖图。"""
    # forward map: source → targets
    forward: dict[str, set[str]] = defaultdict(set)
    # 收集所有 wikilink 的 source
    all_sources = set()
    for f in report.all_files:
        try:
            rel = str(f.relative_to(VAULT_ROOT).with_suffix("").as_posix())
            all_sources.add(rel)
        except ValueError:
            pass

    # 从所有文件中提取 wikilink
    for f in report.all_files:
        try:
            rel = str(f.relative_to(VAULT_ROOT).with_suffix("").as_posix())
            text = f.read_text(encoding="utf-8", errors="replace")
            links = re.findall(r'\[\[([^\]]+)\]\]', text)
            for link in links:
                target = link.split("|")[0].strip()
                if target.startswith("media/") or target.startswith("./media/"):
                    continue
                # 标准化
                t = target.replace(".md", "")
                forward[rel].add(t)
        except Exception:
            pass

    # 构建 reverse map
    dep_map: dict[str, dict[str, list[str]]] = {}
    for f in all_sources:
        dep_map[f] = {
            "referenced_by": sorted(report.wikilink_map.get(f, [])),
            "references": sorted(forward.get(f, [])),
        }

    return dep_map


def save_dependency_map(dep_map: dict) -> None:
    """保存依赖图到 JSON。"""
    DEP_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DEP_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(dep_map, f, ensure_ascii=False, indent=2)
    print(f"  📦 依赖图已保存: {DEP_MAP_PATH}")


# ══════════════════════════════════════════════════════════════════
#  CLI
# ══════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="知识库自动健康检查（五支柱·支柱一）",
    )
    parser.add_argument("--full", action="store_true", help="全量检查 + 依赖图构建")
    parser.add_argument("--quick", action="store_true", help="快速检查（仅断链+frontmatter）")
    parser.add_argument("--changed", nargs="*", default=None, help="增量检查：指定改动的文件")
    parser.add_argument("--dir", nargs="*", default=None, help="按目录检查（相对于 vault root）")
    parser.add_argument("--depmap", action="store_true", help="仅构建依赖图（不执行其他检查）")
    args = parser.parse_args()

    # 确定扫描模式
    report = Report()
    scan_mode = "full"
    target_dirs: list[str] | None = None
    quick = False

    if args.depmap:
        # 仅构建依赖图
        scan_mode = "depmap-only"
        print("🔍 构建依赖图...")
        all_files = collect_md_files(VAULT_ROOT, INCLUDE_DIRS)
        print(f"  找到 {len(all_files)} 个 .md 文件")
        for f in all_files:
            report.all_files.add(f)
        dep_map = build_dependency_map(report)
        save_dependency_map(dep_map)
        print("✅ 依赖图构建完成")
        return

    if args.dir:
        target_dirs = args.dir
        scan_mode = f"dir: {', '.join(target_dirs)}"
        files = collect_md_files(VAULT_ROOT, target_dirs)
    elif args.changed is not None:
        scan_mode = f"changed: {len(args.changed)} files"
        files = [Path(f) if Path(f).is_absolute() else VAULT_ROOT / f for f in args.changed]
    elif args.quick:
        scan_mode = "quick"
        quick = True
        files = collect_md_files(VAULT_ROOT, INCLUDE_DIRS)
    else:
        # 默认全量
        scan_mode = "full"
        files = collect_md_files(VAULT_ROOT, INCLUDE_DIRS)

    print(f"🔍 开始验证（{scan_mode}）...")
    print(f"  受检文件: {len(files)}")

    for f in files:
        if not f.exists() or not f.is_file():
            continue
        try:
            scan_file(f, report, quick)
        except Exception as e:
            try:
                rel = f.relative_to(VAULT_ROOT).as_posix()
            except ValueError:
                rel = str(f)
            report.error(rel, "扫描异常", str(e))

    if quick:
        # 快速模式不更新统计
        pass
    else:
        # 统计
        report.stats["broken_wikilinks"] = len([w for w in report.warnings if w[1] == "断链"])
        report.stats["broken_images"] = len([w for w in report.warnings if w[1] == "图片缺失"])

    # 孤儿文件检测（全量模式）
    if not quick and not args.changed:
        check_orphans(report)

    # 孤儿图片检测（全量模式）
    if not quick and not args.changed:
        check_orphan_images(report)

    # 生成报告
    md = build_report_markdown(report, scan_mode, target_dirs)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    report_path = REPORT_DIR / f"{today}-validation.md"
    report_path.write_text(md, encoding="utf-8")

    # 保存指标
    save_metrics(report)

    # 如果是全量模式，构建依赖图
    if args.full:
        print("  🔗 构建依赖图...")
        dep_map = build_dependency_map(report)
        save_dependency_map(dep_map)

    # 输出摘要
    print(f"\n📊 结果:", file=sys.stderr)
    print(f"  ✅ 受检: {report.stats['files_checked']} 文件", file=sys.stderr)
    print(f"  🔴 Error: {len(report.errors)}", file=sys.stderr)
    print(f"  🟡 Warning: {len(report.warnings)}", file=sys.stderr)
    print(f"  ℹ️  Info: {len(report.infos)}", file=sys.stderr)
    print(f"  📄 报告: {report_path}", file=sys.stderr)
    if args.full:
        depmap_path = DEP_MAP_PATH
        print(f"  📦 依赖图: {depmap_path}", file=sys.stderr)

    # 非零退出码表示有问题
    if report.errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
