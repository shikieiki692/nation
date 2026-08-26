# -*- coding: utf-8 -*-
"""P16 高中氧气行方程式替换 + P25 必做标记。实体编码全部由程序计算，不手抄码点。"""
import pathlib
import re

SLIDES = pathlib.Path(__file__).parent / 'ppt' / 'slides'

def enc(s):
    """非 ASCII 转十进制实体，与该 unpack 目录的序列化风格一致。"""
    return ''.join(f'&#{ord(c)};' if ord(c) > 127 else c for c in s)

RPR_N = ('<a:rPr lang="en-US" sz="1200" noProof="1">'
         '<a:solidFill><a:srgbClr val="6B7280"/></a:solidFill>'
         '<a:latin typeface="Liter"/><a:ea typeface="Noto Sans SC"/></a:rPr>')
RPR_S = RPR_N.replace('noProof="1">', 'noProof="1" baseline="-25000">')

def run(rpr, text, preserve=False):
    sp = ' xml:space="preserve"' if preserve else ''
    return (f'            <a:r>\n              {rpr}\n'
            f'              <a:t{sp}>{enc(text)}</a:t>\n            </a:r>')

# ========== 修改一：slide16 ==========
p16 = SLIDES / 'slide16.xml'
xml = p16.read_text(encoding='utf-8')

m = re.search(r'<a:p>\s*<a:pPr>\s*<a:lnSpc>\s*<a:spcPct val="120000"/>\s*</a:lnSpc>\s*<a:spcBef>\s*<a:spcPts val="300"/>\s*</a:spcBef>\s*</a:pPr>(?:(?!</a:p>).)*?<a:t>C \+ O</a:t>(?:(?!</a:p>).)*?</a:p>', xml, re.S)
assert m, 'P16 target paragraph not found'
old_p = m.group(0)
assert enc('——为什么能助燃？') in old_p, 'P16 paragraph content mismatch'

runs = [
    (RPR_N, '2H', False),
    (RPR_S, '2', False),          # H₂
    (RPR_N, 'O', False),
    (RPR_S, '2', False),          # O₂（H₂O₂ 第二个）
    (RPR_N, ' ═ 2H', True),
    (RPR_S, '2', False),          # H₂O
    (RPR_N, 'O + O', False),
    (RPR_S, '2', False),          # O₂
    (RPR_N, '↑——MnO', False),
    (RPR_S, '2', False),          # MnO₂
    (RPR_N, ' 为什么能加快？', True),
]
new_p = ('<a:p>\n            <a:pPr>\n              <a:lnSpc>\n'
         '                <a:spcPct val="120000"/>\n              </a:lnSpc>\n'
         '              <a:spcBef>\n                <a:spcPts val="300"/>\n'
         '              </a:spcBef>\n            </a:pPr>\n'
         + '\n'.join(run(*r) for r in runs)
         + '\n            <a:endParaRPr lang="en-US" sz="1600" noProof="1"/>\n          </a:p>')

xml = xml.replace(old_p, new_p, 1)
p16.write_text(xml, encoding='utf-8')
print('slide16 patched')

# ========== 修改二：slide25 ==========
p25 = SLIDES / 'slide25.xml'
xml = p25.read_text(encoding='utf-8')

old1 = f'<a:t>{enc("三个小任务，任选一个完成：")}</a:t>'
new1 = f'<a:t>{enc("一个必做，一个选做（二选一）：")}</a:t>'
assert xml.count(old1) == 1, 'P25 lead text not found'
xml = xml.replace(old1, new1, 1)

old2 = f'<a:t>{enc("准备两个本子")}</a:t>'
new2 = f'<a:t>{enc("【必做】准备两个本子")}</a:t>'
assert xml.count(old2) == 1, 'P25 task A title not found'
xml = xml.replace(old2, new2, 1)

p25.write_text(xml, encoding='utf-8')
print('slide25 patched')
