// P8 中心科学图骨架：连线 + 圆（文字由 HTML 原生叠加）
const sharp = require('sharp');
const path = require('path');

const SCALE = 4; // 4px/pt
const W = 640 * SCALE, H = 280 * SCALE;
const C = { x: 320, y: 140, r: 45 };
const SATS = [
  [320, 28], [110, 86], [530, 86], [110, 194], [530, 194], [320, 252]
];
const SR = 27;

function spoke(sx, sy) {
  const dx = sx - C.x, dy = sy - C.y;
  const d = Math.hypot(dx, dy);
  const ux = dx / d, uy = dy / d;
  const x1 = C.x + ux * C.r, y1 = C.y + uy * C.r;
  const x2 = sx - ux * SR, y2 = sy - uy * SR;
  return `<line x1="${x1 * SCALE}" y1="${y1 * SCALE}" x2="${x2 * SCALE}" y2="${y2 * SCALE}" stroke="#2D6A4F" stroke-width="6"/>`;
}

const spokes = SATS.map(([x, y]) => spoke(x, y)).join('');
const sats = SATS.map(([x, y]) =>
  `<circle cx="${x * SCALE}" cy="${y * SCALE}" r="${SR * SCALE}" fill="#FFFFFF" stroke="#2D6A4F" stroke-width="10"/>`
).join('');
const center = `<circle cx="${C.x * SCALE}" cy="${C.y * SCALE}" r="${C.r * SCALE}" fill="#1B4332"/>`;

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">${spokes}${sats}${center}</svg>`;

sharp(Buffer.from(svg)).png().toFile(path.join(__dirname, 'images', 'p8-spokes.png'))
  .then(() => console.log('p8-spokes.png done'))
  .catch(e => { console.error(e); process.exit(1); });
