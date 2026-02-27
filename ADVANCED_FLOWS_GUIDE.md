# Advanced Flows - Failure Analysis & Duplication Checking

## Overview

The framework now includes intelligent flows for:

1. **Test Failure Analysis** - Automatic diagnosis of test failures
2. **Code Duplication Checking** - Pre-execution code quality checks
3. **Framework Integrity Verification** - Ensure framework is ready
4. **Intelligent Suggestions** - AI-powered fix recommendations

---

## New Orchestrators

### Python Advanced Orchestrator
```bash
.venv\Scripts\python.exe advanced_e2e_orchestrator.py \
  "User login and add to cart" \
  -p saucedemo
```

### PowerShell Advanced Demo
```bash
powershell -File .\Run-Advanced-E2E-Demo.ps1 `
  -Project saucedemo `
  -Requirement "User login and add items to cart"
```

---

## STEP 0: PRE-EXECUTION CHECKS

Before running tests, the framework checks:

### 1. Code Duplication Detection
```
CHECKING: Step Definitions
├─ Looking for duplicate step patterns
├─ Identifying shared implementations
└─ Suggesting consolidation

CHECKING: Page Objects
├─ Looking for duplicate locators
├─ Identifying shared elements
└─ Recommending abstraction

RESULT:
├─ Duplication Percentage
├─ Affected Files
└─ Deduplication Suggestions
```

### 2. Framework Integrity
```
CHECKING: Page Files
├─ Count page objects
├─ Verify inheritance
└─ Check naming conventions

CHECKING: Step Files
├─ Count step definitions
├─ Verify annotations
└─ Check implementations

RESULT:
├─ Readiness Status
├─ Issues Found
└─ Recommendations
```

### Example Output
```
[*] Checking for code duplication...

[~] Locator Duplication: 5.2%
  Found 2 duplicate locators
    - Used in 2 locations
    - Used in 3 locations

[OK] Framework ready for execution
```

---

## STEP 4: TEST FAILURE ANALYSIS

### Failure Detection

When tests fail, the framework automatically:

1. **Extracts Error Information**
   - Error type (NoSuchElementException, TimeoutException, etc.)
   - Error message
   - Stack trace analysis

2. **Performs Root Cause Analysis**
   ```
   Error Type: NoSuchElementException
   Cause: Locator not found on page
   Severity: CRITICAL
   ```

3. **Generates Suggestions**
   ```
   Suggested Fixes:
   1. Verify locator selector is correct
   2. Check if element exists in current page context
   3. Update locator in page object
   4. Add wait condition for element to appear
   5. Verify page has loaded completely
   ```

### Error Patterns Recognized

| Error Type | Cause | Suggested Fixes |
|------------|-------|-----------------|
| **NoSuchElementException** | Locator not found | Update locator, add wait, verify page load |
| **StaleElementReferenceException** | DOM refreshed | Re-find element, add wait after action |
| **TimeoutException** | Action too slow | Increase timeout, add visibility wait |
| **AssertionError** | Value mismatch | Update expected, verify test data |
| **ElementNotInteractableException** | Cannot click/type | Scroll, wait clickable, check cover |
| **InvalidElementStateException** | Element disabled | Check enabled state, wait for readiness |

### Example Failure Analysis
```
========================================================================
TEST FAILURE ANALYSIS
========================================================================

Error Type: NoSuchElementException
Severity: CRITICAL
Cause: Locator not found on page

Suggested Fixes:
  1. Verify locator selector is correct
  2. Check if element exists in current page context
  3. Update locator in page object
  4. Add wait condition for element to appear
  5. Verify page has loaded completely

Recommended Actions:
  1. Verify locators are correct and up-to-date
  2. Check if page structure has changed
  3. Update page object with new locators
  4. Re-run test to verify fix
```

---

## DUPLICATION CHECKER

### What It Checks

#### Step Definition Duplication
```
CHECKING: Step Definitions
├─ Finds: @When("I click {string}")
├─ Finds: @When("I click {string}") (DUPLICATE!)
└─ Suggests: Consolidate into single definition
```

#### Locator Duplication
```
CHECKING: Page Objects
├─ Finds: By.id("username") in LoginPage
├─ Finds: By.id("username") in AdminPage (DUPLICATE!)
└─ Suggests: Create shared constant
```

### Deduplication Suggestions

```
=== STEP DEDUPLICATION SUGGESTIONS ===
Found 2 duplicate step definitions

Options:
1. Create shared step definition file
2. Use inheritance for similar steps
3. Create parameterized generic steps
4. Remove redundant step files

=== LOCATOR DEDUPLICATION SUGGESTIONS ===
Found 3 duplicate locators

Options:
1. Create shared locator constants file
2. Use inheritance in page objects
3. Create base page with common locators
4. Use composition for shared elements

⚠️  HIGH DUPLICATION: > 20%
Recommend refactoring to reduce maintenance burden
```

---

## Complete Advanced Flow

### Flow Diagram
```
START
    ↓
[STEP 0] PRE-EXECUTION CHECKS
    ├─ Check code duplication
    ├─ Verify framework integrity
    └─ Generate pre-flight report
    ↓
[STEP 1] START RAG SERVICE
    ├─ Initialize FastAPI server
    └─ Load configuration
    ↓
[STEP 2] GENERATE ARTIFACTS
    ├─ Analyze requirement
    ├─ Detect pages
    └─ Generate features & pages
    ↓
[STEP 3] RUN TESTS
    ├─ Maven clean verify
    ├─ Cucumber executes
    └─ Selenium automates
    ↓
[STEP 4] ANALYZE FAILURES (if any)
    ├─ Extract error information
    ├─ Match error patterns
    ├─ Generate root cause
    └─ Suggest fixes
    ↓
[STEP 5] GENERATE REPORT
    ├─ Create Allure dashboard
    └─ Open in browser
    ↓
END
```

---

## Usage Examples

### Example 1: Complete Advanced Flow
```bash
# PowerShell
powershell -File .\Run-Advanced-E2E-Demo.ps1 `
  -Project saucedemo `
  -Requirement "User login and add to cart"

# Python
.venv\Scripts\python.exe advanced_e2e_orchestrator.py \
  "User login and add to cart" \
  -p saucedemo
```

### Example 2: Skip Pre-Checks
```bash
.venv\Scripts\python.exe advanced_e2e_orchestrator.py \
  "requirement text" \
  -p projectname \
  --skip-checks
```

### Example 3: Custom Framework Path
```bash
.venv\Scripts\python.exe advanced_e2e_orchestrator.py \
  "requirement text" \
  -p projectname \
  -f "D:\DreamProject\reflectioncucumber"
```

---

## Failure Analysis Features

### Intelligent Detection
- Parses test output for error signatures
- Matches against known failure patterns
- Extracts root cause from error message
- Calculates severity level (LOW, MEDIUM, HIGH, CRITICAL)

### Smart Suggestions
- Provides ordered list of potential fixes
- Prioritizes by likelihood
- Includes code examples for common fixes
- Suggests preventive measures

### Actionable Recommendations
- Step-by-step fix procedures
- Code snippets ready to use
- Links to framework documentation
- Suggested next actions

---

## Pre-Execution Check Results

### Healthy Framework
```
[*] Checking for code duplication...

[~] Step Duplication: 0%
    No duplicate steps found

[~] Locator Duplication: 2.1%
    Found 1 duplicate locator

[OK] Framework ready for execution
```

### Issues Detected
```
[*] Checking for code duplication...

[?] Step Duplication: 15%
    Found 3 duplicate step definitions
    - "I click" in 2 files
    - "I enter" in 2 files

[?] Locator Duplication: 18%
    Found 5 duplicate locators

[!] Framework has issues - see above
Recommend refactoring before execution
```

---

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: Run Advanced E2E Tests
  run: |
    cd agent-service
    powershell -File .\Run-Advanced-E2E-Demo.ps1 `
      -Project saucedemo `
      -Requirement "User login scenario"
```

### Jenkins Pipeline Example
```groovy
stage('Advanced Testing') {
    steps {
        dir('agent-service') {
            sh '''
                python advanced_e2e_orchestrator.py \
                  "User login and add to cart" \
                  -p saucedemo
            '''
        }
    }
}
```

---

## Metrics & Reporting

### Pre-Execution Report
- Total files checked
- Duplication percentage
- Severity assessment
- Readiness status

### Failure Analysis Report
- Error type identified
- Root cause analysis
- Severity level
- Recommended fixes

### Overall Quality
- Code duplication metrics
- Test coverage
- Failure patterns
- Trend analysis

---

## Key Benefits

✅ **Automatic Failure Diagnosis** - No manual debugging needed
✅ **Pre-Execution Quality Check** - Catch issues before running
✅ **Code Health Monitoring** - Track duplication trends
✅ **Intelligent Suggestions** - AI-powered fix recommendations
✅ **Framework Integrity** - Verify readiness before execution
✅ **Complete Automation** - All steps orchestrated end-to-end

---

## Next Steps

1. **Run Advanced Flow**
   ```bash
   powershell -File .\Run-Advanced-E2E-Demo.ps1
   ```

2. **Check Pre-Execution Report**
   - Review duplication metrics
   - Check framework integrity
   - Address any issues

3. **Analyze Failures**
   - Review failure analysis
   - Apply suggested fixes
   - Re-run to verify

4. **Monitor Metrics**
   - Track duplication trends
   - Monitor test health
   - Maintain code quality

---

## Commands Quick Reference

```bash
# Run advanced flow (PowerShell)
powershell -File .\Run-Advanced-E2E-Demo.ps1

# Run advanced flow (Python)
.venv\Scripts\python.exe advanced_e2e_orchestrator.py "requirement" -p project

# Skip pre-checks
advanced_e2e_orchestrator.py "requirement" -p project --skip-checks

# Custom framework path
advanced_e2e_orchestrator.py "requirement" -p project -f "path"
```

---

## Summary

The advanced framework now includes:
✅ Intelligent failure analysis
✅ Code duplication checking
✅ Pre-execution verification
✅ Smart fix suggestions
✅ Complete orchestration
✅ Professional reporting

