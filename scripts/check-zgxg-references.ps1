# zgxg- 图片引用完整性检查脚本
# 用法: .\scripts\check-zgxg-references.ps1
# 输出: 控制台报告 + 09-审计报告/zgxg-引用检查-YYYY-MM-DD.md

param(
    [string]$VaultRoot = "C:\Obsidion\妙妙屋",
    [switch]$Quiet
)

$ErrorActionPreference = "Continue"
$date = Get-Date -Format "yyyy-MM-dd"
$reportPath = Join-Path $VaultRoot "09-审计报告\zgxg-引用检查-$date.md"

# 统计变量
$stats = @{
    TotalMediaFiles = 0
    ReferencedFiles = 0
    UnreferencedFiles = 0
    BrokenRefs = 0
    TotalRefs = 0
    FilesByCategory = @{}
}
$referencedFiles = @{}
$brokenRefs = @()

# 1. 获取media/中所有zgxg-文件
$mediaDir = Join-Path $VaultRoot "media"
$mediaFiles = Get-ChildItem $mediaDir -Filter "zgxg-*.jpg" -File -ErrorAction SilentlyContinue
$stats.TotalMediaFiles = $mediaFiles.Count

if (-not $Quiet) {
    Write-Host "=== zgxg- 图片引用完整性检查 ===" -ForegroundColor Cyan
    Write-Host "时间: $date"
    Write-Host "media/中zgxg-文件: $($mediaFiles.Count)"
    Write-Host ""
}

# 2. 读取所有markdown文件内容
$mdFiles = Get-ChildItem $VaultRoot -Filter "*.md" -Recurse -File
$allContent = @{}
foreach ($f in $mdFiles) {
    $relativePath = $f.FullName.Substring($VaultRoot.Length + 1)
    $allContent[$relativePath] = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
}

# 3. 检查所有引用是否指向存在的文件，并记录被引用的文件
$brokenRefs = @()
foreach ($mdPath in $allContent.Keys) {
    $content = $allContent[$mdPath]
    if (-not $content) { continue }

    # 匹配所有media/zgxg-xxx.jpg引用（不关心格式）
    $pattern = 'media/(zgxg-[a-zA-Z0-9_-]+\.jpg)'
    $matches = [regex]::Matches($content, $pattern)
    foreach ($m in $matches) {
        $stats.TotalRefs++
        $imgFile = $m.Groups[1].Value
        $imgPath = Join-Path $mediaDir $imgFile

        if (-not (Test-Path $imgPath)) {
            $brokenRefs += [PSCustomObject]@{
                MdFile = $mdPath
                ImageFile = $imgFile
            }
            $stats.BrokenRefs++
        }

        # 记录被引用的文件
        if (-not $referencedFiles.ContainsKey($imgFile)) {
            $referencedFiles[$imgFile] = @()
        }
        if ($referencedFiles[$imgFile] -notcontains $mdPath) {
            $referencedFiles[$imgFile] += $mdPath
        }
    }
}

# 4. 检查每个zgxg-文件是否被引用
$unreferenced = @()
$referencedList = @()

foreach ($mediaFile in $mediaFiles) {
    $filename = $mediaFile.Name

    if ($referencedFiles.ContainsKey($filename)) {
        $stats.ReferencedFiles++
        $referencedList += [PSCustomObject]@{
            MediaFile = $filename
            MdFiles = ($referencedFiles[$filename] -join ", ")
        }
    } else {
        $stats.UnreferencedFiles++
        $unreferenced += $mediaFile
    }
}

# 5. 输出报告
if (-not $Quiet) {
    Write-Host "=== 检查结果 ===" -ForegroundColor Green
    Write-Host "media/中文件总数: $($stats.TotalMediaFiles)"
    Write-Host "被引用文件数: $($stats.ReferencedFiles)" -ForegroundColor Green
    Write-Host "未被引用文件数: $($stats.UnreferencedFiles)" -ForegroundColor Yellow
    Write-Host "Broken引用数: $($stats.BrokenRefs)" -ForegroundColor $(if ($stats.BrokenRefs -eq 0) { "Green" } else { "Red" })
    Write-Host "总引用次数: $($stats.TotalRefs)"
    Write-Host ""

    if ($unreferenced.Count -gt 0) {
        Write-Host "=== 未被引用的文件 ===" -ForegroundColor Yellow
        $unreferenced | Sort-Object Name | ForEach-Object {
            Write-Host "  $($_.Name) ($([math]::Round($_.Length/1KB))KB)"
        }
        Write-Host ""
    }

    if ($brokenRefs.Count -gt 0) {
        Write-Host "=== Broken引用 ===" -ForegroundColor Red
        $brokenRefs | ForEach-Object {
            Write-Host "  $($_.MdFile) -> $($_.ImageFile)"
        }
        Write-Host ""
    }

    if ($stats.BrokenRefs -eq 0) {
        Write-Host "✅ 所有引用完整，零broken" -ForegroundColor Green
    }
}

# 6. 写入报告文件
$report = @"
# zgxg- 图片引用检查报告

> 检查时间：$date
> 扫描范围：全库 .md 文件

## 统计摘要

| 指标 | 数值 |
|:---|:---:|
| media/ 中 zgxg- 文件总数 | $($stats.TotalMediaFiles) |
| 被引用文件数 | $($stats.ReferencedFiles) |
| 未被引用文件数 | $($stats.UnreferencedFiles) |
| Broken 引用数 | $($stats.BrokenRefs) |
| 总引用次数 | $($stats.TotalRefs) |

## 检查结果

$(if ($stats.BrokenRefs -eq 0) { "✅ **所有引用完整，零broken**" } else { "❌ **发现 $($stats.BrokenRefs) 个broken引用**" })

## 未被引用的文件 ($($unreferenced.Count)个)

$(if ($unreferenced.Count -gt 0) {
    "| 文件名 | 大小 |"
    "|:---|:---:|"
    ($unreferenced | Sort-Object Name | ForEach-Object {
        "| $($_.Name) | $([math]::Round($_.Length/1KB))KB |"
    }) -join "`n"
} else {
    "无"
})

## Broken引用详情

$(if ($brokenRefs.Count -gt 0) {
    "| 文件 | 引用的图片 |"
    "|:---|:---|"
    ($brokenRefs | ForEach-Object {
        "| $($_.MdFile) | $($_.ImageFile) |"
    }) -join "`n"
} else {
    "无"
})
"@

$report | Out-File -FilePath $reportPath -Encoding UTF8
if (-not $Quiet) {
    Write-Host "报告已保存: $reportPath" -ForegroundColor Cyan
}
