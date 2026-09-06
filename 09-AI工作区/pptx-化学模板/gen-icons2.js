// Round 2: extra header icons + hex-corner decoration PNG.
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const path = require('path');
const Lu = require('react-icons/lu');

const OUT = path.join(__dirname, 'icons');

async function rasterizeIcon(Icon, color, filename) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(Icon, { color: `#${color}`, size: '256', strokeWidth: 2 })
  );
  await sharp(Buffer.from(svg)).png().toFile(path.join(OUT, filename));
}

// Flat-top hexagon path, radius R, center (cx, cy)
function hexPath(cx, cy, r) {
  const pts = [];
  for (let k = 0; k < 6; k++) {
    const a = (Math.PI / 3) * k;
    pts.push(`${(cx + r * Math.cos(a)).toFixed(1)},${(cy + r * Math.sin(a)).toFixed(1)}`);
  }
  return `M${pts.join('L')}Z`;
}

async function makeHexCorner() {
  // 180pt x 150pt @ 4px/pt = 720 x 600 px, stroke 4px (=1pt)
  const W = 720, H = 600, R = 130;
  const dx = 1.5 * R;          // flat-top horizontal spacing
  const dy = Math.sqrt(3) * R; // flat-top vertical spacing
  const centers = [
    [250, 230],
    [250 + dx, 230 + dy / 2],
    [250 + 2 * dx, 230],
    [250 + dx, 230 - dy / 2]
  ];
  const paths = centers.map(([cx, cy]) => `<path d="${hexPath(cx, cy, R)}"/>`).join('');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
    <g fill="none" stroke="#E4EAE4" stroke-width="4">${paths}</g>
  </svg>`;
  await sharp(Buffer.from(svg)).png().toFile(path.join(OUT, 'hex-corner.png'));
}

async function main() {
  await rasterizeIcon(Lu.LuList, '1B4332', 'LuList-1B4332.png');
  await rasterizeIcon(Lu.LuPlus, '1B4332', 'LuPlus-1B4332.png');
  await rasterizeIcon(Lu.LuLayoutGrid, '1B4332', 'LuLayoutGrid-1B4332.png');
  await makeHexCorner();
  console.log('done');
}

main().catch(e => { console.error(e); process.exit(1); });
