#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把「作图」档拆成两类，看各自的规模：
  A 画结构 —— 「画出 A 的结构式/构型/结构简式」，本质是推断，画只是表达方式
  B 真作图 —— 装置图 / 相图 / 能级图 / 轨道示意图 / 曲线 等
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import infer_question_type as Q  # noqa: E402
import yaml  # noqa: E402

import re

DRAW_STRUCT = re.compile(
    r"画(?:出|了)?[^。！？\n]{0,14}?(?:结构(?:式|简式)?|构型|构象|立体结构|空间结构|几何构型)"
)
DRAW_REAL = re.compile(
    r"画(?:出|了)?[^。！？\n]{0,14}?(?:装置图|相图|能级图|轨道[示图]|示意[图]?|曲线|图像|图表|流程图|循环图|"
    r"电子构型图|分子轨道图|能级|滴定曲线|标准曲线|工作曲线|循环伏安|谱图|结构图|点阵|晶胞图)"
)


def main() -> None:
    files: list[Path] = []
    for d in Q.TARGET_DIRS:
        files.extend(sorted((Q.VAULT / d).rglob("*.md")))
    files = [p for p in files if p.name not in Q.V.EXCLUDE_FILE_NAMES]

    n_struct = n_real = n_both = n_other = 0
    ex_struct, ex_real = [], []

    for p in files:
        text = Q.read_raw(p)
        fs, fe, lines = Q.split_fm(text)
        if fs is None:
            continue
        try:
            fm = yaml.safe_load("\n".join(lines[fs + 1:fe])) or {}
        except Exception:
            continue
        if not isinstance(fm, dict) or str(fm.get("type", "")).strip() != "题目":
            continue
        if fm.get("question_type") is not None:
            continue
        stem = Q.stem_of(text)
        tier, types, evs = Q.infer(stem)
        if "作图" not in types:
            continue
        if tier != "T1" and Q.is_multi(stem):
            m_t, m_ty, _ = Q.infer_multi(stem)
            if not m_ty or "作图" not in m_ty:
                continue
        a = bool(DRAW_STRUCT.search(stem))
        b = bool(DRAW_REAL.search(stem))
        if a and b:
            n_both += 1
        elif a:
            n_struct += 1
            if len(ex_struct) < 8:
                ex_struct.append(p.name)
        elif b:
            n_real += 1
            if len(ex_real) < 8:
                ex_real.append(p.name)
        else:
            n_other += 1

    print(f"作图档共 {n_struct + n_real + n_both + n_other} 条")
    print(f"  A 画结构（推断的另一种表达）   {n_struct}")
    print(f"  B 真作图（装置/相图/能级/曲线） {n_real}")
    print(f"  两者都有                       {n_both}")
    print(f"  只有泛化「画出…图」未细分       {n_other}")
    print("\nA 例：")
    for x in ex_struct:
        print("   ", x)
    print("B 例：")
    for x in ex_real:
        print("   ", x)


if __name__ == "__main__":
    main()
