[CmdletBinding()]
param(
    [string]$Region = $env:AWS_REGION,
    [string]$Repository = $env:ECR_BACKEND_REPOSITORY,
    [string]$Cluster = $env:ECS_CLUSTER,
    [string]$Service = $env:ECS_BACKEND_SERVICE,
    [string]$ImageTag = $env:IMAGE_TAG
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
docker build -f (Join-Path $root "deployment\backend\Dockerfile") -t $image $root
if ($LASTEXITCODE -ne 0) { throw "Backend image build failed." }
docker push $image
if ($LASTEXITCODE -ne 0) { throw "Backend image push failed." }
aws ecs update-service --cluster $Cluster --service $Service --force-new-deployment --region $Region | Out-Host
if ($LASTEXITCODE -ne 0) { throw "ECS backend deployment failed." }

