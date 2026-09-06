# -*- coding: utf-8 -*-
"""迁移：16 个浅色页统一标题栏 + 右上角六边形装饰 + 正文上移至 y≈70pt。"""
import re
import pathlib

SLIDES = pathlib.Path(__file__).parent / 'slides'

HEX = '  <img src="../icons/hex-corner.png" style="position: absolute; right: 0; top: 0; width: 180pt; height: 150pt;">\n'

HDR = '''  <div style="{rel}margin: 16pt 40pt 0 40pt; width: 640pt; height: 34pt; display: flex; align-items: center;">
    <img src="../icons/{icon}-1B4332.png" style="width: 16pt; height: 16pt;">
    <div style="background: #E8A33D; border-radius: 3pt; margin-left: 8pt; display: flex; justify-content: center;">
      <p style="color: #FFFFFF; font-size: 10pt; font-weight: bold; margin: 2.5pt 7pt;">{chip}</p>
    </div>
    <h1 style="color: #1B4332; font-size: 26pt; font-weight: bold; margin-left: 12pt;">{title}</h1>{extra}
  </div>
  <div style="position: relative; margin: 4pt 40pt 0 40pt; width: 640pt; height: 2.5pt;">
    <div style="position: absolute; left: 0; top: 0.75pt; width: 640pt; height: 1pt; background: #DDE5DD;"></div>
    <div style="position: absolute; left: 0; top: 0; width: 44pt; height: 2.5pt; background: #E8A33D;"></div>
  </div>'''

TIMER = '''
    <div style="position: absolute; right: 0; top: 8pt; display: flex; align-items: center;">
      <img src="../icons/LuTimer-1B4332.png" style="width: 16pt; height: 16pt;">
      <p style="color: #6B7280; font-size: 12pt; margin-left: 6pt; width: 76pt;">限时 3 分钟</p>
    </div>'''

PAGES = {
    '02-usage.html':     dict(icon='LuBookOpen', chip='使用说明', title='模板使用说明'),
    '03-contents.html':  dict(icon='LuList', chip='CONTENTS', title='目录'),
    '05-concept.html':   dict(icon='LuBookOpen', chip='知识点', title='页标题占位'),
    '06-points.html':    dict(icon='LuBookOpen', chip='知识点', title='页标题占位'),
    '07-cards.html':     dict(icon='LuBookOpen', chip='知识点', title='页标题占位'),
    '08-micro.html':     dict(icon='LuSearch', chip='微观探析', title='页标题占位'),
    '09-derivation.html': dict(icon='LuSigma', chip='推导与计算', title='页标题占位'),
    '10-exercise.html':  dict(icon='LuPenLine', chip='例题精讲', title='习题讲评占位'),
    '11-lab.html':       dict(icon='LuFlaskConical', chip='实验探究', title='实验名称占位'),
    '12-phenomena.html': dict(icon='LuTestTubes', chip='现象记录', title='实验现象记录占位'),
    '13-chart.html':     dict(icon='LuChartColumn', chip='数据图表', title='页标题占位'),
    '14-framework.html': dict(icon='LuNetwork', chip='知识框架', title='页标题占位'),
    '15-quiz.html':      dict(icon='LuTarget', chip='课堂练习', title='页标题占位', extra=TIMER),
    '16-timeline.html':  dict(icon='LuHistory', chip='化学史', title='页标题占位'),
    '17-compare.html':   dict(icon='LuTable', chip='对比归纳', title='页标题占位'),
    '18-icons.html':     dict(icon='LuLayoutGrid', chip='图标库', title='图标库 · 复制即用'),
}

for fname, cfg in PAGES.items():
    p = SLIDES / fname
    text = p.read_text(encoding='utf-8')

    # 1) 替换标题栏（第一个 2 空格缩进的容器 div 块）
    rel = 'position: relative; ' if cfg.get('extra') else ''
    new_hdr = HDR.format(rel=rel, icon=cfg['icon'], chip=cfg['chip'],
                         title=cfg['title'], extra=cfg.get('extra', ''))
    new_text, n = re.subn(r'  <div style="(?:position: relative; )?margin: \d+pt 40pt 0 40pt;.*?\n  </div>',
                          new_hdr, text, count=1, flags=re.S)
    assert n == 1, f'{fname}: header block not found'
    text = new_text

    # 2) 目录页遗留的独立橙色线条 div 删除
    if fname == '03-contents.html':
        text, n = re.subn(r'\n  <div style="background: #E8A33D; width: 44pt; height: 4pt; margin: 10pt 40pt 0 40pt;"></div>',
                          '', text, count=1)
        assert n == 1, 'contents: orphan orange line not found'

    # 3) 正文第一块上移至 y≈70pt（标题栏结束于 56.5pt）
    if fname == '15-quiz.html':
        text, n = re.subn(r'margin: 24pt 60pt 0 60pt', 'margin: 16pt 60pt 0 60pt', text, count=1)
    else:
        text, n = re.subn(r'margin: \d+pt 40pt 0 40pt', 'margin: 14pt 40pt 0 40pt', text, count=1)
    assert n == 1, f'{fname}: first content margin not found'

    # 4) body 起始处插入六边形装饰
    assert 'hex-corner' not in text
    text = text.replace('<body>\n', '<body>\n' + HEX, 1)

    p.write_text(text, encoding='utf-8')
    print('migrated', fname)

print('all done')
