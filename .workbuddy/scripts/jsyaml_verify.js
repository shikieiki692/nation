// YAML 解析实测：历史重复键样本对照 + 修复后全库解析验证。
// 当前环境无 js-yaml 4，委托 ruamel.yaml YAML 1.2 strict 兼容后端；非逐异常等价。
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const { DESCRIPTION, loadOne, loadYaml } = require("./yaml_compat_client");

const VAULT = "C:/Obsidion/妙妙屋";
function frontOf(mdText) {
  const lines = mdText.split("\n");
  if (!lines.length || lines[0].trim() !== "---") return null;
  for (let i = 1; i < lines.length; i++) if (lines[i].trim() === "---") return lines.slice(1, i).join("\n");
  return null;
}
function show(label, row) {
  if (row.ok) {
    const doc = row.data || {};
    const kp = doc.knowledge_points;
    const kpStr = kp === undefined ? "undefined" : JSON.stringify(kp).slice(0, 80);
    console.log(`  [${label}] 解析 OK ｜ knowledge_points = ${kpStr}`);
  } else {
    console.log(`  [${label}] ❌ PARSE: ${row.error}`);
  }
}
function gitShow(rev, rel) {
  try {
    return execFileSync("git", ["-C", VAULT, "show", `${rev}:${rel}`],
      { encoding: "utf8", maxBuffer: 10 * 1024 * 1024 });
  } catch { return null; }
}
function collect(root, rows) {
  const walk = dir => {
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
    for (const entry of entries) {
      const p = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (entry.name.startsWith(".")) continue;
        walk(p);
      } else if (entry.name.endsWith(".md")) {
        const fm = frontOf(fs.readFileSync(p, "utf8"));
        if (fm !== null) rows.push({ id: rows.length, rel: path.relative(VAULT, p), source: fm, mode: "strict" });
      }
    }
  };
  walk(root);
}

console.log(`解析后端: ${DESCRIPTION}`);
const rel1 = "04-题库/真题/第36届初赛/题-036-1-纳米硅制备方程式.md";
const before1 = gitShow("5b5e62c2~1", rel1);
const after1 = fs.readFileSync(path.join(VAULT, rel1), "utf8");
console.log("\n① 真题 knowledge_points 重复键（104 条修复样本）");
if (before1) show("修复前", loadOne(frontOf(before1)));
show("修复后", loadOne(frontOf(after1)));

const rel2 = "03-知识点/分析化学/分光光度法.md";
const before2 = gitShow("HEAD", rel2);
const after2 = fs.readFileSync(path.join(VAULT, rel2), "utf8");
console.log("\n② 知识点多字段重复键（94 文件修复样本）");
if (before2) {
  const row = loadOne(frontOf(before2));
  if (row.ok) {
    const d = row.data || {};
    console.log(`  [修复前] 解析 OK ｜ updated=${d.updated} ｜ key_images=${JSON.stringify(d.key_images)} ｜ image_count=${d.image_count}`);
  } else show("修复前", row);
}
{
  const row = loadOne(frontOf(after2));
  if (row.ok) {
    const d = row.data || {};
    console.log(`  [修复后] 解析 OK ｜ updated=${d.updated} ｜ key_images=${JSON.stringify(d.key_images)} ｜ image_count=${d.image_count}`);
  } else show("修复后", row);
}

const questionRows = [];
collect(path.join(VAULT, "04-题库"), questionRows);
collect(path.join(VAULT, "05-真题库"), questionRows);
const kpRows = [];
collect(path.join(VAULT, "03-知识点"), kpRows);
const allRows = [...questionRows, ...kpRows];
allRows.forEach((item, index) => { item.id = index; });
const parsed = loadYaml(allRows);
const failures = allRows.filter(item => !parsed.get(item.id)?.ok)
  .map(item => `${item.rel} :: ${parsed.get(item.id)?.error || "解析后端未返回结果"}`);
const questionErrors = questionRows.filter(item => !parsed.get(item.id)?.ok).length;
const kpErrors = kpRows.filter(item => !parsed.get(item.id)?.ok).length;
console.log(`\n③ 题目库（04+05）全量解析：${questionRows.length} 文件，失败 ${questionErrors}`);
console.log(`\n④ 03-知识点 全量解析：${kpRows.length} 文件，失败 ${kpErrors}`);
failures.slice(0, 12).forEach(item => console.log("  " + item));
process.exit(questionErrors + kpErrors ? 1 : 0);
