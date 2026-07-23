# build_link_map.py — 全库 wikilink 断链映射表生成器 v2
# 用法: python build_link_map.py [vault_root]
# 产出（02-数据库/）: link_map_report.json / link_map_auto.csv / link_map_ambiguous.csv /
#   link_map_nomatch.csv / link_map_rewrite_plan.json / link_map_substring_suggest.csv
# 口径: 与 Obsidian 一致——链接按 basename（去 .md）全库解析，或按相对路径解析；|别名 与 #锚点 剥离。
import os, re, csv, json, sys, unicodedata
from collections import defaultdict

VAULT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT_DIR = os.path.join(VAULT, '02-数据库')
EXCLUDE_TOP = {'.git', '.obsidian', '.trash', '.claude', '.kb', '.agents', '.claudian', 'kb-vault-mcp', 'pptx-workspace'}
ASSET_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.docx', '.doc', '.pptx', '.xlsx', '.mp4', '.mp3', '.wav', '.tex', '.zip', '.json', '.csv', '.ps1', '.py', '.js', '.ts', '.mjs', '.html', '.css', '.excalidraw', '.base'}
# 改写计划的排除规则：模板/skills 里的占位示例链接不该"修复"
REWRITE_EXCLUDE_SRC = ('skills/', '11-模板/')
# 纯 ASCII 名之间的匹配要求 NFKC 后大小写完全一致（防止 TiN→tin(锡) 这类假命中）
SUGGEST_TOP_N = 200  # 对 nomatch 按出现次数前 N 名做子串候选建议

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

LINK_RE = re.compile(r'\[\[([^\[\]]+?)\]\]')
DASHES = dict.fromkeys(map(ord, '‐‑‒–—−―'), '-')
CJK_RE = re.compile(r'[一-鿿]')

def has_cjk(s):
    return bool(CJK_RE.search(s))

def norm(s):
    """归一化：NFKC + 去变音符 + 小写 + 破折号统一 + 空白/下划线/连字符折叠"""
    s = unicodedata.normalize('NFKC', s).translate(DASHES)
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r'[\s_\-]+', '-', s)
    return s.strip('-')

def norm_case(s):
    """同 norm 但保留大小写（用于纯 ASCII 严格匹配）"""
    s = unicodedata.normalize('NFKC', s).translate(DASHES)
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[\s_\-]+', '-', s)
    return s.strip('-')

def walk_md():
    files = []
    for root, dirs, names in os.walk(VAULT):
        rel_root = os.path.relpath(root, VAULT)
        top = rel_root.split(os.sep)[0]
        if top in EXCLUDE_TOP or 'node_modules' in rel_root.split(os.sep):
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for n in names:
            if n.lower().endswith('.md'):
                files.append(os.path.join(root, n))
    return files

def parse_aliases(text):
    m = re.match(r'^\ufeff?---\r?\n(.*?)\r?\n---', text, re.S)
    if not m:
        return []
    fm = m.group(1)
    out = []
    lines = fm.split('\n')
    i = 0
    while i < len(lines):
        lm = re.match(r'^(aliases?)\s*:\s*(.*)$', lines[i].strip())
        if lm:
            val = lm.group(2).strip()
            if val.startswith('['):
                inner = val.strip('[]')
                parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', inner)
                out.extend(p.strip().strip('"\'') for p in parts if p.strip().strip('"\''))
            elif val:
                out.append(val.strip('"\''))
            else:
                j = i + 1
                while j < len(lines) and re.match(r'^\s+-\s+', lines[j]):
                    item = re.sub(r'^\s+-\s+', '', lines[j]).strip().strip('"\'')
                    if item:
                        out.append(item)
                    j += 1
                i = j - 1
        i += 1
    return out

def main():
    files = walk_md()
    basename_map = defaultdict(set)
    alias_map = defaultdict(set)
    path_map = {}
    norm_map = defaultdict(set)      # norm -> relpaths（来自 basename 与 alias）
    case_map = defaultdict(set)      # norm_case -> relpaths
    all_names = defaultdict(set)     # 展示名 -> relpaths（子串建议用）
    file_text = {}

    for fp in files:
        rel = os.path.relpath(fp, VAULT).replace('\\', '/')
        noext = rel[:-3]
        base = os.path.basename(noext)
        path_map[noext] = rel
        basename_map[base].add(rel)
        norm_map[norm(base)].add(rel)
        case_map[norm_case(base)].add(rel)
        all_names[base].add(rel)
        try:
            with open(fp, encoding='utf-8') as f:
                text = f.read()
        except Exception:
            text = ''
        file_text[rel] = text
        for a in parse_aliases(text):
            alias_map[a].add(rel)
            norm_map[norm(a)].add(rel)
            case_map[norm_case(a)].add(rel)
            all_names[a].add(rel)

    occurrences = []
    for rel, text in file_text.items():
        for ln, line in enumerate(text.split('\n'), 1):
            for m in LINK_RE.finditer(line):
                occurrences.append((rel, ln, m.group(1)))

    def resolve(target):
        t = target.split('|', 1)[0].split('#', 1)[0].strip()
        if not t:
            return 'empty', set()
        t = t.replace('\\', '/')
        if os.path.splitext(os.path.basename(t).lower())[1] in ASSET_EXT:
            return 'asset', set()
        if t.lower().endswith('.md'):
            t = t[:-3]
        if '/' in t:
            if t in path_map:
                return 'resolved', {path_map[t]}
            t_base = os.path.basename(t)
            if t_base in basename_map:
                return 'resolved', basename_map[t_base]
            return 'broken', set()
        if t in basename_map:
            return 'resolved', basename_map[t]
        if t in alias_map:
            return 'resolved', alias_map[t]
        return 'broken', set()

    stats = defaultdict(int)
    broken = defaultdict(lambda: {'count': 0, 'occ': []})
    for src, ln, raw in occurrences:
        status, _ = resolve(raw)
        stats[status] += 1
        if status == 'broken':
            t = raw.split('|', 1)[0].split('#', 1)[0].strip().replace('\\', '/')
            if t.lower().endswith('.md'):
                t = t[:-3]
            b = broken[t]
            b['count'] += 1
            b['occ'].append((src, ln))

    def strict_ok(broken_name, target_paths):
        """纯 ASCII 断链名要求与目标名/别名 NFKC 后大小写一致"""
        if has_cjk(broken_name):
            return True
        bn = norm_case(broken_name)
        for disp, paths in all_names.items():
            if paths & target_paths and norm_case(disp) == bn:
                return True
        return False

    auto, ambiguous, nomatch = [], [], []
    for t, info in broken.items():
        cand = set(norm_map.get(norm(t), set()))
        if cand and not strict_ok(t, cand):
            cand = set()
        if len(cand) == 1:
            auto.append((t, next(iter(cand)), info['count'], sorted({s for s, _ in info['occ']})[:5]))
        elif len(cand) > 1:
            ambiguous.append((t, sorted(cand), info['count'], sorted({s for s, _ in info['occ']})[:3]))
        else:
            nomatch.append((t, info['count'], sorted({s for s, _ in info['occ']})[:3]))

    auto.sort(key=lambda x: -x[2])
    ambiguous.sort(key=lambda x: -x[2])
    nomatch.sort(key=lambda x: -x[1])

    # 改写计划：auto 映射 × 全部出现点（排除模板/skills 源）
    rewrite_plan = []
    for t, target, n, _ in auto:
        occs = [{'file': s, 'line': ln} for s, ln in broken[t]['occ'] if not s.startswith(REWRITE_EXCLUDE_SRC)]
        if occs:
            rewrite_plan.append({'old': t, 'new': os.path.splitext(os.path.basename(target))[0], 'target': target, 'occurrences': occs})
    rewrite_plan.sort(key=lambda x: -len(x['occurrences']))

    # 子串候选建议（nomatch 前 N 名）
    suggest = []
    for t, n, srcs in nomatch[:SUGGEST_TOP_N]:
        cands = set()
        tl = t.lower()
        for disp, paths in all_names.items():
            dl = disp.lower()
            if len(tl) >= 2 and (tl in dl or (len(dl) >= 2 and dl in tl)):
                cands.update(paths)
        cands = sorted(cands)[:6]
        if cands:
            suggest.append((t, ' | '.join(cands), n, '; '.join(srcs)))

    by_top = defaultdict(int)
    for t, info in broken.items():
        for s, _ in info['occ']:
            by_top[s.split('/')[0]] += 1

    os.makedirs(OUT_DIR, exist_ok=True)
    report = {
        'vault': VAULT,
        'md_files': len(files),
        'link_occurrences': len(occurrences),
        'resolved': stats['resolved'],
        'asset_links': stats['asset'],
        'empty_links': stats['empty'],
        'broken_occurrences': stats['broken'],
        'broken_unique_names': len(broken),
        'auto_fixable_unique': len(auto),
        'auto_fixable_occurrences': sum(x[2] for x in auto),
        'rewrite_plan_entries': len(rewrite_plan),
        'rewrite_plan_occurrences': sum(len(x['occurrences']) for x in rewrite_plan),
        'ambiguous_unique': len(ambiguous),
        'ambiguous_occurrences': sum(x[2] for x in ambiguous),
        'nomatch_unique': len(nomatch),
        'nomatch_occurrences': sum(x[1] for x in nomatch),
        'broken_by_top_dir': dict(sorted(by_top.items(), key=lambda x: -x[1])),
    }
    with open(os.path.join(OUT_DIR, 'link_map_report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, 'link_map_rewrite_plan.json'), 'w', encoding='utf-8') as f:
        json.dump(rewrite_plan, f, ensure_ascii=False, indent=2)

    def wcsv(name, header, rows):
        with open(os.path.join(OUT_DIR, name), 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)

    wcsv('link_map_auto.csv', ['broken_name', 'fix_target_relpath', 'occurrences', 'sample_sources'],
         [(t, c, n, '; '.join(s)) for t, c, n, s in auto])
    wcsv('link_map_ambiguous.csv', ['broken_name', 'candidates', 'occurrences', 'sample_sources'],
         [(t, ' | '.join(c), n, '; '.join(s)) for t, c, n, s in ambiguous])
    wcsv('link_map_nomatch.csv', ['broken_name', 'occurrences', 'sample_sources'],
         [(t, n, '; '.join(s)) for t, n, s in nomatch])
    wcsv('link_map_substring_suggest.csv', ['broken_name', 'substring_candidates', 'occurrences', 'sample_sources'], suggest)

    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
