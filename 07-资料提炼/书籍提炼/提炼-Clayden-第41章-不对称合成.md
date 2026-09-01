---
title: 提炼-Clayden-第41章-不对称合成
type: 资料提炼
subject: 有机化学
source: Clayden Organic Chemistry 第2版 中文版 Ch.41
source_path: mineru/中文版clayden-chinese-41章1132-1164.md
source_range: line 1–1233
extracted_date: 2026-05-19
template_version: v1.3
status: 已提炼
target_kp: [不对称合成, 手性催化, 对映选择性]
handout_plan:
  - target: "有机化学基础"
    status: completed
    priority: P2
    source_sections: ["第41章 不对称合成（手性助剂、手性配体、Sharpless/Noyori不对称催化）"]
    estimated_pages: 6
knowledge_points: [不对称合成, 手性中心, 不对称氢化, 立体化学基础, 非对映选择性, 羰基反应, Aldol缩合, 金属有机化学, 手性池合成, 拆分技术, 手性助剂, 不对称催化还原, 不对称环氧化, 不对称双羟基化, 配体加速催化, 药物合成, 天然产物合成, 化竞合成题]
---

# 提炼：Clayden 第41章——不对称合成（Asymmetric Synthesis）
[[不对称合成]]

---

## 一、核心概念与定义

### 1.1 为什么需要不对称合成
- **手性与生命**：生物体系是手性环境（酶、受体），对映体往往表现出截然不同的生物活性。
- **实例**：（S）-多巴（L-dopa）可治疗帕金森病，而（R）-多巴不仅无效，还具有毒性。
- **单一对映体的重要性**：香料、药物、农药等领域常需单一对映体。

### 1.2 关键术语回顾
- **对映体（enantiomers）**、**非对映体（diastereomers）**、**R/S**、**+/-**
- **前手性（prochiral）**：一个简单转换即可变为手性的单元（如三角型羰基碳、烯烃碳）。[[手性中心]]
- **对映异位（enantiotopic）**、**非对映异位（diastereotopic）**：描述前手性单元上两个相同取代基的空间关系。
- **对映体过量（ee）**：衡量对映选择性的指标。

---

## 二、获取单一对映体的方法

| 方法 | 原理 | 优缺点 |
|:---|:---|:---|
| **手性池（Chiral Pool）** | 从天然手性化合物（氨基酸、糖、萜类等）出发 | 直接、可靠，但结构受限，对映体可能不均等可得 |
| **拆分（Resolution）** | 用光学纯试剂将对映体混合物分离 | 最大产率50%（单一对映体），但两种对映体都可获得 |
| **手性助剂（Chiral Auxiliary）** | 将手性单元临时连接到底物上，反应后去除 | 化学计量消耗，但可回收；非对映选择性控制 |
| **手性试剂（Chiral Reagent）** | 用手性试剂直接对非手性底物反应 | 化学计量消耗，成本较高 |
| **不对称催化（Asymmetric Catalysis）** | 用手性催化剂催化前手性底物的反应 | 催化剂用量极少，最理想的方法 |

---

## 三、手性池（Chiral Pool）

### 3.1 氨基酸
- 天然L-氨基酸（除半胱氨酸为R外，其余大多为S构型）是最易得的手性池成员。
- 可直接用作合成起始原料，或转化为手性助剂/试剂。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/d61fef6695268760834e149a3dd7aadca6f3af50a30ee213aa4385a581678db3.jpg]] — 天然L-氨基酸通式（line ~73）

### 3.2 羟基酸
- （R）-/(S）-乳酸、扁桃酸、苹果酸、酒石酸等可从天然来源获取。
- 酒石酸（L-(+)-酒石酸 = (R,R)-(+)-酒石酸）是Sharpless不对称环氧化的关键配体来源。

### 3.3 糖类
- 甘露糖 → 甘露醇 → 双缩醛保护 → 裂解得被保护的甘油醛。
- 可用于构建多手性中心分子。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/6be96c8a7973f3ddae79e84d46c4f4c96972385b66e174a4f3ee5509418901f8.jpg]] — 甘露糖转化为甘油醛衍生物（line ~220）

### 3.4 手性池策略的局限
- 合成路线必须“硬塞进”可用起始原料的结构中。
- 很多手性池成员只以一种对映体形式廉价可得。

---

## 四、拆分（Resolution）

- **原理**：利用手性试剂（拆分剂）与外消旋混合物中的一种对映体形成非对映体盐/配合物，利用溶解度差异分离。
- **实例**：Cilag公司用手性不寻常氨基酸的合成中，利用(-)-麻黄碱结晶拆分。
- **优点**：一种拆分剂可得到**两种对映体**（一种结晶析出，另一种留在母液中）。
- **缺点**：最大理论产率50%（若只需一种对映体）。

---

## 五、手性助剂（Chiral Auxiliaries）

### 5.1 策略流程
1. 将光学纯手性助剂连接到非手性底物上。
2. 手性助剂使底物产生非对映异位面，发生非对映选择性反应。
3. 去除手性助剂，得到光学纯产物（原则上可回收助剂）。

### 5.2 Evans 噁唑烷酮助剂
- 由(S)-缬氨酸廉价制得，是最常用的手性助剂之一。
- **应用**：不对称烷基化、羟醛反应（aldol reaction）。
- **优势**：助剂可回收，非对映选择性高。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/ae24f7c3322ac7577e8944ba34e12912af7972cc99a1f8f769bd66fb2bd8ac41.jpg]] — Evans助剂合成路线（line ~307）

### 5.3 其他常见手性助剂
- **Oppolzer 樟脑磺内酰胺（sultam）**：用于共轭加成等反应。
- **8-苯基薄荷醇（8-phenylmenthol）**：用于Diels-Alder反应。
- **伪麻黄碱助剂**：用于不对称烷基化。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/aa0dfeaa8e942255c82ceba767256a5b927d57f1e032ed6e958221cee00ec718.jpg]] — 基于樟脑的助剂（line ~500）

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/34c821eacac1a1f00b0bf31395461ffc4145426f5f213a998cb7c4d4729c5236.jpg]] — 伪麻黄碱助剂（line ~504）

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/6bd3ab8210f67c0d69819730b3d5ca793ceae91547f276879ea75811ef228a79.jpg]] — 8-苯基薄荷基助剂（line ~507）

---

## 六、手性试剂（Chiral Reagents）

### 6.1 鹰爪豆碱（(-)-Sparteine）介导的去质子化
- **原理**：(-)-鹰爪豆碱作为双齿配体与烷基锂络合，形成手性碱。
- 可选择性移去前手性CH₂上的两个对映异位质子之一。
- **应用**：制备富对映的有机锂试剂，进而与亲电试剂反应。
- **缺点**：仍需化学计量的光学纯试剂，成本较高。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/973115d4856445412a675860d5ba8c43c442fdfe36933f8d9db3d3ac5b201976.jpg]] — 鹰爪豆碱介导的锂化（line ~521）

---

## 七、不对称催化（Asymmetric Catalysis）

### 7.1 CBS还原（Corey-Bakshi-Shibata Reduction）
- **试剂**：手性硼杂环（由脯氨酸衍生的氨基醇）+ 硼烷（BH₃）。
- **底物**：芳基-烷基酮（两个取代基空间差异明显时效果最佳）。
- **机理**：硼杂环的Lewis酸性B与羰基O络合，Lewis碱性N与BH₃络合；负氢通过六元环状过渡态迁移。
- **对映选择性**：大取代基（R_L）倾向于占据假平伏键位置。
- **催化量**：通常约10 mol%。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/2e32ccd3cf59020401d2a02b9581954ecdeb56f3d472deb3d973b8913f67c9d3.jpg]] — CBS还原实例：脯氨酸衍生的催化剂，97% ee（line ~579）

### 7.2 Ru/TsDPEN 催化转移氢化
- **催化剂**：Ru(II)配合物 + (S,S)-TsDPEN（N-对甲苯磺酰基-1,2-二苯基乙二胺）。
- **还原剂**：H₂、异丙醇（氧化为丙酮）或甲酸（氧化为CO）。
- **特点**：催化剂用量极低（<<1%），适用于工业生产。
- **Nobel奖**：Noyori（Ru/Rh催化还原）、Sharpless（Os/Ti催化氧化）、Knowles（工业不对称氢化）获2001年诺贝尔化学奖。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/0190c5e064eb80fabdc072b637723eb60b1d3bd0e9c05ed5a371b7851fb0f741.jpg]] — Ru/TsDPEN催化转移氢化（line ~621）

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/864148ac7e4f3deaf08c350c3415b4d02be983ab693b1978c81a375b500f69dc.jpg]] — 16e和18e Ru配合物的合成（line ~637）

### 7.3 Rh/BINAP 不对称氢化
- **配体**：BINAP（2,2'-双二苯膦基-1,1'-联萘），手性源于联萘的阻转异构。
- **特点**：适用于多种不饱和羧酸衍生物的高对映选择性还原。[[不对称氢化]]
- **BINAP的拆分**：通过(S)-BINAP氧化物与二-O-苯甲酰基-L-酒石酸共结晶拆分。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/d54ef6947e37bf01099d98598607b47c82e53631590a3ee519b308ccc4b4ab20.jpg]] — BINAP的合成与拆分（line ~815）

### 7.4 Sharpless 不对称环氧化（Asymmetric Epoxidation, AE）
- **底物**：烯丙醇（局限性：仅对烯丙醇有效）。
- **试剂**：Ti(Oi-Pr)₄ + 酒石酸二乙酯（DET）+ t-BuOOH。
- **催化量**：钛和酒石酸酯都可用催化量。
- **机理**：双核Ti配合物，烯丙醇与Ti络合后，过氧配体从特定面传递氧原子。
- **对映选择性**：L-(+)-DET与D-(-)-DET给出相反构型的环氧。
- **应用**：雌舞毒蛾信息素（disparlure）、普萘洛尔（propranolol）等合成。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/eccbf6a54b4672b5bf12dcb76d44a139f6bafda95ff0e684da32a75c82adcdee.jpg]] — Sharpless AE实例：94% ee（line ~831）

📌 **图片待补：** 71754e3c132a08237d3a1e1ca9139dc1d89dba0a783ba061cc64304896d4845d.jpg — Ti-DET配合物结构（line ~849）

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/5d63ef09dad839b8fc925b808bf38e2a093184cc4773f23edf4e6c0bd4c56817.jpg]] — Sharpless AE对映选择性模型（line ~869）

### 7.5 Jacobsen 环氧化
- **适用范围**：**简单烯烃**（弥补了Sharpless AE仅对烯丙醇有效的不足）。
- **催化剂**：Mn(III)-salen配合物。
- **配体**：salen = 亚乙基双水杨亚胺，由手性双胺与水杨醛缩合制得。
- **特点**：对顺式烯烃效果较好，对反式烯烃选择性较低。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/68df00f09b3f664dd11221ab26798791c2153b31b4ad7817c80626d73adfea38.jpg]] — Jacobsen环氧化：salen配体（line ~946）

### 7.6 Sharpless 不对称双羟基化（Asymmetric Dihydroxylation, AD）
- **试剂**：K₂OsO₂(OH)₄ + K₃Fe(CN)₆ + 手性配体（DHQD₂PHAL 或 DHQ₂PHAL）。
- **配体**：基于二氢奎宁（DHQ）或二氢奎宁定（DHQD）的酞嗪二聚体。
- **催化量**： Os用量极低。
- **特点**：对几乎所有烯烃都有效（富电子或缺电子），选择性极高（>98% ee常见）。
- **AD-mix**：商品化试剂混合物。AD-mix-β含DHQD₂PHAL；AD-mix-α含DHQ₂PHAL。
- **对映选择性模型**：底物按"大-中-小"排列，DHQD配体使Os从顶面进攻，DHQ从底面进攻。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/4ad928fa16b78195d325ffedbe7346aecd37ba94113589ae279e7b025cd8243c.jpg]] — AD反应实例：98% ee（line ~1014）

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/5d498b6c071cec3a093aa732f4adfd16f443c98832ea10f444dabe69cd17436f.jpg]] — AD对映选择性模型（line ~1025）

---

## 八、配体加速催化（Ligand Accelerated Catalysis）

- **核心思想**：手性配体不仅提供手性环境，还**加速**了反应。
- **为什么重要**：如果无配体时"背景反应"速率也很快，则外消旋产物会稀释ee值。
- **理想情况**：背景反应极慢，有手性配体时反应极快——此时对映选择性最高。
- **实例**：Sharpless AD、二烷基锌对醛的加成。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/5de7cb38177a812548cdcdaf0801cf6484773ed6d920e87c00086d9be9f06b4e.jpg]] — 配体加速催化原理图（line ~1098）

---

## 九、碳-碳键的不对称形成

### 9.1 二烷基锌对醛的加成
- **特点**：Et₂Zn与醛在无催化剂时反应极慢。
- **手性氨基醇催化剂**：显著加速反应，并赋予对映选择性。
- **产物**：手性仲醇，ee可达90%以上。
- **炔基锌加成**：催化量Zn(OTf)₂ + Et₃N即可。

![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/462e1d62d6817dee5e3ae07e8cf4caa520fc1000a9b4c3433aa640554c54eba8.jpg]] — 二乙基锌对醛的不对称加成（line ~1122）

---

## 十、关键结论

1. **不对称合成的五种策略**：手性池 < 拆分 < 手性助剂 < 手性试剂 < 不对称催化（效率递增）。
2. **手性助剂的核心逻辑**：通过临时连接光学纯辅助基团，将**对映选择性**问题转化为**非对映选择性**问题。
3. **不对称催化的核心逻辑**：手性催化剂或配体创造不对称环境，使前手性底物的两面产生能量差异。
4. **CBS还原适用于芳基-烷基酮**；空间差异越大，选择性越好。
5. **Sharpless AE仅对烯丙醇有效**，但极为可靠；Jacobsen环氧化适用于简单烯烃。
6. **Sharpless AD几乎适用于所有烯烃**，且选择性极高，是合成手性二醇的首选方法。
7. **配体加速催化**是不对称反应设计的重要原则——好的不对称反应应满足"有配体快、无配体慢"。
8. **2001年诺贝尔化学奖**：Knowles、Noyori、Sharpless，表彰金属催化不对称反应。

---

## 十一、与其他知识点的联系

```
不对称合成
├── 前置知识
│   ├── [[立体化学基础]]（R/S, 对映体, 非对映体, Ch14）
│   ├── [[非对映选择性]]（Ch32 & Ch33）
│   ├── [[羰基反应]]（Ch6, Ch9-11）
│   ├── [[Aldol缩合]]（Ch26）
│   └── [[金属有机化学]]（Ch40, 电子计数, 配位化学）
├── 核心关联
│   ├── [[手性池合成]]（氨基酸、糖、萜类）
│   ├── [[拆分技术]]（结晶拆分、动力学拆分）
│   ├── [[手性助剂]]（Evans噁唑烷酮、Oppolzer sultam）
│   ├── [[不对称催化还原]]（CBS, Ru/TsDPEN, Rh/BINAP）
│   ├── [[不对称环氧化]]（Sharpless AE, Jacobsen）
│   ├── [[不对称双羟基化]]（Sharpless AD）
│   └── 配体加速催化
└── 应用
    ├── [[药物合成]]（L-dopa, propranolol, 抗HIV药物）
    ├── [[天然产物合成]]（信息素、抗生素）
    └── [[03-知识点/有机化学/有机合成|化竞合成题]]（手性中心的构建策略）
```

---

## 十二、竞赛题型

| 题型 | 考查点 | 难度 |
|:---|:---|:---:|
| **手性池策略设计** | 从天然氨基酸/糖出发 retrosynthesis | ★★★★ |
| **手性助剂机理** | Evans助剂在aldol反应中的非对映选择性控制 | ★★★★★ |
| **CBS还原选择** | 预测芳基-烷基酮CBS还原的产物构型 | ★★★ |
| **Sharpless AE模型** | 根据L-(+)-DET/D-(-)-DET预测环氧构型 | ★★★★ |
| **Sharpless AD模型** | 根据底物取代基大小排列预测二醇构型 | ★★★★ |
| **试剂选择** | 根据底物结构选择AE/AD/Jacobsen环氧化 | ★★★★ |
| **对映选择性解释** | 配体加速催化的原理和重要性 | ★★★★ |
| **合成设计** | 多步不对称合成（含去保护、官能团转化） | ★★★★★ |

---

## 十三、关键图片与反应方程式

- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/d61fef6695268760834e149a3dd7aadca6f3af50a30ee213aa4385a581678db3.jpg]] — 天然L-氨基酸通式（line ~73）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/6be96c8a7973f3ddae79e84d46c4f4c96972385b66e174a4f3ee5509418901f8.jpg]] — 甘露糖转化为甘油醛衍生物（line ~220）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/ae24f7c3322ac7577e8944ba34e12912af7972cc99a1f8f769bd66fb2bd8ac41.jpg]] — Evans噁唑烷酮助剂合成（line ~307）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/de66e3d00b59ad43470f7ac1d00b253d91f36439479c2d5004b4f5a781465a21.jpg]] — Lewis酸螯合控制Diels-Alder反应（line ~319）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/973115d4856445412a675860d5ba8c43c442fdfe36933f8d9db3d3ac5b201976.jpg]] — 鹰爪豆碱介导的去质子化（line ~521）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/2e32ccd3cf59020401d2a02b9581954ecdeb56f3d472deb3d973b8913f67c9d3.jpg]] — CBS还原实例（line ~579）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/0190c5e064eb80fabdc072b637723eb60b1d3bd0e9c05ed5a371b7851fb0f741.jpg]] — Ru/TsDPEN催化转移氢化（line ~621）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/d54ef6947e37bf01099d98598607b47c82e53631590a3ee519b308ccc4b4ab20.jpg]] — BINAP的合成与拆分（line ~815）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/eccbf6a54b4672b5bf12dcb76d44a139f6bafda95ff0e684da32a75c82adcdee.jpg]] — Sharpless AE实例（line ~831）
- 📌 **图片待补：** 71754e3c132a08237d3a1e1ca9139dc1d89dba0a783ba061cc64304896d4845d.jpg — Ti-DET双核配合物（line ~849）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/5d63ef09dad839b8fc925b808bf38e2a093184cc4773f23edf4e6c0bd4c56817.jpg]] — Sharpless AE对映面选择性模型（line ~869）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/68df00f09b3f664dd11221ab26798791c2153b31b4ad7817c80626d73adfea38.jpg]] — Jacobsen环氧化salen配体（line ~946）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/4ad928fa16b78195d325ffedbe7346aecd37ba94113589ae279e7b025cd8243c.jpg]] — Sharpless AD实例（line ~1014）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/5d498b6c071cec3a093aa732f4adfd16f443c98832ea10f444dabe69cd17436f.jpg]] — AD对映选择性模型（line ~1025）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/5de7cb38177a812548cdcdaf0801cf6484773ed6d920e87c00086d9be9f06b4e.jpg]] — 配体加速催化原理（line ~1098）
- ![[mineru/03-教材书籍/Clayden有机化学（中文版）/中文版clayden-chinese-41章1132-1164_images/462e1d62d6817dee5e3ae07e8cf4caa520fc1000a9b4c3433aa640554c54eba8.jpg]] — 二乙基锌对醛的不对称加成（line ~1122）

---

## 十四、超纲/非竞赛内容标注

| 内容 | 超纲程度 | 说明 |
|:---|:---:|:---|
| 具体工业合成案例（舞毒蛾信息素、抗HIV药物） | 决赛外 | 仅作方法学展示，不考具体路线 |
| BINAP的拆分与共结晶细节 | 决赛 | 了解概念即可，不考操作细节 |
| CBS催化剂的详细合成步骤 | 决赛 | 了解从脯氨酸到催化剂的转化即可 |
| Ru/TsDPEN配合物的电子计数 | 决赛 | 需懂16e/18e规则（Ch40内容） |
| Sharpless AE的详细双核Ti机理 | 决赛 | 竞赛中常考简化版模型 |
| AD反应的"手性口袋"机理 | 决赛外 | 目前机理仍不完全清晰 |
| 配体加速催化的定量动力学 | 决赛外 | 只需定性理解概念 |
| 二烷基锌加成的详细机理 | 决赛 | 了解氨基醇配体的作用即可 |
| 不对称共轭加成的细节 | 决赛 | 了解有机铜试剂的SN2'选择性即可 |

---

## 十五、存疑或待验证之处

1. **CBS还原的ee值数据**：不同底物（芳基-烷基酮 vs 二烷基酮）的ee差异需要更多实例验证。
2. **Jacobsen环氧化的底物范围**：本章指出其对反式烯烃选择性较低（70-74% ee），需确认竞赛中是否常考顺式烯烃底物。
3. **AD-mix的商品化组成**：AD-mix-α/β的具体配比是否需记忆？竞赛中通常直接给出试剂。
4. **Evans助剂的RAMP/SAMP变体**：本章未涉及，但竞赛合成题中可能出现，需另查资料。
5. **不对称催化的"软/硬"选择性**：某些过渡金属催化的不对称反应是否涉及软硬酸碱理论？本章未明确讨论。

---

*本提炼基于 Clayden Organic Chemistry 第2版中文版第41章（line 1–1233）。*