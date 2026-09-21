"""PDF 线 MiKTeX 环境的两条修复的回归测试（2026-09-21 格式线）。

背景（实测）：
① `fc-conflist` 预热在本机**直接崩**（returncode 3221225477 = 0xC0000005），
   而 xelatex 引擎本身正常 ⇒ 预热失败**不该**把整条线封死。
② 沙箱里没有 fontconfig 配置时，若仍把 `MIKTEX_USERCONFIG` 指进沙箱，
   xelatex 会 `rc=9 / Fontconfig error: Cannot load default config file /
   fontconfig initialization failed!` 直接死掉（0 字节 PDF）；
   **不覆盖** MIKTEX_USER* 则回落到用户配置，同一份 .tex 成功出 202 KB PDF。

本测试锁住：预热失败不 raise（只告警）+ 沙箱配置缺失时回落用户配置。
"""
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

VAULT = Path(r"C:\Obsidion\妙妙屋")
P = VAULT / "11-模板" / "scripts" / "convert_handout_to_pdf.py"

spec = importlib.util.spec_from_file_location("chp_env", P)
chp = importlib.util.module_from_spec(spec)
sys.modules["chp_env"] = chp
try:
    spec.loader.exec_module(chp)
except SystemExit:
    pass

n_pass = n_fail = 0


def check(name, ok, extra=""):
    global n_pass, n_fail
    n_pass += ok
    n_fail += (not ok)
    print("%-4s %-52s %s" % ("PASS" if ok else "FAIL", name, extra))


# ① 沙箱配置可用 → 覆盖 MIKTEX_USER*（保持原设计）
_orig = chp._sandbox_fontconfig_ok
chp._sandbox_fontconfig_ok = lambda: True
e = chp.build_miktex_env()
check("沙箱可用时设置 MIKTEX_USERCONFIG",
      e.get("MIKTEX_USERCONFIG", "").startswith(chp.MIKTEX_SANDBOX),
      e.get("MIKTEX_USERCONFIG", "")[-28:])

# ② 沙箱配置缺失 → 必须**不设置**（回落用户配置）
chp._sandbox_fontconfig_ok = lambda: False
e2 = chp.build_miktex_env()
check("沙箱缺失时**不**设 MIKTEX_USERCONFIG（回落用户配置）",
      "MIKTEX_USERCONFIG" not in e2)
check("沙箱缺失时仍设 HOME/USERPROFILE",
      e2.get("HOME") == chp.WINDOWS_HOME and e2.get("USERPROFILE") == chp.WINDOWS_HOME)
chp._sandbox_fontconfig_ok = _orig

# ③ 预热失败必须**不 raise**，只告警
class _FakeSubproc:
    @staticmethod
    def run(*a, **k):
        return SimpleNamespace(returncode=3221225477,
                               stdout=b"",
                               stderr=b"Fontconfig error: Cannot load default config file\r\n")

    class TimeoutExpired(Exception):
        pass


_orig_sp = chp.subprocess
_orig_decode = chp.decode_subprocess_output
_orig_ready = chp._miktex_ready
try:
    chp.subprocess = _FakeSubproc
    chp.decode_subprocess_output = lambda r: None
    chp._miktex_ready = False
    # 用一个不可能存在的沙箱路径，确保走「需要预热」分支
    _orig_sandbox = chp.MIKTEX_SANDBOX
    chp.MIKTEX_SANDBOX = str(VAULT / ".workbuddy" / "tmp" / "_no_such_sandbox")
    ok = True
    try:
        chp.ensure_miktex_sandbox()
    except Exception as exc:
        ok = False
        print("        异常: %s: %s" % (type(exc).__name__, exc))
    check("预热失败只告警、不 raise", ok)
    check("预热失败后仍标记 ready（允许继续编译）", chp._miktex_ready is True)
finally:
    chp.subprocess = _orig_sp
    chp.decode_subprocess_output = _orig_decode
    chp._miktex_ready = _orig_ready
    if 'chp' in dir() and 'MIKTEX_SANDBOX' in dir(chp):
        pass

print()
print("=" * 62)
print("PASS %d / FAIL %d" % (n_pass, n_fail))
sys.exit(1 if n_fail else 0)
