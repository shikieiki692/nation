# -*- coding: utf-8 -*-
r"""选型试验：`\xrightarrow{...\\...}` 的三种改法哪种能被 texmath 渲染。"""
import io, os, re, subprocess, zipfile
os.chdir(r'C:\Obsidion\妙妙屋')
B = chr(92)
PANDOC = r'C:\Users\蕾赛\AppData\Local\Pandoc\pandoc.exe'

cases = {
    'A 原样(双反斜杠)': '$$' + '\n' + B + 'mathrm{A ' + B + 'xrightarrow{1.;' + B + ';Et_2O' + B + B + '2.;' + B + ';H_3O^+} B}' + '\n' + '$$',
    'B substack': '$$' + '\n' + B + 'mathrm{A ' + B + 'xrightarrow{' + B + 'substack{1.;' + B + ';Et_2O' + B + B + '2.;' + B + ';H_3O^+}} B}' + '\n' + '$$',
    'C 单行(去换行)': '$$' + '\n' + B + 'mathrm{A ' + B + 'xrightarrow{1.;' + B + ';Et_2O , 2.;' + B + ';H_3O^+} B}' + '\n' + '$$',
    'D array 两行': '$$' + '\n' + B + 'begin{array}{l}' + B + 'mathrm{A ' + B + 'xrightarrow{ } B}' + B + B + 'mathrm{C}' + B + 'end{array}' + '\n' + '$$',
    'E substack(独立)': '$$' + '\n' + B + 'substack{a' + B + B + 'b}' + '\n' + '$$',
}
for name, md in cases.items():
    src = '.workbuddy/tmp/opt_pipe/_sel.md'
    io.open(src, 'w', encoding='utf-8', newline='').write(md + '\n')
    out = '.workbuddy/tmp/opt_pipe/_sel.docx'
    r = subprocess.run([PANDOC, src, '-o', out], capture_output=True, text=True, encoding='utf-8')
    x = zipfile.ZipFile(out).read('word/document.xml').decode('utf-8')
    txt = ''.join(re.findall(r'<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>', x))
    lit = any(k in txt for k in ['mathrm', 'xrightarrow', 'substack', 'begin{array}'])
    print('%-18s oMath=%-3d 残留字面=%s  %s' % (name, len(re.findall(r'<m:oMath[ >]', x)), 'YES❌' if lit else 'no✅', (r.stderr or '').strip().split('\n')[-1][:60]))
