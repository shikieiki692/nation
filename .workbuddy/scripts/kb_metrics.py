# -*- coding: utf-8 -*-
"""生成知识库唯一指标事实源。

只读扫描，不修改 vault。口径与现有题库脚本保持一致：
- md 数包含题目、答案、索引和系统文件；
- 题数只统计 type 为 题目/真题 且 status 不是 deprecated 的文件；
- 链接统计排除审计报告、代码块、图片嵌入和已归档目录。
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[2]
QB_ROOTS = [ROOT / '04-题库', ROOT / '05-真题库']
QB_TYPES = {'题目', '真题'}
SKIP_SOURCE_DIRS = {'_归档', '归档', '媒体仓库', '06-外部资料导入', '09-审计报告', '11-模板', '.workbuddy'}
INDEX_SKIP_DIRS = {'.git', '.obsidian', 'node_modules', '媒体仓库'}
ARTIFACT_SKIP_DIRS = {'_归档', '归档', '媒体仓库', '06-外部资料导入', '.workbuddy'}


def frontmatter(path):
    try:
        lines = path.read_text(encoding='utf-8', errors='replace').splitlines()
    except OSError:
        return {}
    if not lines or lines[0].strip() != '---':
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == '---':
            break
        if line and not line[:1].isspace() and ':' in line:
            key, _, value = line.partition(':')
            fields[key.strip()] = value.strip()
    return fields


def is_deprecated(fields):
    # 兼容两种废弃标记：status: deprecated 与 deprecated: true（知识点页多用后者）
    if fields.get('status', '').strip().lower().startswith('deprecated'):
        return True
    return fields.get('deprecated', '').strip().lower() == 'true'


PENDING_DIR = '_待人工复核-空壳与重复卡'


def md_files(root):
    if not root.exists():
        return []
    return [p for p in root.rglob('*.md') if not any(part in {'_归档', '归档'} for part in p.relative_to(ROOT).parts)]


def link_targets(text):
    in_code = False
    pos = 0
    while True:
        fence = text.find('```', pos)
        line_start = text.rfind('\n', 0, fence) + 1 if fence >= 0 else len(text)
        if fence >= 0 and text[line_start:fence].strip() == '':
            in_code = not in_code
            pos = fence + 3
            continue
        start = text.find('[[', pos)
        if start < 0:
            return
        if in_code or (start > 0 and text[start - 1] == '!'):
            pos = start + 2
            continue
        end = text.find(']]', start + 2)
        if end < 0:
            return
        raw = text[start + 2:end]
        target = raw.split('|', 1)[0].split('#', 1)[0].strip()
        if target:
            yield target
        pos = end + 2


def link_metrics():
    rel_paths = set()
    stems = set()
    files = []
    for p in ROOT.rglob('*.md'):
        rel_parts = p.relative_to(ROOT).parts
        if any(part in INDEX_SKIP_DIRS for part in rel_parts):
            continue
        rel = p.relative_to(ROOT).as_posix()
        rel_paths.add(rel)
        rel_paths.add(rel[:-3] if rel.endswith('.md') else rel)
        stems.add(p.stem)
        if not any(part in SKIP_SOURCE_DIRS for part in rel_parts):
            files.append(p)
    total = resolved = 0
    broken = []
    for p in files:
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        for target in link_targets(text):
            total += 1
            clean = target.strip().strip('<>')
            if clean in rel_paths or clean + '.md' in rel_paths or Path(clean).name in stems:
                resolved += 1
            else:
                broken.append({'source': p.relative_to(ROOT).as_posix(), 'target': target})
    return {'total': total, 'resolved': resolved, 'broken_candidates': len(broken), 'sample': broken[:20], 'audit_self_references_excluded': True, 'code_blocks_and_images_excluded': True}


def question_metrics():
    rows = []
    for root in QB_ROOTS:
        for p in md_files(root):
            fields = frontmatter(p)
            if fields.get('type', '').strip() not in QB_TYPES:
                continue
            rows.append((p, fields))
    by_type = {}
    for qtype in sorted(QB_TYPES):
        subset = [f for _, f in rows if f.get('type', '').strip() == qtype]
        by_type[qtype] = {
            'total': len(subset),
            'active': sum(not is_deprecated(f) for f in subset),
            'deprecated': sum(is_deprecated(f) for f in subset),
        }
    return {
        'md_total': sum(len(md_files(root)) for root in QB_ROOTS),
        'question_like_total': len(rows),
        'question_like_active': sum(not is_deprecated(f) for _, f in rows),
        'question_like_deprecated': sum(is_deprecated(f) for _, f in rows),
        'by_type': by_type,
    }


def pending_review_metrics():
    """隔离区统计：_待人工复核-空壳与重复卡 下的卡（多为重复副本，虽标已填充但不应计入可组卷池）"""
    n = 0
    for root in QB_ROOTS:
        for p in md_files(root):
            if PENDING_DIR in p.parts:
                n += 1
    return {'pending_review_cards': n, 'pending_review_dir': PENDING_DIR}


def artifact_metrics():
    handouts = [p for p in (ROOT / '04-课件' / '学生讲义').rglob('*.md') if not any(part in {'_归档', '归档'} for part in p.relative_to(ROOT).parts)] if (ROOT / '04-课件' / '学生讲义').exists() else []
    docx = [p for p in ROOT.rglob('*.docx') if not any(part in ARTIFACT_SKIP_DIRS for part in p.relative_to(ROOT).parts)]
    return {'student_handout_md': len(handouts), 'docx_total': len(docx)}


def main():
    metrics = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'root': str(ROOT),
        'question_bank': question_metrics(),
        'links': link_metrics(),
        'pending_review': pending_review_metrics(),
        'artifacts': artifact_metrics(),
        'definitions': {
            'active_question': 'type in {题目, 真题} and status != deprecated',
            'link_scope': 'exclude audit reports, code blocks, image embeds, archives and external imports',
        },
    }
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
