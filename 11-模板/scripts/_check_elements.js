const fs = require('fs');
const path = require('path');

const fpath = 'C:\\Obsidion\\妙妙屋\\media\\第二周期MO能级对比.关系图.md';
const content = fs.readFileSync(fpath, 'utf8');
const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/);
if (!jsonMatch) { console.log('no json'); process.exit(1); }
const data = JSON.parse(jsonMatch[1]);
console.log('Elements:', data.elements.length);
const types = {};
for (const el of data.elements) {
    types[el.type] = (types[el.type] || 0) + 1;
}
console.log('Types:', JSON.stringify(types));
