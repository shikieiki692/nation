# Phase 0 Step 4: 自动语义分桶（为 Phase 1 决策提供参考）
# 因为所有 189 条都被引 1 次，无法用频率分桶，改用命名特征分类

$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$VAULT = (Get-Location).Path
$v3Path = Join-Path $VAULT '00-首页\syllabus_gap_analysis_v3.json'
$outputPath = Join-Path $VAULT '00-首页\syllabus_gap_v3_categorized.md'

$v3Text = [System.IO.File]::ReadAllText($v3Path, [System.Text.UTF8Encoding]::new($false))
$v3Text = $v3Text.TrimStart([char]0xFEFF)
$v3 = $v3Text | ConvertFrom-Json

$missing = $v3 | Where-Object { $_.Type -eq '真正缺失' }

# 语义分桶规则
# 桶 A：核心概念（短名称、单一概念、人名反应、命名术语）
# 桶 B：题型/总结/比较类（含"总览/总表/总结/训练/对比/比较/网络/分类/整理/识别/判断/规则"等后缀）
# 桶 C：其他（中等长度的复合表述，需人工判断）

# 桶 B 关键词（题型/总结/汇总类）
$bucketBKeywords = @(
    '总览', '总表', '总结', '训练', '对比', '比较', '网络', '分类', '整理', '识别',
    '判断', '辨析', '总图', '初步分析', '专题', '示例', '应用', '记忆', '常见',
    '题型', '错题', '案例', '示意', '与', '及', '中的', '关系', '影响', '差异',
    '变化', '总.+', '.+总', '互译', '规范表达', '推断方法'
)

# 桶 A 关键词/特征（核心反应名 + 命名物质 + 关键术语）
$bucketAKeywords = @(
    # 人名反应/反应类型（一般 5 字以内或含 "反应"）
    'Friedel', 'Horner-Wadsworth-Emmons', 'Newman', 'Fischer', 'Haworth', 'Brønsted',
    'NiAs', 'ene反应', 'pKa',
    # 核心概念（化学基础术语）
    '化学平衡', '原子半径', '离子半径', '共价半径', '电极', '化学电源', '标态', '标准态',
    'σ键与π键', 'σ键', 'π键', '芳香性', '位置异构', '官能团异构', '碳链异构',
    '等温方程', '解离常数', '吸光度', '电子流动箭头规则', '化学位移', '分子离子峰',
    '吡咯', '呋喃', '噻吩', '糖类', '单糖', '糖苷', '还原糖', '异头碳', '异头体',
    '变旋现象', '肽键', '亚胺', '烯胺', '缩醛', '半缩醛', '三苯基膦', '碳骨架构建',
    '速率决定步骤', '位阻效应', '环张力', '过渡态与中间体', '碳正离子重排规律',
    '电子转移与电子对转移', '亲核与亲电', '离去基', '反轴', '稀土元素', '铂系元素',
    '过渡元素', '主族元素', '对角线规则', '元素周期表分区', '静电力', '溶剂极性', '溶剂类型',
    'Brønsted酸碱观点', '马氏规则与中间体稳定性', '位阻效应', '电子效应与稳定性',
    '构象与稳定性', '过氧酸氧化', '羰基烯化反应', '取代基定位效应', '活化基与钝化基'
)

function Get-Bucket($name) {
    # 桶 A 精确匹配
    foreach ($kw in $bucketAKeywords) {
        if ($name -eq $kw) { return 'A_核心概念' }
    }
    # 桶 A 前缀匹配（人名反应）
    foreach ($kw in @('Friedel', 'Newman', 'Fischer', 'Haworth', 'Brønsted', 'NiAs', 'Horner', 'Curtius', 'Swern', 'Dess', 'Corey', 'Wolff', 'Wittig', 'Arbuzov', 'Lawesson')) {
        if ($name -like "$kw*") { return 'A_核心概念' }
    }
    # 桶 B 后缀/关键词
    foreach ($kw in $bucketBKeywords) {
        if ($name -like "*$kw*") { return 'B_题型总结' }
    }
    # 默认桶 C
    return 'C_其他需人工'
}

# 分桶
$buckets = @{
    'A_核心概念' = @()
    'B_题型总结' = @()
    'C_其他需人工' = @()
}

foreach ($m in $missing) {
    $bucket = Get-Bucket $m.Link
    $buckets[$bucket] += $m
}

# 输出 Markdown 报告
$report = New-Object System.Text.StringBuilder
[void]$report.AppendLine('---')
[void]$report.AppendLine('title: 真正缺失 189 KP 语义分桶（Phase 0 输出）')
[void]$report.AppendLine('type: 系统')
[void]$report.AppendLine("generated_at: $(Get-Date -Format 'yyyy-MM-dd HH:mm')")
[void]$report.AppendLine('tags: [系统, 缺口, 分桶, 决策依据]')
[void]$report.AppendLine('---')
[void]$report.AppendLine('')
[void]$report.AppendLine('# 真正缺失 189 KP 语义分桶')
[void]$report.AppendLine('')
[void]$report.AppendLine('> Phase 0 校验产出：用语义规则自动分桶（因为被引次数全部=1，无法按频率分）。')
[void]$report.AppendLine('> 建议用户审阅后再进 Phase 2（批量创建）和 Phase 3（精简）。')
[void]$report.AppendLine('')
[void]$report.AppendLine('## 总览')
[void]$report.AppendLine('')
[void]$report.AppendLine('| 桶 | 数量 | 占比 | 建议处理 |')
[void]$report.AppendLine('|:---|---:|---:|---|')
$total = $missing.Count
foreach ($k in @('A_核心概念', 'B_题型总结', 'C_其他需人工')) {
    $cnt = $buckets[$k].Count
    $pct = [Math]::Round($cnt * 100.0 / $total, 1)
    $action = switch ($k) {
        'A_核心概念' { '✅ 批量创建 KP（Phase 2）' }
        'B_题型总结' { '✂️ 在考纲条目里折叠为段落（Phase 3）' }
        'C_其他需人工' { '👁️ 人工分诊（Phase 4）' }
    }
    [void]$report.AppendLine("| $k | $cnt | $pct% | $action |")
}
[void]$report.AppendLine("| **总计** | **$total** | **100%** | |")

foreach ($k in @('A_核心概念', 'B_题型总结', 'C_其他需人工')) {
    [void]$report.AppendLine('')
    [void]$report.AppendLine("## 桶 $k（$($buckets[$k].Count) 个）")
    [void]$report.AppendLine('')

    $byModule = $buckets[$k] | ForEach-Object {
        $parts = $_.Source -split '/'
        $mod = if ($parts.Count -ge 3) { "$($parts[1])/$($parts[2])" } else { $parts[1] }
        [PSCustomObject]@{
            Link = $_.Link
            Module = $mod
            Source = ($parts[-1] -replace '\.md$', '')
        }
    } | Group-Object Module | Sort-Object @{e='Count';desc=$true}

    foreach ($g in $byModule) {
        [void]$report.AppendLine("### $($g.Name)（$($g.Count)）")
        [void]$report.AppendLine('')
        foreach ($item in ($g.Group | Sort-Object Link)) {
            [void]$report.AppendLine("- ``$($item.Link)`` ← $($item.Source)")
        }
        [void]$report.AppendLine('')
    }
}

[System.IO.File]::WriteAllText($outputPath, $report.ToString(), [System.Text.UTF8Encoding]::new($false))

Write-Host "分桶结果：" -ForegroundColor Cyan
foreach ($k in @('A_核心概念', 'B_题型总结', 'C_其他需人工')) {
    Write-Host ("  {0,-18} : {1,3} 个" -f $k, $buckets[$k].Count)
}
Write-Host ""
Write-Host "报告: $outputPath" -ForegroundColor Green
