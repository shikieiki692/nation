# DECIMER OCSR 测试报告

**测试时间**: 2026-07-07
**DECIMER 版本**: 2.8.0 (模型 V2)
**RDKit 版本**: 2026.3.3
**环境**: Python 3.12, Windows, TensorFlow 2.20

---

## Part A: 基准测试（RDKit 生成的标准 2D 骨架式）

> 用 RDKit 渲染 20 个分子的标准 2D 结构图，再让 DECIMER 识别，测量"理想条件"下的准确率。

| 分子 | 输入 SMILES | DECIMER 输出 | 状态 | Tanimoto | 耗时 |
|:---|:---|:---|:---:|:---:|:---:|
| benzene | `c1ccccc1` | `c1ccccc1` | ✅ EXACT | 1.0 | 3.1s |
| toluene | `Cc1ccccc1` | `C1=CC=C(C=C1)[CH]` | ⚠️ | 0.375 | 0.7s |
| phenol | `Oc1ccccc1` | `Oc1ccccc1` | ✅ EXACT | 1.0 | 0.6s |
| aniline | `Nc1ccccc1` | `Nc1ccccc1` | ✅ EXACT | 1.0 | 0.6s |
| acetophenone | `CC(=O)c1ccccc1` | `CC(=O)c1ccccc1` | ✅ EXACT | 1.0 | 0.6s |
| benzoic acid | `OC(=O)c1ccccc1` | `OC(=O)c1ccccc1` | ✅ EXACT | 1.0 | 0.7s |
| naphthalene | `c1ccc2ccccc2c1` | `c1ccc2ccccc2c1` | ✅ EXACT | 1.0 | 0.7s |
| anthracene | 三环芳烃 | 完全正确 | ✅ EXACT | 1.0 | 0.9s |
| cyclohexane | `C1CCCCC1` | `C1CCCCCC1` (多了1个C) | ⚠️ SIMILAR | 1.0 | 0.5s |
| cyclohexanone | `O=C1CCCCC1` | 完全正确 | ✅ EXACT | 1.0 | 0.5s |
| glucose | D-葡萄糖 | 完全正确 | ✅ EXACT | 1.0 | 1.3s |
| caffeine | 咖啡因 | 完全正确 | ✅ EXACT | 1.0 | 0.9s |
| aspirin | 阿司匹林 | 完全正确 | ✅ EXACT | 1.0 | 0.8s |
| ibuprofen | 布洛芬 | 完全正确 | ✅ EXACT | 1.0 | 0.9s |
| cholesterol | 胆固醇 (C27) | 完全正确 | ✅ EXACT | 1.0 | 2.5s |
| ATP (简化) | 核苷+磷酸 | 完全正确 | ✅ EXACT | 1.0 | 2.8s |
| morphine | 吗啡 | 完全正确 | ✅ EXACT | 1.0 | 1.9s |
| penicillin G | 青霉素G | 完全正确 | ✅ EXACT | 1.0 | 2.0s |
| paracetamol | 对乙酰氨基酚 | 完全正确 | ✅ EXACT | 1.0 | 0.8s |
| vitamin C | 维生素C | 完全正确 | ✅ EXACT | 1.0 | 0.9s |

### 基准统计
- **有效 SMILES**: 20/20 (**100%**)
- **完全匹配**: 18/20 (**90%**)
- **Tanimoto > 0.7**: 19/20 (**95%**)
- **失败项**: toluene (甲基识别为 [CH])，cyclohexane (6元环误判为7元环)

---

## Part B: Vault 真实图片测试

> 测试 vault 中最接近标准结构的有机化学图片。

| 图片 | 描述 | 状态 | SMILES | 分析 |
|:---|:---|:---:|:---|:---|
| enantiomer.png | 2-溴丁烷对映体 | ✅ | `CC[C@@]([2H])(C)Br.CC[C@]([2H])(C)Br` | 接近正确，将CH3误判为[2H] |
| 18-crown-6.png | 18-冠-6 | ✅ | `C1COCCOCCOCCOCCOCCO1` | **完全正确！** |
| aromatic-heterocycles.png | 5个杂环 | ❌ | 含无效符号 [R19][X] | 多分子+简化式，失败 |
| suzuki-cycle.png | 催化循环 | ❌ | 过长且含未闭合括号 | 反应机理图，失败 |
| sn1-coordinate.png | SN1反应坐标 | ⚠️ | MW=4090 的聚合物 | 势能面图，严重幻觉 |
| beckmann-mechanism.png | Beckmann重排 | ❌ | 重复片段拼接 | 多步机理图，失败 |

### Vault 统计
- **有效 SMILES**: 3/6 (50%)，但其中1个结果是荒谬的 (MW=4090)
- **真正可用**: 2/6 (**33%**)

---

## 核心结论

### DECIMER 能力画像

```
                        DECIMER 识别能力
                    ┌─────────────────────────┐
    高准确率 ✅     │  干净2D骨架式            │  ← 基准90%完全匹配
                    │  单分子、无文字标注       │
                    │  标准ChemDraw风格        │
                    ├─────────────────────────┤
    中等 ⚠️        │  含楔线/虚线的立体化学    │  ← 对映体基本正确
                    │  杂原子标记清晰的分子     │
                    │  大环分子               │  ← 冠醚完美识别
                    ├─────────────────────────┤
    低/失败 ❌      │  反应机理图(箭头+多步)    │  ← 完全失败
                    │  R基团占位符            │  ← 幻觉出无效SMILES
                    │  Newman/椅式/3D投影      │  ← 严重误判
                    │  势能面/坐标图           │  ← 灾难性幻觉
                    │  含文字标注的图          │
                    │  多分子组合图            │
                    └─────────────────────────┘
```

### 对你的知识库的适用性判断

| 你的有机内容类型 | 占比(估) | DECIMER 适用性 |
|:---|:---:|:---:|
| 反应机理图（箭头推动） | ~40% | ❌ 完全不适用 |
| 概念示意图（手性/构象/势能面） | ~25% | ❌ 完全不适用 |
| 带R基团的通用反应式 | ~15% | ❌ 不适用 |
| 真题中的反应方程式 | ~15% | ⚠️ 需裁切单分子部分 |
| 干净的2D结构式 | ~5% | ✅ 高精度 |

**结论：DECIMER 对你现有 vault 内容的直接适用性很低（约5%的图片类型适合）。**

### 但 DECIMER 仍有价值的场景

1. **从教材 PDF 中提取结构**：如果你有英文有机化学教材 PDF，可以用 DECIMER Segmentation 先裁切出结构图区域，再识别。教材中的结构图通常比较干净。

2. **从真题 PDF 中提取分子**：决赛试题中的结构式如果单独裁切出来，DECIMER 可以识别。

3. **建立 SMILES 索引**：对能识别的分子，SMILES 可以用于：
   - RDKit 统一重绘标准化结构图
   - 分子量/分子式自动计算
   - Dataview 查询（按分子量筛选等）

4. **反向工作流**（更有价值）：不用 DECIMER 做识别，而是用 RDKit 从 SMILES 生成结构图 → 替换 vault 中的低质量手绘图。这才是真正能提效的管线。

---

## 建议的替代方案

针对你的实际需求（完善有机部分的讲义/习题），更实用的工具组合是：

| 需求 | 推荐工具 | 说明 |
|:---|:---|:---|
| 从 SMILES 生成标准结构图 | **RDKit** `Draw.MolToFile()` | 已安装，随时可用 |
| 从 SMILES 生成高质量渲染图 | **RDKit + MolDraw2D** | 支持楔线、颜色、原子标签 |
| 有机反应式排版 | **mhchem (LaTeX)** | 你已在用的 PDF 管线 |
| 机理分步图 | **Excalidraw** | 你已有的 skill |
| 从 PDF 提取文字+结构 | **MinerU / Marker** | 你的 `mineru/` 目录说明已在用 |

DECIMER 作为"图片→SMILES"的逆向工具，在你的场景下投入产出比不高。**RDKit + SMILES 正向管线** 才是正确方向。

---

*测试脚本和结果保存在 `09-AI工作区/decimer-test-results/`*
