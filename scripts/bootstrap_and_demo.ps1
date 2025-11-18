Param(
    [string]$Profile = $env:DEMO_PROFILE
)

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $repoRoot

function Write-Log {
    param([string]$Message)
    Write-Host "[BOOTSTRAP] $Message"
}

function Fail {
    param([string]$Message)
    Write-Host "[BOOTSTRAP] ERROR: $Message"
    exit 1
}

Write-Log "Detecting Python interpreter..."
$python = $null
foreach ($candidate in @("python", "python3")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $python = $candidate
        break
    }
}
if (-not $python) { Fail "Python 3.10+ is required." }

Write-Log "Checking Python version via $python"
$versionText = & $python -c "import sys; print('.'.join(map(str, sys.version_info[:3])))"
$version = [version]$versionText
if ($version.Major -ne 3 -or $version.Minor -lt 10 -or $version.Minor -gt 12) {
    Fail "Python version $versionText is not supported (need 3.10 - 3.12)."
}

$venvPath = Join-Path $repoRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Log "Creating virtual environment at $venvPath"
    & $python -m venv $venvPath
}

Write-Log "Activating virtual environment"
& "$venvPath\Scripts\Activate.ps1"

Write-Log "Installing project dependencies"
python -m pip install --upgrade pip | Out-Null
python -m pip install -e .[dev]

Write-Log "Sanity-checking package import"
python -c "import enterprise_synthetic_data_hub as pkg; print(getattr(pkg, '__version__', 'dev-build'))"

if (Get-Command make -ErrorAction SilentlyContinue) {
    Write-Log "Running make demo"
    make demo
}
else {
    Write-Log "Running Python fallback demo flow"
    python scripts\run_demo_flow.py
}

Write-Log "Bootstrap completed successfully."
