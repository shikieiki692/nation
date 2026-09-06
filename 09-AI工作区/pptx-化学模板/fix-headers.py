# -*- coding: utf-8 -*-
"""修复：标题栏 margin 恢复 16pt；标题栏之后的第一个正文块 margin-top 归一为 14pt。"""
import re
import pathlib

SLIDES = pathlib.Path(__file__).parent / 'slides'
FILES = ['02-usage.html', '03-contents.html', '05-concept.html', '06-points.html',
         '07-cards.html', '08-micro.html', '09-derivation.html', '10-exercise.html',
         '11-lab.html', '12-phenomena.html', '13-chart.html', '14-framework.html',
         '16-timeline.html', '17-compare.html', '18-icons.html']

DIVIDER_END = 'width: 44pt; height: 2.5pt; background: #E8A33D;"></div>\n  </div>'

for fname in FILES:
    p = SLIDES / fname
    text = p.read_text(encoding='utf-8')

    # 1) 标题栏 margin 14pt -> 16pt（用 height: 34pt 标记定位）
    text, n = re.subn(r'margin: 14pt 40pt 0 40pt; width: 640pt; height: 34pt',
                      'margin: 16pt 40pt 0 40pt; width: 640pt; height: 34pt', text, count=1)
    assert n == 1, f'{fname}: header margin fix failed'

    # 2) 分隔线块之后的第一个正文块 margin-top -> 14pt
    idx = text.find(DIVIDER_END)
    assert idx > 0, f'{fname}: divider not found'
    head, tail = text[:idx], text[idx:]
    tail, n = re.subn(r'margin: \d+pt 40pt 0 40pt', 'margin: 14pt 40pt 0 40pt', tail, count=1)
    assert n == 1, f'{fname}: content margin not found'

    p.write_text(head + tail, encoding='utf-8')
    print('fixed', fname)

print('all done')
