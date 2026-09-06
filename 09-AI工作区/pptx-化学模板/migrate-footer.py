# -*- coding: utf-8 -*-
"""改版二+三：浅色页页脚统一为绝对定位（分隔线 y=384、页码右下角 N / 20），
并加左侧 8pt 墨绿边条 + 底部橙黄进度段。深色页只加页码。"""
import re
import pathlib

SLIDES = pathlib.Path(__file__).parent / 'slides'

# 浅色页序列（页码 -> 进度高度 pt）：6% -> 90%
LIGHT = [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

def sidebar(page):
    i = LIGHT.index(page)
    h = round(405 * (0.06 + i * (0.84 / (len(LIGHT) - 1))))
    top = 405 - h
    return (f'  <div style="position: absolute; left: 0; top: 0; width: 8pt; height: 405pt; background: #1B4332;"></div>\n'
            f'  <div style="position: absolute; left: 0; top: {top}pt; width: 8pt; height: {h}pt; background: #E8A33D;"></div>\n')

def light_footer(page):
    return (f'  <div style="position: absolute; left: 40pt; top: 384pt; width: 640pt; height: 1pt; background: #DDE5DD;"></div>\n'
            f'  <p style="position: absolute; right: 40pt; top: 388pt; width: 80pt; text-align: right; color: #6B7280; font-size: 10pt;">{page} / 20</p>\n')

FILES = {2: '02-usage.html', 3: '03-contents.html', 5: '05-concept.html', 6: '06-points.html',
         7: '07-cards.html', 8: '08-micro.html', 9: '09-derivation.html', 10: '10-exercise.html',
         11: '11-lab.html', 12: '12-phenomena.html', 13: '13-chart.html', 14: '14-framework.html',
         15: '15-quiz.html', 16: '16-timeline.html', 17: '17-compare.html', 18: '18-icons.html',
         19: '19-blank.html'}

FOOTER_RE = re.compile(
    r'\n  <div style="margin: [^"]*?40pt 14pt 40pt;[^"]*?">\s*'
    r'<div style="background: #D9D2C4; height: 1pt;"></div>\s*'
    r'<p[^>]*>课程名称 · 页码 \d+</p>\s*</div>')

for page, fname in FILES.items():
    p = SLIDES / fname
    text = p.read_text(encoding='utf-8')

    # 1) 移除旧页脚（03 目录页原本无页脚）
    if page != 3:
        text, n = FOOTER_RE.subn('', text, count=1)
        assert n == 1, f'{fname}: old footer not found'

    # 2) 左侧边条（插在 <body> 之后、六边形之前）
    assert '#1B4332; width: 8pt' not in text
    text = text.replace('<body>\n', '<body>\n' + sidebar(page), 1)

    # 3) 绝对定位页脚（</body> 之前）
    text = text.replace('\n</body>', '\n' + light_footer(page) + '</body>', 1)

    p.write_text(text, encoding='utf-8')
    print('migrated', fname)

# 深色页：右下角米白 60% 页码，无分隔线
for page, fname in [(1, '01-cover.html'), (4, '04-section.html'), (20, '20-ending.html')]:
    p = SLIDES / fname
    text = p.read_text(encoding='utf-8')
    pg = (f'  <p style="position: absolute; right: 40pt; top: 382pt; width: 80pt; text-align: right; '
          f'color: rgba(250,247,240,0.6); font-size: 10pt;">{page} / 20</p>\n')
    text = text.replace('\n</body>', '\n' + pg + '</body>', 1)
    p.write_text(text, encoding='utf-8')
    print('dark page number ->', fname)

print('all done')
