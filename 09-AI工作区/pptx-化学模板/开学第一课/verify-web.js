// 验证 index.html 放映器与 overview.html
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewportSize: { width: 1280, height: 800 } });

  // 1) index.html 首页
  await page.goto('file://' + path.join(dir, 'index.html').replace(/\\/g, '/'));
  await page.waitForTimeout(800);
  await page.screenshot({ path: 'web-index-p1.png' });
  const p1 = await page.textContent('#page');
  const prevDisabled1 = await page.isDisabled('#prev');

  // 2) 右方向键翻两页
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(400);
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(600);
  const p3 = await page.textContent('#page');
  await page.screenshot({ path: 'web-index-p3.png' });

  // 3) End 到末页，next 应禁用
  await page.keyboard.press('End');
  await page.waitForTimeout(600);
  const pEnd = await page.textContent('#page');
  const nextDisabledEnd = await page.isDisabled('#next');
  await page.screenshot({ path: 'web-index-p25.png' });

  // 4) 按钮返回上一页
  await page.click('#prev');
  await page.waitForTimeout(400);
  const p24 = await page.textContent('#page');

  // 5) overview.html
  await page.goto('file://' + path.join(dir, 'overview.html').replace(/\\/g, '/'));
  await page.waitForTimeout(1500);
  await page.screenshot({ path: 'web-overview.png', fullPage: true });
  const cells = await page.locator('.cell').count();

  console.log(JSON.stringify({ p1, prevDisabled1, p3, pEnd, nextDisabledEnd, p24, cells }));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
