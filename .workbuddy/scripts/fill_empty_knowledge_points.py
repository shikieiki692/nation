# -*- coding: utf-8 -*-
"""
为 25 个 knowledge_points 为空的题库文件补入真实知识点。

背景：上一轮清理把 knowledge_points 里的非术语值（填空题/综合分析/待人工标定 等）
删掉后，这 25 个文件变成空列表，被校验器记为「枚举-题库：knowledge_points 为空列表」。
本脚本按题目实际主题补入，消除这批告警。

铁律（与断链治理一致，不可放宽）：
  1. 只引用 03-知识点 里【真实存在】的笔记 —— 脚本启动即校验，不存在直接中止，
     绝不允许为了填字段而造出新的红链。
  2. 逐行处理、保留原行尾，不做整文件重写，避免 CRLF/LF 抖动。
  3. 只改 knowledge_points 那一行，其余字节不动。
"""
import os
import sys

VAULT = r"C:\Obsidion\妙妙屋"
Struc = os.path.join(VAULT, "04-题库", "教材习题", "结构化学基础")
Clayden = os.path.join(VAULT, "04-题库", "教材习题", "Clayden")

# 题目实际主题 → 知识点（均为 03-知识点 中已存在的笔记）
ASSIGN = {
    # --- Clayden 环加成两题：主题明确 ---
    "题-494-Clayden-Ch34-P6-1,3-偶极环加成立体化学控制": ["立体化学", "周环反应"],
    "题-495-Clayden-Ch34-P7-硝酮环加成区域立体选择性": ["立体化学", "周环反应"],
    # --- 结构化学基础 综合习题 C.1 ~ C.23 ---
    "题-286-结构化学基础-综合-习题C.1": ["分子轨道理论", "共轭效应"],      # β-胡萝卜素 一维势箱 / HOMO-LUMO
    "题-287-结构化学基础-综合-习题C.2": ["晶体结构", "分子轨道理论"],      # KCl 非整比 / 电子入空位
    "题-288-结构化学基础-综合-习题C.3": ["原子轨道", "量子数"],            # 环上粒子 Schrödinger 解
    "题-289-结构化学基础-综合-习题C.4": ["原子轨道", "量子数"],            # He+ 波函数 / n,l,m / 节面
    "题-290-结构化学基础-综合-习题C.5": ["原子结构", "电离能"],            # Sc 3d-4s 结合能 / 互斥能
    "题-291-结构化学基础-综合-习题C.6": ["分子轨道理论", "分子光谱"],      # CO 组态 / 键级 / 远红外测键长
    "题-292-结构化学基础-综合-习题C.7": ["分子轨道理论", "电离能"],        # NO 组态 / 键级 / 电离能比较
    "题-293-结构化学基础-综合-习题C.8": ["分子的对称性判断"],             # 分子几何构型与点群
    "题-294-结构化学基础-综合-习题C.9": ["对映异构", "立体化学"],         # 沙利度胺 R/S 对映体
    "题-295-结构化学基础-综合-习题C.10": ["分子的对称性判断"],            # 立方体模型看分子构型
    "题-296-结构化学基础-综合-习题C.11": ["原子轨道", "分子的对称性判断"], # 杂化轨道 / 构型 / 磁性
    "题-297-结构化学基础-综合-习题C.12": ["分子的对称性判断"],            # C60 多面体拓扑
    "题-298-结构化学基础-综合-习题C.13": ["钙钛矿结构", "密堆积"],        # SrTiO3 键价 / 空隙
    "题-299-结构化学基础-综合-习题C.14": ["18电子规则", "EAN规则", "配位化合物"],
    "题-300-结构化学基础-综合-习题C.15": ["Bragg方程", "体心立方堆积"],    # 系统消光
    "题-301-结构化学基础-综合-习题C.16": ["原子坐标参数", "分子晶体", "分数坐标"],  # 碘晶体
    "题-302-结构化学基础-综合-习题C.17": ["NaCl型结构", "晶胞"],
    "题-303-结构化学基础-综合-习题C.18": ["密堆积", "晶胞"],              # AB2 型 / 四面体空隙
    "题-304-结构化学基础-综合-习题C.19": ["六方密堆积"],                  # Er(A3) / La(A3')
    "题-305-结构化学基础-综合-习题C.20": ["对称元素", "晶体结构"],        # 金刚石 占有率 / 滑移面
    "题-306-结构化学基础-综合-习题C.21": ["原子坐标参数", "晶体结构", "对称元素"],  # 金刚石空间群
    "题-307-结构化学基础-综合-习题C.22": ["NiAs型结构", "六方密堆积"],
    "题-308-结构化学基础-综合-习题C.23": ["钙钛矿", "钙钛矿结构"],
}


def build_kp_index():
    """03-知识点 全部笔记名（Obsidian 按 basename 解析）"""
    names = set()
    root = os.path.join(VAULT, "03-知识点")
    for r, _, fs in os.walk(root):
        for fn in fs:
            if fn.endswith(".md"):
                names.add(fn[:-3])
    return names


def main():
    kp_index = build_kp_index()

    # 铁律 1：先全量校验，任何一个不存在就中止，绝不允许造新红链
    missing = []
    for stem, kps in ASSIGN.items():
        for k in kps:
            if k not in kp_index:
                missing.append((stem, k))
    if missing:
        print("!!! 以下知识点笔记不存在，已中止（不允许造新红链）：")
        for stem, k in missing:
            print(f"    {stem}  ->  {k}")
        sys.exit(1)
    print(f"知识点存在性校验通过：{len(ASSIGN)} 个文件，"
          f"{sum(len(v) for v in ASSIGN.values())} 处引用全部命中 03-知识点\n")

    ok, skipped, failed = 0, [], []
    for stem, kps in ASSIGN.items():
        # 定位文件
        path = None
        for base in (Struc, Clayden):
            cand = os.path.join(base, stem + ".md")
            if os.path.exists(cand):
                path = cand
                break
        if path is None:
            failed.append((stem, "文件未找到"))
            continue

        with open(path, encoding="utf-8", newline="") as f:
            lines = f.read().splitlines(keepends=True)

        new_val = "[" + ", ".join(f'"[[{k}]]"' for k in kps) + "]"
        hit = False
        for i, ln in enumerate(lines):
            body = ln.rstrip("\r\n")
            eol = ln[len(body):]
            if body.startswith("knowledge_points:"):
                old = body.split(":", 1)[1].strip()
                if old != "[]":
                    skipped.append((stem, f"非空({old})，跳过"))
                    hit = True
                    break
                lines[i] = f"knowledge_points: {new_val}{eol}"
                hit = True
                break
        if not hit:
            failed.append((stem, "未找到 knowledge_points 行"))
            continue
        if skipped and skipped[-1][0] == stem:
            continue

        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("".join(lines))
        ok += 1
        print(f"  OK  {stem}")
        print(f'      -> {new_val}')

    print(f"\n=== 改写 {ok} 个 / 跳过 {len(skipped)} / 失败 {len(failed)} ===")
    for s, why in skipped:
        print(f"  [跳过] {s}: {why}")
    for s, why in failed:
        print(f"  [失败] {s}: {why}")


if __name__ == "__main__":
    main()
