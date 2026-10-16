# -*- coding: utf-8 -*-
"""O1 结构核验 v2：整题（题面＋答案）图 hash 集合 vs 源卡；打印非 hash 引用。"""
import io, os, re, json

R = r'C:\Obsidion\妙妙屋'
QB = os.path.join(R, '04-题库')
IMG = re.compile(r'!\[\[([^\]]+)\]\]')
IMG_MD = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
IMG_HTML = re.compile(r'<img[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']', re.I)


def raw(t):
    return IMG.findall(t) + IMG_MD.findall(t) + IMG_HTML.findall(t)


def clean(n):
    # ★ 先剥 `|size` / `\|size` 后缀，**再** basename（顺序反了会把 \| 当成路径分隔符）
    n = re.split(r'\\?\|', n.strip(), maxsplit=1)[0].strip()
    n = os.path.basename(n.replace('\\', '/'))
    m = re.match(r'^([0-9a-fA-F]{8,})', n)
    return (m.group(1)[:12].lower() if m else n.lower())


plan = json.load(io.open(os.path.join(R, r'.workbuddy\tmp\opt_pipe\vol_plan_O1.json'), encoding='utf-8'))
cards = [it.get('path') for g, items in plan for it in items]

for tag in ('答案版', '学生版'):
    VOL = os.path.join(QB, '初赛模拟卷O1（有机·%s）.md' % tag)
    txt = io.open(VOL, encoding='utf-8-sig').read()
    parts = re.split(r'(?m)^### 第 (\d+) 题', txt)
    print('########## %s ##########' % tag)
    tm = te = 0
    for i in range(1, len(parts), 2):
        n = int(parts[i]); blk = parts[i + 1]
        vi = set(clean(x) for x in raw(blk))
        ct = io.open(os.path.join(R, cards[n - 1]), encoding='utf-8-sig').read()
        ci = set(clean(x) for x in raw(ct))
        miss = sorted(x for x in ci - vi if x)
        extra = sorted(x for x in vi - ci if x)
        tm += len(miss); te += len(extra)
        bad = [x for x in raw(blk) if not re.match(r'^[0-9a-fA-F]{8,}', clean(x))]
        flag = '' if not (miss or extra) else '  <<<'
        print('  第%2d题 卷%3d 卡%3d 缺%2d 多%2d%s' % (n, len([x for x in vi if x]), len([x for x in ci if x]), len(miss), len(extra), flag))
        if miss: print('      缺:', miss)
        if extra: print('      多:', extra)
        if bad: print('      非hash引用:', bad)
    print('  ==== 合计：缺 %d，多 %d ====' % (tm, te))
