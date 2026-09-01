# -*- coding: utf-8 -*-
"""
阶段五：残留清理（用户已确认范围）

1. 删 media_downloads 中「库内另有副本」的 14 张图（2.51 MB，零信息损失）
   —— 已用 sha256 全库比对确认副本存在于 媒体仓库/
2. 删 13 个一次性旧脚本，保留 fix_image_refs.py
   —— 根目录：compare_answers.py / _final.py / _v2.py（同一功能三版本）+ random_validation.py
   —— scripts/ 下 10 个零引用脚本

安全前提：全部文件均已 git 跟踪，误删可 `git checkout` 恢复。
"""
import os

VAULT = r"C:\Obsidion\妙妙屋"
MD = os.path.join(VAULT, "09-AI工作区", "media_downloads")

# ---- 1. 有副本的 14 张图（sha256 已确认副本在媒体仓库）----
DUP_IMGS = [
    'deduction_flowchart.png', 'diagonal_relationship.png',
    'diagonal_relationship_new.png', 'diphosphene.png',
    'gas_signals_table.png', 'gas_signals_table_v3.png',
    'latimer_mn_cr.png', 'rutile.png', 'thiosulfate.png',
    'valency_number_line.png', 'xef2.png', 'xef6.png',
    'xeo3.png', 'xeo4.png',
]

# ---- 2. 待删脚本（保留 fix_image_refs.py）----
ROOT_SCRIPTS = [
    'compare_answers.py', 'compare_answers_final.py',
    'compare_answers_v2.py', 'random_validation.py',
]
SUB_SCRIPTS = [
    'book_match.py', 'book_match3.py', 'draw_batch1_jiaoti.py',
    'draw_batch1_wuhua.py', 'draw_batch1_zhenti.py',
    'find_missing_images.py', 'fix_span_wrapper.py', 'match2.py',
    'replace_batch1_wuhua.py', 'review_matches.py',
]

done, failed = [], []

for fn in DUP_IMGS:
    p = os.path.join(MD, fn)
    if not os.path.exists(p):
        failed.append((p, 'not found'))
        continue
    sz = os.path.getsize(p)
    os.remove(p)
    done.append((f'img: {fn}', sz))

for fn in ROOT_SCRIPTS:
    p = os.path.join(VAULT, fn)
    if not os.path.exists(p):
        failed.append((p, 'not found'))
        continue
    sz = os.path.getsize(p)
    os.remove(p)
    done.append((f'root script: {fn}', sz))

for fn in SUB_SCRIPTS:
    p = os.path.join(VAULT, 'scripts', fn)
    if not os.path.exists(p):
        failed.append((p, 'not found'))
        continue
    sz = os.path.getsize(p)
    os.remove(p)
    done.append((f'scripts/{fn}', sz))

total = sum(s for _, s in done)
print(f'=== 已删 {len(done)} 项 / {total/1024/1024:.2f} MB ===')
for label, sz in done:
    print(f'  {sz/1024:8.0f} KB  {label}')
if failed:
    print(f'\n=== 失败 {len(failed)} 项 ===')
    for p, why in failed:
        print(f'  {p}  ({why})')

# 复核：保留项仍在
keep = [os.path.join(VAULT, 'fix_image_refs.py')]
print('\n=== 保留项复核 ===')
for p in keep:
    print(f'  {"OK" if os.path.exists(p) else "缺失!!"}  {os.path.basename(p)}')
print('  media_downloads 剩余图片:',
      len([f for f in os.listdir(MD) if f.lower().endswith(('.png', '.jpg', '.svg'))]))
print('  scripts/ 剩余脚本:',
      len([f for f in os.listdir(os.path.join(VAULT, 'scripts'))
           if f.endswith(('.py', '.ps1'))]))
