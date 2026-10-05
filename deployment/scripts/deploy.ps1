[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Region = $env:AWS_REGION,
    [string]$ApiUrl = $env:PUBLIC_API_URL,
    [string]$ImageTag = $env:IMAGE_TAG
)

$ErrorActionPreference = "Stop"
if ([string]::IsNullOrWhiteSpace($ApiUrl)) { throw "PUBLIC_API_URL is required." }
if ([string]::IsNullOrWhiteSpace($ImageTag)) { throw "IMAGE_TAG is required." }
& (Join-Path $PSScriptRoot "verify-aws.ps1") -Region $Region
if (-not $PSCmdlet.ShouldProcess("ECS services", "Deploy backend and frontend image tag $ImageTag")) { return }
& (Join-Path $PSScriptRoot "deploy-backend.ps1") -Region $Region -ImageTag $ImageTag
& (Join-Path $PSScriptRoot "deploy-frontend.ps1") -Region $Region -ImageTag $ImageTag -ApiUrl $ApiUrl

