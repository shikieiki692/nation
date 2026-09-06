// 照片预处理 v3：contain 等比完整显示（禁止裁剪），米白衬底 + 圆角 + 1pt 细边框
const sharp = require('sharp');
const path = require('path');

const IMG = path.join(__dirname, 'images');

// [源文件, 输出名, 宽pt, 高pt]
const CARDS = [
  ['bubble-tea.jpg', 'card-bubble-tea.png', 184, 150],
  ['smartphone.jpg', 'card-smartphone.png', 184, 150],
  ['fire-extinguisher.jpg', 'card-extinguisher.png', 184, 150],
  ['wheat.jpg', 'card-wheat.png', 352, 300],
  ['mendeleev.jpg', 'card-mendeleev.png', 210, 230],
  ['mendeleev-table.jpg', 'card-mendeleev-table.png', 416, 170],
  ['mof5.png', 'card-mof5.png', 300, 300],
  ['tu-youyou.jpg', 'card-tu-youyou.png', 300, 300],
  ['jacket.jpg', 'card-jacket.png', 300, 300],
  ['rare-earth.jpg', 'card-rare-earth.png', 195, 112],
  ['flame-test.jpg', 'card-flame.png', 200, 180],
  ['tyndall.jpg', 'card-tyndall.png', 200, 180],
  ['chemical-garden.jpg', 'card-garden.png', 200, 180]
];

const SCALE = 3;
const RADIUS_PT = 8;
const BORDER_PT = 1;

async function makeCard(src, dst, wPt, hPt) {
  const W = wPt * SCALE, H = hPt * SCALE;
  const r = RADIUS_PT * SCALE;
  const bw = BORDER_PT * SCALE;

  // contain：完整等比放入，米白衬底
  const buf = await sharp(path.join(IMG, src))
    .resize(W, H, { fit: 'contain', background: '#FAF7F0' })
    .flatten({ background: '#FAF7F0' })
    .png().toBuffer();

  // 圆角裁剪
  const mask = Buffer.from(
    `<svg width="${W}" height="${H}"><rect x="0" y="0" width="${W}" height="${H}" rx="${r}" fill="#fff"/></svg>`
  );
  let rounded = await sharp(buf)
    .composite([{ input: mask, blend: 'dest-in' }])
    .png().toBuffer();

  // 1pt 浅边框（内描边）
  const border = Buffer.from(
    `<svg width="${W}" height="${H}"><rect x="${bw / 2}" y="${bw / 2}" width="${W - bw}" height="${H - bw}" rx="${r}" fill="none" stroke="#DDD6C8" stroke-width="${bw}"/></svg>`
  );
  rounded = await sharp(rounded)
    .composite([{ input: border, blend: 'over' }])
    .png().toBuffer();

  await sharp(rounded).toFile(path.join(IMG, dst));
  console.log('made', dst, `${wPt}x${hPt}pt`);
}

async function main() {
  for (const [src, dst, w, h] of CARDS) await makeCard(src, dst, w, h);
}

main().catch(e => { console.error(e); process.exit(1); });
