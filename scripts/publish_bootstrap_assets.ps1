#!/usr/bin/env pwsh
param()

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$bootstrapSh = Join-Path $repoRoot "scripts/bootstrap_and_demo.sh"
$bootstrapPs1 = Join-Path $repoRoot "scripts/bootstrap_and_demo.ps1"
$stagingDir = Join-Path $repoRoot "dist/bootstrap"

$required = @($bootstrapSh, $bootstrapPs1)
foreach ($file in $required) {
    if (-not (Test-Path $file)) {
        Write-Error "Missing required script: $file"
        exit 1
    }
}

New-Item -ItemType Directory -Force -Path $stagingDir | Out-Null
$stagedSh = Join-Path $stagingDir (Split-Path $bootstrapSh -Leaf)
$stagedPs1 = Join-Path $stagingDir (Split-Path $bootstrapPs1 -Leaf)
Copy-Item $bootstrapSh -Destination $stagedSh -Force
Copy-Item $bootstrapPs1 -Destination $stagedPs1 -Force

$releaseTag = gh release list --limit 1 --json tagName --jq '.[0].tagName' 2>$null
if ([string]::IsNullOrWhiteSpace($releaseTag)) {
    Write-Error "No release found. Create a release (e.g., v0.1.0) before uploading bootstrap assets."
    exit 1
}

& gh release upload $releaseTag $stagedSh $stagedPs1 --clobber
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Output "Bootstrap distribution updated:"
Write-Output "- $(Split-Path $bootstrapSh -Leaf)"
Write-Output "- $(Split-Path $bootstrapPs1 -Leaf)"
