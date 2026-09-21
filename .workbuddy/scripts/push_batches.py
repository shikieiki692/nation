"""分小批推送产物（应对高抖动网络）。

背景：单次 push 15-25MB 反复被 `the remote end hung up unexpectedly` 打断。
策略：把剩余改动按 **~5MB** 切成小批，每批一个 commit，然后
`git push origin <sha>:master` —— 这样每次只需上传该批的对象，失败也不影响已推部分。

每次调用做一件事：
  1. 若 HEAD 尚未推上去 → 只尝试推送一次（失败就退出，下次再试）
  2. 若 HEAD 已推上去且工作区还有改动 → 提交下一小批（然后退出，由下次调用推）
反复调用直到全部推完。
"""
import subprocess
import time
import sys
from pathlib import Path

ROOT = Path(r"C:\Obsidion\妙妙屋")
BATCH_BYTES = 5 * 1024 * 1024
WINCRED = (r"C:/Users/蕾赛/.workbuddy/binaries/PortableGit/versions/1.2.0/"
           r"mingw64/bin/git-credential-wincred.exe")
ENV = {"GIT_TERMINAL_PROMPT": "0"}

CRED = ["-c", "credential.helper=", "-c", "credential.helper=!" + WINCRED,
        "-c", "http.proxy=", "-c", "https.proxy="]


def run(args, timeout=900, check=True):
    r = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout,
                       env={**__import__("os").environ, **ENV})
    if check and r.returncode != 0:
        print("  [cmd %s] rc=%d\n%s%s" % (" ".join(args[:2]), r.returncode,
                                          r.stdout[-400:], r.stderr[-400:]))
    return r


def head():
    return run(["git", "rev-parse", "HEAD"]).stdout.strip()


def remote_head():
    r = run(["git", "ls-remote", "origin", "master"], timeout=60)
    return r.stdout.strip().split("\t")[0] if r.stdout.strip() else ""


def dirty_files():
    """只取**已暂存**的文件（dirty 全量会把并行会话的未跟踪文件也捞进来，害提交失败）。"""
    r = run(["git", "-c", "core.quotepath=false", "diff", "--cached", "--name-only"])
    return [p for p in r.stdout.splitlines() if p.strip()]


def next_batch(paths):
    """按体积贪心取一批（单个文件超限也单独成批）。"""
    items = sorted(((ROOT / p).stat().st_size, p) for p in paths
                   if (ROOT / p).exists() and (ROOT / p).is_file())
    batch, total = [], 0
    for size, p in items:
        if batch and total + size > BATCH_BYTES:
            break
        batch.append(p)
        total += size
    return batch, total


def push_head(h):
    """把当前 HEAD 推到远端，最多试 3 次。成功返回 True。"""
    for i in range(1, 4):
        print("  推送尝试 %d（HEAD=%s）…" % (i, h[:9]))
        r = run(["git"] + CRED + ["push", "origin", "%s:master" % h],
                timeout=1500, check=False)
        rem = remote_head()
        print("    rc=%d 远端=%s" % (r.returncode, rem[:9] or "(空)"))
        if rem == h:
            return True
        time.sleep(3)
    return False


def main():
    for round_no in range(1, 13):
        h, rem = head(), remote_head()
        if h != rem:
            print("[轮 %d] HEAD 未推上去，先补推" % round_no)
            if not push_head(h):
                print("  ✗ 网络持续抖动，请再次运行本脚本继续（已推部分不会回退）。")
                return 2
            continue

        paths = dirty_files()
        if not paths:
            print("[轮 %d] ✓ 工作区干净且已同步，全部完成。" % round_no)
            return 0

        batch, total = next_batch(paths)
        print("[轮 %d] 提交 %d 个文件 / %.2f MB" % (round_no, len(batch), total / 1048576))
        r = run(["git", "commit", "-q", "--only", "-m",
                 "讲义等宽段治理：阶段6 字体补丁分批提交（%d 个文件，%0.1f MB）"
                 % (len(batch), total / 1048576), "--"] + batch)
        if r.returncode != 0:
            print("  ✗ 提交失败。")
            return 1
        print("  commit = %s" % head()[:9])

    print("达到轮次上限，请再次运行本脚本继续。")
    return 2


if __name__ == "__main__":
    sys.exit(main())
