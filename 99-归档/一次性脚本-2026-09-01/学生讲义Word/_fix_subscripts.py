"""Convert Unicode subscripts/superscripts and raw LaTeX subscripts to proper math in markdown files."""
import re, sys, os

sup_map = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4',
           '⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9',
           '⁺':'+','⁻':'-'}
sub_map = {'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4',
           '₅':'5','₆':'6','₇':'7','₈':'8','₉':'9'}

def convert_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()

    # Protect existing math blocks ($...$ and $$...$$)
    math_blocks = []
    def save_math(m):
        math_blocks.append(m.group(0))
        return f'__MATH_{len(math_blocks)-1}__'
    text = re.sub(r'\$\$[\s\S]*?\$\$', save_math, text)
    text = re.sub(r'(?<!\$)\$(?!\$)(?:[^$\\]|\\.)+\$(?!\$)', save_math, text)

    # 1. Convert raw LaTeX subscripts outside math: σ_{2p} → $σ_{2p}$
    # Greek_letter*}_{subscript} → $Greek^*_{subscript}$
    text = re.sub(
        r'(?<!\$)([σπδλθφψωΔ])\*\}_\{([^}]+)\}(?!\$)',
        r'$\1^*_{\2}$', text)
    # Greek_letter_{subscript} → $Greek_{subscript}$
    text = re.sub(
        r'(?<!\$)([σπδλθφψωΔ])_\{([^}]+)\}(?!\$)',
        r'$\1_{\2}$', text)
    # letter_{subscript} → $letter_{subscript}$ (e_g, t_2g, etc.)
    text = re.sub(
        r'(?<!\$)([a-zA-Z])_\{([^}]+)\}(?!\$)',
        r'$\1_{\2}$', text)

    # 2. Convert Unicode subscripts/superscripts to LaTeX math
    def convert_unicode_subs(m):
        letter = m.group(1)
        seq = m.group(2)
        converted = ''
        for ch in seq:
            if ch in sub_map:
                converted += sub_map[ch]
            elif ch in sup_map:
                converted += sup_map[ch]
            else:
                converted += ch
        has_sub = any(ch in sub_map for ch in seq)
        has_sup = any(ch in sup_map for ch in seq)
        if has_sub and has_sup:
            return f'${letter}_{{{converted}}}$'
        elif has_sub:
            return f'${letter}_{{{converted}}}$'
        else:
            return f'${letter}^{{{converted}}}$'

    text = re.sub(
        r'(?<!\$)([A-Za-zα-ωΔ])([₀-₉⁰¹²³⁴-⁹⁺⁻]+)(?!\$)',
        convert_unicode_subs, text)

    # Restore math blocks
    for i, block in enumerate(math_blocks):
        text = text.replace(f'__MATH_{i}__', block)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

    remaining = len(re.findall(r'[₀-₉]', text))
    print(f'Converted {os.path.basename(path)}. Remaining unicode subscripts: {remaining}')

if __name__ == '__main__':
    for p in sys.argv[1:]:
        convert_file(p)
