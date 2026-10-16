"""卷 md 管道表结构审计（可复用）。

判据（机器可判）：
  A. 「两表合并」——同一个以 `|` 开头的连续块里，出现 **>1 条分隔行**（`|:--:|...|`）
     ⇒ pandoc 只会认第一条分隔行定列数，后续表的列会被截断 ⇒ 丢内容（含丢图）。
  B. 「行格数不符」——块内任一行的单元格数 != 分隔行列数 ⇒ 该行被截断/补齐。
  C. 「表内图清单」——逐块列出图 hash，便于与 deliver docx media 对账。

用法:
  python -X utf8 .workbuddy/tmp/opt_pipe/pipe_tbl_audit.py <md 路径> [...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SEPCELL = re.compile(r":?-{1,}:?")
IMG = re.compile(r"!\[\[([0-9a-f]{8})[0-9a-f]*\.(?:jpg|jpeg|png)\]\]")


def split_cells(line: str) -> list[str] | None:
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    # ⛔ 只按 **未转义** 的 `|` 切分（`\|` 是单元格内的字面竖线，pandoc 不当分隔符）
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)[1:-1]]


def is_sep(line: str) -> bool:
    """分隔行 = 每格都形如 :?-+:?（⛔ 不可把 `|` 放进字符类——空行 `|  |  |` 会被误判）。"""
    cs = split_cells(line)
    return bool(cs) and all(SEPCELL.fullmatch(c) for c in cs)


def cells(line: str) -> int:
    cs = split_cells(line)
    return -1 if cs is None else len(cs)


def audit(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        lines = fh.read().replace("\r\n", "\n").split("\n")
    out: list[dict] = []
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            block = lines[i:j]
            seps = [k for k, l in enumerate(block) if is_sep(l)]
            imgs = IMG.findall("\n".join(block))
            if seps:
                ncol = cells(block[seps[0]])
                bad = [
                    (i + k + 1, cells(l))
                    for k, l in enumerate(block)
                    if not is_sep(l) and cells(l) != ncol
                ]
                out.append(
                    {
                        "start": i + 1,
                        "end": j,
                        "nrows": len(block),
                        "ncol": ncol,
                        "nsep": len(seps),
                        "bad_rows": bad,
                        "imgs": imgs,
                    }
                )
            i = j
        else:
            i += 1
    return out


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    total_bad = 0
    for a in argv[1:]:
        p = Path(a)
        rep = audit(p)
        merged = [b for b in rep if b["nsep"] > 1]
        ragged = [b for b in rep if b["bad_rows"]]
        print(f"=== {p.name}｜表块 {len(rep)}｜两表合并 {len(merged)}｜行格数不符 {len(ragged)}")
        for b in merged:
            print(
                f"  [两表合并] L{b['start']}-{b['end']} 分隔行数={b['nsep']} 列={b['ncol']} 图={len(b['imgs'])}"
            )
        for b in ragged:
            print(
                f"  [行格数不符] L{b['start']}-{b['end']} 列={b['ncol']} 异常行={b['bad_rows']} 图={len(b['imgs'])}"
            )
        total_bad += len(merged) + len(ragged)
    print(f"\n合计异常表块 = {total_bad}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
