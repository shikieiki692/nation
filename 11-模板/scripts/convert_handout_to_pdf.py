"""批量转换超级充实版讲义：Markdown → LaTeX PDF（v2）

改进 vs v1：
  - Unicode 上下标使用 Pandoc ^...^ 语法（AST 级，比 LaTeX 字符串替换可靠）
  - 中文→ASCII 图片别名从外部 JSON 加载（不硬编码在代码里）
  - 并行构建支持 `python convert.py --parallel ALL`
  - xelatex 失败自动诊断（显示 .log 尾部）
  - 完整度验证输出（图数/缺图/页数）
"""
import subprocess, os, re, sys, shutil, json
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPTS = r'C:\Obsidion\妙妙屋\11-模板\scripts'
HANDOUTS = r'C:\Obsidion\妙妙屋\04-课件\学生讲义'
PANDOC = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\Lib\site-packages\pypandoc\files\pandoc.exe'
XELATEX = r'C:\Users\蕾赛\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe'
LUA_FILTER = os.path.join(SCRIPTS, 'wrap_images.lua')
PREAMBLE_FILE = os.path.join(SCRIPTS, 'chemistry-preamble.tex')
ALIAS_FILE = os.path.join(SCRIPTS, 'chem_media_aliases.json')

_CHEM_MEDIA = r'C:/Temp/chem_media/'
_CHEM_MEDIA_WIN = r'C:\Temp\chem_media'

env = os.environ.copy()
env['PATH'] += r';C:\Users\蕾赛\AppData\Local\Programs\MiKTeX\miktex\bin\x64'

# ── Unicode 上下标 → ASCII 映射 ──
SUP_MAP = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁺':'+','⁻':'-'}
SUB_MAP = {'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9'}

_media_aliases = None


def get_aliases():
    global _media_aliases
    if _media_aliases is not None:
        return _media_aliases
    if os.path.exists(ALIAS_FILE):
        with open(ALIAS_FILE, encoding='utf-8') as f:
            _media_aliases = json.load(f)
    else:
        _media_aliases = {}
    return _media_aliases


def preprint(source_md: str) -> str:
    """预处理 Markdown（v2）"""
    text = re.sub(r'^---\n.*?\n---\n', '', source_md, flags=re.DOTALL)

    # 剥元数据引用行
    lines = text.split('\n')
    out = []
    for line in lines:
        s = line.strip()
        if s.startswith('> **') and any(k in s for k in ['适用', '对应', '前置', '深度', '课时', '建议', '使用', '版本', '说明']):
            continue
        if s == '>' or s.startswith('> [!') or s.startswith('> ['):
            continue
        if (s.startswith('> ') or s.startswith('>')) and not any(k in s for k in ['🧠', '⚠️', '💡', '🗣️', '📝', '🧪', '✏️', '☐', '✅']):
            txt = s.lstrip('>').strip()
            if txt: out.append(txt)
            continue
        out.append(line)
    text = '\n'.join(out)

    # ── Unicode 上下标 → Pandoc ^...^ / ~...~ 语法 ──
    # Pandoc 的 +superscript+subscript 扩展支持 ^n^ → \textsuperscript{n}
    # 这比 LaTeX 后处理做字符串替换更可靠（AST 级别转换）
    text = re.sub(
        r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+',
        lambda m: '^' + ''.join(SUP_MAP.get(c, c) for c in m.group(0)) + '^',
        text
    )
    text = re.sub(
        r'[₀₁₂₃₄₅₆₇₈₉]+',
        lambda m: '~' + ''.join(SUB_MAP.get(c, c) for c in m.group(0)) + '~',
        text
    )

    # 图片引用
    text = re.sub(r'!\[\[media/([^\]|]+)\|[^\]]*\]\]', r'![](media/\1)', text)
    text = re.sub(r'!\[\[media/([^\]|]+)\]\]', r'![](media/\1)', text)
    text = re.sub(r'\.(lewis\.)?md\)', r'.\1png)', text)

    # wikilink → 纯文本
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)

    # HTML 清理：<center>图 xxx</center> → *图 xxx*（Lua filter 通过 Emph 识别图注）
    text = re.sub(r'<center>图\s*', '*图 ', text, flags=re.IGNORECASE)
    text = re.sub(r'</center>', '*', text)
    text = re.sub(r'<br\s*/?>', ' ', text)
    text = re.sub(r'<sup>([^<]+)</sup>', r'^\1', text)
    text = re.sub(r'<sub>([^<]+)</sub>', r'_\1', text)

    # 来源 Dataview 清理
    text = re.sub(r'\*\*来源\*\*[：:][^\n]*\n?', '', text)
    text = re.sub(r'\*来源\*[：:][^\n]*\n?', '', text)
    text = re.sub(r'来源于[^\n。]*[。]?\n?', '', text)
    text = re.sub(r'[（(]主要内容来源[：:][^）)]*[）)]', '', text)
    text = re.sub(r'\*主要内容来源[：:][^\n]*\n?', '', text)
    text = re.sub(r'\*本讲义依据[^\n]*\n?', '', text)

    # 空括号
    text = re.sub(r'（\s*）', '', text)

    # 表格对齐线：中文破折号 → ASCII
    text = re.sub(r'^\|:——', '|:---', text, flags=re.MULTILINE)
    text = re.sub(r'——:\|$', '---:|', text, flags=re.MULTILINE)
    text = re.sub(r'——:\s*\|', '---:|', text)
    text = re.sub(r'^\s*\|[:\-]*——', lambda m: m.group(0).replace('——', '--'), text, flags=re.MULTILINE)

    def fix_table_alignment(m):
        line = m.group(0)
        if line.count('|') >= 2 and all(c in '|:-\n ——' for c in line.replace('—', ':')):
            return line.replace('——:', '---:').replace(':——', ':---').replace('——', '---')
        return line
    text = re.sub(r'^[|>: \-—:]+\n', fix_table_alignment, text, flags=re.MULTILINE)

    # 例题格式
    text = re.sub(r'(例\d+\s*)\[', r'\1', text)
    text = re.sub(r'\](?=\s*[⭐★])', '', text)
    text = re.sub(r'\](?=\s*$)', '', text)

    # 练习题标题后缀
    text = re.sub(r'(基础巩固|提高训练|挑战题)\s*[（(][^）)]*[）)]', r'\1', text)

    # 参考答案数字编号前加空行
    lines = text.split('\n')
    in_answer = False
    result = []
    for line in lines:
        s = line.strip()
        if '参考答案与提示' in s and s.startswith('#'):
            in_answer = True
        elif in_answer and s.startswith('## ') and '参考答案' not in s:
            in_answer = False
        if in_answer and re.match(r'^\d+[.、]', s) and result and result[-1].strip():
            result.append('')
        result.append(line)
    text = '\n'.join(result)

    # 电子排布特殊乱码
    text = text.replace('3dfl', '3d⁵')
    text = text.replace('4sfl', '4s¹')

    return text


def convert_one(md_name, parallel=False):
    """转换一本讲义为 PDF"""
    md_path = os.path.join(HANDOUTS, md_name)
    if not os.path.exists(md_path):
        return (md_name, False, '文件不存在')

    cn_map = get_aliases()
    safe_name = re.sub(r'[^a-zA-Z0-9_一-鿿-]', '', md_name.replace('.md',''))
    label = f'[{md_name}]'
    if not parallel:
        print(f'\n{"="*50}\n  {md_name}')

    # ── 1. 预处理（使用独立临时文件避免并行竞态）──
    try:
        with open(md_path, encoding='utf-8') as f:
            processed = preprint(f.read())
    except Exception as e:
        return (md_name, False, f'预处理失败: {e}')
    pre_path = os.path.join(SCRIPTS, f'_pre_{safe_name}.md')
    with open(pre_path, 'w', encoding='utf-8') as f:
        f.write(processed)

    title = md_name.replace('.md','').split('-超级充实版')[0] if '超级充实版' in md_name else md_name.replace('.md','')

    # ── 2. Pandoc → LaTeX body（独立文件名）──
    body_path = os.path.join(SCRIPTS, f'_body_{safe_name}.tex')
    try:
        r1 = subprocess.run([
            PANDOC, pre_path, '-o', body_path,
            '--from=markdown+tex_math_dollars+raw_tex+pipe_tables+grid_tables+superscript+subscript-yaml_metadata_block',
            '--to=latex', '--lua-filter=' + LUA_FILTER, '--wrap=preserve',
        ], env=env, capture_output=True, timeout=60)
        for attr in ('stdout', 'stderr'):
            raw = getattr(r1, attr)
            try:
                decoded = raw.decode('utf-8', errors='replace')
            except Exception:
                decoded = raw.decode('gbk', errors='replace')
            setattr(r1, attr, decoded)
        if r1.returncode != 0 or not os.path.exists(body_path):
            err = (r1.stderr or '')[:500]
            return (md_name, False, f'Pandoc 失败: {err}')
    except subprocess.TimeoutExpired:
        return (md_name, False, 'Pandoc 超时(60s)')

    with open(body_path, encoding='utf-8') as f:
        body = f.read()

    # ── 3. 构建完整 LaTeX ──
    with open(PREAMBLE_FILE, encoding='utf-8') as f:
        preamble = f.read()

    full_tex = (
        preamble
        + '\n\\graphicspath{{' + _CHEM_MEDIA + '}}\n'
        + '\\title{' + title + '}\n'
        + '\\date{}\n'
        + '\\setlength{\\tabcolsep}{3.5pt}\n\\small\n'
        + '\\begin{document}\n'
        + '\\maketitle\n'
        + '\\tableofcontents\n'
        + '\\newpage\n'
        + body
        + '\n\\end{document}\n'
    )

    # 后处理：pandoc 产物清理
    full_tex = full_tex.replace('\\pandocbounded{', '')
    full_tex = full_tex.replace('{media/', '{')
    full_tex = full_tex.replace('.md}', '.png}')

    # 转义 caption 中的特殊字符（避免格式断裂）
    # 策略：将所有 caption 中 $...$ 外的 _ 转义
    def escape_caption(m):
        txt = m.group(1)
        txt = txt.replace('%', r'\%')
        parts = txt.split('$')
        for i in range(0, len(parts), 2):
            parts[i] = parts[i].replace('_', r'\_')
        txt = '$'.join(parts)
        return '\\caption{' + txt + '}'
    full_tex = re.sub(r'\\caption\{([^}]*)\}', escape_caption, full_tex)
    for cn, ascii_n in cn_map.items():
        full_tex = full_tex.replace('{' + cn, '{' + ascii_n)

    # ── 4. 缺图+格式检查 + GIF→PNG 转码 ──
    img_count = 0
    missing_imgs = []
    img_format_issues = []

    def check_img(m):
        nonlocal img_count, missing_imgs, img_format_issues
        full_cmd = m.group(0)
        fn = m.group(1)
        img_count += 1

        # 尝试别名查找
        real_fn = fn
        for cn, ascii_n in cn_map.items():
            if ascii_n == fn:
                real_fn = cn
                break

        fp = os.path.join(_CHEM_MEDIA_WIN, real_fn)

        if not os.path.exists(fp):
            # 尝试扩展名变体：jpg↔png↔gif
            base = os.path.splitext(fp)[0]
            found_fp = None
            for ext in ['.png', '.jpg', '.gif', '.jpeg']:
                v = base + ext
                if os.path.exists(v):
                    found_fp = v
                    break

            if found_fp:
                new_fn = os.path.basename(found_fp)
                # GIF → PNG 转换（LaTeX graphicx 不支持 GIF）
                if found_fp.lower().endswith('.gif'):
                    png_fp = base + '.png'
                    if not os.path.exists(png_fp):
                        try:
                            from PIL import Image
                            img = Image.open(found_fp)
                            img.save(png_fp, 'PNG')
                            found_fp = png_fp
                            new_fn = os.path.basename(png_fp)
                            img_format_issues.append(f'{fn} → {new_fn} (GIF→PNG)')
                        except Exception:
                            # Pillow 不可用或转换失败，保留原文件
                            img_format_issues.append(f'{fn} → {new_fn} (⚠️ GIF LaTeX 可能不支持)')
                            pass
                    else:
                        found_fp = png_fp
                        new_fn = os.path.basename(png_fp)
                else:
                    img_format_issues.append(f'{fn} → {new_fn}')

                # 更新 LaTeX 中的引用
                full_cmd = full_cmd.replace('{' + fn + '}', '{' + new_fn + '}')
                return full_cmd

            missing_imgs.append(fn)
            return '\\textbf{[⛔ 缺图: ' + os.path.splitext(fn)[0] + ']}'
        return full_cmd

    full_tex = re.sub(r'\\includegraphics\[[^\]]*\]\{([^}]+)\}', check_img, full_tex)

    # ── 5. xelatex 编译 ──
    safe_name = re.sub(r'[^a-zA-Z0-9_一-鿿-]', '', md_name.replace('.md',''))
    tex_path = os.path.join(SCRIPTS, f'_handout_{safe_name}.tex')
    pdf_temp = os.path.join(SCRIPTS, f'_handout_{safe_name}.pdf')
    pdf_backup = os.path.join(SCRIPTS, f'_handout_{safe_name}_p1.pdf')

    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(full_tex)

    log_errors = []
    for i in range(2):
        try:
            r2 = subprocess.run([
                XELATEX, '-interaction=nonstopmode',
                '-output-directory=' + SCRIPTS, tex_path
            ], capture_output=True, env=env, timeout=600)
            for attr in ('stdout', 'stderr'):
                raw = getattr(r2, attr)
                try:
                    decoded = raw.decode('utf-8', errors='replace')
                except Exception:
                    decoded = raw.decode('gbk', errors='replace')
                setattr(r2, attr, decoded)
        except subprocess.TimeoutExpired:
            return (md_name, False, 'xelatex 超时(600s)')

        if i == 0 and os.path.exists(pdf_temp) and os.path.getsize(pdf_temp) > 20000:
            shutil.copy2(pdf_temp, pdf_backup)

        # 收集错误行
        for line in r2.stdout.split('\n'):
            if any(kw in line for kw in ['! ', 'Error', 'Fatal', 'emergency']):
                log_errors.append(line.strip())

    # 失败诊断
    if (not os.path.exists(pdf_temp) or os.path.getsize(pdf_temp) < 5000):
        log_path = tex_path.replace('.tex', '.log')
        if os.path.exists(log_path):
            with open(log_path, encoding='utf-8', errors='replace') as f:
                log_tail = f.readlines()[-40:]
            log_errors = [l.strip() for l in log_tail if l.strip()]
        if os.path.exists(pdf_backup) and os.path.getsize(pdf_backup) > 20000:
            shutil.copy2(pdf_backup, pdf_temp)

    # ── 6. PDF 完整性验证 ──
    if not os.path.exists(pdf_temp) or os.path.getsize(pdf_temp) < 5000:
        diag = '\n'.join(log_errors[-15:]) if log_errors else 'xelatex 输出为空'
        return (md_name, False, f'PDF 生成失败\n{diag[:600]}')

    with open(pdf_temp, 'rb') as f:
        c = f.read()
    if c[:5] != b'%PDF-' or c.rfind(b'%%EOF') < 0:
        return (md_name, False, 'PDF 完整性校验失败')

    pages = '?'
    # 从 .log 提取页数：xelatex -interaction=nonstopmode 无 Output written,
    # 但日志末尾有 [N] 页标，取最大值
    log_path = tex_path.replace('.tex', '.log')
    if os.path.exists(log_path):
        with open(log_path, encoding='utf-8', errors='replace') as lf:
            log_content = lf.read()
        # 取最后出现的 [N]...] 页标中的最大值
        for m in re.finditer(r'\[(\d+)\]', log_content):
            pages = m.group(1)  # 最后一个即为总页数

    size_kb = os.path.getsize(pdf_temp) // 1024
    out_name = md_name.replace('.md', '.pdf')
    out_path = os.path.join(HANDOUTS, out_name)
    try:
        if os.path.exists(out_path):
            os.remove(out_path)
        shutil.copy2(pdf_temp, out_path)
    except PermissionError:
        alt_path = os.path.join(HANDOUTS, '_new_' + out_name)
        shutil.copy2(pdf_temp, alt_path)
        out_path = alt_path

    miss_str = f', 缺图={len(missing_imgs)} ⚠️' if missing_imgs else ', 全图 ✓'
    msg = f'{size_kb}KB, {pages}p, {img_count}张图{miss_str}'
    if not parallel:
        print(f'  PDF → {os.path.basename(out_path)}  ({msg})')
    return (md_name, True, msg)


if __name__ == '__main__':
    is_parallel = any(a.upper() in ('--PARALLEL', '-P') for a in sys.argv)
    args = [a for a in sys.argv[1:] if not a.upper() in ('--PARALLEL', '-P')]

    if args and args[0].upper() == 'ALL':
        targets = ['原子结构-超级充实版（自学完整）.md',
                   '元素周期表与周期律-超级充实版（自学完整）.md',
                   '分子结构基础-超级充实版（自学完整）.md',
                   '配位化合物基础-超级充实版（自学完整）.md',
                   '晶体学基础-超级充实版（自学完整）.md',
                   '晶体结构基础-超级充实版（自学完整）.md']
    else:
        targets = args if args else ['配位化合物基础-超级充实版（自学完整）.md']

    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

    if is_parallel and len(targets) > 1:
        print(f'\n并行构建 {len(targets)} 本（最多3路并发）...\n')
        results = {}
        with ThreadPoolExecutor(max_workers=3) as pool:
            fut_map = {pool.submit(convert_one, t, True): t for t in targets}
            for fut in as_completed(fut_map):
                name, ok, msg = fut.result()
                results[name] = (ok, msg)
                print(f'  {"✅" if ok else "❌"} {name}' + (f'\n    → {msg}' if not ok else ''))
        print(f'\n结果汇总：')
        ok_count = sum(1 for t in targets if t in results and results[t][0])
        print(f'  {ok_count}/{len(targets)} 成功')
        for t in targets:
            if t in results:
                ok, msg = results[t]
                print(f'  {"✅" if ok else "❌"} {msg}')
    else:
        had_err = False
        for t in targets:
            name, ok, msg = convert_one(t)
            if not ok:
                had_err = True
                print(f'\n  ❌ {name}\n  → {msg}')
        print(f'\n{"="*50}\n{"全部成功 ✅" if not had_err else "部分失败 ❌"}')
