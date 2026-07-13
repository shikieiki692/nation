$ErrorActionPreference = 'Stop'

$bundledPython = 'C:\Users\蕾赛\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$pythonExe = $null
$pythonPrefixArgs = @()

if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonExe = 'python'
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonExe = 'py'
    $pythonPrefixArgs = @('-3.12')
} elseif (Test-Path -LiteralPath $bundledPython) {
    $pythonExe = $bundledPython
} else {
    throw 'No Python runtime available for Word export.'
}

$files = @(
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\2026-06-23-化学计量与计算规范.md',
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\2026-06-23-方程式书写专项.md',
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\2026-06-23-气体基础.md',
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\溶液与相图-超级充实版（自学完整）.md',
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\热力学初步-超级充实版（自学完整）.md',
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\化学动力学-超级充实版（自学完整）.md',
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\化学平衡-超级充实版（自学完整）.md',
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\酸碱理论-超级充实版（自学完整）.md',
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\2026-06-23-沉淀溶解平衡.md',
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\2026-06-23-水中的几种平衡.md',
    'C:\Obsidion\妙妙屋\04-课件\学生讲义\2026-06-23-电化学基础.md'
) 

$script = 'build-all-handout-docx.py'

Push-Location -LiteralPath $PSScriptRoot
try {
    foreach ($file in $files) {
        Write-Host ('[START] ' + (Split-Path $file -Leaf))
        & $pythonExe @pythonPrefixArgs $script --path $file --word-clean
        if ($LASTEXITCODE -ne 0) {
            throw "Word generation failed: $file"
        }
    }
} finally {
    Pop-Location
}

Write-Host '[DONE] chemistry principle round 1 word clean batch complete'
