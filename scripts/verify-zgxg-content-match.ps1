# zgxg- 图片内容匹配验证脚本
# 用法: .\scripts\verify-zgxg-content-match.ps1
# 功能: 检查zgxg-文件名关键词是否与使用上下文匹配

param(
    [string]$VaultRoot = "C:\Obsidion\妙妙屋",
    [switch]$Quiet
)

$ErrorActionPreference = "Continue"
$date = Get-Date -Format "yyyy-MM-dd"

# 关键词映射：文件名关键词 -> 期望的上下文关键词
$keywordMap = @{
    # 化学动力学
    "arrhenius" = @("arrhenius", "活化能", "速率常数", "温度", "动力学")
    "autocatalysis" = @("自催化", "autocatalysis", " autocat")
    "catalysis" = @("催化", "催化剂", "catalysis")
    "rate-equations" = @("速率方程", "rate equation", "反应级数")
    "instantaneous-rate" = @("瞬时速率", "instantaneous", "切线")
    "five-types-vt" = @("v-t曲线", "速率-时间", "浓度-时间")
    "dual-arrhenius" = @("双arrhenius", "dual", "转折")
    "reaction-progress-energy" = @("反应进程", "能量图", "势能", "反应速率", "活化能")

    # 热力学
    "thermodynamic-path" = @("热力学路径", "状态函数", "路径")
    "volume-work" = @("体积功", "pV", "功")
    "joule-free-expansion" = @("joule", "自由膨胀", "绝热")
    "pv-multi-step" = @("pV", "多步", "膨胀")
    "reversible-pv" = @("可逆", "pV", "膨胀")
    "hess-law" = @("盖斯", "hess", "反应热")
    "born-haber" = @("born-haber", "晶格能", "循环")

    # 电化学
    "electrode-double-layer" = @("双电层", "电极", "界面")
    "standard-hydrogen-electrode" = @("标准氢电极", "she", "电极电位")
    "decomposition-voltage" = @("分解电压", "电解", "iv曲线")
    "mno4-latimer" = @("latimer", "mno4", "锰", "氧化还原")

    # 酸碱滴定
    "strong-acid-base-titration" = @("强酸", "强碱", "滴定", "ph")
    "strong-vs-weak-acid" = @("强酸", "弱酸", "对比", "滴定")
    "weak-acid-ka-titration" = @("弱酸", "ka", "滴定", "缓冲")
    "indicator-structures" = @("指示剂", "indicator", "结构")
    "distribution-coefficient" = @("分布系数", "distribution", "α")

    # 晶体场理论
    "octahedral-cft-splitting" = @("八面体", "晶体场", "分裂", "d轨道")
    "tetrahedral-cft-splitting" = @("四面体", "晶体场", "分裂")
    "high-spin-electron-config" = @("高自旋", "低自旋", "电子排布", "构型")
    "jahn-teller" = @("jahn-teller", "姜-泰勒", "畸变")
    "d-orbital-shapes" = @("d轨道", "形状", "角度分布")
    "pauling-cotton" = @("pauling", "cotton", "能级", "电负性")

    # 分子轨道
    "h2-mo-energy" = @("h2", "分子轨道", "mo", "氢")
    "he2-mo-energy" = @("he2", "分子轨道", "氦")
    "o2f2-mo-energy" = @("o2", "f2", "分子轨道", "氧")
    "hf-mo-energy" = @("hf", "分子轨道", "氟化氢")
    "pi-mo-formation" = @("π", "分子轨道", "形成")
    "orbital-symmetry-matching" = @("轨道对称性", "匹配", "对称")

    # 杂化轨道
    "hybridization-types" = @("杂化", "sp", "类型")
    "sp3-hybridization" = @("sp3", "杂化", "四面体")

    # VSEPR
    "vsepr-summary" = @("vsepr", "价层", "电子对")
    "vsepr-classification" = @("vsepr", "分类", "构型")

    # 晶体结构
    "ionic-crystal-classification" = @("离子晶体", "分类", "结构类型")
    "ionic-crystal-properties" = @("离子晶体", "性质", "熔点")
    "nacl-crystal" = @("nacl", "氯化钠", "面心立方")
    "cscl-crystal" = @("cscl", "氯化铯", "简单立方")
    "zns-sphalerite" = @("zns", "闪锌矿", "硫化锌")
    "batio3-perovskite" = @("batio3", "钙钛矿", "钛酸钡")
    "graphite-layered" = @("石墨", "层状", "碳")
    "crystal-lattice-motif" = @("点阵", "结构基元", "晶体")
    "crystal-system-point-group" = @("晶系", "点群", "对称")

    # 元素性质
    "periodic-table-blocks" = @("周期表", "分区", "s区", "p区")
    "electronegativity-periodic" = @("电负性", "周期", "趋势")
    "electron-affinity" = @("电子亲合能", "亲和能", "趋势")
    "first-ionization-energy" = @("电离能", "第一", "趋势")
    "na-penetration" = @("穿透", "渗透", "na", "钠")

    # 配位化学
    "cis-trans-platinum" = @("顺铂", "反铂", "异构", "pt")
    "coordination-bond" = @("配位键", "形成", "配位")
    "edta-chelate" = @("edta", "螯合", "配合物")
    "fac-mer-isomers" = @("fac", "mer", "异构")
    "optical-isomers" = @("光学异构", "旋光", "对映")

    # 其他
    "slater-calculation" = @("slater", "计算", "轨道能量")
    "lewis-structures" = @("lewis", "路易斯", "结构式")
    "molecular-symmetry" = @("对称", "对称性", "群")
    "wavefunction-vs-electron-cloud" = @("波函数", "电子云", "对比")
    "water-hydrogen-bond" = @("水", "氢键", "簇")
}

# 1. 读取所有zgxg-引用
$mdFiles = Get-ChildItem $VaultRoot -Filter "*.md" -Recurse -File
$references = @()

foreach ($f in $mdFiles) {
    $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }

    $relativePath = $f.FullName.Substring($VaultRoot.Length + 1)

    # 匹配所有zgxg-引用
    $matches = [regex]::Matches($content, 'zgxg-([a-zA-Z0-9_-]+)\.jpg')
    foreach ($m in $matches) {
        $filename = "zgxg-$($m.Groups[1].Value).jpg"
        $keyword = $m.Groups[1].Value

        # 获取引用所在的段落上下文（前后500字符）
        $pos = $m.Index
        $start = [Math]::Max(0, $pos - 500)
        $end = [Math]::Min($content.Length, $pos + $filename.Length + 500)
        $context = $content.Substring($start, $end - $start).ToLower()

        # 也检查整个文件的标题和frontmatter
        $fileContext = $content.ToLower()

        $references += [PSCustomObject]@{
            File = $relativePath
            Image = $filename
            Keyword = $keyword
            Context = $context
        }
    }
}

# 2. 分析匹配度
$matches = @()
$mismatches = @()
$uncertain = @()

foreach ($ref in $references) {
    $keyword = $ref.Keyword
    $context = $ref.Context

    if ($keywordMap.ContainsKey($keyword)) {
        $expectedKeywords = $keywordMap[$keyword]
        $found = $false

        # 先检查局部上下文
        foreach ($ek in $expectedKeywords) {
            if ($context.Contains($ek.ToLower())) {
                $found = $true
                break
            }
        }

        # 如果局部上下文没找到，检查整个文件
        if (-not $found) {
            foreach ($ek in $expectedKeywords) {
                if ($fileContext.Contains($ek.ToLower())) {
                    $found = $true
                    break
                }
            }
        }

        if ($found) {
            $matches += $ref
        } else {
            $mismatches += $ref
        }
    } else {
        $uncertain += $ref
    }
}

# 3. 输出结果
if (-not $Quiet) {
    Write-Host "=== zgxg- 图片内容匹配验证 ===" -ForegroundColor Cyan
    Write-Host "时间: $date"
    Write-Host "总引用数: $($references.Count)"
    Write-Host "匹配: $($matches.Count)" -ForegroundColor Green
    Write-Host "不匹配: $($mismatches.Count)" -ForegroundColor $(if ($mismatches.Count -eq 0) { "Green" } else { "Yellow" })
    Write-Host "无法判断: $($uncertain.Count)" -ForegroundColor Gray
    Write-Host ""

    if ($mismatches.Count -gt 0) {
        Write-Host "=== 潜在不匹配 ===" -ForegroundColor Yellow
        $mismatches | ForEach-Object {
            Write-Host "  $($_.Image) in $($_.File)" -ForegroundColor Yellow
        }
        Write-Host ""
    }
}

# 返回结果
return @{
    Total = $references.Count
    Matched = $matches.Count
    Mismatched = $mismatches.Count
    Uncertain = $uncertain.Count
    Mismatches = $mismatches
}
