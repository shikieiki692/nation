// 照片预处理：contain 等比完整显示（禁止裁剪），米白衬底 + 圆角 + 1pt 细边框
const sharp = require('sharp');
const path = require('path');

const IMG = path.join(__dirname, 'images-src');
const OUT = path.join(__dirname, 'images');

// [源文件（images-src/）, 输出名（images/）, 宽pt, 高pt]
const CARDS = [
  ['p02-img1.png', 'card-library.png', 300, 177],
  ['p03-img2.jpg', 'card-p3-library.png', 112, 84],
  ['p03-img1.jpg', 'card-p3-market.png', 112, 84],
  ['p03-img3.png', 'card-p3-lab.png', 112, 84],
  ['p03-img4.png', 'card-p3-parcel.png', 112, 84],
  ['p03-img5.png', 'card-p3-recycle.png', 112, 84]
];

const SCALE = 3;
const RADIUS_PT = 8;
const BORDER_PT = 1;

async function makeCard(src, dst, wPt, hPt) {
  const W = wPt * SCALE, H = hPt * SCALE;
  const r = RADIUS_PT * SCALE;
  const bw = BORDER_PT * SCALE;

  const buf = await sharp(path.join(IMG, src))
    .resize(W, H, { fit: 'contain', background: '#FAF7F0' })
    .flatten({ background: '#FAF7F0' })
    .png().toBuffer();

  const mask = Buffer.from(
    `<svg width="${W}" height="${H}"><rect x="0" y="0" width="${W}" height="${H}" rx="${r}" fill="#fff"/></svg>`
  );
  let rounded = await sharp(buf)
    .composite([{ input: mask, blend: 'dest-in' }])
    .png().toBuffer();

  const border = Buffer.from(
    `<svg width="${W}" height="${H}"><rect x="${bw / 2}" y="${bw / 2}" width="${W - bw}" height="${H - bw}" rx="${r}" fill="none" stroke="#DDD6C8" stroke-width="${bw}"/></svg>`
  );
  rounded = await sharp(rounded)
    .composite([{ input: border, blend: 'over' }])
    .png().toBuffer();

  await sharp(rounded).toFile(path.join(OUT, dst));
  console.log('made', dst, `${wPt}x${hPt}pt`);
}

async function main() {
  for (const [src, dst, w, h] of CARDS) await makeCard(src, dst, w, h);
}

main().catch(e => { console.error(e); process.exit(1); });
