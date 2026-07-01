param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$InputPath,

    [Parameter(Position = 1)]
    [string]$OutputDir,

    [int]$Width = 1600,

    [int]$Height = 2000,

    [Nullable[int]]$Dpi = $null,

    [switch]$EmitPdf,

    [switch]$VerboseRender
)

[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [Console]::OutputEncoding
$env:PYTHONIOENCODING = 'utf-8'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$script = Join-Path $scriptDir 'render_docx_windows.py'

function Resolve-PythonRuntime {
    $candidates = @()
    if ($env:CODEX_BUNDLED_PYTHON) { $candidates += $env:CODEX_BUNDLED_PYTHON }
    if ($env:CODEX_PYTHON) { $candidates += $env:CODEX_PYTHON }
    if ($env:USERPROFILE) {
        $candidates += (Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe')
    }

    foreach ($candidate in $candidates) {
        if (-not [string]::IsNullOrWhiteSpace($candidate) -and (Test-Path -LiteralPath $candidate)) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCmd) {
        return $pythonCmd.Source
    }

    throw "Python runtime not found. Set CODEX_BUNDLED_PYTHON/CODEX_PYTHON or install python."
}

$python = Resolve-PythonRuntime

if (-not (Test-Path -LiteralPath $InputPath)) {
    throw "Input file not found: $InputPath"
}

$inputItem = Get-Item -LiteralPath $InputPath
$resolvedInput = $inputItem.FullName

if ([string]::IsNullOrWhiteSpace($OutputDir)) {
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($inputItem.Name)
    $OutputDir = Join-Path $inputItem.DirectoryName ($stem + '_render')
}

$resolvedOutput = [System.IO.Path]::GetFullPath($OutputDir)

$args = @(
    $script
    $resolvedInput
    '--output_dir'
    $resolvedOutput
    '--width'
    $Width
    '--height'
    $Height
)

if ($Dpi -ne $null) {
    $args += @('--dpi', [string]$Dpi)
}

if ($EmitPdf) {
    $args += '--emit_pdf'
}

if ($VerboseRender) {
    $args += '--verbose'
}

& $python @args

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Render complete"
Write-Host "Input : $resolvedInput"
Write-Host "Output: $resolvedOutput"
