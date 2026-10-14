# -*- coding: utf-8 -*-
r"""把 vol_img_upscale 登记进 X~XV 的 vol_meta post_patches（幂等）。"""
import json, io, os
os.chdir(r'C:\Obsidion\妙妙屋')
WHY = ('图片排版：构建器按朝向定尺寸后 apply_dpi_cap 只缩不放 ⇒ 图偏小（同 XVI/XVII）。'
       '本补丁在保证 ≥150dpi 下放大到 min(dpi上限, CAP_ORG×1.35, 12cm)，幂等；重建 docx 后必须重跑。')
for V in ['X', 'XI', 'XIp', 'XIV', 'XV']:
    p = '.workbuddy/tmp/opt_pipe/vol_meta_%s.json' % V
    if not os.path.isfile(p):
        print('  %-6s vol_meta 缺失 ⇒ 跳过' % V); continue
    d = json.load(io.open(p, encoding='utf-8'))
    pp = d.get('post_patches') or []
    if any(x.get('script') == 'vol_img_upscale.py --vol %s' % V for x in pp):
        print('  %-6s 已登记' % V); continue
    pp.append({'script': 'vol_img_upscale.py --vol %s' % V, 'why': WHY, 'added': '2026-10-14'})
    d['post_patches'] = pp
    json.dump(d, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('  %-6s 已登记 (%d 项)' % (V, len(pp)))
