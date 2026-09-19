// 渲染自证器：读 stdin 的 JSON 数组 [{id, md}]，逐条用 markdown-it+KaTeX 渲染
// 输出 JSON: [{id, katex, dollar, ok}]
//
// 判据演进（2026-09-20）：
//   旧：ok = (katex > 0 && dollar === 0)
//       —— 只适用于「含公式表」。Wave4 起纳入**纯文字表**（不涉及公式渲染，
//          但 Word 导出时 <table> 会被拍平成段落），这类表 katex 恒为 0，
//          用旧判据会 100% 误判为失败（实测 1,068 张假失败）。
//   新：ok = (dollar === 0 && (!hasDollar || katex > 0))
//       —— 无残留 $ 即渲染正确；若原文含 $ 则还须确有渲染发生。
const MarkdownIt = require('markdown-it');
const katex = require('katex');

function makeMd() {
  const md = new MarkdownIt({ html: true });
  md.inline.ruler.before('escape', 'math_inline', function (state, silent) {
    const s = state.pos;
    if (state.src[s] !== '$') return false;
    if (state.src[s + 1] === '$') return false;
    const e = state.src.indexOf('$', s + 1);
    if (e === -1) return false;
    const c = state.src.slice(s + 1, e);
    if (!c.trim()) return false;
    // ⚠️ markdown-it 在 silent（前瞻）模式下要求规则必须推进 state.pos 或返回 false，
    //    否则抛 "inline rule didn't increment state.pos"。故 silent 分支也要设 pos。
    if (silent) { state.pos = e + 1; return true; }
    const t = state.push('math_inline', 'math', 0);
    t.content = c; state.pos = e + 1; return true;
  });
  md.renderer.rules.math_inline = (t, i) =>
    katex.renderToString(t[i].content, { throwOnError: false, output: 'html' });
  return md;
}
const md = makeMd();

let buf = '';
process.stdin.setEncoding('utf-8');
process.stdin.on('data', d => buf += d);
process.stdin.on('end', () => {
  let items;
  try {
    items = JSON.parse(buf);
  } catch (e) {
    process.stdout.write(JSON.stringify({ error: 'bad input: ' + e.message }));
    return;
  }
  const res = items.map(it => {
    let out = '';
    try {
      out = md.render(it.md);
    } catch (e) {
      return { id: it.id, katex: 0, dollar: -1, ok: false, err: String(e) };
    }
    const nk = (out.match(/class="katex"/g) || []).length;
    const nd = (out.match(/\$/g) || []).length;
    const hasDollar = it.md.includes('$');
    return { id: it.id, katex: nk, dollar: nd,
             ok: nd === 0 && (!hasDollar || nk > 0) };
  });
  process.stdout.write(JSON.stringify(res));
});
