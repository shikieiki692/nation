/**
 * Convert Excalidraw .md (Obsidian format) to PNG using Puppeteer.
 *
 * Usage: node excalidraw-to-png.mjs <input.md> [output.png]
 *
 * Strategy: Uses a local HTML page that loads the excalidraw library
 * to render the scene and export to PNG via canvas API.
 */

import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const inputFile = process.argv[2];
if (!inputFile) { process.exit(1); }
const outputFile = process.argv[3] || inputFile.replace(/\.md$/i, '.png');

// 1. Read and extract JSON from Excalidraw .md file
const mdContent = fs.readFileSync(inputFile, 'utf8');
const jsonMatch = mdContent.match(/```json\r?\n([\s\S]*?)\r?\n```/);
if (!jsonMatch) { process.exit(1); }
const sceneData = JSON.parse(jsonMatch[1]);

// 2. Calculate scene bounds
let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
for (const el of sceneData.elements) {
  if (el.isDeleted) continue;
  const x = el.x || 0, y = el.y || 0;
  const w = el.width || 0, h = el.height || 0;
  if (x < minX) minX = x;
  if (y < minY) minY = y;
  if (x + w > maxX) maxX = x + w;
  if (y + h > maxY) maxY = y + h;
}
const padding = 40;
const canvasW = Math.ceil((maxX - minX + padding * 2) * 2);  // 2x for HiDPI
const canvasH = Math.ceil((maxY - minY + padding * 2) * 2);
const sceneW = Math.ceil(maxX - minX + padding * 2);
const sceneH = Math.ceil(maxY - minY + padding * 2);

console.log(`Bounds: (${minX},${minY})→(${maxX},${maxY}) = ${sceneW}×${sceneH}`);

// 3. Build a self-contained HTML page that renders the excalidraw scene to canvas
const sceneJson = JSON.stringify(sceneData);

// Use the excalidraw library from local node_modules to build an export page
const utilsPath = path.join(__dirname, 'node_modules', '@excalidraw', 'utils', 'dist', 'prod', 'index.js');

// Read the exportToBlob/SVG code's actual location — use a bundled approach instead
// Strategy: load the scene into excalidraw via its own library and export

// Build a minimal HTML with the excalidraw library loaded from CDN
// We use page.evaluate to call the library's export function
const html = `<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin:0;background:#fff;">
<div id="root"></div>
<script>
  // We'll inject scene data from Puppeteer
  window.__sceneData = null;
  window.__exportDone = false;
  window.__exportError = null;
</script>
</body></html>`;

const tmpHtml = path.join(__dirname, '_excalidraw_render.html');
fs.writeFileSync(tmpHtml, html, 'utf-8');

// 4. Launch Puppeteer
const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: Math.min(sceneW + 100, 1920), height: Math.min(sceneH + 200, 1080) });

  // Go to the HTML page
  await page.goto('file://' + tmpHtml, { waitUntil: 'networkidle0' });

  // Now we need to use page.exposeFunction to handle the export.
  // Strategy: Use the canvas element directly by importing excalidraw library.
  // The most reliable method: create a canvas, set its size, use excalidraw's renderer.

  // Inject the excalidraw export script
  // We'll load @excalidraw/excalidraw from node_modules via a script tag
  const libPaths = [
    path.join(__dirname, 'node_modules', '@excalidraw', 'excalidraw', 'dist', 'excalidraw.production.min.js'),
    path.join(__dirname, 'node_modules', '@excalidraw', 'excalidraw', 'dist', 'excalidraw.development.js'),
  ];

  let libLoaded = false;
  for (const libPath of libPaths) {
    if (fs.existsSync(libPath)) {
      // Read the library and inject via evaluate
      const libContent = fs.readFileSync(libPath, 'utf8');
      await page.evaluate(content => {
        const script = document.createElement('script');
        script.textContent = content;
        document.head.appendChild(script);
      }, libContent);
      libLoaded = true;
      console.log(`Loaded: ${path.basename(libPath)}`);
      break;
    }
  }

  if (!libLoaded) {
    // Try loading from CDN as fallback (may fail without network — that's fine)
    console.log('Local library not found, attempting CDN load (optional)...');
    try {
      await page.addScriptTag({
        url: 'https://unpkg.com/@excalidraw/excalidraw@latest/dist/excalidraw.production.min.js',
        timeout: 10000,
      });
      libLoaded = true;
      console.log('CDN library loaded');
    } catch (e) {
      console.log('CDN unavailable, using manual canvas render (no library needed)');
    }
  }

  // Brief wait only if library was loaded from CDN (manual render is synchronous)
  if (libLoaded) {
    await new Promise(r => setTimeout(r, 1000));
  }

  // Use the canvas API to render the scene
  const result = await page.evaluate((sceneJson, cw, ch) => {
    try {
      const scene = JSON.parse(sceneJson);

      // Calculate bounds
      let mx = Infinity, my = Infinity, Mx = -Infinity, My = -Infinity;
      for (const el of scene.elements) {
        if (el.isDeleted) continue;
        const x = el.x || 0, y = el.y || 0;
        const w = el.width || 0, h = el.height || 0;
        if (x < mx) mx = x; if (y < my) my = y;
        if (x + w > Mx) Mx = x + w; if (y + h > My) My = y + h;
      }
      const pad = 40;
      const totalW = Math.ceil(Mx - mx + pad * 2);
      const totalH = Math.ceil(My - my + pad * 2);

      // Shift elements to positive coordinates
      for (const el of scene.elements) {
        if (el.isDeleted) continue;
        el.x = (el.x || 0) - mx + pad;
        el.y = (el.y || 0) - my + pad;
      }

      // Create canvas
      const canvas = document.createElement('canvas');
      canvas.width = totalW * 2;
      canvas.height = totalH * 2;
      const ctx = canvas.getContext('2d');
      ctx.scale(2, 2);
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, totalW, totalH);

      // Render elements manually
      for (const el of scene.elements) {
        if (el.isDeleted) continue;

        if (el.type === 'rectangle') {
          ctx.fillStyle = el.backgroundColor || 'transparent';
          ctx.fillRect(el.x, el.y, el.width, el.height);
          ctx.strokeStyle = el.strokeColor || '#000';
          ctx.lineWidth = (el.strokeWidth || 1) * 1.5;
          if (el.roundness && el.roundness.type === 3) {
            const r = Math.min(el.width, el.height) * 0.15;
            ctx.beginPath();
            ctx.moveTo(el.x + r, el.y);
            ctx.lineTo(el.x + el.width - r, el.y);
            ctx.quadraticCurveTo(el.x + el.width, el.y, el.x + el.width, el.y + r);
            ctx.lineTo(el.x + el.width, el.y + el.height - r);
            ctx.quadraticCurveTo(el.x + el.width, el.y + el.height, el.x + el.width - r, el.y + el.height);
            ctx.lineTo(el.x + r, el.y + el.height);
            ctx.quadraticCurveTo(el.x, el.y + el.height, el.x, el.y + el.height - r);
            ctx.lineTo(el.x, el.y + r);
            ctx.quadraticCurveTo(el.x, el.y, el.x + r, el.y);
            ctx.closePath();
            ctx.stroke();
          } else {
            ctx.strokeRect(el.x, el.y, el.width, el.height);
          }
        } else if (el.type === 'text') {
          ctx.fillStyle = el.strokeColor || '#000';
          const fontSize = el.fontSize || 16;
          ctx.font = `${fontSize}px Arial, sans-serif`;
          ctx.textAlign = el.textAlign || 'left';
          ctx.textBaseline = 'middle';

          const lines = (el.text || '').split('\n');
          const lineH = fontSize * 1.25;
          const startY = el.y + (el.height - lines.length * lineH) / 2;

          for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            let x = el.x;
            if (ctx.textAlign === 'center') {
              x = el.x + el.width / 2;
            }
            ctx.fillText(line, x, startY + i * lineH + lineH / 2);
          }
        } else if (el.type === 'ellipse') {
          ctx.strokeStyle = el.strokeColor || '#000';
          ctx.fillStyle = el.backgroundColor || 'transparent';
          ctx.lineWidth = (el.strokeWidth || 1) * 1.5;
          ctx.beginPath();
          ctx.ellipse(el.x + el.width/2, el.y + el.height/2, el.width/2, el.height/2, 0, 0, Math.PI*2);
          ctx.fill();
          ctx.stroke();
        } else if (el.type === 'line') {
          ctx.strokeStyle = el.strokeColor || '#000';
          ctx.lineWidth = (el.strokeWidth || 1) * 1.5;
          if (el.strokeStyle === 'dashed') { ctx.setLineDash([6, 4]); }
          else if (el.strokeStyle === 'dotted') { ctx.setLineDash([2, 3]); }
          else { ctx.setLineDash([]); }
          const pts = el.points || [[0, 0], [0, 60]];
          ctx.beginPath();
          ctx.moveTo(el.x + pts[0][0], el.y + pts[0][1]);
          for (let i = 1; i < pts.length; i++) {
            ctx.lineTo(el.x + pts[i][0], el.y + pts[i][1]);
          }
          ctx.stroke();
          ctx.setLineDash([]);
        } else if (el.type === 'diamond') {
          ctx.strokeStyle = el.strokeColor || '#000';
          ctx.fillStyle = el.backgroundColor || 'transparent';
          ctx.lineWidth = (el.strokeWidth || 1) * 1.5;
          ctx.beginPath();
          ctx.moveTo(el.x + el.width/2, el.y);
          ctx.lineTo(el.x + el.width, el.y + el.height/2);
          ctx.lineTo(el.x + el.width/2, el.y + el.height);
          ctx.lineTo(el.x, el.y + el.height/2);
          ctx.closePath();
          ctx.fill();
          ctx.stroke();
        } else if (el.type === 'arrow') {
          ctx.strokeStyle = el.strokeColor || '#000';
          ctx.lineWidth = (el.strokeWidth || 1) * 1.5;
          if (el.strokeStyle === 'dashed') {
            ctx.setLineDash([6, 4]);
          } else {
            ctx.setLineDash([]);
          }
          ctx.beginPath();
          const points = el.points || [[0, 0], [0, 60]];
          ctx.moveTo(el.x + points[0][0], el.y + points[0][1]);
          for (let i = 1; i < points.length; i++) {
            ctx.lineTo(el.x + points[i][0], el.y + points[i][1]);
          }
          ctx.stroke();
          ctx.setLineDash([]);

          // Draw arrowhead at end
          if (el.endArrowhead === 'arrow') {
            const last = points[points.length - 1];
            const prev = points[points.length - 2] || [0, 0];
            const ax = el.x + last[0];
            const ay = el.y + last[1];
            let angle = Math.atan2(ay - (el.y + prev[1]), ax - (el.x + prev[0]));
            if (points.length === 2 && points[0][0] === 0 && points[0][1] === 0) {
              angle = Math.atan2(last[1], last[0]);
            }
            const headLen = 10;
            ctx.fillStyle = el.strokeColor || '#000';
            ctx.beginPath();
            ctx.moveTo(ax, ay);
            ctx.lineTo(ax - headLen * Math.cos(angle - 0.4), ay - headLen * Math.sin(angle - 0.4));
            ctx.lineTo(ax - headLen * Math.cos(angle + 0.4), ay - headLen * Math.sin(angle + 0.4));
            ctx.closePath();
            ctx.fill();
          }
        }
      }

      // Convert to PNG
      const dataUrl = canvas.toDataURL('image/png');
      return dataUrl;
    } catch (e) {
      return 'ERROR: ' + e.message;
    }
  }, sceneJson, canvasW, canvasH);

  if (result.startsWith('ERROR:')) {
    // Fallback to full-page screenshot method with excalidraw.com
    console.log('Manual render failed:', result);
    console.log('Falling back to excalidraw.com screenshot method...');

    await page.goto('about:blank');
    const encoded = Buffer.from(sceneJson).toString('base64url');
    await page.goto(`https://excalidraw.com/#json=${encoded}`, {
      waitUntil: 'networkidle2',
      timeout: 45000,
    });
    await new Promise(r => setTimeout(r, 4000));

    // Check if canvas is available
    const hasCanvas = await page.evaluate(() => !!document.querySelector('canvas'));
    if (hasCanvas) {
      const canvasEl = await page.$('canvas');
      await canvasEl.screenshot({ path: outputFile });
      console.log(`✅ Saved (via excalidraw.com): ${outputFile}`);
    } else {
      await page.screenshot({ path: outputFile, fullPage: true });
      console.log(`✅ Saved (fallback full page): ${outputFile}`);
    }
  } else {
    // Save the data URL from manual rendering
    const base64Data = result.replace(/^data:image\/png;base64,/, '');
    fs.writeFileSync(outputFile, Buffer.from(base64Data, 'base64'));
    console.log(`✅ Saved (manual render): ${outputFile}`);
  }

} catch (err) {
  console.error('Fatal error:', err.message);
  process.exit(1);
} finally {
  await browser.close();
  try { fs.unlinkSync(tmpHtml); } catch {}
}
