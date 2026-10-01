const { createPPT, makeHtmlSlide, defaultColors } = require('../../11-模板/pptx-toolkit/ppt-engine.js');
const path = require('path');

const OUTPUT_PATH = path.join(__dirname, '..', '试点产出', '2026-06-16-原子结构基础-基础班-课件.pptx');
const COLORS = defaultColors;

const slides = [
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '原子结构基础（基础班）',
      contentHtml: `
<div style="margin-top:56pt;">
  <p style="font-size:18pt; text-align:center;">模型演进 → 轨道图景 → 电子排布 → 周期律解释</p>
  <p style="font-size:12pt; text-align:center; color:#666;">第一轮基础班投影骨架版</p>
</div>`,
      colors: COLORS,
    }),
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '为什么旧的“电子层”语言不够',
      contentHtml: `
<ul style="font-size:16pt; line-height:1.8;">
  <li>电子不会像行星那样沿固定轨道绕核转动</li>
  <li>氢原子线状光谱说明能量是离散的</li>
  <li>必须升级到“能层 + 能级 + 轨道 + 排布”的语言</li>
</ul>`,
      colors: COLORS,
    }),
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '模型演进最小时间线',
      contentHtml: `
<ol style="font-size:15pt; line-height:1.8;">
  <li>Dalton：实心球模型</li>
  <li>Thomson：葡萄干布丁模型</li>
  <li>Rutherford：核式模型</li>
  <li>Bohr：量子化轨道（过渡模型）</li>
  <li>量子图像：轨道是概率分布，不是轨迹</li>
</ol>`,
      colors: COLORS,
    }),
  },
  {
    type: 'table',
    title: '量子数最小框架',
    tableData: [
      ['量子数', '最小口径', '课堂作用'],
      ['n', '决定能层大小', '先看电子所在主层'],
      ['l', '决定亚层类型', '区分 s / p / d / f'],
      ['m_l', '区分同一亚层中的轨道', '只做轨道标签'],
      ['m_s', '区分电子自旋', '为 Pauli / Hund 服务'],
    ],
    tableOptions: { x: 0.5, y: 1.1, w: 9.0, border: { pt: 1, color: 'CCCCCC' }, fontSize: 12 },
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '轨道图景与能级图',
      contentHtml: `
<ul style="font-size:15pt; line-height:1.8;">
  <li>s / p / d 轨道形状用于建立“概率分布”直觉</li>
  <li>Pauling 近似能级图用于解释排布顺序</li>
  <li>课堂只抓：4s 与 3d 的相对顺序会影响排布与失电子</li>
</ul>`,
      colors: COLORS,
    }),
  },
  {
    type: 'table',
    title: '三条排布规则',
    tableData: [
      ['规则', '它管什么', '课堂口令'],
      ['Aufbau', '先填低能轨道', '先找最低能级'],
      ['Pauli', '每个轨道最多两电子且自旋相反', '一个房间最多住两人'],
      ['Hund', '简并轨道先单占后成对', '先分开坐，再考虑配对'],
    ],
    tableOptions: { x: 0.5, y: 1.15, w: 9.0, border: { pt: 1, color: 'CCCCCC' }, fontSize: 12 },
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '排布例题：中性原子与离子',
      contentHtml: `
<ul style="font-size:15pt; line-height:1.75;">
  <li>中性原子：Na、Cl、Fe</li>
  <li>离子：Fe²⁺、Fe³⁺、Cu⁺</li>
  <li>投影只放题干，详细推理交给板书</li>
</ul>`,
      colors: COLORS,
    }),
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: 'Cr / Cu 特例',
      contentHtml: `
<ul style="font-size:15pt; line-height:1.8;">
  <li>Cr：4s¹3d⁵</li>
  <li>Cu：4s¹3d¹⁰</li>
  <li>课堂只要求会认、会写、会解释“半满 / 全满稳定”</li>
</ul>`,
      colors: COLORS,
    }),
  },
  {
    type: 'table',
    title: '周期律趋势统一框架',
    tableData: [
      ['性质', '总体趋势', '统一解释'],
      ['原子半径', '同周期减小', '有效核电荷增强'],
      ['电离能', '总体增大', '电子受核吸引增强'],
      ['电负性', '总体增大', '得电子能力增强'],
    ],
    tableOptions: { x: 0.5, y: 1.15, w: 9.0, border: { pt: 1, color: 'CCCCCC' }, fontSize: 12 },
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '反常点：为什么 Mg > Al，N > O',
      contentHtml: `
<ul style="font-size:15pt; line-height:1.8;">
  <li>Mg &gt; Al：从 3s² 到 3p¹，失电子更容易</li>
  <li>N &gt; O：2p³ 半满稳定，2p⁴ 出现成对电子排斥</li>
  <li>统一回到“更稳定 / 更难失电子”</li>
</ul>`,
      colors: COLORS,
    }),
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '元素推断综合题',
      contentHtml: `
<ul style="font-size:15pt; line-height:1.8;">
  <li>先看电子排布</li>
  <li>再看电离能突变位置</li>
  <li>最后判周期、族属与未成对电子数</li>
</ul>`,
      colors: COLORS,
    }),
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '本节收束：判断顺序卡',
      contentHtml: `
<ol style="font-size:15pt; line-height:1.8;">
  <li>先确认轨道 / 能级语言，而不是只停在电子层</li>
  <li>再用排布三原则写中性原子与离子</li>
  <li>最后把周期律和反常点都压回电子排布解释</li>
</ol>`,
      colors: COLORS,
    }),
  },
];

async function main() {
  await createPPT({
    title: '原子结构基础（基础班）',
    outputPath: OUTPUT_PATH,
    formulas: {},
    slides,
    colors: COLORS,
  });
}

main().catch(console.error);
