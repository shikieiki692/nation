/**
 * 模板：PPT 生成脚本（含 LaTeX 公式自动渲染）
 * ==========================================
 * 使用方式：
 *   1. 复制本文件到 pptx-workspace/ 目录
 *   2. 修改下方的「课程专属内容」区域
 *   3. 运行：node 你的脚本名.js
 *
 * 依赖安装（首次）：
 *   cd pptx-workspace
 *   npm install pptxgenjs katex sharp playwright
 *   npx playwright install chromium
 */

const { createPPT, makeHtmlSlide, defaultColors } = require('../11-模板/pptx-toolkit/ppt-engine.js');
const path = require('path');

// ==================== 课程专属内容（修改此处）====================

const OUTPUT_PATH = path.join(__dirname, '课件名称.pptx');
const COLORS = defaultColors; // 或自定义配色

// ---- 公式注册表：所有 LaTeX 公式在此注册 ----
const formulas = {
    // 示例：f_前缀 + 语义命名
    // f_ideal_gas: 'pV = nRT',
    // f_dalton: 'p_i = p_{\\text{总}} \\cdot x_i',
};

// ---- 幻灯片定义 ----
const slides = [
    // 示例 1：纯文字幻灯片
    {
        type: 'html',
        html: makeHtmlSlide({
            title: '课件标题',
            contentHtml: `
<p style="font-size:18pt; text-align:center; margin-top:60pt;">
  副标题或课程信息
</p>`,
            colors: COLORS
        })
    },

    // 示例 2：带 LaTeX 公式的幻灯片
    {
        type: 'html',
        html: makeHtmlSlide({
            title: '核心公式',
            contentHtml: `
<div style="margin-top:60pt;">
  <p style="font-size:14pt;">这里是文字说明...</p>
</div>`,
            colors: COLORS
        }),
        formulas: [
            // { key: 'f_ideal_gas', x: 2, y: 0.8, h: 0.5 },
        ]
    },

    // 示例 3：表格幻灯片
    {
        type: 'table',
        title: '对比表格',
        tableData: [
            [
                { text: "列A", options: { fill: { color: COLORS.tableHeader }, color: "FFFFFF", bold: true } },
                { text: "列B", options: { fill: { color: COLORS.tableHeader }, color: "FFFFFF", bold: true } },
            ],
            ["数据1", "数据2"],
        ],
        tableOptions: {
            x: 0.5, y: 1.2, w: 9, h: 2,
            border: { pt: 1, color: "CCCCCC" },
            fill: { color: "F5F5F5" },
            fontSize: 12
        }
    },
];

// ==================== 主程序（一般无需修改）====================

async function main() {
    await createPPT({
        title: '课件标题',
        outputPath: OUTPUT_PATH,
        formulas: formulas,
        formulaOptions: { fontSize: 16, color: '333333' },
        slides: slides,
        colors: COLORS
    });
}

main().catch(console.error);
