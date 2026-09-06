#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
把文件/目录送入 Windows 回收站（可还原），支持中文长路径。

为什么不用 send2trash：
  send2trash 会把路径转成 8.3 短名（学生讲~2\_RENDE~1\...）再调 SHFileOperation，
  中文/长路径下短名解析失败，报 [WinError 2] 找不到文件。
  这里直接用 SHFileOperationW 传原始宽字符长路径，绕开短名转换。

用法
  python trash_files.py <清单文件> --apply        # 按清单送回收站
  python trash_files.py <清单文件>                # 试跑前 N 个（默认 5）
"""
import os, sys, ctypes
from ctypes import wintypes

FO_DELETE = 3
FOF_SILENT = 0x0004
FOF_NOCONFIRMATION = 0x0010
FOF_ALLOWUNDO = 0x0040          # 送回收站
FOF_NOERRORUI = 0x0400
FOF_NOCONFIRMMKDIR = 0x0200


class SHFILEOPSTRUCTW(ctypes.Structure):
    _fields_ = [
        ("hwnd", ctypes.c_void_p),
        ("wFunc", ctypes.c_uint),
        ("pFrom", ctypes.c_wchar_p),
        ("pTo", ctypes.c_wchar_p),
        ("fFlags", ctypes.c_uint16),
        ("fAnyOperationsAborted", ctypes.c_int),
        ("hNameMappings", ctypes.c_void_p),
        ("lpszProgressTitle", ctypes.c_wchar_p),
    ]


_shfo = ctypes.windll.shell32.SHFileOperationW
_shfo.argtypes = [ctypes.POINTER(SHFILEOPSTRUCTW)]
_shfo.restype = ctypes.c_int


def trash(paths):
    """批量送回收站。paths 为绝对路径列表，一次性提交（效率高）。"""
    paths = [os.path.abspath(p) for p in paths]
    # pFrom 需要双 null 结尾，多个路径之间用单 null 分隔
    buf = "\0".join(paths) + "\0\0"
    op = SHFILEOPSTRUCTW()
    op.hwnd = None
    op.wFunc = FO_DELETE
    op.pFrom = buf
    op.pTo = None
    op.fFlags = (FOF_ALLOWUNDO | FOF_NOCONFIRMATION |
                 FOF_NOERRORUI | FOF_SILENT)
    rc = _shfo(ctypes.byref(op))
    return rc, bool(op.fAnyOperationsAborted)


def main():
    args = [a for a in sys.argv[1:]]
    apply_mode = "--apply" in args
    if apply_mode:
        args.remove("--apply")
    limit = None
    for a in list(args):
        if a.startswith("--limit="):
            limit = int(a.split("=", 1)[1])
            args.remove(a)
    if not args:
        print("用法: python trash_files.py <清单文件> [--apply] [--limit=N]")
        return 1

    lst = [l.strip() for l in open(args[0], encoding="utf-8") if l.strip()]
    exist = [p for p in lst if os.path.exists(p)]
    print("清单 %d 行 / 存在 %d 个" % (len(lst), len(exist)))
    if not exist:
        return 0

    todo = exist if apply_mode else exist[:limit or 5]
    total_bytes = sum(os.path.getsize(p) for p in todo if os.path.isfile(p))
    print("本次处理 %d 个 / %.2f MB  [%s]"
          % (len(todo), total_bytes / 1048576,
             "APPLY" if apply_mode else "试跑"))

    # 分批提交，每批 200 个，批后校验
    #
    # 注意：SHFileOperationW 在中文长路径下会返回 rc=2 (ERROR_FILE_NOT_FOUND)
    # 但**实际删除成功**（已验证：文件进了回收站且 $I 元数据里原始路径完整）。
    # 这是它内部用短名做后置校验导致的假警报。
    # => 成功与否一律以「文件是否还在」为准，不看 rc。
    BATCH = 200
    done = 0
    failed = []
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        rc, aborted = trash(batch)
        still = [p for p in batch if os.path.exists(p)]
        if still:
            # 有残留 -> 逐个重试一次
            for p in still:
                trash([p])
                if os.path.exists(p):
                    failed.append((p, "仍在"))
                else:
                    done += 1
            done += len(batch) - len(still)
        else:
            done += len(batch)
        print("  ...累计 %d/%d (rc=%d)" % (done, len(todo), rc))

    print()
    print("入回收站 %d 个 / 失败 %d 个" % (done, len(failed)))
    for p, r in failed[:10]:
        print("   FAIL rc=%s %s" % (r, p))
    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
