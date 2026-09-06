/**
 * LaTeX 公式渲染引擎（全局工具）
 * ==========================================
 * 位置：11-模板/pptx-toolkit/latex-render.js
 * 用途：将 LaTeX 公式渲染为 PNG 图片，供 PPT 插入使用
 * 依赖：katex, sharp
 *
 * 使用方法：
 *   const { renderLatex, renderBatch, getImageDimensions } = require('路径/latex-render.js');
 *   const pngPath = await renderLatex('\\mathrm{pH} = \\mathrm{p}K_a', { fontSize: 16 });
 */

function requireWithFallback(moduleName, fallbackPath) {
    try {
        return require(moduleName);
    } catch (error) {
        if (!fallbackPath) throw error;
        return require(fallbackPath);
    }
}

const katex = requireWithFallback(
    'katex',
    'C:\\Obsidion\\妙妙屋\\pptx-workspace\\node_modules\\katex'
);
const sharp = requireWithFallback(
    'sharp',
    'C:\\Obsidion\\妙妙屋\\pptx-workspace\\node_modules\\sharp'
);
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 默认缓存目录：与脚本同级目录下的 formula-cache/
const defaultCacheDir = path.join(__dirname, 'formula-cache');

/**
 * 将 LaTeX 公式渲染为 PNG 图片
 * @param {string} latex - LaTeX 代码（不需要包裹 $ 或 $$）
 * @param {object} options - 配置
 *   @param {number} options.fontSize - 字体大小（pt），默认 16
 *   @param {string} options.color - 字体颜色（RGB 不含 #），默认 '333333'
 *   @param {number} options.scale - 渲染缩放倍数，默认 2（高 DPI）
 *   @param {boolean} options.displayMode - 是否为行间公式，默认 true
 *   @param {string} options.cacheDir - 缓存目录，默认 formula-cache/
 * @returns {string} - PNG 文件绝对路径
 */
async function renderLatex(latex, options = {}) {
    const {
        fontSize = 16,
        color = '333333',
        scale = 2,
        displayMode = true,
        cacheDir = defaultCacheDir
    } = options;

    if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir, { recursive: true });

    // 缓存 key = MD5(latex + fontSize + color + displayMode)
    const cacheKey = crypto.createHash('md5')
        .update(`${latex}_${fontSize}_${color}_${displayMode}`)
        .digest('hex');
    const pngPath = path.join(cacheDir, `${cacheKey}.png`);

    // 已缓存则直接返回
    if (fs.existsSync(pngPath)) return pngPath;

    // KaTeX 渲染为 HTML（内含 SVG）
    const katexHtml = katex.renderToString(latex, {
        throwOnError: true,
        displayMode: displayMode,
        output: 'html'
    });

    // 估算渲染尺寸
    // 每个字符约 fontSize*1.5 px；分数/根号等复杂结构额外乘 2.5
    const hasComplex = /\\(frac|sqrt|dfrac|overline|underline|int|sum|prod)/.test(latex);
    const complexityFactor = hasComplex ? 2.5 : 1.5;
    const estimatedWidth = Math.min(700, Math.max(120, latex.length * fontSize * complexityFactor));
    const estimatedHeight = displayMode ? fontSize * 4 * scale : fontSize * 2.5 * scale;

    // 构建 SVG（透明背景，字体颜色强制统一）
    const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${estimatedWidth}" height="${estimatedHeight}"
     style="background-color:transparent;"
     viewBox="0 0 ${estimatedWidth} ${estimatedHeight}"
     preserveAspectRatio="xMidYMid meet"
     overflow="visible"
>
  <style>
    .katex { font-size: ${fontSize}pt !important; }
    .katex * { color: #${color} !important; }
    .katex .frac-line { border-color: #${color} !important; }
    .katex .overline .overline-line,
    .katex .underline .underline-line { border-color: #${color} !important; }
    .katex .sqrt > .vlist-t { border-color: #${color} !important; }
  </style>
  <foreignObject x="0" y="0" width="100%" height="100%"
                 requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
  >
    <div xmlns="http://www.w3.org/1999/xhtml"
         style="display:inline-block; padding: 5px;"
    >
      ${katexHtml}
    </div>
  </foreignObject>
</svg>`;

    // Sharp 转 PNG
    await sharp(Buffer.from(svg))
        .resize({ width: estimatedWidth, height: estimatedHeight, fit: 'inside' })
        .png()
        .toFile(pngPath);

    return pngPath;
}

/**
 * 批量渲染公式字典
 * @param {object} formulas - { key: latexString, ... }
 * @param {object} options - 传给 renderLatex 的选项
 * @returns {object} - { key: pngPath, ... }
 */
async function renderBatch(formulas, options = {}) {
    const results = {};
    const entries = Object.entries(formulas);
    for (const [key, latex] of entries) {
        results[key] = await renderLatex(latex, options);
    }
    return results;
}

/**
 * 获取图片实际尺寸（用于等比缩放）
 * @param {string} pngPath
 * @returns {object} - { width, height }
 */
async function getImageDimensions(pngPath) {
    const meta = await sharp(pngPath).metadata();
    return { width: meta.width, height: meta.height };
}

/**
 * 计算等比缩放后的尺寸
 * @param {string} pngPath
 * @param {number} targetHeight - 目标高度（英寸）
 * @returns {object} - { width, height }
 */
async function calcImageSize(pngPath, targetHeight) {
    const dim = await getImageDimensions(pngPath);
    const aspect = dim.width / dim.height;
    // PptxGenJS 使用英寸，图片尺寸是像素，需要 DPI 换算
    // 这里假设 96 DPI（浏览器默认）
    const h = targetHeight;
    const w = h * aspect;
    return { width: w, height: h };
}

module.exports = {
    renderLatex,
    renderBatch,
    getImageDimensions,
    calcImageSize
};
