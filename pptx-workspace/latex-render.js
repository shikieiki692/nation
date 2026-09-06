const katex = require('katex');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const cacheDir = path.join(__dirname, 'formula-cache');
if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir, { recursive: true });

/**
 * 将 LaTeX 公式渲染为 PNG 图片
 * @param {string} latex - LaTeX 代码（不需要包裹 $ 或 $$）
 * @param {object} options - 配置
 * @returns {string} - PNG 文件路径
 */
async function renderLatex(latex, options = {}) {
    const {
        fontSize = 16,
        color = '333333',
        scale = 2,
        displayMode = true
    } = options;

    // 生成缓存 key
    const cacheKey = require('crypto').createHash('md5')
        .update(`${latex}_${fontSize}_${color}_${displayMode}`)
        .digest('hex');
    const pngPath = path.join(cacheDir, `${cacheKey}.png`);

    // 如果已缓存，直接返回
    if (fs.existsSync(pngPath)) return pngPath;

    // KaTeX 渲染为 HTML（含 SVG）
    const katexHtml = katex.renderToString(latex, {
        throwOnError: true,
        displayMode: displayMode,
        output: 'html'
    });

    // 计算渲染尺寸（估算）
    // 每个字符约 fontSize*1.5 px，分数/根号等复杂结构额外乘2
    const complexityFactor = latex.includes('\\frac') || latex.includes('\\sqrt') || latex.includes('\\dfrac') ? 2.5 : 1.5;
    const estimatedWidth = Math.min(700, Math.max(120, latex.length * fontSize * complexityFactor));
    const estimatedHeight = displayMode ? fontSize * 4 * scale : fontSize * 2.5 * scale;

    // 构建完整 SVG
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${estimatedWidth}" height="${estimatedHeight}"
         style="background-color:transparent;"
         viewBox="0 0 ${estimatedWidth} ${estimatedHeight}"
         preserveAspectRatio="xMidYMid meet"
         overflow="visible"
         font-size="${fontSize}"
    >
      <style>
        .katex { font-size: ${fontSize}pt !important; }
        .katex .base { color: #${color} !important; }
        .katex .mord { color: #${color} !important; }
        .katex .mop { color: #${color} !important; }
        .katex .mrel { color: #${color} !important; }
        .katex .mbin { color: #${color} !important; }
        .katex .mopen { color: #${color} !important; }
        .katex .mclose { color: #${color} !important; }
        .katex .mpunct { color: #${color} !important; }
        .katex .minner { color: #${color} !important; }
        .katex .msubsup { color: #${color} !important; }
        .katex .frac-line { border-color: #${color} !important; }
        .katex .overline .overline-line,
        .katex .underline .underline-line { border-color: #${color} !important; }
        .katex .sqrt > .root { color: #${color} !important; }
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

    // Sharp 转 PNG（高 DPI）
    await sharp(Buffer.from(svg))
        .resize({
            width: estimatedWidth,
            height: estimatedHeight,
            fit: 'inside'
        })
        .png()
        .toFile(pngPath);

    return pngPath;
}

/**
 * 批量渲染公式字典
 * @param {object} formulas - { key: latexString, ... }
 * @returns {object} - { key: pngPath, ... }
 */
async function renderBatch(formulas, options = {}) {
    const results = {};
    for (const [key, latex] of Object.entries(formulas)) {
        results[key] = await renderLatex(latex, options);
    }
    return results;
}

/**
 * 获取图片实际尺寸（用于等比缩放）
 */
async function getImageDimensions(pngPath) {
    const meta = await sharp(pngPath).metadata();
    return { width: meta.width, height: meta.height };
}

module.exports = { renderLatex, renderBatch, getImageDimensions };
