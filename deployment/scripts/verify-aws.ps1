[CmdletBinding()]
param(
    [string]$Region = $env:AWS_REGION
)

$ErrorActionPreference = "Stop"
if ([string]::IsNullOrWhiteSpace($Region)) { throw "AWS region is required. Set AWS_REGION or -Region." }

Write-Host "Checking AWS identity in region $Region..."
aws sts get-caller-identity --region $Region | Out-Host
if ($LASTEXITCODE -ne 0) { throw "AWS authentication failed." }

