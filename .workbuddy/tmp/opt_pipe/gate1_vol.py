# -*- coding: utf-8 -*-
"""第一闸门（卷族版）：答案版 md 剥「答案区＋> 来源行」后，与学生版 md 对比。
   判据：只允许空行/首尾差异；任何实质行差异都要列出。"""
import io, os, re, glob, difflib

os.chdir(r'C:\Obsidion\妙妙屋')
MD = '04-题库'
VOLS = ['X', 'XI', 'XIp', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']

def strip_fm(t):
    m = re.match(r'^---\r?\n.*?\r?\n---\r?\n', t, re.S)
    return t[m.end():] if m else t

def cut_answers(t):
    """从答案版中剥掉答案区：`#### 答案` 之后直到下一个 `### 第 N 题`（或文件末）。"""
    out, skipping = [], False
    for ln in t.split('\n'):
        if re.match(r'^###\s+第\s*\d+\s*题', ln):
            skipping = False
        elif re.match(r'^#{3,5}\s*答案', ln):
            skipping = True
        if not skipping:
            out.append(ln)
    return '\n'.join(out)

def drop_src(t):
    return '\n'.join(l for l in t.split('\n') if not re.match(r'^>\s*来源[:：]', l))

print('=== 第一闸门：学生版题面 ≡ 答案版题面（剥答案＋来源后）===')
print('%-7s %-9s %-9s %-8s %s' % ('卷', '学生行', '剥后行', '实质差异', '判定'))
for v in VOLS:
    sp = os.path.join(MD, '初赛模拟卷%s（非有机·学生版）.md' % v)
    ap = os.path.join(MD, '初赛模拟卷%s（非有机·答案版）.md' % v)
    if not (os.path.exists(sp) and os.path.exists(ap)):
        print('%-7s （缺文件）' % v)
        continue
    s = strip_fm(io.open(sp, encoding='utf-8-sig').read())
    a = drop_src(cut_answers(strip_fm(io.open(ap, encoding='utf-8-sig').read())))
    sl = [l.rstrip() for l in s.split('\n')]
    al = [l.rstrip() for l in a.split('\n')]
    # 去掉空行后逐行 diff
    sn = [l for l in sl if l.strip()]
    an = [l for l in al if l.strip()]
    diff = [l for l in difflib.unified_diff(sn, an, lineterm='', n=0)
            if l[:1] in '+-' and not l.startswith(('+++', '---'))]
    verdict = 'OK' if not diff else '差异 %d' % len(diff)
    print('%-7s %-9d %-9d %-8d %s' % (v, len(sn), len(an), len(diff), verdict))
    if diff:
        for l in diff[:6]:
            print('        %s' % l[:110])
