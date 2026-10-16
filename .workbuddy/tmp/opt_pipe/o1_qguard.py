# -*- coding: utf-8 -*-
"""通用：比对两份 md 的**题面区**（首个 `## 参考答案`／`<details>` 之前）是否字节相同。
用法：python o1_qguard.py <old.md> <new.md>
"""
import re, sys

ANS_MARK = re.compile(r'(?m)^#{1,3}\s*参考答案|<details')


def q_head(txt):
    m = ANS_MARK.search(txt)
    return txt[:m.start()] if m else txt


a = open(sys.argv[1], encoding="utf-8-sig").read()
b = open(sys.argv[2], encoding="utf-8-sig").read()
qa, qb = q_head(a), q_head(b)
print("题面区字节 旧=%d 新=%d  相同=%s" % (len(qa.encode()), len(qb.encode()), qa == qb))
if qa != qb:
    for i in range(min(len(qa), len(qb))):
        if qa[i] != qb[i]:
            print("首差 @%d\n旧=%r\n新=%r" % (i, qa[max(0,i-60):i+60], qb[max(0,i-60):i+60]))
            break
sys.exit(0 if qa == qb else 1)
