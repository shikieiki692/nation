#!/usr/bin/env node
/**
 * js-yaml 4 解析闸门（Obsidian / Bases 同源解析器）
 * 用法:
 *   node jsyaml_verify.js --list <文件列表路径>     # 只校验列表内文件
 *   node jsyaml_verify.js --dir <目录> [--dir ...]   # 递归校验目录内所有 .md
 * 退出码: 0 = 全部通过；1 = 存在解析失败
 * 铁律: js-yaml 4 遇重复键/非法转义会 THROW，导致整条文件在 Obsidian 里消失。
 *       PyYAML 只做后值覆盖、不报错，因此必须单独用本闸门兜底。
 */
const fs = require("fs"), path = require("path"), yaml = require("js-yaml");

const argv = process.argv.slice(2);
function getArg(k) { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : null; }
const listFile = getArg("--list");
const dirs = [];
for (let i = 0; i < argv.length; i++) if (argv[i] === "--dir") dirs.push(argv[i + 1]);

let files = [];
if (listFile) {
  files = fs.readFileSync(listFile, "utf8").split("\n").map(s => s.trim())
    .filter(Boolean).map(l => l.split("\t")[0]);
} else if (dirs.length) {
  for (const d of dirs) {
    const walk = (dir) => {
      let ents;
      try { ents = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
      for (const e of ents) {
        const p = path.join(dir, e.name);
        if (e.isDirectory()) {
          if (e.name.startsWith(".")) continue;   // 跳过 .workbuddy / .git / .obsidian
          walk(p);
        } else if (e.name.endsWith(".md")) files.push(p);
      }
    };
    walk(d);
  }
} else {
  console.error("需要 --list <文件> 或 --dir <目录>");
  process.exit(2);
}

let ok = 0, noFm = 0, fail = 0;
const failures = [];
for (const f of files) {
  let t;
  try { t = fs.readFileSync(f, "utf8"); } catch (e) { console.error("读取失败: " + f); continue; }
  const lines = t.split(/\r?\n/);
  if (lines[0].trim() !== "---") { noFm++; continue; }
  let end = -1;
  for (let i = 1; i < lines.length; i++) if (lines[i].trim() === "---") { end = i; break; }
  if (end === -1) { noFm++; continue; }
  try {
    yaml.load(lines.slice(1, end).join("\n"), { json: true });
    ok++;
  } catch (e) {
    fail++;
    failures.push(`${f}\t${String(e.message).split("\n")[0]}`);
  }
}

console.log(`js-yaml 4 闸门: 受检 ${files.length} / 通过 ${ok} / 无frontmatter ${noFm} / 失败 ${fail}`);
if (fail) {
  console.log("\n失败明细:");
  for (const l of failures.slice(0, 50)) console.log("  " + l);
  if (failures.length > 50) console.log(`  … 另有 ${failures.length - 50} 条`);
  if (getArg("--out")) fs.writeFileSync(getArg("--out"), failures.join("\n"), "utf8");
}
process.exit(fail ? 1 : 0);
