// 全库 js-yaml 扫描 v2：仅解析 frontmatter 段（与 jsyaml_verify.js 口径一致）
const fs = require("fs"), path = require("path"), yaml = require("js-yaml");
const VAULT = "C:\\Obsidion\\妙妙屋";
const SKIP = new Set([".git", ".workbuddy", ".obsidian", ".trash", ".smart-env", "媒体仓库", "node_modules"]);

function* walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP.has(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (e.name.toLowerCase().endsWith(".md")) yield p;
  }
}

const byTop = {};
let total = 0, withFm = 0, failTotal = 0, unclosed = 0;
for (const f of walk(VAULT)) {
  const rel = path.relative(VAULT, f);
  const top = rel.split(path.sep)[0];
  total++;
  let t;
  try { t = fs.readFileSync(f, "utf8"); } catch { continue; }
  const lines = t.split(/\r?\n/);
  if ((lines[0] || "").trim() !== "---") continue;   // 无 frontmatter，跳过
  withFm++;
  let end = -1;
  for (let i = 1; i < lines.length; i++) {
    if ((lines[i] || "").trim() === "---") { end = i; break; }
  }
  if (end === -1) { unclosed++; add(top, rel, "frontmatter 未闭合"); continue; }
  const fm = lines.slice(1, end).join("\n");
  try { yaml.load(fm, { json: true }); }
  catch (e) {
    const msg = String(e.message).split("\n")[0].replace(/at line (\d+)/, (m, n) => `at line ${+n + 1}`);
    add(top, rel, msg);
  }
}
function add(top, rel, err) {
  failTotal++;
  const b = (byTop[top] = byTop[top] || { total: 0, fails: [] });
  b.fails.push({ rel, err });
}

const lines2 = [];
for (const top of Object.keys(byTop).sort()) {
  const b = byTop[top];
  if (!b.fails.length) continue;
  console.log(`${top}  ❌ ${b.fails.length}`);
  for (const f of b.fails.slice(0, 8)) console.log(`    - ${f.rel}\n      ${f.err}`);
  if (b.fails.length > 8) console.log(`    … 共 ${b.fails.length}`);
  for (const f of b.fails) lines2.push(`${f.rel}\t${f.err}`);
}
console.log(`\n全库 md=${total}，有 frontmatter=${withFm}（未闭合 ${unclosed}），js-yaml 解析失败=${failTotal}`);
fs.writeFileSync(path.join(VAULT, ".workbuddy", "tmp", "_jsyaml_all_fail.txt"), lines2.join("\n"), "utf8");
console.log("清单 → .workbuddy/tmp/_jsyaml_all_fail.txt");
