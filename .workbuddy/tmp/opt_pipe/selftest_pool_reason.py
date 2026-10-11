# -*- coding: utf-8 -*-
"""selftest_pool_reason.py —— 自证 `why_not_in_pool()` 的判定链（P1-7 精神：判据要有牙）。

自证项（每项都必须通过，否则说明复演与主循环不一致）：
  ① 在池卡（卷 XVI 第 1 题） ⇒ 返回 None；
  ② 排除清单卡（xvi_exclude.txt 首条） ⇒ 报「排除清单」；
  ③ 越界闸命中卡（当前 OVERFLOW_HITS 任取一张） ⇒ 报「越界闸」；
  ④ 关掉 ALL_YEARS 后，同一张在池卡若属非 25–26 ⇒ 报「年份闸」；
  ⑤ 不存在的路径 ⇒ 报「文件不存在」。
"""
import importlib.util
import os
import re
import sys

VAULT = r"C:\Obsidion\妙妙屋"
OPT = os.path.join(VAULT, ".workbuddy", "tmp", "opt_pipe")
sys.path.insert(0, OPT)
os.chdir(VAULT)

spec = importlib.util.spec_from_file_location("BORG", os.path.join(OPT, "build_org.py"))
BO = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BO)

fails = []


def probe(desc, path, want_sub, all_years=True):
    BO.ALL_YEARS = all_years
    got = BO.why_not_in_pool(path)
    ok = (want_sub is None and got is None) or (want_sub is not None and got and want_sub in got)
    print("  [%s] %-42s → %s" % ("PASS" if ok else "FAIL", desc, got))
    if not ok:
        fails.append((desc, want_sub, got))


# ① 在池卡：卷 XVI 第 1 题
probe("在池卡（XVI 题1 HYS-15-04）", os.path.join(VAULT, "04-题库/2026机构初赛模拟题/化英社/题-HYS-15-04-近年来随着金属有机框架MOF.md"), None)

# ② 排除清单卡（EXCLUDE 只在传 --exclude 时载入 ⇒ 这里手动注入，验证该分支）
exc = os.path.join(OPT, "xvi_exclude.txt")
if os.path.exists(exc):
    first = [x.strip() for x in open(exc, encoding="utf-8") if x.strip()]
    if first:
        _saved = set(BO.EXCLUDE)
        BO.EXCLUDE = set(first)
        probe("排除清单卡（xvi_exclude 首条，注入 EXCLUDE）", os.path.join(VAULT, first[0]), "排除清单")
        BO.EXCLUDE = _saved

# ③ 越界闸命中卡（跑一次池以填充 OVERFLOW_HITS）
BO.build_pool()
if BO.OVERFLOW_HITS:
    p = BO.OVERFLOW_HITS[0][0]
    probe("越界闸命中卡（OVERFLOW_HITS[0]）", p, "越界闸")
elif BO.ECHO_HITS:
    probe("答案可用闸命中卡（ECHO_HITS[0]）", BO.ECHO_HITS[0], "答案可用闸")
else:
    print("  [SKIP] 本次池无越界/回显命中可测")

# ④ 从池里找一张「非 25–26」的卡，关 ALL_YEARS 后应报年份闸
_pool = BO.build_pool()
_non_recent = None
for _m in _pool:
    for _c in _pool[_m]:
        # 按卡 FM 的 source_norm/source_file 重算年份归属
        _t = open(_c['path'], encoding='utf-8').read()
        _norm = (re.search(r'^source_norm:\s*(.*)$', _t, re.M) or [None, ''])[1].strip()
        _sf = (re.search(r'^source_file:\s*(.*)$', _t, re.M) or [None, ''])[1].strip()
        if BO.in_2526(_norm, _sf) == 0:
            _non_recent = _c['path']
            break
    if _non_recent:
        break
if _non_recent:
    probe("非 25–26 在池卡（关 ALL_YEARS）", _non_recent, "年份闸", all_years=False)
else:
    print("  [SKIP] 池内全是 25–26 卡，年份闸分支无法用真实卡自证")

# ⑤ 不存在路径
probe("不存在的路径", os.path.join(VAULT, "04-题库/2026机构初赛模拟题/化英社/题-不存在.md"), "文件不存在")

BO.ALL_YEARS = True
print("\n自证结果:", "✅ PASS" if not fails else "❌ FAIL %s" % fails)
sys.exit(0 if not fails else 1)
