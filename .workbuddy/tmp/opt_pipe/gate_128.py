# -*- coding: utf-8 -*-
r"""FM strict 闸门 + pandoc 渲染实测（查 docx 里是否残留字面 mathrm）。"""
import io, os, json, subprocess, zipfile, re
os.chdir(r'C:\Obsidion\妙妙屋')
PY = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\python.exe'
P = '04-题库/教材习题/ABOC/题-128-ABOC-Ch4-4.13.1-Cannizzaro 康尼查罗 反应是醛在强碱浓溶液中发生的.md'

src = io.open(P, encoding='utf-8-sig').read()
fm = src.split('---')[1]
r = subprocess.run([PY, '-X', 'utf8', '.workbuddy/scripts/yaml_compat.py'],
                   input=json.dumps([{'id': P, 'source': fm, 'mode': 'strict'}]),
                   capture_output=True, text=True, encoding='utf-8')
print('FM strict:', json.loads(r.stdout)[0].get('ok'))

# pandoc 渲染
tmp = '.workbuddy/tmp/opt_pipe/_r128.md'
io.open(tmp, 'w', encoding='utf-8', newline='').write(src)
out = '.workbuddy/tmp/opt_pipe/_r128.docx'
subprocess.run([r'C:\Users\蕾赛\AppData\Local\Pandoc\pandoc.exe', tmp, '-o', out], capture_output=True)
z = zipfile.ZipFile(out)
x = z.read('word/document.xml').decode('utf-8')
txt = ''.join(re.findall(r'<(?:w|m):t[^>]*>([^<]*)</(?:w|m):t>', x))
print('docx 可见文本中 "mathrm" 出现次数:', txt.count('mathrm'), '（0 = 全部渲染为公式）')
print('oMath 数:', len(re.findall(r'<m:oMath[ >]', x)))
# 抽看含 D2O 的段落
for m in re.finditer(r'D_?2O|D₂O', txt):
    s = max(0, m.start() - 30); print('   片段:', repr(txt[s:m.end() + 20])); break
