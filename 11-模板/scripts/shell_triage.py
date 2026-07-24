# -*- coding: utf-8 -*-
"""薄壳 KP 体检脚本（审计 P1-8）
遍历 03-知识点/**/*.md，提取 frontmatter 关键字段 + 反向引用计数，
输出全量 CSV 到 02-数据库/shell_triage_raw.csv，stdout 打印非已填充子集概要。
"""
import os, re, csv, json, io, sys

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
KP_ROOT = os.path.join(VAULT, '03-知识点')
REV_INDEX = os.path.join(VAULT, '.kb', 'state', 'reverse_index.json')
OUT_CSV = os.path.join(VAULT, '02-数据库', 'shell_triage_raw.csv')

FIELD_RE = re.compile(r'^([A-Za-z_]+):[ \t]*(.*)$')

def read_text(path):
    with open(path, 'rb') as f:
        raw = f.read()
    return raw.decode('utf-8-sig')

def split_frontmatter(text):
    """返回 (fm_lines, body_lines)。无 frontmatter 时 fm_lines=[]"""
    lines = text.split('\n')
    if not lines or lines[0].strip() != '---':
        return [], lines
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            return lines[1:i], lines[i+1:]
    return [], lines

def parse_fm(fm_lines):
    """简易 YAML 子集解析：标量字段 + 列表字段（内联或多行）。"""
    fields = {}   # name -> {'value': str, 'items': [str]}
    order = []
    for ln in fm_lines:
        m = FIELD_RE.match(ln)
        if m:
            name, val = m.group(1), m.group(2).strip()
            fields[name] = {'value': val, 'items': []}
            order.append(name)
        elif re.match(r'^\s+-\s', ln) and order:
            item = re.sub(r'^\s+-\s?', '', ln).strip()
            fields[order[-1]]['items'].append(item)
    return fields

def inline_list_items(val):
    """解析 [a, b] 形式的内联列表"""
    val = val.strip()
    if val.startswith('[') and val.endswith(']'):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [x.strip().strip('"').strip("'") for x in inner.split(',') if x.strip()]
    return None

def list_count(f):
    if f is None:
        return 0, []
    if f['items']:
        return len(f['items']), f['items']
    il = inline_list_items(f['value'])
    if il is not None:
        return len(il), il
    if f['value']:
        return 1, [f['value']]
    return 0, []

def main():
    # 反向引用索引：键为 wikilink 目标（裸名 或 相对路径无后缀）
    with open(REV_INDEX, encoding='utf-8') as f:
        rev = json.load(f)['index']

    rows = []
    for dirpath, _dirs, files in os.walk(KP_ROOT):
        for fn in sorted(files):
            if not fn.endswith('.md'):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, VAULT).replace(os.sep, '/')
            parts = rel.split('/')
            module = parts[1] if len(parts) > 2 else '(根目录)'
            try:
                text = read_text(path)
            except Exception as e:
                rows.append({'relpath': rel, 'module': module, 'error': str(e)})
                continue
            fm_lines, body_lines = split_frontmatter(text)
            fm = parse_fm(fm_lines)

            status = fm.get('status', {}).get('value', '').strip() if fm.get('status') else ''
            has_status = '是' if status else '否'
            importance = fm.get('importance', {}).get('value', '').strip() if fm.get('importance') else ''
            difficulty = fm.get('difficulty', {}).get('value', '').strip() if fm.get('difficulty') else ''

            n_syl, syl_items = list_count(fm.get('syllabus_code'))
            n_ext, _ = list_count(fm.get('source_extracts'))
            n_alias, alias_items = list_count(fm.get('aliases'))

            body = [l for l in body_lines]
            n_body = len(body)
            body_text = '\n'.join(body)
            has_teaching = '是' if ('教学视角' in body_text) else '否'

            # 被引用计数：裸文件名 + 相对路径（无 .md）+ aliases
            stem = fn[:-3]
            rel_noext = rel[:-3]
            targets = {stem, rel_noext}
            for a in alias_items:
                a = a.strip().strip('"').strip("'").strip('[]')
                if a:
                    targets.add(a)
            refs = sum(len(rev.get(t, [])) for t in targets)

            rows.append({
                'relpath': rel,
                'module': module,
                'status': status or '(缺失)',
                'has_status': has_status,
                'importance': importance,
                'difficulty': difficulty,
                'syllabus_code': '; '.join(s.strip('"').strip("'") for s in syl_items),
                'n_source_extracts': n_ext,
                'body_lines': n_body,
                'has_teaching_section': has_teaching,
                'n_aliases': n_alias,
                'inbound_refs': refs,
            })

    fields = ['relpath', 'module', 'status', 'has_status', 'importance',
              'difficulty', 'syllabus_code', 'n_source_extracts',
              'body_lines', 'has_teaching_section', 'n_aliases', 'inbound_refs']
    with open(OUT_CSV, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow(r)

    total = len(rows)
    print(f'全量 {total} 行 -> {OUT_CSV}')
    print()
    print('=== 非已填充子集 ===')
    sub = [r for r in rows if r.get('status') != '已填充']
    print(f'共 {len(sub)} 个')
    for r in sorted(sub, key=lambda x: x['relpath']):
        print('{relpath} | {status} | imp={importance} | syl=[{syllabus_code}] | ext={n_source_extracts} | refs={inbound_refs} | lines={body_lines} | 教学视角={has_teaching_section}'.format(**r))

if __name__ == '__main__':
    main()
