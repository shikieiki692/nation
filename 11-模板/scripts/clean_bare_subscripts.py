"""把 Phase 4 剩余的裸下标转成数学模式，只改 `04-题库/` 源文件。

替换只在 `$...$` / `$$...$$` 之外进行，避免把已进入公式的下标二次包裹。

用法:
    python -X utf8 11-模板/scripts/clean_bare_subscripts.py
"""

from __future__ import annotations

import re
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = VAULT_ROOT / "04-题库"

FIXES: dict[str, list[tuple[str, str]]] = {
    "教材习题/上海中学竞赛课程/题-055-8-上海中学-化学平衡-习题8.md": [
        ("P_H₂O", "$P_\\mathrm{H_2O}$"),
        ("P_MeOH", "$P_\\mathrm{MeOH}$"),
    ],
    "教材习题/上海中学竞赛课程/题-055-上海中学-化学平衡-习题1.md": [
        ("P_H₂O", "$P_\\mathrm{H_2O}$"),
        ("P_MeOH", "$P_\\mathrm{MeOH}$"),
    ],
    "教材习题/上海中学竞赛课程/题-056-上海中学-化学动力学基础-习题1.md": [
        ("dc_A", "$dc_\\mathrm{A}$"),
        ("kc_A", "$kc_\\mathrm{A}$"),
        ("dp_B", "$dp_\\mathrm{B}$"),
        ("c_B,0", "$c_\\mathrm{B,0}$"),
        ("c_A,0", "$c_\\mathrm{A,0}$"),
        ("p_A", "$p_\\mathrm{A}$"),
        ("p_B", "$p_\\mathrm{B}$"),
        ("c_B", "$c_\\mathrm{B}$"),
        ("c_A", "$c_\\mathrm{A}$"),
    ],
    "真题/第25届初赛/分析化学/题-025-4-3-Co氧化数与氧缺陷计算.md": [
        ("S_Co", "$S_\\mathrm{Co}$"),
    ],
    "教材习题/Clayden/题-577-Clayden-Ch31-P8-二维到三维立体化学.md": [
        ("J_AB", "$J_\\mathrm{AB}$"),
        ("J_AX", "$J_\\mathrm{AX}$"),
        ("J_BX", "$J_\\mathrm{BX}$"),
    ],
    "有机化学/有机结构基础与电子效应/题-有机-结构-共轭稳定化能计算.md": [
        ("ΔH_hyd", "$\\Delta H_\\mathrm{hyd}$"),
    ],
    "教材习题/Clayden/题-509-Clayden-Ch35-P9-不稳定阴离子异构化+ABX-NMR.md": [
        ("J_AB", "$J_\\mathrm{AB}$"),
    ],
    "教材习题/Clayden/题-654-Clayden-Ch39-P14-逆向思维：你需要什么证据.md": [
        ("k_H", "$k_\\mathrm{H}$"),
        ("k_D", "$k_\\mathrm{D}$"),
    ],
    "教材习题/Clayden/题-651-Clayden-Ch39-P11-对比同位素效应详细机理分析.md": [
        ("k_H", "$k_\\mathrm{H}$"),
        ("k_D", "$k_\\mathrm{D}$"),
    ],
    "有机化学/活性中间体与反应机理/题-有机-中间体-Hammett方程与反应机理判断.md": [
        ("k_X", "$k_\\mathrm{X}$"),
        ("k_H", "$k_\\mathrm{H}$"),
    ],
    "教材习题/Clayden/题-473-Clayden-Ch37-P9-自由基反应+构象和立体化学复习.md": [
        ("S_N2", "$S_\\mathrm{N}2$"),
    ],
    "教材习题/Clayden/题-586-Clayden-Ch32-P3-环中立体化学控制探索.md": [
        ("S_N2", "$S_\\mathrm{N}2$"),
    ],
    "教材习题/Clayden/题-603-Clayden-Ch33-P8-立体电子控制Felkin-Anh分析.md": [
        ("S_N2", "$S_\\mathrm{N}2$"),
    ],
    "有机化学/芳香反应/题-XES-043-芳香胺制备机理.md": [
        ("S_N2", "$S_\\mathrm{N}2$"),
    ],
    "教材习题/Clayden/题-505-Clayden-Ch35-P5-三环羟基酮retro-DA+电环化开环.md": [
        ("S_N2", "$S_\\mathrm{N}2$"),
    ],
    "教材习题/赵鑫光/题-赵鑫光-原子-例5.md": [
        ("m_e", "$m_\\mathrm{e}$"),
    ],
    "教材习题/上海中学竞赛课程/题-049-13-上海中学-离子键与离子晶体-习题13.md": [
        ("M_A", "$M_\\mathrm{A}$"),
    ],
    "教材习题/上海中学竞赛课程/题-049-上海中学-离子键与离子晶体-习题1.md": [
        ("M_A", "$M_\\mathrm{A}$"),
    ],
    "教材习题/上海中学竞赛课程/题-049-7-上海中学-离子键与离子晶体-习题7.md": [
        ("ρ_LiCl", "$\\rho_\\mathrm{LiCl}$"),
        ("ρ_KCl", "$\\rho_\\mathrm{KCl}$"),
        ("M_LiCl", "$M_\\mathrm{LiCl}$"),
        ("M_KCl", "$M_\\mathrm{KCl}$"),
        ("r_Cl", "$r_\\mathrm{Cl}$"),
        ("r_Li", "$r_\\mathrm{Li}$"),
        ("r_K", "$r_\\mathrm{K}$"),
    ],
    "教材习题/上海中学竞赛课程/题-050-2-上海中学-其他类型晶体-习题2.md": [
        ("d_B-P", "$d_\\mathrm{B-P}$"),
    ],
    "教材习题/上海中学竞赛课程/题-050-上海中学-其他类型晶体-习题1.md": [
        ("d_B-P", "$d_\\mathrm{B-P}$"),
    ],
    "教材习题/中级无机化学/题-025-中级无机化学-配位催化反应-习题8.2.md": [
        ("S_N2", "$S_\\mathrm{N}2$"),
    ],
    "教材习题/无机化学第6版Weller/Ch20/题-WCh20.23-C4v对称性d轨道与MO.md": [
        ("p_x", "$p_x$"),
        ("p_y", "$p_y$"),
    ],
    "教材习题/无机化学第6版Weller/Ch20/题-WCh20.24-MnO4电荷转移与DeltaT.md": [
        ("Δ_T", "$\\Delta_T$"),
    ],
    "教材习题/中级无机化学/题-009-中级无机化学-配位场理论-习题3.2.md": [
        ("Δ_t", "$\\Delta_t$"),
        ("Δ_o", "$\\Delta_o$"),
        ("T_d", "$T_d$"),
    ],
    "教材习题/中级无机化学/题-001-中级无机化学-群论-习题1.4.md": [
        ("T_d", "$T_d$"),
        ("O_h", "$O_h$"),
    ],
    "教材习题/中级无机化学/题-002-中级无机化学-群论-习题1.11.md": [
        ("O_h", "$O_h$"),
        ("e_g", "$e_g$"),
    ],
    "教材习题/中级无机化学/题-003-中级无机化学-群论-习题1.13.md": [
        ("R_x", "$R_x$"),
        ("R_y", "$R_y$"),
        ("R_z", "$R_z$"),
    ],
    "教材习题/中级无机化学/题-037-中级无机化学-无机固体化学-习题10.3.md": [
        ("H_n", "$H_n$"),
    ],
    "教材习题/中级无机化学/题-039-中级无机化学-无机固体化学-习题10.6.md": [
        ("Li_Ni'", "$\\mathrm{Li_{Ni}^{\\prime}}$"),
    ],
    "教材习题/无机化学第6版Weller/Ch18/题-WCh18.10-XeOF3+的129Xe-NMR谱.md": [
        ("C_s", "$C_s$"),
    ],
}


def replace_outside_math(line: str, old: str, new: str) -> str:
    parts = re.split(r"(\$\$[^$]*\$\$|\$[^$\n]*\$)", line)
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace(old, new)
    return "".join(parts)


def main() -> int:
    total = 0
    files = 0
    missing: list[str] = []
    for rel, pairs in FIXES.items():
        path = SRC_ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        text = path.read_text(encoding="utf-8")
        new_text = text
        file_count = 0
        for old, new in pairs:
            before = new_text
            new_text = "\n".join(
                replace_outside_math(line, old, new) for line in new_text.splitlines()
            )
            count = sum(
                1 for a, b in zip(before.splitlines(), new_text.splitlines()) if a != b
            )
            if count == 0:
                missing.append(f"{rel}: {old}")
            file_count += count
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="")
            files += 1
            total += file_count
    print(f"replaced_lines={total} files={files}")
    if missing:
        print("missing:")
        for m in missing:
            print("  " + m)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
