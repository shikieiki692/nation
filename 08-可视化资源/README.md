---
title: 可视化资源
type: 资源
role: 化学教学可视化中心
created: 2026-08-01
updated: 2026-08-01
tags: [可视化, 3D, 晶体结构, 分子模型, 动画]
---

# 可视化资源

> 本文件夹是化学教学可视化资源的**独立管理区**，包含工具指南、CIF 晶体数据、渲染图片、动画脚本和可视化索引。

## 定位

与知识库主体（03-知识点、04-题库等）分开管理，专门服务于**教学可视化**需求：
- 晶体结构 3D 渲染（VESTA / Blender）
- 分子结构建模与动画（Avogadro / Blender）
- 晶胞、空间格子、配位多面体的教学配图

## 目录结构

```
08-可视化资源/
├── README.md                  ← 你在这里
├── 01-工具指南/                软件操作手册（10个文件）
│   ├── 化学可视化工具速查卡.md    ← 一页速查，快速入门
│   ├── VESTA快速上手.md          ← VESTA入门引导
│   ├── VESTA完整操作手册.md       ← VESTA所有功能
│   ├── Avogadro完整指南.md       ← Avogadro所有内容
│   ├── Gaussian完整指南.md       ← Gaussian所有内容
│   ├── Blender化学可视化完整指南.md ← Blender所有内容
│   ├── Molecular Nodes详细使用指南.md ← MN使用指南
│   ├── Molecular Nodes安装排查指南.md ← MN安装问题
│   ├── 晶体与分子空间结构可视化深入教程.md ← 晶体/分子结构
│   └── 化学可视化深入专题-晶体场到反应机理.md ← 高级专题
├── 02-CIF文件库/               晶体结构 CIF 数据文件（84个）
│   ├── 00-分子结构/            分子模型数据
│   ├── 01-单质/               金属、金刚石、石墨等
│   ├── 02-离子晶体/           NaCl、CsCl、ZnS、CaF₂ 等
│   ├── 03-共价晶体/           金刚石、SiO₂、SiC 等
│   ├── 04-金属晶体/           Cu、Fe、Mg 等
│   ├── 05-分子晶体/           冰、干冰、I₂ 等
│   └── 06-配合物/             [Co(NH₃)₆]³⁺、[Fe(CN)₆]⁴⁻ 等
├── 03-渲染图片/                导出的静态图片（按主题分类）
│   ├── 01-晶体结构/
│   ├── 02-分子结构/
│   ├── 03-晶胞模型/
│   └── 04-轨道与能级/
├── 04-动画脚本/                Blender / VESTA Python 脚本
├── 05-模板场景/                Blender 预设场景文件
├── 06-可视化索引/              与知识点的映射关系
│   ├── 无机化学-可视化索引.md
│   ├── 有机化学-可视化索引.md
│   ├── 结构化学-可视化索引.md
│   ├── 物理化学-可视化索引.md
│   └── 可视化资源与知识库整合方案.md
└── 07-规范与标准/              命名、元数据、质量、使用、维护标准
    ├── 可视化资源命名规范.md
    ├── 可视化资源元数据标准.md
    ├── 可视化资源质量检查清单.md
    ├── 可视化资源使用教程.md
    ├── 可视化资源更新维护流程.md
    ├── 01-工具指南目录整理.md
    └── 01-工具指南目录整理执行记录.md
```

## 工作流速查

| 场景 | 推荐工具 | 工作流 |
|:-----|:---------|:-------|
| 快速出晶体结构图 | VESTA | 打开 CIF → 设置样式 → 导出 PNG |
| 分子3D构型 | Avogadro | 构建分子 → 力场优化 → 导出 XYZ |
| 高质量渲染 | Blender + Molecular Nodes | 导入 PDB/CIF → 设置材质灯光 → Cycles 渲染 |
| 晶体结构动画 | VESTA → Blender | VESTA 导出 VRML → Blender 导入 → 设置动画 |
| 批量渲染 | Blender Python 脚本 | `blender --background --python script.py` |

## CIF 数据来源

| 来源 | 说明 | 链接 |
|:-----|:-----|:-----|
| Crystallography Open Database | 免费开放晶体数据库 | [crystallography.net](https://www.crystallography.net/) |
| Materials Project | 材料科学晶体数据 | [materialsproject.org](https://materialsproject.org/) |
| ICSD（受限） | 国际晶体结构数据库 | [icsd.products.fiz-karlsruhe.de](https://icsd.products.fiz-karlsruhe.de/) |
| AMICS Mineral Database | 矿物晶体结构 | [rruff.info](https://rruff.info/ima/) |
| VESTA 内置 | 软件自带示例结构 | VESTA → File → Open |

## 与知识库的关联

可视化资源通过 `06-可视化索引/` 与 `03-知识点/` 建立映射：
- 每个学科模块一份索引文件
- 索引文件列出"哪个 KP → 需要什么可视化 → 对应哪个文件"
- 可在 KP 的 frontmatter 中添加 `visuals` 字段引用
