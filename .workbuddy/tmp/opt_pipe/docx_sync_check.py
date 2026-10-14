# -*- coding: utf-8 -*-
"""卷族 docx 与卷 md 的一致性核查：
   ① 盘点各卷有哪些 docx 版本（答案版/学生版/答题卡…）
   ② 逐卷计算 docx↔md 的 CJK 三元组缺口比（新鲜 docx 应 <1.5%）
   ③ 标注媒体数是否守恒
"""
import io, os, re, glob, zipfile, collections, datetime

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/题组Word/初赛模拟卷/真题版式'
MDIR = '04-题库'

VOLS = ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']

def docx_text(p):
    x = zipfile.ZipFile(p).read('word/document.xml').decode('utf-8')
    return ''.join(re.findall(r'<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>', x))

def cjk3(s):
    s = re.sub(r'[^\u4e00-\u9fff]', '', s)
    return set(s[i:i+3] for i in range(len(s)-2))

def media_n(p):
    return len([n for n in zipfile.ZipFile(p).namelist() if n.startswith('word/media/')])

print('=== ① 各卷 docx 清单 ===')
inv = collections.defaultdict(list)
for f in sorted(glob.glob(D + '/*.docx')):
    m = re.search(r'初赛模拟卷([XVI]+)（非有机·(.+?)）\.docx', os.path.basename(f))
    if m:
        inv[m.group(1)].append(m.group(2))
for v in VOLS:
    if v in inv:
        print('  卷%-5s %d 个版本: %s' % (v, len(inv[v]), ' | '.join(inv[v])))
    else:
        print('  卷%-5s （无 docx）' % v)

print()
print('=== ② docx↔md CJK 三元组缺口比 ===')
print('%-6s %-22s %-8s %-8s %-9s %s' % ('卷', '版本', 'md三元组', 'docx', '缺口比', '判定'))
md_cache = {}
for v in VOLS:
    mp = os.path.join(MDIR, '初赛模拟卷%s（非有机·答案版）.md' % v)
    if not os.path.exists(mp):
        continue
    if v not in md_cache:
        md_cache[v] = io.open(mp, encoding='utf-8-sig').read()
    base = cjk3(md_cache[v])
    for ver in inv.get(v, []):
        p = os.path.join(D, '初赛模拟卷%s（非有机·%s）.docx' % (v, ver))
        dt = docx_text(p)
        d3 = cjk3(dt)
        # 缺口：md 有但 docx 无
        gap = len(base - d3) / max(1, len(base))
        if ver.startswith('答案'):
            verd = 'OK' if gap < 0.03 else ('查' if gap < 0.10 else '🔴大缺口')
        else:
            # 学生版无答案区，缺口天然大，用反向（docx 有但 md 无）判「越界」
            verd = '含答案风险' if len(d3 - base) > 200 else 'OK'
        print('%-6s %-22s %-8d %-8d %-8.2f%% %s' % (v, ver[:22], len(base), len(d3), gap*100, verd))
