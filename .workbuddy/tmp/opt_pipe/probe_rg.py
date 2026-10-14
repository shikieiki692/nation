# -*- coding: utf-8 -*-
r"""直接调用 render_gate.gate_docx 于缺陷文件，看返回值与预处理后内容。"""
import io, os, sys, importlib.util
os.chdir(r'C:\Obsidion\妙妙屋')
spec = importlib.util.spec_from_file_location('rg', '11-模板/scripts/render_gate.py')
rg = importlib.util.module_from_spec(spec)
sys.modules['rg'] = rg
try:
    spec.loader.exec_module(rg)
except SystemExit:
    pass
print('PANDOC_EXT =', rg.PANDOC_EXT[:80])
bh = rg._load_bh() if hasattr(rg, '_load_bh') else None
print('bh:', type(bh).__name__ if bh else None)
if bh:
    t = io.open('.workbuddy/tmp/opt_pipe/_rg_test.md', encoding='utf-8').read()
    pre = bh._preprocess_markdown(rg.strip_frontmatter(t))
    print('--- 预处理后 ---')
    print(repr(pre))
    nf, lit, om, snip = rg.gate_docx(bh, t)
    print('gate_docx => 失败%d 字面$%d oMath%d  %s' % (nf, lit, om, snip))
