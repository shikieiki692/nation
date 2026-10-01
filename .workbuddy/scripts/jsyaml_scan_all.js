// 全库 YAML frontmatter 扫描：严格模式拒绝重复键/非法结构。
// 当前环境缺少 js-yaml 4，本脚本通过 yaml_compat_client.js 委托 ruamel.yaml；
// 口径接近但不宣称与 js-yaml 4 完全等价。--json-mode 可模拟重复键兼容模式。
const fs = require("fs"), path = require("path");
const { DESCRIPTION, loadYaml } = require("./yaml_compat_client");
const VAULT = "C:\\Obsidion\\妙妙屋";
const MODE = process.argv.includes("--json-mode") ? "json" : "strict";
const SKIP = new Set([".git", ".workbuddy", ".obsidian", ".trash", ".smart-env", "媒体仓库", "node_modules"]);

function* walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP.has(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (e.name.toLowerCase().endsWith(".md")) yield p;
  }
}

function add(byTop, top, rel, err) {
  const b = (byTop[top] = byTop[top] || { fails: [] });
  b.fails.push({ rel, err });
}

const byTop = {};
const pending = [];
let total = 0, withFm = 0, unclosed = 0;
for (const f of walk(VAULT)) {
  const rel = path.relative(VAULT, f);
  const top = rel.split(path.sep)[0];
  total++;
  let text;
  try { text = fs.readFileSync(f, "utf8"); } catch { continue; }
  const lines = text.split(/\r?\n/);
  if ((lines[0] || "").trim() !== "---") continue;
  withFm++;
  let end = -1;
  for (let i = 1; i < lines.length; i++) {
    if ((lines[i] || "").trim() === "---") { end = i; break; }
  }
  if (end === -1) {
    unclosed++;
    add(byTop, top, rel, "frontmatter 未闭合");
    continue;
  }
  pending.push({ id: pending.length, top, rel, source: lines.slice(1, end).join("\n"), mode: MODE });
}

const parsed = loadYaml(pending);
let failTotal = unclosed;
for (const item of pending) {
  const row = parsed.get(item.id);
  if (!row || !row.ok) {
    failTotal++;
    add(byTop, item.top, item.rel, row?.error || "解析后端未返回结果");
  }
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
console.log(`\n全库 md=${total}，有 frontmatter=${withFm}（未闭合 ${unclosed}），YAML 解析失败=${failTotal}`);
console.log(`解析后端: ${DESCRIPTION}；模式=${MODE}`);
fs.writeFileSync(path.join(VAULT, ".workbuddy", "tmp", "_jsyaml_all_fail.txt"), lines2.join("\n"), "utf8");
console.log("清单 → .workbuddy/tmp/_jsyaml_all_fail.txt");
process.exit(failTotal ? 1 : 0);
