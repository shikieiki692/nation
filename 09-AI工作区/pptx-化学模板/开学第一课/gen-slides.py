# -*- coding: utf-8 -*-
"""开学第一课 25 页 slides/*.html 生成器 v4（吸收改版优点，套用自有模板）。
备注在 build.js；方程式用 Unicode 下标字符（₂₃₄）与 ⇌ ═ ↑ ↓。"""
import pathlib

OUT = pathlib.Path(__file__).parent / 'slides'
OUT.mkdir(exist_ok=True)

HEAD = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
html { background: #FAF7F0; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #FAF7F0;
  font-family: "Microsoft YaHei", Arial, sans-serif;
  display: flex; flex-direction: column;
}
p, h1, ul { margin: 0; }
</style>
</head>
'''

def hdr(part, icon, title):
    return f'''  <div style="margin: 16pt 40pt 0 40pt; width: 640pt; height: 34pt; display: flex; align-items: center;">
    <img src="../../icons/{icon}-1B4332.png" style="width: 16pt; height: 16pt;">
    <div style="background: #E8A33D; border-radius: 3pt; margin-left: 8pt; display: flex; justify-content: center;">
      <p style="color: #FFFFFF; font-size: 10pt; font-weight: bold; margin: 2.5pt 7pt;">{part}</p>
    </div>
    <h1 style="color: #1B4332; font-size: 26pt; font-weight: bold; margin-left: 12pt; width: 500pt;">{title}</h1>
  </div>
  <div style="position: relative; margin: 4pt 40pt 0 40pt; width: 640pt; height: 2.5pt;">
    <div style="position: absolute; left: 0; top: 0.75pt; width: 640pt; height: 1pt; background: #DDE5DD;"></div>
    <div style="position: absolute; left: 0; top: 0; width: 44pt; height: 2.5pt; background: #E8A33D;"></div>
  </div>'''

def light_page(n, part, icon, title, body):
    i = n - 2
    h = round(405 * (0.06 + i * 0.84 / 23))
    top = 405 - h
    return HEAD + f'''<body>
  <div style="position: absolute; left: 0; top: 0; width: 8pt; height: 405pt; background: #1B4332;"></div>
  <div style="position: absolute; left: 0; top: {top}pt; width: 8pt; height: {h}pt; background: #E8A33D;"></div>
  <img src="../../icons/hex-corner.png" style="position: absolute; right: 0; top: 0; width: 180pt; height: 150pt;">
{hdr(part, icon, title)}
  <div style="position: relative; margin: 14pt 40pt 0 40pt; width: 640pt; flex: 1;">
{body}
  </div>
  <div style="position: absolute; left: 40pt; top: 384pt; width: 640pt; height: 1pt; background: #DDE5DD;"></div>
  <p style="position: absolute; right: 40pt; top: 388pt; width: 80pt; text-align: right; color: #6B7280; font-size: 10pt;">{n} / 25</p>
</body>
</html>
'''

def bottom_line(text, color='#6B7280', top=280):
    return (f'    <p style="position: absolute; left: 0; top: {top}pt; width: 640pt; text-align: center; '
            f'color: {color}; font-size: 13pt;">{text}</p>')

def source_line(text):
    return (f'    <p style="position: absolute; left: 0; top: 284pt; width: 640pt; '
            f'color: #6B7280; font-size: 10.5pt;">{text}</p>')

PAGES = {}

# ---------- P1 封面（+ 英文宽字距小字） ----------
PAGES['01-cover'] = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
html { background: #1B4332; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #1B4332;
  font-family: "Microsoft YaHei", Arial, sans-serif;
  display: flex; flex-direction: column;
}
p, h1 { margin: 0; }
</style>
</head>
<body>
  <div style="width: 720pt; height: 6pt; background: #E8A33D;"></div>

  <div style="display: flex; flex: 1; width: 720pt;">
    <div style="width: 430pt; margin-left: 40pt;">
      <div style="background: #E8A33D; width: 76pt; border-radius: 3pt; margin-top: 68pt; display: flex; justify-content: center;">
        <p style="color: #FFFFFF; font-size: 12pt; font-weight: bold; margin: 4pt 0;">导入</p>
      </div>
      <p style="color: #E8A33D; font-size: 12pt; font-weight: bold; margin-top: 14pt;">M E E T&#x3000;C H E M I S T R Y</p>
      <h1 style="color: #FAF7F0; font-size: 48pt; font-weight: bold; margin-top: 8pt;">遇见化学</h1>
      <div style="background: #E8A33D; width: 56pt; height: 4pt; margin-top: 14pt;"></div>
      <p style="color: #E3EDE6; font-size: 17pt; margin-top: 16pt;">高一 · 开学第一课</p>
      <p style="color: #9DB8A9; font-size: 11.5pt; margin-top: 48pt;">授课教师：___　　2026 年 9 月</p>
    </div>

    <div style="position: relative; width: 250pt;">
      <img src="../../icons/cell-C-92.png" style="position: absolute; left: 6pt; top: 216pt; width: 138pt; height: 138pt;">
      <img src="../../icons/cell-Na-88.png" style="position: absolute; left: 119pt; top: 224pt; width: 132pt; height: 132pt;">
      <img src="../../icons/cell-H-104.png" style="position: absolute; left: 42pt; top: 87pt; width: 156pt; height: 156pt;">
      <img src="../../icons/cell-O-96.png" style="position: absolute; left: 102pt; top: 23pt; width: 144pt; height: 144pt;">
    </div>
  </div>

  <div style="width: 720pt; height: 5pt; background: #2D6A4F;"></div>
  <p style="position: absolute; right: 40pt; top: 382pt; width: 80pt; text-align: right; color: rgba(250,247,240,0.6); font-size: 10pt;">1 / 25</p>
</body>
</html>
'''

# ---------- P2 你身边有化学吗？ ----------
def photo_card(img, caption_html):
    return f'''      <div style="width: 200pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; box-shadow: 2px 2px 8px rgba(0,0,0,0.10);">
        <div style="margin: 8pt 8pt 0 8pt;"><img src="../images/{img}" style="width: 184pt; height: 150pt;"></div>
        <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.4; margin: 8pt 12pt 12pt 12pt;">{caption_html}</p>
      </div>'''

PAGES['02-daily'] = light_page(2, '导入', 'LuLightbulb', '你身边有化学吗？', f'''    <div style="display: flex; justify-content: space-between; margin-top: 12pt;">
{photo_card('card-bubble-tea.png', '<span style="font-weight: bold; color: #1B4332;">奶茶</span>：乳化剂和甜味剂，调出这一杯的口感')}
{photo_card('card-smartphone.png', '<span style="font-weight: bold; color: #1B4332;">手机</span>：锂电池、屏幕玻璃、芯片，全是材料')}
{photo_card('card-extinguisher.png', '<span style="font-weight: bold; color: #1B4332;">灭火器</span>：喷出的二氧化碳，能隔绝氧气灭火')}
    </div>
    <div style="margin: 22pt 0 0 0; background: #FBF0DA; border-left: 5pt solid #E8A33D; border-radius: 3pt; display: flex; align-items: center;">
      <img src="../../icons/LuLightbulb-B45309.png" style="width: 15pt; height: 15pt; margin-left: 12pt;">
      <p style="color: #1F2937; font-size: 15pt; margin: 10pt 14pt 10pt 8pt;"><span style="font-weight: bold; color: #1B4332;">想一想：</span>这三样的共同点？——背后都站着化学</p>
    </div>''')

# ---------- P3 化学×农业（+方程式条 + 来源小字） ----------
PAGES['03-agri'] = light_page(3, '导入', 'LuWheat', '你碗里的饭，有化学的功劳', f'''    <div style="display: flex; margin-top: 2pt;">
      <img src="../images/card-wheat.png" style="width: 352pt; height: 300pt;">
      <div style="width: 264pt; margin-left: 24pt;">
        <p style="color: #B45309; font-size: 42pt; font-weight: bold;">≈48%</p>
        <p style="color: #6B7280; font-size: 11.5pt; margin-top: 0; width: 250pt;">化学肥料间接供养全球人口比例</p>
        <ul style="color: #1F2937; font-size: 14pt; line-height: 1.45; padding-left: 20pt; margin-top: 8pt;">
          <li style="margin-bottom: 8pt;">有统计认为：化学肥料间接供养全球约 48% 人口</li>
          <li style="margin-bottom: 8pt;">1909 年，哈伯实现合成氨；博施把它工业化</li>
          <li>氮肥让粮食大幅增产，化学和「吃饭」直接相关</li>
        </ul>
        <div style="margin-top: 12pt; background: #E3EDE6; border-radius: 5pt;">
          <p style="color: #1B4332; font-size: 14.5pt; font-weight: bold; text-align: center; margin: 8pt 6pt;">N₂ + 3H₂ ⇌ 2NH₃<span style="font-weight: normal; color: #6B7280; font-size: 12pt;">（高温、高压、催化剂）</span></p>
        </div>
        <p style="color: #6B7280; font-size: 10.5pt; margin-top: 10pt;">来源：新华网 / 中国农科院（白由路）</p>
      </div>
    </div>''')

# ---------- P4 化学是什么（+水分子示意） ----------
def kw_card(word, expl):
    return f'''        <div style="width: 132pt; height: 74pt; background: #FFFFFF; border: 2pt solid #2D6A4F; border-radius: 8pt; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <p style="color: #1B4332; font-size: 19pt; font-weight: bold;">{word}</p>
          <p style="color: #6B7280; font-size: 11pt; line-height: 1.3; margin-top: 3pt; text-align: center; width: 118pt;">{expl}</p>
        </div>'''

PAGES['04-what'] = light_page(4, '化学是什么', 'LuBookOpen', '化学是什么', f'''    <div style="display: flex; margin-top: 8pt;">
      <div style="width: 356pt; background: #FBF0DA; border-left: 5pt solid #E8A33D; border-radius: 4pt;">
        <p style="color: #1F2937; font-size: 18pt; line-height: 1.75; margin: 18pt 20pt;">化学是在<span style="font-weight: bold; color: #B45309;">原子、分子</span>水平上，研究物质的<span style="font-weight: bold; color: #B45309;">组成、结构、性质与转化</span>的科学。</p>
      </div>
      <div style="width: 276pt; margin-left: 24pt;">
        <div style="display: flex; justify-content: space-between;">
{kw_card('组成', '物质由什么构成')}
{kw_card('结构', '微粒如何排列连接')}
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 10pt;">
{kw_card('性质', '表现什么特征')}
{kw_card('转化', '如何变成新物质')}
        </div>
      </div>
    </div>
    <div style="display: flex; align-items: center; margin-top: 8pt;">
      <div style="width: 356pt; display: flex; flex-direction: column; align-items: center;">
        <img src="../images/p4-molecule.png" style="width: 161pt; height: 70pt;">
        <p style="color: #1B4332; font-size: 13pt; font-weight: bold; margin-top: 2pt;">H₂O　<span style="font-weight: normal; color: #6B7280; font-size: 11pt;">水分子示意图</span></p>
      </div>
      <p style="color: #1F2937; font-size: 14pt; line-height: 1.5; width: 276pt; margin-left: 24pt;">小到一个原子、一个水分子，大到一种新药、一种航天材料，都在化学的研究范围之内。</p>
    </div>''')

# ---------- P5 化学家做三件事 ----------
def icon_card(icon, name, desc):
    return f'''      <div style="width: 200pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 6pt; box-shadow: 2px 2px 8px rgba(0,0,0,0.12);">
        <div style="background: #1B4332; height: 38pt; border-radius: 5pt 5pt 0 0; display: flex; align-items: center; justify-content: center;">
          <img src="../../icons/{icon}-FFFFFF.png" style="width: 14pt; height: 14pt;">
          <p style="color: #FFFFFF; font-size: 16pt; font-weight: bold; margin-left: 7pt;">{name}</p>
        </div>
        <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.5; margin: 14pt 14pt 16pt 14pt;">{desc}</p>
      </div>'''

PAGES['05-three'] = light_page(5, '化学是什么', 'LuFlaskConical', '化学家做三件事', f'''    <div style="display: flex; justify-content: space-between; margin-top: 26pt;">
{icon_card('LuSearch', '识别', '<span style="font-weight: bold; color: #1B4332;">这是什么</span>：分析成分、鉴定物质，比如检测一杯水的质量')}
{icon_card('LuFlaskConical', '创造', '<span style="font-weight: bold; color: #1B4332;">造出新物质</span>：合成自然界没有的材料、药物和功能分子')}
{icon_card('LuLightbulb', '解释', '<span style="font-weight: bold; color: #1B4332;">为什么这样</span>：用规律说明现象背后的原因，并做出预测')}
    </div>
{bottom_line('这三件事，也是你们三年要练的三种能力')}''')

# ---------- P6 一张表的故事 ----------
PAGES['06-table-story'] = light_page(6, '化学是什么', 'LuLayoutGrid', '一张表的故事', f'''    <div style="display: flex; margin-top: 0;">
      <img src="../images/card-mendeleev.png" style="width: 210pt; height: 230pt;">
      <div style="width: 416pt; margin-left: 14pt;">
        <img src="../images/card-mendeleev-table.png" style="width: 416pt; height: 170pt;">
        <ul style="color: #1F2937; font-size: 14pt; line-height: 1.4; padding-left: 20pt; margin-top: 12pt;">
          <li style="margin-bottom: 7pt;">1869 年，把当时已知的 63 种元素排成一张表</li>
          <li style="margin-bottom: 7pt;">表里有空位——他直接预言了还没发现的元素</li>
          <li style="margin-bottom: 7pt;">「类铝」= 镓、「类硅」= 锗，后来都被证实</li>
          <li><span style="font-weight: bold; color: #1B4332;">一张表，装下了整个物质世界的规律</span></li>
        </ul>
      </div>
    </div>''')

# ---------- P7 2025 诺贝尔化学奖：MOF ----------
PAGES['07-nobel'] = light_page(7, '化学是什么', 'LuAward', '2025 诺贝尔化学奖：MOF', f'''    <div style="display: flex; margin-top: 4pt;">
      <div style="width: 312pt;">
        <ul style="color: #1F2937; font-size: 14pt; line-height: 1.45; padding-left: 20pt;">
          <li><span style="font-weight: bold; color: #B45309;">金属有机骨架（MOF）</span>：像「分子房子」的多孔晶体</li>
        </ul>
        <div style="margin-top: 12pt; background: #FBF0DA; border-left: 5pt solid #E8A33D; border-radius: 4pt;">
          <p style="color: #1F2937; font-size: 14.5pt; line-height: 1.45; margin: 10pt 14pt;">几克 MOF 的内部总面积<br><span style="font-weight: bold; color: #B45309; font-size: 19pt;">≈ 一个足球场</span></p>
        </div>
        <ul style="color: #1F2937; font-size: 14pt; line-height: 1.45; padding-left: 20pt; margin-top: 12pt;">
          <li style="margin-bottom: 8pt;">用途①：储气 · 碳捕集 · 空气净化</li>
          <li style="margin-bottom: 8pt;">用途②：药物递送 · 半导体除毒气</li>
          <li>获奖者：北川进（日）· 罗布森（澳）· 亚吉（美/约旦）</li>
        </ul>
        <p style="color: #6B7280; font-size: 10.5pt; margin-top: 12pt;">来源：诺贝尔奖官方</p>
      </div>
      <div style="margin-left: 26pt;">
        <img src="../images/card-mof5.png" style="width: 300pt; height: 300pt;">
      </div>
    </div>''')

# ---------- P8 化学是中心科学（注解换 v4 完整短语） ----------
P8_SAT = {
    '物理': (320, 28, '原子结构、能量变化，解释反应为何发生', (352, 21, 270, 'left')),
    '生物': (110, 86, '呼吸、光合作用，本质上都是化学反应', (20, 118, 180, 'center')),
    '材料': (530, 86, '从塑料、尼龙到芯片材料，都靠化学合成', (440, 118, 180, 'center')),
    '医学': (110, 194, '新药的设计与合成，是现代医学的地基', (20, 226, 180, 'center')),
    '环境': (530, 194, '污水处理、碳捕集，都要靠化学办法', (440, 226, 180, 'center')),
    '天文': (320, 252, '分析星光，就能知道遥远星球的成分', (352, 245, 270, 'left')),
}
p8_texts = ['''    <img src="../images/p8-spokes.png" style="position: absolute; left: 0; top: 0; width: 640pt; height: 280pt;">
    <p style="position: absolute; left: 275pt; top: 125pt; width: 90pt; text-align: center; color: #FAF7F0; font-size: 20pt; font-weight: bold;">化学</p>''']
for name, (cx, cy, note, (nx, ny, nw, align)) in P8_SAT.items():
    p8_texts.append(f'    <p style="position: absolute; left: {cx - 27}pt; top: {cy - 9}pt; width: 54pt; text-align: center; color: #1B4332; font-size: 13.5pt; font-weight: bold;">{name}</p>')
    p8_texts.append(f'    <p style="position: absolute; left: {nx}pt; top: {ny}pt; width: {nw}pt; text-align: {align}; color: #6B7280; font-size: 11.5pt; line-height: 1.3;">{note}</p>')
PAGES['08-central'] = light_page(8, '化学是什么', 'LuNetwork', '化学是中心科学', '\n'.join(p8_texts))

# ---------- P9 化学×医学（三步叙事 + 2015 大数字） ----------
def step_block(num, title, desc, w=312):
    return f'''        <div style="display: flex; margin-bottom: 10pt;">
          <div style="background: #1B4332; width: 24pt; height: 24pt; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <p style="color: #FAF7F0; font-size: 12pt; font-weight: bold;">{num}</p>
          </div>
          <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.4; margin-left: 10pt; width: {w - 34}pt;"><span style="font-weight: bold; color: #1B4332;">{title}</span>{desc}</p>
        </div>'''

PAGES['09-medicine'] = light_page(9, '为什么学', 'LuPill', '化学×医学：青蒿素与屠呦呦', f'''    <div style="display: flex; margin-top: 2pt;">
      <img src="../images/card-tu-youyou.png" style="width: 300pt; height: 300pt;">
      <div style="width: 312pt; margin-left: 26pt; margin-top: 2pt;">
{step_block('①', '青蒿素 → 抗疟药物', '：从植物黄花蒿中提取出的抗疟疾有效成分')}
{step_block('②', '灵感来自一本古书', '：《肘后备急方》「青蒿一握，绞取汁」，提示不能高温煎煮')}
{step_block('③', '改用乙醚低温提取', '：保住怕热的有效成分——这一步靠的正是化学方法')}
        <div style="background: #1B4332; border-radius: 6pt; margin-top: 4pt;">
          <p style="color: #FAF7F0; font-size: 13pt; margin: 9pt 14pt;"><span style="color: #E8A33D; font-size: 20pt; font-weight: bold;">2015</span>　中国本土科学家首次获得科学类诺贝尔奖</p>
        </div>
        <p style="color: #6B7280; font-size: 10.5pt; margin-top: 8pt;">来源：诺贝尔奖官方</p>
      </div>
    </div>''')

# ---------- P10 化学×材料（三点 + 20 万吨大数字卡） ----------
PAGES['10-material'] = light_page(10, '为什么学', 'LuShirt', '化学×材料：尼龙 66', f'''    <div style="display: flex; margin-top: 2pt;">
      <img src="../images/card-jacket.png" style="width: 300pt; height: 300pt;">
      <div style="width: 312pt; margin-left: 26pt; margin-top: 2pt;">
{step_block('①', '己二腈是尼龙 66 的核心原料', '：没有它，就生产不出这种高强度的合成纤维')}
{step_block('②', '尼龙 66 耐磨、耐热、强度高', '：用于汽车轻量化部件、航空航天材料，也做成高端瑜伽服、冲锋衣面料')}
{step_block('③', '制造技术长期被国外垄断', '：己二腈曾是被「卡脖子」的关键一环')}
        <div style="background: #1B4332; border-radius: 6pt; margin-top: 4pt;">
          <p style="color: #FAF7F0; font-size: 11.5pt; margin: 10pt 14pt 0 14pt;"><span style="color: #E8A33D; font-size: 20pt; font-weight: bold;">20 万吨</span>　2025 年 12 月</p>
          <p style="color: #FAF7F0; font-size: 11.5pt; margin: 2pt 14pt 10pt 14pt;">天辰齐翔（山东）己二腈装置达产</p>
        </div>
        <p style="color: #6B7280; font-size: 10.5pt; margin-top: 8pt;">来源：科技日报</p>
      </div>
    </div>''')

# ---------- P11 稀土（三大数字卡 + 两栏 + 应用行 + 图） ----------
def bignum_card(num, label):
    return f'''      <div style="width: 200pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; display: flex; flex-direction: column; align-items: center; box-shadow: 2px 2px 8px rgba(0,0,0,0.08);">
        <p style="color: #B45309; font-size: 26pt; font-weight: bold; margin-top: 8pt;">{num}</p>
        <p style="color: #6B7280; font-size: 11.5pt; margin: 2pt 8pt 9pt 8pt; text-align: center;">{label}</p>
      </div>'''

PAGES['11-rare-earth'] = light_page(11, '为什么学', 'LuGem', '化学×战略资源：稀土', f'''    <div style="display: flex; justify-content: space-between; margin-top: 2pt;">
{bignum_card('36%', '储量全球第一（约，2024）')}
{bignum_card('60%+', '开采量占全球比例')}
{bignum_card('90%', '精炼产能约占全球')}
    </div>
    <div style="display: flex; margin-top: 14pt;">
      <div style="width: 312pt;">
        <p style="color: #1B4332; font-size: 14.5pt; font-weight: bold;">是什么</p>
        <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.45; margin-top: 6pt; width: 300pt;">17 种金属元素（镧系 15 种 + 钪、钇）；不是「土」，也不算稀有——难在性质太相似，互相分离极难</p>
        <img src="../images/card-rare-earth.png" style="width: 195pt; height: 112pt; margin-top: 10pt;">
      </div>
      <div style="width: 312pt; margin-left: 16pt;">
        <p style="color: #1B4332; font-size: 14.5pt; font-weight: bold;">徐光宪</p>
        <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.45; margin-top: 6pt; width: 300pt;">上世纪 70 年代建立串级萃取理论，像接力赛一样把稀土「兄弟」逐个分开，2008 年获国家最高科学技术奖</p>
        <div style="margin-top: 12pt; background: #E3EDE6; border-radius: 5pt;">
          <p style="color: #1B4332; font-size: 13pt; text-align: center; margin: 8pt 10pt;">应用：手机振动马达 · 新能源车电机 · 风力发电 · 光刻机玻璃</p>
        </div>
      </div>
    </div>
    <p style="color: #6B7280; font-size: 10.5pt; margin-top: 12pt;">来源：知识库 / 公开报道</p>''')

# ---------- P12 健康与安全（三元素卡 + 砖红警示块含方程式） ----------
def elem_card(name, role, desc):
    return f'''      <div style="width: 200pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; box-shadow: 2px 2px 8px rgba(0,0,0,0.08);">
        <div style="margin: 12pt 14pt 0 14pt;">
          <p style="color: #1B4332; font-size: 15pt; font-weight: bold;">{name}</p>
          <p style="color: #2D6A4F; font-size: 12pt; font-weight: bold; margin-top: 2pt;">{role}</p>
          <p style="color: #6B7280; font-size: 11.5pt; line-height: 1.4; margin-top: 6pt; margin-bottom: 12pt;">{desc}</p>
        </div>
      </div>'''

PAGES['12-safety'] = light_page(12, '为什么学', 'LuHeartPulse', '健康与安全', f'''    <div style="display: flex; justify-content: space-between; margin-top: 8pt;">
{elem_card('铁', '血红蛋白的核心成分', '缺铁容易贫血、疲劳；红肉、动物肝脏、菠菜能补')}
{elem_card('碘', '甲状腺激素的原料', '缺碘会让甲状腺肿大；加碘盐就是为这个设计的')}
{elem_card('钙', '骨骼和牙齿的主要成分', '长身体的关键期，奶、豆制品要跟上')}
    </div>
    <div style="margin-top: 14pt; background: #FBEAE8; border: 1.5pt solid #C0392B; border-radius: 6pt;">
      <div style="display: flex; align-items: center; margin-top: 10pt;">
        <img src="../../icons/LuTriangleAlert-C0392B.png" style="width: 17pt; height: 17pt; margin-left: 12pt;">
        <p style="color: #C0392B; font-size: 15pt; font-weight: bold; margin-left: 8pt; width: 580pt;">84 消毒液 + 洁厕灵 = 有毒氯气</p>
      </div>
      <p style="color: #1B4332; font-size: 13.5pt; font-weight: bold; margin: 6pt 14pt 0 14pt;">NaClO + 2HCl ═ NaCl + H₂O + Cl₂↑</p>
      <p style="color: #1F2937; font-size: 12pt; line-height: 1.45; margin: 6pt 14pt;">84 含次氯酸钠（NaClO），洁厕灵含盐酸（HCl）——混用放出黄绿色、刺鼻的氯气，吸入会灼伤呼吸道。</p>
      <p style="color: #C0392B; font-size: 12pt; font-weight: bold; margin: 0 14pt 10pt 14pt;">记住两条：清洁剂绝不混用；闻到刺鼻气味，立刻开窗、离开现场</p>
    </div>''')

# ---------- P13 化学也很美（三图 contain） ----------
def beauty_card(img, caption_html):
    return f'''      <div style="width: 200pt;">
        <img src="../images/{img}" style="width: 200pt; height: 180pt;">
        <p style="color: #1F2937; font-size: 12pt; line-height: 1.4; margin-top: 8pt; width: 196pt;">{caption_html}</p>
      </div>'''

PAGES['13-beauty'] = light_page(13, '为什么学', 'LuSparkles', '化学也很美', f'''    <div style="display: flex; justify-content: space-between; margin-top: 6pt;">
{beauty_card('card-flame.png', '<span style="font-weight: bold; color: #1B4332;">焰色反应</span>：每种金属烧出专属颜色，节日的烟花就靠这个原理')}
{beauty_card('card-tyndall.png', '<span style="font-weight: bold; color: #1B4332;">丁达尔效应</span>：阳光穿过林间雾气，光柱清晰可见——本质是光被胶体微粒散射')}
{beauty_card('card-garden.png', '<span style="font-weight: bold; color: #1B4332;">水中花园</span>：金属盐在硅酸钠溶液里，慢慢长出「石头花」')}
    </div>
{bottom_line('这些现象背后的原理，高中三年都会一一学到', top=278)}''')

# ---------- P14 小结：为什么学化学（四领域卡 + 金句） ----------
def field_card(name, desc):
    return f'''      <div style="width: 148pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; box-shadow: 2px 2px 8px rgba(0,0,0,0.08);">
        <div style="background: #2D6A4F; border-radius: 7pt 7pt 0 0; display: flex; justify-content: center;">
          <p style="color: #FAF7F0; font-size: 14pt; font-weight: bold; margin: 5pt 0;">{name}</p>
        </div>
        <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.4; text-align: center; margin: 10pt 10pt 12pt 10pt;">{desc}</p>
      </div>'''

PAGES['14-summary'] = light_page(14, '为什么学', 'LuKeyRound', '小结：为什么学化学', f'''    <div style="display: flex; justify-content: space-between; margin-top: 22pt;">
{field_card('农业', '化肥与农药，养活更多人')}
{field_card('医学', '新药从实验室走向病房')}
{field_card('材料', '从尼龙面料到芯片')}
{field_card('生活', '柴米油盐里都有学问')}
    </div>
    <div style="display: flex; flex-direction: column; align-items: center; margin-top: 42pt;">
      <p style="color: #1B4332; font-size: 32pt; font-weight: bold;">化学，处处交叉</p>
      <p style="color: #B45309; font-size: 16pt; font-weight: bold; margin-top: 12pt; width: 620pt; text-align: center;">化肥养人 · 药物治病 · 材料强国 · 生活更美</p>
      <div style="background: #E8A33D; width: 56pt; height: 4pt; margin-top: 16pt;"></div>
    </div>''')

# ---------- P15 初中盘点（三卡） ----------
def junior_card(icon, title, sub, desc):
    return f'''      <div style="width: 200pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; box-shadow: 2px 2px 8px rgba(0,0,0,0.10);">
        <div style="display: flex; align-items: center; margin: 14pt 14pt 0 14pt;">
          <img src="../../icons/{icon}-1B4332.png" style="width: 18pt; height: 18pt;">
          <p style="color: #1B4332; font-size: 15pt; font-weight: bold; margin-left: 8pt;">{title}</p>
        </div>
        <p style="color: #2D6A4F; font-size: 11.5pt; font-weight: bold; margin: 4pt 14pt 0 14pt;">{sub}</p>
        <p style="color: #6B7280; font-size: 12pt; line-height: 1.4; margin: 6pt 14pt 14pt 14pt;">{desc}</p>
      </div>'''

PAGES['15-junior'] = light_page(15, '初高中过渡', 'LuBookOpen', '初中盘点', f'''    <div style="display: flex; justify-content: space-between; margin-top: 26pt;">
{junior_card('LuFlame', '氧气', '性质 · 制法 · 检验', '还记得吗？带火星的木条伸进去，会复燃')}
{junior_card('LuTestTubes', '酸碱盐', '指示剂 · 中和反应', '紫色石蕊试液：遇酸变红，遇碱变蓝')}
{junior_card('LuPenLine', '化学方程式', '书写 · 配平 · 计算', '配平的依据，是质量守恒定律')}
    </div>
{bottom_line('高中化学，是站在这些基础上的')}''')

# ---------- P16 变化①：内容（对比表含方程式） ----------
def tcell(w, text, bg='#FFFFFF', color='#1F2937', bold=False, border='#C9D6CC', size=12.5, align='center'):
    b = ' font-weight: bold;' if bold else ''
    return (f'      <div style="width: {w}pt; background: {bg}; border: 1pt solid {border}; display: flex; align-items: center; justify-content: center;">'
            f'<p style="color: {color}; font-size: {size}pt;{b} line-height: 1.4; margin: 8pt 8pt; text-align: {align}; width: {w - 16}pt;">{text}</p></div>')

def hcell(w, text):
    return (f'      <div style="width: {w}pt; background: #1B4332; border: 1pt solid #1B4332; display: flex; align-items: center; justify-content: center;">'
            f'<p style="color: #FAF7F0; font-size: 14pt; font-weight: bold; margin: 7pt 0; text-align: center; width: {w - 12}pt;">{text}</p></div>')

PAGES['16-content'] = light_page(16, '初高中过渡', 'LuTable', '变化①：内容——从「认识」到「讲理」', f'''    <div style="margin-top: 12pt;">
      <div style="display: flex;">
{hcell(110, '')}
{hcell(265, '初中 · 多靠记忆')}
{hcell(265, '高中 · 重在逻辑推理')}
      </div>
      <div style="display: flex;">
{tcell(110, '氧气', bold=True, color='#1B4332')}
{tcell(265, '记住性质和制法：2H₂O₂ ═ 2H₂O + O₂↑（MnO₂ 催化）', size=11.5, align='left')}
{tcell(265, '追问为什么：2H₂O₂ ═ 2H₂O + O₂↑——MnO₂ 为什么能加快？', bg='#FBF0DA', color='#1B4332', border='#E8D9B8', align='left')}
      </div>
      <div style="display: flex;">
{tcell(110, '化学方程式', bold=True, color='#1B4332')}
{tcell(265, '背下来、会配平：3Fe + 2O₂ ═ Fe₃O₄（点燃）', size=11.5, align='left')}
{tcell(265, '同一个方程式还要算「量」：3Fe + 2O₂ ═ Fe₃O₄——系数 3∶2∶1，就是物质的量之比，能算出要多少铁、生成多少产物', bg='#FBF0DA', color='#1B4332', border='#E8D9B8', align='left')}
      </div>
      <div style="display: flex;">
{tcell(110, '实验', bold=True, color='#1B4332')}
{tcell(265, '看现象、记结论')}
{tcell(265, '用证据推出结论', bg='#FBF0DA', color='#1B4332', border='#E8D9B8')}
      </div>
    </div>
{bottom_line('衔接研究共识：初中多靠记忆，高中重在逻辑推理', top=274)}''')

# ---------- P17 变化②：思维 ----------
PAGES['17-thinking'] = light_page(17, '初高中过渡', 'LuAtom', '变化②：思维——宏观辨识与微观探析', f'''    <div style="display: flex; justify-content: space-between; margin-top: 10pt;">
      <div style="width: 305pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; box-shadow: 2px 2px 8px rgba(0,0,0,0.08);">
        <div style="background: #2D6A4F; height: 36pt; border-radius: 7pt 7pt 0 0; display: flex; align-items: center; justify-content: center;">
          <img src="../../icons/LuEye-FFFFFF.png" style="width: 14pt; height: 14pt;">
          <p style="color: #FFFFFF; font-size: 15pt; font-weight: bold; margin-left: 7pt;">初中：看现象</p>
        </div>
        <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.5; margin: 14pt 16pt 16pt 16pt;">带火星的木条伸进集气瓶——复燃了，说明是氧气</p>
        <p style="color: #1B4332; font-size: 14pt; font-weight: bold; margin: 0 16pt;">C + O₂ ═ CO₂（点燃）</p>
        <p style="color: #6B7280; font-size: 13pt; margin: 8pt 16pt 14pt 16pt;">看到什么，记住什么</p>
      </div>
      <div style="width: 305pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; box-shadow: 2px 2px 8px rgba(0,0,0,0.08);">
        <div style="background: #1B4332; height: 36pt; border-radius: 7pt 7pt 0 0; display: flex; align-items: center; justify-content: center;">
          <img src="../../icons/LuAtom-FFFFFF.png" style="width: 14pt; height: 14pt;">
          <p style="color: #FFFFFF; font-size: 15pt; font-weight: bold; margin-left: 7pt;">高中：探微观</p>
        </div>
        <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.5; margin: 14pt 16pt 0 16pt;">氧分子 O₂ 在反应中发生了什么？原子怎么重新组合？</p>
        <p style="color: #1B4332; font-size: 13.5pt; font-weight: bold; margin: 8pt 16pt 0 16pt;">旧键断裂 → 新键形成，放出能量</p>
        <p style="color: #6B7280; font-size: 13pt; margin: 8pt 16pt 14pt 16pt;">现象背后，追问微粒层面的原因</p>
      </div>
    </div>
    <p style="color: #6B7280; font-size: 11pt; text-align: center; margin-top: 18pt; width: 640pt;">高中课标核心素养：<span style="font-weight: bold; color: #2D6A4F;">宏观辨识与微观探析</span>　《普通高中化学课程标准（2017 年版 2020 年修订）》</p>''')

# ---------- P18 变化③：方法（流程 + 模型卡） ----------
def flow_node(title, sub):
    return f'''        <div style="width: 180pt; background: #FFFFFF; border: 2pt solid #2D6A4F; border-radius: 8pt;">
          <p style="color: #1B4332; font-size: 16pt; font-weight: bold; text-align: center; margin-top: 10pt;">{title}</p>
          <p style="color: #6B7280; font-size: 12pt; text-align: center; margin: 4pt 10pt 12pt 10pt;">{sub}</p>
        </div>'''

ARROW = '''        <div style="width: 46pt; display: flex; align-items: center; justify-content: center;">
          <p style="color: #E8A33D; font-size: 24pt; font-weight: bold;">→</p>
        </div>'''

PAGES['18-method'] = light_page(18, '初高中过渡', 'LuBrain', '变化③：方法——证据推理与模型认知', f'''    <div style="display: flex; justify-content: center; margin-top: 22pt;">
{flow_node('证据', '实验现象、数据')}
{ARROW}
{flow_node('推理', '分析、比较、论证')}
{ARROW}
{flow_node('结论', '站得住脚的判断')}
    </div>
    <div style="margin: 20pt 100pt 0 100pt; background: #E3EDE6; border: 1pt solid #B7CDBF; border-radius: 8pt;">
      <p style="color: #1F2937; font-size: 14pt; line-height: 1.5; text-align: center; margin: 14pt 20pt;"><span style="font-weight: bold; color: #1B4332;">模型认知</span>：用模型把看不见的微观世界「画」出来，比如用球棍模型表示分子</p>
    </div>
    <p style="color: #6B7280; font-size: 11pt; text-align: center; margin-top: 20pt; width: 640pt;">高中课标核心素养：<span style="font-weight: bold; color: #2D6A4F;">证据推理与模型认知</span>　《普通高中化学课程标准（2017 年版 2020 年修订）》</p>''')

# ---------- P19 三个「掉队」陷阱（陷阱 + 破解） ----------
def trap_card(title, trap, fix):
    return f'''      <div style="width: 200pt; background: #FBEAE8; border: 1.5pt solid #C0392B; border-radius: 8pt;">
        <div style="display: flex; align-items: center; justify-content: center; margin-top: 12pt;">
          <img src="../../icons/LuTriangleAlert-C0392B.png" style="width: 15pt; height: 15pt;">
          <p style="color: #C0392B; font-size: 15pt; font-weight: bold; margin-left: 7pt;">{title}</p>
        </div>
        <p style="color: #1F2937; font-size: 12pt; line-height: 1.4; text-align: center; margin: 8pt 14pt 0 14pt;">{trap}</p>
        <p style="color: #1B4332; font-size: 12pt; line-height: 1.4; margin: 10pt 14pt 14pt 14pt;"><span style="font-weight: bold;">破解：</span>{fix}</p>
      </div>'''

PAGES['19-traps'] = light_page(19, '初高中过渡', 'LuTriangleAlert', '三个「掉队」陷阱', f'''    <div style="display: flex; justify-content: space-between; margin-top: 22pt;">
{trap_card('只背不思考', '背得滚瓜烂熟，一换情境就不会', '多问一句「为什么」，把结论还原成推理过程')}
{trap_card('攒问题不问', '小问题攒成大窟窿', '当天问，当天清；问老师、问同学，问题不过夜')}
{trap_card('怕计算', '一看到数字题就想跳过', '跟着例题一步步算；计算题套路固定，动手三遍就熟')}
    </div>
{bottom_line('这三个坑避开了，高一化学就稳了一半')}''')

# ---------- P20 上课四步法 ----------
def step_col(num, word, sub, desc):
    return f'''        <div style="width: 152pt; display: flex; flex-direction: column; align-items: center;">
          <div style="background: #1B4332; width: 38pt; height: 38pt; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <p style="color: #FAF7F0; font-size: 16pt; font-weight: bold;">{num}</p>
          </div>
          <div style="width: 140pt; margin-top: 12pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 5pt;">
            <p style="color: #1B4332; font-size: 17pt; font-weight: bold; text-align: center; margin-top: 10pt;">{word}</p>
            <p style="color: #2D6A4F; font-size: 12pt; font-weight: bold; text-align: center; margin-top: 3pt;">{sub}</p>
            <p style="color: #6B7280; font-size: 11.5pt; line-height: 1.4; text-align: center; margin: 5pt 8pt 12pt 8pt;">{desc}</p>
          </div>
        </div>'''

PAGES['20-class'] = light_page(20, '怎么学好', 'LuListChecks', '上课四步法', f'''    <div style="position: relative; margin-top: 32pt;">
      <div style="position: absolute; left: 76pt; top: 18pt; width: 488pt; height: 2pt; background: #2D6A4F;"></div>
      <div style="display: flex; justify-content: space-between;">
{step_col(1, '听', '跟上思路', '耳朵跟着老师走')}
{step_col(2, '记', '记要点', '不抄板书，记关键')}
{step_col(3, '问', '不懂就问', '问题不过夜')}
{step_col(4, '练', '当堂练', '动手才算学会')}
      </div>
    </div>
{bottom_line('每节课按这四步走，课堂效率最高')}''')

# ---------- P21 两个本子 ----------
def book_card(icon, title, desc):
    return f'''      <div style="width: 305pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; box-shadow: 2px 2px 8px rgba(0,0,0,0.10);">
        <div style="background: #1B4332; height: 40pt; border-radius: 7pt 7pt 0 0; display: flex; align-items: center; justify-content: center;">
          <img src="../../icons/{icon}-FFFFFF.png" style="width: 15pt; height: 15pt;">
          <p style="color: #FFFFFF; font-size: 16pt; font-weight: bold; margin-left: 8pt;">{title}</p>
        </div>
        <p style="color: #1F2937; font-size: 14pt; line-height: 1.55; text-align: center; margin: 18pt 18pt 22pt 18pt;">{desc}</p>
      </div>'''

PAGES['21-notebooks'] = light_page(21, '怎么学好', 'LuNotebookPen', '两个本子', f'''    <div style="display: flex; justify-content: space-between; margin-top: 28pt;">
{book_card('LuNotebookPen', '笔记本', '记课堂要点——概念、方法、易错点；只记关键，不抄板书，留出动脑的余地')}
{book_card('LuPenLine', '错题本', '积累错题——错在哪、为什么错；每周翻一次，同类错误不犯第二次')}
    </div>
{bottom_line('别等到第一次考试之后，好习惯从第一节课就开始')}''')

# ---------- P22 课前预习 + 课后复习 ----------
def step3_col(num, title, sub):
    return f'''        <div style="width: 200pt; display: flex; flex-direction: column; align-items: center;">
          <div style="background: #1B4332; width: 40pt; height: 40pt; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <p style="color: #FAF7F0; font-size: 16pt; font-weight: bold;">{num}</p>
          </div>
          <div style="width: 188pt; margin-top: 12pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 5pt;">
            <p style="color: #1B4332; font-size: 15.5pt; font-weight: bold; text-align: center; margin-top: 12pt;">{title}</p>
            <p style="color: #6B7280; font-size: 12.5pt; line-height: 1.45; text-align: center; margin: 6pt 10pt 14pt 10pt;">{sub}</p>
          </div>
        </div>'''

PAGES['22-loop'] = light_page(22, '怎么学好', 'LuRefreshCw', '课前预习 + 课后复习', f'''    <div style="position: relative; margin-top: 32pt;">
      <div style="position: absolute; left: 100pt; top: 19pt; width: 440pt; height: 2pt; background: #2D6A4F;"></div>
      <div style="display: flex; justify-content: space-between;">
{step3_col(1, '课前标疑问', '花 5 分钟翻一遍，标出看不懂的地方')}
{step3_col(2, '课上带着听', '带着问题听课，重点听自己的疑问')}
{step3_col(3, '课后当天清', '当天的疑问当天解决，不拖到明天')}
      </div>
    </div>
{bottom_line('每天课前 5 分钟、课后 10 分钟，换来课堂上听得懂')}''')

# ---------- P23 心态（+ 四阶进度条） ----------
def stage(label, bg, fg):
    return (f'        <div style="width: 140pt; background: {bg}; border-radius: 6pt; display: flex; justify-content: center;">'
            f'<p style="color: {fg}; font-size: 15pt; font-weight: bold; margin: 10pt 0;">{label}</p></div>')

PAGES['23-mindset'] = light_page(23, '怎么学好', 'LuSmile', '心态', f'''    <div style="display: flex; align-items: center; justify-content: center; margin-top: 36pt;">
      <p style="color: #6B7280; font-size: 32pt;">「我不会」</p>
      <p style="color: #E8A33D; font-size: 30pt; font-weight: bold; margin: 0 22pt;">→</p>
      <p style="color: #1B4332; font-size: 36pt; font-weight: bold;">「我还没学会」</p>
    </div>
    <p style="color: #6B7280; font-size: 14pt; text-align: center; margin-top: 14pt; width: 640pt;">只差两个字，心态完全不一样</p>
    <div style="display: flex; justify-content: space-between; margin: 36pt 32pt 0 32pt;">
{stage('听懂', '#E3EDE6', '#1B4332')}
{stage('会做', '#2D6A4F', '#FAF7F0')}
{stage('做对', '#1B4332', '#FAF7F0')}
{stage('熟练', '#E8A33D', '#1B4332')}
    </div>
    <p style="color: #1B4332; font-size: 14pt; font-weight: bold; text-align: center; margin-top: 18pt; width: 640pt;">学会，只是时间问题</p>''')

# ---------- P24 寄语 ----------
def word_card(icon, word, desc):
    return f'''      <div style="width: 200pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; display: flex; flex-direction: column; align-items: center; box-shadow: 2px 2px 8px rgba(0,0,0,0.12);">
        <div style="background: #2D6A4F; width: 48pt; height: 48pt; border-radius: 50%; margin-top: 18pt; display: flex; align-items: center; justify-content: center;">
          <img src="../../icons/{icon}-FFFFFF.png" style="width: 22pt; height: 22pt;">
        </div>
        <p style="color: #1B4332; font-size: 22pt; font-weight: bold; margin-top: 10pt;">{word}</p>
        <p style="color: #6B7280; font-size: 12.5pt; line-height: 1.45; text-align: center; margin: 8pt 14pt 18pt 14pt;">{desc}</p>
      </div>'''

PAGES['24-words'] = light_page(24, '结尾', 'LuGraduationCap', '寄语', f'''    <div style="display: flex; justify-content: space-between; margin-top: 28pt;">
{word_card('LuEye', '看见', '奶茶、烟花、铁生锈——生活处处是课堂')}
{word_card('LuSearch', '追问', '不停在「是什么」，多问一层「为什么」')}
{word_card('LuTarget', '坚持', '每天弄懂一个小点，一学期就是一大步')}
    </div>''')

# ---------- P25 课后任务 + 答疑（必做 + 二选一） ----------
PAGES['25-homework'] = light_page(25, '结尾', 'LuMail', '课后任务 + 答疑', f'''    <div style="display: flex; margin-top: 8pt;">
      <div style="width: 408pt;">
        <div style="background: #FBF0DA; border: 1.5pt solid #E8A33D; border-radius: 6pt;">
          <p style="color: #1F2937; font-size: 14pt; line-height: 1.45; margin: 10pt 14pt;"><span style="font-weight: bold; color: #B45309;">【必做】准备两个本子</span>：笔记本 + 错题本，下节课带来</p>
        </div>
        <div style="background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 6pt; margin-top: 10pt;">
          <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.45; margin: 10pt 14pt;"><span style="font-weight: bold; color: #1B4332;">选做一：找一个生活里的化学现象</span>——拍下来或记下来，下节课分享（比如：切开的苹果为什么会变黄？铁锅为什么会生锈？）</p>
        </div>
        <div style="background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 6pt; margin-top: 10pt;">
          <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.45; margin: 10pt 14pt;"><span style="font-weight: bold; color: #1B4332;">选做二：翻翻课本目录</span>——标出你最好奇的一节</p>
        </div>
      </div>
      <div style="width: 208pt; margin-left: 24pt; background: #E3EDE6; border: 1pt solid #B7CDBF; border-radius: 8pt;">
        <p style="color: #1B4332; font-size: 15pt; font-weight: bold; text-align: center; margin-top: 14pt;">答疑</p>
        <p style="color: #1F2937; font-size: 13pt; text-align: center; margin-top: 10pt;">有问必答</p>
        <p style="color: #1F2937; font-size: 13pt; text-align: center; margin-top: 6pt;">联系方式：___</p>
        <p style="color: #6B7280; font-size: 12pt; line-height: 1.45; text-align: center; margin: 12pt 14pt 14pt 14pt;">问题不过夜，是学好化学最快的路</p>
      </div>
    </div>
    <p style="color: #1B4332; font-size: 18pt; font-weight: bold; text-align: center; margin-top: 18pt; width: 640pt;">下节课见</p>''')

# ---------- 写文件 ----------
ORDER = ['01-cover', '02-daily', '03-agri', '04-what', '05-three', '06-table-story', '07-nobel',
         '08-central', '09-medicine', '10-material', '11-rare-earth', '12-safety', '13-beauty',
         '14-summary', '15-junior', '16-content', '17-thinking', '18-method', '19-traps',
         '20-class', '21-notebooks', '22-loop', '23-mindset', '24-words', '25-homework']

for name in ORDER:
    (OUT / f'{name}.html').write_text(PAGES[name], encoding='utf-8')
print('wrote', len(ORDER), 'slides')
