"""Test full Eisvogel pipeline: pandoc MD -> xelatex PDF (Chinese)"""
import subprocess, os

os.chdir(r'C:\Obsidion\妙妙屋\11-模板\scripts')
env = os.environ.copy()
env['PATH'] += r';C:\Users\蕾赛\AppData\Local\Programs\MiKTeX\miktex\bin\x64'

# Use full paths
pandoc = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\Lib\site-packages\pypandoc\files\pandoc.exe'

# Step 1: MD -> LaTeX
r1 = subprocess.run([
    pandoc, '_test_eisvogel.md', '-o', '_eisvogel_cn.tex',
    '--template=eisvogel',
    '--from=markdown+tex_math_dollars+raw_tex',
    '--include-in-header=chemistry-header.tex',
    '-V', 'CJKmainfont=SimSun',
    '-V', 'CJKsansfont=SimHei',
    '--toc'
], env=env)
print(f'MD->LaTeX: exit={r1.returncode}')

# Step 2: .tex -> PDF
xelatex = r'C:\Users\蕾赛\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe'
r2 = subprocess.run([
    xelatex, '-interaction=nonstopmode', '_eisvogel_cn.tex'
], capture_output=True, text=True, env=env, timeout=120)

# Check result
pdf_path = '_eisvogel_cn.pdf'
if os.path.exists(pdf_path):
    size = os.path.getsize(pdf_path) // 1024
    print(f'PDF OK: {pdf_path} ({size} KB)')
    # Success - rename to show the Chinese version
    os.rename(pdf_path, '_test_eisvogel_final.pdf')
    print(f'Renamed to _test_eisvogel_final.pdf')
else:
    print('NO PDF generated')
    for line in r2.stdout.split('\n')[-10:]:
        if line.startswith('!'):
            print(line)
