# -*- coding: utf-8 -*-
r"""用管线的 _preprocess_markdown 处理「修复前」的 Cannizzaro 卡，看 \\mathrm / \\qquad 是否真坏。"""
import io, os, sys, glob, re, subprocess, zipfile, importlib.util
os.chdir(r'C:\Obsidion\妙妙屋')
spec = importlib.util.spec_from_file_location('rg', '11-模板/scripts/render_gate.py')
rg = importlib.util.module_from_spec(spec); sys.modules['rg'] = rg
try:
    spec.loader.exec_module(rg)
except SystemExit:
    pass
bh = rg._load_pipeline()

for bak in sorted(glob.glob('.workbuddy/tmp/opt_pipe/_bak/bs_*')):
    fs = [f for f in os.listdir(bak) if f.endswith('.md')]
    if not fs:
        continue
    p = os.path.join(bak, fs[0])
    t = io.open(p, encoding='utf-8-sig').read()
    pre = bh._preprocess_markdown(rg.strip_frontmatter(t))
    # 看预处理后是否仍有 \\mathrm / \\qquad
    n1 = len(re.findall(r'\\\\mathrm', pre))
    n2 = len(re.findall(r'\\\\qquad', pre))
    io.open('.workbuddy/tmp/opt_pipe/_pre.md', 'w', encoding='utf-8', newline='').write(pre)
    subprocess.run([r'C:\Users\蕾赛\AppData\Local\Pandoc\pandoc', '-f', rg.PANDOC_EXT, '-t', 'docx',
                    '-o', '.workbuddy/tmp/opt_pipe/_pre.docx', '.workbuddy/tmp/opt_pipe/_pre.md'],
                   capture_output=True, text=True, encoding='utf-8')
    x = zipfile.ZipFile('.workbuddy/tmp/opt_pipe/_pre.docx').read('word/document.xml').decode('utf-8')
    txt = ''.join(re.findall(r'<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>', x))
    print('备份 %s' % os.path.basename(bak))
    print('   预处理后残留 \\\\mathrm=%d  \\\\qquad=%d' % (n1, n2))
    print('   渲染后可见文本残留 mathrm=%d  qquad=%d  (oMath=%d)'
          % (txt.count('mathrm'), txt.count('qquad'), len(re.findall(r'<m:oMath', x))))
