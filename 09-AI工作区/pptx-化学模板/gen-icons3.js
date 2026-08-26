// Round 3: 开学第一课新增页眉/卡片图标
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const path = require('path');
const Lu = require('react-icons/lu');

const OUT = path.join(__dirname, 'icons');

const PLAN = {
  LuWheat: ['1B4332'],
  LuAward: ['1B4332'],
  LuPill: ['1B4332'],
  LuShirt: ['1B4332'],
  LuGem: ['1B4332'],
  LuHeartPulse: ['1B4332'],
  LuSparkles: ['1B4332'],
  LuKeyRound: ['1B4332'],
  LuBrain: ['1B4332'],
  LuListChecks: ['1B4332'],
  LuNotebookPen: ['1B4332'],
  LuRefreshCw: ['1B4332'],
  LuSmile: ['1B4332'],
  LuMail: ['1B4332'],
  LuEye: ['1B4332', 'FFFFFF'],
  LuSearch: ['FFFFFF'],
  LuTarget: ['FFFFFF'],
  LuTriangleAlert: ['FFFFFF']
};

async function main() {
  for (const [name, colors] of Object.entries(PLAN)) {
    const Icon = Lu[name];
    if (!Icon) { console.log('MISSING', name); continue; }
    for (const color of colors) {
      const svg = ReactDOMServer.renderToStaticMarkup(
        React.createElement(Icon, { color: `#${color}`, size: '256', strokeWidth: 2 })
      );
      await sharp(Buffer.from(svg)).png().toFile(path.join(OUT, `${name}-${color}.png`));
    }
  }
  console.log('done');
}

main().catch(e => { console.error(e); process.exit(1); });
