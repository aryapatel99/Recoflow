[CmdletBinding()]
param(
    [string]$Region = $env:AWS_REGION,
    [string]$Repository = $env:ECR_FRONTEND_REPOSITORY,
    [string]$Cluster = $env:ECS_CLUSTER,
    [string]$Service = $env:ECS_FRONTEND_SERVICE,
    [string]$ImageTag = $env:IMAGE_TAG,
    [Parameter(Mandatory = $true)]
    [string]$ApiUrl
)

$ErrorActionPreference = "Stop"
foreach ($pair in @{"Region"=$Region; "Repository"=$Repository; "Cluster"=$Cluster; "Service"=$Service; "ImageTag"=$ImageTag}.GetEnumerator()) {
    if ([string]::IsNullOrWhiteSpace($pair.Value)) { throw "$($pair.Key) is required." }
}

$account = (aws sts get-caller-identity --query Account --output text --region $Region)
if ($LASTEXITCODE -ne 0) { throw "AWS authentication failed." }
$registry = "$account.dkr.ecr.$Region.amazonaws.com"
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $registry
if ($LASTEXITCODE -ne 0) { throw "ECR login failed." }

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\")).Path
$image = "$registry/$Repository`:$ImageTag"
$env:NEXT_PUBLIC_API_URL = $ApiUrl
docker build -f (Join-Path $root "deployment\frontend\Dockerfile") -t $image $root
if ($LASTEXITCODE -ne 0) { throw "Frontend image build failed." }
docker push $image
if ($LASTEXITCODE -ne 0) { throw "Frontend image push failed." }
aws ecs update-service --cluster $Cluster --service $Service --force-new-deployment --region $Region | Out-Host
if ($LASTEXITCODE -ne 0) { throw "ECS frontend deployment failed." }

