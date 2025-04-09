$branchName = git rev-parse --abbrev-ref HEAD

# Get the script execution path
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition

#Go one level up
$rootPath = Split-Path -Parent $scriptPath

Set-Location "$($rootPath)\configs"

# Read JSON files
$common = Get-Content -Raw -Path "common.json" | ConvertFrom-Json
$dev = Get-Content -Raw -Path "$($branchName).json" | ConvertFrom-Json

# Merge JSON objects
$merged = [PSCustomObject]@{}
$dev.PSObject.Properties | ForEach-Object { $merged | Add-Member -NotePropertyName $_.Name -NotePropertyValue $_.Value }
$common.PSObject.Properties | ForEach-Object { $merged | Add-Member -NotePropertyName $_.Name -NotePropertyValue $_.Value }

Set-Location "$($rootPath)\app"

& docker build --no-cache -t "$($merged.ProjectName.ToLower())" .

$ecrUrl = "$($merged.Account).dkr.ecr.$($merged.Region).amazonaws.com/$($merged.ProjectName)$($merged.EnvironmentType)$($merged.EnvironmentName)ecrrepo".ToLower()
& aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin "$($merged.Account).dkr.ecr.$($merged.Region).amazonaws.com"
& docker tag "$($merged.ProjectName.ToLower())" $ecrUrl
& docker push $ecrUrl
& aws ecs update-service --cluster "$($merged.ProjectName)$($merged.EnvironmentType)$($merged.EnvironmentName)ecsCluster" --service "$($merged.ProjectName)$($merged.EnvironmentType)$($merged.EnvironmentName)ecsService" --force-new-deployment --desired-count 1 --no-cli-pager

Set-Location $scriptPath
