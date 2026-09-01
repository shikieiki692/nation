# -*- coding: utf-8 -*-
r"""
从 Windows 回收站按「原始路径」精确还原文件。

背景：阶段2 误删了 110 张被 [[...]]（非嵌入双括号，多写在 frontmatter 的
key_images 里）引用的图片——image_usage_stats.py 只认 ![[...]]，漏了这种写法。
这些文件必须还原。

原理：回收站里每个被删文件生成一对
  $I<随机>  元数据：含原始完整路径（UTF-16LE）+ 删除时间 + 文件大小
  $R<随机>  真实内容
解析 $I 拿到原始路径，把对应 $R 拷回原位。

用法：
  python restore_from_bin.py <需要还原的原始路径清单.txt> [--apply]
"""
import os, re, sys, glob, shutil, struct, collections

# ---- $I 元数据解析 ---------------------------------------------------------
# 实测本机（Win10+，$I 文件 version=2）布局：
#   0x00 uint32 版本(2)
#   0x08 uint64 文件大小
#   0x10 FILETIME 删除时间
#   0x18 uint32 原始路径字符数
#   0x1C      原始路径 UTF-16LE（不定长，以 \0 结尾）
# 注意：网上很多资料写 0x14/0x18，那是旧版(version=1)布局，在本机会解析出乱码。
OFF_LEN = 0x18
OFF_PATH = 0x1C


def parse_i(path):
    try:
        with open(path, "rb") as f:
            b = f.read(OFF_PATH + 600)
    except OSError:
        return None
    if len(b) < OFF_PATH + 4:
        return None
    n = struct.unpack_from("<I", b, OFF_LEN)[0]
    if not (4 <= n <= 32767):
        return None
    try:
        s = b[OFF_PATH: OFF_PATH + n * 2].decode("utf-16-le", "ignore")
    except Exception:
        return None
    s = s.split("\x00")[0]
    if not re.match(r"^[A-Za-z]:[\\/]", s):
        return None
    return s


def build_index():
    """返回 {规范化原始路径: [($R路径, 删除时间), ...]}"""
    idx = collections.defaultdict(list)
    roots = []
    for drv in "CDEFGH":
        # 注意：os.path.join("C:", "x") 得到 "C:x"（盘符后不加分隔符），必须写 "C:\\"
        p = drv + ":\\$Recycle.Bin"
        if os.path.isdir(p):
            roots.append(p)
    if not roots:
        print("  ⚠ 未找到任何 $Recycle.Bin 目录")
    for root in roots:
        try:
            sids = os.listdir(root)
        except OSError:
            continue
        for sid in sids:
            d = os.path.join(root, sid)
            if not os.path.isdir(d):
                continue
            try:
                names = os.listdir(d)      # SYSTEM 等 SID 目录会 PermissionError
            except OSError:
                continue
            for name in names:
                if not name.startswith("$I"):
                    continue
                ip = os.path.join(d, name)
                orig = parse_i(ip)
                if not orig:
                    continue
                rp = os.path.join(d, "$R" + name[2:])
                if not os.path.isfile(rp):
                    continue
                try:
                    mt = os.path.getmtime(ip)
                except OSError:
                    mt = 0
                idx[os.path.normcase(os.path.abspath(orig))].append((rp, mt))
    return idx


def main(apply=False):
    lst = sys.argv[1] if len(sys.argv) > 1 else None
    if not lst or not os.path.isfile(lst):
        print("用法: python restore_from_bin.py <清单> [--apply]")
        return 1
    targets = [l.strip() for l in open(lst, encoding="utf-8") if l.strip()]
    print("待还原 %d 个文件" % len(targets))

    print("[1/2] 建立回收站索引（解析 $I 元数据）...")
    idx = build_index()
    print("  回收站条目 %d 条" % sum(len(v) for v in idx.values()))

    print("[2/2] 还原...")
    done, fail, already = [], [], []
    for t in targets:
        key = os.path.normcase(os.path.abspath(t))
        if os.path.isfile(t):
            already.append(t)
            continue
        cands = sorted(idx.get(key, []), key=lambda x: -x[1])  # 取最新一条
        ok = False
        for rp, _ in cands:
            try:
                os.makedirs(os.path.dirname(t), exist_ok=True)
                shutil.copy2(rp, t)
                if os.path.isfile(t) and os.path.getsize(t) > 0:
                    ok = True
                    break
            except Exception:
                continue
        if ok:
            done.append(t)
        else:
            fail.append(t)

    print("-" * 60)
    print("  已还原 %d" % len(done))
    print("  本来就在 %d" % len(already))
    print("  失败 %d" % len(fail))
    for f in fail[:15]:
        print("      " + f)
    if not apply:
        print("\n（试跑模式，未真正写入）")
    return 0


if __name__ == "__main__":
    main(apply="--apply" in sys.argv)
