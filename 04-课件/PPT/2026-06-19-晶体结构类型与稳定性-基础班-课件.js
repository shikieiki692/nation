const { createPPT, makeHtmlSlide, defaultColors } = require('../../11-模板/pptx-toolkit/ppt-engine.js');
const path = require('path');

const OUTPUT_PATH = path.join(__dirname, '..', '试点产出', '2026-06-19-晶体结构类型与稳定性-基础班-课件.pptx');
const COLORS = defaultColors;

const slides = [
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '晶体结构类型与稳定性（基础班）',
      contentHtml: `
<div style="margin-top:56pt;">
  <p style="font-size:18pt; text-align:center;">堆积 → 填隙 → 配位数 → 稳定性 → 物性</p>
  <p style="font-size:12pt; text-align:center; color:#666;">第一轮样板专题投影骨架版</p>
</div>`,
      colors: COLORS,
    }),
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '结构题统一四问',
      contentHtml: `
<ol style="font-size:16pt; line-height:1.8;">
  <li>哪一类粒子先构成骨架？</li>
  <li>另一类粒子填了什么空隙？</li>
  <li>配位数怎样决定？</li>
  <li>为什么这种结构更稳定？</li>
</ol>`,
      colors: COLORS,
    }),
  },
  {
    type: 'table',
    title: '四种堆积的最小比较',
    tableData: [
      ['堆积', '配位数', '空间利用率', '课堂抓手'],
      ['sc', '6', '低', '最简单模型'],
      ['bcc', '8', '约 68%', '不是最密堆积'],
      ['ccp/fcc', '12', '约 74%', 'ABC 堆积'],
      ['hcp', '12', '约 74%', 'AB 堆积'],
    ],
    tableOptions: { x: 0.5, y: 1.1, w: 9.0, border: { pt: 1, color: 'CCCCCC' }, fontSize: 12 },
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '必须投影图 1：ccp / hcp',
      contentHtml: `
<ul style="font-size:15pt; line-height:1.8;">
  <li>只抓堆积顺序、配位数、空隙类型</li>
  <li>不展开更深晶体学术语</li>
  <li>板书只补“为什么都叫最密堆积”</li>
</ul>`,
      colors: COLORS,
    }),
  },
  {
    type: 'table',
    title: 'NaCl / CsCl / ZnS 对照',
    tableData: [
      ['结构', '骨架', '填隙方式', '配位数'],
      ['NaCl', '阴离子 fcc', '八面体全填', '6:6'],
      ['CsCl', '两套简单立方互穿', '立方体中心位', '8:8'],
      ['ZnS', '阴离子 fcc', '四面体半填', '4:4'],
    ],
    tableOptions: { x: 0.5, y: 1.1, w: 9.0, border: { pt: 1, color: 'CCCCCC' }, fontSize: 12 },
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '必须投影图 2：NaCl / CsCl / ZnS',
      contentHtml: `
<ul style="font-size:15pt; line-height:1.8;">
  <li>同为离子晶体，但填隙方式不同</li>
  <li>课堂统一口令：先看骨架，不先背名字</li>
  <li>板书完整跑“骨架 + 填隙 + 配位数”</li>
</ul>`,
      colors: COLORS,
    }),
  },
  {
    type: 'table',
    title: '稳定性三按钮',
    tableData: [
      ['按钮', '回答什么问题', '课堂说法'],
      ['半径比', '能形成几配位', '能不能坐进去'],
      ['Pauling', '静电账是否算得过来', '为什么这样更稳'],
      ['离子极化', '为什么会偏离理想模型', '是不是已经开始带共价性'],
    ],
    tableOptions: { x: 0.5, y: 1.1, w: 9.0, border: { pt: 1, color: 'CCCCCC' }, fontSize: 12 },
  },
  {
    type: 'table',
    title: '四类晶体与物性',
    tableData: [
      ['类型', '结构单元', '主要作用', '典型物性'],
      ['离子晶体', '离子', '离子键', '高熔点、硬脆、熔融导电'],
      ['分子晶体', '分子', '分子间力/氢键', '低熔点、较软、不导电'],
      ['原子晶体', '原子', '共价网络', '高熔点、高硬度'],
      ['金属晶体', '金属原子骨架', '金属键', '导电导热、延展性好'],
    ],
    tableOptions: { x: 0.45, y: 1.02, w: 9.1, border: { pt: 1, color: 'CCCCCC' }, fontSize: 11 },
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '必须投影图 3：冰 / 金刚石 / 石墨',
      contentHtml: `
<ul style="font-size:15pt; line-height:1.8;">
  <li>冰：开放氢键网络，密度反常</li>
  <li>金刚石：三维共价网络，极硬</li>
  <li>石墨：层内强、层间弱，可导电</li>
</ul>`,
      colors: COLORS,
    }),
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '综合题讲评固定口令',
      contentHtml: `
<ol style="font-size:15pt; line-height:1.8;">
  <li>先看骨架，不先猜结构名</li>
  <li>先看填隙，不先背模板</li>
  <li>先解释为什么稳，再解释为什么有这个性质</li>
</ol>`,
      colors: COLORS,
    }),
  },
  {
    type: 'html',
    html: makeHtmlSlide({
      title: '本节收束：结构题四问 / 物性题三步',
      contentHtml: `
<p style="font-size:15pt; line-height:1.8;">结构题四问：骨架是谁？填了什么空隙？配位数怎么来？稳定性按钮是谁？</p>
<p style="font-size:15pt; line-height:1.8;">物性题三步：结构单元是什么？主要作用力是什么？为什么会有这个性质？</p>`,
      colors: COLORS,
    }),
  },
];

async function main() {
  await createPPT({
    title: '晶体结构类型与稳定性（基础班）',
    outputPath: OUTPUT_PATH,
    formulas: {},
    slides,
    colors: COLORS,
  });
}

main().catch(console.error);
