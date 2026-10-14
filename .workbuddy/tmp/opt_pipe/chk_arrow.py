# -*- coding: utf-8 -*-
r"""渲染复核：两个文件 pandoc→docx，查是否有残留字面宏名（texmath 放弃的痕迹）。"""
import io, os, re, subprocess, zipfile
os.chdir(r'C:\Obsidion\妙妙屋')
PANDOC = r'C:\Users\蕾赛\AppData\Local\Pandoc\pandoc.exe'
FILES = [
 '04-题库/元文件/有机化学阶段测试卷-答案.md',
 '04-题库/有机化学/有机合成与金属有机/题-有机-合成-Grignard试剂与不同羰基化合物反应路线设计.md',
]
for p in FILES:
    tmp = '.workbuddy/tmp/opt_pipe/_chk.md'
    out = '.workbuddy/tmp/opt_pipe/_chk.docx'
    src = io.open(p, encoding='utf-8-sig').read()
    io.open(tmp, 'w', encoding='utf-8', newline='').write(src)
    r = subprocess.run([PANDOC, tmp, '-o', out], capture_output=True, text=True, encoding='utf-8')
    x = zipfile.ZipFile(out).read('word/document.xml').decode('utf-8')
    txt = ''.join(re.findall(r'<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>', x))
    bad = {k: txt.count(k) for k in ['xrightarrow', 'substack', 'mathrm', 'begin{array}'] if txt.count(k)}
    print('%-64s oMath=%-4d 残留=%s' % (os.path.basename(p)[:62], len(re.findall(r'<m:oMath[ >]', x)), bad if bad else '无 ✅'))
    warn = [l for l in (r.stderr or '').split('\n') if 'Could not convert' in l]
    if warn:
        print('   ⚠️ pandoc 转换告警 %d 条' % len(warn))
