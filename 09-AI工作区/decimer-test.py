#!/usr/bin/env python3
"""
DECIMER OCSR 测试脚本
目的：测试 DECIMER 对 vault 中有机化学图片的识别能力
输出：SMILES 结果 + RDKit 验证 + 渲染对比图 + 汇总报告
"""

import os
import sys
import json
import time
from pathlib import Path

# ── 路径配置 ──
VAULT_ROOT = Path(r"C:\Obsidion\妙妙屋")
MEDIA_DIR = VAULT_ROOT / "media"
OUTPUT_DIR = VAULT_ROOT / "09-AI工作区" / "decimer-test-results"

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── 测试图片清单 ──
# 分类选取不同复杂度的有机化学图片
TEST_IMAGES = [
    # (文件名, 预期类型, 难度等级)
    ("ethane-conformations.png", "简单分子", "★"),
    ("cyclohexane-chair.png", "构象分析", "★★"),
    ("chiral-center.png", "手性中心", "★★"),
    ("enantiomer.png", "对映异构", "★★"),
    ("amino-acid-zwitterions.png", "氨基酸", "★★"),
    ("carbocation-stability.png", "碳正离子", "★★★"),
    ("eas-mechanism.png", "反应机理", "★★★"),
    ("sn1-coordinate.png", "反应坐标", "★★★"),
    ("claisen-condensation.png", "缩合反应", "★★★"),
    ("michael-addition.png", "Michael加成", "★★★"),
    ("beckmann-mechanism.png", "重排反应", "★★★★"),
    ("wagner-meerwein.png", "重排机理", "★★★★"),
    ("suzuki-cycle.png", "催化循环", "★★★★"),
    ("aromatic-heterocycles.png", "杂环化合物", "★★★★"),
    ("birch-reduction.png", "还原反应", "★★★★"),
    ("radical-chain.png", "自由基链", "★★★"),
    ("peptide-bond.png", "肽键", "★★★"),
    ("polymer-unit.png", "聚合物", "★★★"),
    ("wh-correlation.png", "Woodward规则", "★★★★★"),
    ("ir-carbonyl-spectrum.png", "IR光谱", "★★★★"),
]


def run_decimer_test():
    """运行 DECIMER OCSR 测试"""
    print("=" * 70)
    print("  DECIMER OCSR 测试 — Vault 有机化学图片识别评估")
    print("=" * 70)
    print()

    # ── Step 1: 加载模型 ──
    print("[1/4] 加载 DECIMER 模型...")
    t0 = time.time()
    try:
        from decimer import predict_smiles_from_image
        model_load_time = time.time() - t0
        print(f"  ✅ 模型加载完成 ({model_load_time:.1f}s)")
    except Exception as e:
        print(f"  ❌ 模型加载失败: {e}")
        print("  尝试使用备选 API...")
        try:
            from decimer import DECIMER
            decimer = DECIMER()
            model_load_time = time.time() - t0
            print(f"  ✅ 备选模型加载完成 ({model_load_time:.1f}s)")
        except Exception as e2:
            print(f"  ❌ 备选也失败: {e2}")
            return

    # ── Step 2: 准备 RDKit ──
    print("[2/4] 初始化 RDKit 验证器...")
    try:
        from rdkit import Chem
        from rdkit.Chem import Draw, AllChem, Descriptors
        rdkit_available = True
        print("  ✅ RDKit 就绪")
    except ImportError:
        rdkit_available = False
        print("  ⚠️ RDKit 不可用，跳过验证环节")

    # ── Step 3: 逐图测试 ──
    print(f"[3/4] 开始测试 {len(TEST_IMAGES)} 张图片...")
    print("-" * 70)

    results = []
    success_count = 0
    rdkit_valid_count = 0

    for idx, (filename, expected_type, difficulty) in enumerate(TEST_IMAGES, 1):
        image_path = MEDIA_DIR / filename
        print(f"\n  [{idx:2d}/{len(TEST_IMAGES)}] {filename}")
        print(f"          类型: {expected_type} | 难度: {difficulty}")

        if not image_path.exists():
            print(f"          ⚠️ 文件不存在，跳过")
            results.append({
                "filename": filename,
                "status": "FILE_NOT_FOUND",
                "expected_type": expected_type,
                "difficulty": difficulty,
            })
            continue

        # 运行 DECIMER
        t1 = time.time()
        try:
            smiles = predict_smiles_from_image(str(image_path))
            inference_time = time.time() - t1
        except Exception as e:
            # 尝试备选 API
            try:
                smiles = decimer.predict_smiles_from_image(str(image_path))
                inference_time = time.time() - t1
            except Exception as e2:
                print(f"          ❌ DECIMER 失败: {e2}")
                results.append({
                    "filename": filename,
                    "status": "DECIMER_ERROR",
                    "error": str(e2),
                    "expected_type": expected_type,
                    "difficulty": difficulty,
                })
                continue

        if smiles and smiles.strip():
            success_count += 1
            print(f"          📝 SMILES: {smiles}")
            print(f"          ⏱️ 耗时: {inference_time:.2f}s")

            # RDKit 验证
            rdkit_valid = False
            mol_weight = None
            num_atoms = None
            num_bonds = None
            canonical_smiles = None

            if rdkit_available:
                try:
                    mol = Chem.MolFromSmiles(smiles)
                    if mol is not None:
                        rdkit_valid = True
                        rdkit_valid_count += 1
                        canonical_smiles = Chem.MolToSmiles(mol)
                        mol_weight = round(Descriptors.MolWt(mol), 2)
                        num_atoms = mol.GetNumAtoms()
                        num_bonds = mol.GetNumBonds()
                        print(f"          ✅ RDKit 验证通过")
                        print(f"          📊 分子量: {mol_weight} | 原子数: {num_atoms} | 键数: {num_bonds}")
                        if canonical_smiles != smiles:
                            print(f"          🔄 标准化: {canonical_smiles}")
                    else:
                        print(f"          ⚠️ RDKit 无法解析该 SMILES")
                except Exception as e:
                    print(f"          ⚠️ RDKit 验证出错: {e}")

            results.append({
                "filename": filename,
                "status": "SUCCESS",
                "smiles": smiles,
                "canonical_smiles": canonical_smiles,
                "rdkit_valid": rdkit_valid,
                "mol_weight": mol_weight,
                "num_atoms": num_atoms,
                "num_bonds": num_bonds,
                "inference_time": round(inference_time, 3),
                "expected_type": expected_type,
                "difficulty": difficulty,
            })
        else:
            print(f"          ❌ DECIMER 返回空结果")
            results.append({
                "filename": filename,
                "status": "EMPTY_RESULT",
                "expected_type": expected_type,
                "difficulty": difficulty,
            })

    # ── Step 4: 生成报告 ──
    print()
    print("=" * 70)
    print("[4/4] 生成测试报告...")
    print("=" * 70)

    total = len(TEST_IMAGES)
    empty = sum(1 for r in results if r["status"] == "EMPTY_RESULT")
    errors = sum(1 for r in results if r["status"] in ("FILE_NOT_FOUND", "DECIMER_ERROR"))

    report_lines = []
    report_lines.append("# DECIMER OCSR 测试报告")
    report_lines.append(f"\n**测试时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**DECIMER 版本**: 2.8.0")
    report_lines.append(f"**测试图片数**: {total}")
    report_lines.append("")

    report_lines.append("## 📊 总体统计")
    report_lines.append("")
    report_lines.append(f"| 指标 | 数值 |")
    report_lines.append(f"|:---|:---|")
    report_lines.append(f"| 总测试数 | {total} |")
    report_lines.append(f"| DECIMER 输出 SMILES | {success_count}/{total} ({success_count/total*100:.0f}%) |")
    report_lines.append(f"| RDKit 验证通过 | {rdkit_valid_count}/{success_count} (SMILES有效率) |" if success_count > 0 else "| RDKit 验证通过 | 0 (无有效SMILES) |")
    report_lines.append(f"| 空结果 | {empty} |")
    report_lines.append(f"| 错误 | {errors} |")
    report_lines.append("")

    report_lines.append("## 📋 详细结果")
    report_lines.append("")

    # 按难度分组
    by_difficulty = {}
    for r in results:
        d = r["difficulty"]
        if d not in by_difficulty:
            by_difficulty[d] = []
        by_difficulty[d].append(r)

    for diff in sorted(by_difficulty.keys()):
        items = by_difficulty[diff]
        report_lines.append(f"### 难度 {diff}")
        report_lines.append("")
        report_lines.append(f"| 图片 | 类型 | 状态 | SMILES | RDKit | 分子量 | 耗时 |")
        report_lines.append(f"|:---|:---|:---|:---|:---:|:---:|:---:|")
        for r in items:
            status_icon = {"SUCCESS": "✅", "EMPTY_RESULT": "⬜", "FILE_NOT_FOUND": "⚠️", "DECIMER_ERROR": "❌"}.get(r["status"], "❓")
            smiles_col = f"`{r['smiles'][:40]}{'...' if len(r.get('smiles',''))>40 else ''}`" if r.get("smiles") else "—"
            rdkit_col = "✅" if r.get("rdkit_valid") else ("❌" if r.get("smiles") else "—")
            mw_col = str(r.get("mol_weight", "—"))
            time_col = f"{r.get('inference_time', '—')}s" if r.get("inference_time") else "—"
            report_lines.append(f"| {r['filename']} | {r['expected_type']} | {status_icon} | {smiles_col} | {rdkit_col} | {mw_col} | {time_col} |")
        report_lines.append("")

    # 写入报告
    report_path = OUTPUT_DIR / "decimer-test-report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"\n  📄 报告已写入: {report_path.relative_to(VAULT_ROOT)}")

    # 写入 JSON 详细数据
    json_path = OUTPUT_DIR / "decimer-test-results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  📊 详细数据: {json_path.relative_to(VAULT_ROOT)}")

    # ── 打印汇总 ──
    print()
    print("=" * 70)
    print("  📊 测试汇总")
    print("=" * 70)
    print(f"  识别成功率: {success_count}/{total} ({success_count/total*100:.0f}%)")
    print(f"  RDKit 有效率: {rdkit_valid_count}/{success_count} ({rdkit_valid_count/success_count*100:.0f}%)" if success_count > 0 else "  RDKit 有效率: N/A")
    print()

    # 按难度的成功率
    print("  按难度分析:")
    for diff in sorted(by_difficulty.keys()):
        items = by_difficulty[diff]
        ok = sum(1 for r in items if r["status"] == "SUCCESS")
        valid = sum(1 for r in items if r.get("rdkit_valid"))
        print(f"    {diff}: {ok}/{len(items)} 识别, {valid}/{ok} RDKit有效")
    print()


if __name__ == "__main__":
    run_decimer_test()
