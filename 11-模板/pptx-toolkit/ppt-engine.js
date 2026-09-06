/**
 * PPT 生成引擎（全局工具）
 * ==========================================
 * 位置：11-模板/pptx-toolkit/ppt-engine.js
 * 用途：封装 html2pptx + PptxGenJS + LaTeX 公式插入的通用逻辑
 * 依赖：pptxgenjs, latex-render.js
 *
 * 设计哲学：
 * - 幻灯片内容用 HTML 定义（文字、布局）
 * - 公式用 LaTeX 定义，自动渲染为 PNG 后通过 addImage 插入
 * - 表格直接在 PptxGenJS 层面添加（最稳定）
 */

const Module = require('module');
const fallbackNodeModules = [
    'C:\\Obsidion\\妙妙屋\\pptx-workspace\\node_modules',
    'C:\\Obsidion\\妙妙屋\\.claude\\node_modules'
];

const existingNodePath = process.env.NODE_PATH ? process.env.NODE_PATH.split(';').filter(Boolean) : [];
process.env.NODE_PATH = [...new Set([...fallbackNodeModules, ...existingNodePath])].join(';');
Module._initPaths();

function requireWithFallback(moduleName, fallbackPath) {
    try {
        return require(moduleName);
    } catch (error) {
        if (!fallbackPath) throw error;
        return require(fallbackPath);
    }
}

const pptxgen = requireWithFallback(
    'pptxgenjs',
    'C:\\Obsidion\\妙妙屋\\pptx-workspace\\node_modules\\pptxgenjs'
);
const html2pptx = require('C:\\Users\\蕾赛\\.claude\\skills\\pptx\\scripts\\html2pptx.js');
const { renderBatch, calcImageSize } = require('./latex-render.js');
const fs = require('fs');
const path = require('path');

// 默认配色方案
const defaultColors = {
    primary: '1C3F60',
    accent: 'E07A5F',
    text: '333333',
    lightText: '666666',
    bg: 'FFFFFF',
    tableHeader: '1C3F60',
    tableAlt: 'F0F4F8'
};

/**
 * 生成标准 16:9 HTML 幻灯片的辅助函数
 */
function makeHtmlSlide({ title, contentHtml, extraStyle = '', colors = defaultColors }) {
    return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
html { background: #${colors.bg}; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #${colors.bg}; font-family: Arial, sans-serif;
  display: flex; flex-direction: column;
}
.header { background: #${colors.primary}; padding: 12pt 30pt; }
.header h1 { color: #FFFFFF; font-size: 22pt; margin: 0; }
.content { margin: 15pt 30pt; flex: 1; }
${extraStyle}
</style>
</head>
<body>
<div class="header"><h1>${title}</h1></div>
<div class="content">${contentHtml}</div>
</body>
</html>`;
}

/**
 * 创建完整 PPT
 * @param {object} config
 *   @param {string} config.title - PPT 标题
 *   @param {string} config.outputPath - 输出文件路径
 *   @param {object} config.formulas - { key: latexString } 公式注册表
 *   @param {object} config.formulaOptions - 传给 renderBatch 的选项
 *   @param {Array} config.slides - 幻灯片定义数组
 *     每个元素：{ type: 'html'|'table', ... }
 *       - type: 'html' → { html: string, formulas?: [{ key, x, y, h }] }
 *       - type: 'table' → { tableData, tableOptions }
 *   @param {object} config.colors - 自定义配色（可选）
 * @returns {Promise>string>} - 输出文件路径
 */
async function createPPT(config) {
    const {
        title,
        outputPath,
        formulas = {},
        formulaOptions = {},
        slides = [],
        colors = defaultColors
    } = config;

    const workDir = path.dirname(outputPath);
    const cacheDir = path.join(workDir, 'formula-cache');

    // Step 1: 批量渲染公式
    console.log('[PPT Engine] 渲染 LaTeX 公式...');
    const fPaths = await renderBatch(formulas, { cacheDir, ...formulaOptions });
    console.log(`[PPT Engine] ✓ ${Object.keys(fPaths).length} 个公式已渲染`);

    // Step 2: 初始化 PPT
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.title = title;
    pptx.author = 'Claudian';

    // Step 3: 逐页生成
    const htmlFiles = [];
    for (let i = 0; i < slides.length; i++) {
        const slideDef = slides[i];
        const htmlPath = path.join(workDir, `_slide_${i + 1}.html`);

        if (slideDef.type === 'html') {
            fs.writeFileSync(htmlPath, slideDef.html);
            htmlFiles.push(htmlPath);
            await html2pptx(htmlPath, pptx);
        } else if (slideDef.type === 'table') {
            // 表格页：先写空 HTML（只保留标题），再叠加表格
            const emptyHtml = makeHtmlSlide({
                title: slideDef.title,
                contentHtml: '<div id="table-area" style="width:660pt;height:280pt;background:#F0F4F8;"></div>',
                colors
            });
            fs.writeFileSync(htmlPath, emptyHtml);
            htmlFiles.push(htmlPath);
            await html2pptx(htmlPath, pptx);

            const slideObj = pptx.getSlide(i);
            slideObj.addTable(slideDef.tableData, slideDef.tableOptions);
        }
    }

    // Step 4: 插入公式图片
    for (let i = 0; i < slides.length; i++) {
        const slideDef = slides[i];
        if (!slideDef.formulas || slideDef.formulas.length === 0) continue;

        const slideObj = pptx.getSlide(i);
        for (const f of slideDef.formulas) {
            const pngPath = fPaths[f.key];
            if (!pngPath) {
                console.warn(`[PPT Engine] ⚠ 公式 key="${f.key}" 未在注册表中找到`);
                continue;
            }
            const size = await calcImageSize(pngPath, f.h);
            slideObj.addImage({
                path: pngPath,
                x: f.x,
                y: f.y,
                w: size.width,
                h: size.height
            });
        }
    }

    // Step 5: 保存
    await pptx.writeFile({ fileName: outputPath });
    console.log(`[PPT Engine] ✅ PPT 已保存: ${outputPath}`);

    // 清理临时 HTML
    for (const f of htmlFiles) {
        try { fs.unlinkSync(f); } catch (e) { /* ignore */ }
    }

    return outputPath;
}

module.exports = { createPPT, makeHtmlSlide, defaultColors };
