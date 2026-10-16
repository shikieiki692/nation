# -*- coding: utf-8 -*-
"""验证 build_org.strip_q_echo 修后：GM-02-02 的 4-5 答案「d) 2分」是否保留。"""
import sys, io
sys.path.insert(0, r'C:\Obsidion\妙妙屋\.workbuddy\tmp\opt_pipe')
import build_org as BO

p = r'C:\Obsidion\妙妙屋\04-题库\2026机构初赛模拟题\伽马\题-GM-02-02-乙酸丁酯是一种重要的有机溶剂.md'
t = io.open(p, encoding='utf-8-sig').read()
j = t.find('## 参考答案')
q, a = t[:j], t[j:]
out = BO.strip_q_echo(q, a)
print('修后 保留「d) 2分」 :', 'd) 2分' in out)
print('修后 保留「c) 2分」 :', 'c) 2分' in out)
print('答案区长度 %d -> %d' % (len(a), len(out)))
# 打印尾部
print('--- 输出尾部 200 字 ---')
print(out[-200:])
