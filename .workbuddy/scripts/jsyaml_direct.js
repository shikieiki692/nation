// 按清单直检指定文件 frontmatter。当前环境无 js-yaml 4，委托 ruamel.yaml 兼容后端。
const fs = require("fs");
const path = require("path");
const { DESCRIPTION, loadYaml } = require("./yaml_compat_client");
const VAULT = "C:/Obsidion/妙妙屋";
const MODE = process.argv.includes("--json-mode") ? "json" : "strict";

function frontOf(mdText) {
  const lines = mdText.split("\n");
  if (!lines.length || lines[0].trim() !== "---") return null;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === "---") return lines.slice(1, i).join("\n");
  }
  return null;
}

const manifest = fs.readFileSync(process.argv[2], "utf8")
  .split(/\r?\n/).map(s => s.trim()).filter(Boolean);
console.log("受检文件数:", manifest.length);
console.log("解析后端:", DESCRIPTION, "；模式=", MODE);
const pending = [];
const missing = [];
const noFm = [];
for (const rel of manifest) {
  const p = path.join(VAULT, rel);
  if (!fs.existsSync(p)) { missing.push(rel); continue; }
  const fm = frontOf(fs.readFileSync(p, "utf8"));
  if (fm === null) { noFm.push(rel); continue; }
  pending.push({ id: pending.length, rel, source: fm, mode: MODE });
}
const parsed = loadYaml(pending);
let ok = 0, err = 0;
for (const rel of missing) { console.log("  X 不存在:", rel); err++; }
for (const rel of noFm) { console.log("  X 无 frontmatter:", rel); }
for (const item of pending) {
  const row = parsed.get(item.id);
  if (!row || !row.ok) {
    console.log("  X PARSE: " + item.rel + " :: " + (row?.error || "解析后端未返回结果"));
    err++;
    continue;
  }
  const d = row.data || {};
  console.log("  OK 解析通过 | title=" + d.title +
    " | serve_rounds=" + JSON.stringify(d.serve_rounds) +
    " | exercise_count=" + d.exercise_count +
    " | exercise_levels=" + JSON.stringify(d.exercise_levels) +
    " | has_images=" + d.has_images +
    " | image_count=" + d.image_count +
    " | stage=" + d.stage +
    " | module=" + d.module);
  ok++;
}
console.log("\n结果：OK " + ok + " / 失败 " + err + " / 无FM " + noFm.length + "  (受检 " + manifest.length + ")");
process.exit(err + noFm.length > 0 ? 1 : 0);
