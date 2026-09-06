const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require('C:\\Users\\蕾赛\\.claude\\skills\\pptx\\scripts\\html2pptx.js');
const { renderBatch, getImageDimensions } = require('./latex-render.js');

const workDir = 'C:\\Obsidion\\妙妙屋\\pptx-workspace';

// ========== 配色 ==========
const colors = {
    primary: '1C3F60',
    accent: 'E07A5F',
    text: '333333',
    lightText: '666666',
    bg: 'FFFFFF',
    tableHeader: '1C3F60',
    tableAlt: 'F0F4F8'
};

// ========== 公式注册表（LaTeX） ==========
const formulas = {
    // Slide 7: 边界判据
    f_h3o_sqrt: '\\mathrm{[H_3O^+]} = \\sqrt{K_a \\cdot c}',
    f_cka_cond: 'c/K_a \\geq 400',
    f_h3o_wrong: '\\mathrm{[H^+]} = 2.1 \\times 10^{-2} \\ > \\ 0.010',
    f_h3o_correct: '\\mathrm{[H^+]} = 8.4 \\times 10^{-3}',

    // Slide 8: 缓冲溶液
    f_hh_equation: '\\mathrm{pH} = \\mathrm{p}K_a + \\lg\\dfrac{[\\mathrm{A}^-]}{[\\mathrm{HA}]}',
    f_buffer_range: '\\mathrm{pH} = \\mathrm{p}K_a \\pm 1',

    // Slide 11: 例题3
    f_ex3_1: '\\mathrm{pH} = 4.76 + \\lg(1) = 4.76',
    f_ex3_2: '\\mathrm{pH} = 4.85\\ (+0.09)',
    f_ex3_3: '\\mathrm{pH} = 11.99\\ (+7.23)',
};

// ========== HTML 生成辅助函数 ==========
function makeHeader(title) {
    return `<div class="header"><h1>${title}</h1></div>`;
}

function makeStyle(extra = '') {
    return `<style>
html { background: #${colors.bg}; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #${colors.bg}; font-family: Arial, sans-serif;
  display: flex; flex-direction: column;
}
.header { background: #${colors.primary}; padding: 12pt 30pt; }
.header h1 { color: #FFFFFF; font-size: 22pt; margin: 0; }
.content { margin: 15pt 30pt; flex: 1; }
${extra}
</style>`;
}

// ========== Slide 1: 标题页 ==========
const slide1 = `<!DOCTYPE html>
<html><head><style>
html { background: #${colors.bg}; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #${colors.primary}; font-family: Arial, sans-serif;
  display: flex; flex-direction: column; justify-content: center; align-items: center;
}
h1 { color: #FFFFFF; font-size: 42pt; margin: 0 0 20pt 0; text-align: center; }
h2 { color: #E07A5F; font-size: 22pt; margin: 0 0 30pt 0; text-align: center; font-weight: normal; }
.info { color: #CCCCCC; font-size: 14pt; text-align: center; }
</style></head>
<body>
<h1>酸碱理论（深化版）</h1>
<h2>Arrhenius → Brønsted → Lewis → HSAB</h2>
<div class="info"><p>提高班 | 120 min | 化学原理</p></div>
</body></html>`;

// ========== Slide 2: 核心结论 ==========
const slide2 = `<!DOCTYPE html>
<html><head>${makeStyle(`
.point { background: #F0F4F8; border-left: 6pt solid #${colors.accent}; padding: 10pt 15pt; margin-bottom: 12pt; }
.point p { color: #${colors.text}; font-size: 13pt; margin: 0; line-height: 1.5; }
.point-num { color: #${colors.accent}; font-weight: bold; font-size: 15pt; }
`)} </head>
<body>
${makeHeader('核心结论（先记住这三句话）')}
<div class="content">
<div class="point"><p><span class="point-num">1.</span> 酸和碱没有绝对定义，只有适用场景。三种理论是<strong>递进扩容</strong>关系，不是互相推翻。</p></div>
<div class="point"><p><span class="point-num">2.</span> "硬亲硬、软亲软"的本质是<strong>键型匹配</strong>：硬-硬→离子键；软-软→共价键。</p></div>
<div class="point"><p><span class="point-num">3.</span> 计算前先判据：c/Ka ≥ 400 才可用简化公式，否则可能得出 [H⁺] > c 的荒谬结果。</p></div>
</div>
</body></html>`;

// ========== Slide 3: 理论演进 ==========
const slide3 = `<!DOCTYPE html>
<html><head>${makeStyle(`
.step { margin-bottom: 5pt; }
.step-title { color: #${colors.primary}; font-size: 12pt; font-weight: bold; margin: 0; }
.step-desc { color: #${colors.text}; font-size: 11pt; margin: 0; margin-left: 10pt; }
.arrow { color: #${colors.accent}; font-size: 11pt; margin: 0; margin-left: 10pt; margin-bottom: 5pt; }
.relation { background: #${colors.accent}; color: #FFFFFF; padding: 5pt 10pt; border-radius: 4pt; font-size: 12pt; font-weight: bold; margin-top: 8pt; }
`)} </head>
<body>
${makeHeader('理论演进脉络')}
<div class="content">
<div class="step"><p class="step-title">Arrhenius（1887）：酸 = 电离出 H⁺，碱 = 电离出 OH⁻</p></div>
<p class="arrow">↓ 局限：无法解释 NH₃ 的碱性、非水体系</p>
<div class="step"><p class="step-title">Brønsted（1923）：酸 = 质子给体，碱 = 质子受体</p></div>
<p class="arrow">↓ 局限：无法解释 BF₃ + NH₃（无质子转移）</p>
<div class="step"><p class="step-title">Lewis（1923）：酸 = 电子对受体，碱 = 电子对给体</p></div>
<p class="arrow">↓ 局限：过于宽泛，缺乏定量标度</p>
<div class="step"><p class="step-title">HSAB（1963）：在 Lewis 基础上按极化难易分类酸碱</p></div>
<div class="relation"><p>关系：Arrhenius ⊂ Brønsted ⊂ Lewis</p></div>
</div>
</body></html>`;

// ========== Slide 4: 拉平效应（占位符，表格由 PptxGenJS 填充）==========
const slide4 = `<!DOCTYPE html>
<html><head>${makeStyle(`.placeholder { width: 660pt; height: 280pt; background: #F0F4F8; }`)} </head>
<body>
${makeHeader('拉平效应 vs 区分效应')}
<div class="content"><div id="table1" class="placeholder"></div></div>
</body></html>`;

// ========== Slide 5: HSAB分类（占位符）==========
const slide5 = `<!DOCTYPE html>
<html><head>${makeStyle(`.placeholder { width: 660pt; height: 280pt; background: #F0F4F8; }`)} </head>
<body>
${makeHeader('软硬酸碱（HSAB）分类')}
<div class="content"><div id="table2" class="placeholder"></div></div>
</body></html>`;

// ========== Slide 6: HSAB核心规则 ==========
const slide6 = `<!DOCTYPE html>
<html><head>${makeStyle(`
.rule {
  background: #${colors.accent}; color: #FFFFFF;
  padding: 15pt 20pt; border-radius: 8pt;
  font-size: 22pt; font-weight: bold; text-align: center;
  margin-bottom: 20pt;
}
.origin { margin-bottom: 15pt; }
.origin-title { color: #${colors.primary}; font-size: 16pt; font-weight: bold; }
.origin-desc { color: #${colors.text}; font-size: 13pt; margin-left: 10pt; }
`)} </head>
<body>
${makeHeader('HSAB 核心规则与物理起源')}
<div class="content">
<div class="rule"><p>硬亲硬，软亲软</p></div>
<div class="origin">
<p class="origin-title">硬-硬匹配</p>
<p class="origin-desc">电荷密度高 → 静电作用主导 → 离子键倾向</p>
</div>
<div class="origin">
<p class="origin-title">软-软匹配</p>
<p class="origin-desc">易极化 → 轨道重叠大 → 共价键倾向</p>
</div>
<p style="color:#666666; font-size:12pt; margin-top:15pt;"><i>注意：硬软与强弱无关！H⁺ 是极硬的酸，但也是极强的酸。</i></p>
</div>
</body></html>`;

// ========== Slide 7: 简化公式边界判据（公式由 addImage 插入）==========
const slide7 = `<!DOCTYPE html>
<html><head>${makeStyle(`
.content { margin: 100pt 30pt 15pt 30pt; }
.warning { background: #FFF3E0; border-left: 6pt solid #FF9800; padding: 8pt 12pt; margin-bottom: 10pt; }
.warning p { color: #${colors.text}; font-size: 11pt; margin: 0; line-height: 1.5; }
`)} </head>
<body>
${makeHeader('简化公式的边界判据（最关键）')}
<div class="content">
<div class="warning">
<p><b>反例</b>：0.010 mol/L 二氯代乙酸（Ka = 4.5×10⁻²）</p>
<p>c/Ka = 0.22 ≪ 400 ❌ 不可用简化公式</p>
<p>若错误使用：[H⁺] = 2.1×10⁻² > 0.010（荒谬！）</p>
<p>精确解：[H⁺] = 8.4×10⁻³，α = 84%</p>
</div>
<p style="color:#666666; font-size:10pt; margin:0;">判据来源：α ≤ 5% 时，c/Ka = (1-α)/α² ≈ 400</p>
</div>
</body></html>`;

// ========== Slide 8: 缓冲溶液（公式由 addImage 插入）==========
const slide8 = `<!DOCTYPE html>
<html><head>${makeStyle(`
.content { margin: 90pt 30pt 15pt 30pt; }
.mechanism { margin-bottom: 10pt; }
.mechanism p { color: #${colors.text}; font-size: 12pt; margin: 0; line-height: 1.5; }
.range { background: #E8F5E9; padding: 10pt 15pt; border-radius: 4pt; }
.range p { color: #2E7D32; font-size: 13pt; margin: 0; }
`)} </head>
<body>
${makeHeader('缓冲溶液与 Henderson-Hasselbalch 方程')}
<div class="content">
<div class="mechanism">
<p><b>缓冲作用机制：</b></p>
<p>外加 H⁺ → 被共轭碱 A⁻ 消耗 → A⁻ + H⁺ → HA</p>
<p>外加 OH⁻ → 被弱酸 HA 消耗 → HA + OH⁻ → A⁻ + H₂O</p>
<p>稀释 → 比值不变 → pH 不变</p>
</div>
<div class="range">
<p>有效缓冲范围：pH = pKa ± 1</p>
<p>缓冲容量最大条件：[A⁻] = [HA]（即 pH = pKa）</p>
</div>
</div>
</body></html>`;

// ========== Slide 9: 例题1 ==========
const slide9 = `<!DOCTYPE html>
<html><head>${makeStyle(`
.label p { color: #${colors.accent}; font-size: 14pt; font-weight: bold; margin-bottom: 8pt; }
.question { background: #F0F4F8; padding: 12pt; border-radius: 4pt; margin-bottom: 12pt; }
.question p { color: #${colors.text}; font-size: 13pt; margin: 0; line-height: 1.5; }
.hint p { color: #${colors.lightText}; font-size: 12pt; margin: 0; }
.answer { background: #E8F5E9; padding: 10pt 15pt; border-radius: 4pt; }
.answer p { color: #2E7D32; font-size: 13pt; margin: 0; }
`)} </head>
<body>
${makeHeader('例题 1：拉平效应与区分效应')}
<div class="content">
<div class="label"><p>⭐⭐⭐ 概念深化</p></div>
<div class="question"><p>在液氨溶剂中，HAc 是强酸；在水中，HAc 是弱酸。解释这一现象，并说明这是拉平效应还是区分效应的体现。</p></div>
<div class="hint"><p>提示：液氨的碱性比水强 → NH₃ 接受质子能力更强 → HAc 在液氨中几乎完全电离</p></div>
<div class="answer">
<p><b>答案</b>：液氨将 HAc "拉平"到 NH₄⁺ 的酸性水平 → <b>拉平效应</b></p>
<p>对比：水对 HAc 具有<b>区分效应</b>（HAc 只部分电离，Ka = 1.8×10⁻⁵）</p>
</div>
</div>
</body></html>`;

// ========== Slide 10: 例题2 ==========
const slide10 = `<!DOCTYPE html>
<html><head>${makeStyle(`
.label p { color: #${colors.accent}; font-size: 14pt; font-weight: bold; margin-bottom: 8pt; }
.question { background: #F0F4F8; padding: 12pt; border-radius: 4pt; margin-bottom: 12pt; }
.question p { color: #${colors.text}; font-size: 13pt; margin: 0; line-height: 1.5; }
.answer { background: #E8F5E9; padding: 10pt 15pt; border-radius: 4pt; }
.answer p { color: #2E7D32; font-size: 12pt; margin: 0; line-height: 1.6; }
`)} </head>
<body>
${makeHeader('例题 2：HSAB 预测配合物稳定性')}
<div class="content">
<div class="label"><p>⭐⭐⭐ 综合应用</p></div>
<div class="question"><p>解释为什么 [Ag(CN)₂]⁻ 的稳定常数远大于 [Ag(NH₃)₂]⁺？为什么 FeF₃ 比 FeI₃ 更稳定？</p></div>
<div class="answer">
<p><b>[Ag(CN)₂]⁻</b>：Ag⁺（软酸）+ CN⁻（软碱）→ 软-软匹配 → 共价键成分大 → 稳定性高</p>
<p><b>[Ag(NH₃)₂]⁺</b>：Ag⁺（软酸）+ NH₃（硬碱）→ 软-硬不匹配 → 稳定性较低</p>
<p><b>FeF₃</b>：Fe³⁺（硬酸）+ F⁻（硬碱）→ 硬-硬匹配 → 离子键 → 晶格能大 → 稳定</p>
<p><b>FeI₃</b>：Fe³⁺（硬酸）+ I⁻（软碱）→ 硬-软不匹配 → 极不稳定，自发分解</p>
</div>
</div>
</body></html>`;

// ========== Slide 11: 例题3（占位符，表格由 PptxGenJS 填充，公式用图片）==========
function makeSlide11(fPaths) {
    return `<!DOCTYPE html>
<html><head>${makeStyle(`
.label p { color: #${colors.accent}; font-size: 14pt; font-weight: bold; margin-bottom: 8pt; }
.placeholder { width: 660pt; height: 240pt; background: #F0F4F8; }
`)} </head>
<body>
${makeHeader('例题 3：缓冲溶液综合计算')}
<div class="content">
<div class="label"><p>⭐⭐⭐⭐ 综合推断 + 定量计算</p></div>
<div id="table3" class="placeholder"></div>
</div>
</body></html>`;
}

// ========== Slide 12: 易错点（占位符）==========
const slide12 = `<!DOCTYPE html>
<html><head>${makeStyle(`.placeholder { width: 660pt; height: 280pt; background: #F0F4F8; }`)} </head>
<body>
${makeHeader('易错点预警')}
<div class="content"><div id="table4" class="placeholder"></div></div>
</body></html>`;

// ========== Slide 13: 总结 ==========
const slide13 = `<!DOCTYPE html>
<html><head><style>
html { background: #${colors.bg}; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #${colors.primary}; font-family: Arial, sans-serif;
  display: flex; flex-direction: column; justify-content: center; align-items: center;
}
h1 { color: #FFFFFF; font-size: 32pt; margin: 0 0 30pt 0; text-align: center; }
.summary { color: #FFFFFF; font-size: 16pt; text-align: center; margin-bottom: 15pt; }
.accent { color: #E07A5F; font-weight: bold; }
</style></head>
<body>
<h1>课堂总结</h1>
<div class="summary">
<p>三大理论是<span class="accent">递进扩容</span>，不是互相推翻</p>
<p>看到"质子转移"用 Brønsted，看到"配位键"用 Lewis，看到"稳定性"用 HSAB</p>
<p>计算前先判 <span class="accent">c/Ka ≥ 400</span>，拒绝盲目套公式</p>
<p>缓冲溶液的有效范围 = <span class="accent">pKa ± 1</span></p>
</div>
<div class="summary">
<p style="font-size:14pt; color:#CCCCCC;">下节课：配位化学与配合物结构</p>
</div>
</body></html>`;

// ==================== 主程序 ====================
async function main() {
    console.log('Step 1: 渲染 LaTeX 公式...');
    const fPaths = await renderBatch(formulas, { fontSize: 16, color: '333333' });
    console.log(`  ✓ 共渲染 ${Object.keys(fPaths).length} 个公式`);

    // 构建动态幻灯片
    const slides = [
        slide1, slide2, slide3, slide4, slide5, slide6,
        slide7, slide8, slide9, slide10,
        makeSlide11(fPaths), slide12, slide13
    ];

    const slideFiles = [];
    for (let i = 0; i < slides.length; i++) {
        const filePath = path.join(workDir, `slide-l${i + 1}.html`);
        fs.writeFileSync(filePath, slides[i]);
        slideFiles.push(filePath);
    }

    console.log('Step 2: 生成 PPT...');
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.title = '酸碱理论（深化版）';
    pptx.author = 'Claudian';

    for (let i = 0; i < slideFiles.length; i++) {
        await html2pptx(slideFiles[i], pptx);
    }

    // Slide 4: 拉平效应表格
    const slide4_obj = pptx.getSlide(3);
    slide4_obj.addTable([
        [
            { text: "概念", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } },
            { text: "定义", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } },
            { text: "典型实例", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } }
        ],
        [
            { text: "拉平效应", options: { bold: true } },
            "溶剂将不同强度的酸/碱拉到同一水平",
            "水中 HCl、HBr、HNO₃、HClO₄ 都表现为 H₃O⁺ 的酸性（pKa ≈ −1.7）"
        ],
        [
            { text: "区分效应", options: { bold: true } },
            "溶剂能区分不同酸/碱的强度",
            "冰醋酸中：HClO₄ > HBr > H₂SO₄ > HCl > HNO₃"
        ]
    ], {
        x: 0.5, y: 1.2, w: 9, h: 2.5,
        colW: [2, 3, 4.5],
        border: { pt: 1, color: "CCCCCC" },
        fill: { color: "F5F5F5" },
        align: "left",
        valign: "middle",
        fontSize: 12
    });

    // Slide 5: HSAB分类表格
    const slide5_obj = pptx.getSlide(4);
    slide5_obj.addTable([
        [
            { text: "", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } },
            { text: "硬", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } },
            { text: "边界", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } },
            { text: "软", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } }
        ],
        [
            { text: "酸", options: { bold: true } },
            "H⁺, Li⁺, Na⁺, Mg²⁺, Al³⁺, Fe³⁺, BF₃",
            "Fe²⁺, Co²⁺, Ni²⁺, Cu²⁺, Zn²⁺",
            "Cu⁺, Ag⁺, Au⁺, Hg²⁺, Pt²⁺, BH₃"
        ],
        [
            { text: "碱", options: { bold: true } },
            "F⁻, OH⁻, H₂O, NH₃, CO₃²⁻, NO₃⁻, O²⁻",
            "Br⁻, NO₂⁻, SO₃²⁻, pyridine",
            "I⁻, S²⁻, CN⁻, CO, R₂S, PR₃, C₂H₄"
        ]
    ], {
        x: 0.5, y: 1.2, w: 9, h: 2,
        colW: [1.5, 3.5, 2.5, 2.5],
        border: { pt: 1, color: "CCCCCC" },
        fill: { color: "F5F5F5" },
        align: "left",
        valign: "middle",
        fontSize: 11
    });

    // Slide 7: 添加 LaTeX 公式图片
    const slide7_obj = pptx.getSlide(6);
    const dim7a = await getImageDimensions(fPaths.f_h3o_sqrt);
    const h7a = 0.45;
    const w7a = h7a * (dim7a.width / dim7a.height);
    slide7_obj.addImage({ path: fPaths.f_h3o_sqrt, x: (10 - w7a) / 2, y: 0.85, w: w7a, h: h7a });

    const dim7b = await getImageDimensions(fPaths.f_cka_cond);
    const h7b = 0.35;
    const w7b = h7b * (dim7b.width / dim7b.height);
    slide7_obj.addImage({ path: fPaths.f_cka_cond, x: (10 - w7b) / 2, y: 1.35, w: w7b, h: h7b });

    // Slide 8: 添加 LaTeX 公式图片
    const slide8_obj = pptx.getSlide(7);
    const dim8a = await getImageDimensions(fPaths.f_hh_equation);
    const h8a = 0.45;
    const w8a = h8a * (dim8a.width / dim8a.height);
    slide8_obj.addImage({ path: fPaths.f_hh_equation, x: (10 - w8a) / 2, y: 0.85, w: w8a, h: h8a });

    // Slide 11: 例题3表格（含公式图片）
    const slide11_obj = pptx.getSlide(10);
    slide11_obj.addTable([
        [
            { text: "步骤", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } },
            { text: "计算内容", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } },
            { text: "结果", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } }
        ],
        [
            "(1)",
            "缓冲溶液 pH（H-H 方程）",
            "pH = 4.76"
        ],
        [
            "(2)",
            "加入 NaOH 后新 pH",
            "pH = 4.85（变化仅 +0.09）"
        ],
        [
            "(3)",
            "HCl 溶液加入等量 NaOH",
            "pH = 11.99（变化 +7.23）"
        ]
    ], {
        x: 0.5, y: 1.2, w: 9, h: 2.2,
        colW: [1, 4.5, 3.5],
        border: { pt: 1, color: "CCCCCC" },
        fill: { color: "F5F5F5" },
        align: "left",
        valign: "middle",
        fontSize: 12
    });

    // Slide 12: 易错点表格
    const slide12_obj = pptx.getSlide(11);
    slide12_obj.addTable([
        [
            { text: "错误想法", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } },
            { text: "正确理解", options: { fill: { color: colors.tableHeader }, color: "FFFFFF", bold: true } }
        ],
        [
            "强酸的共轭碱也强",
            "HCl 是强酸，Cl⁻ 是极弱碱（Ka·Kb = Kw）"
        ],
        [
            "硬 = 强，软 = 弱",
            "硬软是极化难易，与酸碱强度无关"
        ],
        [
            "简化公式总是对的",
            "先判 c/Ka ≥ 400，否则解二次方程"
        ],
        [
            "pH = 7 就是中性",
            "100°C 时中性 pH ≈ 6.13"
        ]
    ], {
        x: 0.5, y: 1.2, w: 9, h: 2.5,
        colW: [3.5, 5.5],
        border: { pt: 1, color: "CCCCCC" },
        fill: { color: "F5F5F5" },
        align: "left",
        valign: "middle",
        fontSize: 12
    });

    const outputPath = path.join(workDir, '酸碱理论-提高班-LaTeX.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`\n✅ PPT saved to: ${outputPath}`);
    console.log(`📊 Total slides: ${slides.length}`);
    console.log(`📝 LaTeX formulas rendered: ${Object.keys(fPaths).length}`);
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
