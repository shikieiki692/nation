# PowerShell script to add missing frontmatter fields
# Must be saved as UTF-8 with BOM for PowerShell to handle Chinese characters
$basePath = "C:\Obsidion\妙妙屋\04-题库\教材习题\无机化学例题与习题"
$files = Get-ChildItem -Path $basePath -Filter "*.md" -Recurse | Where-Object { $_.Name -ne "索引.md" } | Sort-Object FullName

$processed = 0
$skipped = 0
$errors = @()

foreach ($file in $files) {
    try {
        $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
        $lines = $content -split "`r?`n"

        # Find frontmatter boundaries
        $fmStart = -1
        $fmEnd = -1
        $dashCount = 0
        for ($i = 0; $i -lt $lines.Count; $i++) {
            $trimmed = $lines[$i].Trim()
            if ($trimmed -eq "---") {
                $dashCount++
                if ($dashCount -eq 1) { $fmStart = $i }
                if ($dashCount -eq 2) { $fmEnd = $i; break }
            }
        }

        if ($fmStart -eq -1 -or $fmEnd -eq -1) {
            $errors += "No frontmatter: $($file.Name)"
            $skipped++
            continue
        }

        # Extract frontmatter text
        $fmText = ($lines[$fmStart..$fmEnd] -join "`n")

        # Determine chapter number
        $chapter = 0
        if ($file.FullName -match 'Ch(\d+)') {
            $chapter = [int]$Matches[1]
        }

        # Determine exam_stage
        $examStage = "初赛"
        if ($chapter -ge 15) { $examStage = "决赛" }

        # Determine status
        $status = "已填充"
        $bodyText = ($lines[($fmEnd+1)..($lines.Count-1)] -join "`n")

        # Check for answer indicators in the body
        $hasAnswers = $false
        if ($bodyText -match '##\s*(解答|答案|解\b|解析|Answer|Solution)') { $hasAnswers = $true }
        if ($bodyText -match '###\s*(解|答案|解答)') { $hasAnswers = $true }
        if ($bodyText -match '>\s*\*\*解析\*\*') { $hasAnswers = $true }
        if ($bodyText -match '【答案】') { $hasAnswers = $true }
        if ($bodyText -match '## 答案') { $hasAnswers = $true }

        if ($hasAnswers) {
            $status = "已填充"
        } else {
            $isExercise = $file.DirectoryName -match '习题'
            if ($isExercise) {
                $status = "骨架"
            } else {
                $status = "已填充"
            }
        }

        # Check existing fields
        $hasStatus = $fmText -match '(?m)^\s*status:'
        $hasUpdated = $fmText -match '(?m)^\s*updated:'
        $hasTags = $fmText -match '(?m)^\s*tags:'
        $hasExamStage = $fmText -match '(?m)^\s*exam_stage:'

        # Build new fields
        $newFields = @()
        if (-not $hasStatus) { $newFields += "status: $status" }
        if (-not $hasUpdated) { $newFields += "updated: 2026-07-09" }
        if (-not $hasTags) { $newFields += "tags: [化竞, 教材习题, 无机化学例题与习题]" }
        if (-not $hasExamStage) { $newFields += "exam_stage: $examStage" }

        if ($newFields.Count -eq 0) {
            $skipped++
            continue
        }

        # Insert new fields before closing ---
        $insertText = "`n" + ($newFields -join "`n")

        # Build new content
        $beforePart = $lines[0..($fmEnd - 1)]
        $afterPart = $lines[$fmEnd..($lines.Count - 1)]

        $newContent = ($beforePart -join "`n") + $insertText + "`n" + ($afterPart -join "`n")

        [System.IO.File]::WriteAllText($file.FullName, $newContent, (New-Object System.Text.UTF8Encoding $false))
        $processed++
    }
    catch {
        $errors += "Error: $($file.Name): $($_.Exception.Message)"
    }
}

Write-Host "`n=== Summary ==="
Write-Host "Total files: $($files.Count)"
Write-Host "Processed: $processed"
Write-Host "Skipped: $skipped"
Write-Host "Errors: $($errors.Count)"
if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Host "  $_" }
}
