# -*- coding: utf-8 -*-
"""全局断链（全文件索引：任意扩展名 + 目录名亦可解析）"""
import io, os, re, collections
os.chdir(r'C:\Obsidion\妙妙屋')
IDX = set(); BASE = set()
for dp, dn, fn in os.walk('.'):
    if dp.startswith('./.git'):
        continue
    rel = os.path.relpath(dp, '.').replace('\\', '/')
    if rel != '.':
        IDX.add(rel); BASE.add(os.path.basename(dp))
    for f in fn:
        r = (rel + '/' + f).replace('\\', '/')
        if r.startswith('./'):
            r = r[2:]
        IDX.add(r)
        stem = os.path.splitext(f)[0]
        IDX.add(stem); BASE.add(stem)
D = '00-首页/活跃任务'
PLACE = re.compile(r'^(…|\.\.\.|<.*>|哈希|xxx|示例|文件|路径|name)')

def resolvable(l):
    """Obsidian 解析：完整路径 / 带扩展名 / 去扩展名 / 纯文件名 / 纯文件名去扩展名"""
    cands = {l, l[:-3] if l.endswith('.md') else l + '.md',
             os.path.basename(l), os.path.splitext(os.path.basename(l))[0]}
    if cands & IDX or cands & BASE:
        return True
    return False

tot = 0; bad = []
for f in sorted(os.listdir(D)):
    if not f.endswith('.md'):
        continue
    t = io.open(os.path.join(D, f), encoding='utf-8-sig').read()
    for l in re.findall(r'\[\[([^\]|#]+)', t):
        l = l.strip()
        if l.startswith('./'):
            l = l[2:]
        if not l:
            continue
        tot += 1
        if resolvable(l):
            continue
        if PLACE.match(l):
            continue
        bad.append((f, l))
print('wikilink 总数 %-4d ｜ 断链 %d 条（涉及 %d 个文件）' % (tot, len(bad), len({f for f, _ in bad})))
print('（注：`图片剩余待手绘清单.md` 头部自述「已失效，勿据此执行（2026-09-17）…建议迁入 00-首页/归档/」，其条目单独看）')
print()
bad_ex = [(f, l) for f, l in bad if f != '图片剩余待手绘清单.md']
print('排除该失效文件后：断链 %d 条（涉及 %d 文件）' % (len(bad_ex), len({f for f, _ in bad_ex})))
print()
print('按目标聚合（前 12）：')
for k, v in collections.Counter(l for _, l in bad_ex).most_common(12):
    print('   %-3d %s' % (v, k[:72]))
print()
print('按文件聚合（前 8）：')
for k, v in collections.Counter(f for f, _ in bad_ex).most_common(8):
    print('   %-3d %s' % (v, k[:60]))
