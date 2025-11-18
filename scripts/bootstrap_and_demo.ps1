Param(
    [string]$Profile = $env:DEMO_PROFILE
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    $script:CurrentStep++
    Write-Host "[BOOTSTRAP $($script:CurrentStep)/$($script:TotalSteps)] $Message"
}

function Fail {
    param([string]$Message)
    Write-Host "[BOOTSTRAP] ERROR: $Message"
    exit 1
}

function Find-RepoRoot {
    param([string]$StartPath)
    $path = Resolve-Path $StartPath
    while ($path -and $path -ne [System.IO.Path]::GetPathRoot($path)) {
        if (Test-Path (Join-Path $path 'pyproject.toml') -and (Test-Path (Join-Path $path 'src'))) {
            return $path
        }
        $path = Split-Path $path -Parent
    }
    return $null
}

$script:TotalSteps = 8
$script:CurrentStep = 0

if ($PSCommandPath) {
    $repoRoot = Resolve-Path (Join-Path (Split-Path $PSCommandPath) "..")
} else {
    $repoRoot = Find-RepoRoot (Get-Location)
    if (-not $repoRoot) { Fail "Unable to locate the repository root. Clone the repo first." }
}
Set-Location $repoRoot

if (-not [Console]::IsInputRedirected) {
    Write-Host "[BOOTSTRAP] Detected interactive execution."
} else {
    Write-Host "[BOOTSTRAP] Detected non-interactive execution (Invoke-WebRequest pipe)."
}

Write-Step "Checking Python version..."
$python = $null
foreach ($candidate in @("python", "python3")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $python = $candidate
        break
    }
}
if (-not $python) { Fail "Python 3.10+ is required." }
$versionText = & $python -c "import sys; print('.'.join(map(str, sys.version_info[:3])))"
$version = [version]$versionText
if ($version.Major -ne 3 -or $version.Minor -lt 10 -or $version.Minor -gt 12) {
    Fail "Python version $versionText is not supported (need 3.10 - 3.12)."
}

Write-Step "Validating pip availability..."
try {
    & $python -m pip --version | Out-Null
} catch {
    Fail "pip is not available for $python"
}

Write-Step "Checking git installation..."
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Fail "git is required for the demo."
}

Write-Step "Checking download tools (curl/wget/iwr)..."
if (-not (Get-Command curl -ErrorAction SilentlyContinue) -and -not (Get-Command wget -ErrorAction SilentlyContinue) -and -not (Get-Command Invoke-WebRequest -ErrorAction SilentlyContinue)) {
    Fail "Install curl, wget, or ensure Invoke-WebRequest is available."
}

$configPath = Join-Path $repoRoot "config/demo.yaml"
Write-Step "Validating config/demo.yaml..."
if (-not (Test-Path $configPath)) {
    Fail "Missing $configPath (did you clone the full repo?)."
}

$venvPath = Join-Path $repoRoot ".venv"
Write-Step "Preparing virtual environment (.venv)..."
if (-not (Test-Path $venvPath)) {
    & $python -m venv $venvPath
}
& "$venvPath\Scripts\Activate.ps1"

Write-Step "Installing project dependencies..."
python -m pip install --upgrade pip | Out-Null
python -m pip install -e .[dev]

Write-Step "Running guided demo..."
if ($Profile) { $env:DEMO_PROFILE = $Profile }
if (Get-Command make -ErrorAction SilentlyContinue) {
    make demo
} else {
    python scripts\run_demo_flow.py
}

Write-Host "[BOOTSTRAP] Bootstrap completed successfully."
