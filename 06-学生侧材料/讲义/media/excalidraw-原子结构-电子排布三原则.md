# 电子排布三原则

## 原则一：构造原理（Aufbau Principle）

```mermaid
flowchart LR
    A[1s²] --> B[2s²] --> C[2p⁶] --> D[3s²] --> E[3p⁶]
    E --> F[4s²] --> G[3d¹⁰] --> H[4p⁶]
    H --> I[5s²] --> J[4d¹⁰] --> K[5p⁶]
    K --> L[6s²] --> M[4f¹⁴] --> N[5d¹⁰] --> O[6p⁶]
    O --> P[7s²] --> Q[5f¹⁴] --> R[6d¹⁰] --> S[7p⁶]
    
    style A fill:#b2f2bb,stroke:#1e40af
    style F fill:#ffd8a8,stroke:#1e40af
    style G fill:#ffd8a8,stroke:#1e40af
```

> **口诀**：电子填入先低能，能级组内按顺序。1s→2s→2p→3s→3p→4s→3d→4p→5s→4d→5p→6s→4f→5d→6p→7s→5f→6d→7p

## 原则二：Pauli不相容原理

> **同一原子中，无四个量子数完全相同的两个电子。**

$$\text{每个原子轨道最多容纳 } \boxed{2} \text{ 个自旋相反的电子}$$

```mermaid
flowchart TD
    subgraph "允许"
        A["轨道: ↑↓<br>(两个电子, 自旋相反)"]
    end
    subgraph "不允许"
        B["轨道: ↑↑<br>(两个电子, 自旋相同) ✗"]
        C["轨道: ↑↑↑<br>(三个电子) ✗"]
    end
    
    style A fill:#b2f2bb,stroke:#1e40af
    style B fill:#ffc9c9,stroke:#1e40af
    style C fill:#ffc9c9,stroke:#1e40af
```

## 原则三：Hund规则

> **电子在简并轨道上分占不同轨道，自旋平行。**

### 示例：N原子（Z=7）2p³的填充

```mermaid
flowchart LR
    subgraph "正确 ↑ 分占三个轨道"
        A["2p: ▲ │ ▲ │ ▲"]
    end
    subgraph "错误 ✗ 先配对"
        B["2p: ▲▼ │ ▲ │ ○"]
    end
    
    style A fill:#b2f2bb,stroke:#1e40af
    style B fill:#ffc9c9,stroke:#1e40af
```

### 特例：半满/全满额外稳定

| 构型 | 状态 | 额外稳定 | 代表元素 |
|:---:|:---:|:---:|:---|
| p³, d⁵, f⁷ | **半满** | 交换能最大 | N, Cr, Mo |
| p⁶, d¹⁰, f¹⁴ | **全满** | 闭壳层 | Ne, Zn, Cu, Ag |
| p⁰, d⁰, f⁰ | **全空** | 无电子 | (不在讨论范围) |

### 三原则综合应用

```mermaid
flowchart TD
    A[开始排布] --> B[按构造原理<br>确定填充顺序]
    B --> C[按 Pauli 原理<br>每轨道最多2电子]
    C --> D[按 Hund 规则<br>简并轨道分占]
    D --> E{检查是否<br>半满/全满特例?}
    E -->|是| F[调整排布<br>从 s 移一个电子到 d]
    E -->|否| G[保持当前排布]
    F --> G
    G --> H[✅ 完成]
    
    style A fill:#a5d8ff,stroke:#1e40af
    style B fill:#d0bfff,stroke:#1e40af
    style C fill:#d0bfff,stroke:#1e40af
    style D fill:#d0bfff,stroke:#1e40af
    style E fill:#fff3bf,stroke:#1e40af
    style F fill:#ffd8a8,stroke:#1e40af
    style H fill:#b2f2bb,stroke:#1e40af
```
