#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Master Orchestrator - Complete Agentic Test Automation Framework
    Single entry point for all operations

.DESCRIPTION
    Orchestrates: Clean → Test → Report → Serve

.PARAMETER Operation
    full        : Complete flow (clean, test, report, serve)
    test        : Run tests only
    report      : Generate report only
    serve       : Serve existing report
    generate    : Generate from requirement (RAG)

.EXAMPLE
    .\master-agent.ps1 -Operation full
    .\master-agent.ps1 -Operation test
#>

param(
    [ValidateSet('full', 'test', 'report', 'serve', 'generate', 'help')]
    [string]$Operation = 'full',
    [string]$Requirement = '',
    [string]$Project = 'saucedemo'
)

# Configuration
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$TestsCount = 125

# Functions
function Log-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] === $Title ===" -ForegroundColor Cyan
}

function Log-Step {
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] [*] $($args[0])" -ForegroundColor Yellow
}

function Log-Success {
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] [OK] $($args[0])" -ForegroundColor Green
}

function Log-Error {
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] [ERROR] $($args[0])" -ForegroundColor Red
}

function Show-Help {
    Log-Header 'MASTER AGENT - HELP'
    Write-Host @"
OPERATIONS:
  full       : Complete flow - Clean → Test → Report → Serve
  test       : Run tests only (125 tests)
  report     : Generate Allure report from results
  serve      : Serve existing report in browser
  generate   : Generate tests from requirement (RAG)
  help       : Show this help

EXAMPLES:
  .\master-agent.ps1                              # Default: full flow
  .\master-agent.ps1 -Operation test              # Tests only
  .\master-agent.ps1 -Operation generate -Requirement "User login and add items"

WHAT EACH OPERATION DOES:

  full:
    1. Clean build
    2. Compile code
    3. Run 125 tests
    4. Generate Allure report
    5. Serve report in browser

  test:
    • Run all 125 tests
    • Generate test results JSON

  report:
    • Generate Allure dashboard
    • (Requires prior test run)

  serve:
    • Start web server for report
    • Open in default browser

  generate:
    • Generate features from requirement
    • Create page objects with locators
    • (Requires RAG service)

"@
}

function Full-Flow {
    Log-Header 'COMPLETE E2E FLOW'

    # Step 1: Clean
    Log-Step 'Cleaning project'
    Push-Location $ProjectRoot
    mvn clean -q
    Log-Success 'Cleaned'

    # Step 2: Test
    Log-Step "Running $TestsCount tests"
    mvn clean verify
    if ($LASTEXITCODE -ne 0) {
        Log-Error 'Tests failed'
        Pop-Location
        return $false
    }
    Log-Success 'Tests passed'

    # Step 3: Report
    Log-Step 'Generating Allure report'
    mvn allure:report -q
    Log-Success 'Report generated'

    # Step 4: Serve
    Log-Step 'Starting report server'
    Log-Header 'REPORT SERVER STARTED - Browser will open automatically'
    mvn allure:serve

    Pop-Location
    return $true
}

function Test-Only {
    Log-Header 'TEST EXECUTION'
    Log-Step "Running $TestsCount tests"

    Push-Location $ProjectRoot
    mvn clean verify
    $result = $LASTEXITCODE -eq 0
    Pop-Location

    if ($result) {
        Log-Success 'Tests passed'
    } else {
        Log-Error 'Tests failed'
    }

    return $result
}

function Report-Only {
    Log-Header 'REPORT GENERATION'
    Log-Step 'Generating Allure report'

    Push-Location $ProjectRoot
    mvn allure:report
    $result = $LASTEXITCODE -eq 0
    Pop-Location

    if ($result) {
        Log-Success 'Report ready at: target/allure-report/index.html'
    } else {
        Log-Error 'Report generation failed'
    }

    return $result
}

function Serve-Only {
    Log-Header 'SERVING REPORT'
    Log-Step 'Starting web server'

    Push-Location $ProjectRoot
    mvn allure:serve
    Pop-Location
}

function Generate-Mode {
    Log-Header 'RAG GENERATION MODE'

    if ([string]::IsNullOrEmpty($Requirement)) {
        Log-Error 'Requirement text required'
        Write-Host 'Usage: .\master-agent.ps1 -Operation generate -Requirement "Your requirement"'
        return $false
    }

    Log-Step "Requirement: $Requirement"
    Log-Step "Project: $Project"

    Push-Location "$ProjectRoot/agent-service"
    Log-Step 'Generating features and pages...'
    python rag_orchestrator.py generate -r "$Requirement" -p $Project
    $result = $LASTEXITCODE -eq 0
    Pop-Location

    if ($result) {
        Log-Success 'Generation complete'
    } else {
        Log-Error 'Generation failed'
    }

    return $result
}

# Main
Clear-Host
Write-Host "
╔════════════════════════════════════════════════════════╗
║  AGENTIC TEST AUTOMATION FRAMEWORK - MASTER AGENT      ║
║  Complete E2E Orchestration                           ║
╚════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

$success = $false

switch ($Operation) {
    'full' { $success = Full-Flow }
    'test' { $success = Test-Only }
    'report' { $success = Report-Only }
    'serve' { Serve-Only; $success = $true }
    'generate' { $success = Generate-Mode }
    'help' { Show-Help; $success = $true }
}

Log-Header 'STATUS'
if ($success) {
    Write-Host "SUCCESS - All operations completed" -ForegroundColor Green
    Log-Step "Next steps:"
    switch ($Operation) {
        'full' { Write-Host "  • Report opened in browser" }
        'test' { Write-Host "  • Tests completed - Run: .\master-agent.ps1 -Operation report" }
        'report' { Write-Host "  • Report ready - Run: .\master-agent.ps1 -Operation serve" }
        'serve' { Write-Host "  • Report served in browser" }
        'generate' { Write-Host "  • Tests generated - Run: .\master-agent.ps1 -Operation test" }
    }
} else {
    Write-Host "FAILED - Check logs above" -ForegroundColor Red
}

Write-Host ""

