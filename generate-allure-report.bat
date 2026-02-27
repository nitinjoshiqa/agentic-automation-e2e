@echo off
REM Allure Report Generator for Windows
REM This script generates and opens the Allure report in your default browser

cd /d %~dp0

echo.
echo ========================================
echo   Allure Test Report Generator
echo ========================================
echo.

REM Step 1: Run tests
echo [1/3] Running tests...
call mvn clean test -q

if errorlevel 1 (
    echo.
    echo ❌ Tests execution failed!
    echo Please check the logs above for details.
    pause
    exit /b 1
)

echo ✅ Tests completed

REM Step 2: Generate report
echo.
echo [2/3] Generating Allure report...
call mvn allure:report -q

if errorlevel 1 (
    echo.
    echo ❌ Report generation failed!
    echo Please check Maven logs above.
    pause
    exit /b 1
)

echo ✅ Report generated

REM Step 3: Open report
echo.
echo [3/3] Opening report in browser...

if exist "target\site\allure-report\index.html" (
    echo.
    echo ========================================
    echo   ✅ Allure Report Ready!
    echo ========================================
    echo.
    echo Opening in browser...
    start target\site\allure-report\index.html
    echo.
    echo Report: target/site/allure-report/index.html
    echo.
) else (
    echo.
    echo ⚠️  Report folder not found
    echo.
    echo Try running the Allure Serve command:
    echo   mvn allure:serve
    echo.
)

pause

