// 用与 jsyaml_verify.js 完全相同的解析方式，直检指定文件
const fs = require("fs");
const path = require("path");
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

const manifest = fs.readFileSync(process.argv[2], "utf8")
  .split(/\r?\n/).map(s => s.trim()).filter(Boolean);

console.log("受检文件数:", manifest.length);
let ok = 0, err = 0, nofm = 0;
for (const rel of manifest) {
  const p = path.join(VAULT, rel);
  if (!fs.existsSync(p)) { console.log("  X 不存在:", rel); err++; continue; }
  const txt = fs.readFileSync(p, "utf8");
  const fm = frontOf(txt);
  if (fm === null) { console.log("  X 无 frontmatter:", rel); nofm++; continue; }
  try {
    const d = yaml.load(fm);
    const sr = JSON.stringify(d.serve_rounds);
    const el = JSON.stringify(d.exercise_levels);
    console.log("  OK 解析通过 | title=" + d.title +
      " | serve_rounds=" + sr +
      " | exercise_count=" + d.exercise_count +
      " | exercise_levels=" + el +
      " | has_images=" + d.has_images +
      " | image_count=" + d.image_count +
      " | stage=" + d.stage +
      " | module=" + d.module);
    ok++;
  } catch (e) {
    console.log("  X THROW: " + rel + " :: " + String(e.message).split("\n")[0]);
    err++;
  }
}
console.log("\n结果：OK " + ok + " / 失败 " + err + " / 无FM " + nofm + "  (受检 " + manifest.length + ")");
process.exit(err + nofm > 0 ? 1 : 0);
