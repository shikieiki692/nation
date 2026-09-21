# -*- coding: utf-8 -*-
"""自证 `ce_invariant_violations`。

⚠️ 上一版自证的**盲区**：样例 `\\ce{MnO4^-}` 里**没有 LaTeX 命令**，而函数里
   「跳过命令」的分支漏了 `k += 1` ⇒ 死循环；自证完全没抓到，直到把整份
   `Zincke反应.md`（其 `\\ce{}` 内含 `\\cmd`）喂进去才挂死。
   ⇒ 本版**必须含**「`\\ce{}` 内含命令」的用例，并逐例计时（Windows 无 SIGALRM，
      挂死由外层 `timeout` 兜底）。
"""
import importlib.util
import sys
import time
from pathlib import Path

V = Path(r"C:\Obsidion\妙妙屋")
sys.path.insert(0, str(V / "11-模板" / "scripts"))


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, V / rel)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


rg = load("11-模板/scripts/render_gate.py", "rg")
bh = load("11-模板/scripts/build-all-handout-docx.py", "bh")


class FakeOld:
    """模拟修复前：` + ` 被抬成 `^{+}`。"""

    @staticmethod
    def _preprocess_ce_in_math(s):
        return s.replace(" + ", " ^{+} ")


class FakeOldCJK:
    """模拟「含中文的箭头标注整段包 `\\text{}`、里面数字不下标」的旧行为。"""

    @staticmethod
    def _preprocess_ce_in_math(s):
        import re as _re
        return _re.sub(r"->\[([^\]]*)\]",
                       lambda m: "\x5cxrightarrow{\x5ctext{" + m.group(1) + "}}", s)


CASES = [
    ("① 当前管线·含电荷", bh, "$\\ce{MnO4^-}$", 0),
    ("② 当前管线·含命令（上版盲区）", bh, "$\\ce{2KClO3 ->[\\Delta\\,\\text{或}\\,h\\nu] 2KCl + 3O2 ^}$", 0),
    ("③ 当前管线·中文标注已补下标", bh, "$\\ce{R-X + Mg ->[Et2O 或 THF] R-Mg-X}$", 0),
    ("④ 当前管线·正确写法不误报", bh, "$\\ce{MnO_{4}^{-} + 2NaOH}$ 与 $\\ce{S_{N}2}$", 0),
    ("⑤ 模拟旧行为（应响）", FakeOld, "$\\ce{H2SO4 + 2NaOH}$", 3),
    ("⑥ 模拟「中文标注不下标」（应响）", FakeOldCJK, "$\\ce{R-X + Mg ->[Et2O 或 THF] R-Mg-X}$", 1),
]
ok = True
for name, mod, text, want in CASES:
    t0 = time.monotonic()
    got = rg.ce_invariant_violations(mod, text)
    dt = time.monotonic() - t0
    good = (got == want) and dt < 5
    ok &= good
    print("%-38s -> %-6r 期望 %r  (%.3fs)  %s" % (name, got, want, dt, "PASS" if good else "FAIL"))

t0 = time.monotonic()
t = (V / "03-知识点/有机化学/Zincke反应.md").read_text(encoding="utf-8")
got = rg.ce_invariant_violations(bh, t)
dt = time.monotonic() - t0
good = (got == 0) and dt < 20
ok &= good
print("%-38s -> %-6r 期望 %r  (%.3fs)  %s" % ("⑥ 真实文件 Zincke反应.md", got, 0, dt, "PASS" if good else "FAIL"))

print()
print("✅ 全部通过" if ok else "❌ 有失败项")
sys.exit(0 if ok else 1)
