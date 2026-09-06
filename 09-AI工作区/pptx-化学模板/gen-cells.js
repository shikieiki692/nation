// 拟真周期表单元格 PNG（预渲染旋转+阴影，供深色页使用）
const sharp = require('sharp');
const path = require('path');

const OUT = path.join(__dirname, 'icons');

// 元素数据
const ELEMENTS = {
  H:  { num: '1',  name: '氢', mass: '1.008' },
  C:  { num: '6',  name: '碳', mass: '12.01' },
  O:  { num: '8',  name: '氧', mass: '16.00' },
  Na: { num: '11', name: '钠', mass: '22.99' }
};

// size 单位 pt；渲染 4px/pt
function cellSvg(sym, size, bg, rotateDeg) {
  const S = size * 4;                 // 格子边长 px
  const C = Math.round(S * 1.5);      // 画布（留旋转+阴影余量）
  const pad = (C - S) / 2;
  const el = ELEMENTS[sym];
  const fontNum = Math.round(S * 0.106);   // ≈11pt
  const fontSym = Math.round(S * 0.375);   // ≈39pt
  const fontBot = Math.round(S * 0.092);   // ≈9.5pt
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${C}" height="${C}">
  <defs>
    <filter id="sh" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="10" dy="12" stdDeviation="12" flood-color="#0B241A" flood-opacity="0.35"/>
    </filter>
  </defs>
  <g transform="rotate(${rotateDeg} ${C / 2} ${C / 2})">
    <rect x="${pad}" y="${pad}" width="${S}" height="${S}" rx="${Math.round(S * 0.045)}"
      fill="${bg}" stroke="rgba(250,247,240,0.65)" stroke-width="${Math.round(S * 0.014)}" filter="url(#sh)"/>
    <text x="${pad + S * 0.07}" y="${pad + S * 0.14}" font-family="Microsoft YaHei"
      font-size="${fontNum}" fill="rgba(250,247,240,0.85)">${el.num}</text>
    <text x="${pad + S / 2}" y="${pad + S * 0.63}" font-family="Arial, Microsoft YaHei" font-weight="bold"
      font-size="${fontSym}" fill="#FAF7F0" text-anchor="middle">${sym}</text>
    <text x="${pad + S / 2}" y="${pad + S * 0.91}" font-family="Microsoft YaHei"
      font-size="${fontBot}" fill="rgba(250,247,240,0.72)" text-anchor="middle">${el.name} ${el.mass}</text>
  </g>
</svg>`;
}

const CELLS = [
  // 封面（一大三小错落）
  { file: 'cell-H-104.png', sym: 'H', size: 104, bg: '#2D6A4F', rot: -6 },
  { file: 'cell-O-96.png',  sym: 'O', size: 96,  bg: '#24573F', rot: 5 },
  { file: 'cell-C-92.png',  sym: 'C', size: 92,  bg: '#2D6A4F', rot: -4 },
  { file: 'cell-Na-88.png', sym: 'Na', size: 88, bg: '#24573F', rot: 7 },
  // 章节过渡页（2 个中小格）
  { file: 'cell-H-84.png',  sym: 'H', size: 84,  bg: '#2D6A4F', rot: -5 },
  { file: 'cell-C-64.png',  sym: 'C', size: 64,  bg: '#24573F', rot: 6 },
  // 结尾页（2 个小格）
  { file: 'cell-H-64.png',  sym: 'H', size: 64,  bg: '#2D6A4F', rot: -6 },
  { file: 'cell-O-52.png',  sym: 'O', size: 52,  bg: '#24573F', rot: 5 }
];

async function main() {
  for (const c of CELLS) {
    await sharp(Buffer.from(cellSvg(c.sym, c.size, c.bg, c.rot)))
      .png()
      .toFile(path.join(OUT, c.file));
    console.log('made', c.file);
  }
}

main().catch(e => { console.error(e); process.exit(1); });
