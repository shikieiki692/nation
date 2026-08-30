// TEMP analysis: find images appearing in >1 distinct question block in the merged book.
const fs = require("fs");
const path = require("path");

const ROOT = "C:/Obsidion/妙妙屋/04-课件/习题集/习题书-教师版";

function walk(dir) {
  let out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) out = out.concat(walk(full));
    else if (e.name.endsWith(".md") && e.name !== "目录.md" && !e.name.startsWith("_未分类"))
      out.push(full);
  }
  return out;
}

const files = walk(ROOT);
// hash -> Set(blockKey)   where blockKey = fileRel + '##' + first heading line
const hashBlocks = new Map();
let totalRefs = 0;
// hash -> { blockKey -> {file, block, chapter} }
const hashDetails = new Map();

for (const f of files) {
  const text = fs.readFileSync(f, "utf8");
  const lines = text.split(/\r?\n/);
  let curBlock = null;
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^##\s+(\S+)/);
    if (m) curBlock = m[1]; // heading like "1.1" ; block key uses it
    const imgRe = /!\[\[([0-9a-f]{64})\.jpg\]\]/g;
    let im;
    while ((im = imgRe.exec(lines[i])) !== null) {
      totalRefs++;
      const h = im[1];
      if (!hashBlocks.has(h)) hashBlocks.set(h, new Set());
      const blockKey = path.basename(f) + "@" + (curBlock || "pre");
      hashBlocks.get(h).add(blockKey);
      if (!hashDetails.has(h)) hashDetails.set(h, new Map());
      const chapter = f.split(/[\\/]/).slice(-2)[0]; // e.g. 第一篇-化学原理
      hashDetails.get(h).set(blockKey, { file: path.basename(f), block: curBlock || "pre", chapter });
    }
  }
}

// Group: hashes that map to >1 distinct block
const cross = [];
for (const [h, blocks] of hashBlocks) {
  if (blocks.size > 1) {
    cross.push({ h, n: blocks.size });
  }
}
cross.sort((a, b) => b.n - a.n);

const multiRefSameBlock = [...hashBlocks.entries()].filter(([, b]) => b.size === 1);
const multiRefDistinct = [...hashBlocks.entries()].filter(([, b]) => b.size > 1);

console.log("total refs =", totalRefs);
console.log("distinct image hashes =", hashBlocks.size);
console.log("hashes appearing in >1 DISTINCT question-block =", multiRefDistinct.length);
console.log("sum refs in those =", multiRefDistinct.reduce((s, [, b]) => s + b.size, 0));
console.log("hashes with >1 ref but SAME block (legit reuse) =", multiRefSameBlock.length);
console.log("---- cross-question top 60 ----");
cross.slice(0, 60).forEach((x) => console.log(String(x.n).padStart(2), x.h.slice(0, 16)));

// For each cross-question hash, determine chapters spanned
const crossWithChapters = [];
for (const [h, blocks] of hashBlocks) {
  if (blocks.size <= 1) continue;
  const chapters = new Set();
  for (const bk of blocks) chapters.add(hashDetails.get(h).get(bk).chapter);
  crossWithChapters.push({ h, n: blocks.size, chapters: [...chapters] });
}
const crossChapter = crossWithChapters.filter((c) => c.chapters.length > 1);
const sameChapter = crossWithChapters.filter((c) => c.chapters.length === 1);
console.log("\n### cross-question hashes spanning >1 chapter:", crossChapter.length, "refs=", crossChapter.reduce((s,c)=>s+c.n,0));
console.log("### cross-question hashes within 1 chapter:", sameChapter.length, "refs=", sameChapter.reduce((s,c)=>s+c.n,0));

console.log("\n--- cross-chapter list (hash | nBlocks | chapters | sample blocks) ---");
crossChapter.sort((a,b)=>b.n-a.n).forEach((c)=>{
  const sampleBlocks = [...hashDetails.get(c.h).keys()].slice(0,4).map(k=>{
    const d=hashDetails.get(c.h).get(k); return `${d.chapter}/${d.file}@${d.block}`;
  }).join(" ; ");
  console.log(String(c.n).padStart(2), c.h.slice(0,16), "|", c.chapters.join(","), "|", sampleBlocks);
});

// ---- Map each book block to source question group via source-map ----
// Build reverse index: generated_chapter + '@' + qno -> Set(source_title)
const SM_PATH = "C:/Obsidion/妙妙屋/09-审计报告/2026-08-30-习题书V2正式版-source-map.jsonl";
const sm = fs.readFileSync(SM_PATH, "utf8").split(/\r?\n/).filter(Boolean).map(l => {
  try { return JSON.parse(l); } catch { return null; }
}).filter(Boolean);

const rev = new Map(); // key: basename(generated_chapter) + '@' + generated_qno -> Set(source_title)
for (const r of sm) {
  const file = r.generated_chapter.split(/[\\/]/).pop();
  const key = file + "@" + r.generated_qno;
  if (!rev.has(key)) rev.set(key, new Set());
  rev.get(key).add(r.source_title);
}

function groupOf(title) {
  // 题-XXX-Y-*  -> group 题-XXX-Y ; also 题-036b-2-*
  const m = title.match(/^(题-[0-9]+[a-z]*-\d+)/i);
  return m ? m[1] : title;
}

const crossWithGroups = [];
for (const c of crossWithChapters) {
  const groups = new Set();
  const blockGroups = [];
  for (const bk of hashDetails.get(c.h).keys()) {
    const d = hashDetails.get(c.h).get(bk);
    const key = d.file + "@" + d.block;
    const srcs = rev.get(key) || new Set();
    for (const s of srcs) { groups.add(groupOf(s)); blockGroups.push({ blk: `${d.chapter}/${d.file}@${d.block}`, src: s }); }
  }
  crossWithGroups.push({ h: c.h, n: c.n, chapters: c.chapters, chapterCount: c.chapters.length, groups: [...groups], blockGroups });
}

const singleGroup = crossWithGroups.filter((c) => c.groups.length === 1);
const multiGroup = crossWithGroups.filter((c) => c.groups.length > 1);
console.log("\n### cross-question hashes map to a SINGLE source group:", singleGroup.length);
console.log("### cross-question hashes map to MULTIPLE source groups:", multiGroup.length);

// Write a full record CSV: per-hash classification + block->source trace
const outLines = ["hash,block_count,chapter_count,group_count,chapters,groups,blocks_with_sources"];
for (const c of crossWithGroups) {
  const blocksWithSrc = c.blockGroups.map((b) => `${b.blk}=>${b.src}`).join(" ; ");
  outLines.push(`${c.h},${c.n},${c.chapterCount},${c.groups.length},"${c.chapters.join(",")}","${c.groups.join(" | ")}","${blocksWithSrc}"`);
}
const outPath = "C:/Obsidion/妙妙屋/09-审计报告/2026-08-30-习题书V2-合并版跨题图残留.csv";
fs.writeFileSync(outPath, outLines.join("\n")+"\n", "utf8");
console.log("\nWROTE:", outPath, "rows=", crossWithGroups.length);

console.log("\n--- cross-chapter (chapter_count>1) per-hash trace ---");
crossWithGroups.filter((c) => c.chapterCount > 1).sort((a,b)=>b.n-a.n).forEach((c) => {
  console.log("\n[hash]", c.h.slice(0,16), "blocks="+c.n, "groups=", c.groups.join(" | "));
  c.blockGroups.forEach((b) => console.log("   ", b.blk, "=>", b.src));
});
