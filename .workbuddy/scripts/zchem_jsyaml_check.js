const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");
const VAULT = "C:/Obsidion/妙妙屋";
const FILES = [
  "07-资料提炼/网课资料/Zchem 物理化学 上/Zchem物理化学上-网课资料索引.md",
  "07-资料提炼/网课资料/Zchem 物理化学 下/Zchem物理化学下-网课资料索引.md",
  "07-资料提炼/网课资料/Zchem 有机反应合成与机理 上/Zchem有机上-网课资料索引.md",
  "07-资料提炼/网课资料/Zchem 有机反应合成与机理 中/Zchem有机中-网课资料索引.md",
  "07-资料提炼/网课资料/Zchem 有机反应合成与机理 下/Zchem有机下-网课资料索引.md",
  "07-资料提炼/网课资料/README.md",
];
function frontOf(t) {
  const lines = t.split("\n");
  if (!lines.length || lines[0].trim() !== "---") return null;
  for (let i = 1; i < lines.length; i++) if (lines[i].trim() === "---") return lines.slice(1, i).join("\n");
  return null;
}
let ok = 0, bad = 0;
for (const rel of FILES) {
  const p = path.join(VAULT, rel);
  const txt = fs.readFileSync(p, "utf8");
  const fm = frontOf(txt);
  if (fm === null) { console.log(`[NO-FM] ${rel}`); bad++; continue; }
  try {
    const d = yaml.load(fm);
    console.log(`[OK] ${rel}  | title=${d.title}  | updated=${d.updated}  | related=${(d.related_teaching_logic||[]).length}`);
    ok++;
  } catch (e) {
    console.log(`[THROW] ${rel} :: ${String(e.message).split("\n")[0]}`);
    bad++;
  }
}
console.log(`\n受检 ${FILES.length}｜通过 ${ok}｜失败 ${bad}`);
