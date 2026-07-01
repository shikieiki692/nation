"""批量转换超级充实版讲义：Markdown → LaTeX PDF（v3）

改进 vs v2：
  - 图片统一目录：源图统一维护在 vault 根目录 media/，编译缓存改为 workspace-local
  - PDF 成品统一输出到 00-首页/学生讲义PDF/，不再回写源讲义目录
  - Unicode 上下标直接透传（xelatex 原生支持，无需转 Pandoc 语法）
  - 去除 {media/ 剥离逻辑，保持路径一致性
  - 去除 .md}→.png} 扩展名替换
  - MiKTeX 使用 workspace 内沙箱，绕开受限的 AppData 写入
  - 预热 fontconfig，避免 XeLaTeX 首次启动卡死或报默认配置缺失
"""
import subprocess, os, re, sys, shutil, json, hashlib
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPTS = r'C:\Obsidion\妙妙屋\11-模板\scripts'
VAULT_ROOT = r'C:\Obsidion\妙妙屋'
HANDOUTS = r'C:\Obsidion\妙妙屋\04-课件\学生讲义'
PDF_OUTPUT_DIR = os.path.join(VAULT_ROOT, '00-首页', '学生讲义PDF')
VAULT_MEDIA = os.path.join(VAULT_ROOT, 'media')
PANDOC = r'C:\Users\蕾赛\AppData\Local\Programs\Python\Python312\Lib\site-packages\pypandoc\files\pandoc.exe'
XELATEX = r'C:\Users\蕾赛\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe'
LUA_FILTER = os.path.join(SCRIPTS, 'wrap_images.lua')
PREAMBLE_FILE = os.path.join(SCRIPTS, 'chemistry-preamble.tex')
ALIAS_FILE = os.path.join(SCRIPTS, 'chem_media_aliases.json')
MIKTEX_BIN = os.path.dirname(XELATEX)
MIKTEX_INSTALL_ROOT = os.path.normpath(os.path.join(MIKTEX_BIN, os.pardir, os.pardir, os.pardir))
FC_CONFLIST = os.path.join(MIKTEX_BIN, 'fc-conflist.exe')
MIKTEX_SANDBOX = os.path.join(SCRIPTS, '.miktex-sandbox')
MEDIA_CACHE_DIR = os.path.join(SCRIPTS, '.chem_media')
MIKTEX_FLAGS = [
    '--miktex-disable-installer',
    '--miktex-disable-maintenance',
    '--miktex-disable-diagnose',
]

_CHEM_MEDIA_WIN = MEDIA_CACHE_DIR
_CHEM_MEDIA = MEDIA_CACHE_DIR.replace('\\', '/') + '/'

base_env = os.environ.copy()
base_env['PATH'] = base_env.get('PATH', '') + ';' + MIKTEX_BIN

_media_aliases = None
_miktex_ready = False
_miktex_lock = Lock()

# ── Unicode 上下标映射（数字上标转 ASCII）──
SUP_MAP = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁺':'+','⁻':'-'}
SUB_MAP = {'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9'}


def decode_subprocess_output(result):
    for attr in ('stdout', 'stderr'):
        raw = getattr(result, attr)
        if raw is None or isinstance(raw, str):
            continue
        try:
            decoded = raw.decode('utf-8', errors='replace')
        except Exception:
            decoded = raw.decode('gbk', errors='replace')
        setattr(result, attr, decoded)
    return result


def resolve_md_target(md_target):
    md_target = os.path.normpath(md_target)
    if os.path.isabs(md_target):
        md_path = md_target
    else:
        vault_candidate = os.path.normpath(os.path.join(VAULT_ROOT, md_target))
        handout_candidate = os.path.normpath(os.path.join(HANDOUTS, md_target))
        md_path = vault_candidate if os.path.exists(vault_candidate) else handout_candidate
    return os.path.basename(md_path), md_path


def latex_escape_text(text):
    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
    }
    return ''.join(replacements.get(ch, ch) for ch in text)


def build_manual_toc_latex(processed_md):
    entries = []
    for line in processed_md.splitlines():
        m = re.match(r'^##\s+(.+?)\s*$', line)
        if not m:
            continue
        heading = m.group(1).strip()
        heading = re.sub(r'\[\[([^|\]]+)\|([^]]+)\]\]', r'\2', heading)
        heading = re.sub(r'\[\[([^]]+)\]\]', r'\1', heading)
        heading = heading.replace('`', '')
        if heading:
            entries.append(latex_escape_text(heading))

    if not entries:
        return ''

    parts = [
        r'{\large\bfseries 目录\par}',
        r'\vspace{0.6em}',
        r'\begin{itemize}[leftmargin=1.6em,label={},itemsep=0.3em,topsep=0.2em]',
    ]
    for entry in entries:
        parts.append(r'\item ' + entry)
    parts.extend([
        r'\end{itemize}',
        r'\vspace{0.4em}',
    ])
    return '\n'.join(parts) + '\n'


def resolve_windows_home():
    for candidate in (os.path.expanduser('~'), os.environ.get('USERPROFILE'), os.environ.get('HOME')):
        if candidate and os.path.isdir(candidate):
            return candidate
    return r'C:\Users\蕾赛'


WINDOWS_HOME = resolve_windows_home()


def build_miktex_env():
    env = base_env.copy()
    env['MIKTEX_USERCONFIG'] = os.path.join(MIKTEX_SANDBOX, 'config')
    env['MIKTEX_USERDATA'] = os.path.join(MIKTEX_SANDBOX, 'data')
    env['MIKTEX_USERINSTALL'] = os.path.join(MIKTEX_SANDBOX, 'install')
    env['MIKTEX_USERROOTS'] = MIKTEX_INSTALL_ROOT
    env['HOME'] = WINDOWS_HOME
    env['USERPROFILE'] = WINDOWS_HOME
    drive, tail = os.path.splitdrive(WINDOWS_HOME)
    env['HOMEDRIVE'] = drive or 'C:'
    env['HOMEPATH'] = tail or '\\'
    return env


def ensure_miktex_sandbox():
    global _miktex_ready
    if _miktex_ready:
        return
    with _miktex_lock:
        if _miktex_ready:
            return

        for part in ('config', 'data', 'install'):
            os.makedirs(os.path.join(MIKTEX_SANDBOX, part), exist_ok=True)

        cfg_dir = os.path.join(MIKTEX_SANDBOX, 'config', 'fontconfig', 'config')
        required = (
            os.path.join(cfg_dir, 'fonts.conf'),
            os.path.join(cfg_dir, 'localfonts.conf'),
            os.path.join(cfg_dir, 'localfonts2.conf'),
            os.path.join(MIKTEX_SANDBOX, 'data', 'fontconfig', 'cache'),
        )
        if not all(os.path.exists(path) for path in required):
            try:
                probe = subprocess.run(
                    [FC_CONFLIST, *MIKTEX_FLAGS],
                    env=build_miktex_env(),
                    capture_output=True,
                    timeout=120,
                )
                decode_subprocess_output(probe)
            except subprocess.TimeoutExpired as exc:
                raise RuntimeError('MiKTeX fontconfig 预热超时(120s)') from exc

            if probe.returncode != 0 or not all(os.path.exists(path) for path in required):
                detail = (probe.stderr or probe.stdout or '').strip()
                raise RuntimeError(f'MiKTeX fontconfig 预热失败: {detail[:400]}')

        _miktex_ready = True


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


def maybe_normalize_image_copy(src, dst, warnings):
    ext = os.path.splitext(dst)[1].lower()
    if ext not in ('.png', '.jpg', '.jpeg'):
        return False

    try:
        from PIL import Image
    except Exception:
        return False

    try:
        with Image.open(src) as im:
            actual = (im.format or '').upper()
            dpi = im.info.get('dpi')
            dpi_x = dpi[0] if isinstance(dpi, tuple) and len(dpi) > 0 else None
            dpi_y = dpi[1] if isinstance(dpi, tuple) and len(dpi) > 1 else dpi_x
            low_dpi = bool(dpi_x and dpi_y and min(dpi_x, dpi_y) < 30)
            format_mismatch = (
                (ext == '.png' and actual != 'PNG') or
                (ext in ('.jpg', '.jpeg') and actual not in ('JPEG', 'JPG'))
            )

            if not (low_dpi or format_mismatch):
                return False

            save_kwargs = {'dpi': (300, 300)}
            if ext == '.png':
                converted = im.copy()
                save_format = 'PNG'
            else:
                converted = im.convert('RGB')
                save_format = 'JPEG'
                save_kwargs['quality'] = 95

            converted.save(dst, save_format, **save_kwargs)

            reasons = []
            if format_mismatch:
                reasons.append(f'format={actual}->{ext[1:]}')
            if low_dpi:
                reasons.append(f'dpi={dpi_x:.3f}x{dpi_y:.3f}->300')
            warnings.append(f'{os.path.basename(src)} 规范化缓存 ({", ".join(reasons)})')
            return True
    except Exception as exc:
        warnings.append(f'{os.path.basename(src)} 规范化失败，回退原样复制 ({exc})')
        return False


def copy_media_file(src, dst, warnings):
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if maybe_normalize_image_copy(src, dst, warnings):
            return True
        shutil.copy2(src, dst)
        return True
    except Exception as exc:
        warnings.append(f'{os.path.basename(src)} → {dst} ({exc})')
        return False


def validate_pdf_file(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            data = f.read()
        if not data.startswith(b'%PDF-'):
            return False, 'missing %PDF header'
        if data.rfind(b'startxref') < 0:
            return False, 'missing startxref'
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        _ = len(reader.pages)
        return True, ''
    except Exception as exc:
        return False, str(exc)


def preprint(source_md: str) -> str:
    """预处理 Markdown（v2）"""
    text = re.sub(r'^---\n.*?\n---\n', '', source_md, flags=re.DOTALL)

    # 保护代码块：提取 ```...``` 内容，避免 Unicode→LaTeX 转换破坏代码
    _code_blocks = []
    def _save_code(m):
        _code_blocks.append(m.group(0))
        return f'__CODE_BLOCK_{len(_code_blocks)-1}__'
    text = re.sub(r'```[\s\S]*?```', _save_code, text)

    # ── 1. 保护数学表达式：先提取 $...$ 和 $$...$$，后续转换不破坏 LaTeX ──
    _math_blocks = []
    def _save_math(m):
        _math_blocks.append(m.group(0))
        return f'__MATH_BLOCK_{len(_math_blocks)-1}__'
    # 先提取 $$...$$（display math）——允许 closing $$ 出现在行尾
    text = re.sub(r'\$\$[\s\S]*?\$\$', _save_math, text)
    # 再提取 $...$（inline math，不含 $...$ 嵌套）
    text = re.sub(r'(?<!\$)\$(?!\$)(?:[^$\\]|\\.)+\$(?!\$)', _save_math, text)

    # 剥元数据引用行（仅限第一个 ## 标题之前的区域）
    _first_h2 = re.search(r'^## ', text, re.MULTILINE)
    if _first_h2:
        header_end = _first_h2.start()
        header = text[:header_end]
        body = text[header_end:]
    else:
        header, body = text, ''
    lines = header.split('\n')
    out = []
    for line in lines:
        s = line.strip()
        if s.startswith('> **') and any(k in s for k in ['适用', '对应', '前置', '深度', '课时', '建议', '使用', '版本', '说明', '记号约定', '一轮定位', '本讲定位', '定位', '主框架', '辅助教材', '上节衔接', '下节衔接']):
            continue
        if s == '>' or s.startswith('> [!') or s.startswith('> ['):
            continue
        if (s.startswith('> ') or s.startswith('>')) and not any(k in s for k in ['🧠', '⚠️', '💡', '🗣️', '📝', '🧪', '✏️', '☐', '✅']):
            txt = s.lstrip('>').strip()
            if txt: out.append(txt)
            continue
        out.append(line)
    text = '\n'.join(out) + body

    # ── 2. Unicode 特殊符号 → LaTeX 兼容格式（仅影响非 math 区域）──
    # Unicode 罗马数字 → 普通 ASCII（XeLaTeX 字体不支持 Ⅱ/Ⅳ 等，会显示为空白）
    _rommap = {'Ⅻ':'XII','Ⅺ':'XI','Ⅹ':'X','Ⅸ':'IX','Ⅷ':'VIII','Ⅶ':'VII',
               'Ⅵ':'VI','Ⅴ':'V','Ⅳ':'IV','Ⅲ':'III','Ⅱ':'II','Ⅰ':'I'}
    def _roman_repl(m):
        return _rommap.get(m.group(0), m.group(0))
    text = re.sub(r'[Ⅰ-Ⅻ]', _roman_repl, text)
    # 圈数字 → 普通数字
    text = re.sub(r'[①②③④⑤⑥⑦⑧⑨⑩]', lambda m: {'①':'1.','②':'2.','③':'3.','④':'4.','⑤':'5.',
        '⑥':'6.','⑦':'7.','⑧':'8.','⑨':'9.','⑩':'10.'}[m.group(0)], text)
    # 全角括号 → 半角
    text = text.replace('（', '(').replace('）', ')').replace('——', '---')
    # d 轨道/m 量子数
    text = text.replace(r'dₓᵧ', r'$d_{xy}$').replace(r'dₓ₂', r'$d_{xz}$').replace(r'dᵧ₂', r'$d_{yz}$')
    text = text.replace(r'dₓ²₋ᵧ²', r'$d_{x^{2}-y^{2}}$').replace(r'd₂²', r'$d_{z^{2}}$')
    text = text.replace(r'mₗ', r'$m_{l}$').replace(r'mₛ', r'$m_{s}$')
    # 中文下标：T_转 → $T_{转}$（单个中文字符跟在 _ 后面）
    text = re.sub(r'([A-Za-z])_([一-鿿])', r'$\1_{\2}$', text)
    # 单字母下标：α_F 等（希腊/拉丁字母后跟 _ 加一个字母，排除路径/文件名/URL）
    text = re.sub(r'(?<![/\w])([αβγδεζηθικλμνξοπρστυφχψω])_([A-Za-z])(?![/\.\w])', r'$\\1_{\\2}$', text)
    # K_c K_p K_sp K_a K_b K_f 等下标变量在正文（非 math mode）→ LaTeX
    text = re.sub(r'(?<!\$)K_(c|p|sp|a|b|f|w|d)\b(?!\$)', r'$K_{\\1}$', text)
    # ΔᵣG° ΔᵣH° ΔᵣS° 等热力学量在正文中 → LaTeX（已有 Unicode 下标的情况）
    text = re.sub(r'(?<!\$)Δ([ᵣₚ])\s*([HGSCE])°', r'$\\Delta_{\\1} \\2^{\\circ}$', text)
    # ΔG° ΔH° ΔS° E° K° 等无下标的热力学量 → LaTeX
    text = re.sub(r'(?<!\$)(?<!\\Delta_)Δ([HGS])°', r'$\\Delta \\1^{\\circ}$', text)
    text = re.sub(r'(?<!\$)(?<![a-zA-Z])E°', r'$E^{\\circ}$', text)
    text = re.sub(r'(?<!\$)(?<![a-zA-ZΔ])K°', r'$K^{\\circ}$', text)
    # E°_cell, K°_xxx 等模式 → E^{\\circ}_{\\text{cell}}
    text = re.sub(r'(?<!\$)(E|K|Δ_r[GHS])°_(\w+)', r'$\\1^{\\circ}_{\\text{\\2}}$', text)
    # ◦（白色圆圈度数符号）→ ^\\circ
    text = re.sub(r'(?<!\$)(?<![a-zA-Z])◦', r'$^{\\circ}$', text)
    # E◦_cell → E^{\\circ}_{\\text{cell}} 等模式
    text = re.sub(r'(?<!\$)(E|K|Δ_r[GHS])◦_(\w+)', r'$\\1^{\\circ}_{\\text{\\2}}$', text)
    # Unicode 符号 → LaTeX 宏命令（仅影响非 math 区域，math 已被保护）
    _sym_map = {'→':'\\箭', '←':'\\左箭', '↑':'\\上箭', '↓':'\\下箭',
                '⇌':'\\衡', '↔':'\\双箭', '≈':'\\约等于',
                '≤':'\\小于等于', '≥':'\\大于等于', '≠':'\\不等于',
                'σ':'\\西格马', 'π':'\\派'}
    for sym, cmd in _sym_map.items():
        text = text.replace(sym, cmd)
    # 数字上下标：转 Pandoc ^...^ / ~...~ 语法（仅影响非 math 区域）
    text = re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+',
        lambda m: '^' + ''.join(SUP_MAP.get(c, c) for c in m.group(0)) + '^', text)
    text = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]+',
        lambda m: '~' + ''.join(SUB_MAP.get(c, c) for c in m.group(0)) + '~', text)
    # 注意：math 恢复延后到 e_g 转换之后，避免嵌套 $...$

    # 图片引用
    text = re.sub(r'!\[\[media/([^\]|]+)\|[^\]]*\]\]', r'![](media/\1)', text)
    text = re.sub(r'!\[\[media/([^\]|]+)\]\]', r'![](media/\1)', text)
    text = re.sub(r'\.(lewis\.)?md\)', r'.\1png)', text)

    # wikilink → 纯文本
    # 先处理"教学洞察" wikilink → 只保留主题名
    text = re.sub(r'\[\[12-教学洞察/教学洞察-([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'\[\[教学洞察-([^\]]+)\]\]', r'\1', text)
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

    # 目录精简：四级标题降为粗体（不进目录，但保留可见）
    lines = text.split('\n')
    result = []
    for line in lines:
        s = line.strip()
        if s.startswith('#### '):
            heading_text = s[5:].strip()
            line = f'**{heading_text}**'
        result.append(line)
    text = '\n'.join(result)

    # 目录精简：例题和练习题/答案区下的三级标题降级为纯文本（不进目录）
    lines = text.split('\n')
    in_example_section = False
    in_practice_section = False
    result = []
    for line in lines:
        s = line.strip()
        # 匹配任何包含"例题"或"典型例题"的二级标题
        if s.startswith('## ') and ('例题' in s or '典型例题' in s):
            in_example_section = True
        # 匹配任何包含"练习"或"答案"的二级标题
        elif s.startswith('## ') and ('练习' in s or '答案' in s or '参考答案' in s):
            in_practice_section = True
        elif s.startswith('## ') and not s.startswith('### '):
            if in_example_section:
                in_example_section = False
            if in_practice_section:
                in_practice_section = False
        if (in_example_section or in_practice_section) and s.startswith('### '):
            # 将三级标题完全隐藏（不进目录，不显示）
            line = ''
        result.append(line)
    text = '\n'.join(result)

    # ── emoji 替换（删掉 ⭐★，保留教学标记）──
    emoji_map = {'🧠': '[认知冲突]', '⚠️': '[易错点]', '💡': '[理解提示]',
                 '📌': '[要点]', '🗣️': '[教师原话]', '🧪': '[实验]',
                 '✏️': '[练习]', '☐': '[ ]', '✅': '[完成]',
                 '🔑': '[关键]', '⭐': '', '★': ''}
    for emo, rep in emoji_map.items():
        text = text.replace(emo, rep)

    # caption 等处的 Unicode 希腊字母（θ φ α β γ 等）不含 $ 时补齐 math
    def fix_caption_greek(m):
        txt = m.group(1)
        greek = {'α': r'$\alpha$', 'β': r'$\beta$', 'γ': r'$\gamma$',
                 'δ': r'$\delta$', 'θ': r'$\theta$', 'φ': r'$\varphi$',
                 'λ': r'$\lambda$'}
        for c, r in greek.items():
            txt = txt.replace(c, r)
        return '*' + txt + '*'
    text = re.sub(r'\*([^*\n]*(?:θ|φ|α|β|γ|δ|λ|σ)[^*\n]*)\*', fix_caption_greek, text)

    # 图注中的 Z* 等星号：*图 ...* 中的 * 会导致 Pandoc 错误解析为斜体边界
    def _escape_caption_stars(m):
        prefix, body, suffix = m.group(1), m.group(2), m.group(3)
        escaped = body.replace('*', '\\*')
        return prefix + escaped + suffix
    text = re.sub(r'(\*图\s+)(.*?)(\*\s*)$', _escape_caption_stars, text, flags=re.MULTILINE)

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

    # 图片 caption 中 Unicode 希腊字母 → math（只在 *图 xxx* caption 中替换）
    def fix_caption_greek(m):
        txt = m.group(1) or m.group(2) or ''
        greek_map = {'α': r'$\alpha$', 'β': r'$\beta$', 'γ': r'$\gamma$',
                     'δ': r'$\delta$', 'θ': r'$\theta$', 'φ': r'$\varphi$',
                     'λ': r'$\lambda$', 'σ': r'$\sigma$'}
        for c, r in greek_map.items():
            txt = txt.replace(c, r)
        return '*' + txt + '*'
    text = re.sub(r'\*([^*\n]*(?:θ|φ|α|β|γ|δ|λ|σ)[^*\n]*)\*', fix_caption_greek, text)

    # 正文中的 e_g / t_2g / t₂g 下划线格式 → 下标（math 已提取，不会嵌套）
    text = re.sub(r'(?<!\w)e_g(?!\w)', r'$e_g$', text)
    text = re.sub(r'(?<!\w)t_2g(?!\w)', r'$t_{2g}$', text)
    text = re.sub(r'(?<!\w)t₂g(?!\w)', r'$t_{2g}$', text)

    # 恢复数学表达式（在 e_g 转换之后，避免嵌套 $...$）
    for i, block in enumerate(_math_blocks):
        text = text.replace(f'__MATH_BLOCK_{i}__', block)

    # ── 3. 后处理：非 math 区域残留的 Unicode 上下标 → 包裹 $...$ ──
    def _wrap_unicode_subs(m):
        """将残留的 Unicode 上下标序列包裹在 $...$ 中"""
        seq = m.group(0)
        # 跳过已经在 $...$ 内的（简单判断：前面 $ 出现奇数次说明在 math 内）
        pre = text[:m.start()]
        if pre.count('$') % 2 == 1:
            return seq
        parts = []
        for c in seq:
            if c in SUP_MAP:
                parts.append(SUP_MAP[c])
            elif c in SUB_MAP:
                parts.append(SUB_MAP[c])
            else:
                parts.append(c)
        converted = ''.join(parts)
        if any(c in SUP_MAP for c in seq):
            return f'$^{{{converted}}}$'
        else:
            return f'$_{{{converted}}}$'
    text = re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]{2,}', _wrap_unicode_subs, text)
    text = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]{2,}', _wrap_unicode_subs, text)
    # 单个 ° 跟在字母后面（非 math 区域）→ ^\circ
    text = re.sub(r'([A-Za-z])°(?!\s*[$\\{])', r'$\\1^{\\circ}$', text)

    # 恢复代码块
    for i, block in enumerate(_code_blocks):
        text = text.replace(f'__CODE_BLOCK_{i}__', block)

    # H1 标题去掉"超级充实版（自学完整）"等后缀（避免进页眉）
    text = re.sub(r'^(# .+?)\s*[·\-—]\s*超级充实版.*$', r'\1', text, flags=re.MULTILINE)

    return text


def convert_one(md_target, parallel=False):
    """转换一本讲义为 PDF"""
    md_name, md_path = resolve_md_target(md_target)
    if not os.path.exists(md_path):
        return (md_target, False, f'文件不存在: {md_path}')

    cn_map = get_aliases()
    build_key = hashlib.sha1(os.path.normcase(md_path).encode('utf-8')).hexdigest()[:12]
    label = f'[{md_name}]'
    miktex_env = build_miktex_env()
    sync_warnings = []
    if not parallel:
        print(f'\n{"="*50}\n  {md_path}')

    # ── 0. 同步图片：vault 根目录 media/ → workspace-local cache ──
    vault_media = VAULT_MEDIA
    if os.path.exists(vault_media):
        os.makedirs(_CHEM_MEDIA_WIN, exist_ok=True)
        for f in os.listdir(vault_media):
            src = os.path.join(vault_media, f)
            if os.path.isfile(src):
                dst = os.path.join(_CHEM_MEDIA_WIN, f)
                copy_media_file(src, dst, sync_warnings)
        # 同步别名文件：复制中文名→英文名，供别名映射使用
        for cn, ascii_n in cn_map.items():
            src = os.path.join(vault_media, cn)
            if os.path.exists(src):
                dst = os.path.join(_CHEM_MEDIA_WIN, ascii_n)
                copy_media_file(src, dst, sync_warnings)
        # SVG → PNG 转换（xelatex/dvipdfmx 不支持 SVG）
        import struct
        for fn in os.listdir(_CHEM_MEDIA_WIN):
            if fn.lower().endswith('.svg'):
                png_fn = os.path.splitext(fn)[0] + '.png'
                png_path = os.path.join(_CHEM_MEDIA_WIN, png_fn)
                svg_path = os.path.join(_CHEM_MEDIA_WIN, fn)
                if not os.path.exists(png_path):
                    try:
                        import cairosvg
                        cairosvg.svg2png(url=svg_path, write_to=png_path)
                    except Exception:
                        pass  # svg 转 png 失败，留待后续处理
            # 修复合法的 JPG/PNG 被 SVG 内容覆盖（别名同步导致）
            # 检查前 4 字节签名：JPG=FFD8, PNG=89504E47, SVG=3C737667
            if fn.lower().endswith(('.jpg', '.jpeg', '.png')):
                fp = os.path.join(_CHEM_MEDIA_WIN, fn)
                try:
                    with open(fp, 'rb') as f:
                        hdr = f.read(4)
                        is_jpg = hdr[:2] == b'\xff\xd8'
                        is_png = hdr[:4] == b'\x89PNG'
                        is_svg = hdr[:4] == b'<svg'
                    if (fn.lower().endswith(('.jpg', '.jpeg')) and not is_jpg and is_svg):
                        os.remove(fp)
                        print(f'  ⚠️ 移除伪JPG（实为SVG）: {fn}')
                    elif fn.lower().endswith('.png') and not is_png and is_svg:
                        os.remove(fp)
                        print(f'  ⚠️ 移除伪PNG（实为SVG）: {fn}')
                except Exception:
                    pass

    # ── 1. 预处理（使用独立临时文件避免并行竞态）──
    try:
        with open(md_path, encoding='utf-8') as f:
            processed = preprint(f.read())
    except Exception as e:
        return (md_target, False, f'预处理失败: {e}')
    pre_path = os.path.join(SCRIPTS, f'_pre_{build_key}.md')
    with open(pre_path, 'w', encoding='utf-8') as f:
        f.write(processed)

    title = md_name.replace('.md','').split('-超级充实版')[0] if '超级充实版' in md_name else md_name.replace('.md','')

    # ── 2. Pandoc → LaTeX body（独立文件名）──
    body_path = os.path.join(SCRIPTS, f'_body_{build_key}.tex')
    try:
        r1 = subprocess.run([
            PANDOC, pre_path, '-o', body_path,
            '--from=markdown+tex_math_dollars+raw_tex+pipe_tables+grid_tables+superscript+subscript-yaml_metadata_block',
            '--to=latex', '--lua-filter=' + LUA_FILTER, '--wrap=preserve',
        ], env=base_env, capture_output=True, timeout=60)
        decode_subprocess_output(r1)
        if r1.returncode != 0 or not os.path.exists(body_path):
            err = (r1.stderr or '')[:500]
            return (md_target, False, f'Pandoc 失败: {err}')
    except subprocess.TimeoutExpired:
        return (md_target, False, 'Pandoc 超时(60s)')

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
        + '\\thispagestyle{plain}\n'
        + '\\begin{center}\n'
        + '{\\zihao{2}\\bfseries ' + latex_escape_text(title) + '\\par}\n'
        + '\\end{center}\n'
        + '\\vspace{1em}\n'
        + body
        + '\n\\end{document}\n'
    )

    # 后处理：pandoc 产物清理
    full_tex = full_tex.replace('\\pandocbounded{', '')
    # 修复 \pandocbounded{...} 剥离后遗留的 }} → }
    full_tex = re.sub(r'(\\includegraphics(?:\[[^\]]*\])?\{[^}]+\})\}', r'\1', full_tex)
    full_tex = full_tex.replace('{media/', '{')

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

        # 尝试别名查找：双向映射
        # 方向1：MD用英文名，实际文件是中文名 (ascii_n → cn)
        # 方向2：MD用中文名，实际文件用英文名 (cn → ascii_n)
        real_fn = fn
        for cn, ascii_n in cn_map.items():
            if ascii_n == fn:
                real_fn = cn
                break
            if cn == fn:
                real_fn = ascii_n
                # 更新 LaTeX 中的引用为英文名
                full_cmd = full_cmd.replace('{' + fn + '}', '{' + ascii_n + '}')
                fn = ascii_n
                break

        fp = os.path.join(_CHEM_MEDIA_WIN, real_fn)

        if not os.path.exists(fp):
            source_candidates = []
            if os.path.exists(vault_media):
                source_candidates.append(os.path.join(vault_media, real_fn))
                if real_fn != fn:
                    source_candidates.append(os.path.join(vault_media, fn))

            for source_fp in source_candidates:
                if not os.path.exists(source_fp):
                    continue
                try:
                    if not copy_media_file(source_fp, fp, sync_warnings):
                        continue
                except Exception:
                    continue
                if os.path.exists(fp):
                    return full_cmd

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
    tex_path = os.path.join(SCRIPTS, f'_handout_{build_key}.tex')
    pdf_temp = os.path.join(SCRIPTS, f'_handout_{build_key}.pdf')
    pdf_backup = os.path.join(SCRIPTS, f'_handout_{build_key}_p1.pdf')
    stale_outputs = [
        pdf_temp,
        pdf_backup,
        tex_path.replace('.tex', '.aux'),
        tex_path.replace('.tex', '.log'),
        tex_path.replace('.tex', '.out'),
        tex_path.replace('.tex', '.toc'),
    ]

    for stale_path in stale_outputs:
        if os.path.exists(stale_path):
            try:
                os.remove(stale_path)
            except Exception:
                pass

    # 统一行尾为 LF（Pandoc on Windows 生成 CRLF，会导致 \newunicodechar 报错）
    full_tex = full_tex.replace('\r\n', '\n')

    with open(tex_path, 'w', encoding='utf-8', newline='') as f:
        f.write(full_tex)

    try:
        ensure_miktex_sandbox()
    except RuntimeError as exc:
        return (md_target, False, str(exc))

    log_errors = []
    for i in range(2):
        try:
            r2 = subprocess.run([
                XELATEX, *MIKTEX_FLAGS, '-interaction=nonstopmode',
                '-output-directory=' + SCRIPTS, tex_path
            ], capture_output=True, env=miktex_env, timeout=600)
            decode_subprocess_output(r2)
        except subprocess.TimeoutExpired:
            if i > 0 and os.path.exists(pdf_backup) and os.path.getsize(pdf_backup) > 20000:
                backup_ok, _ = validate_pdf_file(pdf_backup)
                if backup_ok:
                    shutil.copy2(pdf_backup, pdf_temp)
                    log_errors.append('xelatex 第二遍超时，已回退到首遍有效 PDF')
                    break
            return (md_target, False, 'xelatex 超时(600s)')

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
        return (md_target, False, f'PDF 生成失败\n{diag[:600]}')

    with open(pdf_temp, 'rb') as f:
        c = f.read()
    if c[:5] != b'%PDF-' or len(c) < 5000:
        return (md_target, False, 'PDF 文件损坏或为空')
    # 自动修复缺失的 %%EOF 标记
    if c.rfind(b'%%EOF') < 0:
        with open(pdf_temp, 'ab') as f:
            f.write(b'\n%%EOF\n')

    pdf_ok, pdf_diag = validate_pdf_file(pdf_temp)
    if not pdf_ok and os.path.exists(pdf_backup) and os.path.getsize(pdf_backup) > 20000:
        backup_ok, backup_diag = validate_pdf_file(pdf_backup)
        if backup_ok:
            shutil.copy2(pdf_backup, pdf_temp)
            pdf_ok, pdf_diag = True, ''
        else:
            pdf_diag = f'{pdf_diag}; backup={backup_diag}'

    if not pdf_ok:
        diag = '\n'.join(log_errors[-15:]) if log_errors else ''
        detail = pdf_diag if not diag else f'{pdf_diag}\n{diag}'
        return (md_target, False, f'PDF 文件结构校验失败\n{detail[:600]}')

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
    os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(PDF_OUTPUT_DIR, out_name)
    try:
        if os.path.exists(out_path):
            os.remove(out_path)
        shutil.copy2(pdf_temp, out_path)
    except PermissionError:
        alt_path = os.path.join(PDF_OUTPUT_DIR, '_new_' + out_name)
        shutil.copy2(pdf_temp, alt_path)
        out_path = alt_path

    miss_str = f', 缺图={len(missing_imgs)} [WARN]' if missing_imgs else ', 全图 OK'
    msg = f'{size_kb}KB, {pages}p, {img_count}张图{miss_str}'
    if sync_warnings and not parallel:
        sample = '; '.join(sync_warnings[:3])
        extra = '' if len(sync_warnings) <= 3 else f' ... 共{len(sync_warnings)}条'
        print(f'  ⚠️ media 缓存同步告警: {sample}{extra}')
    if not parallel:
        print(f'  PDF → {out_path}  ({msg})')
    return (md_target, True, msg)


if __name__ == '__main__':
    is_parallel = any(a.upper() in ('--PARALLEL', '-P') for a in sys.argv)
    args = [a for a in sys.argv[1:] if not a.upper() in ('--PARALLEL', '-P')]

    if args and args[0].upper() == 'ALL':
        targets = ['原子结构-超级充实版（自学完整）.md',
                   '元素周期表与周期律-超级充实版（自学完整）.md',
                   '分子结构基础-超级充实版（自学完整）.md',
                   '配位化合物基础-超级充实版（自学完整）.md',
                   '晶体学与晶体结构-超级充实版（自学完整）.md',
                   '热力学初步-超级充实版（自学完整）.md',
                   '化学平衡-超级充实版（自学完整）.md',
                   '电化学基础-超级充实版（自学完整）.md',
                   '酸碱理论-超级充实版（自学完整）.md',
                   '溶液与相图-超级充实版（自学完整）.md']
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
                print(f'  {"OK" if ok else "FAIL"} {name}' + (f'\n    → {msg}' if not ok else ''))
        print(f'\n结果汇总：')
        ok_count = sum(1 for t in targets if t in results and results[t][0])
        print(f'  {ok_count}/{len(targets)} 成功')
        for t in targets:
            if t in results:
                ok, msg = results[t]
                print(f'  {"OK" if ok else "FAIL"} {msg}')
    else:
        had_err = False
        for t in targets:
            name, ok, msg = convert_one(t)
            if not ok:
                had_err = True
                print(f'\n  ❌ {name}\n  → {msg}')
        print(f'\n{"="*50}\n{"全部成功 OK" if not had_err else "部分失败 FAIL"}')
