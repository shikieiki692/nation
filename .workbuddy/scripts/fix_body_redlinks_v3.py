# -*- coding: utf-8 -*-
"""
阶段七 v3：保守版正文断链修复

v2 教训：算法把"描述不同的子子题"折叠到错误父题，污染了校验报告，
还把一些概念做了越级上位（硒鎓离子→硒，桥连硫配位→氢键 之类）。

v3 策略：
  1. 只做【手工白名单】—— 概念别名/上位/同义，每条都经过人工核对。
  2. 不动 题号- 类（子子题折叠容易错位，留人工拆分）。
  3. 排除 09-审计报告/auto-validation/、.workbuddy/、.git/ 下的源文件。
  4. 每个替换记录 (文件, 旧, 新) 到日志；commit 时只提交日志里出现的文件。
"""
import os, re, sys, collections

VAULT = r"C:\Obsidion\妙妙屋"
LOG = os.path.join(VAULT, ".workbuddy", "scripts", "fix_body_redlinks_v3.log")

# 白名单：仅 1-级 上位 / 同义。逐条人工审过。
# 格式: (old, new, reason)
WHITELIST = [
    ("晶胞计算",       "晶胞",         "上位概念"),
    ("配合物推断",     "配合物",       "上位概念"),
    ("碘量法滴定",     "碘量法",       "上位方法（滴定是技术类型，碘量法是方法名）"),
    ("环丙烯开环",     "三元环开环",   "上位（环丙烯是三元环特例）"),
    ("共轭稳定性",     "共轭效应",     "上位"),
    ("二重旋转轴",     "旋转轴",       "上位"),
    ("对称氢键",       "氢键",         "上位"),
    ("臭氧化机理",     "臭氧化反应",   "上位"),
    ("铁化学",         "铁",           "上位（铁化学是元素化学分支，铁是其核心）"),
    ("高铁酸根",       "铁",           "上位（高铁酸根是 Fe(VI) 物种）"),
    ("铬配合物",       "铬",           "上位"),
    ("亚硝酸钠",       "钠",           "上位（亚硝酸钠是钠盐）"),
    ("单氟磷酸钠",     "磷",           "上位（单氟磷酸钠是含磷化合物）"),
    ("超重元素",       "元素周期律",   "上位（超重元素是周期律研究对象）"),
    # 相同/近义
    ("化学式推导",     "化学式推断",   "近义"),
    ("化学式计算",     "化学式推断",   "上位"),
    ("化学式确定",     "化学式推断",   "近义"),
    ("胶体与表面活性剂", "胶体与表面化学",  "近义（这两都该存在，但 胶体与表面活性剂 是个不存在的简化名）"),
    # 笔记别名：原笔记名是简称，指向一个标准名
    ("硒",             "硒",           "no-op（debug）"),
]
WHITELIST = [(o, n, r) for o, n, r in WHITELIST if o != n]

# ---------- 1. 收集全库 md basename 索引 ----------
def collect_all_md():
    s = set()
    for r, ds, fs in os.walk(VAULT):
        if any(p in {".git", "node_modules", ".obsidian", ".trash",
                     "__pycache__", ".workbuddy", "09-审计报告/auto-validation"}
               for p in r.split(os.sep)):
            continue
        for f in fs:
            if f.endswith(".md"):
                s.add(f[:-3])
    return s

ALL_MD = collect_all_md()
# 验证：所有 target 必须真实存在
for o, n, r in WHITELIST:
    if n not in ALL_MD:
        print(f"!! target 不存在，禁用 {o} -> {n}（{r}）")
WHITELIST = [(o, n, r) for o, n, r in WHITELIST if n in ALL_MD]
print(f"白名单有效条目 {len(WHITELIST)} 条")

# ---------- 2. 应用替换 ----------
def is_excluded(p):
    rel = os.path.relpath(p, VAULT)
    if rel.startswith("09-审计报告/auto-validation"):
        return True
    if rel.startswith(".workbuddy/") or rel.startswith(".git/"):
        return True
    return False

log_lines = []
ok, fail = 0, 0
seen_files = set()
for r, ds, fs in os.walk(VAULT):
    if any(p in {".git", "node_modules", ".obsidian", ".trash",
                 "__pycache__", ".workbuddy"}
           for p in r.split(os.sep)):
        continue
    for f in fs:
        if not f.endswith(".md"):
            continue
        p = os.path.join(r, f)
        if is_excluded(p):
            continue
        try:
            t = open(p, "r", encoding="utf-8", newline="").read()
        except Exception as e:
            log_lines.append(f"FAIL read {p}: {e}")
            fail += 1
            continue
        new_t = t
        file_changes = []
        for old, new, reason in WHITELIST:
            # 匹配 [[old]] 与 [[old|...]] 两种
            pat = re.compile(rf'\[\[{re.escape(old)}(\|[^\]]*)?\]\]')
            if pat.search(new_t):
                new_t2 = pat.sub(f"[[{new}\\1]]", new_t)
                n = len(pat.findall(new_t))
                file_changes.append((old, new, n, reason))
                new_t = new_t2
        if new_t != t:
            try:
                with open(p, "w", encoding="utf-8", newline="") as fp:
                    fp.write(new_t)
            except Exception as e:
                log_lines.append(f"FAIL write {p}: {e}")
                fail += 1
                continue
            seen_files.add(p)
            for old, new, n, reason in file_changes:
                log_lines.append(
                    f"{os.path.relpath(p, VAULT):80s}  {n}× [[{old}]] → [[{new}]]  ({reason})"
                )
            ok += len(file_changes)

open(LOG, "w", encoding="utf-8").write("\n".join(log_lines))
print(f"\n修改 {len(seen_files)} 个文件，{ok} 处替换，{fail} 失败。日志：{LOG}")
for line in log_lines[:30]:
    print(" ", line)
if len(log_lines) > 30:
    print(f"  ... 另有 {len(log_lines)-30} 行")
