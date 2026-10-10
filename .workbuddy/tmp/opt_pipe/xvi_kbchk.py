import os, json
base = r"03-知识点"
idx = {}
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".md"):
            stem = f[:-3]
            rel = os.path.join(root, f).replace("\\", "/")
            idx.setdefault(stem, []).append(rel)
json.dump(idx, open(r".workbuddy/tmp/opt_pipe/xvi_kbidx.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=0)
print("total md:", sum(len(v) for v in idx.values()), "unique stems:", len(idx))

names = ["配合物","MOF材料","配位数","过渡金属羰基化合物","18电子规则","Langmuir吸附等温式",
"晶体密度公式","晶体结构","晶体对称性","超分子作用力","晶胞","密堆积","分子极性与分子间作用力",
"晶体场分裂与磁性","点群初步","Gibbs自由能","Clapeyron方程","相变热力学","分光光度法","溶度积",
"误差","数据处理","分子轨道理论","化学平衡","磁矩","金属有机化学基础","络合滴定","条件稳定常数",
"分布分数","缓冲溶液","标准电极电势","Nernst方程","能带理论","点阵类型","晶胞投影图分析",
"van't Hoff方程","多重平衡","晶体场理论","克拉佩隆方程","配位化学"]
for n in names:
    v = idx.get(n)
    print(("OK   " if v else "MISS ") + n + (("  -> " + v[0]) if v else ""))
