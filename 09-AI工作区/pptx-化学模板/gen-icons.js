// Rasterize Lucide icons (react-icons/lu) to PNG via Sharp, per html2pptx.md.
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const Lu = require('react-icons/lu');

const OUT = path.join(__dirname, 'icons');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT);

// icon name -> list of hex colors (no #)
const PLAN = {
  // white (for orange label chips / dark-green strips)
  LuBookOpen: ['FFFFFF', '1B4332'],
  LuAtom: ['FFFFFF', '1B4332'],
  LuSearch: ['FFFFFF', '1B4332'],
  LuSigma: ['FFFFFF', '1B4332'],
  LuPenLine: ['FFFFFF', '1B4332'],
  LuFlaskConical: ['FFFFFF', '1B4332'],
  LuTestTubes: ['FFFFFF', '1B4332'],
  LuChartColumn: ['FFFFFF', '1B4332'],
  LuNetwork: ['FFFFFF', '1B4332'],
  LuHistory: ['FFFFFF', '1B4332'],
  LuTable: ['FFFFFF', '1B4332'],
  LuTarget: ['FFFFFF', '1B4332', 'E8A33D'],
  LuTimer: ['FFFFFF', '1B4332', 'E8A33D'],
  LuLightbulb: ['FFFFFF', '1B4332', 'B45309', 'E8A33D'],
  LuTriangleAlert: ['FFFFFF', '1B4332', 'C0392B'],
  // library page extras (green only)
  LuFlaskRound: ['1B4332'],
  LuFlame: ['1B4332'],
  LuPipette: ['1B4332'],
  LuCheck: ['1B4332'],
  LuX: ['1B4332'],
  LuGraduationCap: ['1B4332'],
  LuMicroscope: ['1B4332']
};

async function rasterize(IconComponent, color, filename) {
  const svgString = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, {
      color: `#${color}`,
      size: '256',
      // Lucide default stroke-width is 2 -> 统一 2px 线宽
      strokeWidth: 2
    })
  );
  await sharp(Buffer.from(svgString)).png().toFile(filename);
}

async function main() {
  const missing = [];
  for (const [name, colors] of Object.entries(PLAN)) {
    const Icon = Lu[name];
    if (!Icon) { missing.push(name); continue; }
    for (const color of colors) {
      const file = path.join(OUT, `${name}-${color}.png`);
      await rasterize(Icon, color, file);
    }
  }
  if (missing.length) {
    console.log('MISSING ICONS:', missing.join(', '));
  } else {
    console.log('All icons found.');
  }
  console.log('PNG count:', fs.readdirSync(OUT).filter(f => f.endsWith('.png')).length);
}

main().catch(e => { console.error(e); process.exit(1); });
