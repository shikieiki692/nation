/**
 * Convert SVG to PNG using Puppeteer (Edge headless).
 *
 * Usage: node svg-to-png.mjs <input.svg> [output.png] [width]
 *
 * Renders the SVG in a headless browser and screenshots to PNG.
 * Width defaults to 1200px if not specified.
 */

import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const inputFile = process.argv[2];
if (!inputFile) {
  console.error('Usage: node svg-to-png.mjs <input.svg> [output.png] [width]');
  process.exit(1);
}
const outputFile = process.argv[3] || inputFile.replace(/\.svg$/i, '.png');
const width = parseInt(process.argv[4] || '1200', 10);

const svgContent = fs.readFileSync(inputFile, 'utf8');

const browser = await puppeteer.launch({
  executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

const page = await browser.newPage();

// Create an HTML page that renders the SVG at the desired width
const html = `<!DOCTYPE html>
<html><head><style>
  body { margin: 0; padding: 20px; background: white; }
  svg { max-width: ${width}px; height: auto; }
</style></head><body>${svgContent}</body></html>`;

await page.setContent(html, { waitUntil: 'domcontentloaded' });

// Get actual SVG dimensions
const svgBox = await page.evaluate(() => {
  const svg = document.querySelector('svg');
  if (!svg) return null;
  const rect = svg.getBoundingClientRect();
  return { width: rect.width, height: rect.height };
});

if (!svgBox || svgBox.width === 0 || svgBox.height === 0) {
  console.error(`[SVG2PNG] Failed to render: ${inputFile}`);
  await browser.close();
  process.exit(1);
}

// Set viewport to match SVG + padding for border
await page.setViewport({
  width: Math.ceil(svgBox.width) + 40,
  height: Math.ceil(svgBox.height) + 40,
  deviceScaleFactor: 2,  // HiDPI
});

// Re-render with correct viewport
await page.setContent(html, { waitUntil: 'domcontentloaded' });

// Screenshot the body element
const body = await page.$('body');
await body.screenshot({ path: outputFile, type: 'png' });

await browser.close();
console.log(`[SVG2PNG] ${path.basename(inputFile)} → ${path.basename(outputFile)} (${Math.ceil(svgBox.width)}x${Math.ceil(svgBox.height)}px)`);
