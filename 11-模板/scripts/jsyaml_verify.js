#!/usr/bin/env node
/**
 * YAML 1.2 frontmatter 解析闸门。
 * 用法:
 *   node jsyaml_verify.js --list <文件列表路径>
 *   node jsyaml_verify.js --dir <目录> [--dir ...] [--out <失败清单>]
 * 退出码: 0 = 全部通过；1 = 存在解析失败；2 = 参数错误。
 *
 * 当前环境缺少 js-yaml 4，脚本委托 .workbuddy/scripts/yaml_compat.py 的
 * ruamel.yaml YAML 1.2 strict 模式，重复键会失败。该兼容实现不宣称与
 * js-yaml 4 逐字节/逐异常完全等价；不要把输出误标为 js-yaml 4 实测。
 */
const fs = require("fs"), path = require("path");
const { DESCRIPTION, loadYaml } = require("../../.workbuddy/scripts/yaml_compat_client");

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
    const walk = dir => {
      let entries;
      try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
      for (const e of entries) {
        const p = path.join(dir, e.name);
        if (e.isDirectory()) {
          if (e.name.startsWith(".")) continue;
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
const pending = [];
for (const f of files) {
  let text;
  try { text = fs.readFileSync(f, "utf8"); }
  catch (e) { fail++; failures.push(`${f}\t读取失败: ${e.message}`); continue; }
  const lines = text.split(/\r?\n/);
  if (lines[0]?.trim() !== "---") { noFm++; continue; }
  let end = -1;
  for (let i = 1; i < lines.length; i++) if (lines[i].trim() === "---") { end = i; break; }
  if (end === -1) { fail++; failures.push(`${f}\tfrontmatter 未闭合`); continue; }
  pending.push({ id: pending.length, file: f, source: lines.slice(1, end).join("\n"), mode: "strict" });
}
const parsed = loadYaml(pending);
for (const item of pending) {
  const row = parsed.get(item.id);
  if (row?.ok) ok++;
  else {
    fail++;
    failures.push(`${item.file}\t${row?.error || "解析后端未返回结果"}`);
  }
}
console.log(`YAML 1.2 strict 闸门: 受检 ${files.length} / 通过 ${ok} / 无frontmatter ${noFm} / 失败 ${fail}`);
console.log(`解析后端: ${DESCRIPTION}`);
if (fail) {
  console.log("\n失败明细:");
  for (const l of failures.slice(0, 50)) console.log("  " + l);
  if (failures.length > 50) console.log(`  … 另有 ${failures.length - 50} 条`);
  if (getArg("--out")) fs.writeFileSync(getArg("--out"), failures.join("\n"), "utf8");
}
process.exit(fail ? 1 : 0);
