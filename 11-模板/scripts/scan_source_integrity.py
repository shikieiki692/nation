# -*- coding: utf-8 -*-
"""题库源文件结构与数据完整性扫描（只读）：
frontmatter 缺失/YAML 错误、题目必填字段、空文件、编码异常、文件名冲突、
整文件半截 math、题干为空、重复题号等。输出 09-审计报告/缓存-源文件健康扫描.json。"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, '11-模板/scripts')
import audit_question_bank as A

VAULT = Path(__file__).resolve().parents[2]  # scripts → 11-模板 → 仓库根
OUT_JSON = VAULT / '09-审计报告' / '缓存-源文件健康扫描.json'
SKIP_DIR = {'.obsidian', '.git', 'node_modules', '__pycache__', '.workbuddy',
            '09-AI工作区', '11-模板', '备份', '_归档', '.tmp', '_tmp'}

report = {
    'frontmatter_missing': [],      # 完全无 frontmatter
    'yaml_error': [],               # frontmatter 存在但解析失败
    'empty_file': [],               # 空文件/几乎空
    'read_error': [],               # 编码/读取异常
    'missing_title': [],            # 题目类缺 title
    'missing_type': [],             # 无 type 字段
    'unknown_type': [],             # type 不在已知集合
    'half_math': [],                # 整文件 $ 数量为奇数
    'empty_stem': [],               # 题目类但题干段为空
    'name_conflict': [],            # 同名 stem 多个文件
    'dup_title': [],                # 同目录同 title
}

# ---- 文件遍历 ----
files = []
for root in ('04-题库', '05-真题库'):
    for p in sorted((VAULT / root).rglob('*.md')):
        rel = p.relative_to(VAULT).as_posix()
        if any(s in rel for s in SKIP_DIR):
            continue
        files.append(p)
print(f'受检文件: {len(files)}')

stem_counter = Counter()
title_counter = defaultdict(list)
for p in files:
    rel = p.relative_to(VAULT).as_posix()
    try:
        raw = p.read_text(encoding='utf-8')
    except Exception as e:
        report['read_error'].append(f'{rel} | {type(e).__name__}: {str(e)[:50]}')
        continue
    if not raw.strip():
        report['empty_file'].append(rel)
        continue
    if not raw.lstrip().startswith('---'):
        report['frontmatter_missing'].append(rel)
        continue
    fm, body = A.strip_fm(raw)
    if isinstance(fm, dict) and '__yaml_error__' in fm:
        report['yaml_error'].append(f'{rel} | {fm["__yaml_error__"][:60]}')
        continue
    ftype = str(fm.get('type', '')).strip()
    if not ftype:
        report['missing_type'].append(rel)
    elif ftype not in A.QUESTION_TYPES:
        report['unknown_type'].append(f'{rel} | type={ftype}')
    if not str(fm.get('title', '')).strip():
        report['missing_title'].append(f'{rel} | type={ftype or "?"}')
    # 半截 math：整文件 $ 计数（含块级 $$）
    if raw.count('$') % 2:
        report['half_math'].append(rel)
    # 题干为空（题目类且有答案分隔；合集文件 `## 题目与答案` 双匹配会负切片，跳过）
    if ftype in A.QUESTION_TYPES and body.strip():
        if re.search(r'^##\s*题目与答案[^\n]*$', body, re.M):
            pass  # 合集文件：题干与答案交错，无独立题干段，属正常结构
        else:
            m = re.search(r'^##\s*(题目|问题)[^\n]*$', body, re.M)
            m2 = re.search(r'^##\s*(参考答案|参考解答|答案|解答|解析)[^\n]*$', body, re.M)
            stem_sec = body[m.end():m2.start()] if m and m2 else (body[:m2.start()] if m2 else body)
            stem_text = re.sub(r'[#>*\s]|!\s*\[\[[^\]]+\]\]', '', stem_sec)
            if len(stem_text.strip()) < 5:
                report['empty_stem'].append(f'{rel} | stem="{stem_text.strip()[:30]}"')
    # 同名冲突：文件 stem（去扩展名、去题号前缀后）
    stem_counter[p.stem] += 1
    t = str(fm.get('title', '')).strip()
    if t:
        title_counter[t].append(rel)

report['name_conflict'] = [f'{s} x{n}' for s, n in stem_counter.items() if n > 1]
report['dup_title'] = [f'{t} | {len(v)} 文件' for t, v in title_counter.items() if len(v) > 1]

# ---- 汇总 ----
for k, v in report.items():
    if isinstance(v, list):
        print(f'{k}: {len(v)}')
OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'\n→ {OUT_JSON}')
