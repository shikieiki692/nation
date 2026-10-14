# -*- coding: utf-8 -*-
"""10 处卷族断图深查：同名异扩展名？上下文归属？卡片侧是否有图。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
SKIP = ('.git', '.workbuddy', '_bak', '_归档', '_待清理')
BYSTEM = collections.defaultdict(set)
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d not in SKIP and not d.startswith('.git')]
    for f in fn:
        s = os.path.splitext(f)
        if s[1].lower() in ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg'):
            BYSTEM[s[0]].add(s[1])

TARGETS = {
    '初赛模拟卷XI（非有机·答案版）.md': ['hysc13_q05_p06.jpg', 'hysc13_q05_p07.jpg', 'hysc13_q05_p08.jpg'],
    '初赛模拟卷XVII（非有机·答案版）.md': ['1d4def0b1ad682782765178a5a92f3c190101381c85a70e0643653a8f71a8bf5.jpg',
                                          '413bcf86e6487a51dc569271ca43f5f624e1cf92a626945a55c4322288201e37.jpg',
                                          'c033d63ff6b8c892ad6faf21fea716de2da5c6124f2871314baf19c29ab1ae2f.jpg'],
    '初赛模拟卷X（非有机·答案版）.md': ['a6ac38603af86101b5528df8fc8ea8035a0c900f9e2690fdb353be1fcf237185.jpg'],
}
for vol, hh in TARGETS.items():
    p = '04-题库/' + vol
    t = io.open(p, encoding='utf-8-sig').read()
    L = t.split('\n')
    print('◆ %s' % vol)
    for h in hh:
        st = os.path.splitext(h)[0]
        alt = sorted(BYSTEM.get(st, []))
        # 上下文：向上找最近的 ### 第 N 题
        ln = next((i for i, l in enumerate(L) if h in l), -1)
        head = ''
        for j in range(ln, -1, -1):
            if re.match(r'^###\s*第', L[j]):
                head = L[j].strip()[:50]; break
        print('   %-70s' % h[:70])
        print('       同名异扩展名: %s ｜ 上下文: %s' % (alt or '无', head))
    print()
print('=== 这些图名在库内任何文本中被提到吗（引用源）===')
for vol, hh in TARGETS.items():
    for h in hh:
        st = os.path.splitext(h)[0]
        hits = []
        for f in glob.glob('04-题库/**/*.md', recursive=True):
            try:
                if st in io.open(f, encoding='utf-8-sig', errors='replace').read():
                    hits.append(os.path.basename(f)[:56])
            except Exception:
                pass
        print('   %-40s → %s' % (h[:40], hits[:3] if hits else '**全库无引用**'))
