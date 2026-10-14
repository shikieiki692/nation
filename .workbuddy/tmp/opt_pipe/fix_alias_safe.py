# -*- coding: utf-8 -*-
r"""别名修正（稳健版）：把 `![[名.jpg\|N]]` / `![[名.jpg\N]]` 统一为 `![[名.jpg]]`。

残留判据＝**图名内含 `|` 或 `\`**（直白可靠，不用易错的正则转义）。
"""
import io, os, re, shutil, datetime, sys

ROOT = r"C:\Obsidion\妙妙屋"
VOLS = ['X', 'XI', 'XIp', 'XIV', 'XV', 'XVI']
BAK = os.path.join(ROOT, '.workbuddy/tmp/opt_pipe/_bak/alias_fix2_%s'
                   % datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
os.makedirs(BAK, exist_ok=True)

EMBED = re.compile(r'!\[\[([^\]]+)\]\]')


def dirty_names(text):
    return [m.group(1) for m in EMBED.finditer(text) if ('|' in m.group(1) or '\\' in m.group(1))]


def clean(text):
    """逐个处理脏图名：切掉 `\` 或 `|` 之后的一切，保留 .ext 前的部分。"""
    def fix(m):
        inner = m.group(1)
        if '|' not in inner and '\\' not in inner:
            return m.group(0)
        core = re.split(r'[\\|]', inner)[0].strip()
        return '![[%s]]' % core
    return EMBED.sub(fix, text)


tot = 0
for v in VOLS:
    for tag in ['学生版', '答案版']:
        p = os.path.join(ROOT, '04-题库', '初赛模拟卷%s（非有机·%s）.md' % (v, tag))
        if not os.path.isfile(p):
            continue
        d = io.open(p, encoding='utf-8', newline='').read()
        before = len(EMBED.findall(d))
        bad_before = dirty_names(d)
        if not bad_before:
            print('  %-5s %-4s 干净' % (v, tag)); continue
        new = clean(d)
        after = len(EMBED.findall(new))
        bad_after = dirty_names(new)
        if before != after or bad_after:
            print('  %-5s %-4s !! 异常（图数 %d→%d，残留 %d）跳过' % (v, tag, before, after, len(bad_after)))
            continue
        shutil.copy2(p, os.path.join(BAK, os.path.basename(p)))
        io.open(p, 'w', encoding='utf-8', newline='').write(new)
        tot += len(bad_before)
        print('  %-5s %-4s 修正 %-3d 处 ｜ 图数 %d ✓ ｜ 例：%s' % (v, tag, len(bad_before), after, bad_before[0][:44]))
print('\n合计修正 %d 处 ｜ 备份：%s' % (tot, BAK))
