"""修复 Word 转换日志中剩余的少量源文件公式数据错误。

用法:
    python -X utf8 11-模板/scripts/fix_remaining_word_math.py
"""

from __future__ import annotations

from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = VAULT_ROOT / "04-题库"

FIXES = {
    "教材习题/结构化学基础/题-099-结构化学基础-对称性-习题4.17.md": [
        (r"\begin{array}{c}H\H\end{array}", r"\begin{array}{c}H\\H\end{array}"),
    ],
    "教材习题/无机化学例题与习题/Ch10-氧化还原反应/例题/例10.10-电势-pH图.md": [
        (r"\E&", r"\\&"),
    ],
    "教材习题/中级无机化学/题-013-中级无机化学-配合物反应机理-习题4.4.md": [
        (r"\mathrm{Pt(NH_3)_2(tu)_2^{2+}$", r"\mathrm{Pt(NH_3)_2(tu)_2^{2+}}$"),
    ],
    "教材习题/无机化学例题与习题/Ch13-硼族元素/习题/Ch13-简答与计算题.md": [
        (
            r"\mathrm{(CH_3)_3N + BCl_3 = (CH_3)_3N \rightarrow BCl_3$",
            r"\mathrm{(CH_3)_3N + BCl_3 = (CH_3)_3N \rightarrow BCl_3}$",
        ),
    ],
    "教材习题/赵鑫光/题-赵鑫光-晶体-习33.md": [
        (r'" \mathrm{NiO}"', r"\mathrm{NiO}"),
    ],
    "教材习题/赵鑫光/题-赵鑫光-晶体-例15.md": [
        (r'" \mathrm{NiO}"', r"\mathrm{NiO}"),
    ],
}

REWRITE_14_23 = r"""\begin{aligned}
&\mathrm{Cu^{2+} + e^- \rightleftharpoons Cu^+} \qquad E^{\ominus}(\mathrm{Cu^{2+}/Cu^+}) = 0.153\ \mathrm{V}\\
&\mathrm{Cu(NH_3)_4^{2+} + e^- \rightleftharpoons Cu(NH_3)_2^+ + 2NH_3} \qquad E^{\ominus}(\mathrm{Cu(NH_3)_4^{2+}/Cu(NH_3)_2^+}) = ?\\
&E^{\ominus}(\mathrm{Cu(NH_3)_4^{2+}/Cu(NH_3)_2^+}) = E^{\ominus}(\mathrm{Cu^{2+}/Cu^+}) + 0.0592\ \mathrm{V} \times \lg \frac{[\mathrm{Cu^{2+}}]}{[\mathrm{Cu^+}]}\\
&E_1^{\ominus} = 0.153\ \mathrm{V} + 0.0592\ \mathrm{V} \times \lg \frac{K_{\text{稳}}(\mathrm{Cu(NH_3)_2^+})}{K_{\text{稳}}(\mathrm{Cu(NH_3)_2^{2+}})}\\
&\qquad = 0.153\ \mathrm{V} + 0.0592\ \mathrm{V} \times \lg \frac{7.2 \times 10^{10}}{2.1 \times 10^{13}}\\
&\qquad = 0.007\ \mathrm{V}\\
&\mathrm{Cu^+ + e^- \rightleftharpoons Cu} \qquad E^{\ominus}(\mathrm{Cu^+/Cu}) = 0.521\ \mathrm{V}\\
&\mathrm{Cu(NH_3)_2^+ + e^- \rightleftharpoons Cu + 2NH_3} \qquad E^{\ominus}(\mathrm{Cu(NH_3)_2^+/Cu}) = ?\\
&\qquad E^{\ominus}(\mathrm{Cu(NH_3)_2^+/Cu}) = E^{\ominus}(\mathrm{Cu^+/Cu}) + 0.0592\ \mathrm{V} \times \lg[\mathrm{Cu^+}]\\
&\qquad E_2^{\ominus} = 0.521\ \mathrm{V} + 0.0592\ \mathrm{V} \times \lg \frac{1}{7.2 \times 10^{10}} = -0.121\ \mathrm{V}
\end{aligned}"""


def main() -> int:
    for rel, pairs in FIXES.items():
        path = SRC_ROOT / rel
        if not path.exists():
            print(f"missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            if old not in text:
                print(f"not found: {rel}: {old!r}")
                continue
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8", newline="")

    p14 = SRC_ROOT / "化学原理/Ch14-配位化合物/14-23.md"
    if p14.exists():
        text = p14.read_text(encoding="utf-8")
        marker = r"\begin{array}{r l} & (2) \left\{"
        lines = text.splitlines(keepends=True)
        for i, line in enumerate(lines):
            if marker in line and "end{array}" in line:
                lines[i] = REWRITE_14_23 + "\n"
                break
        p14.write_text("".join(lines), encoding="utf-8", newline="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
