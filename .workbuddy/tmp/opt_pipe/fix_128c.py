# -*- coding: utf-8 -*-
r"""修 Cannizzaro 卡的 `$$...\\qquad...$$`（texmath 放弃）→ 拆成两个 $$ 块。"""
import io, os, shutil, datetime
os.chdir(r'C:\Obsidion\妙妙屋')
P = '04-题库/教材习题/ABOC/题-128-ABOC-Ch4-4.13.1-Cannizzaro 康尼查罗 反应是醛在强碱浓溶液中发生的.md'
BAK = '.workbuddy/tmp/opt_pipe/_bak/bs3_%s' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(BAK, exist_ok=True)
shutil.copy2(P, os.path.join(BAK, os.path.basename(P)))

B = chr(92)
t = io.open(P, encoding='utf-8-sig').read()
old = ("$$" + "\n"
       "[\\mathrm{T_1}] = K_1[\\mathrm{PhCHO}][\\mathrm{OH^-}]," + B + B + "qquad\n"
       "[\\mathrm{T_2}] = K_2[\\mathrm{PhCHO}][\\mathrm{OH^-}]^2\n"
       "$$")
new = ("$$\n"
       "[\\mathrm{T_1}] = K_1[\\mathrm{PhCHO}][\\mathrm{OH^-}]\n"
       "$$\n\n"
       "$$\n"
       "[\\mathrm{T_2}] = K_2[\\mathrm{PhCHO}][\\mathrm{OH^-}]^2\n"
       "$$")
assert old in t, '未匹配到目标块'
t2 = t.replace(old, new)
assert B + B not in t2.replace(B + B + ' ', ''), '仍有非空白的双反斜杠'
io.open(P, 'w', encoding='utf-8', newline='').write(t2)
print('已写盘 %d → %d 字节；备份 %s' % (len(t), len(t2), BAK))
