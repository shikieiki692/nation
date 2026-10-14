# -*- coding: utf-8 -*-
"""把「第40届chemy初赛模拟10~18 + 无机19 + 有机20~22」的每套，
与 chemmy 全部官方合集套（32~39 届）做**题名指纹**比对，定位真身。"""
import io, os, re, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
CARD = '04-题库/2026机构初赛模拟题/chemy/题-*.md'


def load():
    d = collections.defaultdict(set)   # source_norm -> set(指纹)
    for p in glob.glob(CARD):
        t = io.open(p, encoding='utf-8-sig').read()
        m = re.search(r'^source_norm:\s*"?chemy-(.+?)"?\s*$', t, re.M)
        if not m:
            continue
        s = m.group(1)
        # 指纹 = 文件名去掉「题-CM-<套>-<题>-」前缀后的前 16 字
        fp = re.sub(r'^题-CM-\d+-\d+-', '', os.path.basename(p)[:-3])[:16]
        fp = re.sub(r'\s+', '', fp)
        d[s].add(fp)
    return d


D = load()
TARGETS = [k for k in D if re.match(r'第40届chemy初赛', k)]
OTHERS = [k for k in D if not k.startswith('第40届')]

print('目标套数 %d ；对照套数 %d' % (len(TARGETS), len(OTHERS)))
print()
for tk in sorted(TARGETS, key=lambda x: (len(x), x)):
    tk_fp = D[tk]
    best = []
    for ok in OTHERS:
        inter = tk_fp & D[ok]
        if inter:
            best.append((len(inter), ok, len(D[ok])))
    best.sort(reverse=True)
    tag = ('第%d套' % int(re.search(r'模拟\s*(\d+)', tk).group(1))) if re.search(r'模拟\s*(\d+)', tk) else tk
    if best:
        print('◆ %-28s (%d卡) 命中：' % (tk, len(tk_fp)))
        for n, ok, tot in best[:4]:
            print('      %2d/%d ↔ %s (%d卡)' % (n, len(tk_fp), ok, tot))
    else:
        print('◆ %-28s (%d卡) ⇒ 与库内任何套均无同题' % (tk, len(tk_fp)))
