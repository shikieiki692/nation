// check_dvjs.js —— 语法解析 00-首页/活跃任务.md 里的 dataviewjs 块
const fs = require('fs');
const p = process.argv[2];
const t = fs.readFileSync(p, 'utf8');
const blocks = [...t.matchAll(/```dataviewjs\n([\s\S]*?)```/g)].map(m => m[1]);
console.log('dataviewjs 块数 =', blocks.length);
let ok = 0;
blocks.forEach((c, i) => {
  try {
    // dataviewjs 在 async 上下文中执行 ⇒ 用 async IIFE 包住以允许顶层 await
    new Function('dv', 'app', 'return (async () => {' + c + '})();');
    ok++; console.log('  块#' + (i + 1) + ' 语法 OK（' + c.split('\n').length + ' 行）');
  } catch (e) {
    console.log('  块#' + (i + 1) + ' 语法错误: ' + e.message);
  }
});
// 同时统计 dataview(非js) 块
const plain = [...t.matchAll(/```dataview\n([\s\S]*?)```/g)].length;
console.log('dataview(表格) 块数 =', plain);
console.log(ok === blocks.length ? 'ALL SYNTAX OK' : 'HAS ERRORS');
