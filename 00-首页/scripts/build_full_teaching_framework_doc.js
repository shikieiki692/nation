const fs = require("fs");
const path = require("path");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  Header,
  Footer,
  AlignmentType,
  HeadingLevel,
  WidthType,
  BorderStyle,
  PageNumber,
  PageOrientation,
  ShadingType,
} = require("docx");

const outDir = "C:/Obsidion/妙妙屋/04-课件/试点产出";
const outFile = path.join(outDir, "2026-06-19-全备课框架-教师查看版.docx");

fs.mkdirSync(outDir, { recursive: true });

const border = { style: BorderStyle.SINGLE, size: 1, color: "C7CED6" };
const cellBorders = { top: border, bottom: border, left: border, right: border };

const p = (text, opts = {}) =>
  new Paragraph({
    spacing: { after: opts.after ?? 120, before: opts.before ?? 0 },
    alignment: opts.align ?? AlignmentType.LEFT,
    heading: opts.heading,
    pageBreakBefore: opts.pageBreakBefore ?? false,
    children: (opts.runs || [new TextRun({ text, bold: opts.bold, size: opts.size ?? 24 })]),
  });

const bullet = (text) =>
  new Paragraph({
    text,
    bullet: { level: 0 },
    spacing: { after: 80 },
  });

const makeCell = (text, width, opts = {}) =>
  new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    children: [
      new Paragraph({
        spacing: { after: 60, before: 60 },
        alignment: opts.align ?? AlignmentType.LEFT,
        children: [
          new TextRun({
            text,
            bold: !!opts.bold,
            size: opts.size ?? 22,
          }),
        ],
      }),
    ],
  });

const makeTable = (rows, widths) =>
  new Table({
    columnWidths: widths,
    width: { size: 100, type: WidthType.PERCENTAGE },
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    rows,
  });

const overviewTable = makeTable(
  [
    new TableRow({
      tableHeader: true,
      children: [
        makeCell("轮次", 1100, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
        makeCell("定位", 2500, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
        makeCell("核心内容", 3900, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
        makeCell("当前使用口径", 1850, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
      ],
    }),
    new TableRow({
      children: [
        makeCell("第一轮", 1100, { bold: true }),
        makeCell("高中到竞赛的衔接轮", 2500),
        makeCell("化学原理入门、结构语言建立、基础工具化训练", 3900),
        makeCell("完整展开", 1850, { align: AlignmentType.CENTER }),
      ],
    }),
    new TableRow({
      children: [
        makeCell("第二轮", 1100, { bold: true }),
        makeCell("元素直觉 + 分析思维建立", 2500),
        makeCell("元素化学主干、容量分析、元素推断综合训练", 3900),
        makeCell("完整展开", 1850, { align: AlignmentType.CENTER }),
      ],
    }),
    new TableRow({
      children: [
        makeCell("第三轮", 1100, { bold: true }),
        makeCell("有机系统 + 结构/物化深化", 2500),
        makeCell("有机反应体系、晶体与配位深化、动力学与热力学深化", 3900),
        makeCell("完整展开", 1850, { align: AlignmentType.CENTER }),
      ],
    }),
    new TableRow({
      children: [
        makeCell("第四轮", 1100, { bold: true }),
        makeCell("冲刺缝合与难点突破", 2500),
        makeCell("高等有机、立体选择性、人名反应、晶体推断、配位深化、物化综合、真题模拟", 3900),
        makeCell("完整展开", 1850, { align: AlignmentType.CENTER }),
      ],
    }),
    new TableRow({
      children: [
        makeCell("第五轮+", 1100, { bold: true }),
        makeCell("决赛专题与后续拓展", 2500),
        makeCell("决赛深水区、前沿专题、个性化补强", 3900),
        makeCell("简要带过", 1850, { align: AlignmentType.CENTER }),
      ],
    }),
  ],
  [1100, 2500, 3900, 1850]
);

const round1Table = makeTable(
  [
    new TableRow({ tableHeader: true, children: [
      makeCell("模块", 2500, { bold: true, shading: "EAF2F8" }),
      makeCell("内容概述", 4200, { bold: true, shading: "EAF2F8" }),
      makeCell("备注", 2650, { bold: true, shading: "EAF2F8" }),
    ]}),
    new TableRow({ children: [
      makeCell("化学计量与气体", 2500),
      makeCell("有效数字、理想气体状态方程、Dalton 分压、溶液浓度换算、基础化学计量", 4200),
      makeCell("建立单位感和计算规范", 2650),
    ]}),
    new TableRow({ children: [
      makeCell("原子结构与周期律", 2500),
      makeCell("电子排布、周期律趋势、电离能、电负性、基础元素推断", 4200),
      makeCell("只讲直觉与工具，不做高阶量子化", 2650),
    ]}),
    new TableRow({ children: [
      makeCell("酸碱/热力学/平衡/电化学", 2500),
      makeCell("Brønsted/Lewis 酸碱、焓熵自由能、平衡常数、原电池和 Nernst 方程基础", 4200),
      makeCell("服务后续分析化学和元素化学", 2650),
    ]}),
    new TableRow({ children: [
      makeCell("结构化学初步", 2500),
      makeCell("Lewis 结构、VSEPR、杂化轨道、氢键、晶体和配合物基础", 4200),
      makeCell("只建立语言，不追求全理论", 2650),
    ]}),
  ] ,
  [2500, 4200, 2650]
);

const round2Table = makeTable(
  [
    new TableRow({ tableHeader: true, children: [
      makeCell("模块", 2400, { bold: true, shading: "EAF2F8" }),
      makeCell("内容概述", 4300, { bold: true, shading: "EAF2F8" }),
      makeCell("备注", 2650, { bold: true, shading: "EAF2F8" }),
    ]}),
    new TableRow({ children: [
      makeCell("主族与过渡元素", 2400),
      makeCell("氢、卤素、氧硫氮磷、碳硅硼铝、碱金属碱土金属、稀有气体，以及 Ti-V-Cr-Mn、Fe-Co-Ni-Cu-Zn、Ag-Au-Hg-Mo-W", 4300),
      makeCell("目标是形成元素直觉和题面信号识别", 2650),
    ]}),
    new TableRow({ children: [
      makeCell("分析化学主线", 2400),
      makeCell("容量分析基础、酸碱滴定、氧化还原滴定、沉淀滴定、络合滴定、重量分析、分光光度法、误差处理", 4300),
      makeCell("第二轮系统讲完，不再后拖", 2650),
    ]}),
    new TableRow({ children: [
      makeCell("情境化元素推断", 2400),
      makeCell("颜色、沉淀、气体、价态变化、配位反应等多信号综合推断", 4300),
      makeCell("是第二轮的能力收束点", 2650),
    ]}),
  ],
  [2400, 4300, 2650]
);

const round3Table = makeTable(
  [
    new TableRow({ tableHeader: true, children: [
      makeCell("模块", 2500, { bold: true, shading: "EAF2F8" }),
      makeCell("内容概述", 4200, { bold: true, shading: "EAF2F8" }),
      makeCell("备注", 2650, { bold: true, shading: "EAF2F8" }),
    ]}),
    new TableRow({ children: [
      makeCell("有机系统 12 专题", 2500),
      makeCell("电子效应、立体化学、机理基础、取代/消除、加成、羰基化学、重排、芳香反应、周环反应、自由基反应、逆合成与金属有机、杂原子与生物高分子", 4200),
      makeCell("核心是机理思维与迁移能力", 2650),
    ]}),
    new TableRow({ children: [
      makeCell("结构深化", 2500),
      makeCell("晶体结构深化、配合物结构深化", 4200),
      makeCell("从会算升级到会推断", 2650),
    ]}),
    new TableRow({ children: [
      makeCell("物化深化", 2500),
      makeCell("化学动力学深化、热力学与平衡深化", 4200),
      makeCell("只到初赛与高频竞赛题可用边界", 2650),
    ]}),
  ],
  [2500, 4200, 2650]
);

const round4Table = makeTable(
  [
    new TableRow({ tableHeader: true, children: [
      makeCell("编号", 900, { bold: true, shading: "EAF2F8", align: AlignmentType.CENTER }),
      makeCell("专题", 3300, { bold: true, shading: "EAF2F8" }),
      makeCell("作用", 2700, { bold: true, shading: "EAF2F8" }),
      makeCell("说明", 2450, { bold: true, shading: "EAF2F8" }),
    ]}),
    ["4-1", "高等有机：反应机理与轨道理论", "统一物理有机语言", "支撑 4-2、4-3"],
    ["4-2", "有机立体化学与构象分析", "解决近年立体热点", "冲刺高频页"],
    ["4-3", "人名反应系统归类", "零散反应压成机理族", "强调迁移"],
    ["4-4", "晶体结构深度与推断", "空间推断与投影判断", "高分结构区"],
    ["4-5", "配合物与配位化学深化", "磁性、JT、MO 级判断", "深化结构化学"],
    ["4-6", "元素化学深度与结构推断综合", "从记忆转向推断", "跨专题缝合"],
    ["4-7", "物化综合计算", "冲刺大分值综合计算", "热力学/电化学/动力学联立"],
    ["4-8", "近五年真题限时模拟", "真题验证与讲评收束", "第四轮总出口"],
  ].map((r) => new TableRow({ children: [makeCell(r[0], 900, { align: AlignmentType.CENTER }), makeCell(r[1], 3300), makeCell(r[2], 2700), makeCell(r[3], 2450)] })),
  [900, 3300, 2700, 2450]
);

const depthTable = makeTable(
  [
    new TableRow({ tableHeader: true, children: [
      makeCell("轮次", 1300, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
      makeCell("深度上限", 3400, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
      makeCell("教师提醒", 4600, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
    ]}),
    new TableRow({ children: [
      makeCell("第一轮", 1300, { bold: true }),
      makeCell("原则上不高于《普通化学原理》；结构、晶体、配位、电化学、水溶液平衡可适度加深到《无机化学》层次", 3400),
      makeCell("以建立语言和工具为主，禁止高阶理论挤占主线", 4600),
    ]}),
    new TableRow({ children: [
      makeCell("第二轮", 1300, { bold: true }),
      makeCell("系统讲元素化学与分析化学主线", 3400),
      makeCell("不再把分析化学主内容后拖到第三轮", 4600),
    ]}),
    new TableRow({ children: [
      makeCell("第三轮", 1300, { bold: true }),
      makeCell("有机系统、结构深化、物化深化", 3400),
      makeCell("允许机理与推导显著加深，但仍服务初赛主线", 4600),
    ]}),
    new TableRow({ children: [
      makeCell("第四轮", 1300, { bold: true }),
      makeCell("更深但不能更散，以冲刺专题和真题策略为核心", 3400),
      makeCell("不再新铺大量冷门知识", 4600),
    ]}),
    new TableRow({ children: [
      makeCell("第五轮+", 1300, { bold: true }),
      makeCell("决赛专题和前沿补强", 3400),
      makeCell("当前只保留方向，不在本版中展开细节", 4600),
    ]}),
  ],
  [1300, 3400, 4600]
);

const children = [
  p("中国化学奥林匹克全备课框架（教师查看版）", { heading: HeadingLevel.TITLE, align: AlignmentType.CENTER, size: 34 }),
  p("版本日期：2026-06-19", { align: AlignmentType.CENTER, size: 22, after: 80 }),
  p("用途：作为整体备课框架供教师查看，帮助快速理解从第一轮到第四轮的课程结构、深度边界与衔接逻辑；第五轮及后续方向仅作简要说明。", { after: 180 }),
  p("一、总览", { heading: HeadingLevel.HEADING_1 }),
  p("本框架采用“先基础语言、再系统专题、再深化迁移、最后冲刺缝合”的四轮主线结构。前四轮是当前的完整主线，第五轮及后续保留为决赛和个性化补强方向。"),
  overviewTable,
  p("二、跨轮次深度边界", { heading: HeadingLevel.HEADING_1 }),
  p("深度切分的核心原则是：同一知识点可以多轮次使用，但不同轮次只承担该轮的目标深度，避免提前展开高阶推导或冷门内容。"),
  depthTable,
  p("三、第一轮：化学原理与结构基础衔接", { heading: HeadingLevel.HEADING_1 }),
  p("第一轮的核心任务，是把学生从高中化学拉到竞赛化学的语言体系中。不是把所有知识点一次讲完，而是建立后续能不断复用的工具和表达。"),
  round1Table,
  bullet("教师提醒 1：第一轮默认采用“问题/现象 → 铺垫 → 推理 → 形成结论”的路径，不建议直接结论先行。"),
  bullet("教师提醒 2：方程式书写、量子数判断、复杂推导等，只作为服务主线的工具，不应喧宾夺主。"),
  bullet("教师提醒 3：第一轮课后材料，以帮助学生建立基本语言和计算规范为主。"),
  p("四、第二轮：元素化学与分析化学系统轮", { heading: HeadingLevel.HEADING_1 }),
  p("第二轮的任务，是让学生形成元素直觉和分析化学计算能力。它既是元素化学主干轮，也是后续陌生情境推断题的关键准备轮。"),
  round2Table,
  bullet("教师提醒 1：元素化学不应只停留在“记性质”，要训练颜色、沉淀、气体、价态变化等多信号综合判断。"),
  bullet("教师提醒 2：分析化学主内容在第二轮系统讲完，不再拖到第三轮。"),
  bullet("教师提醒 3：第二轮是从“会背”转向“会由现象推断”的关键轮。"),
  p("五、第三轮：有机系统与结构/物化深化", { heading: HeadingLevel.HEADING_1, pageBreakBefore: true }),
  p("第三轮是课程难度和专题密度显著上升的一轮。核心不只是内容增多，而是开始要求学生具备有机机理、结构推断和深化计算的连续思维能力。"),
  round3Table,
  bullet("教师提醒 1：第三轮有机要突出“电子效应 → 中间体 → 机理 → 选择性 → 合成”的主线。"),
  bullet("教师提醒 2：晶体和配位深化要从“会算”升级到“会推断”“会读图”“会组织分析语言”。"),
  bullet("教师提醒 3：物化深化仍然要守住初赛可考边界，不宜提前铺满决赛深水区。"),
  p("六、第四轮：冲刺缝合与高分区压缩", { heading: HeadingLevel.HEADING_1 }),
  p("第四轮不是再铺新一轮基础知识，而是把前三轮已经建立的工具、专题和思维，压缩成能直接应对高分题和真题模拟的综合判断链。"),
  round4Table,
  bullet("教师提醒 1：第四轮可以更深，但不能更散。"),
  bullet("教师提醒 2：优先做最能影响分界线的专题，不追求“背景越多越好”。"),
  bullet("教师提醒 3：真题模拟和讲评策略，本身就是第四轮的重要组成部分。"),
  p("七、第五轮及后续方向（简版）", { heading: HeadingLevel.HEADING_1 }),
  p("第五轮及后续阶段，主要面向决赛深水区、前沿专题与个性化补强。当前在教师查看版中只保留方向说明，不展开成完整专题表。"),
  bullet("可能内容：决赛结构化学、物理化学深化、前沿有机方法学、超分子化学、专题化实验思想。"),
  bullet("适用对象：已稳定完成前四轮主线，且需要继续向省队/决赛层推进的学生。"),
  bullet("当前建议：第五轮以后按具体教师资源、学生层次和真实竞赛目标单独规划。"),
  p("八、推荐使用方式", { heading: HeadingLevel.HEADING_1 }),
  bullet("第一次接手课程的老师：先看本文件，再分别看第一轮到第四轮总体框架。"),
  bullet("需要快速判断某一知识点该放哪一轮：先看本文件，再看“轮次深度切分总表”。"),
  bullet("需要知道当前哪些专题已经真正落地：看“备课与教学思路待办”。"),
  bullet("需要往下产出具体备课材料：按“总体框架 → 备课大纲 → 学生讲义”的顺序推进。"),
  p("九、当前执行口径", { heading: HeadingLevel.HEADING_1 }),
  p("截至 2026-06-19，当前课件主线只推进“备课大纲 + 学生讲义”。本文件是教师查看版总框架，目标是帮助统一理解课程结构，并不替代实时进度页。"),
];

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Microsoft YaHei", size: 22 },
      },
    },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        run: { font: "Microsoft YaHei", size: 40, bold: true, color: "1F1F1F" },
        paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 120, after: 200 }, outlineLevel: 0 },
      },
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { font: "Microsoft YaHei", size: 30, bold: true, color: "1F3B5B" },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 0 },
      },
    ],
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1200, bottom: 1440, left: 1200 },
        size: { orientation: PageOrientation.PORTRAIT },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "全备课框架（教师查看版）", size: 18, color: "666666" })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "第 ", size: 18, color: "666666" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "666666" }),
            new TextRun({ text: " 页", size: 18, color: "666666" }),
          ],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outFile, buffer);
  console.log(outFile);
});
