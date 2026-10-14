# -*- coding: utf-8 -*-
r"""判定「缺图」是否已被卷内**等价图**覆盖：按**尺寸**（同图不同编码时尺寸一致）在卷内图里找近似匹配，
并输出尺寸完全一致者，供人工判断。
用法：python judge_equiv.py <卷> <图名前缀> [更多前缀…]
"""
import os, re, sys, io, hashlib
from PIL import Image

ROOT = r"C:\Obsidion\妙妙屋"
VOL = sys.argv[1]
PREFIXES = sys.argv[2:]
IMG_DIRS = [r for r, d, f in os.walk(os.path.join(ROOT, '04-题库')) if os.path.basename(r) == 'images']
EMBED = re.compile(r'!\[\[([^\]]+)\]\]')


def find(pre):
    for d in IMG_DIRS:
        for f in os.listdir(d):
            if f.startswith(pre):
                return os.path.join(d, f)
    return None


# 卷内图（两版）
vol_names = set()
for tag in ['学生版', '答案版']:
    p = os.path.join(ROOT, '04-题库', '初赛模拟卷%s（非有机·%s）.md' % (VOL, tag))
    if os.path.isfile(p):
        vol_names |= set(EMBED.findall(io.open(p, encoding='utf-8-sig').read()))

# 卷内图的尺寸表
vol_sizes = {}
for n in vol_names:
    q = find(os.path.basename(n)[:24])
    if q:
        try:
            vol_sizes.setdefault(Image.open(q).size, []).append(n[:20])
        except Exception:
            pass

for pre in PREFIXES:
    q = find(pre)
    if not q:
        print('%s → 文件未找到' % pre); continue
    sz = Image.open(q).size
    same = vol_sizes.get(sz, [])
    verdict = '✅ 卷内已有**同尺寸**等价图 %s' % same[:3] if same else '🔴 卷内**无同尺寸**图 ⇒ 真缺'
    print('%-18s %s  %s' % (pre, sz, verdict))
