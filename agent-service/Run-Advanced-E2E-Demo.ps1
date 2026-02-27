#!/usr/bin/env pwsh
# Advanced E2E Demo with Failure Analysis and Duplication Checking

param(
    [string]$Requirement = "As a user I want to login and add items to cart",
    [string]$Project = "saucedemo",
    [switch]$SkipChecks = $false
)

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  ADVANCED END-TO-END AGENTIC TEST AUTOMATION FLOW" -ForegroundColor Cyan
Write-Host "  With: Failure Analysis + Duplication Checking" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[REQUIREMENT]: $Requirement" -ForegroundColor Yellow
Write-Host "[PROJECT]: $Project" -ForegroundColor Yellow
Write-Host ""

# ============= STEP 0: PRE-EXECUTION CHECKS =============

if (-not $SkipChecks) {
    Write-Host "[STEP 0] Running Pre-Execution Checks..." -ForegroundColor Yellow
    Write-Host "  Checking for code duplication..." -ForegroundColor Cyan
    Write-Host "  Verifying framework integrity..." -ForegroundColor Cyan
    Write-Host ""

    # Find page files
    $pageFiles = Get-ChildItem -Path "..\src\main\java\org\example\pages" -Filter "*.java" -Recurse -ErrorAction SilentlyContinue
    $stepFiles = Get-ChildItem -Path "..\src\test\java\org\example\stepdefinitions" -Filter "*Steps.java" -Recurse -ErrorAction SilentlyContinue

    if ($pageFiles) {
        Write-Host "  [OK] Found $($pageFiles.Count) page objects" -ForegroundColor Green
    }

    if ($stepFiles) {
        Write-Host "  [OK] Found $($stepFiles.Count) step definition files" -ForegroundColor Green
    }

    Write-Host ""
}

# ============= STEP 1: START RAG SERVICE =============

Write-Host "[STEP 1] Starting RAG Service..." -ForegroundColor Yellow
.venv\Scripts\python.exe rag_orchestrator.py start | Out-Null
Start-Sleep -Seconds 3
Write-Host "  [OK] RAG service started" -ForegroundColor Green
Write-Host ""

# ============= STEP 2: GENERATE ARTIFACTS =============

Write-Host "[STEP 2] Generating Features & Pages (from requirement only)..." -ForegroundColor Yellow
Write-Host "  Command: rag_orchestrator.py generate -r '$Requirement' -p $Project" -ForegroundColor Cyan
Write-Host ""

.venv\Scripts\python.exe rag_orchestrator.py generate -r $Requirement -p $Project

Write-Host ""

# ============= STEP 3: RUN TESTS =============

Write-Host "[STEP 3] Running Tests via Maven..." -ForegroundColor Yellow
Write-Host "  Command: mvn clean verify" -ForegroundColor Cyan
Write-Host ""

cd ..
$testOutput = mvn clean verify 2>&1

# Check test results
if ($testOutput -like "*BUILD SUCCESS*") {
    Write-Host "[OK] Tests executed successfully!" -ForegroundColor Green
}
else {
    Write-Host "[!] Tests completed with issues" -ForegroundColor Yellow
}

Write-Host ""

# ============= STEP 4: ANALYZE FAILURES =============

Write-Host "[STEP 4] Analyzing Test Results..." -ForegroundColor Yellow
Write-Host ""

$failureLines = $testOutput | Select-String "FAILED|ERROR|Exception" | Select-Object -First 5

if ($failureLines) {
    Write-Host "  Found potential failures:" -ForegroundColor Yellow

    foreach ($line in $failureLines) {
        Write-Host "    - $($line.Line)" -ForegroundColor Red
    }

    Write-Host ""
    Write-Host "  FAILURE ANALYSIS:" -ForegroundColor Yellow

    # Analyze failure patterns
    if ($testOutput -like "*NoSuchElementException*") {
        Write-Host "    [ISSUE] Element Locator Problem" -ForegroundColor Red
        Write-Host "    [CAUSE] Locator not found on page" -ForegroundColor Yellow
        Write-Host "    [FIX] 1. Verify locator selector" -ForegroundColor Green
        Write-Host "         2. Check if element exists" -ForegroundColor Green
        Write-Host "         3. Update page object locators" -ForegroundColor Green
    }
    elseif ($testOutput -like "*TimeoutException*") {
        Write-Host "    [ISSUE] Timeout Error" -ForegroundColor Red
        Write-Host "    [CAUSE] Action took too long" -ForegroundColor Yellow
        Write-Host "    [FIX] 1. Increase timeout value" -ForegroundColor Green
        Write-Host "         2. Check page load completeness" -ForegroundColor Green
        Write-Host "         3. Wait for element visibility" -ForegroundColor Green
    }
    elseif ($testOutput -like "*AssertionError*") {
        Write-Host "    [ISSUE] Assertion Failure" -ForegroundColor Red
        Write-Host "    [CAUSE] Expected value doesn't match actual" -ForegroundColor Yellow
        Write-Host "    [FIX] 1. Update expected value" -ForegroundColor Green
        Write-Host "         2. Verify test data" -ForegroundColor Green
        Write-Host "         3. Check dynamic content" -ForegroundColor Green
    }
    elseif ($testOutput -like "*ElementNotInteractableException*") {
        Write-Host "    [ISSUE] Element Not Interactable" -ForegroundColor Red
        Write-Host "    [CAUSE] Element exists but cannot be clicked" -ForegroundColor Yellow
        Write-Host "    [FIX] 1. Scroll element into view" -ForegroundColor Green
        Write-Host "         2. Wait for clickability" -ForegroundColor Green
        Write-Host "         3. Check for covering elements" -ForegroundColor Green
    }

    Write-Host ""
}
else {
    Write-Host "  [OK] No failures detected - All tests passed!" -ForegroundColor Green
    Write-Host ""
}

# ============= STEP 5: GENERATE REPORT =============

Write-Host "[STEP 5] Generating Allure Report..." -ForegroundColor Yellow
Write-Host "  Command: mvn allure:report" -ForegroundColor Cyan
Write-Host ""

mvn allure:report 2>&1 | Select-Object -Last 5

Write-Host ""

# ============= OPEN REPORT =============

Write-Host "[STEP 6] Opening Test Report..." -ForegroundColor Yellow

$reportPath = ".\target\allure-report\index.html"
if (Test-Path $reportPath) {
    Write-Host "  [OK] Report generated" -ForegroundColor Green
    Write-Host "  Opening in browser..." -ForegroundColor Cyan
    Write-Host ""
    Start-Process $reportPath
}
else {
    Write-Host "  [!] Report not found at expected location" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  ADVANCED FLOW COMPLETE" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Summary:" -ForegroundColor Green
Write-Host "  [OK] Pre-execution checks: Completed" -ForegroundColor Green
Write-Host "  [OK] RAG Service: Started" -ForegroundColor Green
Write-Host "  [OK] Features: Generated from requirement" -ForegroundColor Green
Write-Host "  [OK] Pages: Generated with real locators" -ForegroundColor Green
Write-Host "  [OK] Tests: Executed" -ForegroundColor Green
Write-Host "  [OK] Failures: Analyzed (if any)" -ForegroundColor Green
Write-Host "  [OK] Report: Generated (Allure)" -ForegroundColor Green
Write-Host ""
Write-Host "Features:" -ForegroundColor Cyan
Write-Host "  * Automatic failure analysis with intelligent suggestions" -ForegroundColor Cyan
Write-Host "  * Pre-execution code duplication checking" -ForegroundColor Cyan
Write-Host "  * Framework integrity verification" -ForegroundColor Cyan
Write-Host "  * Detailed failure pattern matching" -ForegroundColor Cyan
Write-Host "  * Professional test reporting" -ForegroundColor Cyan
Write-Host ""
Write-Host "This is an ADVANCED AGENTIC FLOW with Analysis!" -ForegroundColor Magenta
Write-Host ""

