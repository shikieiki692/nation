# -*- coding: utf-8 -*-
r"""CM-55-05：按 32 届答案 PDF 原文重写 5-1 方程式（源验证）。"""
import io, os, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
B = chr(92); D = B + 'Delta'
p = '04-题库/2026机构初赛模拟题/chemy/题-CM-55-05-1961年Vaska报导了一.md'
bak = '.workbuddy/tmp/opt_pipe/_bak/cm5505_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(bak, exist_ok=True)
shutil.copy2(p, os.path.join(bak, os.path.basename(p)))

t = io.open(p, encoding='utf-8-sig').read()
old = ('$' + B + 'mathrm { IrCl _{ 3 } ( H _{ 2 } O ) _{ 3 } + 3 PPh _{ 3 } + HCON ( CH _{ 3 } ) _{ 2 } '
       '+ PhNH _{ 2 }  ' + D + ' _{ TC } l ( CO ) ( PPh _{ 3 } ) _{ 2 } + [ ( CH _{ 3 } ) _{ 2 } NH _{ 2 } ] Cl '
       '+ ( CO ) _{ 2 } ' + D + ' _{ TC } l }$' + '\n' + '$-$')
new = ('$' + B + 'mathrm{IrCl_3(H_2O)_3 + 3PPh_3 + HCON(CH_3)_2 + PhNH_2 ' + B + 'rightarrow '
       'IrCl(CO)(PPh_3)_2 + [(CH_3)_2NH_2]Cl + POPh_3 + PhNH_3Cl + 2H_2O}$')
print('命中次数:', t.count(old))
assert t.count(old) == 1, '未按预期命中，未写盘'
t2 = t.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='').write(t2)
print('✅ 已修 %d → %d 字节' % (len(t), len(t2)))
i = t2.find('5-1 $')
print('复验:', t2[i:i + 220].replace('\n', '⏎'))
print('残留 Delta_{TC}:', t2.count(D + ' _{ TC }'))
