# -*- coding: utf-8 -*-
"""物质的分类 30 页 slides/*.html 生成器 v2（逐字搬运源课件，只套模板外壳）。
文字逐字取自 source-fenlei-text.txt，仅修三处笔误（P13 2NaO→2NaOH、
P6 标淮→标准、P9 对进同一事物行→对同一事物进行）+ P1 删除错误章节名；
化学式转 Unicode 下标。备注在 build.js。"""
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

DARK_HEAD = HEAD.replace('#FAF7F0', '#1B4332')

TOTAL = 30


def hdr(part, icon, title, size=24):
    return f'''  <div style="margin: 16pt 40pt 0 40pt; width: 640pt; min-height: 34pt; display: flex; align-items: center;">
    <img src="../../icons/{icon}-1B4332.png" style="width: 16pt; height: 16pt;">
    <div style="background: #E8A33D; border-radius: 3pt; margin-left: 8pt; display: flex; justify-content: center;">
      <p style="color: #FFFFFF; font-size: 10pt; font-weight: bold; margin: 2.5pt 7pt;">{part}</p>
    </div>
    <h1 style="color: #1B4332; font-size: {size}pt; font-weight: bold; margin-left: 12pt; width: 470pt; line-height: 1.3;">{title}</h1>
  </div>
  <div style="position: relative; margin: 4pt 40pt 0 40pt; width: 640pt; height: 2.5pt;">
    <div style="position: absolute; left: 0; top: 0.75pt; width: 640pt; height: 1pt; background: #DDE5DD;"></div>
    <div style="position: absolute; left: 0; top: 0; width: 44pt; height: 2.5pt; background: #E8A33D;"></div>
  </div>'''


def light_page(n, part, icon, title, body, tsize=24):
    i = n - 2
    h = round(405 * (0.06 + i * 0.84 / (TOTAL - 2)))
    top = 405 - h
    return HEAD + f'''<body>
  <div style="position: absolute; left: 0; top: 0; width: 8pt; height: 405pt; background: #1B4332;"></div>
  <div style="position: absolute; left: 0; top: {top}pt; width: 8pt; height: {h}pt; background: #E8A33D;"></div>
  <img src="../../icons/hex-corner.png" style="position: absolute; right: 0; top: 0; width: 180pt; height: 150pt;">
{hdr(part, icon, title, tsize)}
  <div style="position: relative; margin: 10pt 40pt 0 40pt; width: 640pt; flex: 1;">
{body}
  </div>
  <div style="position: absolute; left: 40pt; top: 384pt; width: 640pt; height: 1pt; background: #DDE5DD;"></div>
  <p style="position: absolute; right: 40pt; top: 388pt; width: 80pt; text-align: right; color: #6B7280; font-size: 10pt;">{n} / {TOTAL}</p>
</body>
</html>
'''


def tcell(w, text, bg='#FFFFFF', color='#1F2937', bold=False, border='#C9D6CC', size=12, align='center'):
    b = ' font-weight: bold;' if bold else ''
    return (f'      <div style="width: {w}pt; background: {bg}; border: 1pt solid {border}; display: flex; align-items: center; justify-content: center;">'
            f'<p style="color: {color}; font-size: {size}pt;{b} line-height: 1.4; margin: 6pt 6pt; text-align: {align}; width: {w - 12}pt;">{text}</p></div>')


def hcell(w, text, size=13):
    return (f'      <div style="width: {w}pt; background: #1B4332; border: 1pt solid #1B4332; display: flex; align-items: center; justify-content: center;">'
            f'<p style="color: #FAF7F0; font-size: {size}pt; font-weight: bold; margin: 6pt 4pt; text-align: center; width: {w - 10}pt;">{text}</p></div>')


def answer_card(ans):
    return (f'        <div style="background: #E8A33D; border-radius: 6pt; width: 132pt; display: flex; justify-content: center; align-items: center;">'
            f'<p style="color: #1B4332; font-size: 14pt; font-weight: bold; margin: 6pt 8pt; width: 116pt; text-align: center;">答案：{ans}</p></div>')


def exam_q(text, size=13):
    return f'''    <div style="background: #FFFFFF; border: 1pt solid #DDD6C8; border-left: 5pt solid #1B4332; border-radius: 4pt;">
      <p style="color: #1F2937; font-size: {size}pt; line-height: 1.5; margin: 9pt 14pt;">{text}</p>
    </div>'''


def explain(text, mt=8, size=11.5):
    return f'''    <div style="margin-top: {mt}pt; background: #E3EDE6; border-radius: 5pt;">
      <p style="color: #1F2937; font-size: {size}pt; line-height: 1.5; margin: 8pt 14pt;">{text}</p>
    </div>'''


PAGES = {}

# ---------- P1 封面（深色；删源文件误入的「第一章 化学反应的热效应」） ----------
PAGES['01-cover'] = DARK_HEAD + '''<body>
  <div style="width: 720pt; height: 6pt; background: #E8A33D;"></div>
  <div style="display: flex; flex: 1; width: 720pt;">
    <div style="width: 430pt; margin-left: 40pt;">
      <div style="background: #E8A33D; width: 96pt; border-radius: 3pt; margin-top: 66pt; display: flex; justify-content: center;">
        <p style="color: #FFFFFF; font-size: 12pt; font-weight: bold; margin: 4pt 0;">必修第一册</p>
      </div>
      <p style="color: #9DB8A9; font-size: 13pt; margin-top: 22pt;">第一章 物质及其变化</p>
      <p style="color: #E3EDE6; font-size: 16pt; margin-top: 8pt;">第一节 物质的分类及转化</p>
      <h1 style="color: #FAF7F0; font-size: 40pt; font-weight: bold; margin-top: 14pt;">第1课时 物质的分类</h1>
      <div style="background: #E8A33D; width: 56pt; height: 4pt; margin-top: 16pt;"></div>
      <p style="color: #9DB8A9; font-size: 12pt; margin-top: 26pt;">本节重点　简单的分类方法及其物质的分类</p>
    </div>
    <div style="position: relative; width: 250pt;">
      <img src="../../icons/cell-C-92.png" style="position: absolute; left: 6pt; top: 216pt; width: 138pt; height: 138pt;">
      <img src="../../icons/cell-Na-88.png" style="position: absolute; left: 119pt; top: 224pt; width: 132pt; height: 132pt;">
      <img src="../../icons/cell-H-104.png" style="position: absolute; left: 42pt; top: 87pt; width: 156pt; height: 156pt;">
      <img src="../../icons/cell-O-96.png" style="position: absolute; left: 102pt; top: 23pt; width: 144pt; height: 144pt;">
    </div>
  </div>
  <div style="width: 720pt; height: 5pt; background: #2D6A4F;"></div>
  <p style="position: absolute; right: 40pt; top: 382pt; width: 80pt; text-align: right; color: rgba(250,247,240,0.6); font-size: 10pt;">1 / 30</p>
</body>
</html>
'''

# ---------- P2 情境导入（图书馆源图 + 原文） ----------
PAGES['02-scene'] = light_page(2, '情境导入', 'LuLightbulb', '为什么要分类？', f'''    <div style="display: flex; margin-top: 2pt;">
      <div style="width: 300pt;">
        <img src="../images/card-library.png" style="width: 300pt; height: 177pt;">
        <p style="color: #6B7280; font-size: 10.5pt; text-align: center; margin-top: 4pt; width: 300pt;">国家图书馆（亚洲规模最大的图书馆）</p>
      </div>
      <div style="width: 316pt; margin-left: 24pt;">
        <p style="color: #1F2937; font-size: 13pt; line-height: 1.55; width: 316pt;">图书馆里有那么多的书籍，为什么你能很快就找到你需要的书？</p>
        <p style="color: #1F2937; font-size: 13pt; line-height: 1.55; margin-top: 10pt; width: 316pt;">超市里有那么多的商品，为什么你能很快就找到你要买的零食呢？</p>
      </div>
    </div>
    <div style="margin-top: 14pt; background: #FBF0DA; border-left: 5pt solid #E8A33D; border-radius: 3pt;">
      <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.6; margin: 10pt 14pt;">图书馆中数不胜数的图书要分类陈列以便于人们查找，快递企业对数以千万计的物品要分类处理以提高工作效率。同样，为了认识和研究的方便，对于数以千万计的物质，人们常根据物质的<span style="font-weight: bold; color: #B45309;">组成、结构、性质或用途</span>等进行分类。</p>
    </div>''')

# ---------- P3 分类法应用广泛（五图源图） ----------
def mini_photo(img, caption):
    return f'''      <div style="width: 120pt; display: flex; flex-direction: column; align-items: center;">
        <img src="../images/{img}" style="width: 112pt; height: 84pt;">
        <p style="color: #1F2937; font-size: 11.5pt; text-align: center; margin-top: 7pt; width: 118pt;">{caption}</p>
      </div>'''

PAGES['03-everywhere'] = light_page(3, '情境导入', 'LuLayoutGrid', '分类法在实际生产生活中的应用广泛', f'''    <div style="display: flex; justify-content: space-between; margin-top: 30pt;">
{mini_photo('card-p3-library.png', '图书馆中陈列书籍')}
{mini_photo('card-p3-market.png', '超市里摆放货品')}
{mini_photo('card-p3-lab.png', '实验室里码放药品')}
{mini_photo('card-p3-parcel.png', '物流公司分拣快递')}
{mini_photo('card-p3-recycle.png', '垃圾分类')}
    </div>''')

# ---------- P4 啥叫分类 ----------
PAGES['04-what'] = light_page(4, '情境导入', 'LuBookOpen', '啥叫分类？', f'''    <div style="display: flex; align-items: center; margin-top: 40pt;">
      <p style="color: #1B4332; font-size: 22pt; font-weight: bold; margin-left: 20pt;">分类：</p>
    </div>
    <div style="margin: 20pt 20pt 0 20pt; background: #FBF0DA; border-left: 5pt solid #E8A33D; border-radius: 4pt;">
      <p style="color: #1F2937; font-size: 19pt; line-height: 1.7; margin: 20pt 24pt;">根据研究对象的<span style="font-weight: bold; color: #B45309;">共同点</span>和<span style="font-weight: bold; color: #B45309;">差异点</span>，将它们区分为不同种类和层次的科学方法。</p>
    </div>''')

# ---------- P5 阅读材料（原文整段） ----------
PAGES['05-elements'] = light_page(5, '主题 1 · 分类标准与方法', 'LuFlaskConical', '【阅读材料】有限的元素组成了种类繁多的物质', f'''    <p style="color: #1F2937; font-size: 13pt; line-height: 1.75; margin-top: 8pt; width: 620pt; text-align: justify;">氢是元素周期表中原子序数为1的元素，含氢元素的物质有 H₂、H₂O、H₂SO₄ 等。碳是组成生物体的主要元素之一，金刚石、石墨、C₆₀、温室气体之一的CO₂中都有碳元素的身影。Na是一种活泼的金属，生理盐水中的 NaCl溶液、碱面里的 Na₂CO₃、管道疏通剂的有效成分 NaOH 中都含有钠元素。钙是生长发育所必需的元素，自热米饭发热包中的 CaO、用来杀菌除虫的波尔多液[由 Ca(OH)₂ 和 CuSO₄ 配制而成]、大理石的主要成分 CaCO₃ 都含有钙元素。钡是生产绿色烟花必须添加的一种元素，用X射线检查肠胃病时病人服用的 BaSO₄浊液（俗称钡餐）当中也含有钡元素。</p>''', tsize=18)

# ---------- P6 如何分类（清单 + 原文段落） ----------
PAGES['06-think'] = light_page(6, '主题 1 · 分类标准与方法', 'LuSearch', '如何对短文中划线的物质进行分类？', f'''    <div style="margin-top: 4pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt;">
      <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.7; margin: 10pt 14pt 12pt 14pt;">H₂、H₂O、H₂SO₄、金刚石、石墨、C₆₀、CO₂、Na、NaCl溶液、Na₂CO₃、NaOH、CaO、Ca(OH)₂、CuSO₄、CaCO₃、BaSO₄浊液</p>
    </div>
    <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.7; margin-top: 18pt; width: 620pt; text-align: justify;">分类有一定的<span style="font-weight: bold; color: #B45309;">标准</span>，根据不同的标准，人们对研究对象进行不同的分类。在高中化学的学习中，对物质及其变化的分类标准将从物质的<span style="font-weight: bold; color: #1B4332;">组成和性质</span>等宏观视角，拓展到物质的<span style="font-weight: bold; color: #1B4332;">构成、结构和参加化学反应的粒子</span>等微观视角。</p>''')

# ---------- P7 树状分类法（概念 + 源形状图裁切） ----------
PAGES['07-tree'] = light_page(7, '主题 1 · 分类标准与方法', 'LuNetwork', '分类法一　树状分类法', f'''    <div style="margin-top: 2pt; background: #FBF0DA; border-left: 5pt solid #E8A33D; border-radius: 4pt;">
      <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.55; margin: 8pt 14pt;"><span style="font-weight: bold; color: #B45309;">概念</span>　对同一类事物按照属性进一步进行细化分类的方法，分级，递进，每一级一个分类标准</p>
    </div>
    <div style="display: flex; justify-content: center; margin-top: 8pt;">
      <img src="../images-src/p07-tree.png" style="width: 620pt; height: 168pt;">
    </div>
    <div style="margin-top: 10pt; background: #E3EDE6; border-radius: 5pt;">
      <p style="color: #1B4332; font-size: 12.5pt; margin: 8pt 14pt;"><span style="font-weight: bold;">特点</span>　同一层级的物质为并列关系　｜　上下层级的物质为包含关系</p>
    </div>''')

# ---------- P8 树状分类举例（源图 + 例子标注行） ----------
PAGES['08-tree-big'] = light_page(8, '主题 1 · 分类标准与方法', 'LuNetwork', '树状分类法举例：按物质的组成分类', f'''    <div style="display: flex; justify-content: center; margin-top: 2pt;">
      <img src="../images-src/p08-img1.png" style="width: 620pt; height: 236pt;">
    </div>
    <div style="margin-top: 8pt; background: #E3EDE6; border-radius: 5pt;">
      <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.55; margin: 8pt 14pt;"><span style="font-weight: bold; color: #1B4332;">混合物</span>：NaCl溶液、BaSO₄浊液　<span style="font-weight: bold; color: #1B4332;">氧化物</span>：H₂O、CO₂、CaO　<span style="font-weight: bold; color: #1B4332;">酸</span>：H₂SO₄　<span style="font-weight: bold; color: #1B4332;">碱</span>：NaOH、Ca(OH)₂　<span style="font-weight: bold; color: #1B4332;">盐</span>：Na₂CO₃、CuSO₄、CaCO₃</p>
    </div>''')

# ---------- P9 交叉分类法（概念 + 源连线图） ----------
PAGES['09-cross'] = light_page(9, '主题 1 · 分类标准与方法', 'LuLayoutGrid', '分类法二　交叉分类法', f'''    <div style="display: flex; margin-top: 6pt;">
      <div style="width: 340pt;">
        <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.6; width: 330pt;"><span style="font-weight: bold; color: #B45309;">概念</span>　根据不同的分类标准，对同一事物进行多种分类的一种分类方法</p>
        <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.6; margin-top: 12pt; width: 330pt;"><span style="font-weight: bold; color: #1B4332;">特点</span>　对一种事物用两种及以上标准分类，物质类别间有相交叉的部分</p>
        <p style="color: #6B7280; font-size: 12pt; line-height: 1.55; margin-top: 12pt; width: 330pt;">基于物质的组成、结构、性质、用途等多角度分类</p>
        <p style="color: #6B7280; font-size: 12pt; line-height: 1.55; margin-top: 8pt; width: 330pt;">根据组成的阳离子分类　｜　根据组成的阴离子分类</p>
      </div>
      <div style="margin-left: 24pt; display: flex; flex-direction: column; align-items: center;">
        <img src="../images-src/p09-img1.png" style="width: 246pt; height: 213pt;">
        <p style="color: #6B7280; font-size: 10.5pt; margin-top: 4pt;">示例：交叉分类法举例</p>
      </div>
    </div>''')

# ---------- P10 思考1：单质分类（原文文字） ----------
PAGES['10-element'] = light_page(10, '主题 1 · 分类标准与方法', 'LuAtom', '【思考1】利用树状分类法对单质进行分类，可以怎样分类？并举例说明。', f'''    <div style="margin-top: 18pt; background: #FBF0DA; border-left: 5pt solid #E8A33D; border-radius: 4pt;">
      <p style="color: #1F2937; font-size: 15pt; margin: 12pt 16pt;"><span style="font-weight: bold; color: #B45309;">单质</span></p>
      <p style="color: #1F2937; font-size: 14pt; line-height: 1.6; margin: 0 16pt 12pt 16pt;">（1）定义：由同种元素组成的纯净物（同种元素可能会组成不同的单质）</p>
    </div>
    <div style="margin-top: 16pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt;">
      <p style="color: #1F2937; font-size: 14pt; margin: 12pt 16pt 0 16pt;"><span style="font-weight: bold; color: #1B4332;">（2）同素异形体</span></p>
      <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.6; margin: 6pt 16pt 12pt 16pt;">形成方式　①原子个数不同　②原子排列方式不同</p>
    </div>''', tsize=15)

# ---------- P11 同素异形体（原文 + 源 gif） ----------
def kv_line(k, v):
    return f'''        <p style="color: #1F2937; font-size: 13.5pt; line-height: 1.6; margin-top: 8pt; width: 430pt;"><span style="font-weight: bold; color: #1B4332;">{k}</span>　{v}</p>'''

PAGES['11-allotrope'] = light_page(11, '主题 1 · 分类标准与方法', 'LuGem', '（2）同素异形体', f'''    <div style="display: flex; margin-top: 4pt;">
      <div style="width: 440pt;">
{kv_line('定义', '同种元素组成不同的单质')}
{kv_line('形成方式', '①原子个数不同　②原子排列方式不同')}
{kv_line('性质差异', '主要体现在物理性质上')}
{kv_line('相互转化', '属于化学变化')}
{kv_line('常见同素异形体', '①金刚石、石墨和C₆₀　②O₂和O₃　③P（红磷）和P₄（白磷）')}
      </div>
      <div style="width: 184pt; margin-left: 16pt; display: flex; flex-direction: column; align-items: center;">
        <p style="color: #1B4332; font-size: 13pt; font-weight: bold; text-align: center; margin-top: 8pt; width: 184pt;">由同种元素组成的物质，一定是纯净物吗？</p>
      </div>
    </div>
    <div style="margin-top: 12pt; background: #FBF0DA; border-left: 5pt solid #E8A33D; border-radius: 3pt;">
      <p style="color: #1F2937; font-size: 13pt; margin: 9pt 14pt;">由同种元素组成的物质，<span style="font-weight: bold; color: #B45309;">不一定是纯净物</span>。如氧气（O₂）和臭氧（O₃）的混合物。</p>
    </div>''')

# ---------- P12 思考2：氧化物分类（源形状图裁切） ----------
PAGES['12-oxide'] = light_page(12, '主题 1 · 分类标准与方法', 'LuFlaskRound', '【思考2】利用树状分类法对氧化物进行分类，可以怎样分类？并举例说明。', f'''    <div style="display: flex; justify-content: center; margin-top: 6pt;">
      <img src="../images-src/p12-tree.png" style="width: 620pt; height: 263pt;">
    </div>''', tsize=15)

# ---------- P13 阅读材料：氧化物性质（方程式 + 两问） ----------
PAGES['13-oxide-prop'] = light_page(13, '主题 1 · 分类标准与方法', 'LuFlaskConical', '【阅读材料】几种氧化物的重要化学性质', f'''    <div style="display: flex; justify-content: space-between; margin-top: 2pt;">
      <div style="width: 312pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt;">
        <div style="background: #2D6A4F; border-radius: 7pt 7pt 0 0; display: flex; justify-content: center;">
          <p style="color: #FAF7F0; font-size: 13pt; font-weight: bold; margin: 5pt 0;">酸性氧化物</p>
        </div>
        <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5; margin: 8pt 12pt 0 12pt;">与水反应只生成相应价态的酸，如：</p>
        <p style="color: #1B4332; font-size: 12.5pt; font-weight: bold; margin: 4pt 12pt 0 12pt;">SO₂ + H₂O = H₂SO₃</p>
        <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5; margin: 6pt 12pt 0 12pt;">或与碱反应只生成一种盐和水，如：</p>
        <p style="color: #1B4332; font-size: 12.5pt; font-weight: bold; margin: 4pt 12pt 10pt 12pt;">SO₂ + 2NaOH = Na₂SO₃ + H₂O</p>
      </div>
      <div style="width: 312pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt;">
        <div style="background: #1B4332; border-radius: 7pt 7pt 0 0; display: flex; justify-content: center;">
          <p style="color: #FAF7F0; font-size: 13pt; font-weight: bold; margin: 5pt 0;">碱性氧化物</p>
        </div>
        <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5; margin: 8pt 12pt 0 12pt;">与水反应只生成相应价态的碱，如：</p>
        <p style="color: #1B4332; font-size: 12.5pt; font-weight: bold; margin: 4pt 12pt 0 12pt;">Na₂O + H₂O = 2NaOH</p>
        <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5; margin: 6pt 12pt 0 12pt;">或与酸反应只生成一种盐和水，如：</p>
        <p style="color: #1B4332; font-size: 12.5pt; font-weight: bold; margin: 4pt 12pt 10pt 12pt;">Na₂O + 2HCl = 2NaCl + H₂O</p>
      </div>
    </div>
    <div style="display: flex; margin-top: 12pt; align-items: center;">
      <div style="width: 640pt; background: #FBF0DA; border-left: 4pt solid #E8A33D; border-radius: 3pt;">
        <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5; margin: 7pt 12pt;">已知 3NO₂ + H₂O = 2HNO₃ + NO，<span style="font-weight: bold; color: #B45309;">NO₂ 是酸性氧化物吗？</span></p>
        <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5; margin: 0 12pt 7pt 12pt;">已知 2Na₂O₂ + 2H₂O = 4NaOH + O₂↑，<span style="font-weight: bold; color: #B45309;">Na₂O₂ 是碱性氧化物吗？</span></p>
      </div>
    </div>''')

# ---------- P14 组成与性质的关联（源形状图裁切 + 原文两句） ----------
PAGES['14-link'] = light_page(14, '主题 1 · 分类标准与方法', 'LuRefreshCw', '［思考］物质组成和性质之间是否存在某种关联？', f'''    <div style="display: flex; justify-content: center; margin-top: 4pt;">
      <img src="../images-src/p14-fig.png" style="width: 540pt; height: 214pt;">
    </div>
    <div style="margin-top: 10pt; background: #E3EDE6; border-radius: 5pt;">
      <p style="color: #1B4332; font-size: 13.5pt; font-weight: bold; text-align: center; margin: 9pt 14pt;">大多数金属氧化物是碱性氧化物　｜　大多数非金属氧化物是酸性氧化物</p>
    </div>''')

# ---------- P15 辨析：两问两提示（原文） ----------
PAGES['15-sure'] = light_page(15, '主题 1 · 分类标准与方法', 'LuTriangleAlert', '辨析：这些「一定」对吗？', f'''    <div style="margin-top: 8pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt;">
      <p style="color: #1B4332; font-size: 13.5pt; font-weight: bold; line-height: 1.55; margin: 10pt 14pt;">① 非金属氧化物一定是酸性氧化物吗？酸性氧化物一定是非金属氧化物吗？</p>
      <p style="color: #1F2937; font-size: 12pt; line-height: 1.55; margin: 6pt 14pt 10pt 14pt;"><span style="font-weight: bold; color: #B45309;">提示</span>　非金属氧化物大多是酸性氧化物，但不一定全是，如NO、CO不是酸性氧化物；酸性氧化物也不一定是非金属氧化物，如Mn₂O₇是酸性氧化物，但却是金属氧化物。</p>
    </div>
    <div style="margin-top: 12pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt;">
      <p style="color: #1B4332; font-size: 13.5pt; font-weight: bold; line-height: 1.55; margin: 10pt 14pt;">② 金属氧化物一定是碱性氧化物吗？碱性氧化物一定是金属氧化物吗？</p>
      <p style="color: #1F2937; font-size: 12pt; line-height: 1.55; margin: 6pt 14pt 10pt 14pt;"><span style="font-weight: bold; color: #B45309;">提示</span>　金属氧化物大多是碱性氧化物，但不一定全是，如Al₂O₃是金属氧化物，却是两性氧化物；碱性氧化物一定是金属氧化物。</p>
    </div>''')

# ---------- P16 思考3：酸的分类（源形状图裁切） ----------
PAGES['16-acid'] = light_page(16, '主题 1 · 分类标准与方法', 'LuTable', '【思考3】利用树状分类法对酸进行分类，可以怎样分类？并举例说明。', f'''    <div style="display: flex; justify-content: center; margin-top: 6pt;">
      <img src="../images-src/p16-fig.png" style="width: 610pt; height: 295pt;">
    </div>''', tsize=15)

# ---------- P17 思考4：碱的分类（源大图） ----------
PAGES['17-base'] = light_page(17, '主题 1 · 分类标准与方法', 'LuTable', '【思考4】利用树状分类法对碱进行分类，可以怎样分类？并举例说明。', f'''    <div style="display: flex; justify-content: center; margin-top: 8pt;">
      <img src="../images-src/p17-img1.png" style="width: 620pt; height: 267pt;">
    </div>''', tsize=15)

# ---------- P18 思考5：盐的分类（源大图） ----------
PAGES['18-salt'] = light_page(18, '主题 1 · 分类标准与方法', 'LuTable', '【思考5】利用树状分类法对盐进行分类，可以怎样分类？并举例说明。', f'''    <div style="display: flex; justify-content: center; margin-top: 8pt;">
      <img src="../images-src/p18-img1.png" style="width: 400pt; height: 275pt;">
    </div>''', tsize=15)

# ---------- P19 思考交流：化学反应的分类（源形状图裁切） ----------
PAGES['19-reaction'] = light_page(19, '主题 1 · 分类标准与方法', 'LuList', '【思考交流】化学反应的分类', f'''    <p style="color: #1F2937; font-size: 13pt; line-height: 1.5; margin-top: 0; width: 620pt;">在初中我们学习过四种基本化学反应类型，它们是按照什么标准进行分类的？将化学反应又可以按照哪些不同的标准进行分类呢？</p>
    <div style="display: flex; justify-content: center; margin-top: 6pt;">
      <img src="../images-src/p19-fig.png" style="width: 610pt; height: 260pt;">
    </div>''')

# ---------- P20 课堂小结（源双图） ----------
PAGES['20-summary'] = light_page(20, '课堂小结', 'LuKeyRound', '课堂小结', f'''    <div style="display: flex; justify-content: space-between; margin-top: 10pt;">
      <div style="width: 305pt; display: flex; flex-direction: column; align-items: center;">
        <div style="background: #1B4332; border-radius: 6pt; width: 200pt; display: flex; justify-content: center;">
          <p style="color: #FAF7F0; font-size: 15pt; font-weight: bold; margin: 6pt 0;">树状分类法</p>
        </div>
        <img src="../images-src/p20-img2.png" style="width: 170pt; height: 183pt; margin-top: 10pt;">
        <p style="color: #1F2937; font-size: 12.5pt; text-align: center; margin-top: 8pt; width: 290pt;">特点：同层次中各类别间相互独立</p>
      </div>
      <div style="width: 305pt; display: flex; flex-direction: column; align-items: center;">
        <div style="background: #2D6A4F; border-radius: 6pt; width: 200pt; display: flex; justify-content: center;">
          <p style="color: #FAF7F0; font-size: 15pt; font-weight: bold; margin: 6pt 0;">交叉分类法</p>
        </div>
        <img src="../images-src/p20-img1.jpg" style="width: 230pt; height: 166pt; margin-top: 14pt;">
        <p style="color: #1F2937; font-size: 12.5pt; text-align: center; margin-top: 12pt; width: 290pt;">特点：物质类别间有相交叉的部分</p>
      </div>
    </div>''')

# ---------- P21 典例 1 ----------
PAGES['21-ex1'] = light_page(21, '主题 2 · 典例与练习', 'LuPenLine', '典例 1', f'''{exam_q('【典例1】下列各组物质，按化合物、单质、混合物的顺序排列的是（　　）')}
    <p style="color: #1F2937; font-size: 13pt; line-height: 1.7; margin-top: 8pt; width: 620pt;">A．干冰、铁、氯化氢　　B．生石灰、白磷、熟石灰</p>
    <p style="color: #1F2937; font-size: 13pt; line-height: 1.7; width: 620pt;">C．烧碱、液态氧、碘酒　　D．空气、氮气、胆矾</p>
    <div style="display: flex; margin-top: 8pt; align-items: center;">
{answer_card('C')}
    </div>
{explain('【解析】A．氯化氢是纯净物，不是混合物，A项错误；B．熟石灰是纯净物，不是混合物，B项错误；C．烧碱的化学式为NaOH，属于化合物；液态氧的化学式为O₂，属于单质；碘酒是碘的酒精溶液，属于混合物。C项正确；D．空气是由N₂、O₂等气体组成的混合物，不是化合物，胆矾是纯净物不是混合物，D项错误。', size=11)}''')

# ---------- P22 典例 2 ----------
PAGES['22-ex2'] = light_page(22, '主题 2 · 典例与练习', 'LuPenLine', '典例 2', f'''{exam_q('【典例2】将下列各组物质分类正确的是（　　）')}
    <p style="color: #1F2937; font-size: 13pt; line-height: 1.7; margin-top: 8pt; width: 620pt;">A．酸：硫酸、醋酸、NaHSO₄、硝酸</p>
    <p style="color: #1F2937; font-size: 13pt; line-height: 1.7; width: 620pt;">B．同素异形体：金刚石、石墨、C₆₀、无定形碳</p>
    <p style="color: #1F2937; font-size: 13pt; line-height: 1.7; width: 620pt;">C．盐：生石灰、硝酸钾、CaCO₃、苛性钠</p>
    <p style="color: #1F2937; font-size: 13pt; line-height: 1.7; width: 620pt;">D．碱：纯碱、烧碱、乙醇、熟石灰</p>
    <div style="display: flex; margin-top: 8pt; align-items: center;">
{answer_card('B')}
    </div>
{explain('【解析】A．酸是电离出的阳离子都是氢离子的物质，NaHSO₄不是酸，故A错误；B．同素异形体是同种元素形成的不同单质，金刚石、石墨、C₆₀、无定形碳都是碳元素形成的不同单质，故B正确；C．生石灰是氧化物，不是盐，故C错误；D．纯碱为盐，乙醇是有机物不是碱，故D错误；故选B。', size=11)}''')

# ---------- P23 典例 3（源概念关系图） ----------
PAGES['23-ex3'] = light_page(23, '主题 2 · 典例与练习', 'LuPenLine', '典例 3', f'''{exam_q('【典例3】化学概念在逻辑上存在如下关系：')}
    <div style="display: flex; justify-content: center; margin-top: 6pt;">
      <img src="../images-src/p23-img1.jpg" style="width: 429pt; height: 114pt;">
    </div>
    <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.6; margin-top: 8pt; width: 620pt;">对下列概念的说法正确的是（　　）</p>
    <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.6; width: 620pt;">A．化合物与纯净物属于重叠关系　　B．化合物与碱性氧化物属于交叉关系</p>
    <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.6; width: 620pt;">C．分解反应与复分解反应属于并列关系　　D．硫酸与硝酸只有交叉关系</p>
    <div style="display: flex; margin-top: 6pt; align-items: center;">
{answer_card('C')}
    </div>
{explain('【解析】纯净物与化合物、化合物与碱性氧化物属于包含关系；分解反应与复分解反应属于并列关系；硫酸与硝酸既有交叉关系（都是含氧酸），又有并列关系（一元酸、二元酸）。', mt=6, size=11)}''')

# ---------- P24 典例 4（源五环图 + 表格） ----------
def rcell(w, text, bg='#FFFFFF', bold=False, color='#1F2937'):
    return tcell(w, text, bg=bg, bold=bold, color=color, size=10)

PAGES['24-ex4'] = light_page(24, '主题 2 · 典例与练习', 'LuPenLine', '典例 4', f'''{exam_q('【典例4】奥运五环代表着世界人民团结在一起。下列各项中的物质，能满足如图中阴影部分关系的是（　　）', size=12.5)}
    <div style="display: flex; margin-top: 6pt;">
      <img src="../images-src/p24-img1.jpg" style="width: 300pt; height: 97pt; margin-top: 10pt;">
      <div style="margin-left: 18pt;">
        <div style="display: flex;">
{hcell(44, '选项', size=11)}
{hcell(58, '①', size=11)}
{hcell(58, '②', size=11)}
{hcell(58, '③', size=11)}
{hcell(66, '④', size=11)}
        </div>
        <div style="display: flex;">{hcell(44, 'A', size=11)}{rcell(58, 'NaCl')}{rcell(58, 'K₂SO₄')}{rcell(58, 'KCl')}{rcell(66, '(NH₄)₂SO₄')}</div>
        <div style="display: flex;">{hcell(44, 'B', size=11)}{rcell(58, 'Na₂SO₄')}{rcell(58, 'K₂SO₄')}{rcell(58, 'KCl')}{rcell(66, 'NH₄Cl')}</div>
        <div style="display: flex;">{hcell(44, 'C', size=11)}{rcell(58, 'NaCl')}{rcell(58, 'Na₂SO₄')}{rcell(58, 'KNO₃')}{rcell(66, 'NH₄Cl')}</div>
        <div style="display: flex;">{hcell(44, 'D', size=11)}{rcell(58, 'Na₂SO₄')}{rcell(58, 'K₂SO₄')}{rcell(58, 'KNO₃')}{rcell(66, '(NH₄)₂SO₄')}</div>
      </div>
    </div>
    <div style="display: flex; margin-top: 6pt; align-items: center;">
{answer_card('B')}
    </div>
{explain('【解析】A．NaCl是钠盐、盐酸盐，不是硫酸盐，(NH₄)₂SO₄是铵盐、硫酸盐，不是盐酸盐，A错误；B．Na₂SO₄是钠盐、硫酸盐，K₂SO₄是钾盐、硫酸盐，KCl是钾盐、盐酸盐，NH₄Cl是铵盐、盐酸盐，B正确；C．NaCl是钠盐、盐酸盐，不是硫酸盐，KNO₃是钾盐、硝酸盐，不是盐酸盐，C错误；D．KNO₃是钾盐、硝酸盐，不是盐酸盐，(NH₄)₂SO₄是铵盐、硫酸盐，不是盐酸盐，D错误；答案选B。', mt=6, size=10.5)}''')

# ---------- P25 典例 5（原文含填空线） ----------
PAGES['25-ex5'] = light_page(25, '主题 2 · 典例与练习', 'LuSearch', '典例 5', f'''{exam_q('【典例5】下列五组物质，每组中有一种物质从某种角度分析与其他三种不同，请找出该物质，并说明理由。', size=12.5)}
    <div style="margin-top: 8pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 6pt;">
      <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.7; margin: 9pt 14pt 0 14pt;">（1）Fe、S、C、P　＿＿＿＿＿</p>
      <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.7; margin: 0 14pt;">（2）H₂、O₂、N₂、S　＿＿＿＿＿</p>
      <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.7; margin: 0 14pt;">（3）Fe₂O₃、Na₂CO₃、CuO、H₂O　＿＿＿＿＿</p>
      <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.7; margin: 0 14pt 9pt 14pt;">（4）AgCl、BaSO₄、KNO₃、CaCO₃　＿＿＿＿＿</p>
    </div>
    <div style="margin-top: 10pt; background: #E8A33D; border-radius: 6pt;">
      <p style="color: #1B4332; font-size: 12pt; font-weight: bold; line-height: 1.6; margin: 9pt 14pt;">Fe；Fe为金属　｜　S；常温下S为固体　｜　Na₂CO₃；Na₂CO₃为盐　｜　KNO₃；KNO₃易溶于水（或AgCl；AgCl酸根离子中不含氧）</p>
    </div>''')

# ---------- 检测题公共件 ----------
def test_block(no, lines, ans):
    ps = ''.join(f'<p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5; margin: 0 14pt;">{t}</p>' for t in lines)
    return f'''      <div style="background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; margin-bottom: 10pt;">
        <div style="margin-top: 9pt;"></div>
        {ps}
        <p style="color: #B45309; font-size: 12pt; font-weight: bold; margin: 6pt 14pt 9pt 14pt;">答案：{ans}</p>
      </div>'''

# ---------- P26 课堂检测 1-2 ----------
PAGES['26-test12'] = light_page(26, '主题 2 · 典例与练习', 'LuListChecks', '课堂检测', f'''    <div style="margin-top: 0;">
{test_block('题 1', ['1．Na₂CO₃、NaCl、NaOH、Na₂SO₄可按某种标准划分为一类物质，下列分类标准不正确的是（　　）', 'A．钠的化合物　B．纯净物　C．钠盐　D．无机物'], 'C')}
{test_block('题 2', ['2．已知由碳元素组成的单质有金刚石、石墨和足球烯（C₆₀）等，由氧元素组成的单质有O₂和O₃，下列说法不正确的是（　　）', 'A．一种元素可能形成两种或两种以上不同的单质', 'B．单质的种类一定多于元素的种类', 'C．由同一种元素形成的几种单质互为同素异形体', 'D．金刚石、石墨和足球烯（C₆₀）在氧气中燃烧都只能生成一种物质'], 'D')}
    </div>''')

# ---------- P27 课堂检测 3-4（含源图甲乙） ----------
PAGES['27-test34'] = light_page(27, '主题 2 · 典例与练习', 'LuListChecks', '课堂检测（续）', f'''    <div style="margin-top: 0;">
      <div style="background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 8pt; margin-bottom: 10pt;">
        <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5; margin: 9pt 14pt 0 14pt;">3．物质的分类如图所示：</p>
        <div style="display: flex; align-items: center; margin: 4pt 14pt 0 14pt;">
          <img src="../images-src/p27-img2.png" style="width: 267pt; height: 114pt;">
          <div style="margin-left: 14pt; width: 320pt;">
            <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5;">由图判断下列说法中不正确的是（　　）</p>
            <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5;">A．图甲所示的分类方法属于树状分类法</p>
            <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5;">B．图乙所示的分类方法属于交叉分类法</p>
            <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5;">C．碱性氧化物一定是金属氧化物</p>
            <p style="color: #1F2937; font-size: 11.5pt; line-height: 1.5;">D．非金属氧化物一定是酸性氧化物</p>
          </div>
        </div>
        <p style="color: #B45309; font-size: 12pt; font-weight: bold; margin: 4pt 14pt 9pt 14pt;">答案：D</p>
      </div>
{test_block('题 4', ['4．下列物质的分类正确的一组是（　　）', 'A．冰水混合物、水银、澄清石灰水、淀粉属于混合物', 'B．NaHSO₄、HCl、HNO₃在水中能电离出氢离子，按分类属于酸', 'C．非金属氧化物CO₂、CO、SO₃均为酸性氧化物', 'D．冰醋酸、酒精属于有机物'], 'D')}
    </div>''')

# ---------- P28 课堂检测 5（表格题） ----------
def dcell(text, bold=False, bg='#FFFFFF', color='#1F2937'):
    return tcell(120, text, bg=bg, bold=bold, color=color, size=11)

PAGES['28-test5'] = light_page(28, '主题 2 · 典例与练习', 'LuListChecks', '课堂检测（续）', f'''{exam_q('5．下列物质的分类正确的是（　　）')}
    <div style="margin-top: 10pt;">
      <div style="display: flex;">
{hcell(40, '', size=11)}{hcell(120, '碱', size=11.5)}{hcell(120, '酸', size=11.5)}{hcell(120, '盐', size=11.5)}{hcell(120, '碱性氧化物', size=11.5)}{hcell(120, '酸性氧化物', size=11.5)}
      </div>
      <div style="display: flex;">{hcell(40, 'A', size=11)}{dcell('Na₂CO₃')}{dcell('H₂SO₄')}{dcell('NaOH')}{dcell('SO₂')}{dcell('CO₂')}</div>
      <div style="display: flex;">{hcell(40, 'B', size=11)}{dcell('NaOH')}{dcell('HCl')}{dcell('NaCl')}{dcell('Na₂O')}{dcell('NO')}</div>
      <div style="display: flex;">{hcell(40, 'C', size=11)}{dcell('KOH')}{dcell('HNO₃')}{dcell('CaCO₃')}{dcell('CaO')}{dcell('Mn₂O₇')}</div>
      <div style="display: flex;">{hcell(40, 'D', size=11)}{dcell('NaOH')}{dcell('HCl')}{dcell('CaF₂')}{dcell('Na₂O₂')}{dcell('SO₂')}</div>
    </div>
    <div style="display: flex; margin-top: 12pt; align-items: center;">
{answer_card('C')}
    </div>
''')

# ---------- P29 课堂检测 6 ----------
PAGES['29-test6'] = light_page(29, '主题 2 · 典例与练习', 'LuListChecks', '课堂检测（续）', f'''{exam_q('6．下列各组均有四种物质，其中有一种物质与其他三种物质的类别不同，请将该物质的化学式或名称填在横线上', size=12.5)}
    <div style="margin-top: 10pt; background: #FFFFFF; border: 1pt solid #DDD6C8; border-radius: 6pt;">
      <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.8; margin: 10pt 16pt;">（１）CuO、NO₂、NaOH、Fe₂O₃　　（２）O₂、N₂、Al、C　　（３）空气，食盐水，蒸馏水，豆浆</p>
      <p style="color: #1F2937; font-size: 12.5pt; line-height: 1.8; margin: 0 16pt 10pt 16pt;">（４）空气，氢气，碘酒，盐酸　　（５）冰，干冰，氧化铜，铜丝</p>
    </div>
    <div style="margin-top: 12pt; background: #E8A33D; border-radius: 6pt;">
      <p style="color: #1B4332; font-size: 13pt; font-weight: bold; line-height: 1.6; margin: 10pt 16pt;">（NaOH）　（Al）　（蒸馏水）　（氢气）　（铜丝）</p>
    </div>
''')

# ---------- P30 结尾（深色，原文 Thank you for watching + 源 gif） ----------
PAGES['30-end'] = DARK_HEAD + '''<body>
  <div style="width: 720pt; height: 6pt; background: #E8A33D;"></div>
  <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;">
    <h1 style="color: #FAF7F0; font-size: 36pt; font-weight: bold; margin-top: 24pt;">Thank you for watching</h1>
    <div style="background: #E8A33D; width: 56pt; height: 4pt; margin-top: 22pt;"></div>
  </div>
  <div style="width: 720pt; height: 5pt; background: #2D6A4F;"></div>
  <p style="position: absolute; right: 40pt; top: 382pt; width: 80pt; text-align: right; color: rgba(250,247,240,0.6); font-size: 10pt;">30 / 30</p>
</body>
</html>
'''

# ---------- 写文件 ----------
ORDER = ['01-cover', '02-scene', '03-everywhere', '04-what', '05-elements', '06-think',
         '07-tree', '08-tree-big', '09-cross', '10-element', '11-allotrope', '12-oxide',
         '13-oxide-prop', '14-link', '15-sure', '16-acid', '17-base', '18-salt',
         '19-reaction', '20-summary', '21-ex1', '22-ex2', '23-ex3', '24-ex4',
         '25-ex5', '26-test12', '27-test34', '28-test5', '29-test6', '30-end']

for name in ORDER:
    (OUT / f'{name}.html').write_text(PAGES[name], encoding='utf-8')
print('wrote', len(ORDER), 'slides')
