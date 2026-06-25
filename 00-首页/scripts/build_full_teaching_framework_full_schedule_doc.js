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
const outFile = path.join(outDir, "2026-06-20-全备课框架-逐课完整版-增广版.docx");

fs.mkdirSync(outDir, { recursive: true });

const border = { style: BorderStyle.SINGLE, size: 1, color: "C7CED6" };
const cellBorders = { top: border, bottom: border, left: border, right: border };

const p = (text, opts = {}) =>
  new Paragraph({
    spacing: { after: opts.after ?? 120, before: opts.before ?? 0 },
    alignment: opts.align ?? AlignmentType.LEFT,
    heading: opts.heading,
    pageBreakBefore: opts.pageBreakBefore ?? false,
    children: opts.runs || [new TextRun({ text, bold: opts.bold, size: opts.size ?? 22 })],
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
        spacing: { after: 50, before: 50 },
        alignment: opts.align ?? AlignmentType.LEFT,
        children: [
          new TextRun({
            text,
            bold: !!opts.bold,
            size: opts.size ?? 18,
          }),
        ],
      }),
    ],
  });

const makeTable = (rows, widths) =>
  new Table({
    columnWidths: widths,
    width: { size: 100, type: WidthType.PERCENTAGE },
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    rows,
  });

const scheduleTable = (rows) =>
  makeTable(
    [
      new TableRow({
        tableHeader: true,
        children: [
          makeCell("课次", 900, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
          makeCell("专题 / 模块", 2100, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
          makeCell("本节讲什么", 3900, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
          makeCell("本节重心", 2300, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
          makeCell("承接 / 备注", 2300, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
        ],
      }),
      ...rows.map((row) =>
        new TableRow({
          children: [
            makeCell(row.lesson, 900, { align: AlignmentType.CENTER }),
            makeCell(row.module, 2100),
            makeCell(row.content, 3900),
            makeCell(row.focus, 2300),
            makeCell(row.note, 2300),
          ],
        })
      ),
    ],
    [900, 2100, 3900, 2300, 2300]
  );

const overviewTable = makeTable(
  [
    new TableRow({
      tableHeader: true,
      children: [
        makeCell("轮次", 1100, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
        makeCell("定位", 2800, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
        makeCell("建议课量", 1500, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
        makeCell("这一轮主要解决什么", 4600, { bold: true, shading: "DDEBF7", align: AlignmentType.CENTER }),
      ],
    }),
    ["第一轮", "原理与结构语言衔接", "16 节", "把学生从高中化学带入竞赛语言，建立计量、气体与溶液、周期律、酸碱、热力学、电化学、结构和配位的基础工具"],
    ["第二轮", "元素化学与分析化学系统轮", "16 节", "形成元素直觉、现象信号识别能力，以及滴定/误差/分光光度法的系统分析能力"],
    ["第三轮", "有机系统 + 结构/物化深化", "22 节", "建立有机机理主线，补齐波谱、晶体、配位、动力学与热力学深化，形成综合推断能力"],
    ["第四轮", "冲刺缝合与高分区压缩", "12 节", "围绕机理证据、立体、结构推断、物化综合和真题模拟，压缩为比赛可调用的判断链"],
    ["第五轮+", "决赛与后续拓展", "略", "仅保留方向，不在本版逐节展开"],
  ].map((r, i) =>
    i === 0
      ? r
      : new TableRow({
          children: [
            makeCell(r[0], 1100, { bold: true }),
            makeCell(r[1], 2800),
            makeCell(r[2], 1500, { align: AlignmentType.CENTER }),
            makeCell(r[3], 4600),
          ],
        })
  ),
  [1100, 2800, 1500, 4600]
);

const round1 = [
  ["1", "化学计量总入口", "有效数字、物质的量五量关系、配平、限量试剂、产率、组成与平均式、守恒思想", "先把所有定量题都拉回到 n、方程式和守恒", "覆盖化学原理 01 与计量主干"],
  ["2", "气体与化学计量", "理想气体方程、密度形式、Avogadro 视角、摩尔体积、化合体积定律、气体计量综合", "把计算工具和气体模型接通", "覆盖化学原理 02 的基础主线"],
  ["3", "气体与溶液", "Dalton 分压、排水集气校正、浓度换算、气体扩散、速率分布直觉、压缩因子入口、分子量测定", "把气体题从套公式提升为条件判断", "补足普化原理中常见但上一版未显式承接的点"],
  ["4", "溶液与物质状态", "分散相/连续相、溶解度、Henry 定律、Raoult 定律、稀溶液通性、溶剂极性、溶剂化/疏水作用", "让溶液不只剩浓度换算", "覆盖化学原理 03 并服务分析化学"],
  ["5", "原子结构 I", "能层、能级、轨道图像、电子排布、量子数作标签、失电子顺序、核外电子组织", "把高中电子层语言升级为轨道语言", "覆盖化学原理 04/09 的前半"],
  ["6", "原子结构 II 与周期律", "原子半径、电离能、电子亲合能、电负性、s/p/d/f 区、元素分区、周期反常、基础元素推断", "用电子结构解释性质变化", "后续 Lewis 酸碱、配位、元素化学都要复用"],
  ["7", "酸碱理论 I", "Brønsted 酸碱、Lewis 酸碱、HSAB、Ka/Kb、pH、共轭酸碱对、解离常数语言", "建立三套酸碱语言的入口", "覆盖化学原理 05 的概念层"],
  ["8", "酸碱理论 II", "缓冲溶液、两性物种、多元酸近似、酸碱平衡简算、结构与酸碱性、滴定前置视角", "把酸碱题真正做成可算可解释", "为第二轮滴定曲线与指示剂选择做前置"],
  ["9", "热力学 I", "体系与环境、状态函数、量热、内能、焓、热化学方程式、Hess 定律、生成焓", "先有热量账本，再谈自发性", "覆盖化学原理 06 的前半"],
  ["10", "热力学 II", "键焓、熵、Gibbs 自由能、标准态、生化标准态入口、Born-Haber 入口、自发性与方向判断", "把热力学从放热/吸热升级成统一判据", "为平衡、电化学、元素稳定性做桥梁"],
  ["11", "动力学与平衡入口", "速率、速率方程、反应级数直觉、Arrhenius 方程、活化能、指前因子、碰撞/能量剖面", "让学生先区分快慢和彻底", "覆盖化学动力学基础而避免拆成过薄小课"],
  ["12", "化学平衡", "K/Q、Le Châtelier、Ksp、稳定常数、多重平衡基础、平衡与热力学关系", "形成平衡的统一问题意识", "覆盖化学原理 07 并承接第二轮滴定与配位分析"],
  ["13", "氧化还原与电化学 I", "氧化态、半反应工具、原电池、标准电极电势、反应方向、ΔG/K/E 对照", "把配平降级成工具，把电势升成主线", "服务元素化学与滴定分析"],
  ["14", "氧化还原与电化学 II", "Nernst 方程、pH/浓度/分压影响、化学电源、电解入口、法拉第观念", "建立可迁移的电化学计算模型", "覆盖化学原理 08 的广度面"],
  ["15", "分子结构与化学键", "Lewis 结构、结构表达、形式电荷、共振、VSEPR、杂化、等电子体、离子/共价/金属键、偶极矩与分子极性", "形成结构题最常用的判断语言", "覆盖化学原理 10/11 与有机 21/23 的前置"],
  ["16", "结构综合与预热", "分子轨道初步、氢键/范德华力、对称操作入口、晶胞与堆积入口、配位键/命名/螯合效应、有机结构预热", "用一节课把第一轮结构线收束成后续入口", "第一轮收束课，兼顾有机与无机桥梁"],
].map(([lesson, module, content, focus, note]) => ({ lesson, module, content, focus, note }));

const round2 = [
  ["1", "元素化学总入口 + 氢卤素", "元素直觉方法、氢的特殊性、氢化物、卤素通性、互化物、含氧酸、拟卤素、歧化反应", "先建立读元素题的视角，再进具体族", "从最经典的主族信号入手"],
  ["2", "氧族与氮族 I", "H2S、SO2、SO3、硫代硫酸盐、过二硫酸盐、NOx、NH3、N2H4、HN3", "抓住氧化还原、配位和气体信号三条线", "高频真题来源之一"],
  ["3", "氧族与氮族 II + 磷体系", "硝酸体系、铵盐、磷单质与氧化物、正偏焦磷酸、缩合关系、磷氮硫交叉现象", "把价态、结构、酸碱和缩合统一起来", "用结构语言服务元素化学"],
  ["4", "碳硅硼铝主线", "CO/CO2、碳酸盐、氰化物、硅酸盐、Sn/Pb 价态、硼烷、硼酸、铝的两性、对角线规则", "让主族化学不只剩方程式记忆", "补足结构化解释的广度"],
  ["5", "碱金属碱土与稀有气体", "氢化物、过氧化物/超氧化物、焰色、硫酸盐/碳酸盐溶解度、Be/Al 与 Li/Mg、Xe 化合物、晶格能直觉", "把普通主族题和陌生结构题连起来", "Xe/VSEPR 是后续结构推断桥梁"],
  ["6", "过渡金属 I", "Ti、V、Cr、Mn 的价态、颜色、氧化性、配位倾向、重要工业/滴定情境", "颜色信号和氧化态变化同讲", "过渡金属主线入口"],
  ["7", "过渡金属 II", "Fe、Co、Ni、Cu、Zn 的变价、配位、磁性直觉、歧化/两性/电池与催化应用", "把元素题和配位题打通", "第二轮高频得分区"],
  ["8", "过渡金属 III + 深度桥梁", "Ag、Au、Hg、Mo、W、多酸、镧系收缩、稀土入口、铂族催化与元素深度视角", "补足第二轮元素面的上沿", "为第四轮元素深度留桥梁而不抢跑"],
  ["9", "元素推断方法课", "颜色、沉淀、气体、配位、价态变化、结构信号的组合判断", "从背性质转成读题链", "第二轮最关键的方法课"],
  ["10", "元素推断综合实战", "实验叙事、真题切片、单质制备与方程式书写、陌生物质到元素和方程式的完整推断", "训练完整表达和路径比较", "第二轮能力出口"],
  ["11", "容量分析总论与酸碱滴定 I", "基准物质、标准溶液、PBE/分布分数、滴定逻辑、活度直觉、指示剂来源", "建立分析化学语言，不把滴定只做成套公式", "结合书籍提炼补厚课堂内容"],
  ["12", "酸碱滴定 II", "滴定曲线、弱酸/多元酸、终点误差、双指示剂法、缓冲容量、PBE/CBE 直觉、分别滴定判别", "让曲线、平衡和误差三件事合在一起讲", "原版过薄，这里做成完整大课"],
  ["13", "氧化还原与沉淀滴定", "碘量法、KMnO4 法、Mohr/Volhard/Fajans、介质控制、电子守恒与终点判断", "把电化学基础迁移到分析化学", "分析化学核心综合课"],
  ["14", "络合滴定与重量分析", "EDTA、条件稳定常数、金属指示剂、封闭与僵化、掩蔽与解蔽、重量分析、称量形式", "把配位平衡和实验操作结果挂起来", "与第二轮配位/元素线相互支撑"],
  ["15", "误差处理与分光光度法", "准确度/精密度、偏差/误差、标准曲线、线性回归、Lambert-Beer、差示分光入口、方法选择", "让数据处理成为分析化学主线的一部分", "补足课堂广度和实验表达"],
  ["16", "第二轮综合收束", "分析化学综合题、元素-分析联动题、第二轮结业讲评与方法回收", "把元素直觉和定量分析真正缝合", "第二轮总结课"],
].map(([lesson, module, content, focus, note]) => ({ lesson, module, content, focus, note }));

const round3 = [
  ["1", "第三轮起步", "结构表达、命名、sp3/σ 键、构象、pKa 与有机酸碱入口、最小有机图景", "先把学生带入第三轮语言，不急着上难机理", "参考学而思批次 A 的进入顺序"],
  ["2", "电子效应与反应性", "诱导、共轭、超共轭、共振论、前线轨道、稳定性、芳香性与酸碱性判断", "把电子效应做成全轮通用语言", "服务后续所有机理与选择性"],
  ["3", "立体化学与构象基础", "结构表达、异构现象、互变异构、E/Z、D/L、手性中心/轴、R/S、Fischer/Newman、环己烷构象", "重新校准空间语言", "第三轮高频基础课"],
  ["4", "选择性与立体结果", "反应立体化学、syn/anti、Markovnikov/反 Markovnikov、1,2/1,4、软硬亲核试剂、构象影响", "把区域/立体选择性讲成判断链", "为取代、加成、周环铺路"],
  ["5", "活性中间体与能量图", "反应本质、机理表示、碳正/负离子、自由基、卡宾、苯炔、过渡态、Hammond、动力学/热力学控制", "把机理图背后的能量语言讲清", "第三轮机理总入口"],
  ["6", "SN/E 竞争系统", "SN1、SN2、E1、E2、E1cb、邻基参与、位阻/溶剂/离去基/碱性综合判断", "不把取代消除切得过碎", "参考学而思批次 B 的打包方式"],
  ["7", "烯烃炔烃加成系统", "亲电加成、马氏/反马氏、溴鎓离子、环氧化/臭氧解、共轭二烯、炔烃水合与还原、端炔酸性", "把加成规则和路径切换一起讲", "兼顾后续合成工具"],
  ["8", "羰基化学 I", "亲核加成、缩醛/亚胺/烯胺、Wittig、Grignard 加成、氧化/还原、酰基亲核取代与保护基", "把羰基题最常见的两三类路径先立起来", "第三轮有机中轴之一"],
  ["9", "羰基化学 II 与缩合", "烯醇/烯醇负离子、羰基α位反应、Aldol、Claisen、Mannich、Knoevenagel、安息香与极性翻转", "把 C-C 键构建系统讲完", "参考学而思批次 D/E 与 ABOC"],
  ["10", "重排反应", "1,2-迁移、Pinacol、Semipinacol、Beckmann、Baeyer-Villiger、Brook、Favorskii、Curtius/Hofmann", "把重排按缺电子中心与迁移类型组织", "为第四轮人名反应打底"],
  ["11", "芳香反应", "芳香性、Friedel-Crafts、EAS 定位、NAS、苯炔、Birch、Vilsmeier、杂环定位差异", "把芳香体系从背定位变成会解释", "兼顾后续杂环与波谱题"],
  ["12", "周环反应", "电环化、Diels-Alder、1,3-偶极环加成、σ 迁移、Ene、轨道对称性基础", "周环单列成完整大课而不再拆碎", "第三轮高频热点"],
  ["13", "自由基反应", "链式反应、选择性、Barton、环化、Baldwin 规则、光氧化还原、Norrish/NHC-硼入口", "把自由基从口诀课变成体系课", "对应近年命题热点"],
  ["14", "逆合成与合成设计", "逆合成、FGA、切断策略、合成子/等价体、保护基、多步路线、官能团互变", "从单反应过渡到设计路线", "第三轮综合能力课"],
  ["15", "金属有机与偶联", "有机锂、Grignard、Gilman、Suzuki、Heck、Negishi、Stille、18 电子规则入口", "补足第三轮后段工具箱", "连接有机与配位化学"],
  ["16", "杂原子与特殊体系", "膦化合物、含硫/含硅体系、杂环、叶立德、特殊官能团化学", "把常见但分散的特殊体系集中收口", "提升课堂广度"],
  ["17", "糖氨基酸高分子与超分子", "糖的构型与变旋、还原糖、等电点、肽键/Edman、高分子结构、分子识别与超分子入口", "少考但必须建立系统入口", "第三轮有机收束课"],
  ["18", "有机波谱与结构确证", "IR、1H/13C NMR、MS、UV-Vis 的最小可用框架，结构确定与机理辅助证据", "补上原版明显不足的广度", "覆盖有机 30 并连接题目阅读"],
  ["19", "晶体结构深化", "对称性、7 大晶系、Bravais 点阵、堆积、典型晶体结构、原子坐标、Bragg/XRD 入口", "从会记模型升级到会推结构", "第三轮结构深化上半"],
  ["20", "配位化学深化", "晶体场/配体场、光谱化学序列、CFSE、Jahn-Teller、磁性、取代机理与几何构型推断", "把配位题拉到高分区层次", "第三轮结构深化下半"],
  ["21", "动力学深化", "积分速率方程、半衰期、初速法/级数判断、Arrhenius、稳态近似、催化、过渡态语言", "形成规范的物化计算与机理语言", "为第四轮综合计算预热"],
  ["22", "热力学与平衡深化", "化学势、van't Hoff、Clausius-Clapeyron、蒸气压/沸点升高/凝固点降低/渗透压", "把物化后半段真正系统讲完", "第三轮总结课"],
].map(([lesson, module, content, focus, note]) => ({ lesson, module, content, focus, note }));

const round4 = [
  ["1", "高等有机 I", "标记实验、交叉实验、Hammett、KIE、活化熵、酸碱催化、立体化学作为机理证据", "先把‘怎么判断机理’讲清，而不只讲结论", "参考 Clayden 第39章的证据组织方式"],
  ["2", "高等有机 II", "Curtin-Hammett、Bent 规则、轨道对称性、非经典中间体、卡宾/氮宾/苯炔与材料型机理推断", "从会写机理升级到会读材料和会解释", "第四轮有机总入口"],
  ["3", "立体与构象深化", "A 值、中环张力、阻转异构、轴手性、环翻转、动态立体化学与低温谱学直觉", "把构象分析推进到定量与动态层", "立体冲刺上半"],
  ["4", "不对称合成与选择性模型", "Felkin-Anh、Cram 螯合、Evans 助剂、Sharpless/Jacobsen、CBS/BINAP、选择性模型比较", "让立体化学真正服务反应设计", "补足原版立体课的宽度"],
  ["5", "人名反应系统 I", "Pinacol/Beckmann/Baeyer-Villiger/Curtius/Hofmann 等迁移族、骨架重排、缩环扩环判别", "不再按字母背诵，而按机理族组织", "对应人名反应归类上半"],
  ["6", "人名反应系统 II", "Aldol/Claisen/Mannich 族、Claisen/Cope 周环族、光化学族、Suzuki/Heck/Negishi 偶联族", "形成完整的人名反应地图", "对应人名反应归类下半"],
  ["7", "晶体结构深度与推断", "投影图还原三维、晶系判断、钙钛矿/尖晶石/MAX-MXene、缺陷化学、XRD 指标化基础", "把近年晶体题高频考法压成判断流程", "结构冲刺核心课"],
  ["8", "配位化学冲刺", "MO 层面的 σ/π 成键、18 电子与稀土视角、磁性、自旋交叉、Jahn-Teller、反位效应", "把配位题提升到真正的深水区", "结构高分区核心课"],
  ["9", "元素化学深度与结构推断", "多酸、Zintl 相、金属-金属多重键、镧系收缩、铂族催化、Latimer/Frost/Ellingham、陌生物质推断", "把元素题从背诵型推进到推断型", "第四轮元素综合课"],
  ["10", "物化综合计算", "BDE 循环、热力学-电化学-动力学联立、电池容量与能量密度、相平衡/依数性接口、综合计算讲评", "把计算题真正做成冲分课", "第四轮计算核心课"],
  ["11", "真题限时模拟", "近五年真题整卷或半卷限时、答题顺序、时间分配、过程分追踪", "让前面专题回到真实比赛场景", "完整模拟执行"],
  ["12", "真题讲评与冲刺策略", "逐题讲评、命题思路拆解、专题回扣、错因归档、最后一轮策略复盘", "把冲刺专题收束为比赛界面", "第四轮总结课"],
].map(([lesson, module, content, focus, note]) => ({ lesson, module, content, focus, note }));

const children = [
  p("中国化学奥林匹克全备课框架（逐课完整版·增广版）", { heading: HeadingLevel.TITLE, align: AlignmentType.CENTER, size: 34 }),
  p("版本日期：2026-06-20", { align: AlignmentType.CENTER, size: 22, after: 60 }),
  p("用途：作为教师查看用的完整排课版本，重点回答“每一节课讲什么”。本版在大课口径基础上继续按考纲条目和资料提炼增广课堂覆盖面，不再只停留在专题名，而是尽量把每节课应当承接的知识点簇直接写进排课表。", { after: 160 }),
  p("一、总览", { heading: HeadingLevel.HEADING_1 }),
  p("整体结构按照“第一轮打语言、第二轮建直觉、第三轮成体系、第四轮做冲刺”的主线排布。前四轮逐节展开，第五轮及之后仅保留方向说明。与上一版相比，本版继续减少偏碎课次，并把考纲、教材和网课中原本被轻触或漏掉的广度点更明确地补入每一轮。"),
  overviewTable,
  p("二、修订原则", { heading: HeadingLevel.HEADING_1 }),
  bullet("一节课不再对应单一 KP，而要同时容纳主线概念、支撑工具、代表题型和易错点/跨模块连接。"),
  bullet("优先按认知问题打包，而不是按教材章节名词切得过碎。"),
  bullet("凡是考纲明写、书籍有稳定章节、网课有成熟讲法的内容，原则上都应在相应轮次留下课堂入口，并尽量在表里显式写出。"),
  bullet("第三轮与第四轮尤其避免“只剩专题名”，而要保证学生在课堂上真正见到方法、例题、证据和结构化判断。"),
  p("三、使用说明", { heading: HeadingLevel.HEADING_1 }),
  bullet("这份文档优先服务教师快速把握全课程，不替代单专题备课大纲。"),
  bullet("每一轮内部按“课次 - 专题 - 本节讲什么 - 本节重心 - 承接关系”排布。"),
  bullet("如果实际班级课时长度不同，可按专题边界压缩或合并，但建议尽量保留每节课的重心顺序。"),
  p("四、第一轮逐课排布（16 节）", { heading: HeadingLevel.HEADING_1 }),
  p("第一轮解决的是语言和工具问题。学生在这一轮不需要见到全部深水区，但必须把计量、气体与溶液、周期律、酸碱、电化学、结构和配位的基础表达练到顺手；因此每节课都应是一个能独立成型的知识包，而不是只有一个名词标题。"),
  scheduleTable(round1),
  p("五、第二轮逐课排布（16 节）", { heading: HeadingLevel.HEADING_1, pageBreakBefore: true }),
  p("第二轮解决的是元素直觉和分析化学计算。元素化学不再只讲“记性质”，而要训练由颜色、沉淀、气体、配位和价态变化反推元素与反应链；分析化学也不应只剩公式，而要保留曲线、误差、条件控制和方法选择。"),
  scheduleTable(round2),
  p("六、第三轮逐课排布（22 节）", { heading: HeadingLevel.HEADING_1, pageBreakBefore: true }),
  p("第三轮是系统化的一轮。有机机理、波谱、结构深化和物化深化在这里同时成形，重心是让学生具备连续推理能力，而不是继续做碎片化记忆；因此本版将原先偏碎的若干有机小课重新打包成更完整的反应族与方法课。"),
  scheduleTable(round3),
  p("七、第四轮逐课排布（12 节）", { heading: HeadingLevel.HEADING_1, pageBreakBefore: true }),
  p("第四轮是冲刺压缩轮。这里不是重新铺知识，而是把前三轮内容重新整理成比赛时能直接调用的判断链、专题界面和真题策略；同时保留足够的课堂厚度，让每节课都能真正完成一次高价值的冲刺训练。"),
  scheduleTable(round4),
  p("八、第五轮及之后（简述）", { heading: HeadingLevel.HEADING_1 }),
  bullet("第五轮以后主要面向决赛深水区、前沿专题、个性化补强。"),
  bullet("这部分建议按教师资源和学生层次单独规划，不纳入本版逐节排布。"),
  bullet("若后续要继续扩写，可在本版结构上增补“决赛版逐课排布”。"),
];

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Microsoft YaHei", size: 20 },
      },
    },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        run: { font: "Microsoft YaHei", size: 40, bold: true, color: "1F1F1F" },
        paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 120, after: 180 }, outlineLevel: 0 },
      },
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { font: "Microsoft YaHei", size: 28, bold: true, color: "1F3B5B" },
        paragraph: { spacing: { before: 220, after: 140 }, outlineLevel: 0 },
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          margin: { top: 1100, right: 900, bottom: 1100, left: 900 },
          size: { orientation: PageOrientation.LANDSCAPE },
        },
      },
      headers: {
        default: new Header({
          children: [
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              children: [new TextRun({ text: "全备课框架（逐课完整版·增广版）", size: 18, color: "666666" })],
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [
                new TextRun({ text: "第 ", size: 18, color: "666666" }),
                new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "666666" }),
                new TextRun({ text: " 页", size: 18, color: "666666" }),
              ],
            }),
          ],
        }),
      },
      children,
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outFile, buffer);
  console.log(outFile);
});
