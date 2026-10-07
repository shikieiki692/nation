# -*- coding: utf-8 -*-
"""yamlcheck.py —— FM 校验（口径同库内 js-yaml4 严格语义）。

· 重复键 ⇒ THROW（js-yaml4 在 Obsidian 里会让整页消失，P0）
· FM 无法解析 ⇒ 报错
· `pool_scope` 必须在 FM 内、值在允许集里、且只出现一次
用法：python yamlcheck.py <paths.txt>   # 每行一个相对路径
"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Obsidion\妙妙屋\11-模板\scripts")
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

ROOT = r"C:\Obsidion\妙妙屋"
FM = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", re.S)
OK_VALS = {"有机化学", "讲稿", "无答案练习", "待复核", "真题重合"}

y = YAML(typ="safe", pure=True)
y.allow_duplicate_keys = False

paths = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
bad, nokey = [], 0
for rel in paths:
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    t = open(p, encoding="utf-8-sig").read()
    if "\r\n" in t:
        bad.append((rel, "含 CRLF")); continue
    m = FM.match(t)
    if not m:
        bad.append((rel, "无 FM")); continue
    fm = m.group(1)
    try:
        d = y.load(fm)
    except Exception as e:
        bad.append((rel, "YAML 解析失败: %s" % str(e)[:80])); continue
    if not isinstance(d, dict):
        bad.append((rel, "FM 非映射")); continue
    ps = d.get("pool_scope")
    if ps is None:
        nokey += 1                     # 入池卡本就不该有 pool_scope ⇒ 只计数，不判错
    else:
        if ps not in OK_VALS:
            bad.append((rel, "pool_scope 值非法: %r" % ps))
        if len(re.findall(r"(?m)^pool_scope[ \t]*:", fm)) != 1:
            bad.append((rel, "pool_scope 键数≠1"))

print("校验 %d 文件；无 pool_scope %d；异常 %d" % (len(paths), nokey, len(bad)))
for rel, why in bad[:30]:
    print("  ✗", why, "|", rel)
print("RESULT:", "PASS" if not bad else "FAIL(%d)" % len(bad))
