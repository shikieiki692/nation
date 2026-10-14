# -*- coding: utf-8 -*-
r"""卷级「图源覆盖」核验器：逐题比对**源卡图数** vs **卷内图数**，揪出丢图。

背景（2026-10-14 卷 XVII 第 1 题实测）：
  建卡丢了 3 张图（ZnN₂正交／化合物D／化合物E），但**图注 4/5/6/7 全留着** ⇒ 被合并成
  「图 4～图 7」，**外观完全看不出丢图**；正文却照旧引用「图 5」「图 6」⇒ 引而无图。
  ⇒ 决定性判据＝**回源逐题对号**（源卡图数 vs 卷内图数），而非看卷内图数是否「够多」。

用法：
  python verify_fig_coverage.py --vol XVII            # 单卷报告
  python verify_fig_coverage.py --vol XVII --strict   # 有缺图即 exit 1（可作闸门）
  python verify_fig_coverage.py --all                 # 全部有 plan 的卷

判据（三级）：
  🔴 缺图   —— 源卡图数 > 卷内图数（**正文引用可能落空**）
  🟠 多图   —— 卷内图数 > 源卡图数（可能重复引用，或跨题合并）
  ✅ 一致
退出码：--strict 且存在 🔴 ⇒ 1；否则 0。
"""
import io, os, re, sys, json, glob, hashlib

ROOT = r"C:\Obsidion\妙妙屋"
O = os.path.join(ROOT, '.workbuddy', 'tmp', 'opt_pipe')
IMG = re.compile(r'!\[\[([^\]]+)\]\]')
# ★ 源卡（chemy 等）用的是**标准 markdown 图语法** `![](images/xxx.jpg)`，
#   卷内用的是 Obsidian wikilink `![[xxx.jpg]]` ⇒ **必须两种都认**，否则源卡图数恒为 0（2026-10-14 实测踩过）
IMG_MD = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
# 图片搜索目录（内容 sha 比对用）
IMG_DIRS = glob.glob(os.path.join(ROOT, '04-题库', '**', 'images'), recursive=True)

VOL = None
for i, a in enumerate(sys.argv):
    if a == '--vol' and i + 1 < len(sys.argv):
        VOL = sys.argv[i + 1]
STRICT = '--strict' in sys.argv
ALL = '--all' in sys.argv


def cards_of_plan(vol):
    """返回 [(题序, 源卡相对路径)]（按 plan 的组内顺序）。"""
    p = os.path.join(O, 'vol_plan_%s.json' % vol)
    if not os.path.isfile(p):
        return None
    pl = json.load(io.open(p, encoding='utf-8'))
    out, n = [], 0
    for _group, items in pl:
        for it in items:
            n += 1
            out.append((n, it.get('path', '')))
    return out


def imgs_in_md(path):
    """统计 md 的图引用（**两种语法都算**）：`![[hash.jpg]]` 与 `![](images/hash.jpg)`。"""
    try:
        t = io.open(path, encoding='utf-8-sig').read()
    except Exception:
        return None
    return IMG.findall(t) + IMG_MD.findall(t)


def norm_hash(name):
    """归一化：取文件名中的 hash 前缀（wikilink 只写 hash，md 语法带 images/ 前缀）。"""
    b = os.path.basename(name)
    m = re.match(r'^[0-9a-f]{8,}', b)
    return m.group(0)[:12] if m else b


def content_key(name):
    """★ 以**图片内容 sha256** 作 key —— 库内存在「同图不同名」（如 f86442ad 与 ce154830 内容一致，
    系历史遗留命名）⇒ 只比文件名会误报「缺图」。找不到文件则退化为文件名前缀。"""
    b = os.path.basename(name)
    for d in IMG_DIRS:
        p = os.path.join(d, b)
        if os.path.isfile(p):
            try:
                return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
            except Exception:
                break
    return norm_hash(name)


def vol_images(vol):
    """卷内逐题图引用 —— **学生版与答案版的并集**。

    理由：源卡通常「题面区 + 答案区」都有图；学生版只含题面区 ⇒ 只用学生版会比出大量假缺图
    （2026-10-14 实测：第 1 题源卡 11 张、学生版 8 张 ⇒ 假报「缺 6」，实为答案区的图在答案版里）。
    """
    merged, tags = {}, []
    for tag in ['学生版', '答案版']:
        p = os.path.join(ROOT, '04-题库', '初赛模拟卷%s（非有机·%s）.md' % (vol, tag))
        if not os.path.isfile(p):
            continue
        tags.append(tag)
        d = io.open(p, encoding='utf-8-sig').read()
        parts = re.split(r'(?m)^### 第 (\d+) 题', d)
        for i in range(1, len(parts), 2):
            n = int(parts[i])
            merged.setdefault(n, [])
            merged[n].extend(imgs_in_md_text(parts[i + 1]))
    if not merged:
        return None, None, None
    return merged, '＋'.join(tags), None


def imgs_in_md_text(t):
    return IMG.findall(t) + IMG_MD.findall(t)


def check(vol):
    cards = cards_of_plan(vol)
    if cards is None:
        print('[%s] 无 plan 文件，跳过' % vol)
        return 0
    volmap, tag, vpath = vol_images(vol)
    print('=' * 92)
    print('卷 %s —— 图源覆盖核验（卷内取自 %s；两种图语法都统计）' % (vol, tag))
    print('-' * 92)
    print('%-4s %-8s %-8s %-6s %s' % ('题', '源卡图', '卷内图', '缺', '缺失的图（hash 前12）'))
    miss = 0
    tot_src = tot_vol = 0
    for n, cpath in cards:
        cp = os.path.join(ROOT, cpath)
        ci = imgs_in_md(cp)
        vs = volmap.get(n, []) if volmap else []
        if ci is None:
            print('%-4d %-8s %-8d %-6s ⚠ 源卡缺失：%s' % (n, '?', len(vs), '', cpath[:50]))
            continue
        src_h = [content_key(x) for x in ci]
        vol_h = {content_key(x) for x in vs}
        missing = [h for h in src_h if h not in vol_h]
        # 去重保序
        seen, uniq = set(), []
        for h in missing:
            if h not in seen:
                seen.add(h); uniq.append(h)
        tot_src += len(set(src_h)); tot_vol += len({content_key(x) for x in vs})
        if uniq:
            mark = '🔴 %d' % len(uniq); miss += 1
            print('%-4d %-8d %-8d %-6s %s  ｜ %s'
                  % (n, len(src_h), len(vs), len(uniq), ' '.join(h[:10] for h in uniq[:4]), os.path.basename(cpath)[:36]))
        elif len({content_key(x) for x in vs}) > len(set(src_h)):
            print('%-4d %-8d %-8d %-6s 🟠 卷内多 %d 张 ｜ %s'
                  % (n, len(src_h), len(vs), 0, len({content_key(x) for x in vs}) - len(set(src_h)), os.path.basename(cpath)[:36]))
    print('-' * 92)
    print('合计：源卡图 %d ｜ 卷内图 %d ｜ 缺图题 %d' % (tot_src, tot_vol, miss))
    print('VERDICT:', 'FAIL' if miss else 'PASS')
    return 1 if (miss and STRICT) else 0


rc = 0
if ALL:
    for p in sorted(glob.glob(os.path.join(O, 'vol_plan_*.json'))):
        v = os.path.basename(p)[len('vol_plan_'):-len('.json')]
        rc |= check(v)
else:
    if not VOL:
        print('用法：verify_fig_coverage.py --vol <卷> [--strict] ｜ --all'); sys.exit(2)
    rc = check(VOL)
sys.exit(rc)
