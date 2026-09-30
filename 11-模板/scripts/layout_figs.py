#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""layout_figs.py —— 把 Markdown 中「多图组」并排成表格（试卷 / 讲义通用）

背景（2026-09-30 用户要求）
    多图题的图在 docx 里逐张独占一行，一页只放几张图。改用「表格并排」。

范式（经 pandoc 管线实测）
    表头行 = 标号（①② / A B C / σ π / P2 …），数量不匹配时留空；
    正文行 = 图；图后短注释（如横轴 n）另起一行放图下方。

    | ① | ② |
    | :---: | :---: |
    | ![[a.jpg\\|250]] | ![[b.jpg\\|250]] |

    ⚠️ 表格单元格内的 `|` 必须转义成 `\\|`，否则被当列分隔符。
    build-all-handout-docx.py 的 _docx_image_repl 已在 2026-09-30 支持该转义。
    ⚠️ 不要用 `<br>` 把标号塞进图同一格——实测 pandoc 不换行，文字会压在图里。

标签驱动的子组切分（2026-09-30 追加，解决「示例/记号/投影」这类结构）
    「以冒号结尾的短行」（如 `示例:`、`记号：`、`投影：`）旧版含中文被判为正文 ⇒
    **打断**图组，于是「记号：」下面两张图各自独占一行（实测 8-1-2 就是这样乱的）。
    现改为：不打断，且作**子组边界**，标签升级成该子组的表格表头：

        | 示例: |
        | :---: |
        | ![[a.jpg\\|250]] |

        | 记号： |  |
        | :---: | :---: |
        | ![[b.jpg\\|250]] | ![[c.jpg\\|250]] |
        | $4^{6}3^{8}$ |  |

    短公式行（`$…$`，≤30 字）作为「图的注释」并入其下方一行
    （常是图内标签被 OCR 抓到外层）。⛔ 触发门槛：组内标签 **≥2 个**才切分，
    单个标签（如「注意：」）不触发，避免误伤正文。
    ⚠️ 标签与图进同一张表 ⇒ Word 不会把「标签留在上页、图推到下页」。
    ⚠️ 逐轮迭代时**不要 v1/v2 混用**（v1 已表格化的组，v2 接管不了，其标签会被丢）
    ⇒ 改规则后应从**未排版的原始 md** 重新跑一遍。

列数与图宽（实测：A4 正文宽 ≈ 449pt）
    2 图 → 2 列 / 250px；3 图 → 3 列 / 175px；4 图 → 2 列 ×2 行；
    5 图及以上 → 3 列多行 / 175px；标签子组内单图 → 1 列 / 250px。
    （3 列 ×180px 实测右边界 526pt，已顶到页边距；175px 留余量。）
    宽度再按 min(目标, max(原图宽,120)) 收敛 —— **小图不放大**（曾遇 90px 的图
    硬拉 175px，放大近 2 倍发糊）。

用法
    python layout_figs.py <file.md> [more.md ...]        # dry-run
    python layout_figs.py --go <file.md> [...]           # 写盘
"""
from __future__ import annotations
import os
import re
import sys

try:
    from PIL import Image
except Exception:      # pragma: no cover
    Image = None

IMG = re.compile(r'^[ \t]*!\[\[([0-9a-fA-F]{64}\.[A-Za-z0-9]+)(?:\|[^\]]*)?\]\][ \t]*$')
TBL = re.compile(r'^[ \t]*\|')
HEAD = re.compile(r'^[ \t]*#{1,6}[ \t]')


def is_img(l: str) -> bool:
    return bool(IMG.match(l))


def is_blank(l: str) -> bool:
    return not l.strip()


def is_short(l: str) -> bool:
    """短 token 行（标号 / 横轴标签等）。排除：表格行、标题、公式、列表、正文。"""
    s = l.strip()
    if not s or len(s) > 8:
        return False
    if s[0] in '|#$>*-!+=':
        return False
    if re.search(r'[\u4e00-\u9fff\uff00-\uffef]', s):   # 含中文 / 全角标点
        return False
    if re.search(r'[。，、；：？！]', s):
        return False
    return True


def collect(lines, start):
    """从图行 start 起收集整组；返回 (img_names, toks, end, npre)。

    toks   组内所有短 token，按出现顺序（图前、图间的都算）。
    npre   其中「位于第一张图之前」的 token 个数。它们在主循环里**已经写进
           out** 了，必须由调用方删除，否则会贴在表格前面 ⇒ pandoc 认为表格
           行是段落延续，整张表格退化为字面文本（2026-09-30 实测踩坑）。
    """
    imgs = [IMG.match(lines[start]).group(1)]
    toks = []
    k = start - 1
    tmp = []
    while k >= 0:
        if is_blank(lines[k]):
            k -= 1
            continue
        if is_short(lines[k]):
            tmp.append(lines[k].strip())
            k -= 1
            continue
        break
    toks.extend(reversed(tmp))
    npre = len(tmp)
    k = start + 1
    while k < len(lines):
        if is_blank(lines[k]):
            k += 1
            continue
        if is_short(lines[k]):
            toks.append(lines[k].strip())
            k += 1
            continue
        if is_img(lines[k]):
            imgs.append(IMG.match(lines[k]).group(1))
            k += 1
            continue
        break
    return imgs, toks, k, npre


def drop_trailing_tokens(out, cnt, pred=None):
    """从 out 尾部删掉 cnt 个「前置 token」（连同其间空行），并保证尾部留一个空行。

    pred 默认 is_short；标签驱动路径要传 _tok_or_label（标签含中文、is_short 不认）。
    """
    pred = pred or is_short
    removed = 0
    while removed < cnt and out:
        s = out[-1]
        if pred(s):
            out.pop()
            removed += 1
        elif not s.strip():
            out.pop()
        else:
            break
    if out and out[-1].strip():
        out.append('')
    return out


def split_toks(toks, n):
    """按数量关系把 token 拆成 (表头, 注释)。"""
    if len(toks) == n:
        return toks, []
    if len(toks) == 2 * n:
        return toks[0::2], toks[1::2]
    if n - 1 <= len(toks) <= n:
        return toks + [''] * (n - len(toks)), []
    return [''] * n, []


def plan(n):
    if n == 2:
        return 2, 250
    if n == 3:
        return 3, 175
    if n == 4:
        return 2, 250
    return 3, 175


_W_CACHE: dict = {}


def img_width(name):
    """读原图像素宽（找不到返回 None）。"""
    if name in _W_CACHE:
        return _W_CACHE[name]
    w = None
    if Image is not None:
        for d in ('媒体仓库', '.'):
            p = os.path.join(d, name)
            if os.path.exists(p):
                try:
                    w = Image.open(p).size[0]
                except Exception:
                    w = None
                break
    _W_CACHE[name] = w
    return w


def fit_w(name, target):
    """目标宽度，但**不放大**（原图更窄时按原图）。

    小图强行拉到 target 会糊（实测 5-1 的 P2 单元只有 90px 宽，拉到 175px
    放大近 2 倍）。下限 120px 兜底，免得过小看不清。
    """
    ow = img_width(name)
    if not ow:
        return target
    return min(target, max(ow, 120))


def render_block(imgs, toks):
    n = len(imgs)
    cols, w = plan(n)
    heads, notes = split_toks(toks, n)
    out = []
    for r0 in range(0, n, cols):
        row = imgs[r0:r0 + cols]
        # 断言：必须是真正的文件名（64 hex + 扩展名），防止把行号/序号写进去
        for x in row:
            assert re.fullmatch(r'[0-9a-fA-F]{64}\.[A-Za-z0-9]+', x), \
                '非法图名（疑似行号）: %r' % x
        k = len(row)
        h = heads[r0:r0 + cols] + [''] * (cols - k)
        nt = notes[r0:r0 + cols] + [''] * (cols - k) if notes else None
        out.append('| ' + ' | '.join(h) + ' |')
        out.append('| ' + ' | '.join([':---:'] * cols) + ' |')
        out.append('| ' + ' | '.join('![[%s\\|%d]]' % (x, fit_w(x, w))
                                      for x in row) + ' |')
        if nt and any(nt):
            out.append('| ' + ' | '.join(nt) + ' |')
        out.append('')
    return out


LABEL_RE = re.compile(r'[：:]$')
NOTE_RE = re.compile(r'^\$[^$]{1,30}\$$')


def is_label(l: str) -> bool:
    """标签行：以冒号结尾的短行（「示例:」「记号：」「投影：」）。

    这类行在旧逻辑里含中文 ⇒ 被判为正文 ⇒ **打断**图组，于是「记号：」下面的
    两张图各自独占一行（实测 8-1-2 就是这样乱掉的）。现改为：不打断，且作为
    **子组边界**，标签本身升级成该子组的表格表头。
    """
    s = l.strip()
    if not s or len(s) > 10:
        return False
    if s[0] in '|#$>*-!+=':
        return False
    return bool(LABEL_RE.search(s))


def is_note(l: str) -> bool:
    """短公式行（如 `$4^{6}3^{8}$`）——常是图内标签被 OCR 抓到外层，作图的注释。"""
    return bool(NOTE_RE.match(l.strip()))


def _tok_or_label(l: str) -> bool:
    return is_short(l) or is_label(l)


def collect_v2(lines, start):
    """标签驱动的子组收集。返回 (segments, end, npre)；标签 <2 时 segments=None。

    segments = [(label, [img…], [note|None…]), …]
    """
    seq = []
    k = start - 1
    pre = []
    while k >= 0:
        if is_blank(lines[k]):
            k -= 1
            continue
        if is_label(lines[k]):
            pre.append(('label', lines[k].strip()))
            break
        if is_short(lines[k]) or is_note(lines[k]):
            k -= 1
            continue
        break
    seq.extend(reversed(pre))
    seq.append(('img', IMG.match(lines[start]).group(1)))
    k = start + 1
    while k < len(lines):
        if is_blank(lines[k]):
            k += 1
            continue
        if is_label(lines[k]):
            seq.append(('label', lines[k].strip()))
            k += 1
            continue
        if is_img(lines[k]):
            seq.append(('img', IMG.match(lines[k]).group(1)))
            k += 1
            continue
        if is_note(lines[k]) or is_short(lines[k]):
            seq.append(('note', lines[k].strip()))
            k += 1
            continue
        break
    if sum(1 for t, _ in seq if t == 'label') < 2:
        return None, start, 0
    segs, cur = [], [None, [], []]
    for t, x in seq:
        if t == 'label':
            if cur[1] or cur[0]:
                segs.append(cur)
            cur = [x, [], []]
        elif t == 'img':
            cur[1].append(x)
            cur[2].append(None)
        else:
            if cur[1]:
                cur[2][-1] = ((cur[2][-1] + ' ' + x) if cur[2][-1] else x)
    if cur[1] or cur[0]:
        segs.append(cur)
    return segs, k, len(pre)


def render_segments(segs):
    out = []
    for label, imgs, notes in segs:
        if not imgs:
            # 只有标签、没有图（例如该组的图已被前一轮排成表格）——
            # 此时标签必须保留成普通段落，⛔ 不能丢（丢过「投影：」）。
            if label:
                out.append(label)
                out.append('')
            continue
        n = len(imgs)
        cols, w = (1, 250) if n == 1 else plan(n)
        for x in imgs:
            assert re.fullmatch(r'[0-9a-fA-F]{64}\.[A-Za-z0-9]+', x), x
        head = [label or ''] + [''] * (cols - 1)
        out.append('| ' + ' | '.join(head) + ' |')
        out.append('| ' + ' | '.join([':---:'] * cols) + ' |')
        for r0 in range(0, n, cols):
            row = imgs[r0:r0 + cols]
            k = len(row)
            out.append('| ' + ' | '.join(
                ['![[%s\\|%d]]' % (x, fit_w(x, w)) for x in row]
                + [''] * (cols - k)) + ' |')
            nts = [(notes[r0 + i] or '') if r0 + i < n else '' for i in range(cols)]
            if any(nts):
                out.append('| ' + ' | '.join(nts) + ' |')
        out.append('')
    return out


def process(text):
    lines = text.split('\n')
    out, i, nblocks, nfigs = [], 0, 0, 0
    while i < len(lines):
        if is_img(lines[i]) and not (out and TBL.match(out[-1] or '')):
            segs, end2, npre2 = collect_v2(lines, i)
            if segs:
                drop_trailing_tokens(out, npre2, pred=_tok_or_label)
                out.extend(render_segments(segs))
                nblocks += len(segs)
                nfigs += sum(len(s[1]) for s in segs)
                i = end2
                continue
            imgs, toks, end, npre = collect(lines, i)
            if len(imgs) >= 2:
                drop_trailing_tokens(out, npre)
                out.extend(render_block(imgs, toks))
                nblocks += 1
                nfigs += len(imgs)
                i = end
                continue
        out.append(lines[i])
        i += 1
    return '\n'.join(out), nblocks, nfigs


def selfcheck(new, path):
    """断言：每个 pipe table 的「表头行」之前必须是空行（或文件开头）。

    pandoc 只有在表格前有空行时才把它当表格；否则整张表退化成字面文本
    （2026-09-30 实测踩坑：标号 `①` 贴在表格前 → 渲染出 `① | ① | ② |…`）。
    """
    lines = new.split('\n')
    bad = []
    for k, l in enumerate(lines):
        if re.match(r'^[ \t]*\|[ \t]*:?-{2,}[ \t]*\|', l) and k >= 2:
            head = lines[k - 1]
            prev = lines[k - 2]
            if not head.lstrip().startswith('|') or prev.strip():
                bad.append((k + 1, prev[:40], head[:40]))
    return bad


def main():
    args = sys.argv[1:]
    go = '--go' in args
    files = [a for a in args if a != '--go']
    if not files:
        print(__doc__)
        return 1
    for p in files:
        raw = open(p, encoding='utf-8').read()
        new, nb, nf = process(raw)
        if new == raw:
            print('  跳过（无变更）:', p)
            continue
        bad = selfcheck(new, p)
        print('  %s → %d 个图组 / %d 图并排；表格前缺空行 = %d'
              % (p.split('/')[-1], nb, nf, len(bad)))
        for b in bad[:5]:
            print('      ⚠️ 行%d 前两行: %r / %r' % b)
        if go:
            if bad:
                print('      ⛔ 自检失败，拒绝写盘:', p)
                continue
            open(p, 'w', encoding='utf-8', newline='\n').write(new)
    print('DONE', 'GO' if go else 'dry')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
