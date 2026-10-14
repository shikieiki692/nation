# -*- coding: utf-8 -*-
"""验证：现有新卷 docx 的 word/media 内容 hash 集合 vs 卷 md 引用图（实际落点）的内容 hash 集合。
若一致 ⇒ 说明「图源＝卡片 images/」，重构只需修搜索路径。"""
import io, os, re, zipfile, hashlib, glob, collections

os.chdir(r'C:\Obsidion\妙妙屋')
D = '00-首页/题组Word/初赛模拟卷/真题版式'


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]


# 全库图片内容索引（排除 .git/.workbuddy）
BYHASH = collections.defaultdict(list)
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d not in ('.git', '.workbuddy')]
    for f in fn:
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                p = os.path.join(dp, f)
                BYHASH[sha(open(p, 'rb').read())].append(p.replace('\\', '/'))
            except Exception:
                pass
print('全库图片内容 hash 数:', len(BYHASH))

for v in ['XVI', 'XVII', 'X']:
    md = '04-题库/初赛模拟卷%s（非有机·答案版）.md' % v
    dx = os.path.join(D, '初赛模拟卷%s（非有机·答案与解析版·真题版式）.docx' % v)
    if not (os.path.exists(md) and os.path.exists(dx)):
        print('卷%s 缺文件' % v); continue
    t = io.open(md, encoding='utf-8-sig').read()
    names = [os.path.basename(x) for x in re.findall(r'!\[\[([^\]|]+?\.(?:jpg|jpeg|png))', t, re.I)]
    md_hashes = set()
    for n in names:
        hits = [p for p in BYHASH.values() for p in [] ]  # noop
    # md 图的 hash：按文件名找文件再算
    name2hash = {}
    for h, paths in BYHASH.items():
        for p in paths:
            name2hash.setdefault(os.path.basename(p), h)
    md_h = set(name2hash[n] for n in names if n in name2hash)
    z = zipfile.ZipFile(dx)
    media = [x for x in z.namelist() if x.startswith('word/media/')]
    dx_h = set(sha(z.read(x)) for x in media)
    inter = md_h & dx_h
    print('卷%-5s md图=%-3d(有hash %-3d) ｜ docx media=%-3d ｜ 内容交集=%-3d ｜ 一致率=%.0f%%'
          % (v, len(names), len(md_h), len(media), len(inter), 100.0 * len(inter) / max(1, len(md_h))))
    if media:
        print('        docx media 名样例:', [os.path.basename(x) for x in media[:3]])
    # 反查：docx 的图能在库里找到出处吗
    miss = [h for h in dx_h if h not in BYHASH]
    print('        docx 图内容在库中找不到的: %d' % len(miss))
