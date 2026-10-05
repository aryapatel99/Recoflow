[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Url
)

$ErrorActionPreference = "Stop"
$response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 15
if ($response.StatusCode -ne 200) { throw "Health check returned HTTP $($response.StatusCode)." }
Write-Host "Healthy: $Url"

