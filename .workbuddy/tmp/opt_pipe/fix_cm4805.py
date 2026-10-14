# -*- coding: utf-8 -*-
r"""CM-48-05：按源扫描 PDF（p12/p13 目读）逐条重录。每条断言命中=1，否则整卡不写盘。"""
import io, os, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
B = chr(92); D = B + 'Delta'
p = '04-题库/真题/chemy/题-CM-48-05-向含有少量酚酞指示剂的水溶液.md'
bak = '.workbuddy/tmp/opt_pipe/_bak/cm4805_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
shutil.copy2(p, os.path.join(bak, os.path.basename(p)))
t = io.open(p, encoding='utf-8-sig').read()

def M(s):
    return (s.replace('@', B))

FIXES = [
 # ── 题面 ──
 (M('亚硫酸氢钠 - $\\mathrm{NaHSO_3^-}$ )'),
  M('亚硫酸氢钠（$\\mathrm{NaHSO_3}$）'), '题面：NaHSO₃ 非 NaHSO₃⁻'),
 (M('亚硫酸氢根 (HSOj)'),
  M('亚硫酸氢根 ($\\mathrm{HSO_3^-}$)'), '题面：(HSOj)→(HSO₃⁻)'),
 (M('亚硫酸根平衡浓度[SO门与亚硫酸氢根平衡浓度[HSO]。'),
  M('亚硫酸根平衡浓度[$\\mathrm{SO_3^{2-}}$]与亚硫酸氢根平衡浓度[$\\mathrm{HSO_3^-}$]。'), '题面：方括号内符号'),
 (M('计算 $K_2(\\mathrm{HSO_3^-})$ e'),
  M('计算 $K_2(\\mathrm{HSO_3^-})$。'), '题面：尾随 e→。'),
 # ── 答案 5-1 ──
 (M('该一价负离子为： HOCH₂SO3'),
  M('该一价负离子为：$\\mathrm{HOCH_2SO_3^-}$'), '5-1：HOCH₂SO₃⁻ 上标负号'),
 (M('甲醛与亚硫酸氢根的反应方程式为：HCHO $^ +$ HSO; → HOCH₂SOj (1分）'),
  M('甲醛与亚硫酸氢根的反应方程式为：$\\mathrm{HCHO}+\\mathrm{HSO_3^-}\\rightarrow\\mathrm{HOCH_2SO_3^-}$（1分）'), '5-1 第一式'),
 (M('\\mathrm{H_2O}+\\mathrm{^-OCH_2SO_3^-}+\\mathrm{HSO_3^-}\\rightarrow\\mathrm{HOCH_2SO_3^-}+\\mathrm{HO^-}$ (1分）'),
  M('\\mathrm{H_2O}+\\mathrm{^-OCH_2SO_3^-}\\rightarrow\\mathrm{HOCH_2SO_3^-}+\\mathrm{HO^-}$（1分）'), '5-1 第二式：删多余 +HSO₃⁻'),
 # ── 答案 5-2-1 ──
 (M('物料守恒： $| 11 _{ 1 } \\mathrm { SO } _{ 3 } | + | 11 \\mathrm { SO } _{ 3 } | + | \\mathrm { SO } _{ 3 } ^{ 1 - } | = \\mathrm { c } ( \\mathrm { Nall } \\mathrm { SO } _{ 3 } ) + \\mathrm { c } ( \\mathrm { Na } _{ 2 } \\mathrm { SO } _{ 3 } )$ (1分）'),
  M('物料守恒：$\\mathrm{[H_2SO_3]+[HSO_3^-]+[SO_3^{2-}]=c(NaHSO_3)+c(Na_2SO_3)}$（1分）'), '5-2-1 物料守恒'),
 (M('电荷守恒： ""\\* $\\mathrm { | + | Na ^{ * } | = | OII ^{ - } | + | IISO _{ 3^{ - } } | + 2 \\times | SO _{ 3^{ 2 } } | }$ (1分）'),
  M('电荷守恒：$\\mathrm{[H^+]+[Na^+]=[OH^-]+[HSO_3^-]+2\\times[SO_3^{2-}]}$（1分）'), '5-2-1 电荷守恒'),
 (M('注1： 将其中 [ $\\mathrm { { c ( NallsO , ) + c ( Na , SO , ) } }$ 表示为数值 1.0×10-²³mol·dm\\~³或1.01×10-³mol·dm\\~, 也可得分；'),
  M('注1：将其中 $c(\\mathrm{NaHSO_3})+c(\\mathrm{Na_2SO_3})$ 表示为数值 $1.0\\times10^{-3}\\ \\mathrm{mol\\cdot dm^{-3}}$ 或 $1.01\\times10^{-3}\\ \\mathrm{mol\\cdot dm^{-3}}$，也可得分；'), '注1'),
 (M('$[\\mathrm{HSO_3^-}]\\gg[\\mathrm{SO_3^{2-}}]$, 所以： $| 11 \\mathrm { S } \\mathbf { 0 } _{ 3 } \\mathbf { \\bar { \\Gamma } } | + | \\mathrm { S } \\mathbf { 0 } _{ 3 } \\mathbf { \\bar { \\Gamma } } ^{ 2 } | = \\mathrm { c } ( \\mathrm { Nall } \\mathrm { S } \\mathbf { 0 } _{ 3 } ) + \\mathrm { c } ( \\mathrm { Na } _{ 2 } \\mathrm { S } \\mathbf { 0 } _{ 3 } )$ [H+]>>[OH], 所以： $| \\mathrm { II } ^{ * } | + | \\mathrm { Na } ^{ * } | = | \\mathrm { IISO } _{ 3 } ^{ - } | + 2 \\times | \\mathrm { SO } _{ 3 } ^{ 2 - } | \\mathrm { : }$ ['),
  M('$[\\mathrm{HSO_3^-}]\\gg[\\mathrm{SO_3^{2-}}]$，所以：$\\mathrm{[HSO_3^-]+[SO_3^{2-}]=c(NaHSO_3)+c(Na_2SO_3)}$；$[\\mathrm{H^+}]\\gg[\\mathrm{OH^-}]$，所以：$\\mathrm{[H^+]+[Na^+]=[HSO_3^-]+2\\times[SO_3^{2-}]}$'), '注2 两式'),
 # ── 答案 5-2-2 / 5-2-3 ──
 (M('$| \\mathrm { { SO } , ^{ 2 - } } | = 1.4 \\times 10^{ - 5 } \\mathrm { { mol } \\cdot d \\mathrm { { m } ^{ - 3 } } }$ (1分)$[\\mathrm{SO_3^{2-}}]=1.0\\times10^{-3} ~ \\mathrm { mol \\cdot dm ^{ - 3 } }$ (1分）'),
  M('$[\\mathrm{SO_3^{2-}}]=1.4\\times10^{-5}\\ \\mathrm{mol\\cdot dm^{-3}}$（1分）$[\\mathrm{HSO_3^-}]=1.0\\times10^{-3}\\ \\mathrm{mol\\cdot dm^{-3}}$（1分）'), '5-2-2 两式'),
 (M('$1.3\\times10^{-5}$ 1算成 $1.3 \\times 10^{ - 5 }$ 或 $1.5\\times10^{-5}$ mol·dm-³, 也可得分， 但有效数字必须是两位'),
  M('注：$[\\mathrm{SO_3^{2-}}]$算成 $1.3\\times10^{-5}$ 或 $1.5\\times10^{-5}\\ \\mathrm{mol\\cdot dm^{-3}}$，也可得分，但有效数字必须是两位'), '5-2-2 注'),
 # ── 答案 5-3-1 / 5-3-3 ──
 (M('甲醛消耗总速率： $\\nu ( \\mathrm { HCH } 0 ) = k ( \\mathrm { SO _{ 3 } } ^{ 2 - } ) \\mathrm { c } ( \\mathrm { Na _{ 2 } SO _{ 3 } } ) [ \\mathrm { HCH } ($ OI$\\mathrm { ' + D + ' 3 = } k ( \\mathrm { SO _{ 3 } ^{ 2 - } ) e ( Na _{ 2 } SO _{ 3 } ) }$ (1分）'),
  M('甲醛消耗总速率：$\\nu(\\mathrm{HCHO})=k(\\mathrm{SO_3^{2-}})\\mathrm{c}(\\mathrm{Na_2SO_3})[\\mathrm{HCHO}]$\n\n$a=k(\\mathrm{SO_3^{2-}})\\mathrm{c}(\\mathrm{Na_2SO_3})$（1分）'), '5-3-1 速率式＋a 式'),
 (M('注2： 数值运算结果0.54算成0.53或0.55， 也可得分， 但有效数字必须是两位注3： 答案写上负号， 表示消耗， 也可得分；'),
  M('注2：数值运算结果 0.54 算成 0.53 或 0.55，也可得分，但有效数字必须是两位\n\n注3：答案写上负号，表示消耗，也可得分；'), '5-3-1 注2/注3 断行'),
 (M('(HCHO] $[\\mathrm{HCHO}]=1.2\\times10^{-4}$ mol·dm-³ (2分）'),
  M('$[\\mathrm{HCHO}]=1.2\\times10^{-4}\\ \\mathrm{mol\\cdot dm^{-3}}$（2分）'), '5-3-3：删游离 (HCHO]'),
]

n_ok = 0
for old, new, why in FIXES:
    c = t.count(old)
    if c != 1:
        print('❌ 命中 %d 次，跳过：%s' % (c, why))
        continue
    t = t.replace(old, new)
    n_ok += 1
    print('✅ %s' % why)
print()
print('成功 %d / %d' % (n_ok, len(FIXES)))
if n_ok != len(FIXES):
    print('⚠️ 有未命中项 ⇒ 不写盘')
    raise SystemExit(1)
# 收尾：统一 mol·dm-³ → mol·dm⁻³；更新校勘注
t = t.replace('mol·dm-³', 'mol·dm⁻³')
t = t.replace('mol·dm\\~³', 'mol·dm⁻³')
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('✅ 已写盘 %d 字节；备份 %s' % (len(t), bak))
