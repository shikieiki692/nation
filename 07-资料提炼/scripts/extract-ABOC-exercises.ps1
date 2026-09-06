# ABOC剩余习题提取脚本
# 从ABOC源文件中提取自学练习和章末习题

$sourceFile1 = "C:\Obsidion\妙妙屋\mineru\03-教材书籍\ABOC有机化学\ABOC202505_1-200.md"
$sourceFile2 = "C:\Obsidion\妙妙屋\mineru\03-教材书籍\ABOC有机化学\ABOC202505_200-397.md"
$outputDir = "C:\Obsidion\妙妙屋\04-题库\教材习题\ABOC"

# 读取源文件
$content1 = Get-Content $sourceFile1 -Raw -Encoding UTF8
$content2 = Get-Content $sourceFile2 -Raw -Encoding UTF8

# 合并内容
$allContent = $content1 + "`n" + $content2

# 提取自学练习的正则表达式
$exercisePattern = "(?m)^自学练习 (\d+\.\d+(?:\.\d+)?(?:-\d+)?)\s+(.*?)(?=^自学练习 \d|^# |^$|\Z)"

# 提取章末习题的正则表达题
$chapterExercisePattern = "(?m)^# T(\d+)\.\s+(.*?)(?=^# T\d|^# |^$|\Z)"

# 提取所有自学练习
$exercises = [regex]::Matches($allContent, $exercisePattern)

Write-Host "Found $($exercises.Count) self-study exercises"

# 提取所有章末习题
$chapterExercises = [regex]::Matches($allContent, $chapterExercisePattern)

Write-Host "Found $($chapterExercises.Count) chapter-end exercises"

# 定义已提取的练习编号
$extractedExercises = @(
    "1.1.1", "1.2.2-1", "1.3.1-3",  # Ch1
    "2.2.2", "2.3", "2.4-2",  # Ch2
    "3.1.2", "3.4",  # Ch3
    "4.1", "4.5.1",  # Ch4
    "5.1", "5.3",  # Ch5
    "6.1", "6.5.1",  # Ch6
    "7.2.1-1", "7.2-1",  # Ch7
    "8.6",  # Ch8
    "9.2-2"  # Ch9
)

# 定义已提取的章末习题
$extractedChapterExercises = @(
    "1-T1", "2-T3", "3-T3", "4-T3", "5-T3", "6-T3", "7-T3", "8-T3", "9-T3"
)

# 计数器
$nextNumber = 80  # 从080开始

# 处理自学练习
foreach ($exercise in $exercises) {
    $exerciseId = $exercise.Groups[1].Value
    $exerciseContent = $exercise.Groups[2].Value

    # 检查是否已提取
    if ($extractedExercises -contains $exerciseId) {
        continue
    }

    # 确定章节
    $chapter = [math]::Floor([double]$exerciseId.Split('.')[0])

    # 创建文件名
    $safeContent = ($exerciseContent -replace '[^\w]', ' ').Trim()
    $shortContent = $safeContent.Substring(0, [math]::Min(30, $safeContent.Length))
    $fileName = "题-$($nextNumber.ToString("D3"))-ABOC-Ch$chapter-$exerciseId-$shortContent.md"

    # 创建文件内容
    $fileContent = @"
---
title: $fileName
type: 题目
source: ABOC 第$chapter章 自学练习（ARX's Basic Organic Chemistry 第3版）
subject: 有机化学
module: 基础要求-有机化学
submodule: Ch.$chapter
question_type: 机理书写题
difficulty: 2
teaching_level: 巩固
exam_stage: 初赛
syllabus_codes: ["$(31 + $chapter - 1)"]
knowledge_points: ["[[]]"]
tags: [化竞, ABOC, 有机化学]
aliases: [ABOC-Ch$chapter-$exerciseId]
updated: $(Get-Date -Format "yyyy-MM-dd")
---

# 题-$($nextNumber.ToString("D3"))：$($exerciseContent.Trim().Substring(0, [math]::Min(50, $exerciseContent.Trim().Length)))

> **来源**：ABOC 第$chapter章 自学练习 $exerciseId
> **难度**：⭐⭐
> **教学层级**：巩固

---

## 题目

$exerciseContent

---

## 答案

（答案见 [[提炼-ABOC-第12章-习题解析]]）

---

## 解题思路

（待补充）

---

## 知识点

- [[]]

---

## 相关题目

- [[题-062-ABOC-Ch1-1.1.1-离去基判断]]
- [[题-063-ABOC-Ch1-1.2.2-1-S-C反键轨道与端基效应]]
- [[题-064-ABOC-Ch1-1.3.1-3-金刚烷合成（碳正离子重排）]]
"@

    # 写入文件
    $filePath = Join-Path $outputDir $fileName
    $fileContent | Out-File -FilePath $filePath -Encoding UTF8

    Write-Host "Created: $fileName"
    $nextNumber++
}

# 处理章末习题
foreach ($exercise in $chapterExercises) {
    $exerciseNumber = $exercise.Groups[1].Value
    $exerciseContent = $exercise.Groups[2].Value

    # 检查是否已提取
    $chapterNum = [math]::Ceiling([double]$exerciseNumber / 10)
    if ($extractedChapterExercises -contains "$chapterNum-T$exerciseNumber") {
        continue
    }

    # 确定章节（根据题号范围）
    if ($exerciseNumber -le 13) { $chapter = 1 }
    elseif ($exerciseNumber -le 22) { $chapter = 2 }
    elseif ($exerciseNumber -le 31) { $chapter = 3 }
    elseif ($exerciseNumber -le 40) { $chapter = 4 }
    elseif ($exerciseNumber -le 49) { $chapter = 5 }
    elseif ($exerciseNumber -le 58) { $chapter = 6 }
    elseif ($exerciseNumber -le 64) { $chapter = 7 }
    elseif ($exerciseNumber -le 67) { $chapter = 8 }
    else { $chapter = 9 }

    # 创建文件名
    $safeContent = ($exerciseContent -replace '[^\w]', ' ').Trim()
    $shortContent = $safeContent.Substring(0, [math]::Min(30, $safeContent.Length))
    $fileName = "题-$($nextNumber.ToString("D3"))-ABOC-Ch$chapter-T$exerciseNumber-$shortContent.md"

    # 创建文件内容
    $fileContent = @"
---
title: $fileName
type: 题目
source: ABOC 第$chapter章 章末习题（ARX's Basic Organic Chemistry 第3版）
subject: 有机化学
module: 基础要求-有机化学
submodule: Ch.$chapter
question_type: 合成设计题
difficulty: 3
teaching_level: 拓展
exam_stage: 初赛
syllabus_codes: ["$(31 + $chapter - 1)"]
knowledge_points: ["[[]]"]
tags: [化竞, ABOC, 有机化学]
aliases: [ABOC-Ch$chapter-T$exerciseNumber]
updated: $(Get-Date -Format "yyyy-MM-dd")
---

# 题-$($nextNumber.ToString("D3"))：$($exerciseContent.Trim().Substring(0, [math]::Min(50, $exerciseContent.Trim().Length)))

> **来源**：ABOC 第$chapter章 章末习题 T$exerciseNumber
> **难度**：⭐⭐⭐
> **教学层级**：拓展

---

## 题目

$exerciseContent

---

## 答案

（答案见 [[提炼-ABOC-第12章-习题解析]]）

---

## 解题思路

（待补充）

---

## 知识点

- [[]]

---

## 相关题目

- [[题-053-ABOC-Ch1-T1-金刚烷合成]]
- [[题-054-ABOC-Ch2-T3-硫叶立德vs半缩硫醛选择性]]
- [[题-055-ABOC-Ch3-T3-特殊氧化烯烃邻二醇切断]]
"@

    # 写入文件
    $filePath = Join-Path $outputDir $fileName
    $fileContent | Out-File -FilePath $filePath -Encoding UTF8

    Write-Host "Created: $fileName"
    $nextNumber++
}

Write-Host "Done! Created $($nextNumber - 80) files"