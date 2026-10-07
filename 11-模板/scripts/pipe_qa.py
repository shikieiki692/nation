#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨管线统一 QA 门禁（2026-10-07 建）。

为什么需要它：今天在管线上踩的坑几乎都能被它自动拦住——
  ① 管线脚本放在 `.workbuddy/`（gitignore）⇒ 清理工作区即丢失
  ② 硬编码 `C:\Obsidion\妙妙屋` ⇒ 换机器即崩
  ③ 生成类脚本没有 dry-run ⇒ 误跑就改写库（今天实际发生：改写 3 个卷 ＋ 回填 150 张卡 used_in）
  ④ 生成/回填入口不在 `__main__` 内 ⇒ import 即产生副作用
  ⑤ 改完没跑测试 ⇒ 引入重复题等缺陷而不自知

用法：
    python 11-模板/scripts/pipe_qa.py            # 只跑静态检查
    python 11-模板/scripts/pipe_qa.py --with-tests   # 再跑 pipe_tests.py
退出码 0 = 全过；1 = 有失败。
"""
import os
import re
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# ── 管线清单：(文件名, 是否生成类[写盘/回填], 说明) ──
PIPES = [
    ("fm_parse.py", False, "FM 解析唯一口径"),
    ("pipe_tests.py", False, "管线回归测试基座"),
    ("gen_module_set.py", True, "模块习题集生成"),
    ("build_module_book.py", True, "模块习题书生成"),
    ("special_papers.py", True, "一分册/二分册专项卷组卷"),
    ("build_student_edition.py", True, "习题集学生版生成"),
    ("testpaper_v2.py", True, "三篇阶段测试卷"),
    ("gen_weak_drill.py", True, "弱项补强卷（唯一按 KP 抽题）"),
    ("qa_simvol_papers.py", False, "初赛模拟卷 QA"),
    ("testpaper_generate.py", True, "阶段测试卷 v1（旧版，已被 v2 取代）"),
    ("zj_generate.py", True, "ZJ 卷生成"),
    ("gen_r1.py", True, "第一轮练习册"),
    ("gen_r1_mixed.py", True, "第一轮混合版"),
]
# 已知的历史遗留：这些脚本仍在 .workbuddy/（gitignore 会丢），迁入前先豁免
KNOWN_MISSING = {"testpaper_generate.py", "zj_generate.py", "gen_r1.py", "gen_r1_mixed.py"}
# 库模块：只被 import，不作可执行脚本 ⇒ 不要求 __main__ 保护
LIB_MODULES = {"fm_parse.py": "解析器，被 import", "pipe_tests.py": "测试脚本，自带 main", "pipe_qa.py": "门禁脚本，自带 main"}

WRITE_CALL = re.compile(r"(?:^|\s)(?:[\w.]+\.)?(write_text|write_bytes|open\s*\([^)]*[\"'][wa])", re.M)
MAIN_GUARD = re.compile(r'if\s+__name__\s*==\s*[\'"]__main__[\'"]')

results = []


def chk(name, ok, detail=""):
    results.append((name, bool(ok), detail))


for fn, gen, desc in PIPES:
    p = os.path.join(HERE, fn)
    if not os.path.exists(p):
        if fn in KNOWN_MISSING:
            chk("%-26s 位置" % fn, True, "未入库（已登记豁免）")
        else:
            chk("%-26s 位置" % fn, False, "**文件不存在于 11-模板/scripts/**")
        continue
    chk("%-26s 位置" % fn, True, desc)
    src = open(p, encoding="utf-8", errors="replace").read()

    # ① 硬编码 vault 绝对路径
    hard = re.search(r'C:[\\/]+Obsidion', src)
    chk("%-26s 无硬编码路径" % fn, not hard,
        "" if not hard else "含 Obsidion 绝对路径（换机器会崩）")

    # ② 生成类脚本必须有 dry-run（除非它只写 .workbuddy/tmp 之外的 staging）
    if gen:
        has_dry = ("--write" in src and "DRY-RUN" in src) or ("APPLY" in src and "dry" in src.lower())
        chk("%-26s 有 dry-run" % fn, has_dry,
            "" if has_dry else "生成类脚本但无 dry-run ⇒ 误跑即改写库")

    # ③ 生成/回填入口必须在 __main__ 内（用 AST 判断「模块顶层」的直接调用，
    #    不能按行匹配——否则函数体内的 open(...,'w') 会被误判成顶层写盘）
    if MAIN_GUARD.search(src):
        top = src.split('if __name__', 1)[0]
        bad_top = []
        try:
            import ast
            tree = ast.parse(src)
            for node in tree.body:                    # 只看**模块顶层**节点
                if isinstance(node, ast.Try):
                    nodes = list(node.body)
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    nodes = []                        # 函数/类定义体不算顶层执行
                else:
                    nodes = [node]
                for n in nodes:
                    for sub in ast.walk(n) if not isinstance(n, (ast.FunctionDef, ast.ClassDef)) else []:
                        if isinstance(sub, ast.Call):
                            # ⚠️ 别用 `fn` 这个名字——外层循环变量也是它，会被覆盖
                            callee = sub.func
                            cname = getattr(callee, "attr", None) or getattr(callee, "id", None)
                            if cname in ("write_text", "write_bytes", "open", "save"):
                                bad_top.append(cname)
        except SyntaxError as e:
            bad_top = ["<语法错误 %s>" % str(e)[:30]]
        chk("%-26s 顶层不写盘" % fn, not bad_top,
            "" if not bad_top else "模块顶层有写盘调用：%s" % ",".join(sorted(set(bad_top))))
    else:
        # 库模块（被 import 的解析器）豁免 main 保护
        chk("%-26s main 保护" % fn, LIB_MODULES.get(fn),
            "" if LIB_MODULES.get(fn) else "缺 `if __name__ == \"__main__\"` 保护（import 即执行）")

print("=" * 74)
print("跨管线统一 QA 门禁　　脚本 %d 条" % len(PIPES))
print("=" * 74)
for name, ok, detail in results:
    print("  %s %-30s %s" % ("✔" if ok else "✘", name, detail))

bad = [r for r in results if not r[1]]
print()
print("静态检查：%d/%d 通过" % (len(results) - len(bad), len(results)))
if bad:
    print("失败：" + "、".join(n for n, _, _ in bad))

rc = 1 if bad else 0
if "--with-tests" in sys.argv:
    print("\n---- 跑测试基座 ----")
    r = subprocess.run([sys.executable, os.path.join(HERE, "pipe_tests.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r.stdout[-1200:])
    rc = rc or r.returncode

sys.exit(rc)