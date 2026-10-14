# -*- coding: utf-8 -*-
"""卷族三版本一致性核查（修正版）
 A. 学生版 docx  ↔ 学生版 md
 B. 答案版 docx  ↔ 答案版 md
 C. 学生版 md    ↔ 答案版 md（题面必须一致；判据=只允许空行/答案区差异）
 D. 答题卡 docx 结构
"""
import io, os, re, glob, zipfile, collections

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/题组Word/初赛模拟卷/真题版式'
MD = '04-题库'
VOLS = ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']

def docx_text(p):
    x = zipfile.ZipFile(p).read('word/document.xml').decode('utf-8')
    return ''.join(re.findall(r'<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>', x))

def cjk3(s):
    s = re.sub(r'[^\u4e00-\u9fff]', '', s)
    return set(s[i:i+3] for i in range(len(s)-2))

def media_n(p):
    return len([n for n in zipfile.ZipFile(p).namelist() if n.startswith('word/media/')])

print('=== A/B. 各版本 docx ↔ 对应 md 缺口比 ===')
print('%-6s %-6s %-8s %-8s %-9s %-8s %s' % ('卷', '版本', 'md三元组', 'docx', '缺口比', 'media', '判定'))
rows = []
for v in VOLS:
    for tag, docxver, mdver in [('学生', '学生版·真题版式', '学生版'), ('答案', '答案与解析版·真题版式', '答案版')]:
        mdp = os.path.join(MD, '初赛模拟卷%s（非有机·%s）.md' % (v, mdver))
        dxp = os.path.join(D, '初赛模拟卷%s（非有机·%s）.docx' % (v, docxver))
        if not (os.path.exists(mdp) and os.path.exists(dxp)):
            print('%-6s %-6s  [缺失 md=%s docx=%s]' % (v, tag, os.path.exists(mdp), os.path.exists(dxp)))
            continue
        base = cjk3(io.open(mdp, encoding='utf-8-sig').read())
        dt = cjk3(docx_text(dxp))
        gap = len(base - dt) / max(1, len(base))
        mn = media_n(dxp)
        # md 图引用数
        mt = io.open(mdp, encoding='utf-8-sig').read()
        mref = len(re.findall(r'!\[\[([^\]|]+?\.(?:jpg|jpeg|png))', mt, re.I))
        verdict = 'OK' if gap < 0.03 else ('查' if gap < 0.10 else '🔴大缺口')
        mflag = '' if mn == mref else (' 🔴图差(%d/%d)' % (mn, mref))
        print('%-6s %-6s %-8d %-8d %-8.2f%% %-8d %s%s' % (v, tag, len(base), len(dt), gap*100, mn, verdict, mflag))
        rows.append((v, tag, gap, mn, mref))

print()
print('=== C. 学生版 md ↔ 答案版 md（题面差异）===')
for v in VOLS:
    sp = os.path.join(MD, '初赛模拟卷%s（非有机·学生版）.md' % v)
    ap = os.path.join(MD, '初赛模拟卷%s（非有机·答案版）.md' % v)
    if not (os.path.exists(sp) and os.path.exists(ap)):
        continue
    s = io.open(sp, encoding='utf-8-sig').read()
    a = io.open(ap, encoding='utf-8-sig').read()
    # 学生版题面应完整出现在答案版里（按块）
    s_blk = [b.strip() for b in re.split(r'\n(?=### )', s) if b.strip()]
    a_flat = re.sub(r'\s+', '', a)
    miss = [b[:30] for b in s_blk if re.sub(r'\s+', '', b)[:60] not in a_flat]
    print('  卷%-6s 学生块 %-4d 未在答案版找到 %-3d %s' % (v, len(s_blk), len(miss), miss[:2] if miss else 'OK'))

print()
print('=== D. 答题卡 ===')
for v in VOLS:
    p = os.path.join(D, '初赛模拟卷%s（非有机·答题卡）.docx' % v)
    if not os.path.exists(p):
        continue
    t = docx_text(p)
    print('  卷%-6s 文本 %-5d 字 ｜ 含「答题卡」=%d ｜ 含「姓名」=%d' % (v, len(t), t.count('答题卡'), t.count('姓名') + t.count('班级')))
