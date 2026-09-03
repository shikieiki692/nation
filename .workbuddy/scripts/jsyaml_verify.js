// js-yaml 实测：Dataview 同款解析器对重复键的真实行为 + 修复后全库解析验证
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const yaml = require("js-yaml");

const VAULT = "C:/Obsidion/妙妙屋";

function frontOf(mdText) {
  const lines = mdText.split("\n");
  if (!lines.length || lines[0].trim() !== "---") return null;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === "---") return lines.slice(1, i).join("\n");
  }
  return null;
}

function tryLoad(label, fmText) {
  try {
    const doc = yaml.load(fmText);
    const kp = doc && doc.knowledge_points;
    const kpStr = kp === undefined ? "undefined" : JSON.stringify(kp).slice(0, 80);
    console.log(`  [${label}] 解析 OK ｜ knowledge_points = ${kpStr}`);
    return true;
  } catch (e) {
    console.log(`  [${label}] ❌ THROW: ${String(e.message).split("\n")[0]}`);
    return false;
  }
}

// ── ① 真题样本：修复前（5b5e62c2~1）vs 修复后（工作区）──
const rel1 = "04-题库/真题/第36届初赛/题-036-1-纳米硅制备方程式.md";
let before1 = null;
try {
  before1 = execFileSync("git", ["-C", VAULT, "show", `5b5e62c2~1:${rel1}`],
    { encoding: "utf8", maxBuffer: 10 * 1024 * 1024 });
} catch (e) { /* ignore */ }
const after1 = fs.readFileSync(path.join(VAULT, rel1), "utf8");
console.log("① 真题 knowledge_points 重复键（104 条修复样本）");
if (before1) tryLoad("修复前", frontOf(before1));
tryLoad("修复后", frontOf(after1));

// ── ② 03-知识点 样本：本轮 94 文件修复前（HEAD）vs 修复后 ──
const rel2 = "03-知识点/分析化学/分光光度法.md";
let before2 = null;
try {
  before2 = execFileSync("git", ["-C", VAULT, "show", `HEAD:${rel2}`],
    { encoding: "utf8", maxBuffer: 10 * 1024 * 1024 });
} catch (e) { /* ignore */ }
const after2 = fs.readFileSync(path.join(VAULT, rel2), "utf8");
console.log("\n② 知识点多字段重复键（94 文件修复样本）");
if (before2) {
  try {
    const d = yaml.load(frontOf(before2));
    console.log(`  [修复前] 解析 OK ｜ updated=${d.updated} ｜ key_images=${JSON.stringify(d.key_images)} ｜ image_count=${d.image_count}`);
  } catch (e) {
    console.log(`  [修复前] ❌ THROW: ${String(e.message).split("\n")[0]}`);
  }
}
try {
  const d = yaml.load(frontOf(after2));
  console.log(`  [修复后] 解析 OK ｜ updated=${d.updated} ｜ key_images=${JSON.stringify(d.key_images)} ｜ image_count=${d.image_count}`);
} catch (e) {
  console.log(`  [修复后] ❌ THROW: ${String(e.message).split("\n")[0]}`);
}

// ── ③ 全库题目 frontmatter 批量解析（修复后应 0 失败）──
let n = 0, nErr = 0, nNoFm = 0;
const errs = [];
function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name.endsWith(".md")) {
      let txt;
      try { txt = fs.readFileSync(p, "utf8"); } catch { continue; }
      const fm = frontOf(txt);
      if (fm === null) { nNoFm++; continue; }
      n++;
      try { yaml.load(fm); } catch (err) {
        nErr++;
        if (errs.length < 6) errs.push(`${path.relative(VAULT, p)} :: ${String(err.message).split("\n")[0]}`);
      }
    }
  }
}
walk(path.join(VAULT, "04-题库"));
walk(path.join(VAULT, "05-真题库"));
console.log(`\n③ 题目库（04+05）js-yaml 全量解析：${n} 文件，失败 ${nErr}，无 frontmatter ${nNoFm}`);
errs.forEach(e => console.log("  " + e));

// ── ④ 03-知识点 全量解析 ──
let m = 0, mErr = 0;
const merrs = [];
walk2(path.join(VAULT, "03-知识点"));
function walk2(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk2(p);
    else if (e.name.endsWith(".md")) {
      let txt;
      try { txt = fs.readFileSync(p, "utf8"); } catch { continue; }
      const fm = frontOf(txt);
      if (fm === null) continue;
      m++;
      try { yaml.load(fm); } catch (err) {
        mErr++;
        if (merrs.length < 6) merrs.push(`${path.relative(VAULT, p)} :: ${String(err.message).split("\n")[0]}`);
      }
    }
  }
}
console.log(`\n④ 03-知识点 js-yaml 全量解析：${m} 文件，失败 ${mErr}`);
merrs.forEach(e => console.log("  " + e));
