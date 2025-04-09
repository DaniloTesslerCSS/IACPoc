param (
    [string]$type,
    [string]$action
)

function DeployInfra {
    param (
        [string]$env,
        [string]$action
    )

    $scriptPath = Split-Path -Parent $MyInvocation.PSCommandPath
    $scriptPath = $scriptPath + "\iac"

    Set-Location $scriptPath

    switch ($action.ToLower())
    {
        "validate"
        {
            Write-Output "Strting stack validation"

            & cdk synth -c env=$env
        }

        "deploy"
        { 
            Write-Output "Strting stack deployment"

            & cdk deploy --all --require-approval never -c env=$env
        }
        
        default 
        { 
            Write-Output "Unknown action."
        }
    }

    Set-Location ".."
}

function DeployCode {
    param (
        [string]$env,
        [string]$action
    )
    

}

$branchName = git rev-parse --abbrev-ref HEAD

switch ($type.ToLower()) 
{
    "infra" 
    { 
        Write-Output "Initiating AWS infraestrucutre deployment based on $branchName branch"
        DeployInfra -env $branchName -action $action  
    }
    
    "code" 
    { 
        Write-Output "Initiating code build and deployment based on $branchName branch"
        #DeployCode -env $branchName -action $action 
        Write-Output "NOT IPLEMENTED" 
    }
    
    default { Write-Output "USE: deploy.ps1 -type [infra|code] -action [deploy|validate]" }
}