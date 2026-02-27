@echo off
REM Generate Test Report - Simple & Reliable
cd /d %~dp0

echo.
echo Running tests...
call mvn clean test

if exist "target\cucumber-reports\cucumber.html" (
    echo.
    echo Opening test report...
    start target\cucumber-reports\cucumber.html
    echo ✅ Report opened in browser
) else (
    echo ❌ Report not found
)

pause

