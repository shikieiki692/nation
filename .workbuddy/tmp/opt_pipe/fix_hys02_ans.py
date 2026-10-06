# -*- coding: utf-8 -*-
"""fix_hys02_ans.py —— 回源补录 HYS-02-06 的参考答案（源＝02-讲义/物化专题2答案，扫描件逐页目视）。
默认 dry-run；--apply 写盘。
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')
PATH = '04-题库/2026机构初赛模拟题/化英社/题-HYS-02-06-在噪声中偏向于随机里定轨在化.md'

NEW = r'''**6.1.1** $0$（1 分）

**6.1.2**

$$P = \frac{10!}{7!\,3!}\left(\frac{1}{2}\right)^{10} = 11.72\%$$（2 分）

**6.2.1** 在平衡状态下，相邻两个位置有 $\frac{p(x+a)}{p(x)} = e^{Fa/kT} = 6.99$（1 分）；平衡态净流量为 0，故 $p_+ p(x) = p_- p(x+a)$，即 $\frac{p_+}{p_-} = 6.99$（1 分）；结合 $p_+ + p_- = 1$，解得 $p_- = 87.48\%$，$p_+ = 12.52\%$（2 分）。〔共 4 分〕

**6.2.2** $Na(p_+ - p_-) = 7.50a \approx 60\ \mathrm{nm}$（2 分）

**6.2.3** 定义随机变量 $N_+ = n_+$，描述分子向右运动的次数：$P(N_+ = n_+) = \frac{10!}{n_+!\,n_-!}p_+^{n_+}p_-^{n_-}$。做功的期望值为

$$[W] = \sum_{n_+=0}^{10}\frac{10!}{n_+!\,n_-!}p_+^{n_+}p_-^{n_-}(n_+ - n_-) = NFa(p_+ - p_-) = 6 \times 10^{-20}\ \mathrm{J}$$（2 分）

**6.2.4** (d)(e)（2 分）

**6.3** (c)(d)（2 分）

**6.4.1** 当 $\beta$ 远小于 $\omega^*$ 时，$\kappa_{KR} \approx 1$，$k = k_{TST}\kappa_{KR} = \frac{k_B T}{h}e^{-\frac{\Delta G_m}{RT}}$（1 分）；当 $\beta$ 远大于 $\omega^*$ 时，$\kappa_{KR} = \frac{1}{1 + \frac{\beta}{2\omega^*}} \approx \frac{\omega^*}{\beta}$（2 分），故 $k = k_{TST}\kappa_{KR} = \frac{k_B T}{h}e^{-\frac{\Delta G_m}{RT}} \times \frac{\omega^* m D}{k_B T} = \frac{\omega^* m D}{h}e^{-\frac{\Delta G_m}{RT}}$（1 分）。〔共 4 分〕

**6.4.2** 针对该势能面有 $\frac{\mathrm{d}V}{\mathrm{d}x} = -a_0 x + c_0 x^3$；故该势能面三个极值点为 $0$、$\pm\sqrt{\frac{a_0}{c_0}}$，显然前者为过渡态，后两者为平衡位置。（3 分）〔共 4 分〕

**6.4.3** 在 $0$ 附近近似有 $V = E_0 - \frac{a_0}{2}x^2 + \frac{c_0}{4}x^4 \approx E_0 - \frac{a_0}{2}x^2$（2 分），即 $\omega^* = \sqrt{\frac{a_0}{m}} = 2.04 \times 10^{14}\ \mathrm{s^{-1}}$（1 分）；在 $\sqrt{\frac{a_0}{c_0}}$ 附近近似有

$$V = E_0 - \frac{a_0}{2}\cdot\frac{a_0}{c_0} + \frac{c_0}{4}\cdot\frac{a_0^2}{c_0^2} \approx E_0 - \frac{a_0^2}{4c_0} + a_0\left(x - \sqrt{\frac{a_0}{c_0}}\right)^2$$（2 分）

即 $\omega_0 = \sqrt{\frac{2a_0}{m}} = 2.88 \times 10^{14}\ \mathrm{s^{-1}}$（1 分），$E_0 = \frac{a_0^2}{4c_0} = 26.3\ \mathrm{kJ/mol}$（2 分）。〔共 8 分〕

**6.4.4** $\beta = \frac{k_B T}{mD} = 2.49 \times 10^{4}\ \mathrm{s^{-1}}$（1 分）；$\kappa_{KR} = \sqrt{1 + \left(\frac{\beta}{2\omega^*}\right)^2} - \frac{\beta}{2\omega^*} = 0.56$（1 分）；$k = k_{TST}\kappa_{KR} = 0.56 \times \frac{k_B T}{h}e^{-\frac{E}{RT}} = 9.2 \times 10^{7}\ \mathrm{s^{-1}}$（2 分）。〔共 4 分〕'''

raw = open(PATH, 'rb').read()
bom = raw[:3] == b'\xef\xbb\xbf'
t = raw.decode('utf-8-sig')
i = t.index('## 参考答案')
j = t.index('## 知识点映射')
assert 0 < i < j, '锚点异常'
t2 = t[:i] + '## 参考答案\n\n' + NEW + '\n\n' + t[j:]
print('原参考答案段长 %d 字 → 新 %d 字' % (j - i, len(NEW) + 2))
if '--apply' in sys.argv:
    open(PATH, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + t2.encode('utf-8'))
    print('已写盘')
else:
    print('dry-run')
