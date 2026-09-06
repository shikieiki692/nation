---
title: CIF 文件库
type: 资源索引
purpose: 晶体结构 CIF 数据文件管理
created: 2026-08-01
updated: 2026-08-01
tags: [可视化, CIF, 晶体结构, 数据]
---

# CIF 文件库

> 存放化学教学常用晶体结构的 CIF（Crystallographic Information File）文件。
> 可直接用 VESTA、Avogadro 2 打开查看。

## 分类目录

| 目录 | 内容 | 典型结构 |
|:-----|:-----|:---------|
| [[02-CIF文件库/01-单质/README\|01-单质]] | 单质晶体 | Cu、Fe、C（金刚石/石墨）、Si、Na |
| [[02-CIF文件库/02-离子晶体/README\|02-离子晶体]] | 离子化合物 | NaCl、CsCl、ZnS、CaF₂、TiO₂ |
| [[02-CIF文件库/03-共价晶体/README\|03-共价晶体]] | 共价网络晶体 | 金刚石、SiO₂、SiC、BN |
| [[02-CIF文件库/04-金属晶体/README\|04-金属晶体]] | 金属晶体 | Cu、Fe、Mg、W、Ti |
| [[02-CIF文件库/05-分子晶体/README\|05-分子晶体]] | 分子晶体 | 冰（H₂O）、干冰（CO₂）、I₂、S₈ |
| [[02-CIF文件库/06-配合物/README\|06-配合物]] | 配位化合物 | [Co(NH₃)₆]³⁺、[Fe(CN)₆]⁴⁻ |

## 使用方法

### 用 VESTA 打开
```
VESTA → File → Open → 选择 .cif 文件
```

### 用 Avogadro 2 打开
```
Avogadro → File → Open → 选择 .cif 文件
```

### 命名规范
```
{化学式}-{空间群符号}.cif
例：NaCl-Fm-3m.cif、CsCl-Pm-3m.cif、ZnS-F-43m.cif
```

## CIF 数据来源

| 来源 | 链接 | 说明 |
|:-----|:-----|:-----|
| Crystallography Open Database | [crystallography.net](https://www.crystallography.net/) | 免费开放 |
| Materials Project | [materialsproject.org](https://materialsproject.org/) | 注册后免费下载 |
| AMICS Mineral Database | [rruff.info](https://rruff.info/ima/) | 矿物晶体结构 |
| VESTA 内置示例 | 安装目录/examples/ | 软件自带 |
| 手动创建 | 用 Avogadro 构建 → 导出 CIF | 自定义结构 |

## 待补充清单

以下是教学高频需要但尚未添加的晶体结构：

### 单质
- [ ] Cu（面心立方）→ 已移至 `04-金属晶体/Cu-Fm-3m.cif`
- [ ] Fe（体心立方）→ 已移至 `04-金属晶体/Fe-Im-3m.cif`
- [ ] C（金刚石）→ 已移至 `03-共价晶体/C-Fd-3m.cif`
- [ ] C（石墨）
- [ ] Na（体心立方）
- [ ] Mg（六方密堆）→ 已移至 `04-金属晶体/Mg-P63mmc.cif`

### 离子晶体
- [x] NaCl（岩盐结构）→ `02-离子晶体/NaCl-Fm-3m.cif`
- [x] CsCl → `02-离子晶体/CsCl-Pm-3m.cif`
- [x] ZnS（闪锌矿）→ `02-离子晶体/ZnS-F-43m.cif`
- [ ] ZnS（纤锌矿）
- [x] CaF₂（萤石）→ `02-离子晶体/CaF2-Fm-3m.cif`
- [x] TiO₂（金红石）→ `02-离子晶体/TiO2-P42mnm.cif`
- [ ] Al₂O₃（刚玉）

### 共价晶体
- [x] 金刚石（C）→ `03-共价晶体/C-Fd-3m.cif`
- [ ] SiO₂（β-鳞石英）
- [x] Si（金刚石结构）→ `03-共价晶体/Si-Fd-3m.cif`
- [ ] SiC（碳化硅）
- [ ] BN（立方氮化硼）

### 金属晶体
- [x] Cu（面心立方）→ `04-金属晶体/Cu-Fm-3m.cif`
- [x] Fe（体心立方）→ `04-金属晶体/Fe-Im-3m.cif`
- [x] Mg（六方密堆）→ `04-金属晶体/Mg-P63mmc.cif`
- [ ] W（体心立方）

### 分子晶体
- [x] H₂O（冰 Ih）→ `05-分子晶体/H2O_ice-P63mmc.cif`
- [x] CO₂（干冰）→ `05-分子晶体/CO2-Pa-3.cif`
- [ ] I₂
- [ ] S₈

### 配合物
- [x] K₃[Fe(CN)₆] → `06-配合物/K3FeCN6-R-3c.cif`
- [ ] [Co(NH₃)₆]Cl₃
- [ ] CuSO₄·5H₂O
